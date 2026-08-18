# PocketHost

Load when: hosting the PocketBase instance on PocketHost. Default per `../core.md`.

Docs: **no capture bundled.** Capture `pockethost.io` into
`../../docs/references/pockethost/` and index it (`../../docs/index.md`) — the topic
citations below then resolve to page ranges at read time. Until then verify against the live
docs (`../research.md`); cite topics by name, never pages.

## What it gives you

Managed PocketBase: an instance, a subdomain, TLS, and the admin UI, without running a
server. You still get the PocketBase admin, `pb_hooks`, and `pb_migrations`.

## Cost — settled, don't re-raise it

**The user has unlisted free PocketHost plans.** Treat hosting as zero-cost here: it skips
the checkpoint's money question (`../profile.md`), and cost is no reason to prefer another
host. Worth saying because the public pricing page sells paid per-slot plans only, so every
session that reads it re-raises this correctly and pointlessly. Note the arrangement only
where silence would mislead — a setup doc telling the reader to go buy a slot is wrong.
Hibernation and the pooled storage cap still apply whatever the plan.

## What to design around

**Instances hibernate when idle.** The first request after idle pays a cold start (topics:
*Limits*, covering hibernation and usage limits). This matters for:
- Perceived speed on a landing page that hits the API on load — prefer static content that
  doesn't need the backend to render.
- Cron/scheduled hooks — a sleeping instance isn't running your scheduler. Don't build
  anything that depends on a job firing reliably on a schedule you don't control. Scheduled
  backups have the same hole: a missed interval is not replayed on wake.
- Webhooks from third parties — a cold start can push you past a sender's timeout. Senders
  that retry are fine; senders that don't will drop events.

**One instance, one region.** No horizontal scale, no failover. Fine for most projects,
disqualifying for anything needing availability guarantees. Say this out loud during the
stack decision.

**Disk is capped, pooled across the account, and lopsided.** The allowance is per slot but
shared account-wide, so a second instance spends the same budget. The database ceiling is
the far tighter of the two — file storage is generous by comparison, which means a project
storing no files gets no benefit from the half it was given and binds on the half it wasn't.
Large uploads to a small instance is the wrong shape: put files in R2 (see `cloudflare.md`)
and store references. And before promising anyone that a table "easily fits", measure one
real row with its indexes and divide — row count is the number that matters, and it is
never the one the plan quotes.

**Deployment is not git-based.** Hooks and migrations get pushed over SFTP or the `phio`
CLI, which has a deploy key and a CI example (topics: *SFTP file access*, *phio CLI*). Wire
that up rather than dragging files into a GUI client by hand. Keep the repo as the source of
truth and treat the instance as a deploy target, not the place where changes originate.
Schema edited in the admin UI without a committed migration will eventually be lost
(`pocketbase.md`). `phio` syncs `pb_*` and excludes `pb_data/**`, so a deploy moves schema
and hooks and can never overwrite the live database.

**A deploy does not apply a migration; the next start does.** PocketBase runs unapplied
migrations when it *serves*, so files landing on the instance change nothing until it
restarts. A hibernating instance applies them on its next wake, which hides the gap; one
that is already awake keeps serving the old schema until someone power-cycles it in the
dashboard. Build the deploy around that: wake it, then health-check it — a migration that
throws leaves PocketBase unable to start, and the failed health check is the only signal.

**There is no remote rollback.** SFTP is file access only — no shell, no `exec`, no
`migrate down` against the instance. Down migrations still belong in the repo and still get
round-trip tested locally, but the way back from a migration that already applied is
restore-from-backup. That is what makes backups non-optional here, and why additive
migrations (add a field, don't rename one) are worth the discipline: an additive mistake is
a dead field rather than an outage.

**Admin Sync makes the account password a database credential.** On by default, it copies
the PocketHost account login into the instance as its superuser. So the credential a CI job
needs for `phio` is also full admin on the data — scope the repo and rotate accordingly, and
check whether scoped account access keys exist before settling for the account password.

**JS hooks over Go.** Go extensions require compiling your own binary, which a managed host
may not accommodate. Plan on `pb_hooks` JS unless you've confirmed otherwise. The JSVM is
narrower than it looks — no promises or async, CommonJS only, no Node standard library, and
a partial ECMAScript surface (topic: *Extending PocketBase via JavaScript*). Read that
before designing a hook around anything asynchronous. If the project genuinely needs Go
extensions, raise it before choosing PocketHost.

## Operating

- Turn on backups and **test a restore** (topic: *Backing up and restoring*). Managed does
  not mean backed up the way you assume.
- Pin how you'll move between PocketBase versions before you need to (topic: *Changing
  PocketBase versions*) — upgrades are the host's, not yours.
- Keep a local PocketBase running the same version for development. Don't develop against
  production.
- Superuser MFA on, per PocketBase's production recommendations.
- Watch disk usage. Hitting the cap on a database is a bad failure mode.
- Set up an uptime check so you learn about downtime before a user tells you.

## When to move off

Name these in advance so the decision is made calmly, not during an outage:

- Sustained write concurrency SQLite can't take
- Availability requirements a single instance can't meet
- Storage growth past what the account's pooled allowance covers
- A need for Go extensions the host won't run

The exit path is a PocketBase instance on any VPS or container host — same binary, same
data. Low lock-in, which is part of why it's the default.

## Checklist

- [ ] Cold start acceptable for the actual usage pattern
- [ ] Nothing critical depends on a scheduled job on a sleeping instance
- [ ] Large files in object storage, not instance disk
- [ ] Migrations committed to the repo, applied to the instance
- [ ] Backups on, restore tested
- [ ] Disk and uptime monitored
- [ ] Current free-tier limits actually verified, not assumed

## Volatile claims

Pointers, not values (`../research.md`); `tools/staleness.py` reports them past their date.

- Free-tier instance limits and hibernation behavior — verify by 2026-11 against
  pockethost.io. The checklist above already refuses to assume them.
- Plan prices and what a paid tier changes — verify by 2026-11 against pockethost.io.
- Database and file-storage ceilings, and how they pool per account — verify by 2026-11
  against pockethost.io. Design against a measured row count, not a quoted size.
- Whether scoped account access keys exist for CI — verify by 2026-11 against pockethost.io.
  Until then the account password is the only documented CI credential, and it is superuser.
