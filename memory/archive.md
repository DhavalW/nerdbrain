# Archive

Finished entries retired from `observations.md` — shipped into a pack, or declined and gone
quiet. Same format, same ids, never renumbered.

Nothing here is deleted. A declined entry is the record that stops it being re-proposed;
removing it re-opens the loop it closed. This file is not read on the normal path, so it
can grow without costing anyone context.

The entries below are the provenance of rules already written into the packs — each one is
why a line in this repo says what it says.

### obs-0001 — 2026-08-12
- **Observation:** Treat recording an observation and granting it authority as two steps:
  writing it down needs no approval, acting on it does.
- **Rests on:** stated outright (2026-08-12)
- **Target:** `../instructions/learning.md`
- **Status:** shipped

### obs-0002 — 2026-08-12
- **Observation:** Where approval can be expressed by merging a pull request, merging is
  the yes and closing is the no — one approval channel that works while the user is away.
- **Rests on:** stated outright (2026-08-12)
- **Target:** `../instructions/learning.md`
- **Status:** shipped

### obs-0003 — 2026-08-12
- **Observation:** When a convention has proved worth keeping, make it a check rather than
  a paragraph — an unchecked standard drifts, and nobody notices until it has.
- **Rests on:** seen 3 times (2026-08-12)
- **Target:** `../instructions/meta-rules.md`
- **Status:** shipped

### obs-0010 — 2026-08-13
- **Observation:** Weigh a change to this repo's foundations — entry point, router, gate,
  ledger format, approval path, always-loaded set — thoroughly before proposing it, not
  after, because everything built afterwards inherits it.
- **Rests on:** stated outright (2026-08-13)
- **Target:** `../CLAUDE.md`
- **Status:** shipped

### obs-0013 — 2026-08-13
- **Observation:** A tool that reports a machine's status code to a human has not
  reported anything — lead with the consequence in plain words, keep the code as a
  footnote, and name the next step.
- **Rests on:** seen once (2026-08-13)
- **Target:** `../instructions/copy.md`
- **Status:** shipped

### obs-0015 — 2026-08-13
- **Observation:** A pack governs the software being built, not the session building it —
  "the user" in a rule means whoever ends up using the artifact, so a safety rule about
  untrusted input never becomes grounds to refuse an instruction from the person you are
  working with.
- **Rests on:** stated outright (2026-08-13)
- **Target:** `../instructions/index.md`
- **Status:** shipped

### obs-0017 — 2026-08-15
- **Observation:** Commit a config file with its schema's full shape — every field written
  out, unset values as explicit `null`, never left to a schema default or collapsed to a
  bare `null` block — and read "configured" from whatever resolves the config rather than
  from the raw file, because a filled-in shape silently flips any presence check.
- **Rests on:** stated outright (2026-08-15)
- **Target:** `../instructions/ux-admin.md`
- **Status:** shipped

### obs-0019 — 2026-08-14
- **Observation:** When approval is needed for a list of items, put it somewhere the user
  can act on it later — persistent, tickable, outside the turn — rather than in a prompt
  that must be answered while the session waits.
- **Rests on:** stated outright (2026-08-14)
- **Target:** `../instructions/learning.md`
- **Status:** declined

### obs-0020 — 2026-08-14
- **Observation:** When a session works from an instructions repo attached beside the
  project, mark everything belonging to the instructions repo in one fixed, visually
  distinct block, so meta-work is separable at a glance from the work itself.
- **Rests on:** stated outright (2026-08-14)
- **Target:** `../instructions/profile.md`
- **Status:** shipped

### obs-0021 — 2026-08-14
- **Observation:** A rule promoted into a pack should keep a pointer to the evidence that
  produced it, because without provenance a rule from one sighting is indistinguishable
  from one proved ten times, and neither can be retired on evidence later.
- **Rests on:** seen once (2026-08-14)
- **Target:** `../instructions/meta-rules.md`
- **Status:** shipped

### obs-0035 — 2026-08-17
- **Observation:** On PocketBase, `required: true` on a number field means "must not be
  zero", not "must be present" — any numeric field where zero is a legitimate value has to
  be left non-required or it rejects a valid write.
- **Rests on:** seen once (2026-08-17)
- **Target:** `../instructions/platforms/pocketbase.md`
- **Status:** shipped

### obs-0036 — 2026-08-17
- **Observation:** Record the response shapes a vendor's client is most often assumed wrong
  — a pack that only says "read the docs" is followed by a client that didn't, and the
  balance-check endpoint is the one whose wrong shape fails before any work is done.
- **Rests on:** seen once (2026-08-17)
- **Target:** `../instructions/platforms/keywords-everywhere.md`
- **Status:** shipped

### obs-0041 — 2026-08-17
- **Observation:** Write a status report for a reader who is not reading the code — what
  changed and what it means for them, never the mechanism; the technical register of the
  work leaks into the reply unless the report is deliberately written for someone outside it.
- **Rests on:** seen once (2026-08-17)
- **Target:** `../instructions/profile.md`
- **Status:** shipped

### obs-0042 — 2026-08-17
- **Observation:** A writing rule with no check at the moment of sending gets broken without
  anyone noticing — require an explicit self-declared pass/fail in the output itself, so the
  rule is looked at when it is being broken and a skipped check is visible to the reader.
- **Rests on:** seen once (2026-08-17)
- **Target:** `../instructions/profile.md`
- **Status:** shipped
