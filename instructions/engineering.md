# Engineering

Load when: writing or changing non-trivial code.

## Standard

Production-grade means: someone else can read it, it fails in ways you predicted, and it
doesn't need you present to work. Prototype-grade is a legitimate choice — but it should be
a stated choice, not an accident.

## Match the codebase

Before writing, read enough to know the local idiom: naming, file layout, error handling,
test style, comment density. New code should be indistinguishable from good existing code.
Your preferences lose to the project's conventions.

## Rules

**Errors**
- Handle the failure you can actually recover from. Let the rest bubble with context.
- No silent catches. An empty `catch {}` is a bug you're hiding from yourself.
- Error messages say what failed, what was expected, and what to do. Include the value.
- Fail fast at boundaries. Validate input where it enters the system, then trust it inside.

**State and data**
- One source of truth per fact. Derived state is derived, not stored and hoped to be in sync.
- Make invalid states unrepresentable where the language lets you.
- Nothing partially applied: an operation either completes or leaves things as they were.
- Every change has a way back — the down path is written with the forward one, and nothing
  destructive runs without a confirmation (`destructive-actions.md`).

**Async**
- Everything that crosses the network gets a timeout.
- Retries only for genuinely transient failures, with backoff, with a cap. Never retry a
  non-idempotent write blindly.
- Handle the loading, empty, error, and success states. All four. Every time.
- Cancel in-flight work when the thing that asked for it goes away.

**Structure**
- Function does one thing. If the name needs "and", split it.
- Duplication is cheaper than the wrong abstraction. Wait for the third instance.
- Dependencies point inward: UI depends on logic, logic doesn't depend on UI.
- Delete dead code. Don't comment it out. Git has it.

**Dependencies**
- Every one is a liability: bundle size, supply chain, breakage, upgrade tax.
- Ask: could this be 30 lines? Is it maintained? What's its dependency tree?
- Say so before adding one that isn't obviously warranted.

**Comments**
- Comment *why*, never *what*. The code says what.
- Document the non-obvious: the workaround, the ordering constraint, the reason for the
  weird-looking line, the link to the issue.
- No comment restating the function signature. No banner headings for two-line files.

## A guard covers a route, not an outcome

Building something to prevent an outcome is not the same as preventing it. List the routes
to that outcome and say which one the guard actually reaches; whatever is left over is not
covered by the guard existing, and needs a rule in words instead. Write that rule as an
instruction to whoever must obey it — "never do X" — never as a description of what the
guard does, because a description binds nobody on the paths the guard does not run
(obs-0055).

Do this while shipping the guard, not later. A gap in coverage is invisible from inside the
part that works, so it surfaces when somebody thinks to ask — and mostly nobody does.

## Testing

Full rules in `testing.md` — load it whenever code changes. The short version: tests ship
in the same commit as the change, a bug fix gets a test that failed before the fix, and
the suite's real output gets reported. "Should pass" is not a result.

## Before saying done

- [ ] It runs
- [ ] Tests pass, and you ran them
- [ ] Linter/typechecker clean
- [ ] No leftover debug logging, commented code, or scratch files
- [ ] No secrets, no hardcoded env-specific values
- [ ] Failure paths handled, not just the happy one
- [ ] Anything you couldn't verify is stated plainly
