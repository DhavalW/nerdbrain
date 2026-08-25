#!/usr/bin/env python3
"""Draft a topic -> page-range map for a doc snapshot PDF.

Usage:
    pip install pymupdf   # once
    python3 tools/index-pdf.py docs/references/<platform>/<source>_<date>_<time>.pdf
    python3 tools/index-pdf.py --per-page docs/references/<platform>/<snapshot>.pdf

For each page it takes the largest-font text spans as the page's heading, then
groups consecutive pages that fall under the same top-level heading into ranges
and prints a draft markdown table for docs/index.md.

The output is a DRAFT. Read it, merge over-split rows, name the topics properly,
and only then paste it into the index. --per-page prints the raw page:heading
list instead, which is the better starting point for article-per-page captures
like the AppSumo help centre.
"""

import argparse
import sys

try:
    import pymupdf
except ImportError:
    sys.exit("pymupdf not installed. Run: pip install pymupdf")


def page_headings(page):
    """All text spans on the page, as (font_size, text), largest first."""
    spans = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span["text"].strip()
                if len(text) > 2:
                    spans.append((round(span["size"], 1), text))
    spans.sort(key=lambda s: -s[0])
    return spans


def top_heading(spans):
    """Join the spans sharing the page's largest font size into one heading."""
    if not spans:
        return None, None
    top_size = spans[0][0]
    parts = [t for s, t in spans if s >= top_size - 0.1]
    return top_size, " ".join(parts)[:120]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdf")
    ap.add_argument("--per-page", action="store_true",
                    help="print raw page:heading lines instead of a grouped table")
    args = ap.parse_args()

    doc = pymupdf.open(args.pdf)
    pages = [(i + 1, *top_heading(page_headings(p))) for i, p in enumerate(doc)]

    print(f"# {args.pdf} — {len(doc)} pages\n")

    if args.per_page:
        for num, size, head in pages:
            print(f"{num:>4}: {head or '(no text)'}")
        return

    # A heading well above the document's median top-size marks a new section;
    # smaller top-headings are subsections and stay inside the current range.
    sizes = sorted(s for _, s, _ in pages if s)
    cutoff = sizes[len(sizes) // 2] if sizes else 0

    sections = []
    for num, size, head in pages:
        if head and size and size >= cutoff and (not sections or head != sections[-1][0]):
            sections.append([head, num, num])
        elif sections:
            sections[-1][2] = num

    print("| Topic | Pages |")
    print("|---|---|")
    for head, start, end in sections:
        rng = str(start) if start == end else f"{start}–{end}"
        print(f"| {head} | {rng} |")
    print(f"\n(draft: {len(sections)} sections — merge over-split rows before pasting)")


if __name__ == "__main__":
    main()
