# Gumroad commercial mechanics

Load when: the question is money rather than code — fees, chargebacks, payouts, refund
policy, or localized pricing. The API integration is in `gumroad.md`.

Docs: **no capture bundled.** Capture the seller-facing `gumroad.com` help centre into
`../../docs/references/gumroad/` and index it (`../../docs/index.md`) — the topic citations
below then resolve to page ranges at read time. Until then verify against the live docs
(`../research.md`); cite topics by name, never pages.

## The commercial mechanics aren't in the API

Payout settings, refund policy, content protection and fees are help-centre material, not
endpoints. Two of them change how you build:

- **Chargebacks have account-level consequences.** Payouts are paused automatically above a
  1% chargeback rate, and past ~1% of *customers* disputing, Gumroad enforces a refund policy
  on the whole account. Make refunds easy in your own support flow; it's cheaper than a
  dispute.
- **Test purchases are free while logged in as the seller** — use that path, don't pay
  yourself with a card.

PPP prices are readable per country through the Products API, which is what you'd use to
show localized pricing on your own site.

## Checklist

- [ ] Fees and payout terms verified against the live help centre, not assumed

## Volatile claims

Pointers, not values (`../research.md`); `tools/staleness.py` reports them past their date.

- Platform fee, payout schedule and minimum payout — verify by 2026-11 against the live
  help centre.
- The chargeback rate that triggers an account-level refund policy — verify by 2026-11
  against the live help centre.
