# AGENTS.md

Instructions for any coding agent working with this repo. `CLAUDE.md` is the full version,
written for Claude Code and its skills; this is the same protocol for agents that don't read
that file. The packs themselves are plain markdown and assume nothing about which agent
reads them.

This repo turns up in one of two roles.

## Before any task, in either role: sync with the original

`DhavalW/nerdbrain` is the original. If `origin` is anything else, this clone is a fork and
may be missing upstream commits — including corrections to the very packs a reference
session is about to hold work to.

Run `tools/fork-sync.sh check` at session start and at the start of each new task. On
`behind:N`, run `tools/fork-sync.sh sync` and carry on. On `fetch-failed`, say so in a line
and start the task anyway. On `upstream-mismatch`, ask which repo is the original.

On `conflict` or `dirty-overlap`, never resolve it on your own judgement — read
`instructions/fork-sync.md` and follow it: `tools/fork-sync.sh plan` for both sides of every
clash, put the choice to the user file by file in plain language with what each option costs,
wait, then carry out their answer with `tools/fork-sync.sh resolve`.

The sync is one-way and history-preserving: upstream `main` only, merge never rebase, no
force-push, nothing pushed back to the original, and no merging over uncommitted work.

Four paths never move between this clone and any other, in either direction, by any means —
no sync, no merge, no cherry-pick, no pull request: `docs/references/` and everything in it,
`docs/scrape-list.md`, `docs/scrape-done.md`, `docs/wanted.md`. The script enforces that
where it runs; the rule binds you where it doesn't. The queue is why — a capture tool reads
it and opens each URL in the owner's browser.

## As a reference, alongside the repo actually being worked on

The usual case, and the whole instruction is: hold the work to what's in here. Change
nothing in this repo.

1. **Read `instructions/core.md` and `instructions/profile.md` once per session.** Core is
   how the work runs; profile is who it runs for. Both always apply.
2. **Consult the router — `instructions/index.md` — at the start of every task and every
   iteration of one**, not only when the work changes kind. It is already in context, so the
   check is free, and rule 4 means most checks load nothing. What it catches is a sub-task
   running on whatever packs the last one needed.
3. **Load every pack the router matches — all of them.** No count to hit: the minimum that
   covers the work is the target, and a pack dropped to keep the number down takes its rules
   with it. The economy is in not reading what the router didn't match.
4. **Never load the same pack twice.** A pack in context is still in force; re-reading it
   buys nothing but bloat. This is what makes rules 2 and 3 affordable.
5. **Report what belongs to this repo in the nerdbrain block, when there is something to
   report** — a pack loaded, a ledger entry written, an approval waiting. Last thing in the
   reply and nowhere else; the shape is in `instructions/profile.md`. A turn that loaded and
   wrote nothing gets no block. Don't summarize a pack back to the user; it is their repo.

Platform docs work the same way: `docs/index.md` routes to a platform's index, and that index
maps topics to page ranges. Read the index before opening any PDF, and only the platform you
need.

**Precedence**, highest first: what the user said in this conversation, then the target
project's own conventions, then these packs. The rules in `CLAUDE.md` govern *this* repo only
— never impose them on the project being worked on.

## When the work needs docs this repo doesn't have

Write the gap down at the moment you hit it — that session is the only one that knows it
exists. A crawlable start URL goes in `docs/scrape-list.md`, in the four-column shape that
file sets out; anything a person has to fetch by hand goes in `docs/wanted.md`. Neither
needs approval, because neither governs anything.

Rows in `docs/scrape-done.md` are receipts from the capture tool, and clearing them is a
session-start job: check the PDF is on disk under `docs/references/<source>/`, has selectable
text, covers the section that was asked for, is listed and mapped in that folder's own index,
and that `tools/check.py` is green. All five, and both rows go in the same commit. Any of
them failing, both rows stay and the reply says which. `instructions/doc-capture.md` is the
full protocol.

## When the work turns up something worth keeping

A correction, a preference said in passing, an approach that held, a pack that was wrong or
silent. Generalize it past the current project and append it to `memory/observations.md` at
the end of the task — the format is in `memory/index.md`.

Appending needs no approval, because an entry there governs nothing. Turning one into a rule
does need approval, per item, and never happens as a side effect of noticing something.
Secrets are never recorded, in any form, anywhere in this repo.

Anything you actually want decided is asked in the nerdbrain approvals block, in the fixed
layout `instructions/profile.md` sets out. Naming an item's id is the yes; silence is not.

A rule that would hold for anyone can go back to the public repo this one was forked from.
**Offer it and wait** — never open an upstream PR unasked. The version that leaves names no
project, client or internal service, and carries the rule without the evidence that proved
it. `CONTRIBUTING.md` has the shape.

## As the work itself

Changing a pack, the router, a doc snapshot, a skill, or the gate: read `CLAUDE.md` and
follow it. The short version is that this repo is held to its own standards, derived content
is rebuilt in the same commit that made it stale, and `python3 tools/check.py` has to pass
before anything is committed.

Anything foundational — the entry point, the router, the gate, the ledger format, the
approval path, the always-loaded set — is a checkpoint decision every time. Test the premise
against what actually depends on it, give the cost in real units, propose, and stop. The
full rule is under *Changing something foundational* in `CLAUDE.md`.
