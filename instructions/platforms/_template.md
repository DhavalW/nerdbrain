# <Platform Name>

Template for a new platform pack. Copy, fill in, delete what doesn't apply, add the row to
`../index.md`. Keep it under ~100 lines — a pack that's too long to load defeats the point.

Write for the reader who has to make a decision, not for the reader who wants a tutorial.
Anything the vendor's docs already say well, point at instead of restating.

---

Load when: <the specific trigger — "payments via X", "hosting on Y">.

Docs: `../../docs/references/<platform>/<source>_*.pdf` — exact dated filename and page map
live in the index beside the PDFs, which `../../docs/index.md` routes you to. Cite by source
prefix, never the exact name, and cite **topics by name, never page numbers** — both change
on every refresh; the agent resolves topic → pages in that index at read time. / No local
snapshot — verify against <url> (`../research.md`).

## What it is

Two or three lines. What problem it solves, what it replaces.

## When to use it, when not to

- Good at: <the cases where it's clearly right>
- Bad at: <the cases where it fails, and the honest disqualifiers>
- The alternative you'd compare it against: <what, and the deciding factor>

State the disqualifiers plainly. A pack that only lists strengths is marketing.

## Cost model

- What's free, what's metered, **which limit gets hit first**
- What the architecture should do to stay under it
- Verified on <date> from <where>, or marked unverified

## Key concepts

Only the ones that change how you'd build. Skip the tour.

## Gotchas

The things that cost an afternoon. This is usually the most valuable section:

- Behavior that contradicts the obvious expectation
- Silent failures, eventual consistency, surprising defaults
- Anything that changed in a recent major version
- The thing everyone gets wrong the first time

## Security notes

- Where the secret lives, and whether it can ever be client-side
- What must be verified server-side
- Webhook signature verification, if applicable

## Doc page map

| Topic | Pages |
|---|---|
| <topic> | <n–m> |

## Checklist

- [ ] <the things that must be true before shipping on this platform>
