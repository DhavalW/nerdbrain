# Memory

The ledger. The packs hold durable rules; this holds the evidence that produces them —
observations written down as they happen, before anyone knows whether they will hold.

- `observations.md` — the live ledger.
- `archive.md` — entries that are finished: shipped into a pack, or declined and gone quiet.

## Why this exists

A lesson is cheapest to capture at the moment it happens and gone by the next session
(`../instructions/learning.md`). Without somewhere to put one, every observation not
approved in the session that saw it was discarded — so a first sighting could never become
a second, a rule declined in March came back in June as if new, and a proposal made to a
user who had stepped away was simply lost.

**An entry here governs nothing.** It is a note, not a rule: no agent's behavior changes
because something is written down here. That is exactly why writing one needs no approval,
and why promoting one into a pack still needs an explicit yes.

## Who writes to it

Any session, at the end of a task, as part of `../instructions/learning.md`. Appending is
free and needs no permission. Two things are still forbidden:

- **Never record a secret.** Keys, tokens, connection strings, private hostnames, customer
  data. The full rule is in `../instructions/learning.md` and it applies here without
  exception — this file is the likeliest place for one to land, because an observation
  arrives attached to the real thing that proved it.
- **Never edit a pack from here.** Promotion is a separate, approved step. An agent that
  reads an `open` entry and acts on it has skipped the gate.

## The entry format

Fixed, because a scheduled job parses it. Four fields, in this order, under a heading that
carries the id and the date it was first seen:

```
### obs-0042 — 2026-08-12
- **Observation:** One sentence, imperative, generalized past the project that produced it.
- **Rests on:** seen once (2026-08-12)
- **Target:** `../instructions/shipping.md`
- **Status:** open
```

- **Observation** — the rule as it would be written, not the story of what happened. Strip
  the app, keep the shape (`../instructions/learning.md`).
- **Rests on** — `stated outright`, `seen once`, or `seen N times`, each followed by the
  dates in brackets. This is the field that makes the ledger worth having: it is the
  difference between a guess and a case.
- **Target** — the pack it would land in, as a backticked path. `unplaced` when no pack
  covers the subject and the promotion would create one.
- **Status** — `open`, `proposed`, `shipped`, or `declined`. Nothing else.

One optional field may follow them:

- **Last raised** — `YYYY-MM-DD`, the day the entry was put to the user in conversation.
  It resets the clock in `../tools/staleness.py`, and it is the only thing stopping a
  session raising the same three proposals at the end of every task.

`../tools/check.py` enforces the shape: unique ids, the four fields in order, a known
status, a target that resolves, and a real date if `Last raised` is there.

## Two ways an entry gets promoted

Both end in the user saying yes to a specific item. Neither one is allowed to skip that.

**The weekly run**, when a credential is configured. It drafts the pack edits and opens a
PR; merging is the yes, closing is the no.

**A session, in conversation**, when nothing else picked the entry up. `staleness.py`
reports ripe `open` entries that have sat for ten days or more, and any session finishing
a task with this repo in context raises those directly
(`../instructions/learning.md`). This is the path that runs in a fresh clone with no
secret configured, and it is why the loop closes either way. Those are raised in the nerdbrain
approvals block, whose fixed layout makes the ask answerable at a glance
(`../instructions/profile.md`).

## The lifecycle

**open** → written by a session, waiting for evidence or for someone to pick it up.

**proposed** → a promotion run has opened a PR carrying the pack edit. The status flip
rides in that same PR, so the ledger and the proposal are never out of step.

**shipped** → approved and written into a pack. From the weekly run that means the PR was
merged — **merging is the yes**, per item: drop the commits you don't want and merge the
rest. From a session it means the user said yes in conversation and
`/update-instructions-in-nerdbrain-repo` wrote it.

**declined** → refused. The weekly run reconciles its own closed PRs before drafting
anything new, so a no is recorded once and never re-proposed; a no given in conversation
is written straight to the entry. If the same thing happens again, a new entry says it is
the second time — the one case `../instructions/learning.md` allows re-raising a declined
rule.

Silence is not either answer. An entry the user didn't respond to stays `open` with its
`Last raised` date set, which delays it rather than dropping it.

Entries seen again before promotion don't get a second line. Bump the count and add the
date to **Rests on** — that accumulation is the whole point.

## Archiving

`shipped` and `declined` entries move to `archive.md` once they stop being useful context.
Nothing is deleted: a declined entry is the record that stops it being re-proposed, and
deleting it re-opens the loop it closed. The archive is not read on the normal path, so it
can grow.

## What this is not

Not a log of what sessions did — that is what git history is for. Not a place for facts
about one project, which belong in that project's own docs. Not a queue of work. If an
entry doesn't read as a candidate rule that would still make sense in an unrelated project
two years from now, it belongs somewhere else or nowhere.
