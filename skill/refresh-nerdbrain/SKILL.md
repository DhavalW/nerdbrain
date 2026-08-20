---
name: refresh-nerdbrain
description: Rebuild this repo's derived content after files change — page maps for new, replaced or deleted doc snapshots, router rows and inventory lines for new packs, the /nerdbrain trigger list, and the doc index tables. Use when the user types /refresh-nerdbrain, or asks to refresh, resync, reindex or rebuild the nerdbrain repo after dropping in a snapshot, adding or renaming a pack, or removing either. For work inside the nerdbrain repo itself — never run it against a project that merely has nerdbrain attached as a reference.
---

# refresh-nerdbrain

Parts of this repo are derived from other parts. Drop a PDF into `docs/` and its platform's
file list and page maps are stale. Add a pack and the router and inventory are stale. Add a
platform and the `/nerdbrain` skill stops triggering on its name. This skill walks the drift,
rebuilds it, and leaves the gate green.

`tools/check.py` finds most of it and names the fix in every failure message. The rest of
this file is the part the gate can't see.

## 1. Confirm where you are

Run from the nerdbrain repo root — `instructions/index.md` and `tools/check.py` both present.
If this session has nerdbrain attached as a reference beside another repo, this skill operates
on the nerdbrain clone and nothing else. Say so and stop rather than guess: rebuilding derived
content in the wrong repo is worse than doing nothing.

## 2. See what moved

```bash
git status --short
git log --oneline -15
python3 tools/check.py
```

The gate compares disk against the indexes in both directions, so it catches a snapshot
with no row and a row with no snapshot. What it cannot catch is a file replaced *in place*
under the same name — the row still resolves, and the page map underneath it is now
fiction. So also look at what recent commits touched:

```bash
git log --stat -8 -- docs/ instructions/ skill/
```

A commit that touched a PDF without touching its map, or a pack without touching
`instructions/index.md`, is drift the gate will pass.

## 3. Rebuild, by kind of drift

| What changed | What to rebuild |
|---|---|
| New snapshot under `docs/` | An entry in the `## Files` section of that platform's `docs/references/<platform>/index.md` — filename and page count — and a page map drafted with `python3 tools/index-pdf.py <pdf>`. Refresh the router row's file and page counts in `docs/index.md` |
| New platform folder under `docs/references/` | An index.md beside the PDFs (source, capture date, companion pack, a `## Files` section, maps) **and** a router row in `docs/index.md`. The gate fails on either one missing |
| Snapshot refreshed (same source, new capture) | New row, and the map **fully re-derived**. Page numbers shift between captures, so the old map is void, not roughly right. Then remove the superseded PDF and its rows — see §5 |
| Snapshot deleted | Drop its `## Files` entry and its entire map section, and check no pack cited it by source prefix |
| Same filename, new contents | Nothing fails, and everything downstream is wrong. Re-derive the map whenever a commit touches a PDF |
| New pack under `instructions/` | Router row **and** inventory line in `instructions/index.md`. Both, same commit — a pack the router can't reach may as well not exist |
| New platform pack | The above, plus the platform's name in the description in `skill/nerdbrain/SKILL.md`, or `/nerdbrain` won't trigger on it. Start from `instructions/platforms/_template.md` |
| New template under `architectures/`, `stacks/`, `themes/` | Inventory line only. These are checkpoint menus, not routed packs — no router row |
| Pack renamed or removed | Repoint or remove the router row and inventory line, fix every citation of it, and leave a redirect stub at the old path — three lines naming the pack that took over — if anything might still point there |
| Pack contents changed | Check the inventory one-liner still describes it, the router row still matches when it should load, and no page number or dated filename crept in |
| Pack over its line budget | Split it at the seam between two load triggers, verbatim, and route each half — never trim to fit. No seam means leave it; two halves that always load together cost more than the one file did |
| New skill under `skill/` | A symlink under `.claude/skills/` so it's live when the repo is attached, and the skill's line in the `README.md` layout block. `install.sh` finds anything with a `SKILL.md` on its own |
| Unindexed PDF sitting under `docs/references/` | `python3 tools/autoindex.py` drafts the `## Files` rows and page maps. Then do the human half: merge over-split rows, rename topics to match the document, delete the `draft map, unreviewed` headings |
| A pack gained a claim about a limit, price or free tier | A line in that pack's `## Volatile claims` section — a pointer to the live source with a verify-by month, never a copied value. The gate rejects an undated one |
| A ledger entry was promoted into a pack | Flip that entry's Status to `shipped` in the same commit as the pack edit, so the ledger and the packs never disagree about what is already a rule |
| A profile line stopped being true | Remove it from `instructions/profile.md` and say so. Nothing auto-expires there, and a wrong profile line is worse than a missing one — it gets used to pre-fill an answer nobody checked |

Drafts from `index-pdf.py` are drafts: merge the over-split rows, and name each topic the
way the document names it. Article-per-page captures take `--per-page`, which is what a
help centre with one article per page wants.

**Maps never go in `docs/index.md`.** It is the router — platforms, what each capture is,
and where its index lives — and it is read by anyone opening any vendor doc, so a map put
there costs context to every reader who wanted a different platform. Maps go beside the
PDFs, always.

## 4. The parts no checker sees

Read these yourself; `tools/check.py` has no opinion on any of them:

- Inventory one-liners that no longer describe their pack.
- Router rows whose trigger has drifted from what the pack now covers.
- The layout block in `README.md`, when a directory is added or renamed.
- Page-map topic names that have drifted from the documents' own headings. Packs cite
  topics by name, so a renamed heading breaks resolution silently.
- Cross-references that still resolve as paths but now point at the wrong idea.
- Profile lines that have quietly stopped being true. The gate checks that
  `instructions/profile.md` fits its budget, never that it is right, and a stale line there
  gets spent pre-filling a checkpoint answer.
- Ledger entries whose Status disagrees with reality — `proposed` for a PR that merged
  weeks ago, `open` for a rule some other commit already wrote into a pack.

`python3 tools/staleness.py` covers the time-based half of this: volatile claims past their
verify-by month, captures aging out, indexes with no source URL. Run it here and act on what
it names — it reports and never fails, so nothing else will make you look.

## 5. Deleting is a confirmation, not a step

Removing a superseded PDF, dropping table rows, deleting a pack — all destructive, and
`instructions/destructive-actions.md` governs this repo like any other. Name exactly what goes,
wait for an answer, and never assume one because the intent seems obvious. Additive work —
new rows, drafted maps, router entries — just do.

## 6. Finish green

Re-run `python3 tools/check.py` until it passes. Never reach green by silencing it: deleting
a stale row when the real fix is indexing the new capture is gate evasion
(`instructions/testing-gates.md`).

Commit the rebuilt artifacts with the change that made them stale, or on their own if that
change is already committed. The message says what was re-derived and what was removed.

Then report in a few lines: what changed on disk, what you rebuilt, and what needs the
user — a snapshot with no pack yet, a pack whose docs are gone, anything you couldn't
verify.
