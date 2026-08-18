<!--
Drop-in for a project that should pick up these instruction packs automatically,
without anyone typing /nerdbrain.

  cp ~/.nerdbrain/templates/CLAUDE.md ./CLAUDE.md

Then fill in the project-specific section at the bottom and delete this comment.
If the project already has a CLAUDE.md, paste just the "Instructions" block into it.
-->

# <Project name>

## Instructions

This project follows the instruction packs in the `nerdbrain` repo.

**At the start of a session, and before any non-trivial work:**

1. Locate the repo: `$NERDBRAIN_HOME`, else `~/.nerdbrain`. If neither exists, clone
   `https://github.com/dhavalw/nerdbrain.git` to `~/.nerdbrain`. If it can't be reached, say so
   in one line and carry on without it.
2. Read `instructions/index.md` (the router) and `instructions/core.md` (always applies).
3. Load the packs the router table matches to the task. Two to four, not all of them.
4. Read `docs/index.md` before opening any vendor PDF — it maps topics to page ranges.
5. Re-consult the router whenever the work turns into a different kind of work — a new
   surface, a new concern (auth, payments, user-visible copy), a new platform — and load
   only what is newly matched. Never read the same pack twice in a session; what's already
   in context still applies.

The `/nerdbrain` skill does all of this if it's installed, and so does attaching the
`nerdbrain` repo to the session — its own `CLAUDE.md` carries the same protocol.

**The rule that matters most, from `instructions/core.md`:** every question for me goes in
one batch at the very start — options, tradeoffs, a marked recommendation — written out in
the reply, and then you stop and wait. Not a pop-up form: those time out, and my silence is
never a yes. I may need hours to answer; the questions wait that long. Ask the cheap ones
here too if my answer would help — I'd rather decide everything at once and then go do
something else while you build.

Anything you discover later, ask through the form and keep moving: if it times out, take
the recommendation and log the assumption for me to review at the end. The exception is
anything destructive or expensive to reverse — that one waits for me no matter how long.

Precedence: what I say in conversation > this file and the existing code > platform packs >
type packs > topic packs > `instructions/core.md`.

## This project

<!-- Delete what doesn't apply. Anything here overrides the packs. -->

- **What it is:**
- **Architecture:** <!-- chosen template from instructions/architectures/, + deviations -->
- **Stack:** <!-- chosen template from instructions/stacks/, + deviations -->
- **Design theme:** <!-- chosen template from instructions/themes/, + deviations -->
- **Deployed to:**
- **Run locally:** `<command>`
- **Tests:** `<command>`
- **Deploy:** `<how>`

### Conventions specific to this project

<!-- Only things that differ from the packs. Don't restate them. -->

### Gotchas

<!-- The things that would cost someone an afternoon. -->
