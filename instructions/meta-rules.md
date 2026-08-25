# Meta-rules

Load when: writing, editing, promoting or retiring a rule in this repo. Not for using the
packs — only for changing them.

The packs govern the work. This governs the packs. `../CLAUDE.md` holds the parts every
session needs; this holds the parts only a rule-change needs, which is why it isn't loaded
by default.

## A rule is not finished until it states four things

Every rule promoted into a pack carries these, in the rule or in the section around it:

- **Fires when** — the situation, not the topic. "A collection where every record has one
  owner" beats naming one vendor's rule syntax. A rule whose trigger is a topic gets loaded
  and then
  ignored, because nothing in the work ever matches it.
- **Enforced by** — one of `gate`, `review question`, or `advisory`, said out loud. A rule
  with no enforcement is a wish, and wishes are why long instruction files stop being
  followed. **A convention worth keeping becomes a check, not a paragraph** — an unchecked
  standard drifts and nobody notices until it has, so if it can live in `../tools/check.py`
  it belongs there (obs-0003).
- **Rests on** — carried forward from the ledger entry that produced it.
- **Conflicts with** — the pack and line it contradicts, or "none found" after looking. With
  sixty-odd files, a contradiction is now likelier than a duplicate, and two packs that
  disagree make both unreliable.

## The falsifiability bar

**A rule has to be breakable.** If no piece of work could be shown to violate it, it is a
value, not a rule, and it costs context on every load without changing an outcome.

- "Write good code" — not a rule. Nothing fails it.
- "Every async call has a timeout" — a rule. A file either has them or doesn't.
- "Be careful with migrations" — not a rule.
- "A migration ships with its down migration in the same commit" — a rule.

Values are still worth having. They belong in the prose that frames a pack, not in its
bullets, and they are never what a gate checks.

## Provenance survives promotion

A rule promoted from the ledger keeps its entry id, appended in brackets: `(obs-0003)`.
Multiple entries, multiple ids (obs-0021).

This is what makes the rule reviewable later. Without it, a line proved once in 2026 and a
line the user has restated ten times read identically, and neither can be retired on
evidence. The id resolves to the entry's **Rests on** field, which is where the evidence
actually lives — so the pack line stays short.

Rules that predate this convention don't get backfilled by guesswork. Tag one when you can
identify its entry, leave it alone when you can't.

## Rules get retired, not just added

Every instruction system that fails, fails this way: it only ever grows, compliance drops as
it grows, and nobody can tell which rules are still load-bearing. Adding is not the
dangerous operation — accumulating is.

So retirement is a normal move, not an admission of error:

- **A rule that never fires is dead weight.** If no task in months has matched its trigger,
  propose removing it. Its `(obs-NNNN)` id and the archived entry keep the reasoning.
- **A rule the work keeps overriding is wrong**, not disobeyed. Two overrides is a
  correction to write down (`learning.md`).
- **A rule superseded by a gate is redundant.** Once `../tools/check.py` enforces something,
  the paragraph explaining it can shrink to a line naming the check.
- **Retiring is a promotion in reverse** and needs the same explicit yes, per item. Removed
  rules leave a ledger entry saying what was removed and why, so the same rule isn't
  re-proposed in six months as if it were new.

## Splitting, not trimming

The rule itself is in `profile.md` and `../CLAUDE.md`: a pack over budget gets split at an
honest seam, and rules already approved don't get cut to make room for new ones. Raising a
recorded budget is allowed, shows in the diff, and belongs in the commit message.

Nothing new here — it is listed because "the pack is full" is the most common reason someone
reaches for the wrong fix.

## Where approval happens

Nothing here becomes a rule without an explicit yes, per item. The channels are in
`learning.md` and there are two: the weekly promotion PR, where merging is the yes, and the
nerdbrain approvals block in conversation, where naming an item's id is the yes.

An agent may write to the ledger freely and may never edit a pack from it. That gap is the
whole design, not an inconvenience to route around.

## Style is not separate from this

A rule written badly is followed badly. The base writing method in `profile.md` governs pack
prose exactly as it governs a reply: plain, direct, short sentences, no flair. A pack that
would not survive `anti-ai-tells.md` isn't finished, and a rule that needs re-reading to
parse will be skimmed instead.
