# Reversibility and rollback

Load when: the work touches data, schema, deployed state, config, or anything living
outside the repo — migrations, deletes, deploys, third-party resources. In short, whenever
`git revert` alone would not put things back. Confirming a destructive step before running
it is in `destructive-actions.md`.

The standard: **every change ships with the way back.** A rollback returns the codebase
*and* the running app to the state they were in as if the change had never happened — code,
schema, data, config, and external state together. A change that only knows how to go
forward isn't finished; it's a bet.

## Build the way back with the change

Before writing the forward path, know what undoes it. Same commit, not a follow-up:

- **Code** — a revertible commit or range. No half-migrated call sites left for a later
  cleanup that would make the revert conflict.
- **Schema** — the down migration, written alongside the up migration, never "if we ever
  need it". Reversible means *tested* reversible: apply, roll back, apply again, against a
  real instance (`testing.md`).
- **Data** — anything that rewrites or drops rows takes a restore point first, and the down
  path restores from it. A down migration that recreates an empty column is not a rollback.
- **Config and env** — record the previous values before changing them; the rollback puts
  them back. Same for feature flags, access rules, quotas, webhook targets, DNS.
- **External state** — resources the change creates elsewhere (buckets, keys, domains,
  webhook registrations, mail templates) get listed with what removes or restores each.
- **Docs** — the archive discipline in `documentation.md` already keeps the outgoing
  version; the rollback restores it.

Prefer changes that are reversible by construction: add before you remove,
expand-then-contract instead of rename-in-place, new endpoint beside the old one, a flag
instead of a replacement. The contract step is its own later change, separately confirmed,
once the rollback window has closed.

## The rollback runbook

Written when the change is made, not when it's on fire. Lives in the project's operations
doc (`documentation.md`) and names, in order:

1. The revert — commit or range, and the deploy that carries it
2. The reverse migrations, by name, in the order they must run
3. The restore point the data comes from, and how to verify it landed
4. The manual steps, if any (below)
5. How to know it worked: what to check, what should be true afterwards

## Rolling back runs the reverse path itself

A rollback that depends on remembering things fails at the worst possible moment. Wire the
reverse migrations into the rollback path so triggering it executes them — the user rolls
back, and the schema and data come back with the code. Don't leave a down migration sitting
in a folder hoping someone runs it.

Before executing: if any step is destructive, permanent, or touches real user data, confirm
first, per `destructive-actions.md`. If every step is cheap and reversible, run it and
report what ran.

## When automatic isn't possible

Some of it won't automate: a dashboard toggle, a DNS change, a vendor support ticket, an
email already delivered, a payment already settled. That is not a reason to skip the
rollback — it's a reason to say so:

- List every manual step in order, with exactly what to click or run, and how to verify it.
- Say plainly what cannot be undone at all, and what the closest recovery is.
- Confirm the whole plan — automatic and manual together — before starting any of it.
- Then run the automatic part and report which manual steps are still outstanding. Never
  report a partial rollback as a completed one.


## Checklist

- [ ] Down path written in the same commit as the forward change
- [ ] Down path tested by actually rolling back and re-applying
- [ ] Restore point taken before anything that overwrites or deletes data
- [ ] Previous config, flag, and external-state values recorded before the change
- [ ] Rollback runbook in the operations doc, with verification steps
- [ ] Rollback executes the reverse migrations itself, not from memory
- [ ] Manual steps listed explicitly; anything unrecoverable stated as such
