# Personas — per-domain critic subagents

> **Not instructions. Nothing in this folder governs anything.**

Parked 2026-08-15, designed but not built. Read `index.md` before acting on any of this.

## The problem it solves

Each domain — copy, security, SEO, UX, design, engineering — should have its own loop for
critiquing, fixing, observing, learning and evolving. When work is happening in a domain,
the agent's context should be focused on that domain and its nuances, and should get there
automatically.

The packs already hold per-domain *knowledge*. What is missing is a per-domain *actor*:
nothing today makes the copy expert critique the copy before the user sees it, and nothing
gives that critique a window free of the other five concerns.

## The mechanism: isolation, not folders

Context isolation is the whole point. A subagent that loads exactly two packs into its own
window produces sharper critique than the same packs competing for attention in a main
window that also holds the project's code, the conversation, and four other domains.

An earlier version of this argument treated the subagent's pack re-read as the cost this
repo exists to avoid. That was wrong in scale: this repo's problem is *many packs in one
window*, and a critic loading two packs into a *separate* window costs the main window
nothing.

## Why not a folder tree

Moving `../instructions/copy.md` to a per-domain folder was considered and rejected. It
breaks 15+ citations, the router table, the gate's pack discovery and the skill, and it buys
co-location of two files. Packs are also not one-to-one with domains: `core`, `planning`,
`reversibility`, `types/*` and `platforms/*` have no critic and never will. Roughly six to
eight packs are domains.

## The shape

One file per persona, packs left where they are:

```
personas/
  _template.md
  copy.md        ->  symlinked to .claude/agents/copy-critic.md
  security.md
  engineering.md
```

Each file is a Claude Code subagent definition plus the five verbs:

```
---
name: copy-critic
description: <the routing trigger>
tools: Read, Grep, Glob        # read-only, always
model: sonnet                  # critique does not need the big model
---
## Loads      the packs this persona reads, and only those
## Critiques  the five questions this domain asks of any work
## Fixes      what it may propose - it never edits
## Observes   what counts as a learning here, and what is just noise
## Evolves    the pack a promotion from this domain lands in
```

`install.sh` already globs `skill/`; it needs one line to also glob `personas/`.

## Where each verb runs

| Verb | Runs in | Reason |
|---|---|---|
| Critique | the subagent | Isolated window; only that domain's packs compete for attention |
| Observe | the subagent | It notices in-domain things a main session holding six concerns misses |
| Fix | the main session | Coherent editing of a shared artifact is where multi-agent reliably fails |
| Learn | the main session | One writer to the ledger; six critics appending in parallel is a conflict a task |
| Evolve | the main session | Promotion needs the user's tick, and no subagent can hold that authority |

Critics *return* candidate observations in their report. The main session dedupes them
against the ledger and writes. Isolation buys focus, not autonomy.

## Routing is already built

No new routing logic is needed. The pack router already computes which domains are in play,
so a persona fires when its packs were loaded and never otherwise. That also caps the noise:
personas cannot all pile onto every task, because the router already decided they were not
relevant.

## Failure modes and their brakes

**Critics manufacture findings.** A reviewer with a mandate to critique will always find
something — the same disease as filler in `../instructions/learning.md`. Every persona file
states the bar, and states that *nothing to flag is a normal result*, in those words.

**Personas drift from their packs.** A persona says it loads `../instructions/copy.md`;
someone splits that pack; the persona now loads half a domain. Extend the gate: `## Loads`
must resolve, and every persona must be inventoried in `../instructions/index.md`.

## Cost

- Six persona files at ~50 lines. Not loaded by any reference session.
- Per critic run: ~200 lines of pack plus the artifact. Parallel, so one run of wall-clock.
- Main-session context: unchanged, and lower than reviewing inline with six packs loaded.
- No change to the ledger format, the always-loaded set, the router table, or any pack path.
- One new gate rule, ~25 lines.

## What would make this wrong

- **Critics only ever agree with the work.** Then they cost tokens for theatre, and plain
  review checklists inside the packs would have been enough.
- **Their observations are consistently thinner than the main session's.** A critic sees the
  artifact, not the conversation where the user corrected something — and those corrections
  are the highest-value learning source in the system.

## When it is picked up

Start with three: `copy`, `security`, `engineering`. Run them for a couple of weeks, then
check the ledger for whose entries actually got promoted. Expanding to six on the strength
of a design argument is how a repo ends up with six things nobody reads.

The open question at parking time: three to start, or all six.
