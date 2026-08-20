---
name: update-nerdbrain
description: Turn a one-line ask into a durable rule in the nerdbrain repo — find the pack it belongs in, write it in house style, rebuild the router and inventory, run the gate, commit and push. Use when the user types /update-nerdbrain, or asks to add a rule, standard, preference or house rule to their instructions, to remember a correction so it applies next time, or to change or drop something a pack already says. Operates on the nerdbrain repo only — never on a target project's own CLAUDE.md, even when nerdbrain is attached there as a reference.
---

# update-nerdbrain

The shorthand for "make this a standing rule." The user states it once, in a line. This
skill does the pedantic part: placement, house style, derived content, the gate, the commit.

## 1. Confirm you're in the right repo

**This is the step the short name makes load-bearing.** `/update-nerdbrain` reads like a
request to update whatever instructions are in front of you, and it is not one: it edits the
nerdbrain repo and nothing else, ever.

`instructions/index.md` and `tools/check.py` both present, or you are not in nerdbrain. When
this session has nerdbrain attached as a reference beside another repo, the edit lands in the
nerdbrain clone and nowhere else — never in the target project's `CLAUDE.md`, `AGENTS.md`,
`.cursorrules` or any other instruction file it carries.

A rule that governs only *that* project belongs in that project's own file. If the ask reads
that way, say which one you think it is and stop — writing a project-local rule into the
portable brain pollutes every future session, and writing a portable rule into one project
loses it.

## 2. Restate the rule before placing it

Write the ask back as one sentence in the imperative, the way a pack would phrase it. That
sentence is what you're about to place, and a misread is cheap to catch there and expensive
to catch after four files have moved.

Ambiguity about *what behavior is wanted* is a checkpoint question (`instructions/core.md`):
ask it once, up front. Ambiguity about *which file it goes in* is yours to settle — that's
the pedantry the user is handing off.

Then weigh it. A rule that will still be true across projects in six months belongs here. A
fact about one app, or a preference that dies with the task, doesn't.

## 3. Place it

Read `instructions/index.md` and search the packs for what's already there. A rule that
extends or contradicts an existing line is an edit to that line — two packs disagreeing is
worse than a rule that never got written down.

| The rule… | Goes |
|---|---|
| fits a pack's subject | in that pack, in the section that already covers the neighborhood |
| must fire on every task, whatever its shape | one bullet in `instructions/core.md`, the detail in the topic pack it points at |
| is specific to a platform | that `instructions/platforms/*.md` pack — a new platform starts from `instructions/platforms/_template.md` and needs its name in `skill/nerdbrain/SKILL.md`'s description |
| covers a subject no pack has | a new pack, under ~100 lines with a clear load trigger, plus a router row and an inventory line in the same commit |
| is a pattern proven in a shipped app | the family's capture file (`instructions/stacks/_template.md` and its siblings) — inventory line, no router row |
| comes from a snapshot's contents: filenames, page numbers | that platform's `docs/references/<platform>/index.md`, never a pack. The gate rejects it in a pack |
| is about the user rather than the work — a preference, something they own or already pay for, how they weigh a tradeoff | `instructions/profile.md`. Keep it short: it is loaded on every task, and it earns its place by shortening the checkpoint |
| is a claim about a limit, price or free tier | that platform pack's `## Volatile claims` section, as a pointer to the live source with a verify-by month. Never as a copied number |

Core is always loaded and short on purpose. A rule earns a line there only if it has to
apply when its topic pack isn't loaded — otherwise the pack alone is enough. When the rule
does go both places, core carries the one-line version and the pack carries the how.

Adding to a pack that already runs long? Cut something stale in the same edit, or split the
pack. A pack too long to load defeats the router.

## 3b. If the pack is already at its budget

Split it, don't trim it. Find the seam between two load triggers, move whole sections
verbatim, route each half, then add the new rule to the half it belongs to. Trimming to
make room silently trades a rule the user already approved for the one they just asked for.

## 4. Write it the way the packs write

The packs have to survive the standards they set, so hold the new text to
`instructions/copy.md` and `instructions/anti-ai-tells.md` before saving. Assert the rule,
name the failure mode it prevents, and stop — no rationale essay, nothing from the delete
list, sentence-case headings, wrapped at ~95 columns. Match the voice and bullet shape of
the pack you're editing; a paragraph that reads like it was pasted in from elsewhere is the
tell.

## 5. Rebuild and gate

Every derivation the edit touched has to be rebuilt in the same commit: the router row, the
inventory one-liner, the platform list in the `/nerdbrain` description, the `README.md` layout
block if a directory appeared. `/refresh-nerdbrain` walks all of it; the gate names the fix
for whatever you missed.

```bash
python3 tools/check.py
```

Re-run until it passes. Never reach green by loosening the checker — if a failure looks
wrong, that's a question for the user, not an edit to `tools/check.py`.

## 6. Ship it

If the rule came from a ledger entry, **flip that entry's Status to `shipped` in the same
commit** (`memory/index.md`). A rule that is live in a pack while its entry still says `open`
gets proposed all over again by the next promotion run.

If it came from the conversation and no entry exists, add one at `shipped` — the ledger is
the record of what was decided and why, and a rule that arrives with no trace of its evidence
is the thing nobody can re-litigate later.

Commit on a branch, with a message that says what behavior changed rather than which lines
moved. Push. If a PR is already open on that branch, it gets the commit and a body that
matches the diff (`instructions/shipping.md`). Opening a new PR stays the user's call.

## 7. Report in one line

Name the pack and the rule, nothing more:

> nerdbrain: shipping.md — open PRs get pushed to as the work runs. Router row updated, gate
> green, pushed.

Don't read the pack back to the user. They wrote it.

## Arguments

| Invocation | Do |
|---|---|
| `/update-nerdbrain <rule>` | Place that rule |
| `/update-nerdbrain` | Take the rule from the conversation just now — the correction, the thing that went wrong, the preference said in passing. Restate it and get a yes before writing |
| `/update-nerdbrain <pack>: <rule>` | Placement is settled; edit that pack |
| `/update-nerdbrain drop <rule>` | Take a rule out. Deleting is destructive (`instructions/destructive-actions.md`) — name exactly what goes and wait for the answer |
