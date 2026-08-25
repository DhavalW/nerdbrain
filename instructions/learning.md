# Learning

Load when: a task is wrapping up and these packs came along as a reference, or the work
just produced a correction, a preference said in passing, or a pattern worth keeping.

Every pack here got written because someone noticed something once. This is the part that
keeps noticing. A lesson is cheapest to capture at the moment it happens and gone by the
next session, so the end of a task is a capture point, not just a report.

The bar is **would this be useful if it holds**, not *has it happened enough times yet*.
Repetition is evidence, not a threshold: a thing seen once gets recorded too, said plainly
as a first sighting. The user's yes is the filter, and there isn't another one.

**Recording and approving are separate** (obs-0001). Every observation goes into the ledger
(`../memory/index.md`), which needs no permission because an entry there governs nothing.
Only promotion into a pack changes behavior, and that still needs an explicit yes. This is
what stops a lesson dying with the session that saw it: the yes can come later, or never,
and the observation survives either way.

## What counts

Worth proposing:

- A correction. The user changed what you did or rejected the approach. What they changed
  it *to* is the rule.
- A preference said in passing — "I never want X", "always do Y here" — including one aimed
  at a single file that clearly isn't about that file.
- A checkpoint decision the same shape of project will face again: an architecture, a
  stack, where the trust boundary sits, build or buy.
- A pattern that survived contact: the auth flow that held, the deploy that stopped
  breaking, the schema that never needed reshaping.
- A first sighting — a failure mode, an approach that worked, a constraint that bit, seen
  exactly once. Waiting for a second occurrence mostly means losing it: the session that
  saw the first one won't be around for the second. Propose it, say it's once.
- A gap. A pack said nothing where the task needed guidance, or said something the work
  proved wrong. Both are edits, and the wrong line is the more urgent one.
- How the user reasons — what they weighed, what they threw out first, what they refused to
  trade. Harder to catch than a rule and worth more, because it applies where no rule
  exists yet.

Not worth proposing:

- A fact about this app: collection names, routes, its copy. That belongs in the project's
  own docs.
- Something a pack already says. Say it was covered, move on.
- A one-off forced by a constraint that won't recur — the deadline, the borrowed account,
  the vendor outage that day.
- Filler. A proposal offered because the section expects one: a generic best practice, a
  restatement of what the task did, advice no one needed. Nothing worth keeping is a fine
  result — say so in a line and stop.

## Generalize before proposing

A learning has to outlive the project that produced it. Strip the app, keep the shape.

- Name the situation it fires in, not the app it fired in: "a collection where every record
  has one owner" beats "the invoices collection".
- Keep the reason. A rule without its failure mode gets followed into the case it was never
  meant for.
- Point at the family, not the instance — the class of service, the shape of the flow.
- The test: would this line still make sense in an unrelated project two years from now? If
  it only parses with this repo open beside it, it's a project doc.

Some learnings won't generalize at all, and forcing them produces a vague line nobody can
act on. Say it's project-specific and let it go.

## Record at the end, never mid-task

The task finishes first. A capture prompt is not a reason to halt a run (`core.md`).

- One batch when the work is done, after the report, kept short.
- Each proposal is one sentence in the imperative, the pack it would live in, and what in
  this task triggered it.
- **Say what it rests on** — seen once here, seen several times, or stated outright by the
  user. A first sighting dressed up as settled fact is what makes these hard to trust;
  labelled honestly it's a question with its evidence attached, which is decidable.
- Strongest first. If the run turned up more than a handful, propose those and name the
  rest in a line — a long list gets skimmed, and that's how the good one gets lost.
- Where placement or wording is a real fork, offer the options rather than picking for the
  user.
- Silence is not approval, and neither is a dismissed prompt. Unanswered means unwritten —
  and now also means still on the books, as an `open` entry that keeps collecting evidence.
- **Write the entry whether or not you raise it in chat.** Raising it is for the strong
  ones; recording it is for all of them. An observation you judged too thin to mention is
  exactly the one that becomes a case on its third sighting.
- Seen it before? Don't add a second entry. Bump the count on the existing one and add the
  date, so the ledger says "three times" instead of saying one thing three ways.

## Also clear the backlog, in the same breath

Recording alone would just grow a pile nobody reads. So the end of a task is also when
entries that have gone unpicked-up get put to the user — including ones from sessions
months ago that this task had nothing to do with.

`python3 tools/staleness.py` names them: `open` entries at the promotion bar — stated
outright, or seen twice or more — that have sat ten days without anyone acting. Ten days
means the weekly run either isn't configured or passed them over, and a repo with no
credential set is the normal case, not the exception. That is the whole point: **the loop
closes with or without the automation.**

- **At most three, strongest first**, alongside whatever this task itself produced. A long
  list at the end of a report gets skimmed.
- **Raise them in the nerdbrain approvals block**, in the standard shape (`profile.md`), never
  as loose prose in the middle of a report. Same layout every time is what lets the user
  find it, read it and answer it in seconds instead of parsing a paragraph.
- **Set `Last raised` to today on each one you raise**, answered or not. Without it the same
  three come back tomorrow, and being nagged by your own instructions repo is how people
  stop reading it.
- **A yes goes through `/update-nerdbrain`** and the entry becomes
  `shipped`. A no is written straight to the entry as `declined` — a refusal is worth
  recording precisely because it stops the question being asked a third time.
- **Nothing at all is a fine outcome.** No ripe entries means say nothing; don't manufacture
  a proposal to fill the section.

## Nothing is written without an explicit yes

- Per item. A yes to one proposal is not a yes to the batch.
- **Merging the promotion PR is the yes**, and closing it is the no (obs-0002). Per item
  means per commit: drop the ones you don't want, merge the rest, and only what was merged
  is a rule. It is the channel that works when nobody is at the keyboard.
- **In conversation, the yes is the user naming the item's id.** Anything else is silence:
  not the reply that talks about something else, not a thumbs-up on the report as a whole.
  Ask in the approvals block, in writing, and let the turn end — the batch keeps.
- Whatever the channel, promotion is where the rule gets its trigger, its enforcement and
  its provenance id — `meta-rules.md` has the bar it has to clear.
- Approved in conversation goes through `/update-nerdbrain`, which
  handles placement, house style, the router and inventory rebuild, the gate, and the
  commit — and flips the ledger entry to `shipped` in the same change.
- Declined is recorded, not forgotten: the entry stays at `declined` so nothing re-proposes
  it. If the same thing happens again, a fresh entry says it is the second time.
- This gate covers the nerdbrain repo only. The project you're working in has its own
  instructions; approval here is not permission there, and never the reverse.

## Never record a secret

The repo is readable by anyone who has it, and git history keeps what a later commit
deletes. A captured learning is the likeliest way a secret gets in, because it arrives
attached to the real thing that proved the rule.

- Out, always: keys, tokens, passwords, connection strings, private hostnames and internal
  endpoints, customer or user data, anything under an NDA.
- Redact by shape, not by value. The rule is "verify the webhook signature before trusting
  the payload" — never the signing secret that demonstrated it.
- The same applies to the proposal itself. Don't paste the secret into chat to ask whether
  it can be recorded.
- If a learning genuinely can't be written without the sensitive part, offer the ways
  around it: a placeholder with the real value in the project's own ignored env file, a
  pointer to where the value lives, or the rule stated one level up where the specific
  doesn't matter.
- If none of those work, say plainly that recording it is a leak risk, name what would be
  exposed and to whom, and let the user decide. Never decide it for them, and never record
  it "for now".
