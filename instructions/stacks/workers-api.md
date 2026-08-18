# Workers API stack

For services without a UI, or the server side of someone else's UI: APIs, proxies,
webhook receivers, bots, scheduled jobs. No PocketBase, no pages — just edge compute and
edge storage.

## The pieces

| Layer | Tool | Why this one |
|---|---|---|
| Compute | Cloudflare Workers | Instant cold starts, cron triggers, runs where the request lands |
| Config / flags / cache | KV | Cheap reads at the edge; eventually consistent |
| Files / blobs | R2 | S3-compatible, no egress fees |
| Relational data | D1 | SQLite semantics at the edge, when KV's model isn't enough |
| Coordination | Durable Objects (reluctantly) | Only for real per-key consistency; usually paid |

## Serves architectures

The functions half of `../architectures/static-plus-functions.md`, grown into a service of
its own. Not a general app backend — an app with users and CRUD wants
`../architectures/baas-client.md` instead; you'd be rebuilding PocketBase piecewise here.

## Wiring

- One Worker per service, deployed via `wrangler` from the repo; bindings (KV, R2, D1,
  secrets) declared in `wrangler.toml`, secret *values* set via `wrangler secret` — never
  in the file (`../security.md`).
- Cron triggers replace "a server with a crontab" for scheduled work.
- Not Node: web-standard runtime. Verify a package works on Workers before depending on
  it (`../platforms/cloudflare.md`).

## Tradeoffs

- Strong: zero infrastructure, global by default, scales to zero and from zero instantly;
  the cheapest way to run a small always-available service.
- Weak: CPU-time caps rule out heavy compute; storage options are each a compromise (KV
  eventual, D1 single-region-writes, DO paid); local dev is an emulation, so staging
  catches what localhost can't.
- Ceiling: long-running processes, websockets at scale, heavy relational load. Exit is a
  container on any host — keep handlers thin over a portable core so the move is a
  re-wrap, not a rewrite.

## Cost

Free tier is generous for APIs: the daily request cap bites first, then KV writes. Cache
responses and batch writes; verify current numbers at decision time (`../research.md`).

## Best practices

- Structure as router → thin handlers → plain-function core. The core has unit tests that
  never touch Workers APIs (`../testing.md`); handlers stay too thin to hide bugs.
- Idempotency keys on anything a caller might retry — at-least-once delivery is the norm
  at the edge.
- Version the API from day one (`/v1/`): edge deploys are instant and global, and so are
  breakages.
- Auth every route explicitly, deny by default — there is no "internal network" here;
  every endpoint is on the public internet (`../security.md`).
