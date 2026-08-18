#!/usr/bin/env bash
# Installs this clone's skills for Claude Code, globally.
#
#   git clone https://github.com/dhavalw/nerdbrain.git ~/.nerdbrain
#   ~/.nerdbrain/install.sh
#
# Every directory under skill/ that holds a SKILL.md gets installed, so a new
# skill needs no edit here. Re-run any time. It's idempotent.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$HOME/.claude/skills"

[ -f "$REPO/skill/nerdbrain/SKILL.md" ] || { echo "error: $REPO/skill/nerdbrain/SKILL.md not found — run this from inside the nerdbrain clone" >&2; exit 1; }

mkdir -p "$SKILL_DIR"

INSTALLED=""
for SKILL_SRC in "$REPO"/skill/*/; do
  SKILL_SRC="${SKILL_SRC%/}"
  [ -f "$SKILL_SRC/SKILL.md" ] || continue
  NAME="$(basename "$SKILL_SRC")"
  DST="$SKILL_DIR/$NAME"

  # Replace an existing install, whatever form it took.
  if [ -L "$DST" ] || [ -e "$DST" ]; then
    rm -rf "$DST"
  fi

  if ln -s "$SKILL_SRC" "$DST" 2>/dev/null; then
    HOW="symlinked"
  else
    cp -R "$SKILL_SRC" "$DST"
    HOW="copied (symlink unavailable; re-run after pulling to update)"
  fi

  INSTALLED="$INSTALLED
    /$NAME  →  $DST  ($HOW)"
done

cat <<EOF

  Installed:$INSTALLED
    repo     $REPO

  Load your packs in any project:   /nerdbrain
  Add a rule to the packs:          /update-instructions-in-nerdbrain-repo <rule>
  Rebuild this repo after changes:  /refresh-nerdbrain
  Pin the repo location:            export NERDBRAIN_HOME="$REPO"

EOF

if [ "$REPO" != "$HOME/.nerdbrain" ] && [ -z "${NERDBRAIN_HOME:-}" ]; then
  echo "  Note: the skill looks in \$NERDBRAIN_HOME, then ~/.nerdbrain."
  echo "  This clone is elsewhere — set NERDBRAIN_HOME in your shell profile."
  echo
fi
