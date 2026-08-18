# PocketBase

Load when: PocketBase is the backend — modelling collections, writing API rules, querying
from a client. Default choice per `../core.md`. Hooks, migrations and running it in
production are in `pocketbase-server.md`.

Docs: **no capture bundled.** Capture `pocketbase.io` into
`../../docs/references/pocketbase/` and index it (`../../docs/index.md`) — the topic
citations below then resolve to page ranges at read time. Until then verify against the live
docs (`../research.md`); cite topics by name, never pages.

## What it is

Single Go binary over SQLite. Gives you auth, CRUD REST API, realtime subscriptions, file
storage, an admin UI, and an extension layer (Go or embedded JS) in one process.

Good at: solo-dev apps, admin tooling, anything that needs auth + persistence + an admin UI
without assembling four services.

Bad at: high concurrent write throughput (SQLite, one writer), horizontal scale (one
instance), and anything needing a managed multi-region database. If the design needs those,
say so during the stack decision (`../stack-and-architecture.md`), not after building.

## Collections

Three kinds:

- **Base** — normal data
- **Auth** — has identity/password/verification; you can have several (`users`, `staff`)
- **View** — read-only, defined by a SQL query. Excellent for aggregates and denormalized
  reads. Remember it's recomputed per query.

Schema notes:
- Define fields in the admin UI or in a migration; either way commit the migration.
- Relations can be single or multi. Multi-relations are stored as a JSON array — filtering
  and expanding them behaves differently from single (doc topic: *Working with relations*).
- Back-relations (`otherCollection_via_field`) let you expand the reverse direction, with
  caveats worth reading (same section).
- Index anything you filter or sort on. SQLite will happily table-scan.
- **`required: true` on a number means "must not be zero", not "must be present".** A field
  where zero is a legitimate value — a cost, a count, a balance delta — must be left
  non-required, or a valid write is rejected. Fires when: any numeric field whose domain
  includes 0. Enforced by: review question, on every migration that marks a number required.
  The damage lands late — the rejection arrives at the write, after whatever produced the
  zero has already happened and been paid for (obs-0035).

## API rules — this is the security model

Every collection has five rules: list, view, create, update, delete.

- **`null` (locked)** = superusers only. This is the default and the safe state.
- **Empty string** = public, no auth. Deliberate choice, never an accident.
- **An expression** = evaluated per request against the record.

Rules are filter expressions, not code. Before writing any, read the doc topic *API rules
and filters* — syntax, special identifiers, modifiers, and examples.

Non-negotiables:

- **Set all five rules on every collection before it holds real data.** An unset rule you
  meant to fill in later is the most common PocketBase security bug.
- Ownership goes in the rule: the record's owner field must match the authenticated user.
  Never rely on the client filtering to its own records.
- Guard against anonymous first: an authenticated check that passes for empty auth is a hole.
- Rules apply to realtime subscriptions too — but verify what a subscriber can observe,
  including whether they can see records appear and disappear.
- Fields the client must not set (role, plan, credits, owner) must be protected. Do it in
  the rule or in a hook, and test that a crafted request can't set them.
- `@request.*` identifiers let a rule inspect the incoming request. Their exact names have
  changed across major versions — read them from the docs, never from memory.

Test rules by actually calling the API as an unauthenticated user and as a different user
(`../testing.md`). Not by reading the expression and believing it.


## Files

Doc topic: *Files upload and handling*. Stored on disk (or S3-compatible), served by
filename under the record. Thumbnails are generated on request via a query param.
Protected files need a short-lived file token — use that for anything not public. Set size
and MIME constraints on the field.

## Client SDK

- Auth state persists in the SDK store; wire it to your app's session handling.
- `expand` fetches relations in one call — but only where the requester passes the related
  collection's view rule.
- Realtime subscriptions are a socket per client. Unsubscribe on unmount.
- The SDK auto-cancels duplicate in-flight requests by key, which surprises people. Know
  it before you debug it.


## Checklist

- [ ] All five rules set explicitly on every collection
- [ ] Ownership enforced in rules, verified by calling the API as another user
- [ ] Client-settable fields audited; privileged fields blocked
- [ ] Indexes on filtered and sorted fields

- [ ] File fields size/type constrained; non-public files protected
