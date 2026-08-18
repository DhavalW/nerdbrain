# Emailit

Load when: an app has to send transactional mail (magic links, receipts, license
delivery), or has to check whether an address is real before relying on it.

Docs: **no capture bundled.** Capture `emailit.com` into `../../docs/references/emailit/`
and index it (`../../docs/index.md`) so the topic citations below resolve to page ranges.
Until then verify against the live docs (`../research.md`); cite topics by name, never pages.

## What it is

A REST + SMTP mail API with a v2 JSON interface, per-workspace API keys, signed webhooks,
templates with aliases and draft/publish versioning, suppression lists, and a real-time
email verification endpoint. One vendor covers both halves of "send the mail" and "is this
address worth sending to".

## When to use it, when not to

- Good at: transactional sending from your own domain, plus deliverability checking in the
  same account and the same API key.
- Bad at: anything needing more than 5,000 sends a day without a support conversation, or
  bulk campaign sending at short notice — the daily limit is a warm-up mechanism, not a
  formality.
- The alternative you'd compare it against: Resend or Postmark for sending, ZeroBounce or
  NeverBounce for verification. The deciding factor is whether one vendor for both is worth
  more than best-in-class at either.

## Cost model

- **2 requests per second** on every endpoint, workspace-wide, shared across API keys and
  SMTP. Over it, `429`.
- **5,000 emails per day** to start, across API, SMTP and campaigns, reset at midnight UTC.
  Raised by contacting support once you have a sending record, not by a plan toggle.
- The verification endpoint documents a `402` response, so it is credit-metered. **Prices
  are not in the snapshot** — verify against the live pricing page before committing
  (`../research.md`).
- Verified 2026-08-09 from the docs snapshot; limits only, no prices.

## Key concepts

**Verification is a real check, not a regex.** `POST /email-verifications` returns
`result` (`safe`, `invalid`, `disposable`, `disabled`, `inbox_full`, `unknown`), a `risk`
band with a 0–100 `score`, and a `checks` object breaking out syntax, MX, SMTP connect,
disposable, role account, catch-all, gibberish and domain age. `mode: "fast"` skips SMTP
probing and returns `null` for the fields that need it.

**Idempotency is offered, so use it.** `POST /emails` takes an `Idempotency-Key` header
that suppresses duplicate sends for 24 hours. Anything that sends mail from a retried
handler needs it.

**Templates carry an alias and versions.** Creating a template with an existing alias adds
a version rather than colliding; drafts publish explicitly. That is the staging story —
you do not need a second account for it.

**Suppressions are first-class.** Bounces and complaints land in a suppression list you can
read, add to, and expire (`keep_until`). Treat it as the source of truth for "stop mailing
this address", not your own bounce counter.

## Gotchas

- **The daily limit is shared across every sending path.** A campaign can eat the quota a
  transactional magic link needed an hour later. Reserve headroom deliberately.
- **A domain is only verified when every required DNS record passes**, and the docs say
  propagation can take hours. This is the step that delays a launch, so do it first.
- Sending domains need DKIM, SPF/return-path and (for click and open tracking) a CNAME.
  Tracking silently does nothing until that record resolves.
- `to`, `cc` and `bcc` cap at 50 recipients each.
- Fast-mode verification returns `null`, not `false`, for the SMTP-dependent fields.
  Treating `null` as "no" marks good addresses bad.

## Security notes

- The API key is a bearer token with workspace scope. Server-side only — there is no
  browser-safe variant, and a leaked key can send from your domain.
- Webhooks are signed: `X-Emailit-Signature`, HMAC-SHA256 over the raw body. Verify it in
  constant time before parsing, and answer 2xx quickly — delivery retries on a backoff
  schedule, so handlers must be idempotent as well as fast.
- Webhook URLs are validated against SSRF on creation, which does not remove your own
  obligation to authenticate the endpoint.
- Verification responses carry deliverability intelligence about real people. Log the
  verdict, not the payload.

## Checklist

- [ ] Sending domain verified — every required DNS record green, checked, not assumed
- [ ] API key server-side only, rotated out of any place it was pasted during setup
- [ ] `Idempotency-Key` on every send that can be retried
- [ ] Webhook signature verified in constant time; handler idempotent and fast
- [ ] Daily-limit headroom reserved for transactional mail
- [ ] Suppression list honoured before sending, not after bouncing
- [ ] Verification failure policy decided: `unknown` and provider outages must not block a
      user who has already paid

## Volatile claims

Pointers, not values (`../research.md`); `tools/staleness.py` reports them past their date.

- Daily sending limits and the warm-up thresholds — verify by 2026-11 against the live
  docs; the snapshot carries limits as of its capture date and no prices at all.
- Verification pricing behind the credit-metered endpoint — verify by 2026-11 live.
