# Approval channels that outlive the turn

> **Not instructions. Nothing in this folder governs anything.**

Parked 2026-08-15. Built once, then backed out unbuilt — approvals stay in chat for now.
Read `index.md` before acting on any of this.

## The problem

An approval asked in a reply dies with the reply. The user reads the report on a phone,
means to come back to it, and the turn ends. The weekly promotion PR solves this, but only
with a credential configured, and only once a week.

## What was designed

A file at memory/inbox.md, holding one entry per pending approval as two checkboxes —
`promote` and `drop`, both blank meaning still waiting. Ticked in an editor, or from a phone
against a mirrored GitHub issue where task lists render as real clickable boxes. A later
session reads the ticks, applies them, and clears the item.

Verified along the way: a hosted page cannot do this job. The artifact runtime available
here offers no persistent state, so a checkbox page could render but never return the answer
to a session. An approval surface that cannot be read back is not a surface.

## Why it was backed out

Two mechanisms for one decision is one too many while the volume is this low. Chat asks
already reach the user; what they lacked was a fixed shape, and that shipped instead — the
approvals block in `../instructions/profile.md`. Ledger entries that go unanswered stay
`open`, keep collecting evidence, and are re-raised on the ten-day clock, so nothing is lost
by an unanswered ask. That is the property the inbox was meant to provide, and the ledger
already had it.

## The part that was real, and would come back with it

Two approval channels running at once diverge, and the divergence is silent:

- An entry `open` in the inbox is also eligible for the weekly PR. Tick the box, merge the
  PR, and the same rule lands in the pack twice.
- Tick `drop` while the PR is open, then merge it: two contradictory answers, no defined
  winner.
- Close the PR (a no) with the item still in the inbox: a later tick re-opens a closed
  decision.
- Two open promotion PRs edit the same packs and flip status lines in the same file — a
  hand-resolved conflict for no benefit.

The fixes, if this is ever revived: **one entry belongs to exactly one channel, and the
ledger's Status field says which** — `open` means the conversational channel, `proposed`
means an open PR owns it. The weekly job excludes ids already raised; it stops rather than
opening a second PR while one is open; it deletes items for entries it decided; it rebases
before pushing. A gate rule enforces that no decided entry sits in the inbox.

Two of those stand on their own even with no inbox — never two open promotion PRs, and
rebase before pushing — and could be proposed separately as ordinary PR hygiene.

## What would have to change to revive it

Volume. At a handful of pending items the block is easier to answer than a file is to open.
When the ledger routinely carries ten ripe entries and the block can only show three, the
overflow needs somewhere to live, and this is that somewhere.
