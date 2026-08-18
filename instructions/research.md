# Research & Docs

Load when: touching an unfamiliar API, library, or service, or making any factual claim
about how one behaves.

## The rule

**Never invent an API.** No guessed method names, parameters, response shapes, config keys,
env var names, rate limits, or pricing. If you haven't verified it, either verify it or say
plainly that you haven't.

A plausible-looking wrong method name costs more debugging time than asking would have cost.

## Order of sources

1. **Official current docs online.** The source of truth for anything version-sensitive:
   API surface, limits, pricing, free-tier ceilings, deprecations, current best practice.
2. **The snapshots in `../docs/`.** Local, fast, no network, and mapped by page range in
   each platform's index, which `../docs/index.md` routes you to. Best for orientation, and
   for reading a lot of one thing cheaply.
   **They are dated snapshots** — the date is in the filename. Treat them as accurate for
   concepts and shapes, and as possibly stale for limits, prices, and recent additions.
3. **The library's actual source or type definitions** in `node_modules`. Beats prose docs
   for exact signatures.
4. **Nothing else.** Not memory, not a blog post, not what the API "probably" looks like.

Practical flow: orient in the local snapshot, then verify anything that could have changed
against the live docs. If a live check isn't possible, use the snapshot and **say which
version/date you relied on.**

## Using the local snapshots

`../docs/index.md` names the platforms and points at their indexes; the index beside a
platform's PDFs maps them to page ranges by topic. Open the one platform you need.

- Read the page range for the topic, not the whole file. These run 24–225 pages. In
  Claude Code, the `Read` tool takes a `pages` parameter (20 pages per call at most); in
  another harness, use whatever partial-read mechanism it has.
- Filenames are versioned (`<source>_<YYYYMMDD>_<HHMM>[_partN].pdf`) and change on every
  refresh. Reference snapshots by source prefix — `references/<source>/<source>_*.pdf` —
  never by exact name; only the per-source indexes hold those. A listed name missing from
  disk means the snapshot was refreshed: glob the prefix and fix the index, don't conclude
  the docs are gone.
- If the index doesn't cover what you need, search adjacent ranges before reading broadly.
- When you find something the index doesn't list, add it to the index.

## Verifying

- Prefer the docs page that shows a full request and response over the prose description.
- Check the version. Docs for v3 will actively mislead you on v2.
- For anything about cost or quota, get the number and cite where it came from. Never
  estimate a free-tier limit from memory — those change and are load-bearing for
  architecture (see `stack-and-architecture.md`).
- When docs and observed behavior disagree, trust observed behavior and note the conflict.

## Saying what you don't know

Good: "The docs cover the create call; they don't say whether batch is rate-limited
separately. Assuming it is, and building with backoff. Worth confirming."

Bad: silently picking a limit and building around it.

Every unverified assumption gets stated where the user will see it, not buried in a
comment.

A hedge in chat does not travel. The code comment, the commit message, the README line and
the PR body outlive the conversation, and each one repeats the claim as settled fact to
whoever reads it next. Mark it where you write it down — "per the docs, unverified" — or
leave the claim out. One wrong assertion means correcting every artifact that carried it.

## Adding to this repo

When you research a platform thoroughly enough to be useful twice, write it down:

- Platform gets a pack in `instructions/platforms/` (start from `platforms/_template.md`)
- Vendor docs go in `docs/references/<platform>/`, indexed with page ranges in that
  folder's `index.md`, with a router row in `docs/index.md`
- Put the capture date in the filename, as the existing files do
- Replacing a snapshot means: new file in, old file out, the platform index updated,
  page maps re-derived — `tools/index-pdf.py` drafts them. Packs cite topics by name and
  never page numbers, so a refresh touches only the doc indexes, not the instructions
- `tools/check.py` detects an incomplete refresh from either direction (unindexed file on
  disk, indexed file missing from disk). Run it after any docs change and treat each
  failure as a rebuild instruction — the message names the fix
