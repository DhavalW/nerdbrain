# BrowserAct workflows

Load when: building, running or integrating a BrowserAct workflow — browser and proxy
modes, stored credentials, the REST API, MCP, callbacks. Whether to use BrowserAct at all,
and what it costs, is in `browseract.md`.

Docs: **no capture bundled.** Capture `docs.browseract.com` into
`../../docs/references/browseract/` and index it (`../../docs/index.md`) — the topic
citations below then resolve to page ranges at read time. Until then verify against the live
docs (`../research.md`); cite topics by name, never pages.

## Key concepts

**Browser mode decides whether the site sees a returning user.** Standard Browser keeps a
fixed browser ID with cookies, cache and history across runs — the only sane choice for
anything logged in. Private Browser starts clean and destroys everything afterwards.
Switching a workflow from Standard to Private wipes the stored data; the UI warns once.

**Proxy mode pairs with browser mode**, and the docs give a rule worth keeping: if the
account should look like the same user over time, use a static proxy with Standard Browser;
if you only care what the page shows right now, use their rotating residential pool with
Private Browser. Custom HTTP/SOCKS5 proxies are supported, with a Proxy Check that reports
the outbound IP and detected region before a run uses it.

**Credentials live in a vault, not in the workflow.** Credential Center holds the username,
password and a TOTP secret; you authorize a credential onto named workflows, then enable
*Use Stored Credentials* on the Start node. Authenticator apps only — email and SMS codes
are listed as coming, not shipped.

**Driving it over REST.** Bearer key in `Authorization`. `POST /v2/workflow/run-task` with a
`workflow_id` and `input_parameters` returns a `task_id`; poll `get-task-status` for the
status alone or `get-task` for steps, screenshots, output, credits and download files — or
pass `callback_url` / `status_change_callback_url` and be told. `stop-task` and
`resume-task` are PUTs, and a canceled task can't be resumed. Statuses: `created`,
`running`, `finished`, `canceled`, `pausing`, `paused`, `failed`, `unknown`.

**Browser state survives runs on purpose.** `save_browser_data: true` returns a `profile_id`
you can pass to a later run to reuse its cookies.

**Published is deployed.** MCP tools and integrations run the last *published* version of a
workflow — editing configuration without publishing changes nothing — and input parameters
freeze at publish, so changing them means a new version.

## Gotchas

- **Downloads expire twice over**: 50 MB per file, 100 files per run, retrievable for 30
  minutes after the run, deleted after seven days. Collect them in the job that ran the
  task, never in a nightly sweep. Hover-triggered downloads aren't supported at all.
- Put a Wait after each download trigger. Two downloads fired close together and the
  system keeps only the latest file.
- A task session is capped at seven hours.
- Callbacks must answer within 30 seconds; 5xx gets retried at most three times. Make the
  handler idempotent — retries mean duplicate deliveries.
- `Extract Data` reads a page or a whole list; `Extract Data Item` only works inside a Loop
  List. Picking the wrong one is the usual cause of "extracted no data" — the other two
  being content below the fold (add Scroll) and content still loading (add a short Wait).
- **Workflows break when the site's markup changes.** The docs' answer is to re-select the
  element and test weekly. That maintenance is the real cost of this approach; budget for it
  before promising anyone a reliable feed.
- CAPTCHA coverage (Cloudflare, reCAPTCHA, DataDome) is quoted at 95% auto-detected. Design
  for the other 5%: a blocked run is a normal outcome, not an exception.
- The docs themselves warn off automating production social accounts. Use dedicated ones.

## Security notes

- The API key is a bearer token with account scope — server-side only, no browser-safe
  variant, and it can spend credits. Keys don't expire; rotation is manual.
- Callback URLs must be publicly reachable, cap at 2048 characters, and private addresses
  are rejected. **The snapshot documents no signature on the callback**, so treat it as
  unauthenticated: use an unguessable path, and confirm the real outcome with `get-task`
  rather than trusting the body. Verify against the live docs before relying on this.
- Vaulted credentials are real logins with their 2FA seeds attached. A compromised
  BrowserAct account is a compromised LinkedIn account. Dedicated accounts, never a
  personal or admin one.
- Scraped output routinely contains personal data. What you keep and for how long is a
  checkpoint decision (`../core.md`), not something to settle by writing it to a bucket.

## Checklist

- [ ] Browser mode and proxy chosen deliberately — static plus Standard when logged in
- [ ] Credentials in Credential Center on dedicated accounts, never inline in a workflow
- [ ] Workflow republished after every config change; integrations run the published version
- [ ] Runs kept to ~1,000 records, larger jobs split across scheduled runs
- [ ] Downloads collected inside the 30-minute window
- [ ] Callback endpoint treated as unauthenticated; outcome confirmed via `get-task`
- [ ] API key server-side only, with a known rotation path

- [ ] Blocked runs, CAPTCHAs and markup changes handled as expected failures
