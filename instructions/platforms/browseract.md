# BrowserAct

Load when: deciding whether a task needs a real browser driving a site that has no usable
API, and what that will cost. Building and running the workflows — nodes, credentials,
REST, gotchas, security — is in `browseract-workflows.md`.

Docs: **no capture bundled.** Capture `docs.browseract.com` into
`../../docs/references/browseract/` and index it (`../../docs/index.md`) — the topic
citations below then resolve to page ranges at read time. Until then verify against the live
docs (`../research.md`); cite topics by name, never pages.

## What it is

Cloud browser automation. You assemble a workflow on a canvas from nodes — Visit Page,
Click Element, Input Text, Extract Data, Loop List, Pagination, Condition, Human
Interaction — publish it, and run it from the dashboard, on a schedule through Make or n8n,
over REST, or as an MCP tool. Nothing runs locally.

Three concepts, and the docs are strict about them: a **workflow** is the blueprint, a
**node** is one browser action, a **task** is one execution — with its own inputs, step log
and screenshots, output (JSON, CSV, XML, Markdown) and credit cost.

## When to use it, when not to

- Good at: sites with no API where the data sits behind a login, a search box, or
  pagination; recurring extraction; giving an agent a browser job it can trigger over MCP.
- Bad at: anything the site already exposes as an API — you would pay credits per click for
  what one HTTP call returns. Also bad past roughly a thousand records per run (the docs
  recommend splitting, and warn that stability degrades well before ten thousand), and for
  anything that needs your own model: you get their web-automation engine, not a choice.
- The alternative you'd compare it against: Playwright you host yourself. The deciding
  factor is the tedious part — residential proxies, fingerprints, CAPTCHA handling, a
  credential vault. If the target site doesn't fight back, self-hosted Playwright is free.

## Cost model

- **Every action is metered: 1 action = 5 credits.** Navigate, click, input, extract, wait,
  back, scroll. Loops multiply — Loop is iterations × 5, Loop List is item count × 5. The
  docs' own example: ten products is roughly 5–10 steps, so 25–50 credits.
- **Credits don't roll over.** The monthly allocation expires at the cycle boundary. Spend
  order is daily bonus first (gone at midnight), then monthly, then permanent top-ups.
- Credit packs are tied to the *current* cycle too — bought the day before a reset, they
  last a day. Non-refundable, and not sold to free accounts at all.
- Monthly → yearly isn't a switch. You cancel, then buy the yearly plan.
- The ceiling is concurrency, not requests: 1 task for free accounts, 20 concurrent for
  paid. The API documents no rate limit.
- Verified 2026-08-10 from the snapshot — mechanics only. Plan prices aren't in the
  capture; check the live pricing page (`../research.md`).

## Checklist

- [ ] Credit burn estimated before a bulk run — actions × 5, and loops multiply
