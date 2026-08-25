# Destructive actions

Load when: a step deletes, drops, overwrites, force-pushes, rotates keys, touches
production, spends money, or mails real users — and whenever you are unsure whether it
qualifies. Designing the rollback for a change is in `reversibility.md`.

## Confirm before destroying — always, and at the start

Never assume consent for something that can't be taken back. The rule from `core.md`, in
detail:

- **Ask before, not after.** Harvest every destructive step the work will need during the
  decision checkpoint (`core.md`, `planning.md`) and get it confirmed in the same batch as
  everything else, so a long run never parks itself halfway waiting on a human.
- **Wait indefinitely.** No timeout, no default, no "proceeding since I didn't hear back".
  Silence is not consent and an expired prompt is not consent — which is why the request
  goes in the reply as plain text, at the end, and the turn ends there. Resume when the
  user says yes, whenever that is.
- **Never behind a timed form.** Mid-task questions are asked that way and take the
  recommendation when the timer runs out (`core.md`); destruction is the case that rule
  exempts. A prompt nobody saw has authorized nothing.
- **One confirmation, one action.** Approval to drop a column is not approval to drop the
  table beside it, and it does not carry into the next session.
- **Show the blast radius.** What's affected, how much of it, whether it can be undone, and
  what the backup is. "Delete 4,812 orders older than a year — restore point taken,
  recoverable for a week" beats "OK to clean up old orders?"
- **If one surfaces mid-run anyway**, stop before doing it, finish everything that doesn't
  depend on it, and end the turn with the question. This is the one halt `core.md` allows,
  and it means the harvest missed something.

## What counts as destructive

Assume yes if it's here, or if undoing it would need someone else's cooperation: dropping
or truncating tables, columns, or collections; deleting records, files, buckets, or
branches; `push --force` and any history rewrite; overwriting an existing file with
generated content; resetting a shared or production environment; rotating or revoking keys,
tokens, and access; DNS and domain changes; sending real email or notifications to real
users; anything that charges or refunds money; disabling backups; installing to or
uninstalling from a live tenant; any migration run against production data.

New files, new columns, code on a branch, local scratch state — not destructive. Don't ask
about those. Asking about everything trains the answer "yes".


## Checklist

- [ ] Every destructive step confirmed up front — asked, waited for, never assumed
