# Observations

The live ledger. Format, lifecycle and the rules for writing here: `index.md`.

Newest last. Ids are permanent — never reuse one, even after an entry is archived.

**Forking this repo?** These entries came with it. Nothing here governs anything, so they
cost you nothing sitting there — but they are candidate rules drawn from someone else's
evidence, and the honest thing to do with a rule you have no evidence for is decline it.
Clear the file entirely if you would rather start from your own work; that is a supported
starting state, not a broken one.

### obs-0004 — 2026-08-12
- **Observation:** A budget ratchet needs headroom to work; at zero headroom it stops
  measuring growth and starts blocking the next legitimate addition.
- **Rests on:** seen once (2026-08-12)
- **Target:** unplaced
- **Status:** open

### obs-0005 — 2026-08-12
- **Observation:** Prefer a new file and a deliberate budget raise over trimming rules the
  user already approved to make room for a new one.
- **Rests on:** stated outright (2026-08-12)
- **Target:** `../instructions/learning.md`
- **Status:** open

### obs-0011 — 2026-08-13
- **Observation:** In any repo the user's future work depends on, treat a change to its
  foundations as a checkpoint decision every time, and test the premise against what
  actually depends on it before the proposal is made.
- **Rests on:** stated outright (2026-08-13)
- **Target:** `../instructions/planning.md`
- **Status:** open

### obs-0008 — 2026-08-13
- **Observation:** Exempt the guaranteed-read entry point from the modularity standard that
  governs the files it points at — moving a foundational rule behind a pointer to save
  context trades a certainty for a small saving.
- **Rests on:** seen once (2026-08-13)
- **Target:** `../instructions/documentation.md`
- **Status:** open

### obs-0009 — 2026-08-13
- **Observation:** Before splitting a file at an apparent seam, check what each half writes
  to — a rule the file already states twice is evidence that both halves need it and the
  seam is not real.
- **Rests on:** seen once (2026-08-13)
- **Target:** unplaced
- **Status:** open

### obs-0007 — 2026-08-13
- **Observation:** When a feature's only working path runs on optional infrastructure —
  a scheduled job, a credential, a webhook — build the manual path too, because the
  unconfigured state is the one it will spend most of its life in.
- **Rests on:** stated outright (2026-08-13)
- **Target:** `../instructions/engineering.md`
- **Status:** open

### obs-0006 — 2026-08-12
- **Observation:** An efficiency claim written into a comment is a factual claim — verify
  what the optimization actually saves, or describe the mechanism without the number.
- **Rests on:** seen once (2026-08-12)
- **Target:** `../instructions/research.md`
- **Status:** open

### obs-0012 — 2026-08-13
- **Observation:** When a copy rule is mechanically checkable — a banned character, a
  banned word, a required tag — write it as a test in the repo that holds the rule
  instead of leaving it on a checklist someone has to remember.
- **Rests on:** seen once (2026-08-13)
- **Target:** `../instructions/copy.md`
- **Status:** open

### obs-0014 — 2026-08-13
- **Observation:** Assume the reader of an interface is a layman in the subject it
  covers, even when the buyer is technical: plain sentence first, the technical term and
  the raw evidence as subtext underneath it.
- **Rests on:** stated outright (2026-08-13)
- **Target:** `../instructions/copy.md`
- **Status:** open

### obs-0016 — 2026-08-14
- **Observation:** Pushing commits updates a pull request's diff, never its title or
  body — treat a PR appearing mid-session as a turn that re-routes to
  `../instructions/shipping.md`, and never report a PR as updated on the strength of
  a push.
- **Rests on:** seen once (2026-08-14)
- **Target:** `../instructions/shipping.md`
- **Status:** open

### obs-0018 — 2026-08-14
- **Observation:** Before designing an approval or input surface on a hosted page, verify
  the platform can persist the answer back somewhere an agent reads — a page that collects
  a decision it cannot return is a dead end, and assuming the capability is inventing an API.
- **Rests on:** seen once (2026-08-14)
- **Target:** `../instructions/research.md`
- **Status:** open

### obs-0022 — 2026-08-15
- **Observation:** A quota on a stage that costs nothing to run is not a guardrail — bound
  one run, never a calendar period, because a period cap whose backlog outgrows it leaves
  the pipeline permanently and silently working on a subset.
- **Rests on:** seen once (2026-08-15)
- **Target:** `../instructions/engineering.md`
- **Status:** open

### obs-0023 — 2026-08-15
- **Observation:** Meter a budget against the artefact the work produced, never against a
  log of what each run intended, because two runs racing on the same batch write two
  intentions and produce one artefact.
- **Rests on:** seen once (2026-08-15)
- **Target:** `../instructions/engineering.md`
- **Status:** open

### obs-0024 — 2026-08-15
- **Observation:** When a scheduled job graph encodes a dependency order, assert that order
  in a test — an order expressed only as dates or times is a comment, and it drifts silently
  the first time a stage moves.
- **Rests on:** seen once (2026-08-15)
- **Target:** `../instructions/testing.md`
- **Status:** open

### obs-0025 — 2026-08-15
- **Observation:** A file a stage writes but its deploy step never persists is worse than a
  missing feature, because every consumer reads its absence as a valid answer; check that
  each declared output is actually covered by a commit or upload path.
- **Rests on:** seen once (2026-08-15)
- **Target:** `../instructions/shipping.md`
- **Status:** open

### obs-0026 — 2026-08-15
- **Observation:** Profile before optimising and record what you measured, including the
  optimisation that turned out slower — an unmeasured guess about a hot path sends the next
  session down the same wrong branch.
- **Rests on:** seen once (2026-08-15)
- **Target:** `../instructions/engineering.md`
- **Status:** open

### obs-0027 — 2026-08-15
- **Observation:** Before designing on a managed platform's storage allowance, measure one
  real row with its indexes and convert the cap into a row count — a plan that reasons in
  megabytes hides the ceiling until the data is already there.
- **Rests on:** seen once (2026-08-15)
- **Target:** `../instructions/stack-and-architecture.md`
- **Status:** open

### obs-0028 — 2026-08-15
- **Observation:** Treat "the files are deployed" and "the change is live" as separate
  states whenever a platform applies changes on its own restart — name what triggers the
  apply, and make the deploy verify it rather than reporting success on upload.
- **Rests on:** seen once (2026-08-15)
- **Target:** `../instructions/shipping.md`
- **Status:** open

### obs-0029 — 2026-08-15
- **Observation:** When a deploy credential doubles as an admin credential on the same
  platform, say so where the secret is configured — the scope a token carries is invisible
  at the point someone pastes it into CI.
- **Rests on:** seen once (2026-08-15)
- **Target:** `../instructions/security.md`
- **Status:** open

### obs-0030 — 2026-08-15
- **Observation:** A generated artifact that a scheduled job commits must derive every field
  from its inputs — one wall-clock timestamp turns "commit only if changed" into a commit
  every run, and the rebuild it triggers looks like real activity.
- **Rests on:** seen once (2026-08-15)
- **Target:** `../instructions/engineering.md`
- **Status:** open

### obs-0031 — 2026-08-17
- **Observation:** A per-run cap and a period budget are different limits, and enforcing
  only the first leaves the second decorative — a run-sized ceiling passes its own check on
  every run while the schedule multiplies it past the annual one, so any spend path with a
  stated period allowance needs something that sums actual spend against it before the call.
- **Rests on:** seen once (2026-08-17)
- **Target:** `../instructions/engineering.md`
- **Status:** open

### obs-0032 — 2026-08-17
- **Observation:** A long-running job needs a heartbeat, not only a progress counter — when
  the slow part is one call rather than many, a reporter that speaks on completion goes
  silent exactly when a watcher most needs evidence the job is alive.
- **Rests on:** seen once (2026-08-17)
- **Target:** `../instructions/ux-admin.md`
- **Status:** open

### obs-0033 — 2026-08-17
- **Observation:** Never import another system's bulk action as a per-item human judgement —
  check how the source records a verdict before trusting the count, because a select-all
  sweep and a reviewed decision are the same field, and a permanence rule turns the mistake
  into one with no way back.
- **Rests on:** seen once (2026-08-17)
- **Target:** `../instructions/engineering.md`
- **Status:** open

### obs-0034 — 2026-08-17
- **Observation:** Verify a client against the vendor's captured docs before its first real
  call, not after — a response shape assumed from what the endpoint "obviously" returns
  fails on the very first request, and for a preflight check that is the request standing
  between a run and spending money.
- **Rests on:** seen once (2026-08-17)
- **Target:** `../instructions/research.md`
- **Status:** open

### obs-0037 — 2026-08-17
- **Observation:** An algorithm proven on the data you have is unproven on the data you are
  about to import — re-measure the clustering, the join or the sort against a realistic
  corpus before treating that phase as done, because the failure is usually a collapse
  rather than a slowdown.
- **Rests on:** seen once (2026-08-17)
- **Target:** `../instructions/engineering.md`
- **Status:** open

### obs-0038 — 2026-08-17
- **Observation:** Test an optimization against the naive implementation it replaces, on
  random inputs and not only a hand-picked fixture — a filter derived from per-item maths is
  where the asymmetric case hides, and a curated corpus will not contain it.
- **Rests on:** seen once (2026-08-17)
- **Target:** `../instructions/testing.md`
- **Status:** open

### obs-0039 — 2026-08-17
- **Observation:** Alert on faults and never on guards firing — a limit refusing is a
  decision working, and an alert that fires on decisions is one nobody reads by the second
  week, so route refusals to a summary and reserve the notification for what broke.
- **Rests on:** seen once (2026-08-17)
- **Target:** `../instructions/ux-admin.md`
- **Status:** open

### obs-0040 — 2026-08-17
- **Observation:** When two bootstrap scripts touch the same rows, make each one assert the
  state it needs rather than documenting an order — an "already exists, leaving it alone"
  branch silently keeps whatever the other script wrote, and an ordering nobody can enforce
  is not a fix.
- **Rests on:** seen once (2026-08-17)
- **Target:** `../instructions/engineering.md`
- **Status:** open

### obs-0043 — 2026-08-17
- **Observation:** Semantic understanding is a language model's job, not an algorithm's —
  when code needs to know what text *means*, call a model; deterministic methods may only
  pre-filter to cut the workload, and only where the filter provably drops nothing a model
  would have accepted.
- **Rests on:** stated outright (2026-08-17)
- **Target:** `../instructions/engineering.md`
- **Status:** open

### obs-0044 — 2026-08-17
- **Observation:** Give model-backed work a provider chain rather than one hardcoded
  vendor — local model, hosted API, and a deferred batch path — each declaring what it can
  do, with the order and per-provider limits configurable by the owner rather than by a
  redeploy.
- **Rests on:** stated outright (2026-08-17)
- **Target:** `../instructions/stack-and-architecture.md`
- **Status:** open
