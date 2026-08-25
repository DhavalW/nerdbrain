# nerdbrain

An agentic AI brain that learns and self-evolves to work according to your preferences.

## Sync with the original before you start

`DhavalW/nerdbrain` is the original. Every other copy of this repo is a fork, and a fork
falls behind the moment the original moves. Nobody should have to notice that happening.

**Before starting any task here, bring the fork up to date with the original's `main`.**
Session start counts as a start, and so does the beginning of each new task in a long
session. Once per task is enough — don't re-check between turns of the same task, and don't
re-check straight after a sync you just ran.

One command does the whole check:

```
tools/fork-sync.sh check
```

It reads and changes nothing. What it prints decides what happens next:

| Verdict | Means | Do |
|---|---|---|
| `not-a-fork` | `origin` is the original | Nothing, and don't raise it again this session |
| `in-sync` | The branch already has every upstream commit | Start the task |
| `behind:N` | N commits missing, merge is clean | `tools/fork-sync.sh sync`, report in a line, start |
| `dirty-overlap` | Uncommitted edits on files upstream also changed | Stop and ask — see below |
| `conflict` | The merge would collide | Stop and ask — see below |
| `upstream-mismatch` | An `upstream` remote points elsewhere | Stop, ask which repo is the original |
| `fetch-failed` | The original is unreachable | Say so in a line and start the task anyway |

A completed sync is worth one line: how many commits arrived and what they touched. Not a
section, not a walk through the upstream diff. When nothing came down, say nothing.

### Rules the sync never breaks

Upstream `main` is the only thing fetched — no other upstream branch, no tags. If a task
needs something off a different upstream branch, that is a request the user makes, not a
sync.

Nothing flows back up. The fork pulls from the original and never pushes to it, never opens
a pull request against it, never touches its branches. `fork-sync.sh` points the upstream
remote's push URL at a dead scheme, so a stray `git push upstream` fails loudly instead of
succeeding.

Merge, never rebase. A merge commit keeps both histories and leaves every existing checkout
of the fork valid. Rebasing the fork onto upstream rewrites commits people already have,
which is exactly how work gets lost — the thing this instruction exists to prevent. Same
reasoning rules out `push --force`, `reset --hard`, and amending a commit that has been
pushed.

Uncommitted work is never merged over. When the working tree is dirty and none of the dirty
files are ones upstream touched, the script stashes, merges, and restores; the two file sets
don't intersect, so that is safe rather than hopeful. Any overlap at all and it refuses.

Local `main` gets fast-forwarded when it can be and left alone when it can't. A `main`
carrying the fork's own commits is somebody's decision, not drift to be corrected.

### When it conflicts

The verdict names the files. Don't pick a resolution. The fork's changes are somebody's work
and upstream's changes are somebody else's, and from inside the merge you cannot tell which
one the user cares about.

Put it to them in the reply:

1. What upstream changed, one line per conflicting file.
2. What the fork changed in the same file, same shape.
3. The resolutions worth considering — normally take upstream, keep the fork's version, or
   merge the two by hand — with a recommendation where the diff actually supports one.

Then end the turn and wait. No timer, no default, no proceeding because nothing came back.
Nothing is broken while you wait: `fork-sync.sh` aborts the merge and restores the working
tree *before* it reports, so the repo sits exactly where it started.

`dirty-overlap` is the same conversation with a shorter fix — commit or stash the in-flight
edits, then re-run — so name the files that clash and ask.

### If the script isn't there

The protocol is the instruction; the script is only how it gets run. In a checkout that
predates it, do the same thing by hand: add the `upstream` remote, `git fetch --no-tags
upstream main`, read `git rev-list --count HEAD..upstream/main`, and merge with `--no-ff`,
under every rule above.
