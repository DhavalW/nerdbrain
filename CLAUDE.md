# nerdbrain

A portable, self-evolving brain for AI coding agents. Attach it to a session and the agent
picks up how its owner works, what their work already runs on, and the documentation that
work depends on — then gets better at all three as it is used.

This repo turns up in a session in one of two roles, and they want opposite things from you.

- **A reference, attached alongside the repo actually being worked on.** The usual case. The
  packs here are the standard that work is held to; this repo is not the work. Follow
  *Reference mode*, and change nothing here.
- **The work itself** — a change to a pack, the router, a doc snapshot, the skill, or the
  gate. Follow *Working on this repo* and everything below it.

## Sync with the original before you start

`DhavalW/nerdbrain` is the original. Every other copy of this repo is a fork, and a fork
falls behind the moment the original moves — including the packs a reference session is
about to hold work to. Nobody should have to notice that happening.

**Before starting any task, in either role, bring the fork up to date with the original's
`main`.** Session start counts as a start, and so does the beginning of each new task in a
long session. Once per task is enough — don't re-check between turns, or straight after a
sync you just ran.

```
tools/fork-sync.sh check
```

It reads and changes nothing. What it prints decides what happens next:

| Verdict | Means | Do |
|---|---|---|
| `not-a-fork` | `origin` is the original | Nothing, and don't raise it again this session |
| `in-sync` | The branch has every upstream commit | Start the task |
| `behind:N` | N commits missing, merge is clean | `tools/fork-sync.sh sync`, report in a line, start |
| `dirty-overlap` | Uncommitted edits on files upstream also changed | Load `instructions/fork-sync.md` |
| `conflict` | The merge would collide | Load `instructions/fork-sync.md` |
| `upstream-mismatch` | An `upstream` remote points elsewhere | Stop, ask which repo is the original |
| `fetch-failed` | The original is unreachable | Say so in a line and start the task anyway |

A completed sync is worth one line: how many commits arrived and what they touched. When
nothing came down, say nothing.

Five rules it never breaks, here rather than behind a pointer because a session that never
follows one still has to obey them. Upstream `main` is the only thing fetched — no other
branch, no tags. Nothing flows back up; *Sharing a learning upstream* below is the only path
by which anything leaves this repo, and `fork-sync.sh` points the upstream remote's push URL
at a dead scheme so a stray push fails loudly instead of succeeding. Merge, never rebase — a
merge commit keeps both histories and leaves every existing checkout of the fork valid, which
is also why `push --force`, `reset --hard` and amending a pushed commit are out. And
uncommitted work is never merged over: the script stashes only when none of the dirty files
are ones upstream touched, and refuses outright on any overlap.

The fifth is what the sync will not carry, in either direction: the captures under
`docs/references/`, and `docs/scrape-list.md`, `docs/scrape-done.md` and `docs/wanted.md`
beside them. Those belong to whoever owns this clone. The queue is the sharp end — it is read
by a tool that opens each URL in the owner's browser and commits the result to their
repository, so a row that arrived by merging somebody else's copy would be an unattended
crawler taking instructions from a stranger. `fork-sync.sh` keeps this clone's version of all
four, silently, and never asks about a clash in one.

**A conflict is never resolved on your own judgement.** The fork's change is somebody's
deliberate work and the original's is somebody else's. Load `instructions/fork-sync.md`: it
carries how to put the choice to the user and how to carry out their answer.

## Reference mode

Loading the right packs is your job, not the user's. They attached the repo instead of
typing anything, and that is the whole instruction: hold the work to what's in here.

**Before starting any task, and again whenever the work turns into a different kind of
work:**

1. **Consult the router** — `instructions/index.md`. On the first consultation of a session,
   read `instructions/core.md` and `instructions/profile.md` as well; both always apply.
   Core is how the work runs, profile is who it runs for — use it to arrive at the decision
   checkpoint with the answers already filled in, rather than asking what's settled.
2. **Load every pack the router matches — all of them, however many that is.** There is no
   count to aim at: the minimum that covers the work is the target, and a pack dropped to
   keep a number down takes its rules with it. The economy is in not reading what the router
   *didn't* match. If a platform is in play, `docs/index.md` routes you to that platform's
   index, which maps topics to page ranges — read the platform's index before opening any
   vendor PDF, and only that platform's.
3. **Load nothing twice.** Track what you've already read from here. Re-routing reads only
   what is newly matched — packs already in context are still in force, and re-reading them
   buys nothing but bloat. This is what makes step 2 affordable and the re-check below free.
4. **Report what belongs to this repo in the nerdbrain block, when there is something to
   report** — a pack loaded, a ledger entry written, something needing a yes. Last thing in
   the reply and nowhere else, in the fixed shape in `instructions/profile.md`. A turn that
   loaded nothing and wrote nothing gets no block: the shape exists to carry news, and one
   that says "nothing" every time stops being read. Never summarize a pack back to the user —
   it is their repo.

**Re-consult the router at the start of every task, and every iteration of one** — not only
when the work changes kind. The check is free, because the router is already in context and
step 3 means most checks load nothing. What it catches is the sub-task quietly running on
whatever the last one happened to need: a new surface (a screen, an API, a deploy), a new
concern (auth, payments, uploads, user-visible copy), a new platform.

The `/nerdbrain` skill ships in this repo and is live whenever the repo is attached
(`.claude/skills/nerdbrain`). Invoking it runs steps 1–2 for you, but nobody has to invoke
anything for this protocol to apply.

Precedence, from `instructions/index.md`: what the user says beats the target project's
`CLAUDE.md` and its existing conventions, which beat these packs. The gate and invariants
below govern *this* repo only — never impose them on the project being worked on.

The traffic runs both ways. What the task turns up — a correction, a preference said in
passing, an architecture that held, a pack that was wrong or silent, a shape seen just the
once — gets generalized past this project and written to the ledger when the work is done,
so it reaches projects that don't exist yet (`instructions/learning.md`, format in
`memory/index.md`). Recorded with what it rests on.

**Recording and approving are separate, and that separation is the point.** An entry in
`memory/observations.md` governs nothing, so writing one needs no permission and no
session has to win an argument to keep a lesson alive. Promoting one into a pack changes
behavior, so it needs an explicit yes, per item — and secrets never get written here at
all, in either place.

Finishing a task is also when the backlog gets cleared. `tools/staleness.py` names the
ledger entries that have been ripe for ten days without anyone acting on them, and those go
to the user directly — at most three at a time, each marked `Last raised` so the same ones
don't come back tomorrow. They are raised in the nerdbrain approvals block — one fixed layout,
ids to reply with, evidence attached — because an ask buried in prose gets skimmed
(`instructions/profile.md`). That path is what closes the loop when the weekly job has no
credential configured, which is the default state of a fresh clone.

Docs the task needed and this repo didn't have go in `docs/wanted.md`, same terms: no
approval, because it's a worklist and not a rule. The half of that worklist a crawler can
do unattended goes in `docs/scrape-list.md` instead — a start URL and the folder it belongs
in, in the shape SiteToPDF reads out of GitHub and captures without being asked. Rows in
`docs/scrape-done.md` are its receipts, and clearing them is a session-start job: verify
the PDF landed and is indexed, then delete the pair, or leave both and say what failed.
Both halves are in `instructions/doc-capture.md`.

## Sharing a learning upstream

This repo is a fork of a public one, and the loop runs in both directions. A rule the user
approves here is theirs; a rule that would hold for anyone is worth sending back, and that
is how the shared brain gets better faster than any single fork can.

**Ask before anything leaves this repo, every time.** A learning arrives attached to the
work that produced it, and the user is the only one who knows whether the generalized
version still carries something they don't want public. So:

1. **Offer it, don't send it.** When a shipped rule reads as generally true, say so in one
   line at the end of the task and ask whether to open an upstream PR. Silence is no, the
   way it is everywhere else here.
2. **Generalize harder than the pack needed.** The version that goes upstream mentions no
   project, no employer, no client, no internal service, no unreleased product. If stripping
   those leaves nothing, there was nothing general in it — say so and drop it.
3. **Never send the ledger entry's evidence, only its rule.** Dates and counts are fine;
   what proved it usually isn't.
4. **Nothing sensitive crosses, ever**, and the standard is the one under *Invariants*
   below — the same bar, applied to a wider audience.

An upstream PR is a normal contribution: one rule per commit, the pack it lands in, what it
rests on, and the gate green. `CONTRIBUTING.md` has the full shape.

## Working on this repo

`/update-nerdbrain <rule>` is the shorthand for the most common change here: the user
states a rule in a line, and the skill places it, writes it in house style, rebuilds the
router and inventory, and runs the gate. It ships in this repo
(`.claude/skills/update-nerdbrain`) and everything below still governs; the skill just
saves the user from restating it every time.

**It edits this repo and nothing else.** The name is short, so the guard is not in the name:
a rule that governs only the project you happen to be working in belongs in that project's
own `CLAUDE.md`, and this skill never touches it. When the ask could be read either way, say
which one you think it is and wait.

This repo *is* the instruction system, so changes here follow its own rules. The packs in
`instructions/` apply to work on this repo too — especially `instructions/copy.md` and
`instructions/anti-ai-tells.md` (the packs must read the way they tell others to write), and
the decision-checkpoint protocol from `instructions/core.md` — questions in the reply, then
stop until they're answered.

Writing or retiring a rule has its own pack: `instructions/meta-rules.md`, the bar a rule
clears before it governs anything. Load it for any change to a rule, not for using one.

## Changing something foundational

The entry point, the router, the gate, the ledger format, the approval path, the
always-loaded set. Every project runs through these, so a wrong change here isn't one bad
commit — it's a bad rule applied silently to everything built afterwards, including projects
that don't exist yet. Getting one of these right matters more than shipping it this session.

They are checkpoint decisions, always, however obvious the change looks. Before proposing
one:

- **Test the premise instead of stating it.** Read what actually depends on the thing you're
  changing; don't reason from its shape. Proposing to split a file is a claim that nothing
  needs both halves — go and check, because the answer is usually in the file.
- **Give the cost and the benefit in real units.** Lines, tokens, what stops being
  guaranteed. "Cleaner" and "more modular" aren't measurements, and a ratio quoted without
  checking its denominator is worse than no number at all.
- **Name what would have to be true for this to be wrong**, and say which way the evidence
  actually fell.
- **A proposal you keep returning to is telling you something about your reasoning**, not
  strengthening its case. Three passes at the same change means test the premise, not
  restate it.
- **Propose, then stop.** Never build a foundational change while the answer is outstanding,
  however cheap it looks to do both.

Once settled, record it where the next session will hit the same pressure — the budget
comments in `tools/check.py` are the working example. A decision that isn't written down
gets re-derived, and re-derived wrong, on roughly a monthly cycle.

## The gate

```
python3 tools/check.py
```

Run it before every commit; CI runs it on every push and fails the build. It enforces the
invariants below. If a change genuinely requires relaxing one, that's a checkpoint
decision — raise it, don't quietly edit the checker.

Two things it deliberately doesn't do, because a gate that fails on the passage of time
turns an unrelated push into someone else's problem:

- `python3 tools/staleness.py` **reports** what's going out of date — volatile claims past
  their verify-by month, captures aging out, indexes with no source URL. Reports only; the
  weekly job puts it in front of the user.
- `python3 tools/autoindex.py` drafts the `## Files` rows and page maps for captures that
  have none, so a PDF dropped into `docs/references/` becomes a PR instead of a chore. The
  drafts still need a human pass — `index-pdf.py` over-splits and doesn't know the
  document's own headings.

## What runs on its own

Three workflows, and only one of them costs anything:

| Workflow | Fires | Does |
|---|---|---|
| `consistency` | every push and PR | `tools/check.py`. Fails the build |
| `index-captures` | a PDF lands under `docs/references/` | drafts index entries, opens a PR. Deterministic — no model, no credentials |
| `promote-learnings` | Mondays | reads the ledger, drafts the pack edits it has earned, opens one PR. Needs `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN`; without either it exits clean |

**Merging the promotion PR is the approval**, per commit: drop the ones you don't want,
merge the rest. Closing it is a decline, and the next run records that in the ledger so
the same proposal doesn't come back. Nothing in this repo is ever merged by an agent.

## Sync: derived content rebuilds automatically

Parts of this repo are derived from other parts: the page maps and file lists in the doc
indexes derive from the PDFs on disk, the router table in `docs/index.md` derives from those
indexes, the router and inventory lines derive from the pack
files, the skill description's platform list derives from `instructions/platforms/`. When
a source changes, its derivations are stale — and the gate detects every such case, in
both directions, with a message that names the fix.

So the gate is also the change detector. `/refresh-nerdbrain`
(`.claude/skills/refresh-nerdbrain`) runs the whole rebuild as one step, including the drift
the gate can't see — a snapshot replaced under the same filename, an inventory line that no
longer describes its pack. The
protocol below applies whether or not you invoke it:

1. **Run it at session start** — files may have changed since the last session (a snapshot
   dropped in by hand, a pack edited elsewhere) — **and again after any change you make**
   under `docs/`, `instructions/`, or `skill/`.
2. **Treat each failure as a rebuild task, not an error report.** Do the fix the message
   names: re-derive page maps with `tools/index-pdf.py`, update the platform index's file
   list, add the router row and inventory line, extend the skill description. Re-run until
   green.
3. **Ship the rebuilt artifacts in the same commit** as the change that made them stale —
   never leave the repo red for the next session.
4. **Never silence the gate instead of rebuilding.** Deleting a stale table row to clear a
   missing-file error when the real fix is indexing the new capture is gate evasion
   (`instructions/testing-gates.md`). If a failure seems wrong, that's a checkpoint question,
   not an edit to the checker.

## Invariants

- **Instructions carry durable knowledge only.** Anything derived from a snapshot's
  contents — exact filenames, page numbers — lives in the per-platform doc index beside the
  PDFs (`docs/references/<source>/index.md`) and is resolved at read time. `docs/index.md`
  is a router: sources and where their indexes are, no filenames, so reading it to find one
  source doesn't load every other source's maps. Each index's `## Files` section is the
  manifest for its folder, and the gate tallies the two against each other. Packs cite
  snapshots by source prefix and doc topics by name, never by page.
- **The ledger records; the packs govern.** An entry in `memory/observations.md` changes no
  behavior, which is exactly why any session may append one without asking. Only promotion
  into a pack makes it a rule, and only the user approves that. An agent that reads an
  `open` entry and acts on it has skipped the gate the whole system is built around.
- **A claim that decays says so.** Limits, prices and free-tier ceilings go in a pack's
  `## Volatile claims` section as pointers to the live source with a verify-by month —
  never as a copied value, which is how a stale number gets quoted as fact
  (`instructions/research.md`).
- **Nothing sensitive, anywhere in here.** No keys, tokens, connection strings, private
  hostnames, customer data, or anything under an NDA — not in a pack, an example, a commit
  message, or a file that "gets cleaned up later". Anyone with the repo can read it, and
  history keeps what a later commit deletes. When a rule can't be written without the
  sensitive part, take one of the ways around it in `instructions/learning.md`, or say
  it's a leak risk and let the user decide.
- **One inventory.** `instructions/index.md` is the only complete list of packs. The
  README describes directories, not files, precisely so it can't drift.
- **Every pack is routed.** A pack not reachable from the router table might as well not
  exist. New pack = router row + inventory line, same commit.
- **References resolve.** Relative to the citing file or the repo root; globs must match.

## Changing things

- **New topic/type pack:** keep it under ~100 lines with a clear load trigger; add the
  router row and inventory line in `instructions/index.md`.
- **A pack over its budget gets split, not trimmed.** Find the seam where it serves two
  different load triggers, move whole sections verbatim, route each half. Nothing is
  reworded or dropped — every original line lands in exactly one half, and only a
  cross-reference whose target moved gets repaired. No honest seam (every section fires on
  the same trigger) means leave it and say so: halves that always load together cost more
  than the one file did. `instructions/core.md` is the standing example.
- **New platform pack:** start from `instructions/platforms/_template.md`; also update the
  platform list in `skill/nerdbrain/SKILL.md`'s frontmatter description, or the skill won't
  trigger on the new platform's name.
- **New architecture/stack/theme template:** capture the proven pattern using that
  family's capture file (e.g. `instructions/stacks/_template.md`), then add the inventory
  line in `instructions/index.md` — the gate enforces it. These are checkpoint menus, not
  auto-loaded packs — no router row.
- **New or refreshed doc snapshot:** follow the procedure in `docs/index.md` — dated
  filename, an entry and page map in that platform's index (drafted with
  `tools/index-pdf.py`), router row updated, old capture removed. Pushing the PDF to `main`
  and letting `index-captures` draft the entry does the same thing, one review later.
- **A queued capture, or its receipt:** append a row to `docs/scrape-list.md`, or delete
  the verified pair from it and `docs/scrape-done.md`, per `instructions/doc-capture.md`.
  No approval and no router row — both files are worklists, not rules, and neither one
  crosses a fork sync in either direction.
- **A new ledger entry:** append it to `memory/observations.md` in the format
  `memory/index.md` sets out, at the end of the task. No approval, no router row, no
  inventory line — it isn't a pack. Seen it before? Bump the existing entry's count instead
  of adding a second one.
- **Superseding a pack:** leave a short pointer at the old path — a three-line stub naming
  the pack that took the rules over — so stale references degrade to a redirect, not a 404.
- **New skill:** a directory under `skill/<name>/SKILL.md`, symlinked into
  `.claude/skills/` so it's live when the repo is attached. `install.sh` picks up anything
  under `skill/` on its own — no edit needed there.
- **A mechanism changed:** `MECHANICS.md` is the public explanation of how the five
  mechanisms fit, and `README.md` is the pitch. Both are derived from behavior, so a change
  to how something works updates them in the same commit or they become fiction.
- **Anything a contributor has to know:** `CONTRIBUTING.md`. It is the outward-facing half
  of `instructions/meta-rules.md` — when the bar for a rule moves, both move.
- **Editing the checker or a skill:** these are load-bearing for every future session.
  Test them (`tools/check.py` must pass on the repo; a skill's steps must match the repo
  layout) and say in the commit message what behavior changed.

## Style

Follow the repo's own standards: assertive, specific, no filler, sentence-case headings,
~100-line packs, wrapped at ~95 columns. A pack that wouldn't survive its own
`instructions/anti-ai-tells.md` review isn't done.

**Length and wrap are gated, not advisory.** Every always-loaded file has a recorded line
budget in `tools/check.py`; going over fails the build. It's a ratchet — shrinking is free,
so lower the number when you trim. Files already over the ~100 standard are pinned at their
exact size with no headroom, which makes that list the trim backlog. Raising a number is
sometimes right; it shows in the diff and belongs in the commit message. Raising one to
clear a red build without saying why is gate evasion (`instructions/testing-gates.md`).
