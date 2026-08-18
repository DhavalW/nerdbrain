# AppSumo (Lifetime Deals)

Load when: building or adapting a product to sell on AppSumo — the deal, the listing, and
what an LTD does to the architecture. For code redemption and the licensing integration,
load `appsumo-licensing.md`.

Docs:

Docs: **no capture bundled.** Capture `help.appsumo.com` — the partner help centre, one
article per page, cited below **by title** into `../../docs/references/appsumo/` and index it
(`../../docs/index.md`) — the topic citations below then resolve to page ranges at read time.
Until then verify against the live docs (`../research.md`); cite topics by name, never pages.

Never resolve it from memory. Policy details change and money depends on them, so
**verify anything you'd act on** (`../research.md`).

## What an LTD means for the architecture

A lifetime deal is a one-time payment for perpetual access. That reshapes the product:

- **Per-user recurring cost is your enemy.** Every LTD customer is a permanent cost with no
  recurring revenue. Anything that costs you per-seat per-month (a paid API call per user,
  per-user storage that only grows, an expensive per-tenant instance) will slowly consume
  the deal revenue. This is the strongest possible argument for the client-first,
  free-tier-first architecture in `../stack-and-architecture.md`.
- **Design a metered layer up front.** Consumable resources (AI credits, API calls, exports,
  storage) need a quota system from day one — enforced server-side (`../security.md`).
  Retrofitting quotas onto customers who bought "unlimited" is a support disaster. The
  article *Understanding AI Credits on AppSumo* shows how metering is framed to buyers.
- **Support volume arrives in a spike**, at launch, from users who all bought at once and
  are all setting up simultaneously. Read *How to Ensure Your Support Team is Ready for
  Launch*.
- **Tiers are permanent.** Whatever a tier includes, it includes forever. Be careful what
  goes in the base tier.

## Listing and launch

The doc index groups these under "Becoming a partner" and "Running the listing":
submission and vetting, verification, categories, the founders' post, pricing and list
price, the partner portal, post-launch updates (*My deal is live! Now what?*, *Updating
your offer*, *My Deal Terms Changed*, *Deal Price Changes*).

## Reviews

Reviews drive the deal, and the review period overlaps the refund window, which means the
first week matters disproportionately. The index has a "Reviews" group: guidelines,
moderation, vetting, *How to Ask for Honest Reviews* (includes email templates), and
*Maximizing Your AI Review Summary*.

Practical consequence for the build: **onboarding quality is review quality.** A customer
who can't get set up in the first ten minutes leaves a review about that. This is exactly
what the setup checklist in `../ux-admin.md` is for — build it before launch, not after.

## Checklist

- [ ] No per-user recurring cost that scales without recurring revenue
- [ ] Quota/metering built in from the start for any consumable
- [ ] Onboarding and setup checklist ready before launch
- [ ] Support ready for a launch-day spike
