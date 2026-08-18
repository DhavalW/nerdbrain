# Alpine prototype stack

For prototypes, internal tools, and simple apps: no build step, no framework runtime,
readable in one file. Optimized for time-to-working and time-to-understanding.

## The pieces

| Layer | Tool | Why this one |
|---|---|---|
| Frontend | Alpine.js + plain HTML/CSS | Declarative interactivity, zero tooling; the page *is* the source |
| Styling | Hand-rolled CSS (or one small utility sheet) | No pipeline; keep it inspectable |
| Data, if needed | PocketBase on PocketHost | Accounts and persistence without leaving no-build land |
| Hosting | Cloudflare Pages | Drag-and-drop or repo-wired; nothing to compile |

## Serves architectures

`../architectures/client-only.md` (its natural home) and the small end of
`../architectures/baas-client.md`. Not for `../architectures/local-first-sync.md` — sync
state outgrows Alpine fast.

## Wiring

There barely is any — that's the point. HTML files in a repo, Pages serves them, the
PocketBase SDK loads from a `<script>` tag when data enters the picture. An agent or a
human can read the entire app top to bottom.

## Tradeoffs

- Strong: fastest honest path to something working; trivially debuggable; nothing to
  maintain; excellent for validating an idea before investing.
- Weak: no types, no components, no bundler tree-shaking; shared state across many
  elements gets stringly and fragile.
- Ceiling: roughly "state spans several screens." Past it, rebuild on
  `default-free-tier.md` with a real frontend — a prototype's job is to be replaced, and
  the PocketBase schema carries over untouched.

## Cost

Zero. Nothing here meters.

## Best practices

- **Declare it a prototype at the checkpoint** (`../core.md` asks) — the quality bar for
  error handling and tests is deliberately lower, and that's only acceptable when stated.
- Prototype-grade doesn't waive security: if it has accounts, the PocketBase rules
  discipline applies in full (`../platforms/pocketbase.md`). A leaked prototype is a leak.
- Keep each page self-contained; the moment you want shared components, take it as the
  ceiling signal rather than inventing an include system.
- Pin the Alpine and SDK versions in the script tags — "latest" breaks on its schedule,
  not yours.

## Proven in

The natural first rung for most app ideas on this repo's defaults; graduate deliberately.
