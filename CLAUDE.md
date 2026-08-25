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
| `conflict` | The merge would collide | `plan`, then ask — see below |
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

Both sides changed the same lines and nothing decides which is right. Don't guess. The fork's
change is somebody's deliberate work and the original's change is somebody else's, and from
inside the merge neither looks more important than the other.

Get the evidence first — this reads and starts nothing:

```
tools/fork-sync.sh plan
```

It prints, for every clashing file, which upstream commits touched it and why, which of the
fork's commits touched it and why, and both diffs.

Then put it to the user **one file at a time**, because different files often want different
answers. For each: what the original was trying to do, what the fork was trying to do, two or
three ways to reconcile them that actually fit this clash, and which one you'd pick and why.

The approaches to draw from:

| Approach | What happens | What it costs |
|---|---|---|
| Take the original's version | The fork's change to that file is dropped | You lose that change. Fine when it was incidental, or the original has since done the same thing better |
| Keep the fork's version | The original's change to that file is dropped | You lose whatever the original fixed, and the same clash returns every time it touches that file again |
| Combine them by hand | Both changes survive | Real work, and it needs someone who understands both sides. Usually right when the two are doing different things that happen to sit close together |
| Take the original, then redo the fork's change on top of it | Both survive, and the fork's change now fits the new code | More work than combining, and the only one that holds when the original reorganised the area |
| Move the fork's change somewhere it can't collide | The clash stops coming back | A small redesign now instead of paying the same tax at every sync |
| Leave the sync for later | Nothing changes | The gap grows and the next conflict is bigger. Only reasonable mid-task |

Write all of it in the user's language, not git's. "The original raised the network timeout to
90 seconds; this fork lowered it to 10 on purpose, so one of those has to give" beats a diff,
and a recommendation without its reason attached is worth nothing.

Then end the turn and wait. No timer, no default, no proceeding because nothing came back.
Nothing is broken while you wait: `plan` never starts a merge, and every command that does
abort it before reporting.

### Carrying out what they chose

The sync isn't finished when the question is answered. Answer, then do it.

```
tools/fork-sync.sh resolve config.ini=manual strings.yml=upstream legacy.txt=fork
```

`upstream` takes the original's copy of that file, `fork` keeps this fork's, `manual` leaves it
for you. Every conflicting file needs a choice — leave one out and the command refuses and
commits nothing. The working tree has to be clean first, because hand-merging on top of
uncommitted edits is the mess this whole protocol exists to avoid.

For each `manual` file, write the reconciled version yourself: both intents, exactly as agreed,
and nothing else. No tidying, no reformatting, no fixing the unrelated thing you noticed two
lines down. Then `git add` it and finish:

```
tools/fork-sync.sh resolve --continue
```

That refuses while a conflict marker survives anywhere, commits the merge with the per-file
decisions recorded in its message, and fast-forwards local `main`. Run `check` again afterwards
— the job is done when it says `in-sync`, not when the merge commits.

Two things end the run rather than continue it. If an approach turns out to be impossible once
you are in the file — the original deleted the function the fork's change lived in — run
`tools/fork-sync.sh resolve --abort` and go back to the user with what you found; never
substitute a different approach because it was nearby. And if their answer doesn't cover every
clashing file, ask about the rest before starting.

Report what landed in a line per file, then get on with the task that was actually asked for.

`dirty-overlap` is the same conversation with a shorter fix. The clash is with edits that were
never committed, so name the files and offer to commit them, stash them, or leave the sync for
later.

### If the script isn't there

The protocol is the instruction; the script is only how it gets run. In a checkout that
predates it, do the same thing by hand: add the `upstream` remote, `git fetch --no-tags
upstream main`, read `git rev-list --count HEAD..upstream/main`, and merge with `--no-ff`,
under every rule above.
