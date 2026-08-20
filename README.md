# nerdbrain

**A portable, self-evolving brain for AI coding agents.** Attach it to a session and the
agent picks up how you work, what your work already runs on, and the documentation that work
depends on — then gets better at all three every time you use it.

It is a plain GitHub repository. No runtime, no service, no account. Which is the point: it
plugs into Claude Code today and into whatever replaces Claude Code later, and the record of
your preferences stays in a repo you own.

```bash
git clone https://github.com/dhavalw/nerdbrain.git ~/.nerdbrain
~/.nerdbrain/install.sh
```

Then, in any project:

```
/nerdbrain
```

Or attach the repo to a Claude Code session alongside the one you're working in, and nobody
has to type anything at all.

---

## Why

Standing instructions have a shape problem. One long file gets partly ignored, so people
write less of it down, so the agent knows less, so the same corrections get made every week.
Meanwhile the agent's training data has a cutoff, and the API you're integrating shipped a
breaking change after it.

nerdbrain fixes both halves and closes the loop between them.

### What you get

**Your preferences, learned once, applied everywhere.** A correction you make today is a
rule the agent follows next month, in a different project, in a different tool. You don't
write instructions — you work, and the repo notices.

**Fewer questions, better answers.** Everything the brain already knows arrives at the
decision checkpoint pre-filled. The questions get fewer as the profile grows, and that is
measurable.

**Fewer wrong calls from stale training data.** Documentation your work depends on lives in
the repo as indexed snapshots, mapped topic-to-page. The agent reads six pages instead of
guessing at an API from memory.

**Portable by construction.** Any agent that can read a repo can use this one. Switch
harnesses, switch models, switch employers — the brain comes with you, because it's a git
remote and not a vendor's database.

**Private by default.** Your preferences, your context, your captured docs, in your own
repository. Nothing is uploaded anywhere to make this work.

**Less supervision.** The rules that survive are the ones that stop the failures you already
hit. Long autonomous runs go further before they need you, and the ones that do need you ask
everything at once, at the start, instead of stalling four times.

**It compounds across everyone.** A rule that would hold for anyone can go back upstream as
a pull request. Your fork learns from your work; everyone's fork learns from everyone's.

---

## How it works, in one screen

```
you work  →  agent notices  →  ledger entry  →  you approve  →  it's a rule
                (no approval needed)             (per item)      (loaded on the tasks it fits)
```

Four moving parts:

**A router, not a manifesto.** `instructions/index.md` maps the shape of a task to the two
to four packs it actually needs. Everything else stays out of context.
`instructions/core.md` (how the work runs) and `instructions/profile.md` (who it runs for)
are always loaded, and deliberately short.

**A ledger that records without governing.** A session that notices something writes it to
`memory/observations.md` — with what it rests on, and whether it was seen once or stated
outright. Writing needs no permission, because an entry there changes nothing. That
separation is what stops lessons dying with the session that had them.

**An approval gate that is always explicit.** A rule only governs after you say yes, per
item. Two channels, both of which work while you're away: merge the weekly pull request, or
name an item's id in chat. Silence is never a yes, and an unanswered item just comes back
another day.

**A consistency gate.** `tools/check.py` enforces the invariants — references resolve, every
pack is routed, no page numbers in packs, ledger entries parse, always-loaded files stay
inside their line budgets. CI runs it on every push.

`MECHANICS.md` has the full picture, with diagrams.

---

## Setup

`install.sh` symlinks this clone's skills into `~/.claude/skills/`, so `git pull` is all it
takes to update them.

| Invocation | Does |
|---|---|
| `/nerdbrain` | Auto-routes from the current task |
| `/nerdbrain <pack>` | Loads a specific pack |
| `/nerdbrain list` | Prints the inventory |
| `/nerdbrain refresh` | Force-pulls the repo |
| `/nerdbrain docs <topic>` | Looks up the topic's page range and reads it |
| `/update-nerdbrain <rule>` | Turns one line into a placed, styled, gated rule |
| `/refresh-nerdbrain` | Rebuilds derived content after files change |

Cloned somewhere other than `~/.nerdbrain`? Set `NERDBRAIN_HOME` to point at it.

For a project that should pick the packs up every session with no repo attached at all, copy
`templates/CLAUDE.md` into the project root.

### Make it yours

Fork it. The brain is only as good as what's in it, and what's in it should be yours.

1. **Fork, clone, install.** What ships is the craft layer — how to plan, test, secure,
   write and ship — plus the machinery that learns. Opinionated defaults, and yours to
   strike.
2. **Empty what isn't yours.** `instructions/profile.md` starts nearly blank on purpose,
   and `memory/observations.md` ships with candidate rules from other people's work —
   clearing it is a supported starting state.
3. **Work normally.** The repo fills up on its own. When it asks to promote something, say
   yes or ignore it — ignoring costs nothing.
4. **Write a platform pack the second time you look something up.** `platforms/` ships
   empty because your platforms aren't anyone else's, and
   `instructions/platforms/_template.md` is the form.
5. **Capture the docs your work depends on.** Drop a PDF into `docs/references/<source>/`
   and push; a workflow drafts its index and opens a pull request.
6. **Send the general ones home.** `CONTRIBUTING.md` has the shape.

### Bringing your own docs

Any PDF with selectable text works — an export, a spec, a contract, a regulation. For
documentation that only exists as a website, **[SiteToPDF](https://sitetopdf.com)** is the
companion tool: it turns a docs site into the dated, multi-part PDFs this index is shaped
around. Nothing here requires it — the filename convention is the only contract.

---

## What's in the repo

```
instructions/    the router (index.md), the always-loaded core.md and profile.md, the
                 topic packs, project-type packs under types/, your own platform packs
                 under platforms/, and the checkpoint menus: architectures/, stacks/,
                 themes/
memory/          the ledger: index.md is the format, observations.md the live entries,
                 archive.md the finished ones
docs/            index.md, wanted.md, plus references/<source>/ for your doc snapshots and
                 each source's own page-map index
skill/           one directory per skill: /nerdbrain, /update-nerdbrain,
                 /refresh-nerdbrain
templates/       CLAUDE.md drop-in for projects
tools/           index-pdf.py drafts page maps, autoindex.py drafts whole index entries,
                 staleness.py reports what's going out of date, check.py is the gate
site/            the landing page, one self-contained index.html
CLAUDE.md        the entry point: how to use this repo, and how to work on it
AGENTS.md        the same protocol for agents that don't read CLAUDE.md
MECHANICS.md     the five mechanisms and how they fit, with diagrams
CONTRIBUTING.md  what a good contribution looks like, and what won't be merged
```

The full pack inventory lives in `instructions/index.md` — deliberately the only complete
list, so it can't drift out of sync with a copy here.

---

## What runs on its own

| Workflow | Fires | Does |
|---|---|---|
| `consistency` | every push and PR | `tools/check.py`. Fails the build |
| `index-captures` | a PDF lands under `docs/references/` | drafts index entries, opens a PR. Deterministic — no model, no credentials |
| `promote-learnings` | Mondays | reads the ledger, drafts the pack edits it has earned, opens one PR |

`promote-learnings` is the only part that costs anything, and it does nothing until you add
either `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN` to the repository's Actions secrets.
Without one it reports that and exits clean — everything else works regardless, because a
session finishing a task raises the same backlog with you directly.

**Nothing in this repo is ever merged by an agent.** Merging the pull request is the
approval, per commit: drop what you don't want, merge the rest.

---

## Contributing

Yes, please — see `CONTRIBUTING.md`. The lowest-friction contribution is one entry in
`memory/observations.md`: a rule you noticed, one sentence, with what it rests on. It needs
no argument to land, because an entry there governs nothing until someone approves it.

Never send anything sensitive or identifying. Git history keeps what a later commit deletes.

## License

MIT. See `LICENSE`.
