# Contributing

nerdbrain gets better the way it says everything gets better: someone notices something,
writes it down with what it rests on, and someone else decides whether it becomes a rule.
Contributions are that loop, run across forks instead of across sessions.

## The shapes a contribution takes

| You have | It goes | Approval |
|---|---|---|
| A rule that held on real work | A pack under `instructions/`, or a new one | Maintainer merge |
| A pattern proven in a shipped app | `instructions/architectures/`, `stacks/` or `themes/`, via that folder's capture template | Maintainer merge |
| Knowledge of a platform nothing covers | `instructions/platforms/<name>.md`, from `instructions/platforms/_template.md` | Maintainer merge |
| A candidate rule with thin evidence | One entry in `memory/observations.md` | None needed — it governs nothing |
| A gap in the docs mechanism | `docs/wanted.md`, or an issue | None needed |

Ledger entries are the low-friction path and the one to reach for when unsure. An entry
changes no behavior, so it needs no argument — it just stops the observation dying with the
session that had it.

## Before you open a pull request

```bash
python3 tools/check.py
```

Green, every time. CI runs the same gate and fails the build. If a check looks wrong, say so
in the PR — don't edit the checker to get past it. Loosening a gate to land a change is the
one thing that will get a PR closed without discussion.

`python3 tools/staleness.py` reports what is quietly going out of date. It never fails a
build; read it before touching anything under `docs/`.

## What a good rule looks like

`instructions/meta-rules.md` is the bar, and it applies to contributions exactly as it
applies to the maintainers. The short version:

- **One sentence, imperative.** The rule as it would be written, not the story that produced
  it.
- **Name the failure mode it prevents.** A rule without its reason gets followed into the
  case it was never meant for.
- **Generalized past the project that produced it.** Would this still make sense in an
  unrelated codebase two years from now? If it only parses with your repo open beside it,
  it's a project doc.
- **Say what it rests on** — stated outright, seen once, or seen N times. A first sighting
  labelled honestly is welcome. A first sighting dressed up as settled fact is not.
- **House style.** `instructions/copy.md` and `instructions/anti-ai-tells.md` govern the
  packs themselves. Sentence-case headings, wrapped at ~95 columns, under ~100 lines a pack.
  A pack that wouldn't survive its own review isn't done.

## What will not be merged

- **Anything sensitive.** Keys, tokens, connection strings, private hostnames, customer or
  employer data, anything under an NDA. Git history keeps what a later commit deletes, so
  this is checked before merge and there is no "clean it up after".
- **Anything identifying.** Your client's name, your internal service names, your unreleased
  product. Strip them or the rule isn't general enough yet.
- **Copied vendor values.** Prices, limits and free-tier ceilings go in a `## Volatile
  claims` section as a pointer to the live source with a verify-by month. A copied number is
  a stale number with a delay on it.
- **Page numbers or dated filenames in a pack.** Those live in the per-source doc index and
  resolve at read time. The gate rejects them.
- **Vendor documentation itself.** Don't send captures upstream — they're large, they're
  someone else's copyright, and they go stale. Send the pack that *reads* one.

## One rule per commit

The promotion machinery, and the humans reviewing, both work per item: a reviewer drops the
commits they don't want and merges the rest. A PR carrying five rules in one commit is all
or nothing, which usually means nothing.

## If a pack is at its line budget

Split it at the seam between two load triggers, moving whole sections verbatim, and route
each half. Don't trim an existing rule to make room for yours — that trades a rule someone
already approved for one nobody has yet. If there's no honest seam, say so in the PR and
propose raising the budget in `tools/check.py`, with the reason in the commit message.

## Contributing from inside a session

If an agent working with your fork produced the rule, it should offer it rather than send
it — the ask-first rule is in `CLAUDE.md` under *Sharing a learning upstream*. Review what
leaves. The generalized sentence is usually safe; the evidence behind it usually isn't.
