# Cloudflare

Load when: hosting, deploying, edge compute, object storage, or CDN. Default per `../core.md`.

Docs: **no capture bundled.** Capture the `developers.cloudflare.com` sections you actually
build on into `../../docs/references/cloudflare/` and index it (`../../docs/index.md`) — the
topic citations below then resolve to page ranges at read time. Until then verify against the
live docs (`../research.md`); cite topics by name, never pages.

## Default setup

**Pages, connected to the GitHub repo.** Push to a branch gets a preview deploy; push to the
default branch gets production. No CI to build, no deploy scripts, no tokens to manage.
Take this path unless something specific rules it out.

**Wire it from the dashboard, and assume the operator cannot run code.** Cloudflare's GitHub
App holds the connection on Cloudflare's side — nothing in the repo to leak or rotate — while
a `wrangler`-from-Actions deploy needs an API token in repository secrets and buys nothing
for a build Cloudflare runs itself. There is also no terminal at the other end: setup is a
browser or it doesn't happen, which makes a deploy that needs someone to run a command
unfinished. Put build values in dashboard settings or committed files (`.nvmrc`, not an env
var someone must remember), and where no browser path exists — a database seeded once, a
restore — name it in the setup steps with who runs it, rather than hiding it in a "just run".

Static assets served from Pages are the cheapest thing in the stack. Anything you can render
at build time is effectively free to serve — the main argument for the static-first
architecture in `../stack-and-architecture.md`.

## Picking the piece

| Need | Use | Watch out for |
|---|---|---|
| Static site, SPA shell | **Pages** | Monthly build cap; builds, not requests, are the limit |
| Server logic, API proxy, secret-holding | **Workers** | Per-invocation CPU cap and daily request cap |
| Small config, feature flags, session-ish data | **KV** | Eventually consistent; **writes** are the tight quota |
| Files, uploads, backups, large assets | **R2** | No egress fee — the reason to pick it over S3. **Needs a card on file**, opt-in (`../profile.md`) |
| Relational data at the edge | **D1** | SQLite semantics; daily rows-read cap |
| Coordination, per-object consistency | **Durable Objects** | Usually paid; a real design commitment |

Reach for a Worker only when the work can't be static or client-side. Every Worker
invocation is metered; a cached static response is not.

## Workers

- Not Node. It's a web-standard runtime — `fetch`, `Request`, `Response`, Web Crypto. Many
  npm packages won't work. Check before depending on one.
- Stateless per invocation. Use KV/R2/D1/DO for anything that must persist.
- There's a CPU-time cap per request. Heavy computation belongs on the client
  (`../stack-and-architecture.md`), not here.
- Secrets go in Worker secrets, never in `wrangler.toml`, never in the repo
  (`../security.md`).
- `waitUntil` for work that should finish after the response is sent.
- Use the Cache API deliberately — a cache hit is the cheapest possible outcome.

## KV, R2, D1

- **KV** is read-optimized and eventually consistent. Do not use it for anything needing
  read-after-write. Batch writes; the write quota bites long before the read quota.
- **R2** for anything file-shaped. Pair it with PocketBase/PocketHost rather than filling
  instance disk (`pockethost.md`). Serve via a Worker or a bound custom domain, with
  access rules — a public bucket is a public bucket.
  **Enabling it wants card details even for the free allowance** (`../profile.md`), so R2 is
  proposed, never assumed: flag the card and put the card-free option beside it — instance
  disk while small, a committed export, another store — then let the user pick.
- **D1** is SQLite. Same strengths and same single-writer constraint as PocketBase's
  storage. Migrations are your responsibility.

## Caching

The biggest cost and performance lever available.

- Long `max-age` + `immutable` on hashed assets.
- `stale-while-revalidate` on HTML: fast for the user, fewer origin hits for you.
- Cache API inside Workers for repeated upstream calls, especially metered third-party APIs.
- Know how to purge, and purge narrowly, before you need to.

## DNS, domains, TLS

- Custom domain on Pages, TLS automatic.
- Decide www vs apex, and trailing slash, once. Redirect the other permanently.
- Set up redirects for any URL you change — permanently (`../types/static-site.md`).

## Costs

- Static requests: effectively free. Worker invocations, KV writes, D1 row reads: metered.
- The first limit hit is usually **Worker requests/day** or **KV writes/day**, not storage.
- Set usage alerts before launch, not after the first spike (`../shipping.md`).

## Checklist

- [ ] Pages + GitHub integration wired from the dashboard, previews working
- [ ] No Cloudflare API token in the repo or its CI secrets
- [ ] Every setup step doable in a browser; the exceptions named as such
- [ ] Everything that could be static, is
- [ ] Workers only where genuinely required
- [ ] Secrets in Worker secrets, not in config or repo
- [ ] Cache headers set deliberately on assets and HTML
- [ ] R2 buckets not accidentally public
- [ ] Domain, TLS, www/trailing-slash policy settled
- [ ] Usage alerts configured
- [ ] Current limits verified, not assumed

## Volatile claims

Pointers, not values (`../research.md`); `tools/staleness.py` reports them past their date.

- Free-tier ceilings for Worker requests, KV operations and D1 reads — verify by 2026-11
  against the live limits page. The local capture is Analytics only and carries none.
- Which operations are metered rather than free — verify by 2026-11 against live pricing.
