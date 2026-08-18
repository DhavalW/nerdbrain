# AGENTS.md

Instructions for any coding agent working with this repo. `CLAUDE.md` is the full version,
written for Claude Code and its skills; this is the same protocol for agents that don't read
that file. The packs themselves are plain markdown and assume nothing about which agent
reads them.

This repo turns up in one of two roles.

## As a reference, alongside the repo actually being worked on

The usual case, and the whole instruction is: hold the work to what's in here. Change
nothing in this repo.

1. **Read `instructions/core.md` and `instructions/profile.md` once per session.** Core is
   how the work runs; profile is who it runs for. Both always apply.
2. **Consult the router — `instructions/index.md` — before starting, and again whenever the
   work turns into a different kind of work.** A new surface, a new concern (auth, payments,
   uploads, user-visible copy), a new platform. A follow-up about code already in context is
   not a turn.
3. **Load the two-to-four packs the router matches.** Six is a lot. Loading everything wastes
   the context this system exists to save.
4. **Never load the same pack twice.** A pack in context is still in force; re-reading it
   buys nothing but bloat.
5. **Report what belongs to this repo in the nerdbrain block**, last thing in the reply and
   nowhere else — packs loaded, ledger entries written, approvals waiting. The shape is in
   `instructions/profile.md`. Don't summarize a pack back to the user; it is their repo.

Platform docs work the same way: `docs/index.md` routes to a platform's index, and that index
maps topics to page ranges. Read the index before opening any PDF, and only the platform you
need.

**Precedence**, highest first: what the user said in this conversation, then the target
project's own conventions, then these packs. The rules in `CLAUDE.md` govern *this* repo only
— never impose them on the project being worked on.

## When the work turns up something worth keeping

A correction, a preference said in passing, an approach that held, a pack that was wrong or
silent. Generalize it past the current project and append it to `memory/observations.md` at
the end of the task — the format is in `memory/index.md`.

Appending needs no approval, because an entry there governs nothing. Turning one into a rule
does need approval, per item, and never happens as a side effect of noticing something.
Secrets are never recorded, in any form, anywhere in this repo.

Anything you actually want decided is asked in the nerdbrain approvals block, in the fixed
layout `instructions/profile.md` sets out. Naming an item's id is the yes; silence is not.

`proposals/` holds parked designs and **governs nothing** — not routed, not draft rules, not
read to decide how to work. Open one only when the user names that work.

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
