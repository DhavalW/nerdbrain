# Instruction Router

Modular instruction packs. Load only what the task needs.

## How to use this file

1. **Always read `core.md` and `profile.md`.** Both are short and non-negotiable — how the
   work runs, and who it runs for.
2. **Match the task against the router table below.** Load every pack that matches.
3. **Load the minimum that covers the work — and never less than that.** There is no count
   to hit. Four packs where the task needs four, seven where it needs seven. A pack the
   router matched is a pack the work needs, and dropping one to keep a number down is how
   the rule it carried gets broken.
4. **Do not read what the router did not match.** That is the whole economy, and it is
   enough: an unmatched pack is context spent on work you are not doing.

If the user names a pack explicitly ("use the design pack", "skip the anti-AI-tells rules"),
their instruction wins over this table.

### Loading discipline

Context stays cheap through *what* is loaded, never through *how much*. Three rules:

- **Route every task, and every iteration of one.** Come back here at the start of each new
  piece of work in a session — not only when the work changes kind. The check costs nothing:
  this table is already in context. What it prevents is a sub-task running on whatever packs
  the last one happened to need.
- **Read the delta, never the set.** Track what you have already loaded this session. A pack
  in context stays in force; re-reading it costs context and buys nothing. Most re-routes
  match nothing new — that is the expected result of a cheap check, not a wasted one.
- **Load everything the match names.** No cap, no trimming to a number. The router decides
  what the minimum is; your job is to not go under it.
- **Precision is the whole budget.** With no count cap, the only thing keeping context cheap
  is that a match means the task actually does this thing — not that it plausibly might.
  Adjacent to auth is not `security.md`. When a pack is a maybe, leave it: the re-route at
  the next iteration catches it the moment it becomes a yes, and that is what re-routing is
  for.
- **Load at the last responsible moment.** A pack the work reaches on its fourth step gets
  loaded on the fourth step, not up front in case it comes up. Same set by the end, less of
  it held while it does nothing.

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
| Needing docs this repo doesn't have, or a capture waiting to be filed | `doc-capture.md` (writes to `../docs/scrape-list.md`) |
| Adding, editing, promoting or retiring a rule *in this repo* | `meta-rules.md` |
| A fork sync this repo can't merge on its own: `conflict` or `dirty-overlap` | `fork-sync.md` |

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
| `stacks/` | Tool combinations that shipped together | Any new app |
| `themes/` | Visual positions with systems attached | Anything with a user-facing surface |

Each menu folder carries a capture file (e.g. `stacks/_template.md`) — the format for
adding a pattern proven in a shipped app.

### Platform packs

Load when the platform is in play. **The folder ships empty** — one pack per platform you
actually build on, written from `platforms/_template.md` as you go. A pack is worth writing
the second time you look something up: it names the gotchas, points at the capture in
`../docs/`, and marks the claims that decay so they get re-verified instead of quoted.

| Platform | Load |
|---|---|
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
doc-capture.md              queueing a docs gap for a crawler, and filing the PDF that
                            comes back
fork-sync.md                reconciling this fork with the original when the merge collides:
                            the approaches and what each costs, then carrying out the answer
meta-rules.md               how a rule gets made here: the bar it clears, provenance,
                            retirement. Loaded only when changing a rule, not when using one
types/browser-extension.md
types/static-site.md
types/web-app.md
architectures/client-only.md          everything in the browser, no backend
architectures/baas-client.md          thick client + a managed backend-as-a-service
architectures/static-plus-functions.md  static site + a few edge functions
architectures/local-first-sync.md     device-primary data, background sync
architectures/_template.md            capture format for proven architectures
stacks/_template.md                   capture format for proven stacks; the menu fills
                                      as you capture the ones that shipped
themes/minimal-editorial.md           typography carries everything
themes/dense-utilitarian.md           density is respect; instrument feel
themes/warm-approachable.md           warmth via material, for non-experts
themes/bold-editorial.md              scale contrast as the statement
themes/_template.md                   capture format for proven themes
platforms/_template.md                write one per platform you build on
../docs/index.md            router to the per-source doc indexes
../docs/wanted.md           docs a session needed and this repo didn't have
../docs/scrape-list.md      URLs queued for capture; ../docs/scrape-done.md is the receipt
../memory/index.md          the ledger: entry format, lifecycle, what may be written
```

The ledger, the wanted list and the two scrape files are not packs and carry no router
row — they are written to, not loaded. `learning.md` and `doc-capture.md` say when.
