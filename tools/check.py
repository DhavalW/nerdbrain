#!/usr/bin/env python3
"""Consistency gate for this repo. Run before committing; CI runs it on every push.

Enforces the invariants that keep the pack system reliable as it grows:

  1. Every backtick-quoted .md/.pdf reference resolves (relative to the citing
     file or the repo root). Globs must match at least one file.
  2. Dated snapshot filenames (…_YYYYMMDD_HHMM…) appear ONLY in the doc indexes.
     Everything else must cite by source prefix.
  3. Instruction packs carry no page numbers - they cite doc topics by name and
     resolve pages via the indexes at read time.
  4. Every instruction pack is listed in instructions/index.md (router or
     inventory), so the router never silently forgets a pack.
  5. Each capture folder's `## Files` list matches the PDFs in that folder
     exactly, both directions - no unindexed snapshot, no listed ghost.
  6. Every dated filename the indexes mention anywhere - prose included, not
     just the file lists - exists on disk.
  7. Every platform pack's name appears in the /nerdbrain skill description, so
     the skill triggers on it.
  8. Every capture folder has an index.md, and docs/index.md points at it - so
     a platform's maps are always reachable from the router.
  9. Every always-loaded file stays inside its recorded line budget. A ratchet:
     growth fails until someone raises the number on purpose.
 10. The always-loaded set has a total budget, so splitting a file cannot fake
     a reduction that a reader never sees.
 11. Prose wraps at ~95 columns wherever wrapping is possible.
 12. Every ledger entry parses: unique id, the four fields in order, a known
     status, evidence stated in one of the three allowed forms. A weekly job
     reads this file, so a malformed entry is a silently skipped observation.
 13. A `## Volatile claims` section marks every claim with a verify-by month,
     which is what makes tools/staleness.py able to report it.

What this deliberately does NOT check is whether any of it is still TRUE - a
page map that drifted from the document, an inventory line that stopped
describing its pack, a claim whose verify-by date has passed. Those need
judgement or a clock: `/refresh-nerdbrain` covers the first two,
`tools/staleness.py` reports the third, and neither belongs in a gate that
should stay green on an unrelated push.

This doubles as the change detector: whenever files change, run it and treat
each failure as a rebuild task - every message names the fix. Exit code 0 =
clean, 1 = violations. Pure stdlib - no dependencies.
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Example paths that instructions legitimately mention but that live in target
# projects, not in this repo. Basenames only.
PROJECT_EXAMPLE_FILES = {
    "CLAUDE.md", "README.md", "ARCHITECTURE.md",
    "architecture.md", "data-model.md", "operations.md", "decisions.md",
    "auth.md", "redemption.md", "sync.md",
}

# Files whose absence from the instructions/index.md listing is deliberate.
NOT_IN_INDEX = {"index.md", "app-agent.md"}

DATED_NAME = re.compile(r"_20\d{6}_\d{4}")


def dated_name_allowed():
    """The doc indexes — the only files allowed to carry exact snapshot names.

    Discovered rather than listed: `docs/index.md` plus any `index.md` sitting
    beside a platform's captures. A large article-per-page capture gets its own
    index next to the PDFs, and hardcoding those paths meant the third such
    capture failed the gate for existing. The invariant is unchanged — exact
    filenames still live only in indexes, and rule 6 still checks every name
    they list is on disk.
    """
    found = {"docs/index.md"}
    for path in glob.glob(os.path.join(ROOT, "docs", "references", "*", "index.md")):
        found.add(os.path.relpath(path, ROOT).replace(os.sep, "/"))
    return found


DATED_NAME_ALLOWED = dated_name_allowed()

PAGE_CITE = re.compile(
    r"\bpart[12],?\s+p\d|\bp[12]:\d|\bp\d+(?:[–—-]\d+)?\b|\bpages?\s+\d+\s*[–-]\s*\d+"
)

REF = re.compile(r"`([^`\s]+\.(?:md|pdf))`")


def md_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules")]
        for f in filenames:
            if f.endswith(".md"):
                yield os.path.join(dirpath, f)


def rel(path):
    return os.path.relpath(path, ROOT)


def check_refs(errors):
    for path in md_files():
        text = open(path, encoding="utf-8").read()
        base = os.path.dirname(path)
        for ref in REF.findall(text):
            if ref.startswith(("http", "<", "~")) or "<" in ref or "YYYY" in ref:
                continue
            if "archive/" in ref or os.path.basename(ref) in PROJECT_EXAMPLE_FILES:
                continue
            candidates = [os.path.normpath(os.path.join(b, ref)) for b in (base, ROOT)]
            if "*" in ref:
                if not any(glob.glob(c) for c in candidates):
                    errors.append(f"{rel(path)}: glob `{ref}` matches nothing")
            elif not any(os.path.exists(c) for c in candidates):
                errors.append(f"{rel(path)}: broken reference `{ref}`")


def check_dated_names(errors):
    for path in md_files():
        if rel(path) in DATED_NAME_ALLOWED:
            continue
        for n, line in enumerate(open(path, encoding="utf-8"), 1):
            if DATED_NAME.search(line):
                errors.append(
                    f"{rel(path)}:{n}: dated snapshot filename outside the doc "
                    f"indexes - cite by source prefix instead"
                )


def check_page_cites(errors):
    for path in md_files():
        if not rel(path).startswith("instructions" + os.sep):
            continue
        for n, line in enumerate(open(path, encoding="utf-8"), 1):
            if line.lstrip().startswith(("#", ">")):
                continue
            if PAGE_CITE.search(line):
                errors.append(
                    f"{rel(path)}:{n}: page citation in an instruction pack - "
                    f"cite the doc topic by name; pages live in the doc indexes"
                )


def check_index_lists_packs(errors):
    index = open(os.path.join(ROOT, "instructions", "index.md"), encoding="utf-8").read()
    for path in glob.glob(os.path.join(ROOT, "instructions", "**", "*.md"), recursive=True):
        name = os.path.relpath(path, os.path.join(ROOT, "instructions"))
        if os.path.basename(name) in NOT_IN_INDEX:
            continue
        if name.replace(os.sep, "/") not in index:
            errors.append(
                f"instructions/index.md: pack {name} is not listed - add a router "
                f"row and an inventory line"
            )


PDF_IN_TICKS = re.compile(r"`([^`]+\.pdf)`")


def files_section(text):
    """The `## Files` block of an index: everything up to the next `## `.

    Returns None when the index has no such section - that is itself the error,
    because the tally has nothing to read.
    """
    match = re.search(r"^## Files\s*$", text, re.M)
    if not match:
        return None
    rest = text[match.end():]
    nxt = re.search(r"^## ", rest, re.M)
    return rest[:nxt.start()] if nxt else rest


def check_index_lists_pdfs(errors):
    """The file list in each index must match its folder exactly, both ways.

    Every capture folder's index.md carries a `## Files` section, one bullet per
    PDF. That list is the manifest: a name in it that is not on disk means a
    refresh moved on without updating the index, and a PDF on disk that is not
    in it means a capture was dropped in and never indexed - unreachable, since
    nothing routes a reader to it. Both fail here.

    Only the `## Files` section counts. Filenames mentioned in prose elsewhere
    in an index do not satisfy the tally, so the manifest stays in one place a
    human and this checker can both find.
    """
    docs_root = os.path.join(ROOT, "docs")
    for path in sorted(glob.glob(os.path.join(docs_root, "**", "*.pdf"), recursive=True)):
        folder = os.path.dirname(path)
        if os.path.dirname(folder) != os.path.join(docs_root, "references"):
            rel_pdf = os.path.relpath(path, ROOT).replace(os.sep, "/")
            errors.append(
                f"{rel_pdf}: snapshot outside a capture folder - move it to "
                f"docs/references/<platform>/ so an index can list it"
            )

    for folder in sorted(glob.glob(os.path.join(docs_root, "references", "*"))):
        if not os.path.isdir(folder):
            continue
        on_disk = {os.path.basename(p) for p in glob.glob(os.path.join(folder, "*.pdf"))}
        index_path = os.path.join(folder, "index.md")
        rel_index = os.path.relpath(index_path, ROOT).replace(os.sep, "/")
        if not on_disk or not os.path.exists(index_path):
            continue  # rule 8 reports the missing index
        section = files_section(open(index_path, encoding="utf-8").read())
        if section is None:
            errors.append(
                f"{rel_index}: no `## Files` section - add one listing every PDF in "
                f"this folder as `- \\`<name>.pdf\\` — <N> pages`; the gate tallies it"
            )
            continue
        listed = {n for n in PDF_IN_TICKS.findall(section) if "*" not in n}
        for name in sorted(on_disk - listed):
            errors.append(
                f"{rel_index}: {name} is on disk but not in `## Files` - add it, and "
                f"map it with tools/index-pdf.py"
            )
        for name in sorted(listed - on_disk):
            errors.append(
                f"{rel_index}: `## Files` lists {name}, which is not on disk - the "
                f"snapshot was refreshed or removed; fix the list and re-derive its map"
            )


def check_capture_folders_are_routed(errors):
    """A platform's index must exist, and the router must point at it.

    The mirror of rule 4 for docs: an index docs/index.md doesn't link is as
    unreachable as a pack the router forgets, and the maps in it may as well not
    exist."""
    root_index = open(os.path.join(ROOT, "docs", "index.md"), encoding="utf-8").read()
    folders = {os.path.dirname(p) for p in
               glob.glob(os.path.join(ROOT, "docs", "references", "*", "*.pdf"))}
    for folder in sorted(folders):
        rel_index = os.path.relpath(
            os.path.join(folder, "index.md"), os.path.join(ROOT, "docs")
        ).replace(os.sep, "/")
        if not os.path.exists(os.path.join(folder, "index.md")):
            errors.append(
                f"docs/{rel_index}: capture folder has no index - create one (source, "
                f"capture date, pack, file list, page maps) and add its router row"
            )
        elif rel_index not in root_index:
            errors.append(
                f"docs/index.md: {rel_index} is not in the captures table - add a "
                f"router row pointing at it"
            )


DATED_PDF = re.compile(r"[\w./-]*_20\d{6}_\d{4}[\w.-]*\.pdf")


def check_indexed_pdfs_exist(errors):
    """Every dated filename an index mentions in prose must exist on disk.

    The `## Files` sections are excluded because rule 5 tallies those exactly,
    in both directions; this catches the other mentions - a map heading, a
    caveat, a "read part 3 instead" - that a refresh would otherwise leave
    pointing at a file that is gone."""
    for index_rel in DATED_NAME_ALLOWED:
        index_path = os.path.join(ROOT, index_rel)
        base = os.path.dirname(index_path)
        text = open(index_path, encoding="utf-8").read()
        section = files_section(text)
        if section:
            text = text.replace(section, "")  # rule 5 owns the file lists
        for name in set(DATED_PDF.findall(text)):
            if not any(os.path.exists(os.path.join(b, name)) for b in (base, ROOT)):
                errors.append(
                    f"{index_rel}: lists {name} which is not on disk - the snapshot "
                    f"was refreshed or removed; update the table and re-derive its "
                    f"page map (tools/index-pdf.py)"
                )


LEDGER_FILES = ("memory/observations.md", "memory/archive.md")

ENTRY_HEADING = re.compile(r"^### (obs-\d{4}) — (20\d\d-\d\d-\d\d)\s*$", re.M)
ENTRY_FIELDS = ("Observation", "Rests on", "Target", "Status")
OPTIONAL_FIELDS = ("Last raised",)
STATUSES = ("open", "proposed", "shipped", "declined")
RESTS_ON = re.compile(r"^(stated outright|seen once|seen \d+ times)\b")
ISO_DATE = re.compile(r"^20\d\d-\d\d-\d\d$")

# Values wrap - packs here are written to ~95 columns and observations are
# sentences - so a field runs until the next one starts, not to end of line.
FIELD = re.compile(r"^- \*\*([^:*]+):\*\*[ \t]*(.*?)(?=\n- \*\*|\Z)", re.M | re.S)


def ledger_entries(text):
    """(obs_id, first_seen, [(label, value), ...], line_no) for each entry.

    One parser, used by the gate here and by tools/staleness.py. A second
    implementation of this is how the two would start disagreeing about which
    entries exist. Values come back whitespace-normalized to one line, so a
    wrapped observation reads as the sentence it is.
    """
    matches = list(ENTRY_HEADING.finditer(text))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        fields = [(label, " ".join(value.split()))
                  for label, value in FIELD.findall(text[match.end():end])]
        yield (match.group(1), match.group(2), fields,
               text[:match.start()].count("\n") + 1)


def check_ledger_entries(errors):
    """Every ledger entry parses the way the promotion job expects.

    The ledger is the one file here that a scheduled run reads unattended, and
    an entry it cannot parse is not an error it can report - it is an
    observation that silently never gets promoted. So the shape is gated even
    though the content is free-form: unique ids across both files, the four
    fields present and in order, a status from the known set, and evidence in
    one of the three forms the promotion threshold is defined against.

    `Last raised` may follow them. It records when an entry was put to the user
    in conversation, which is what stops a session raising the same one every
    time it finishes a task.
    """
    seen = {}
    for name in LEDGER_FILES:
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            errors.append(f"{name}: missing - the ledger's files are part of the format")
            continue
        text = open(path, encoding="utf-8").read()

        stray = [
            n for n, line in enumerate(text.splitlines(), 1)
            if line.startswith("### ") and not ENTRY_HEADING.match(line)
        ]
        for n in stray:
            errors.append(
                f"{name}:{n}: entry heading must read `### obs-NNNN — YYYY-MM-DD` - "
                f"the promotion job matches on exactly that"
            )

        for obs_id, _first_seen, found, line_no in ledger_entries(text):
            if obs_id in seen:
                errors.append(
                    f"{name}:{line_no}: duplicate id {obs_id}, already used in "
                    f"{seen[obs_id]} - ids are permanent and never reused"
                )
            seen[obs_id] = name

            labels = [label for label, _ in found]
            unknown = [l for l in labels[len(ENTRY_FIELDS):]
                       if l not in OPTIONAL_FIELDS]
            if labels[:len(ENTRY_FIELDS)] != list(ENTRY_FIELDS) or unknown:
                errors.append(
                    f"{name}:{line_no}: {obs_id} has fields {labels or 'none'} - it needs "
                    f"exactly {list(ENTRY_FIELDS)}, in that order, optionally followed by "
                    f"{list(OPTIONAL_FIELDS)}"
                )
                continue
            values = dict(found)
            if "Last raised" in values and not ISO_DATE.match(values["Last raised"].strip()):
                errors.append(
                    f"{name}:{line_no}: {obs_id} was last raised "
                    f"'{values['Last raised'].strip()}' - use a YYYY-MM-DD date"
                )
            if values["Status"].strip() not in STATUSES:
                errors.append(
                    f"{name}:{line_no}: {obs_id} has status '{values['Status'].strip()}' - "
                    f"use one of {', '.join(STATUSES)}"
                )
            if not RESTS_ON.match(values["Rests on"].strip()):
                errors.append(
                    f"{name}:{line_no}: {obs_id} rests on '{values['Rests on'].strip()}' - "
                    f"use 'stated outright', 'seen once', or 'seen N times', then the dates"
                )


VOLATILE_HEADING = re.compile(r"^## Volatile claims\s*$", re.M)
VERIFY_BY = re.compile(r"verify by 20\d\d-(?:0[1-9]|1[0-2])\b")


def check_volatile_claims(errors):
    """A claim marked as volatile carries the month it must be re-verified by.

    The section exists so tools/staleness.py can report a claim before it has
    quietly misled someone. An entry with no date is invisible to that report,
    which is worse than not marking it at all - it looks handled.
    """
    for path in sorted(glob.glob(os.path.join(ROOT, "instructions", "**", "*.md"),
                                 recursive=True)):
        text = open(path, encoding="utf-8").read()
        match = VOLATILE_HEADING.search(text)
        if not match:
            continue
        rest = text[match.end():]
        nxt = re.search(r"^## ", rest, re.M)
        body = rest[:nxt.start()] if nxt else rest
        offset = text[:match.end()].count("\n")
        for n, line in enumerate(body.splitlines(), offset + 1):
            if line.startswith("- ") and not VERIFY_BY.search(line):
                errors.append(
                    f"{rel(path)}:{n}: volatile claim with no verify-by month - end it "
                    f"with 'verify by YYYY-MM against <source>' or drop it from the section"
                )


# Line budgets for the files that cost context on every task. The standard in
# CLAUDE.md is ~100 lines a pack; these are recorded ceilings, not targets.
#
# This is a ratchet, not a limit. Shrinking a file is free - drop its recorded
# number when you do. Growing past it fails, which is the point: a file gets
# big one justified paragraph at a time, and nobody notices until the file is
# the problem. Raising a number here is allowed and sometimes right; it shows
# up in the diff and belongs in the commit message, which is the whole
# mechanism. Bumping one to clear a red build without saying why is gate
# evasion (`instructions/testing.md`), same as any other.
#
# Files above the ~100 standard are recorded at what they measure today and
# marked as debt. They are not permission to grow - they are a list of what to
# trim when someone has the time.
PACK_BUDGET = 100

BUDGETS = {
    # The entry point, and deliberately exempt from the ~100-line pack standard.
    # It is over that ceiling and it is not debt.
    #
    # Splitting it has been proposed three times, on the reasoning that reference
    # sessions pay for maintenance rules they never use. That reasoning is wrong,
    # and the file itself shows why: a reference session writes to the ledger and
    # clears the backlog, so it needs the ledger invariant, the secrets invariant
    # and the ledger row under "Changing things" - all of which sit in the half a
    # split would move out. The file already states the ledger rule twice, once
    # per mode, precisely because both modes need it. There is no seam.
    #
    # What a split would actually trade: ~100 lines, about 1.5k tokens, against
    # the one file Claude Code is guaranteed to load. Everything else in this repo
    # is reachable only if an agent follows a pointer. Foundational rules do not
    # belong behind a pointer to save half a percent of a context window.
    #
    # So: raise this number when the entry point genuinely needs to say more, and
    # trim it when something here is redundant. Do not propose the split again
    # without new evidence that the seam exists.
    #
    # 220 -> 248 for "Changing something foundational", which is the rule that
    # governs proposals like the split above. Stated outright by the user: this
    # repo is critical to everything built after it, so a foundational change is
    # weighed thoroughly before it is proposed, not after.
    #
    # 248 -> 262 for the meta-rules pointer, the parked-work rule and the block
    # that reference mode reports through. All three are things a session must
    # not have to follow a pointer to discover: where rules come from, which
    # folder is explicitly not one, and how to say any of it back to the user.
    #
    # 262 -> 290 for "Sharing a learning upstream". This repo is forked, and a
    # fork sending a rule back to the public one is the only path here where
    # something leaves the user's own repository. The ask-first rule that governs
    # it cannot sit behind a pointer for the same reason the secrets invariant
    # cannot: a session that never follows the pointer still has to obey it.
    #
    # 290 -> 295 for the two rows telling a session to rebuild MECHANICS.md and
    # CONTRIBUTING.md. Both are derived from behavior and read by people who
    # never open a pack, so a change that leaves them stale ships a lie to
    # exactly the audience that cannot check it. 295 -> 293 when the parked-work
    # folder was dropped and its paragraph went with it.
    #
    # 293 -> 297 for the routing rules the user restated: load every match rather
    # than a count, re-route at every task boundary rather than only when the work
    # changes kind, and show the report block only when it has news. All three are
    # reference-mode behavior, which is the half of this file that a session
    # working in another repo actually executes.
    "CLAUDE.md": 297,
    "docs/index.md": 95,            # the doc router; keep it a router
    # The pack inventory; grows with the packs. 170 -> 175 for the loading
    # discipline rewrite: no count cap, route every iteration, read the delta.
    # Three rules where there were two, and the third is what makes the second
    # affordable, so none of them stands alone.
    "instructions/index.md": 175,
    # The one always-loaded file that is SUPPOSED to grow, because it grows by
    # learning something and shortens the checkpoint in exchange. 100 -> 165 when
    # it took on the base writing method and both nerdbrain blocks. The approvals
    # block is the only approval channel there is, so its layout has to be in
    # context on every reply, in reference mode too - it cannot live in a pack
    # that only some tasks load.
    # 165 -> 175 for the fill-in scaffolding. A fork starts with this file nearly
    # empty, so it has to say what belongs in each section and what an empty
    # section means. That text is read once per fork and then deleted as real
    # lines replace it - trim this number as they do.
    # 175 -> 185 for the rule that the block only appears when it has something
    # to report. It costs more lines than the rule it replaced because it has to
    # resolve a conflict rather than state a preference: obs-0042 put the `plain`
    # self-check in the block precisely so it happened every reply, and a block
    # that can now be absent needs to say the check still runs when the printing
    # does not.
    "instructions/profile.md": 185,
    # --- already over the ceiling: pinned at their exact current size, so every
    # --- further line is a deliberate, visible decision. Trim one, lower its number.
    "instructions/security.md": 105,
    "instructions/core.md": 165,  # always loaded - the worst one to bloat
    "instructions/documentation.md": 108,
    # The biggest pack here, and the one to trim first when someone has time.
    # It stays whole because there is no honest seam: capture, the backlog
    # sweep and the approval gate all fire at exactly one moment - a task
    # finishing - so any two halves would always load together.
    "instructions/learning.md": 152,
    "memory/index.md": 115,
    "instructions/reversibility.md": 80,
    "instructions/stack-and-architecture.md": 125,  # 122 -> 125, card-on-file axis
    # 100 -> 113 for the dashboard-deploy rule and R2's card gate. The pack sat
    # at 99, so neither could land without cutting an approved rule - the trade
    # profile.md says not to make. No honest seam either: deploys, storage
    # primitives and caching all fire on "Cloudflare is in play".
    # 100 -> 128 for how a PocketHost deploy actually behaves: migrations apply
    # on the instance's next start rather than on upload, there is no remote
    # rollback because SFTP has no shell, and Admin Sync makes the account
    # password a superuser credential. Each was learned by getting it wrong
    # once. Splitting the deploy half out was refused deliberately - the whole
    # point is that these are in context whenever PocketHost is referenced, so
    # both halves would always load together and cost more than one file.
    "instructions/testing.md": 95,
    # 100 -> 115 for "The config file". The pack was exactly at the ceiling, so
    # the rule could not land without either cutting an approved one or raising
    # this. Splitting was weighed and refused: the new section is 14 lines, and
    # a 14-line half that loads on the same trigger as the other 101 costs more
    # than the whole file did. Trimming was refused too - cutting approved rules
    # to make room for new ones is the trade `profile.md` says not to make.
    "instructions/ux-admin.md": 115,
}


# The set read at the top of every session, whatever it is split across. This
# tuple is the declaration of what "always loaded" means, and its total is
# capped - so splitting a big always-on file into three smaller ones cannot
# clear the per-file budgets while costing a reader exactly as much as before.
#
# The total is the sum of the members' own budgets above: 297 + 175 + 165 + 185.
# Every member now has an entry, profile.md included - it earned one when it took
# on the writing method and the nerdbrain block, both of which have to apply to
# every reply and so cannot live in an on-demand pack.
#
# 689 -> 787 as those landed, then 787 -> 803: up for the upstream-contribution rule
# and the profile's fill-in scaffolding, down further when the platform table left the
# router. The ratchet works in both directions and this is the direction to prefer.
#
# 803 -> 822 for the routing and reporting rules stated outright by the user
# (obs-0045 to obs-0047). This is the trade the always-loaded set exists to make
# visible: 19 lines paid on every session, against a sub-task that runs on the
# wrong packs because nobody re-checked, and a status block nobody reads because
# it speaks every turn. Worth it, and worth seeing in the diff. The profile is still the member that is SUPPOSED to
# grow, because it grows by learning something and pays for itself by shortening
# the checkpoint - a profile that answers three standard questions has already
# earned its lines back.
#
# Growth *inside* a member is rule 9's job and binds first; this rule binds when
# the *set itself* grows - a fifth file declared always-loaded blows the total
# immediately, which is the case it exists for.
#
# Leaving a new file out of this tuple is a claim that it is NOT always loaded,
# which is a change to when its rules apply, and belongs at a checkpoint.
ALWAYS_LOADED = ("CLAUDE.md", "instructions/index.md", "instructions/core.md",
                 "instructions/profile.md")
ALWAYS_LOADED_BUDGET = 822


def check_always_loaded_total(errors):
    total = sum(
        len(open(os.path.join(ROOT, name), encoding="utf-8").read().rstrip("\n").split("\n"))
        for name in ALWAYS_LOADED
    )
    if total > ALWAYS_LOADED_BUDGET:
        listed = ", ".join(ALWAYS_LOADED)
        errors.append(
            f"the always-loaded set ({listed}) totals {total} lines, over its "
            f"{ALWAYS_LOADED_BUDGET}-line budget - every session pays this before it "
            f"starts; splitting a file across more files does not reduce it"
        )


def budgeted_files():
    """Governed: CLAUDE.md, the two routers, and every instruction pack.

    Not the per-platform doc indexes - those are opened one at a time, by a
    reader who wants that platform, so Gumroad's 400 lines cost nothing to
    anyone reading about PocketBase. The whole point of the router split was to
    make their size not matter.

    Not memory/observations.md or memory/archive.md either. Those are data and
    they are meant to grow: the ledger accumulating evidence is the mechanism,
    not the problem. memory/index.md is the part that gets read to understand
    them, so that one is budgeted like a pack.
    """
    files = {"CLAUDE.md", "AGENTS.md", "docs/index.md", "memory/index.md"}
    for path in glob.glob(os.path.join(ROOT, "instructions", "**", "*.md"), recursive=True):
        files.add(os.path.relpath(path, ROOT).replace(os.sep, "/"))
    return sorted(files)


def check_line_budgets(errors):
    for name in budgeted_files():
        path = os.path.join(ROOT, name)
        count = len(open(path, encoding="utf-8").read().rstrip("\n").split("\n"))
        budget = BUDGETS.get(name, PACK_BUDGET)
        if count > budget:
            errors.append(
                f"{name}: {count} lines, over its {budget}-line budget - trim it, or "
                f"raise the budget in tools/check.py and say why in the commit message"
            )


WRAP = 95


def check_wrap_width(errors):
    """Prose wraps at ~95 columns, where wrapping is possible at all.

    A line is exempt when a single unbreakable token - a long path, a snapshot
    filename, a URL - is itself wider than the room left for it, because no
    amount of wrapping would help. Tables, fenced code and YAML frontmatter are
    skipped for the same reason: their width isn't a prose choice.
    """
    for path in md_files():
        name = rel(path).replace(os.sep, "/")
        in_fence = in_front = False
        for n, raw in enumerate(open(path, encoding="utf-8"), 1):
            line = raw.rstrip("\n")
            if line.startswith("```"):
                in_fence = not in_fence
                continue
            if n == 1 and line.strip() == "---":
                in_front = True
                continue
            if in_front:
                if line.strip() == "---":
                    in_front = False
                continue
            if in_fence or line.startswith(("|", "    ", "\t")) or len(line) <= WRAP:
                continue
            indent = len(line) - len(line.lstrip())
            longest = max((len(tok) for tok in line.split()), default=0)
            if indent + longest > WRAP:
                continue  # unwrappable: one token is wider than the line allows
            errors.append(
                f"{name}:{n}: {len(line)} columns, over {WRAP} - rewrap the paragraph"
            )


def check_skill_triggers_on_platforms(errors):
    """The /nerdbrain skill triggers on platform names in its description. A
    platform pack whose name is missing there is unreachable by name."""
    skill = open(os.path.join(ROOT, "skill", "nerdbrain", "SKILL.md"),
                 encoding="utf-8").read()
    description = next(
        (l for l in skill.splitlines() if l.startswith("description:")), "").lower()
    for path in glob.glob(os.path.join(ROOT, "instructions", "platforms", "*.md")):
        stem = os.path.basename(path)[:-3]
        if stem.startswith("_"):
            continue
        if stem.replace("-", " ") not in description:
            errors.append(
                f"skill/nerdbrain/SKILL.md: platform '{stem}' missing from the "
                f"frontmatter description - add it so /nerdbrain triggers on its name"
            )


def main():
    errors = []
    for check in (check_refs, check_dated_names, check_page_cites,
                  check_index_lists_packs, check_index_lists_pdfs,
                  check_indexed_pdfs_exist, check_skill_triggers_on_platforms,
                  check_capture_folders_are_routed, check_line_budgets,
                  check_always_loaded_total, check_wrap_width,
                  check_ledger_entries,
                  check_volatile_claims):
        check(errors)
    if errors:
        print(f"FAIL - {len(errors)} violation(s). Each message names its fix; "
              f"rebuild the derived content, don't just silence the error:")
        for e in errors:
            print(" ", e)
        return 1
    print("ok - references resolve, no dated names or page cites outside the "
          "indexes, packs and snapshots indexed both directions, every capture "
          "folder routed, skill triggers cover all platforms, files inside "
          "their line budgets, ledger entries parse, volatile claims dated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
