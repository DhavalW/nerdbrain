# Doc Index

Local snapshots of the documentation your work depends on — vendor APIs, platform guides,
contracts, regulations, internal specs. This file is a router, not a map: it says which
sources have a capture and where each one's index lives. **The page maps and exact
filenames are in the per-source indexes** — open the one you need and nothing else.

**A fresh fork ships with no captures**, and the table below is empty. That is not a
missing feature: what belongs here is *your* documentation, and nobody else's is a
substitute. The mechanism is what ships — indexing, routing, page maps, the gate that
keeps them honest, and a workflow that drafts an index the moment a PDF lands.

## How to use this

1. **Find the source below and open its index.** That file lists its captures, their exact
   filenames, and the topic → page-range map.
2. **Read the page range, not the file.** These are large. In Claude Code, the `Read` tool
   takes a `pages` parameter (`"41-48"`), max 20 pages per call; elsewhere, use the
   harness's partial-read mechanism.
3. **These are dated snapshots.** The capture date is in the filename. Concepts and API
   shapes are reliable; **limits, prices, and recent additions may be stale** — verify those
   against the live source (`../instructions/research.md`).

Companion instruction packs live in `../instructions/platforms/`. They cite doc topics by
name — never by page — and resolve them through these indexes at read time.

## Captures

| Source | Captured | Index |
|---|---|---|

_Empty. Add a row when the first capture lands._

## Where the PDFs come from

Any PDF works — an export, a scan, a spec someone emailed you. What the maps need is
selectable text; a scan without OCR indexes to nothing.

For documentation that only exists as a website, the capture step is turning a doc site
into a paginated PDF. **SiteToPDF** is the companion tool for that job: it crawls a docs
site and produces the dated, multi-part PDFs this index is shaped around, in the
`<source>_<YYYYMMDD>_<HHMM>[_partN].pdf` form the gate expects. Nothing here requires it —
the naming convention is the only contract, and any tool that meets it works the same way.

It can also fetch its own worklist. `scrape-list.md` is a queue of start URLs a session
wrote down when it hit a docs gap; SiteToPDF reads it out of GitHub, captures each row into
`references/<source>/`, and appends a receipt to `scrape-done.md` for the next session to
verify and clear (`../instructions/doc-capture.md`).

## Filenames are versioned

Captures are named `<source>_<YYYYMMDD>_<HHMM>[_partN].pdf` — the exact string changes with
every refresh. So:

- **One folder per source under `references/`**, holding its captures and an `index.md`.
  A snapshot's path is `references/<source>/<name>_<date>_<time>[_partN].pdf`.
- **Exact filenames live only in these indexes** — this router names none. Everywhere else
  (platform packs, other docs) references a snapshot by source prefix,
  `references/<source>/<source>.io_*.pdf`, and resolves the real name in the index.
- **Every index carries a `## Files` section** listing each PDF in its folder as
  `- \`<name>.pdf\` — <N> pages`. That section is the manifest, and `tools/check.py` tallies
  it against the folder in both directions: a PDF on disk that isn't listed, or a listed name
  that isn't on disk, fails the build. Mentioning a filename in prose elsewhere in the index
  does not count — the manifest stays in one place.
- **If a name an index lists doesn't exist on disk**, don't conclude the docs are gone: glob
  for the source prefix, use what you find, and fix that index.
- **Instruction packs never carry page numbers.** They cite topics by name (*Going to
  production*, *Rate limits*) and resolve them in the source's index at read time. Keep
  topic names close to the documents' own headings so those citations keep resolving across
  refreshes.

## Adding or refreshing a capture

- **New capture for an existing source:** add every file to that index's `## Files`
  section with its page count, and a page map drafted with `python3 tools/index-pdf.py <pdf>`
  (`--per-page` for article-per-page captures). Update the router row's file and page counts.
- **New source:** create `references/<source>/index.md` — source URL, capture date, companion
  pack, a `## Files` section, then the maps — and add a router row here. The gate enforces
  all three.
- **Record the source URL in the index**, not just the domain. A refresh starts by going
  back to the page that was captured, and reconstructing that from a filename prefix is
  archaeology. `tools/staleness.py` lists the indexes still missing one.
- **Replacing a snapshot:** add the new file, update the index's `## Files` section, and
  **re-derive its page map**. Page numbers shift between captures, so the old map is void, not
  approximately right. Move the old PDF out; never leave two captures of one source sitting
  ambiguously side by side.
- **`tools/check.py` polices all of this from both directions** — a PDF its index doesn't
  list, a name listed with no file behind it, an index no router row points at, a snapshot
  sitting outside a capture folder. Run it after touching anything under `docs/`.
- **A PDF pushed with no index entry opens its own PR.** The `index-captures` workflow
  drafts the `## Files` rows and the page map and puts them up for review, so dropping a
  capture into the repo is the whole job. The draft still needs a human pass: `index-pdf.py`
  over-splits, and topic names have to match the document's own headings.

## What's missing

`wanted.md` is the other half of this index: the docs a session needed and this repo didn't
have and no crawler can fetch — a PDF someone has to obtain, a page range a map never
covered. Anything with a crawlable start URL goes on `scrape-list.md` instead. Both get
written the moment a session falls through to live docs, which is the only moment anyone
knows.
