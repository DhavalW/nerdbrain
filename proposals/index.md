# Proposals — not instructions

> **Not instructions. Nothing in this folder governs anything.**

Parked designs. Work that was thought through, agreed to be worth doing, and deliberately
not built yet. It lives here so the reasoning survives the conversation that produced it.

## The one rule

**Nothing here is a rule.** Not a draft rule, not a pending rule, not a rule awaiting
approval. A file in this folder has exactly the authority of a note on a whiteboard: none.

If you are an agent working in this repo:

- **Never load a file here to decide how to work.** The router in
  `../instructions/index.md` is the only list of things that govern, and nothing here is on
  it — by design, not by omission.
- **Never cite one as justification.** "The proposal says to" is not a reason to do
  anything.
- **Never move one into `../instructions/` without an explicit yes**, per item, through the
  normal approval path in `../instructions/learning.md`.
- **Read one only when the user asks you to pick the work up**, by name.

`../tools/check.py` enforces the boundary in both directions: every file here carries the
banner above, and no instruction pack is allowed to reference this folder at all. A pack
that cited a proposal would be the first step in a proposal quietly becoming a rule.

## Why not the ledger

`../memory/observations.md` holds candidate *rules* — one sentence each, waiting on
evidence and a yes. This folder holds candidate *work*: designs too large to be a sentence,
with their tradeoffs, costs and rejected alternatives attached.

Different things, different lifecycles. A ledger entry gets promoted into a pack. A proposal
here gets built, or dropped, and either way the file is the record of why.

## Parked

| Proposal | What it is | Parked because |
|---|---|---|
| `personas.md` | Per-domain critic subagents with isolated context | Deferred — the rest of the system landed first |
| `self-maintenance.md` | Generating what is described as derived, so drift becomes mechanical | Deferred — reports and generators, none of it urgent |
| `approval-channels.md` | A tick-box inbox that outlives the turn, and the two-channel divergence it creates | Built, then backed out — approvals stay in chat while the volume is low |
