# Documentation

Load when: making any change worth documenting — features, architecture, data model,
decisions, operational procedures. In practice: most non-trivial work.

The standard: **docs are part of the change, not a follow-up.** A change isn't done until
the docs that describe the affected part are true again. "Update docs later" means never.

## Where docs live

Modular files in the project's `docs/` folder — one file per concern, each small enough to
read in a few minutes. Not one growing `ARCHITECTURE.md` that nobody dares touch.

```
docs/
  README.md            index: what each doc covers, one line each
  architecture.md      system shape, boundaries, where data lives, + diagram
  data-model.md        collections/tables, key fields, relations, + diagram
  flows/               one file per non-obvious flow (auth.md, redemption.md, sync.md)
  operations.md        deploy, backup/restore, env vars, monitoring, the runbook
  decisions.md         what was chosen and why, plus assumptions logged mid-build
  archive/             superseded versions — see below
```

Adjust names to the project; keep the shape: an index, small single-purpose files, an
archive. `decisions.md` is where a checkpoint answer lands once given (`core.md`): the
question, the options, what was picked, and why. Chat scrollback is where questions are
*asked*; this file is what survives the session. Assumptions taken mid-build land here too,
marked `ASSUMED` until the user confirms or overrides them — that mark is what makes them
findable when they come back to review.

Every doc starts with two lines of front matter:

```
Updated: 2026-08-09
Covers: how records sync between the client cache and the server
```

## Diagrams

Use a diagram when structure or flow is the point — architecture, data model, state
machines, anything with more than three moving parts. Prose describing a graph is worse
than the graph.

- **Mermaid in the markdown.** Diffable, renders on GitHub, no binary files, no export
  step, and an agent can update it like any other text. Draw.io/PNG exports go stale the
  moment the source file is lost.
- One diagram per concern: system context, data model (ER), a sequence diagram per
  non-obvious flow. Not one mega-diagram of everything.
- The diagram must match the code *now*. A stale diagram is worse than none — it's
  confidently wrong. Diagrams are part of the same update rule as prose.
- Keep them small enough to update without dread. If a diagram is painful to maintain,
  split it.

## Keeping docs current

When these change, the matching doc changes in the same commit:

| Change | Update |
|---|---|
| Architecture, service boundaries, where data lives | `architecture.md` + diagram |
| Schema, collections, relations, access rules | `data-model.md` + diagram |
| A user-visible or non-obvious flow | the flow's file |
| Env vars, deploy steps, backup, monitoring | `operations.md` (and `.env.example`) |
| A change with a rollback path — migrations, data, external state | `operations.md` runbook (see `reversibility.md`) |
| A checkpoint decision or logged assumption | `decisions.md` (see `core.md`, `planning.md`) |

Update means *rewrite the affected part to be true* — not append a changelog line under
stale prose. The current doc reads as if written today, cleanly, with no "UPDATE:"
scar tissue.

## Archiving — history without confusion

The current docs must never contain stale content, and history must never be overwritten.
Both, via the archive:

- **Before a material rewrite** of a doc (changed meaning, not typos or wording), copy the
  outgoing version to `docs/archive/` as `YYYY-MM-DD-<name>.md` — date of supersession,
  e.g. `docs/archive/2026-08-09-architecture.md`.
- Stamp the archived copy at the top — date, what superseded it, why, where it's recorded:
  `> Archived 2026-08-09. Superseded by ../architecture.md. Why: R2 move (Q3 in decisions.md).`
- The current doc points back only when the history is genuinely useful:
  `Previous design: archive/2026-08-09-architecture.md`.
- **Archive is append-only.** Never edit or delete archived versions; never "fix" an old
  doc. Git has the fine-grained history — the archive exists so a human or agent can read
  the previous *coherent* state without archaeology.
- Nothing in `archive/` is load-bearing. Agents and readers treat it as context for *why*,
  never as instructions for *what is*. If you find yourself reading the archive to learn
  how the system works today, the current docs have failed — fix them.

Same discipline as `decisions.md`: an answered question keeps its record; superseded docs
keep theirs.

## What not to write

- Docs that restate the code. Document *why* and *shape*, not line-by-line what.
- API-reference prose for internal functions — types and signatures already say it.
- Aspirational docs for things not built. Docs describe what is, plans live in the plan.
- A doc nobody will ever load. If it has no reader, it has no reason.

## Checklist

- [ ] Every affected doc rewritten to true, in the same commit as the change
- [ ] Diagrams match the code as of this change
- [ ] Materially rewritten docs archived first, dated, with a superseded-by note
- [ ] Archive untouched except for additions
- [ ] `docs/README.md` index still accurate
- [ ] Decisions traceable: change → its `decisions.md` entry
