# Doc capture

Load when: the task needed documentation this repo doesn't have, or a session is starting
and `../docs/scrape-done.md` has rows in it.

Two halves of one loop. A session that hits a docs gap writes the gap down as a row a
crawler can act on; the next session checks what the crawler committed and clears the row.
Neither half asks permission, because neither changes a rule — the queue is a worklist and
the receipt is a fact about the filesystem.

The crawler is not part of this repo and does not have to be. **SiteToPDF** reads
`../docs/scrape-list.md` out of GitHub, captures each row, commits the PDF under
`../docs/references/`, and appends to `../docs/scrape-done.md`. Any tool that honours those
two files works identically. Nothing here waits on one being connected: the rows are worth
writing even when the only thing that will ever act on them is a person.

## Queue a gap the moment you hit one

The trigger is falling through to live docs, or wanting to and not being able to. That
session is the only one that knows the gap exists, and it knows for about a minute.

- **A crawlable start URL goes in `../docs/scrape-list.md`**, in the four-column shape that
  file sets out. Anything else — a PDF someone has to obtain, a page range an index missed —
  goes in `../docs/wanted.md`. Disjoint on purpose.
- **Write the row at the end of the task**, with the ledger entry, not mid-work.
- **Name the section, not the site.** The crawl scopes itself to the start URL's directory,
  so a URL one level too high captures a marketing site and one level too low captures four
  pages.
- **A stale capture is a row too** — same source, same folder, `Wanted for` saying what
  went out of date. The refresh replaces the file it supersedes.
- **Say so in the report.** One line naming the source and why, so the user can strike it
  before anything crawls.

## Reconcile at the start of a session

`../docs/scrape-done.md` with rows in it means a capture landed since the last session.
Clear it before starting the task — it is a filesystem check and a small edit, and leaving
it means the same rows are re-checked every session from now on.

For each row, all five have to hold:

1. **The PDF is on disk.** Glob `../docs/references/<source>/<source>_*.pdf`. Match the
   source prefix, never a filename from the row — the row deliberately carries none.
2. **It has selectable text.** Read a page from the middle. A scan with no OCR indexes to
   nothing, and the row is the only warning anyone gets.
3. **It is what was asked for.** The pages belong to the section the `Start URL` names, and
   there are roughly as many as `Pages` claims.
4. **The folder's `index.md` lists it** in `## Files` and maps its topics to page ranges.
   Missing? That is the reconcile's work, not a reason to fail the row — draft the map with
   `../tools/index-pdf.py` and write the entry.
5. **`../docs/index.md` routes to that index**, and `python3 tools/check.py` is green.

**All five: delete both rows** — the one in `../docs/scrape-done.md` and the one in
`../docs/scrape-list.md` it answers — in the same commit as the index work.

**Any of them fails: leave both rows exactly as they are** and say which check failed, in
one line, in the report. Leaving the pair intact is what stops the loop: a queue row with a
receipt beside it is one the crawler already believes it has done, so it will not capture
it again, and nothing re-runs on its own until a person decides what to do. Deleting the
receipt to force a retry produces the same bad capture on a schedule.

## What the two files are not

- **Not a rule.** Neither one routes anything or changes how work is done. An agent that
  reads a queue row and starts fetching pages itself has misread the file: the row exists
  because the capture belongs to a tool that can do it unattended and version the result.
- **Not a record of what this repo has.** That is the per-source index, always. A row is in
  flight by definition — it is written to be deleted.
- **Not a place for anything sensitive.** A start URL behind a login, an internal hostname,
  a customer's subdomain: none of them go in a file the whole repo can read, and a capture
  tool with a token would commit the result next to it. The rule in `learning.md` applies
  here without exception.
