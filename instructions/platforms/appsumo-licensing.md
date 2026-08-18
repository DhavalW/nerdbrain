# AppSumo licensing (redemption and the Licensing API)

Load when: implementing code redemption, license tiers, stacking, or the AppSumo webhook
and OAuth integration. The deal itself — listing, reviews, and what an LTD does to the
architecture — is in `appsumo.md`.

Docs, two captures with different jobs:

Docs: **no capture bundled.** Capture `docs.licensing.appsumo.com` (the Licensing API, which
is what you actually build against) and `help.appsumo.com` (the partner help centre, one
article per page, cited below **by title**) into `../../docs/references/appsumo/` and index
it (`../../docs/index.md`) — the topic citations below then resolve to page ranges at read
time. Until then verify against the live docs (`../research.md`); cite topics by name, never
pages.

Never resolve either from memory. Policy details change and money depends on them, so
**verify anything you'd act on** (`../research.md`).

## Redemption and licensing

Read before implementing — the doc index groups these under "Start here if you're building
the product": *How do I set up my redemption flow?*, *Codes and Redemption Instructions*,
*How do I activate my license?*, *What is a license?*, *Invalid Codes*.

What the implementation has to handle:

- **Code redemption** — user arrives with a code, creates or links an account, gets access.
  This flow is what AppSumo reviews and what customers hit first. It carries an outsized
  share of launch support load. Make its error states specific (`../copy.md`).
- **Stacking** (*What is Stacking?*) — buying multiple codes to move up tiers. Your
  entitlement model must handle N codes on one account, not just one. Design for it even
  if the deal launches single-tier; retrofitting it is painful.
- **Tier changes** (*Upgrading / downgrading my license*, *How can I list multiple plan
  tiers?*) — including what happens to data over the limit when someone downgrades or
  refunds.
- **Refunds** — a refunded code must revoke access. Have the deactivation path built and
  tested before launch, not after the first refund. Read the refund-policy articles
  (partner-facing: *What is AppSumo's refund policy for my listing?*; also *Refund FAQ*
  and *Understanding Refund Activity on AppSumo*) and confirm the current window and terms
  rather than assuming.
- **Add-ons** (*License add-ons*).

Treat license state as server-authoritative. A client-side entitlement check is a
suggestion, and an LTD audience is technical enough to find it.

## The licensing integration

The help centre explains the deal; the Licensing API capture is the wiring. Its shape, so
you can plan the work before reading it:

- **Two mechanisms, both required.** Webhooks tell your system about license lifecycle
  events; OAuth is how the customer arrives in your app with a license key attached.
  Neither works alone, and both URLs must validate in the Partner Portal before you get
  OAuth keys at all — so do that first, not the week of launch.
- **The license key is the identity.** AppSumo stores no customer email, only keys. You
  collect the email yourself at the redirect URL and link it there (topic: *Webhook
  Object*).
- **A tier change mints a brand-new key.** Upgrade and downgrade each issue a fresh UUID and
  send a simultaneous `deactivate` for the old one, with `prev_license_key` tying them
  together. An entitlement model that assumes one permanent key per customer breaks the
  first time anyone stacks.
- **Your 200 is the state transition.** An `activate` event arrives with the license still
  inactive — AppSumo flips it only after your success response, and the same holds for
  deactivate. A handler that quietly 500s leaves the customer stranded on both sides
  (topic: *Sending a successful response*).
- **Verify the signature.** Webhooks carry HMAC-SHA256 over timestamp + raw body in
  `X-Appsumo-Signature`, keyed by your API key (topic: *Webhook Security*). The docs frame
  verification as optional. Treat it as mandatory (`../security.md`) — this endpoint hands
  out entitlements.
- **Add-ons hang off `parent_license_key`**, and refunding a parent cascades to them.
- **Don't change validated URLs once live.** It breaks the connection, and reopening them
  needs AppSumo (topic: *How Can I Reset My OAuth and Webhook URLs?*).

The capture omits the site's own API section — the Licensing API and Partner profile API
endpoint references — so verify anything about those against the live docs
(`../research.md`).

## Store the identity, not just the code

Capture the redemption identity (the code, the AppSumo-side identifier, the purchase email)
against the account, permanently, and keep an audit trail of tier changes. You will need it
for support ("I stacked three codes but only see tier 2"), for refund handling, and for
reconciliation. Relevant articles: *How can I receive customers' contact information?* and
*How do I track my sales and refunds?*.

## Checklist

- [ ] Redemption flow implemented, with specific error states
- [ ] Stacking supported in the entitlement model
- [ ] Upgrade, downgrade, and refund/revoke paths built and tested
- [ ] Webhook signature verified before the payload is trusted
- [ ] Key rotation on tier change handled — new key, `prev_license_key`, old one deactivated
- [ ] Entitlements enforced server-side
- [ ] Redemption identity and tier history stored and auditable
