# Instruction Router

Modular instruction packs. Load only what the task needs.

## How to use this file

1. **Always read `core.md` and `profile.md`.** Both are short and non-negotiable — how the
   work runs, and who it runs for.
2. **Match the task against the router table below.** Load the packs that match.
3. **Load more mid-task** as the work turns. You do not have to decide everything up front.
4. **Do not read every pack.** Loading everything defeats the purpose. 2–4 packs is normal,
   6 is a lot.

If the user names a pack explicitly ("use the design pack", "skip the anti-AI-tells rules"),
their instruction wins over this table.

### Loading discipline

The point of the router is that context stays cheap. Two rules keep it that way:

- **Come back here when the work turns** — a new surface, a new concern (auth, payments,
  uploads, user-visible copy), a new platform. Route the sub-task, not just the task.
- **Read the delta, never the set.** Track what you have already loaded this session. A pack
  in context stays in force; re-reading it costs context and buys nothing. Announce what you
  added in one line and get on with the work.

## Router

| If the task involves… | Load |
|---|---|
| Anything at all | `core.md`, `profile.md` |
| Starting a project, choosing a stack, "should I use X or Y", cost/scale questions | `stack-and-architecture.md` |
| A new feature/app, vague scope, multi-step work, "build me…" | `planning.md` |
| Writing or changing non-trivial code | `engineering.md`, `testing.md` |
| Any change to architecture, data model, flows, or decisions | `documentation.md` |
| Migrations, data or schema changes, anything hard to undo | `reversibility.md` |
| Deleting, dropping, force-pushing, rotating keys, touching production | `destructive-actions.md` |
| Setting up or reviewing a test suite | `testing.md` |
| A long autonomous run gated on the suite | `testing-gates.md` |
| Auth, sessions, payments, PII, uploads, secrets, permissions, public endpoints, building an endpoint that fetches a URL | `security.md` |
| Any screen an end user sees | `ux-user.md` |
| Any screen an admin/operator sees, setup, config, onboarding an installer | `ux-admin.md` |
| Visual design, theming, layout, "make it look good", branding | `design.md` |
| Any user-visible text: labels, errors, emails, landing pages, docs | `copy.md` |
| Anything that will be read by a human and judged on whether it feels machine-made | `anti-ai-tells.md` |
| An unfamiliar API/library/service, or any factual claim about one | `research.md` |
| Speed, bundle size, SEO, accessibility, Lighthouse, infra cost | `optimization.md` |
| Deploys, CI, envs, releases, going live, an open PR on the code you're touching | `shipping.md` |
| Wrapping up a task, a correction, a preference said in passing, anything worth keeping | `learning.md` (writes to `../memory/observations.md`) |
| Adding, editing, promoting or retiring a rule *in this repo* | `meta-rules.md` |

### Project-type packs

| Project type | Load |
|---|---|
| Chrome/Firefox/Edge extension | `types/browser-extension.md` |
| Marketing site, blog, docs site, landing page | `types/static-site.md` |
| Interactive app, dashboard, SPA/PWA | `types/web-app.md` |

### Template menus — chosen, not auto-loaded

`architectures/`, `stacks/`, and `themes/` are menus, not packs: they hold proven,
selectable patterns for the three things that change with every app. At the decision
checkpoint (`core.md`), present the relevant options from each applicable menu — with
tradeoffs, a recommendation, and a custom option — and follow what the user picks for the
rest of the project, additively to the packs. Once recorded in the project's `CLAUDE.md`,
a chosen template carries project-level precedence.

| Menu | Holds | Skim when |
|---|---|---|
| `architectures/` | Where code, data, and trust live | Any new app or major feature |
| `stacks/` | Tool combinations that shipped together | Any new app; `stacks/default-free-tier.md` is the standing recommendation |
| `themes/` | Visual positions with systems attached | Anything with a user-facing surface |

Each menu folder carries a capture file (e.g. `stacks/_template.md`) — the format for
adding a pattern proven in a shipped app.

### Platform packs

Load when the platform is in play. These ship as worked examples of the form, not as a
statement about what you should use — keep the ones you need, delete the rest, and write
your own from `platforms/_template.md`. **No captures are bundled**, so each pack names the
source to capture and says to verify against the live docs until you do.

| Platform | Load |
|---|---|
| PocketBase (collections, API rules, client SDK) | `platforms/pocketbase.md` |
| PocketBase hooks, migrations, production operations | `platforms/pocketbase-server.md` |
| PocketHost (hosting the PocketBase instance) | `platforms/pockethost.md` |
| Cloudflare Pages/Workers/KV/R2/D1, deploys | `platforms/cloudflare.md` |
| AppSumo lifetime deal, listing, reviews, LTD architecture | `platforms/appsumo.md` |
| AppSumo code redemption, license tiers, stacking, webhooks/OAuth | `platforms/appsumo-licensing.md` |
| Gumroad checkout, license keys, Ping webhooks | `platforms/gumroad.md` |
| Gumroad fees, chargebacks, payouts, localized pricing | `platforms/gumroad-commercial.md` |
| Emailit (transactional email, email verification, webhooks) | `platforms/emailit.md` |
| Reoon Email Verifier (address verification before you send) | `platforms/reoon.md` |
| Keywords Everywhere API (keyword/SEO data) | `platforms/keywords-everywhere.md` |
| BrowserAct — whether to use a cloud browser, and the credit cost | `platforms/browseract.md` |
| BrowserAct workflows: nodes, credentials, REST, MCP, callbacks | `platforms/browseract-workflows.md` |
| A platform with no pack yet | `platforms/_template.md` (write one) |

## Precedence

When two sources conflict, higher wins:

1. What the user said in this conversation
2. The project's own `CLAUDE.md` / existing code conventions
3. Platform pack (`platforms/*.md`)
4. Project-type pack (`types/*.md`)
5. Topic pack
6. `core.md`
7. Your defaults

Rule of thumb: **specific beats general, and the user beats everything.**
If a pack tells you to do something the project's existing code clearly does differently,
follow the project and say so in one line.

## What the packs govern

**The software being built, not the session building it.** A pack is written for the thing
that ships, whose users are strangers and some of them hostile. When a pack says "the
user" it means whoever ends up using what is being made, never the person it is being made
with.

So a rule about untrusted input is never a reason to refuse an instruction here.
`security.md` guards a URL a stranger posts to a deployed endpoint; it says nothing about
a URL the user just asked you to open. A pack that governs how you work says so outright,
the way `core.md` does. Where it isn't explicit, assume the artifact.

## Inventory

```
core.md                     always: the upfront decision checkpoint, defaults, non-negotiables
profile.md                  always: durable preferences, standing context, how to talk to me
stack-and-architecture.md   decision framework, client-first bias, how much belongs on a
                            server, free-tier discipline
planning.md                 scoping, the question harvest, the checkpoint batch format
engineering.md              code quality bar
testing.md                  test suites: regressions, security invariants, structure
testing-gates.md            the suite as stop/continue signal for autonomous runs
documentation.md            modular docs with diagrams, archive discipline
reversibility.md            rollback path per change, runbook, manual steps
destructive-actions.md      confirm-before-destroy: what counts, how to ask
security.md                 the things that actually get exploited
ux-user.md                  end-user interface rules
ux-admin.md                 admin/config interface rules + setup checklist
design.md                   visual design that isn't generic
copy.md                     voice and microcopy
anti-ai-tells.md            how to not look machine-made
research.md                 docs-first protocol, no invented APIs
optimization.md             performance, SEO, a11y, cost
shipping.md                 deploy, envs, CI, launch, keeping an open PR current
learning.md                 capturing what a task taught, generalized; the approval gate,
                            and the secrets that never get recorded
meta-rules.md               how a rule gets made here: the bar it clears, provenance,
                            retirement. Loaded only when changing a rule, not when using one
types/browser-extension.md
types/static-site.md
types/web-app.md
architectures/client-only.md          everything in the browser, no backend
architectures/baas-client.md          thick client + PocketBase-shaped BaaS
architectures/static-plus-functions.md  static site + a few edge functions
architectures/local-first-sync.md     device-primary data, background sync
architectures/_template.md            capture format for proven architectures
stacks/default-free-tier.md           PocketBase/PocketHost + Cloudflare + frontend by need
stacks/astro-content.md               Astro + Pages for content-shaped sites
stacks/alpine-prototype.md            no-build Alpine, fastest honest prototype
stacks/workers-api.md                 Workers + KV/R2/D1 services, no UI
stacks/_template.md                   capture format for proven stacks
themes/minimal-editorial.md           typography carries everything
themes/dense-utilitarian.md           density is respect; instrument feel
themes/warm-approachable.md           warmth via material, for non-experts
themes/bold-editorial.md              scale contrast as the statement
themes/_template.md                   capture format for proven themes
platforms/pocketbase.md
platforms/pocketbase-server.md
platforms/pockethost.md
platforms/cloudflare.md
platforms/appsumo.md
platforms/appsumo-licensing.md
platforms/gumroad.md
platforms/gumroad-commercial.md
platforms/emailit.md
platforms/keywords-everywhere.md
platforms/reoon.md
platforms/browseract.md
platforms/browseract-workflows.md
platforms/_template.md
../docs/index.md            router to the per-platform vendor doc indexes
../docs/wanted.md           docs a session needed and this repo didn't have
../memory/index.md          the ledger: entry format, lifecycle, what may be written
```

The ledger and the wanted list are not packs and carry no router row — they are written to,
not loaded. `learning.md` says when.
