---
name: nerdbrain
description: Load your nerdbrain instruction packs, doc index, and architecture/stack/theme template menus from the nerdbrain repo, then apply the router rules to the current task. Use when the user types /nerdbrain, or asks to load their instructions, standards, preferences, house rules, templates, or the docs for a platform they have a pack for. Also use at the start of a new project or feature to present the template menus and pick up the ask-before-building rules, and before starting a task in any session where the nerdbrain repo is attached as a reference alongside another repo — route the task through the packs before working on it.
---

# nerdbrain

Connects this session to the `nerdbrain` repo and loads the right instruction packs for
whatever is being worked on. The user should not have to attach the repo manually.

## 1. Find the repo

Resolve in this order and stop at the first hit:

1. An `nerdbrain` checkout already attached to this session — its `CLAUDE.md` is in your
   context, so the repo is on disk; use that path and skip the refresh
2. `$NERDBRAIN_HOME`, if set and it contains `instructions/index.md`
3. `~/.nerdbrain/instructions/index.md`
4. `./instructions/index.md` — you may already be working inside the repo
5. Not found → clone it (next step)

```bash
NERDBRAIN="${NERDBRAIN_HOME:-$HOME/.nerdbrain}"
[ -f "$NERDBRAIN/instructions/index.md" ] || [ -f "./instructions/index.md" ] && echo found
```

**If not found, clone it.** Most people run their own fork, because the brain fills up with
their preferences — so ask which repo before assuming, and prefer any nerdbrain remote
already configured in this session over the upstream one:

```bash
git clone --depth 1 https://github.com/dhavalw/nerdbrain.git "$HOME/.nerdbrain"
```

If that fails on auth (a personal fork is often private), try in order: `gh repo clone
<owner>/nerdbrain ~/.nerdbrain`, then SSH (`git@github.com:<owner>/nerdbrain.git`). In a
Claude Code remote/web session, use the `add_repo` tool for that repo and follow the clone
command it returns.

If it still can't be reached, say so in one line and continue the task without it. Don't
stall the work over a docs fetch.

## 2. Refresh it

Best effort, non-blocking. A stale copy is fine; a hang is not.

```bash
git -C "$NERDBRAIN" pull --ff-only --quiet 2>/dev/null || true
```

Skip the pull if the clone is less than a day old, or if step 1 resolved to the current
working directory (you're probably editing it).

Then verify the repo is in sync with itself:

```bash
python3 "$NERDBRAIN/tools/check.py"
```

If it fails, the derived content (page maps, index tables, router lines) is stale
relative to the files on disk — each failure message names its fix. Rebuild before
relying on the affected parts: re-derive page maps with `tools/index-pdf.py`, update the
tables, re-run until green. Working inside the nerdbrain repo itself, commit the rebuild;
loading it from another project, fix it in place and tell the user in one line so they
can commit it later. Don't read a page map the gate just called stale.

## 3. Load

Always:

- `instructions/index.md` — the router
- `instructions/core.md` — non-negotiables and defaults
- `instructions/profile.md` — durable preferences, standing context, how to talk to the user

**Use the profile before you ask anything.** Every checkpoint question it already answers
goes into the batch pre-filled and marked as from the profile, for correction rather than
composition. Asking cold what the profile settles is the waste this system exists to remove.

Then read the router table in `instructions/index.md` and load the packs that match the task
at hand. **Load all of them.** There is no count to hit — the minimum that covers the work
is the target, and a pack left out to keep the number down takes its rules with it. What you
don't read is everything the router didn't match.

**Skip what you already have.** If packs were loaded earlier in this session, read only what
the current task newly matches. A pack in context is still in force; re-reading it is pure
bloat — and it is what makes re-routing cheap enough to do every time.

If a platform is in play, read `docs/index.md` — a router — and open only that platform's
index from it for the page ranges. Reading another platform's maps is the bloat this whole
system exists to avoid.

If the project's decision log carries `ASSUMED` entries the user never reviewed, surface
them before building anything on top of them.

## 4. Apply

Follow the loaded packs for the rest of the session, at the precedence stated in
`instructions/index.md`: the user's instructions beat the project's conventions, which
beat the packs.

Route every task and every iteration of one, not just the first. Go back to the router table
at each new piece of work and load whatever is newly matched — a new surface, a new concern
(auth, payments, uploads, user-visible copy), a new platform. Most checks will match nothing
new, which is the point: the check is free and the miss is not.

## 5. Confirm

Everything belonging to this repo goes in one block, last thing in the reply — packs loaded,
ledger entries written, approvals waiting — and nowhere else in the reply. That is what lets
the user tell meta-work from the project they actually asked about.

**Only when there is something in it.** A pack loaded or dropped, a ledger entry written or
bumped, something proposed for this repo. A turn that re-routed and matched nothing new gets
no block — the shape carries news, and one that reports "nothing" every reply stops being
read before the reply where it counted.

```


  ─── nerdbrain ─────────────────────────────

  packs     core planning stack-and-architecture security ux-user

  ───────────────────────────────────────────


```

The blank lines inside the fence are part of the format — they are what makes it read as a
separate block rather than more reply. Later in the same session, report the delta only:
`packs    +copy +ux-user`, and nothing at all on the turns where the delta is empty. The
full shape, and the rule that it stays rigid, are in `instructions/profile.md`.

Do not summarize the packs back to the user. It is their repo.

## Arguments

| Invocation | Do |
|---|---|
| `/nerdbrain` | Auto-route from the current task |
| `/nerdbrain <pack>` | Load that pack specifically (`/nerdbrain pocketbase`, `/nerdbrain design`) |
| `/nerdbrain list` | Print the inventory from `instructions/index.md`, load nothing else |
| `/nerdbrain refresh` | Force `git pull`, report the new HEAD |
| `/nerdbrain docs <topic>` | Find the platform in `docs/index.md`, look the topic up in its index, read the page range |

A named pack overrides the router — load what was asked for.

## Notes

- Snapshots under `docs/` are dated. Verify limits and prices against live docs
  (`instructions/research.md`).
- If you research a platform well enough to reuse, propose it back — a pack from
  `instructions/platforms/_template.md`, an index beside any captures, and a router row in
  `docs/index.md` — and write it once the user says yes. Nothing lands in this repo
  unapproved (`instructions/learning.md`).
- **At the end of the task, write what it taught to `memory/observations.md`** — the format
  is in `memory/index.md`. That needs no approval, because an entry there governs nothing;
  turning one into a rule still does. Seen it before? Bump the existing entry rather than
  adding a second.
- **Then run `python3 tools/staleness.py` and clear the backlog it reports.** Ledger entries
  ripe for ten days or more get raised with the user directly — at most three, strongest
  first — and each one you raise gets `Last raised` set to today. This is how a rule gets
  approved when the weekly job has no credential configured, which is the default state of a
  fresh clone (`instructions/learning.md`).
- **Raise them in the nerdbrain approvals block**, in the standard shape from
  `instructions/profile.md` — ids, target pack, the rule in a line, what it rests on. Naming
  an id is the yes; nothing else is.
- **Needed docs this repo didn't have?** Write it down at the moment you fall back to live
  docs — you are the only one who knows the gap exists, and only right then. A crawlable
  start URL goes in `docs/scrape-list.md`, where a capture tool will pick it up unattended;
  anything a person has to fetch by hand goes in `docs/wanted.md`.
- **Rows in `docs/scrape-done.md` are captures waiting to be filed.** Clear them at the
  start of a session, before the task: verify each PDF is on disk, readable, the section
  that was asked for, and indexed — then delete the receipt and the queue row it answers,
  together. Any check failing, leave both and say which. `instructions/doc-capture.md`.
