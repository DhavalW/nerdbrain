# nerdbrain

**An AI coding agent that learns how you work, and keeps what it learns.**

Every session starts from zero. You correct the same things, restate the same preferences,
and watch it make a mistake you already explained last week.

The usual fix is to write it all down in an instructions file. That means guessing, up
front, every preference you have and every mistake the agent might make. Nobody can do
that. So the file is always incomplete, and the gaps are exactly where the corrections keep
happening.

nerdbrain works the other way round. **You don't write the rules. The agent notices them.**
It watches how you work, writes down what it learned, and asks you to approve it. Say yes
once and it follows that rule in every project after that — a month later, in a different
codebase, without you remembering you ever said it.

It is a plain GitHub repository. No service, no account, nothing running in the background.

> **Works with Claude Code today.** It's markdown in a git repo, so in principle any agent
> that can read a repository can use it — but Claude Code is the only one it has been
> tested with so far.

---

## How to use it

**Attach this repo to your session, alongside the project you're working on.** That's the
whole setup. Nothing to type, no command to remember.

- **Claude Code on the web** — add `nerdbrain` as a second repository in the session.
- **Claude Code in the terminal** — clone it anywhere, then `claude --add-dir <path>`, or
  `/add-dir <path>` once you're already in.

The agent reads `CLAUDE.md` at the top of this repo and takes it from there: it loads the
instructions that fit the task, follows them, and records anything worth keeping when the
task is done.

Two other ways in, if attaching the repo doesn't suit you:

```bash
git clone https://github.com/dhavalw/nerdbrain.git ~/.nerdbrain
~/.nerdbrain/install.sh          # installs the /nerdbrain skill globally
```

Then type `/nerdbrain` in any project to pull the instructions in on demand. Or copy
`templates/CLAUDE.md` into a project's root, and that project picks them up every session
with no repo attached at all.

---

## What you get

| The change | What it means day to day |
|---|---|
| **You stop writing instructions** | A correction today becomes a rule next month, in a project that doesn't exist yet. You work; the repo notices. |
| **It fits you more closely over time** | Every approved rule narrows the gap between what you'd have done and what the agent does. Month six is better than month one. |
| **Fewer questions, asked up front** | Anything the brain already knows arrives pre-filled. What's left gets asked once, before the work starts — not as an interruption four hours in. |
| **Fewer mistakes from stale training data** | Docs your work depends on sit in the repo as indexed snapshots. The agent reads six pages of the real reference instead of recalling an API that changed. |
| **Nothing changes behind your back** | A rule only takes effect after you say yes to it, one item at a time. Silence is never a yes. |
| **It's yours** | Your preferences, your context, your captured docs, in your own repository. Nothing is uploaded anywhere to make this work. |

---

## Everyone's agent learns from everyone's work

This is the second reason it's open source, and the more interesting one.

A private instructions file only ever learns from you. A fork of a public repo can learn
from everybody.

1. **Fork it.** Your fork is yours — your preferences, your projects, your docs.
2. **Your agent learns in your fork,** from your work, at your pace.
3. **The general ones go home.** When a rule isn't about your project, your employer or
   your clients, the agent offers to send it upstream as a pull request. You decide, every
   time. Nothing leaves without your yes.
4. **What's merged comes back to everyone.** Your fork checks the original before each task
   and merges what's new, on its own.

So a hundred people's agents are learning in parallel, and the general lessons pool. Nobody
has to hit the same problem twice for everybody.

Two hard limits on what crosses. Anything identifying — a project, an employer, a client,
an internal service — is stripped before a rule is offered, and if stripping it leaves
nothing then there was nothing general there. And your captured documents and your capture
queue never move between forks in either direction, in any way, at all.

`CONTRIBUTING.md` has the shape of a good contribution. The lowest-friction one is a single
entry in `memory/observations.md`: a rule you noticed, one sentence, with what it rests on.
It needs no argument to land, because an entry there governs nothing until someone approves
it.

---

## How the learning works

```
you work  →  agent notices  →  writes it down  →  you approve  →  it's a rule
                               (no permission)     (one at a time)  (loaded when it fits)
```

Four moving parts.

**A router, not a manifesto.** One long instructions file gets partly ignored — that's the
failure everyone has already had. So the instructions here are split into small packs, and
`instructions/index.md` maps the task in front of the agent to the handful it actually
needs. A security task loads the security pack. A landing page doesn't.

**A ledger that records but doesn't govern.** When a session notices something, it writes a
line in `memory/observations.md` — what it learned, and what makes it think so. Writing
needs no permission, because a line there changes nothing. That's the point: a lesson
survives even when nobody has time to argue about it.

**An approval gate.** A note becomes a rule only when you say so, per item. Two ways to
say it, both of which work while you're away: merge the weekly pull request, or name the
item in chat. An item you ignore stays a note and comes back another day.

**A consistency check.** `tools/check.py` runs on every push and fails the build if the
brain has rotted — a broken reference, an unrouted pack, a file grown past its budget.

`MECHANICS.md` has the long version, with diagrams.

---

## Making it yours

The brain is only as good as what's in it, and what's in it should be yours.

1. **Fork, clone, install.** What ships is the craft layer — how to plan, test, secure,
   write and ship — plus the machinery that learns. Opinionated defaults, and yours to
   strike.
2. **Empty what isn't yours.** `instructions/profile.md` starts nearly blank on purpose,
   and `memory/observations.md` ships with candidate rules from other people's work.
   Clearing it is a supported starting state.
3. **Work as normal.** The repo fills up on its own. When it asks to promote something, say yes
   or ignore it — ignoring costs nothing.
4. **Write a platform pack the second time you look something up.** `platforms/` ships
   empty because your platforms aren't anyone else's;
   `instructions/platforms/_template.md` is the form.
5. **Capture the docs your work depends on.** Drop a PDF into `docs/references/<source>/`
   and push; a workflow drafts its index and opens a pull request.

### Bringing your own docs

Any PDF with selectable text works — an export, a spec, a contract, a regulation. For
documentation that only exists as a website, **[SiteToPDF](https://sitetopdf.com)** is the
companion tool: it turns a docs site into the dated, multi-part PDFs this index is shaped
around. Nothing here requires it — the filename convention is the only contract.

**And it can take the ask from here.** A session that needs docs this repo doesn't have
writes a row into `docs/scrape-list.md`. SiteToPDF, pointed at your fork, reads that queue,
offers each row for a one-click yes, crawls it, commits the PDF, and leaves a receipt in
`docs/scrape-done.md`. The next session checks the capture landed and clears both rows. The
gap closes without anyone remembering it existed.

---

## What's in the repo

```
instructions/    the router (index.md), the always-loaded core.md and profile.md, the
                 topic packs, project-type packs under types/, your own platform packs
                 under platforms/, and the checkpoint menus: architectures/, stacks/,
                 themes/
memory/          the ledger: index.md is the format, observations.md the live entries,
                 archive.md the finished ones
docs/            index.md, wanted.md, the scrape-list.md / scrape-done.md capture queue,
                 plus references/<source>/ for your doc snapshots and each source's own
                 page-map index
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

### The commands, if you installed the skill

| Type this | And it |
|---|---|
| `/nerdbrain` | Works out what you're doing and loads the packs that fit |
| `/nerdbrain <pack>` | Loads one specific pack |
| `/nerdbrain list` | Prints the inventory |
| `/nerdbrain docs <topic>` | Finds the topic's page range and reads it |
| `/update-nerdbrain <rule>` | Turns one line into a placed, styled, checked rule |
| `/refresh-nerdbrain` | Rebuilds derived content after files change |

Cloned somewhere other than `~/.nerdbrain`? Set `NERDBRAIN_HOME` to point at it.

---

## What runs on its own

| Workflow | Fires | Does |
|---|---|---|
| `consistency` | every push and PR | `tools/check.py`. Fails the build |
| `index-captures` | a PDF lands under `docs/references/` | drafts index entries, opens a PR. Deterministic — no model, no credentials |
| `promote-learnings` | Mondays | reads the ledger, drafts the pack edits it has earned, opens one PR |

`promote-learnings` is the only part that costs anything, and it does nothing until you add
either `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN` to the repository's Actions secrets.
Without one it reports that and exits clean. Everything else works regardless, because a
session finishing a task raises the same backlog with you directly.

**Nothing in this repo is ever merged by an agent.** Merging the pull request is the
approval, per commit: drop what you don't want, merge the rest.

---

## Contributing

Yes, please — see `CONTRIBUTING.md`.

Never send anything sensitive or identifying. Git history keeps what a later commit deletes.

## License

MIT. See `LICENSE`.
