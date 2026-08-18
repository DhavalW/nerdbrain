# Self-maintenance — drift and duplication

> **Not instructions. Nothing in this folder governs anything.**

Parked 2026-08-15, designed but not built. Read `index.md` before acting on any of this.

## The root cause

**A gate can only catch drift between a source and a derivation if there is a generation
step.** Several things in this repo are *described* as derived but are hand-written, and the
gate checks only that they exist — never that they still say the right thing.

That is why `/refresh-nerdbrain` needs human judgement for work a script should own, and it is
the single idea behind everything below.

## A. Generate the router row and inventory line

The highest-value item, and the only one that removes a class of drift rather than reporting
on it.

Today `../tools/check.py` rule 4 checks that a pack's filename appears somewhere in
`../instructions/index.md`. A pack can be rewritten from scratch and its inventory line will
still pass, because nothing compares the line to the pack.

- **Source:** each pack's `Load when:` line. Most packs already have one.
- **Generator:** extend `../tools/autoindex.py` to emit the router row and the inventory line
  from it.
- **Gate:** compare generated against committed, the way the capture indexes are already
  tallied against their folders.
- **Cost:** ~60 lines of Python. No new files, no format change.

Packs with no `Load when:` line would need one — that is the real work, and it is worth it
on its own, because a pack with no stated trigger is a pack the router is guessing about.

## B. Near-duplicate reporter

Nothing detects the same rule stated in two packs and then drifting apart as one is edited.

- Normalize sentences, shingle them, report pairs above a similarity threshold.
- ~40 lines using `difflib`. Pure stdlib, consistent with the rest of `../tools/`.
- **Report only, never a gate failure.** Deliberate duplication is legitimate here —
  `../CLAUDE.md` states the ledger rule twice on purpose, once per mode. A gate that fails on
  it would be wrong, and the fix would be to delete a rule that should stay.
- Lands in `../tools/staleness.py`, which is already the home for "needs judgement".

## C. Dead-rule detection, for free

A rule nothing ever fires is dead weight, and dead weight is what makes long instruction
files stop being followed.

There is no usage data today. The obvious fix — log which packs load on each task — costs a
write every task and produces merge conflicts on a file every session touches.

The free proxy is already in the repo: **a pack that has never been the `Target` of a ledger
entry, and whose file has not changed in six months, is a pack nothing has learned from.**
Zero new writes, derived entirely from `../memory/observations.md` and git.

Add real load-logging only if that proves too coarse to act on.

## D. Contradiction sweep

"These two packs disagree" is not detectable without semantics, so this is the one item that
needs a model and therefore a credential.

- Monthly, as a sibling to the existing weekly promotion job.
- **Opens an issue, not a pull request.** A contradiction needs a decision about which side
  is right; a PR would imply the fix is already known.
- Degrades to nothing without the credential, same as every other scheduled thing here.

## E. Generate any approval surface from the ledger

Only relevant if `approval-channels.md` is ever revived. A surface hand-written by whichever
session raises an entry can drift from the ledger; one generated from it cannot, for exactly
the reason A gives. Same machinery, so the two would be built together or not at all.

## Order

A first — it is the only item that removes a class of drift rather than reporting on it.
Then B and C, which are reports. D costs money and needs a human at the other end anyway. E
does not exist as work until something revives the surface it would generate.
