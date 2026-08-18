# Reoon Email Verifier

Load when: checking whether an email address is worth sending to — signup forms,
redemption flows, list hygiene before a send.

Docs: **no capture bundled.** Capture the logged-in API Settings page at
`emailverifier.reoon.com` into `../../docs/references/reeonemailverifier/` and index it
(`../../docs/index.md`) — the topic citations below then resolve to page ranges at read time.
Until then verify against the live docs (`../research.md`); cite topics by name, never pages.

## What it is

A single-address verification API with two modes, plus a bulk endpoint and a WordPress
plugin. `GET /api/v1/verify?email=…&key=…&mode=quick|power` returns JSON: a `status`, a
set of named booleans, and the domain's MX records.

## The two modes, and why the choice is not close

| | QUICK | POWER |
|---|---|---|
| Time | < 0.5 s | seconds to **over a minute** |
| Checks | syntax, disposable, MX, domain accepts mail, invalid/expired domain, role account, spamtrap | all of that, plus individual inbox existence, inbox full, disabled, catch-all, an `overall_score` |
| Vendor's own recommendation | *"Best for: During user registration on your website"* | deep checks where waiting is acceptable |

**Quick, for anything a human is waiting on.** The docs are blunt about the trade:
*"Quick Mode does not check individual inbox status. If the domain, syntax and a few other
things are good, all emails including non-existing ones from that domain will be marked as
valid in quick mode."* So quick mode catches typos, throwaways and dead domains — it
cannot tell you a mailbox exists. Design around that rather than reaching for power mode,
because a minute-long request on a signup form is not a verification, it is an outage.

## Cost model

- **Credits**, tracked as two pools: `remaining_daily_credits` and
  `remaining_instant_credits`. `GET /api/v1/check-account?key=…` returns both, plus
  `api_status`.
- Verified 2026-08-09 from the docs snapshot: **limits and per-verification cost are not
  in the capture**. Check the account page for the current plan (`../research.md`).
- Poll the balance on a schedule, not per request. Running out mid-launch is silent
  otherwise — the API simply stops answering usefully while your form still submits.

## Key concepts

**Read the booleans, not just `status`.** Both modes return explicitly named flags —
`is_valid_syntax`, `is_disposable`, `is_role_account`, `mx_accepts_mail`, `is_spamtrap`,
`is_free_email`, and in power mode also `is_deliverable`, `is_disabled`, `has_inbox_full`,
`can_connect_smtp`, `is_catch_all`, `is_safe_to_send`, `overall_score`. They are
unambiguous and stable; a decision built on them survives a vocabulary change.

**`is_spamtrap` is the one worth refusing on.** A typo costs a buyer two minutes; sending
to a spam trap costs you sender reputation across every recipient.

**`is_role_account`** (`info@`, `support@`) is a signal, not a verdict. Plenty of
legitimate buyers use one.

**GET, not POST.** The key travels in the query string, which means it lands in any
intermediary's access log. Server-side only, and never from a browser.

## Gotchas

- **The `status` enum is truncated in the current capture.** The samples prove `"valid"`
  (quick) and `"safe"` (power); the comment listing the rest is cut off at the page edge.
  Do not branch on values you have not seen — use the booleans, or verify the enum live.
- **Quick mode says "valid" for addresses that do not exist.** Stated in the docs, easy to
  forget, and it is the difference between "this address is real" and "this domain would
  accept mail for it".
- **Catch-all domains cannot be resolved by anybody**, in either mode. Treat
  `is_catch_all` as "cannot tell", not as a pass.
- Pages 7–11 of the capture (bulk validation) hold no extractable text. Re-capture if you
  need the bulk endpoint.

## Security notes

- The API key authenticates by query parameter. Keep it server-side, rotate it if it ever
  appears in a log or a browser URL, and create a separate key per integration — the
  settings page supports several.
- Verification responses are deliverability intelligence about real people. Log the
  verdict, not the payload.
- A verifier is a dependency on somebody else's uptime in front of your signup form.
  Decide the failure policy before you need it: for a flow where the user has already
  paid, the only defensible answer is to let them through and record the address as
  unjudged.

## Checklist

- [ ] Quick mode for anything a user waits on; power mode only for offline work
- [ ] Decisions driven by the named booleans, not by unverified `status` strings
- [ ] Spam traps refused; role accounts allowed
- [ ] Key server-side only, never in a browser or a client-side URL
- [ ] Credit balance monitored on a schedule, and alerted on
- [ ] Failure policy decided: an outage or an exhausted balance must not block a paying
      customer
