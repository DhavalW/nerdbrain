# Planning

Load when: the ask is a feature or an app rather than an edit, the scope is fuzzy, or the
work will span more than a couple of files.

## Sequence

1. **Restate the goal** in 3 bullets: what it does, who it's for, what "done" means.
   If you can't, you don't understand the ask yet.
2. **Harvest every question the whole task will raise** — not just the ones blocking step
   one. Walk the plan end-to-end and collect the ask-me items from each loaded pack: stack
   options, admin UI and setup checklist (`ux-admin.md`), budget, deploy target, data
   retention, anything scope-forking, and **every destructive or irreversible step the plan
   will require** (`destructive-actions.md`). The measure of a good harvest: after the
   checkpoint, nothing halts the build.
3. **Sort them:** *blocking* (a wrong guess makes the work wrong) vs *assumable* (state a
   default and flag it).
4. **Run the decision checkpoint** (`core.md`): list the batch in the reply, end the turn,
   and wait for the answers however long they take. The template-menu
   choices — architecture, stack, theme, each with a custom option (`core.md`) — and any
   option formatted per `stack-and-architecture.md` go in this same batch — one
   checkpoint, not two.
5. **Write the plan. Then build straight through.**

## The batch

Written into the reply, at the end, under its own heading. One block, numbered, each
question standing on its own:

```
Q3. Where do uploaded images live?
    Why it matters: instance disk is capped; the wrong choice means a migration later.
    A. Object storage, references in the database — survives a move  ← recommended
    B. Database file fields — simpler, but shares the capped instance disk
```

Rules:

- Number them so the answer can be short: "3A, 5B, rest as recommended."
- Every question carries a marked recommendation, and "rest as recommended" must always be
  a safe answer.
- Plain text in the reply, never a prompt widget — widgets expire and the expiry reads as a
  yes (`core.md`). Mid-build is the reverse: form, timer, assume-and-continue.
- Nothing after the batch. It ends the reply and ends the turn.
- Once answered, the answers become the project's decision record (`documentation.md`),
  along with any assumption logged mid-build and what would change if it's overridden.

## Asking well

- Batch. One checkpoint beats six interruptions — that is the entire point.
- Give each question real options with consequences attached, not "what do you want?"
- Recommend one and mark it. A question with no recommendation pushes work back uphill.
- Assume defaults for anything already answered in `core.md`. Don't re-ask those.
- **Pre-fill from `profile.md` rather than asking cold.** A question it already answers goes
  in the batch with the answer written in and marked as from the profile, so the user
  strikes what's wrong instead of composing what's right. A batch that asks a settled
  preference for the third time is the system failing to have learned anything.
- Never ask something you could determine by reading the repo.
- A cheap decision can ride along if the user's taste would improve it — in this batch,
  while they're already deciding, never as its own interruption an hour later.

Bad: "What database do you want?"
Good: "The managed option gives you auth and an admin UI free, but one instance is a single
point of failure. The serverless one scales flatter and you'd build auth yourself.
Recommend the managed one — you need admin tooling more than you need scale. OK?"

## The plan itself

Keep it short enough to read in a minute:

- **Milestones** — each independently shippable, in order, each ending at a test gate:
  suite green including the milestone's new tests (`testing.md`)
- **File map** — what gets created or touched
- **Data model** — collections/tables, key fields, relations
- **Interfaces** — the contract between pieces, if there's more than one piece
- **Risks** — what could make this take 3x longer
- **Explicitly out of scope** — the things you decided *not* to build

That last one matters. Uncaptured scope becomes a surprise later.

## When to skip planning

- A one-file change with obvious intent
- A bug with a known cause
- The user already gave you the plan

Skipping is fine. Say you're skipping and start.

## Mid-build

- Questions that surface now follow the `core.md` protocol: ask through the form and take
  the recommendation if it times out, logging the assumption. Only the destructive and the
  expensive-to-reverse wait for a real answer. No other mid-run halts.
- If the plan turns out wrong, say so and re-plan. Don't quietly build something else.
- If you discover work outside the agreed scope, note it, finish what was agreed, and
  raise it at the end.
