# Default free-tier stack

The standing recommendation (`../core.md`): full app capability — auth, data, files,
realtime, hosting, CI — at zero cost, scaling as far as free tiers go.

## The pieces

| Layer | Tool | Why this one |
|---|---|---|
| Backend / data | PocketBase on PocketHost | Auth + CRUD + realtime + files + admin UI in one managed instance |
| Hosting / deploy | Cloudflare Pages, GitHub-wired | Push-to-deploy, per-branch previews, static serving effectively free |
| Frontend, simple | Alpine.js | Interactivity without a build pipeline |
| Frontend, complex | React/Preact or Svelte | Real state management; Preact when bundle size matters, Svelte when interaction-heavy |
| Server extras | Cloudflare Workers (only if needed) | Secret-holding proxy, webhooks — the jobs PocketBase hooks can't take |

Say which frontend and why at the checkpoint — "by complexity" is the menu, not the answer.

## Serves architectures

`../architectures/baas-client.md` (canonical), `../architectures/local-first-sync.md`
(PocketBase as sync target). The frontend half alone serves
`../architectures/client-only.md`.

## Wiring

- Repo on GitHub → Cloudflare Pages builds on push; production branch = production deploy,
  every other branch gets a preview URL. No CI config needed for deploys.
- The client talks to PocketBase directly via its SDK; the PocketBase URL is public config,
  not a secret. Real secrets live in Worker env, never in the client (`../security.md`).
- `pb_migrations/` and `pb_hooks/` live in the repo and get applied to the instance —
  the repo is the source of truth, the instance is a deploy target
  (`../platforms/pockethost.md`).
- Local dev runs the same PocketBase version as the instance. Never develop against prod.

## Tradeoffs

- Strong: fastest path from idea to deployed app with accounts; nothing to operate; every
  piece independently replaceable.
- Weak: two dashboards (Cloudflare, PocketHost); instance sleep on the free tier means
  cold starts; no server-side rendering in this shape.
- Ceiling: PocketBase's single writer and single region. Exit path is the same binary on a
  VPS, or swapping the data layer entirely — the client-side investment survives either.

## Cost

Free at steady state for indie-scale apps. First limits to bite: PocketHost instance
sleep/disk, then Worker invocations if you added any. Verify current numbers at decision
time (`../research.md`) — they move.

## Best practices

- Large files go to R2 with references in PocketBase, not onto instance disk
  (`../platforms/cloudflare.md`).
- Don't add a Worker until a concrete secret/webhook/trust need exists. Most apps on this
  stack never need one.
- Platform packs carry the depth: `../platforms/pocketbase.md`,
  `../platforms/pockethost.md`, `../platforms/cloudflare.md`.
