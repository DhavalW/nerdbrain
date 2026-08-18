# Keywords Everywhere API

Load when: pulling keyword, traffic, or backlink data — SEO tooling, content planning,
competitor research.

Docs: **no capture bundled.** Capture `api.keywordseverywhere.com` into
`../../docs/references/keywordseverywhere/` and index it (`../../docs/index.md`) — the topic
citations below then resolve to page ranges at read time. Until then verify against the live
docs (`../research.md`); cite topics by name, never pages.

## What's in the docs

Endpoints for keyword data (volume, CPC, competition, trend), credit balance, valid
countries and currencies, "People Also Search For", related keywords, domain keywords,
URL keywords, URL traffic metrics, and domain backlinks — plus an MCP server integration
section with per-client setup, if querying it as a tool beats writing a client. Find each
in the doc index.

Each endpoint section follows the same shape: request body params → status codes →
success response fields → sample success → sample error responses. Map your response
handling from the endpoint's own fields section — they differ between endpoints.

## It costs credits

This is the design constraint. Every call spends a metered balance, so the client is not a
thin HTTP wrapper — it's a budget manager.

- **Cache everything, aggressively.** Search volume changes monthly at best, so a 24-hour
  cache is conservative and a week is often fine. On disk or in KV, keyed by
  keyword + country + currency.
- **Deduplicate before calling.** Normalize case and whitespace, drop repeats, and check the
  cache — across the whole batch, not per item.
- **Batch.** The keyword endpoints take many keywords per request, and one batched request
  is nothing like the same latency as one request each.
- **Check the balance before a large job** (credit-balance endpoint) and fail loudly with
  the number rather than burning through the remainder halfway.
- **Handle 402 explicitly.** Insufficient-credit responses are documented per endpoint. A
  credits-exhausted failure needs a different user message from a network failure
  (`../copy.md`).
- **Never retry a 402 or a 401.** Retrying a paid call that failed for a non-transient
  reason spends credits for nothing.

## The three shapes that get assumed wrong

"Read the endpoint's section first" is above and is the rule; these are here because a client
written against this pack skipped it and got all three wrong, and the first fails before any
work is done. Fires when: writing or reviewing a client for this API. Enforced by: review
question against the doc index, per endpoint (obs-0036).

- **The credit-balance endpoint answers a bare array with the balance as its only element**
  — `[95597755]` — not an object with a `credits` key. This is the preflight call, so an
  object-shaped assumption throws on the first real request of any job.
- **The keyword endpoints cap how many keywords one call accepts** (value in Volatile
  claims). Enforce it client-side and chunk past it — it is documented, so exceeding it is a
  client bug, and a 4xx after the spend is committed is the wrong place to find out.
- **The keyword response reports what the call actually cost and what remains.** Log those,
  never a count of the keywords you sent — only the provider's number is evidence, and an
  inferred spend produces a ledger that is merely plausible.

## Keys

**The API key is a secret with a balance attached.** It cannot go in client-side code —
anyone who reads it can drain it. This is a textbook case for a server-side proxy per
`../stack-and-architecture.md`: a Worker holds the key, enforces your own per-user quota,
and caches responses (`cloudflare.md`).

If you're building a tool that lets *users* supply their own key, store it encrypted, mask
it in the UI, and never log it (`../ux-admin.md`, `../security.md`).

## Response handling

- Volume data is monthly and historical; label it with its period in the UI rather than
  presenting it as live.
- Missing data is normal — long-tail keywords legitimately return zero or null. Distinguish
  "no data" from "error" in the interface.
- Country and currency must be valid values from the countries/currencies endpoints.
  Validate before spending a call.

## Checklist

- [ ] Key server-side only, never in client code
- [ ] Cache layer in front of every endpoint
- [ ] Dedupe and batch before calling
- [ ] Balance checked before large jobs
- [ ] 402 and 401 handled distinctly, and never retried
- [ ] Per-user quota enforced if users share your key
- [ ] Country/currency validated against the documented lists
- [ ] "No data" distinguished from "failed"

## Volatile claims

Pointers, not values (`../research.md`); `tools/staleness.py` reports them past their date.

- Credit prices and the credit cost per endpoint — verify by 2026-11 against the live
  pricing page. Credits are the entire cost model, so a stale number misprices the design.
- Maximum keywords per call, in the keyword endpoint's own section; verify by 2027-02
  against the doc index. Chunk to what it says — a ceiling copied into code outlives the
  doc that set it.
