# Tests as gates for autonomous runs

Load when: setting up or running a long autonomous run that uses the suite as its
stop/continue signal. What to test, and the determinism the gates depend on, is in
`testing.md`.

## Tests as halting points for long-running agents

For autonomous runs, the suite is the objective control loop:

- **Define the gates in the plan** (`planning.md`): each milestone ends at "suite green,
  including the new tests for this milestone." A gate is a defined place to stop, verify,
  and only then continue — not an interruption.
- **Green gate → proceed** to the next milestone without asking (`core.md`: no mid-task
  halts for things the checkpoint covered).
- **Red gate → stop building forward.** Diagnose. Three honest outcomes:
  1. The change is wrong → fix the change.
  2. The test is wrong or obsolete → update it, and say so explicitly in the commit.
  3. The failure reveals a genuine decision (behavior conflict, security invariant in the
     way, spec ambiguity) → finish what doesn't depend on it and take it to the user by the
     mid-task rule (`core.md`) — the form for an ambiguity, a written ask and an ended turn
     when the way forward would weaken a security invariant.
- **Never make a gate green by weakening it.** Deleting an assertion, loosening a
  tolerance, skipping a test, or hard-coding an expected value to the observed value is
  gate evasion, not progress. If the gate is genuinely wrong, changing it is a visible,
  stated decision — outcome 2 or 3, never a silent edit.
- An agent inheriting a project runs the suite *before* changing anything, so pre-existing
  failures aren't later attributed to its work. Note them up front.

This is why determinism matters (`testing.md`): a gate that flickers cannot halt anything.

## Checklist

- [ ] Gates defined per milestone for autonomous work
- [ ] No test weakened, skipped, or deleted to get to green without a stated decision
