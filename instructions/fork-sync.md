# Fork sync conflicts

Load when: `tools/fork-sync.sh check` reports `conflict` or `dirty-overlap`. The check
itself, the verdict table and the rules the sync never breaks are in the repo's `CLAUDE.md`
and always apply; this pack is only the part that fires when the merge won't go through on
its own.

## When it conflicts

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

## Carrying out what they chose

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

## What the sync never carries

Four paths are the owner's own and cross in neither direction: `../docs/references/` and
everything in it, `../docs/scrape-list.md`, `../docs/scrape-done.md` and `../docs/wanted.md`.
They are filtered out before the conflict list is built, so they never reach the
conversation above — a clash in one is not a decision anybody should be asked to make, and
`fork-sync.sh` settles it by keeping this clone's version.

Two consequences worth knowing rather than rediscovering. A file the original *added* under
one of those paths is removed from the merge rather than adopted, which is what stops an
upstream capture queue reaching a crawler that would act on it. And a `plan` that lists
nothing while `check` said `conflict` cannot happen — the verdict is computed from the same
filtered list.

## If the script isn't there

The protocol is the instruction; the script is only how it gets run. In a checkout that
predates it, do the same thing by hand: add the `upstream` remote, `git fetch --no-tags
upstream main`, read `git rev-list --count HEAD..upstream/main`, and merge with `--no-ff`,
under every rule above — then put back this clone's own copy of the four local-only paths,
which is the one step a plain `git merge` will not do for you.
