#!/usr/bin/env python3
"""Freshness report for this repo. Reports; it does not fail the build.

`tools/check.py` gates what is structurally wrong right now. This reports what
is quietly going out of date, which is a different thing: nothing here is a
defect on the day it appears, and making CI red because a date passed would
turn an unrelated push into someone else's problem.

Four questions:

  1. Which volatile claims are past their verify-by date? Packs mark the claims
     that decay - limits, prices, free-tier ceilings - in a `## Volatile claims`
     section, as pointers to the live source rather than copies of the value.
  2. Which platform packs have no such section at all? Either they carry nothing
     that decays, or nobody has looked. Both are worth seeing.
  3. Which captures are old enough that concepts are still fine but specifics
     probably aren't?
  4. Which capture indexes don't record where they were captured from? Without
     the source URL a refresh starts with archaeology.

The output is written to be pasted into a PR body or an issue. Exit code is 0
unless --strict, which the weekly promotion run does not use.

Pure stdlib - no dependencies.
"""

import argparse
import datetime as dt
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check import LEDGER_FILES, ledger_entries  # noqa: E402  one parser, not two

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VOLATILE_HEADING = re.compile(r"^## Volatile claims\s*$", re.M)
VERIFY_BY = re.compile(r"verify by (20\d\d)-(0[1-9]|1[0-2])\b")
CAPTURE_DATE = re.compile(r"_(20\d\d)(\d\d)(\d\d)_\d{4}")
# A `Source:` line, not any URL anywhere in the file. These indexes are page
# maps of documentation, and documentation quotes URLs constantly - matching
# loosely passed an index whose only http string was a Gumroad API field
# description caught mid-word in a table row.
SOURCE_FIELD = re.compile(r"^Source:\s*<?https?://\S", re.M)

CAPTURE_STALE_MONTHS = 6

# Ripe means the bar the weekly promotion run works to: said outright, or seen
# at least twice. `seen once` is not ripe - it stays open and keeps collecting.
RIPE_EVIDENCE = re.compile(r"^(?:stated outright|seen (\d+) times)")

# How long a ripe entry sits before a session should raise it in conversation.
# Long enough that the weekly job gets first refusal, short enough that a repo
# with no credential configured still moves.
UNPICKED_DAYS = 10


def months_between(then, now):
    return (now.year - then.year) * 12 + (now.month - then.month)


def section(text, heading):
    """The body of a `## ` section: everything up to the next `## `."""
    match = heading.search(text)
    if not match:
        return None
    rest = text[match.end():]
    nxt = re.search(r"^## ", rest, re.M)
    return rest[:nxt.start()] if nxt else rest


def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def packs():
    return sorted(glob.glob(os.path.join(ROOT, "instructions", "**", "*.md"),
                            recursive=True))


def overdue_claims(today):
    """Volatile claims whose verify-by month has passed."""
    out = []
    for path in packs():
        body = section(open(path, encoding="utf-8").read(), VOLATILE_HEADING)
        if not body:
            continue
        for line in body.splitlines():
            match = VERIFY_BY.search(line)
            if not match:
                continue
            due = dt.date(int(match.group(1)), int(match.group(2)), 1)
            if months_between(due, today) >= 0:
                claim = line.strip().lstrip("- ").split(" — ")[0]
                out.append((rel(path), f"{due:%Y-%m}", claim))
    return out


def unmarked_platform_packs():
    """Platform packs with no `## Volatile claims` section."""
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "instructions", "platforms", "*.md"))):
        if os.path.basename(path).startswith("_"):
            continue
        if not VOLATILE_HEADING.search(open(path, encoding="utf-8").read()):
            out.append(rel(path))
    return out


def aging_captures(today):
    """Capture folders whose newest snapshot is older than the threshold."""
    out = []
    for folder in sorted(glob.glob(os.path.join(ROOT, "docs", "references", "*"))):
        if not os.path.isdir(folder):
            continue
        dates = []
        for pdf in glob.glob(os.path.join(folder, "*.pdf")):
            match = CAPTURE_DATE.search(os.path.basename(pdf))
            if match:
                dates.append(dt.date(*(int(g) for g in match.groups())))
        if not dates:
            continue
        newest = max(dates)
        age = months_between(newest, today)
        if age >= CAPTURE_STALE_MONTHS:
            out.append((rel(folder), f"{newest:%Y-%m-%d}", age))
    return out


def awaiting_a_person(today):
    """Ripe `open` entries that nothing has picked up.

    The weekly promotion run gets first refusal on these. When it isn't running
    - no credential configured, which is the default state of a fresh clone -
    nothing else would ever raise them, and the ledger would fill up with rules
    the user never got asked about. So after UNPICKED_DAYS they become the
    session's job: any task finishing with this repo in context puts them to the
    user directly (`../instructions/learning.md`).

    `Last raised` restarts the clock, which is what keeps that from turning into
    the same three proposals at the end of every task.
    """
    out = []
    for name in LEDGER_FILES:
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            continue
        for obs_id, first_seen, found, _line in ledger_entries(
                open(path, encoding="utf-8").read()):
            values = {label: value.strip() for label, value in found}
            if values.get("Status") != "open":
                continue
            match = RIPE_EVIDENCE.match(values.get("Rests on", ""))
            if not match or (match.group(1) and int(match.group(1)) < 2):
                continue
            since = values.get("Last raised") or first_seen
            try:
                waited = (today - dt.date.fromisoformat(since)).days
            except ValueError:
                continue
            if waited >= UNPICKED_DAYS:
                out.append((obs_id, waited, values.get("Observation", ""),
                            values.get("Target", "unplaced")))
    return sorted(out, key=lambda row: -row[1])


def indexes_without_source(_today=None):
    """Capture indexes that record no URL to re-capture from."""
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "docs", "references", "*", "index.md"))):
        if not SOURCE_FIELD.search(open(path, encoding="utf-8").read()):
            out.append(rel(path))
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 if anything is overdue (default: report only)")
    parser.add_argument("--today", metavar="YYYY-MM-DD",
                        help="evaluate against this date instead of today")
    args = parser.parse_args()

    today = (dt.date.fromisoformat(args.today) if args.today
             else dt.date.today())

    claims = overdue_claims(today)
    unmarked = unmarked_platform_packs()
    aging = aging_captures(today)
    sourceless = indexes_without_source()
    waiting = awaiting_a_person(today)

    print(f"# Freshness report — {today:%Y-%m-%d}\n")

    print("## Ledger entries waiting on a person\n")
    if waiting:
        print(f"Ripe for {UNPICKED_DAYS}+ days and still `open`. Raise these in "
              f"conversation at the end of the next task, then set `Last raised`:\n")
        for obs_id, waited, observation, target in waiting:
            print(f"- **{obs_id}** ({waited} days) → {target}\n  {observation}")
    else:
        print("None.")

    print("\n## Claims past their verify-by date\n")
    if claims:
        for path, due, claim in claims:
            print(f"- `{path}` — due {due} — {claim}")
    else:
        print("None.")

    print("\n## Platform packs with nothing marked as volatile\n")
    if unmarked:
        print("Either they carry no decaying claim, or nobody has checked:\n")
        for path in unmarked:
            print(f"- `{path}`")
    else:
        print("None.")

    print(f"\n## Captures older than {CAPTURE_STALE_MONTHS} months\n")
    if aging:
        print("Concepts and shapes are still good; limits, prices and new features are not:\n")
        for path, newest, age in aging:
            print(f"- `{path}` — newest capture {newest} ({age} months)")
    else:
        print("None.")

    print("\n## Capture indexes with no source URL\n")
    if sourceless:
        print("Add the URL the capture came from, so refreshing it is a click:\n")
        for path in sourceless:
            print(f"- `{path}`")
    else:
        print("None.")

    overdue = bool(claims or aging)
    if args.strict and overdue:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
