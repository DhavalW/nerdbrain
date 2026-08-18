# Testing

Load when: writing or changing code (tests ship with it) or reviewing a suite. Using the
suite as the halting signal for a long autonomous run is in `testing-gates.md`.


## Why the suite exists

Four jobs, in priority order:

1. **Catch regressions** — a change that breaks existing behavior fails loudly before
   anyone ships or builds on it.
2. **Enforce safety and security invariants** — the rules that must never regress
   (authorization, quotas, data integrity) are encoded as tests, not remembered.
3. **Catch bugs at the boundaries** — where they actually live.
4. **Gate long-running agents** — a green suite is a well-defined "safe to continue"
   signal; a red one is a stop sign that doesn't depend on judgment in the moment.

A suite that only proves the happy path does none of these.

## Tests ship with the change

- New behavior arrives with the tests that pin it. Not in a later commit.
- A bug fix arrives with a test that failed before the fix. No exceptions — this is the
  regression contract.
- Deliberately changed behavior updates its tests *in the same commit*, with the change
  called out in the commit message. A test silently edited to match new behavior is
  indistinguishable from a bug being institutionalized.
- Run the suite and report the real output (`core.md`). "Should pass" is not a result.

## What to test

- **Behavior, not implementation.** Assert what the caller observes, not the internals.
  Tests that break on refactors are a tax that teaches people to ignore failures.
- **Boundaries:** empty, one, many, malformed, too large, wrong type, the failure path.
  The happy path is the least interesting test in the file.
- **Contracts between pieces:** the API response shape the client relies on, the events a
  module emits, the schema a migration produces.
- **The way back:** a migration's down path is exercised, not assumed — apply, roll back,
  apply again, and assert the schema and data are what they were (`reversibility.md`).
- **Don't chase coverage numbers.** Cover what breaking would actually hurt. 100% coverage
  of getters proves nothing; one test on the money path proves a lot.
- Fast and deterministic. A flaky test is worse than no test — it trains everyone (and
  every agent) to rerun until green, which hides real failures. Fix or delete flakes;
  never learn to live with them.
- No test depends on another test's leftovers, wall-clock time, network weather, or order.

## Security and safety invariants

The suite is where `security.md` becomes enforceable. Encode the invariants that must
never regress:

- **Authorization:** every protected resource has a test calling it as an anonymous user
  and as a *different* authenticated user, asserting denial. For PocketBase, exercise the
  real API against the rules (`platforms/pocketbase.md`) — reading the rule expression is
  not a test.
- **Privileged fields:** a crafted request setting `role`, `plan`, `credits`, `owner`
  gets rejected — proven, not assumed.
- **Quotas and money:** exceeding a limit blocks; a forged price or webhook without a valid
  signature is refused; refund/revoke paths actually revoke.
- **Input handling:** the oversized payload, the injection-shaped string, the wrong
  content type — rejected at the boundary.

Mark these distinctly (a `security` tag, a dedicated file). They carry a stricter rule
than other tests: **weakening or deleting one is never a routine edit.** If one blocks
a change, that conflict goes to the user and the turn ends there — it is exactly the kind
of decision the checkpoint protocol exists for.


## Structure

- Mirror the source layout so the test for a thing is findable from the thing.
- One behavior per test, named as a sentence: `rejects expired codes at redemption`.
- Shared setup in fixtures/factories with safe defaults; each test states only what it
  cares about.
- Integration tests run against a real local instance (PocketBase runs fine locally —
  `platforms/pockethost.md`), never against production.
- The whole suite runs in CI on every push and fails the build on any failure
  (`shipping.md`). A suite that can be skipped will be.


## Checklist

- [ ] New behavior and bug fixes arrive with their tests, same commit
- [ ] Boundaries and failure paths covered, not just the happy path
- [ ] Security invariants encoded as tests, tagged, exercised via the real API
- [ ] Suite deterministic — zero known flakes

- [ ] Suite wired into CI, failing the build
- [ ] Real output reported, not "should pass"
