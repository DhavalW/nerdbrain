#!/usr/bin/env python3
"""Draft index entries for capture PDFs that don't have any yet.

Dropping a PDF into `docs/references/<platform>/` leaves the repo red: rule 5 of
`tools/check.py` sees a snapshot its index doesn't list. The fix is mechanical -
add the `## Files` row with a page count, then draft a page map with
`tools/index-pdf.py` - and mechanical work should not need a session.

So this does the mechanical half and nothing else. It appends the file rows and
a page map clearly marked as an unreviewed draft, and the `index-captures`
workflow opens a PR with the result. What it deliberately does NOT do:

  * Invent an index for a new platform folder. That file records the source URL,
    the capture date and the companion pack - none of which are on disk to be
    read. It reports the folder and stops.
  * Decide between grouped and per-page maps. It drafts grouped; an
    article-per-page capture wants `index-pdf.py --per-page` instead.
  * Merge the over-split rows or name topics the way the document names them.
    `index-pdf.py` says its output is a draft, and it means it.

That last part is why this opens a PR instead of pushing: the draft is a
starting point for a human pass, not an answer.

Usage:
    pip install pymupdf
    python3 tools/autoindex.py            # write the drafts
    python3 tools/autoindex.py --dry-run  # just say what it would do
"""

import argparse
import glob
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check import files_section, PDF_IN_TICKS  # noqa: E402  same invariant, one definition

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PDF = os.path.join(ROOT, "tools", "index-pdf.py")

DRAFT_MARKER = "draft map, unreviewed"

FILES_HEADING = re.compile(r"^## Files\s*$", re.M)
NEXT_HEADING = re.compile(r"^## ", re.M)
PDF_BULLET = re.compile(r"^- `[^`]+\.pdf`.*$", re.M)


def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def page_count(pdf):
    import pymupdf
    with pymupdf.open(pdf) as doc:
        return doc.page_count


def unindexed():
    """(folder, index_path, [pdf, ...]) per capture folder with missing entries."""
    out = []
    for folder in sorted(glob.glob(os.path.join(ROOT, "docs", "references", "*"))):
        if not os.path.isdir(folder):
            continue
        on_disk = sorted(glob.glob(os.path.join(folder, "*.pdf")))
        if not on_disk:
            continue
        index_path = os.path.join(folder, "index.md")
        if not os.path.exists(index_path):
            out.append((folder, None, on_disk))
            continue
        section = files_section(open(index_path, encoding="utf-8").read())
        listed = set() if section is None else set(PDF_IN_TICKS.findall(section))
        missing = [p for p in on_disk if os.path.basename(p) not in listed]
        if missing:
            out.append((folder, index_path, missing))
    return out


def draft_map(pdf):
    """index-pdf.py's grouped draft, or a note if it could not be produced."""
    result = subprocess.run(
        [sys.executable, INDEX_PDF, pdf],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return f"_Map could not be drafted: {result.stderr.strip().splitlines()[-1]}_"
    return result.stdout.strip()


def files_span(text):
    """(start, end) of the `## Files` body, or None when there is no such section.

    Indices, not the substring: a short or blank section is not unique in the
    file, and splicing it back by content rewrites the first place it happens to
    match instead of the section itself.
    """
    match = FILES_HEADING.search(text)
    if not match:
        return None
    nxt = NEXT_HEADING.search(text, match.end())
    return match.end(), nxt.start() if nxt else len(text)


def add_file_rows(index_path, pdfs):
    """Add `## Files` rows for each PDF, keeping the section's own format."""
    text = open(index_path, encoding="utf-8").read()
    rows = "".join(
        f"- `{os.path.basename(p)}` — {page_count(p)} pages\n" for p in pdfs
    )
    span = files_span(text)
    if span is None:
        return text.rstrip("\n") + f"\n\n## Files\n\n{rows}"
    start, end = span
    bullets = list(PDF_BULLET.finditer(text[start:end]))
    if bullets:
        # Join the existing list rather than landing under the prose below it.
        at = start + bullets[-1].end()
        return text[:at] + "\n" + rows.rstrip("\n") + text[at:]
    # `\s*$` in the heading pattern already ate the blank line after it.
    return text[:start].rstrip("\n") + "\n\n" + rows + "\n" + text[end:].lstrip("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true",
                        help="report what would be drafted, write nothing")
    args = parser.parse_args()

    work = unindexed()
    if not work:
        print("Nothing to do - every capture is indexed.")
        return 0

    needs_human = []
    drafted = []

    for folder, index_path, pdfs in work:
        if index_path is None:
            needs_human.append(rel(folder))
            continue
        names = [os.path.basename(p) for p in pdfs]
        print(f"{rel(index_path)}: drafting {len(names)} entr(y/ies): {', '.join(names)}")
        if args.dry_run:
            drafted.append((rel(index_path), names))
            continue

        text = add_file_rows(index_path, pdfs)
        maps = "\n\n".join(
            f"## {os.path.basename(p)} — {DRAFT_MARKER}\n\n"
            f"Drafted by `tools/autoindex.py`. Merge the over-split rows and rename each\n"
            f"topic the way the document does before trusting this map. An\n"
            f"article-per-page capture wants `index-pdf.py --per-page` instead.\n\n"
            f"```\n{draft_map(p)}\n```"
            for p in pdfs
        )
        open(index_path, "w", encoding="utf-8").write(
            text.rstrip("\n") + "\n\n" + maps + "\n"
        )
        drafted.append((rel(index_path), names))

    if needs_human:
        print("\nCapture folders with no index.md - these need a person:")
        for folder in needs_human:
            print(f"  {folder}: create index.md (source URL, capture date, companion "
                  f"pack, `## Files`), then re-run")

    return 0


if __name__ == "__main__":
    sys.exit(main())
