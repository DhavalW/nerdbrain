# Scrape done

What the capture tool finished. One row per successful run: the source it captured, where
it started, and what it got. **Nothing writes here by hand** — a row is the tool's receipt,
and the next session's job is to check it against what is actually on disk.

Rows are not the record. `references/<source>/index.md` is the record; this file is the
handoff between a tool that cannot read the repo's indexes and a session that can. A row
lives for one reconcile and then goes, along with the `scrape-list.md` row that asked for
it (`../instructions/doc-capture.md`).

**A row here is a claim, not proof.** The tool reports what it committed; whether the PDF
is on disk, has selectable text, and is indexed is checked by the session that clears it.
An unverifiable row stays put and says why.

## The shape

Five columns, in this order, appended under `## Captured`:

| Column | What the tool writes |
|---|---|
| `Source` | The `Source` from the queue row, unchanged |
| `Start URL` | The `Start URL` from the queue row, unchanged |
| `Captured` | `YYYY-MM-DDTHH:MMZ`, UTC, when the run finished |
| `Pages` | How many pages the crawl captured |
| `Parts` | How many PDF files it split into — 1 unless the capture was large |

Filenames are deliberately absent. They carry a timestamp that shifts with every refresh,
and this repo resolves a snapshot by source prefix and reads the exact name out of the
platform's own index beside the PDFs. A row that named files would be a second place
for them to drift.

## Captured

| Source | Start URL | Captured | Pages | Parts |
|---|---|---|---|---|

_Empty. Rows arrive when a capture lands and leave when a session verifies it._
