# PocketBase server-side

Load when: writing hooks, changing schema through migrations, or deploying and operating a
PocketBase instance. Collections, API rules and the client SDK are in `pocketbase.md`.

Docs: **no capture bundled.** Capture `pocketbase.io` into
`../../docs/references/pocketbase/` and index it (`../../docs/index.md`) — the topic
citations below then resolve to page ranges at read time. Until then verify against the live
docs (`../research.md`); cite topics by name, never pages.

## Extending

Two paths, same hooks — each has its own full doc section (*Extend with Go*, *Extend with
JavaScript*):

- **Go** — compile PocketBase as a library. Faster, full ecosystem, real tests. Use for
  anything substantial.
- **Embedded JS** — drop files in `pb_hooks/`. No build step, no redeploy pipeline. Good
  for small hooks and for PocketHost. Read the *caveats and limitations* part of the JS
  overview before committing to it — the engine has real restrictions.

Use hooks for what rules can't express: side effects, derived fields, external calls,
enforcing invariants across records. Keep authorization in rules where it can live there —
rules are declarative and harder to get subtly wrong.

Hooks are per-request and synchronous. Slow external calls in a hook make every write slow.
For anything slow, use the scheduler (doc topic: *Jobs scheduling*).

## Migrations

- Migrations live in `pb_migrations/` and run on start (doc topic: *Migrations*, in both
  the Go and JS sections).
- Commit them. Schema changed in the admin UI without a committed migration is schema you
  will lose.
- Write the down path in the same commit, and prove it by rolling back and re-applying
  against a local instance (`../reversibility.md`).
- A migration that drops a field or rewrites records takes a backup first — that backup is
  what its down path restores from. Dropping is destructive: confirm it before you run it.
- Deploy migrations before the code that depends on them (`../shipping.md`).


## Production

Doc topic: *Going to production* — read its **recommendations** subsection in full; it's
short and covers superuser MFA, the rate limiter, file descriptor limits, `GOMEMLIMIT`,
and settings encryption. Backups and restore are in the same section — and test the
restore, per `../shipping.md`.

If hosting on PocketHost, see `pockethost.md` — some of this is managed for you and some
isn't.


## Checklist

- [ ] Migrations committed, reversible, tested from empty

- [ ] Backups configured and a restore tested
- [ ] Production recommendations applied
