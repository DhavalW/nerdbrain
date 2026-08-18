# Gumroad

Load when: integrating Gumroad — license verification, entitlements, or the Ping webhook.
Fees, chargebacks and payout mechanics are in `gumroad-commercial.md`.

Docs, two captures with different jobs:

Docs: **no capture bundled.** Capture `gumroad.com` — the REST API reference and the Ping
webhook page, whose delivery semantics are the part that matters into
`../../docs/references/gumroad/` and index it (`../../docs/index.md`) — the topic citations
below then resolve to page ranges at read time. Until then verify against the live docs
(`../research.md`); cite topics by name, never pages.

## What it is

A checkout, file host, and payout system for digital goods. It replaces assembling Stripe +
delivery + VAT handling + a customer library yourself. In exchange it owns the buyer
relationship and takes a cut per sale.

Good at: getting paid for a digital product this week, one-off or subscription, without
building billing. Bad at: being your entitlement system — see below. The alternative you'd
compare it against is Stripe direct; the deciding factor is whether you want to own tax,
invoicing and delivery.

## License keys are the integration

For anything gated, the product's licensing is the whole API surface you need. `POST
/licenses/verify` takes `product_id` + `license_key` and returns the purchase, and it is the
one endpoint that **needs no OAuth application** — so a desktop or client app can check a
key without you shipping credentials. There's also enable, disable, `decrement_uses_count`
and rotate (topic: *Licenses*).

Design around these, all from the verify response:

- **`uses` increments on every call by default.** `increment_uses_count` defaults to `"true"`,
  so a client that verifies on each launch inflates the count forever, and any seat limit you
  build on `uses` will strand a legitimate customer. Pass `"false"` for liveness checks and
  increment only on a real activation.
- **`success: true` does not mean entitled.** The purchase carries `refunded`, `disputed`,
  `chargebacked`, `subscription_ended_at`, `subscription_cancelled_at` and
  `subscription_failed_at`. A refunded buyer still verifies successfully. Check those fields
  or you're shipping a product that never revokes.
- **Subscriptions end in more than one way** — cancelled, failed payment, or a fixed term
  running out — and each sets a different field. Treat "has a valid key" and "is currently
  paying" as separate questions.
- **`is_multiseat_license`** exists; if you sell team plans, read seats from there rather
  than inventing your own convention.

## Ping is a trigger, not a data feed

Gumroad's webhook (`resource_subscriptions` in the API, "Ping" in the docs) has semantics
worth building against explicitly rather than discovering in production:

- **At-least-once, unordered.** A refund can arrive before the sale it reverses, and it
  carries the *same* `sale_id`. Deduplicate on `sale_id` **together with** `resource_name`,
  never `sale_id` alone.
- **The payload is unsigned**, and it's form-encoded, not JSON. So don't trust it as fact:
  take the `sale_id`, read the sale back through the API, and reconcile periodically against
  your own records (`../security.md`).
- **Retries give up.** A failed delivery is retried after 1 minute, 3, 10, and an hour, then
  stops — and only on 499/500/502/503/504. Any other non-2xx, a timeout, or a connection
  error is never retried. Your endpoint has **5 seconds**: acknowledge first, work after.
- **Subscribe per event.** There are eight resources — `sale`, `refund`, `dispute`,
  `dispute_won`, `cancellation`, `subscription_updated`, `subscription_ended`,
  `subscription_restarted` — each its own subscription. Wiring only `sale` is the common
  mistake; it's the one that leaves refunded customers with access.
- `subscription_updated` carries `old_plan`/`new_plan` and an `effective_as_of`, and a
  downgrade **takes effect at the end of the billing period**, not on receipt. Don't
  downgrade entitlements when the event lands.

## Scopes and secrets

OAuth scopes are narrow and worth using: `view_sales` (also required to subscribe to sales),
`edit_products`, `edit_sales`, `view_payouts`, `view_tax_data`, `mark_sales_as_shipped`.
`account` is broad but not universal — endpoints with a tighter boundary, like media, refuse
an account-only token (topic: *Scopes*).

The access token is a server-side secret, always. The one thing that may live in a client is
a license-key check, because verify needs no application credentials — and even then the
entitlement decision it feeds belongs on your server (`../security.md`).

## Checklist

- [ ] License verification server-side, with `increment_uses_count=false` for liveness checks
- [ ] Refunded / disputed / chargebacked / subscription-ended all revoke access
- [ ] Every relevant Ping resource subscribed, not just `sale`
- [ ] Ping handler idempotent on `sale_id` + `resource_name`, responding inside 5 seconds
- [ ] Ping treated as a trigger — sale re-read through the API before anything is granted
- [ ] Periodic reconciliation against your own records, for the pings that never arrive
- [ ] Access token server-side only, with the narrowest scopes that work
