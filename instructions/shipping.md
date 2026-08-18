# Shipping

Load when: deploys, environments, CI, releases, going live, or an open PR sits on the code
you're touching.

## Environments

- Local, preview, production. Preview per branch — Cloudflare Pages gives this via the
  GitHub integration for free (see `platforms/cloudflare.md`).
- Production data never reaches local or preview. Seed instead.
- Every environment-specific value comes from config, never a hardcoded conditional.
- `.env.example` lists every variable with a comment on what it's for and where to get it.
  Keep it current; it is the real setup documentation.
- Know which of your env vars are public (build-inlined) and which are secret
  (see `security.md`).

## Git

- Small commits with messages that say *why*. The diff says what.
- Branch per change. Never commit straight to the default branch.
- Never commit: secrets, build output, `node_modules`, local config, scratch files.
- Check `.gitignore` before the first commit.

## Open pull requests

Check what's already open before starting. If a PR covers what you're about to touch — same
feature, same files — that branch is where the work goes. Don't open a second one against
the same code.

Then keep it current as the work runs, without being asked each time:

- Commits land on the PR's branch as you make them, not in one drop at the end. A branch
  that lags behind the work is a PR nobody can review.
- When the scope moves, rewrite the title and body to match the diff. A description that
  still describes the first commit is worse than no description.
- **The description covers this repo's change and nothing else.** A session often spans two
  repos — this one attached beside the project it governs — and the sibling's story leaks
  in: what its PR did, which of its files moved, why its build went red. None of that is
  actionable by whoever reviews this diff, and it is stale the moment that branch moves.
  Where outside context genuinely justifies the change, state it in a line without naming
  the other repo or its PR.
- Deal with what the PR is stuck on: review comments, red CI, a base branch that moved
  underneath it. Push the fix, or say in the thread why it isn't yours to fix.
- A merged PR is finished. Follow-up work branches from the default branch instead — never
  stacked on merged history.

Updating a PR that is already open is automatic. Opening a new one isn't; that stays the
user's call.

## CI

Minimum useful pipeline: install → typecheck → lint → test → build. Fail the build on any
of them. A CI that can go green while broken is worse than no CI.

Add later, when they'd pay for themselves: preview deploy, Lighthouse budget, bundle-size
check, dependency audit.

Keep it under a few minutes. A slow pipeline gets bypassed.

## Before going live

- [ ] Runs from a clean clone with only `.env.example` as a guide
- [ ] Migrations tested forward, and tested backward — apply, roll back, apply again
- [ ] Backups configured and a restore actually tested (an untested backup is not a backup)
- [ ] Secrets set in the host, not in the repo
- [ ] Custom domain, HTTPS, redirects (www policy, trailing slash) settled
- [ ] 404 and 500 pages exist and match the design
- [ ] `robots.txt` correct — the classic launch bug is shipping `Disallow: /` from staging
- [ ] Error tracking on and verified with a deliberate test error
- [ ] Uptime check on the critical path
- [ ] Free-tier usage alerts set
- [ ] Rollback runbook written, and it runs the reverse migrations itself
      (`reversibility.md`)

## Releasing

- Ship small and often. A large release is a large blast radius.
- Migrations deploy separately from and before the code that needs them, and stay
  backwards-compatible for one release.
- Feature-flag anything risky.
- Watch errors for the first few minutes after deploy. Don't ship and walk away.
- Know how to roll back before you need to — the way back ships with the change, and a
  release that destroys anything is confirmed before it runs (`destructive-actions.md`).

## After

- Write down what broke and why. The same class of thing breaks twice otherwise.
- Update `.env.example` and the setup checklist when config changes (see `ux-admin.md`),
  and `docs/operations.md` per `documentation.md`.
- Delete the feature flag once the feature is permanent.
