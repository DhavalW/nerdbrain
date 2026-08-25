# Scrape list

The queue. One row per documentation site that should exist under `references/` and
doesn't — or exists and has gone stale. A session writes rows here when the work needs
docs this repo can't answer from; a capture tool reads them, crawls each start URL, and
commits the PDF where the row says. Nothing here governs anything: it is a worklist that
happens to be machine-readable.

**The shape is fixed, because a program parses it.** A malformed row is a capture that
silently never happens, so `../tools/check.py` rejects one rather than letting it sit here
looking queued.

## How to add a row

Append to the table under `## Queue`. Four columns, in this order, no others:

| Column | What goes in it |
|---|---|
| `Source` | The folder under `references/`. Lowercase, digits, single hyphens |
| `Start URL` | `https://…` — where the crawl starts. It stays inside that section |
| `Wanted for` | One short line: what the work needed. No pipes, no line breaks |
| `Requested` | `YYYY-MM-DD`, the day the row was written |

- **The source is the folder, and it is also the filename stem.** A row with source
  `pocketbase` produces `references/pocketbase/pocketbase_<date>_<time>.pdf` and an index
  beside it. Reuse the existing folder name when refreshing, or the refresh lands in a new
  folder next to the old one.
- **Point the start URL at the section, not the home page.** A crawl scopes itself to its
  start URL's directory, so `https://site.com/docs/api` captures the API reference and
  `https://site.com` captures a marketing site.
- **One row per source.** Wanting more of a site that is already queued is a reason to
  widen the start URL, not to add a second row.
- **A refresh is a row too.** Same source, same folder — the capture replaces what is
  there. Say so in `Wanted for` ("stale — pricing changed").
- **No URL to crawl?** It belongs in `wanted.md` instead: a PDF someone has to obtain by
  hand, a page range an index doesn't cover, an index fix. The two files are disjoint on
  purpose — this one is only the part a crawler can do unattended.

Adding a row needs no approval. Removing one is the job of the reconcile step in
`../instructions/doc-capture.md`, and it happens only once the capture is on disk.

## Queue

| Source | Start URL | Wanted for | Requested |
|---|---|---|---|

_Empty. The first row arrives the first time a session needs docs this repo doesn't have._
