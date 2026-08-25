# Wanted

Docs this repo doesn't have and a session needed, **and that no crawler can fetch on its
own**: a PDF someone has to obtain, a spec behind a login, a page range an existing map
never covered. Anything with a crawlable start URL goes on `scrape-list.md` instead, where
a capture tool will pick it up unattended. The two files are disjoint, and which one a gap
lands in is decided by whether a URL alone is enough to close it.

The point is to stop losing the moment of discovery. An agent that falls back to live docs
because nothing local covered the question knows something worth writing down — and it is
the only one who knows it, right then. By the next session that knowledge is gone and the
gap gets rediscovered from scratch.

## How to add

Any session, no approval needed — this file routes nothing and governs nothing.

```
- <url> — what was needed, and what the fallback cost. — first wanted YYYY-MM-DD
```

- **One entry per gap, not per session.** Hit an existing gap again? Add the date to that
  entry rather than a new line; a gap wanted four times is the one to capture first.
- **Name the URL, not the topic.** "Cloudflare Workers docs" is a search; a URL is a
  capture — and a URL a crawler can start from belongs on `scrape-list.md`, not here.
- **A page range that an index doesn't cover counts.** So does a topic the capture has but
  the map never mentions — that one is an index fix, not a capture, so say which it is.
- **Remove the entry when the capture lands**, in the same change that indexes it.

## Wanted

_Empty. The first entry arrives the first time a session falls through to live docs._

## Captured but unpacked

Not a docs gap — a snapshot with no instruction pack in front of it, so nothing routes a
reader to it and the maps sit unused. Start one from
`../instructions/platforms/_template.md`.

_Empty._
