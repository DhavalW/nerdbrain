#!/usr/bin/env bash
#
# Keep a fork of DhavalW/nerdbrain current with the original's main branch.
#
#   tools/fork-sync.sh check    read-only: what state is this clone in?
#   tools/fork-sync.sh sync     bring upstream main in, when the merge is clean
#   tools/fork-sync.sh plan     read-only: both sides of every clash, to explain to a person
#   tools/fork-sync.sh resolve FILE=upstream|fork|manual ...   carry out a chosen resolution
#   tools/fork-sync.sh resolve --continue | --abort
#
# Exit 0 = nothing needed, or the sync succeeded.
# Exit 1 = the user has to decide something. Stop and ask.
# Exit 2 = the script could not run.
#
# It never pushes anywhere, never rebases, and never rewrites history. The protocol
# it implements — including what to do with each verdict — is in CLAUDE.md.

set -uo pipefail

UPSTREAM_URL="${NERDBRAIN_UPSTREAM:-https://github.com/DhavalW/nerdbrain}"
UPSTREAM_REF="refs/remotes/upstream/main"

say() { printf '%s\n' "$*"; }
verdict() { printf 'status: %s\n' "$1"; }
indent() { sed 's/^/  /'; }

# github.com/Owner/Repo.git, git@github.com:Owner/Repo and https://…/Repo/ compare equal.
normalize() {
  printf '%s' "$1" \
    | sed -e 's#^git@\([^:]*\):#\1/#' \
          -e 's#^[a-z+]*://##' \
          -e 's#^[^@/]*@##' \
          -e 's#\.git$##' \
          -e 's#/*$##' \
    | tr '[:upper:]' '[:lower:]'
}

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || { verdict error; say "not inside a git work tree"; exit 2; }
cd "$ROOT" || exit 2

BRANCH="$(git symbolic-ref --quiet --short HEAD)" || {
  verdict error; say "HEAD is detached. Check out a branch before syncing."; exit 2
}

ORIGIN="$(git config --get remote.origin.url || true)"
[ -n "$ORIGIN" ] || { verdict error; say "no origin remote"; exit 2; }


CHOICES="$(git rev-parse --git-dir)/fork-sync-choices"

# During a merge, git's "ours" is this fork and "theirs" is the original. Nobody remembers
# which way round that goes, so the choices are spelled fork= and upstream= instead.
take_side() { # take_side <path> <HEAD|MERGE_HEAD>
  local path="$1" src="$2"
  if git cat-file -e "$src:$path" 2>/dev/null; then
    mkdir -p "$(dirname "$path")"
    git show "$src:$path" > "$path" || return 1
    git add -- "$path"
  else
    git rm -q --force --ignore-unmatch -- "$path"   # that side deleted it
  fi
}

finish_merge() {
  local unresolved marked
  unresolved="$(git diff --name-only --diff-filter=U)"
  if [ -n "$unresolved" ]; then
    verdict unresolved
    say "Still conflicted, so nothing was committed:"
    printf '%s\n' "$unresolved" | indent
    say "Edit them, 'git add' each one, then: tools/fork-sync.sh resolve --continue"
    exit 1
  fi
  marked="$(git grep -l --cached -e '^<<<<<<< ' -e '^>>>>>>> ' 2>/dev/null)"
  if [ -n "$marked" ]; then
    verdict unresolved
    say "Conflict markers are still in the staged copy of:"
    printf '%s\n' "$marked" | indent
    say "A hand-merge is not finished until the markers are gone. Nothing was committed."
    exit 1
  fi
  local decided=""
  [ -f "$CHOICES" ] && decided="$(tr '\n' ' ' < "$CHOICES")"
  git commit -q --no-edit -m "Merge upstream main into $BRANCH" \
    ${decided:+-m "Resolved: $decided"} || {
      verdict error; say "merge commit failed"; exit 2; }
  rm -f "$CHOICES"
  say "merge committed${decided:+ — resolved: $decided}"
  if [ "$BRANCH" != "main" ] && git show-ref --verify --quiet refs/heads/main; then
    if git fetch . "$UPSTREAM_REF:refs/heads/main" >/dev/null 2>&1; then
      say "fast-forwarded local main to upstream main"
    else
      say "local main carries its own commits; left untouched"
    fi
  fi
  verdict synced
  exit 0
}

# --continue and --abort run mid-merge: no fetch, no recomputing anything.
if [ "${1:-}" = "resolve" ]; then
  case "${2:-}" in
    --continue)
      git rev-parse --verify -q MERGE_HEAD >/dev/null || {
        verdict error; say "no merge in progress"; exit 2; }
      finish_merge
      ;;
    --abort)
      git merge --abort 2>/dev/null
      rm -f "$CHOICES"
      verdict aborted
      say "merge abandoned, working tree back where it started"
      exit 0
      ;;
  esac
fi

if [ "$(normalize "$ORIGIN")" = "$(normalize "$UPSTREAM_URL")" ]; then
  verdict not-a-fork
  say "origin is the original ($ORIGIN). Nothing to sync."
  exit 0
fi

# An upstream remote pointing elsewhere was set deliberately. Leave it alone and ask.
EXISTING="$(git config --get remote.upstream.url || true)"
if [ -z "$EXISTING" ]; then
  git remote add upstream "$UPSTREAM_URL" || { verdict error; say "could not add upstream remote"; exit 2; }
  say "added remote upstream -> $UPSTREAM_URL"
elif [ "$(normalize "$EXISTING")" != "$(normalize "$UPSTREAM_URL")" ]; then
  verdict upstream-mismatch
  say "remote 'upstream' points at $EXISTING, not $UPSTREAM_URL"
  say "Not rewriting a remote someone set on purpose. Ask which one is the original."
  exit 1
fi
# Belt and braces: nothing this repo does can push to the original.
git remote set-url --push upstream no-push://fork-sync-is-one-way 2>/dev/null

# main, and only main, and only ever in this direction.
if ! FETCH_LOG="$(git fetch --no-tags upstream "+refs/heads/main:$UPSTREAM_REF" 2>&1)"; then
  verdict fetch-failed
  say "could not reach $UPSTREAM_URL:"
  printf '%s\n' "$FETCH_LOG" | indent
  exit 0
fi

BEHIND="$(git rev-list --count "HEAD..$UPSTREAM_REF")"
if [ "$BEHIND" = "0" ]; then
  verdict in-sync
  say "$BRANCH already contains every commit on upstream main."
  exit 0
fi

incoming_commits() {
  say ""
  say "$BEHIND commit(s) on upstream main are missing from $BRANCH:"
  git log --oneline --no-decorate "HEAD..$UPSTREAM_REF" | indent
}

INCOMING="$(git diff --name-only "HEAD...$UPSTREAM_REF")"
DIRTY="$(git status --porcelain --untracked-files=no | cut -c4- | sed 's/.* -> //')"
OVERLAP="$(comm -12 <(printf '%s\n' "$INCOMING" | sort -u) <(printf '%s\n' "$DIRTY" | sort -u) | sed '/^$/d')"

# A dry run: writes no ref, touches no working tree. Exit 1 means the merge would conflict.
MT="$(git merge-tree --write-tree --name-only HEAD "$UPSTREAM_REF" 2>/dev/null)"
MT_RC=$?
CONFLICTS="$(printf '%s\n' "$MT" | tail -n +2 | sed -n '/^$/q;p')"

case "${1:-check}" in
  check)
    if [ -n "$OVERLAP" ]; then
      verdict dirty-overlap
      incoming_commits
      say ""
      say "Uncommitted edits sit on files the upstream change also touches:"
      printf '%s\n' "$OVERLAP" | indent
      exit 1
    fi
    if [ "$MT_RC" -ne 0 ]; then
      verdict conflict
      incoming_commits
      say ""
      say "The merge would conflict in:"
      printf '%s\n' "$CONFLICTS" | indent
      exit 1
    fi
    verdict "behind:$BEHIND"
    incoming_commits
    say ""
    say "Merge is clean. Run: tools/fork-sync.sh sync"
    exit 0
    ;;

  sync)
    if [ -n "$OVERLAP" ]; then
      verdict dirty-overlap
      say "Refusing to merge over uncommitted edits to:"
      printf '%s\n' "$OVERLAP" | indent
      exit 1
    fi

    STASHED=no
    if [ -n "$(git status --porcelain)" ]; then
      if git stash push --include-untracked \
           --message "fork-sync $(date -u +%Y-%m-%dT%H:%M:%SZ)" >/dev/null 2>&1; then
        STASHED=yes
        say "stashed uncommitted work — none of it on incoming files"
      fi
    fi

    if git merge --no-ff --no-edit -m "Merge upstream main into $BRANCH" "$UPSTREAM_REF" >/dev/null; then
      say "merged $BEHIND commit(s) from upstream main"
    else
      BLOCKED="$(git diff --name-only --diff-filter=U)"
      git merge --abort 2>/dev/null
      [ "$STASHED" = yes ] && git stash pop >/dev/null 2>&1
      verdict conflict
      say "Merge aborted and the working tree put back. Conflicting files:"
      printf '%s\n' "${BLOCKED:-$CONFLICTS}" | indent
      exit 1
    fi

    if [ "$STASHED" = yes ] && ! git stash pop >/dev/null 2>&1; then
      verdict stash-conflict
      say "Merge landed, but restoring the stash conflicted."
      say "Nothing is lost — the work is the top entry of: git stash list"
      exit 1
    fi

    # Keep local main honest too, but only where that costs nothing.
    if [ "$BRANCH" != "main" ] && git show-ref --verify --quiet refs/heads/main; then
      if git fetch . "$UPSTREAM_REF:refs/heads/main" >/dev/null 2>&1; then
        say "fast-forwarded local main to upstream main"
      else
        say "local main carries its own commits; left untouched"
      fi
    fi

    verdict synced
    exit 0
    ;;

  # Read-only: the evidence needed to explain the clash to a person.
  plan)
    if [ "$MT_RC" -eq 0 ] && [ -z "$OVERLAP" ]; then
      verdict behind:"$BEHIND"
      say "Nothing to reconcile — this merge is clean. Run: tools/fork-sync.sh sync"
      exit 0
    fi
    BASE="$(git merge-base HEAD "$UPSTREAM_REF")"
    verdict plan
    incoming_commits
    OLD_IFS="$IFS"; IFS=$'\n'
    for f in $CONFLICTS $OVERLAP; do
      say ""
      say "=== $f ==="
      say ""
      say "  the original changed it in:"
      git log --oneline --no-decorate "$BASE..$UPSTREAM_REF" -- "$f" | sed 's/^/    /'
      git diff --stat "$BASE" "$UPSTREAM_REF" -- "$f" | sed 's/^/    /'
      say ""
      say "  this fork changed it in:"
      git log --oneline --no-decorate "$BASE..HEAD" -- "$f" | sed 's/^/    /'
      git diff --stat "$BASE" HEAD -- "$f" | sed 's/^/    /'
      say ""
      say "  --- what the original did ---"
      git diff "$BASE" "$UPSTREAM_REF" -- "$f" | tail -n +5 | head -60 | indent
      say "  --- what this fork did ---"
      git diff "$BASE" HEAD -- "$f" | tail -n +5 | head -60 | indent
    done
    IFS="$OLD_IFS"
    say ""
    say "Diffs are capped at 60 lines each; use git diff $BASE..$UPSTREAM_REF -- <file> for the rest."
    exit 0
    ;;

  # Carry out a resolution the user chose: resolve FILE=upstream FILE=fork FILE=manual
  resolve)
    shift
    [ $# -gt 0 ] || { verdict error; say "usage: resolve FILE=upstream|fork|manual ..."; exit 2; }
    if [ -n "$(git status --porcelain)" ] && ! git rev-parse --verify -q MERGE_HEAD >/dev/null; then
      verdict error
      say "Working tree is not clean. Commit or stash before resolving — a hand-merge on top"
      say "of uncommitted edits is the case this script exists to avoid."
      exit 2
    fi

    if ! git rev-parse --verify -q MERGE_HEAD >/dev/null; then
      git merge --no-ff --no-commit "$UPSTREAM_REF" >/dev/null 2>&1
    fi

    UNMERGED="$(git diff --name-only --diff-filter=U)"
    : > "$CHOICES"
    for arg in "$@"; do
      f="${arg%%=*}"; side="${arg#*=}"
      case "$side" in
        upstream) take_side "$f" MERGE_HEAD || { verdict error; say "could not take upstream $f"; exit 2; }; say "$f <- the original" ;;
        fork)     take_side "$f" HEAD       || { verdict error; say "could not keep fork $f";     exit 2; }; say "$f <- this fork" ;;
        manual)   say "$f <- left for a hand-merge" ;;
        *) verdict error; say "unknown choice '$side' for $f — use upstream, fork or manual"; exit 2 ;;
      esac
      printf '%s=%s\n' "$f" "$side" >> "$CHOICES"
    done

    # Every conflicted file needs a decision. Silence is not one.
    MISSING=""
    OLD_IFS="$IFS"; IFS=$'\n'
    for f in $UNMERGED; do
      grep -qF "$f=" "$CHOICES" || MISSING="$MISSING$f"$'\n'
    done
    IFS="$OLD_IFS"
    if [ -n "$MISSING" ]; then
      verdict undecided
      say "These are conflicted and were not given a choice, so nothing was committed:"
      printf '%s' "$MISSING" | indent
      say "Re-run with a choice for each, or: tools/fork-sync.sh resolve --abort"
      exit 1
    fi

    finish_merge
    ;;


  *)
    verdict error
    say "usage: tools/fork-sync.sh check | sync | plan"
    say "       tools/fork-sync.sh resolve FILE=upstream|fork|manual ... | --continue | --abort"
    exit 2
    ;;
esac
