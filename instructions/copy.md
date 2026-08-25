# Copy & Voice

Load when: writing anything a person reads. Buttons, errors, empty states, emails, landing
pages, onboarding, docs, release notes.

Copy is interface. A confusing label costs more than a slow query.

## Voice

Talk like a competent person explaining something to a colleague. Direct, specific,
unhurried. Not a brand, not a butler, not a hype man.

- Second person. "You" not "the user."
- Active voice. "We couldn't save this" not "This could not be saved."
- Present tense.
- Short sentences beat clever ones.
- Assume intelligence, not knowledge. Explain the domain, not the concept of buttons.

## Rules

**Be specific.** Every vague word can be replaced with a real one.
"Something went wrong" → "Couldn't reach the server. Check your connection and retry."
"Optimize your workflow" → "Cut invoice approval from three days to one."

**Buttons say what happens.** "Send invitations" not "Submit." "Delete 4 files" not "OK."
The user should be able to read only the button and know the outcome.

**Errors do three things:** say what happened, say whose problem it is, say what to do next.
Never blame the user. Never expose a stack trace to an end user (admins are different — see
`ux-admin.md`).

**A code is not a message.** A status code, exit code or exception name handed to a person
has reported nothing. Lead with what it means for them, keep the code underneath as a
footnote, and name the next step. "HTTP 202" is unactionable; "your site showed a 'prove
you are human' screen instead of the page" says what happened, and "ask whoever runs your
hosting to let the AI crawlers through" says what to do. The code still ships, below the
sentence, for whoever they forward it to (`ux-admin.md`).

**Empty states sell the feature.** One line on what lives here and why it's useful, then
the button that creates the first one.

**Front-load.** Most important word first. People scan; they don't read.

**Cut ruthlessly.** Every draft has 30% fat. "In order to" → "to". "Please note that" →
delete. "We're excited to announce" → delete.

**Be consistent.** One name per concept, everywhere, forever. If it's a "workspace" in the
nav it isn't a "project" in the settings.

**Numbers over adjectives.** "Under 200ms" not "blazing fast." "12,000 teams" not
"trusted by many."

## Words to delete

`seamless` `robust` `leverage` `utilize` `empower` `unlock` `elevate` `supercharge`
`game-changing` `cutting-edge` `revolutionary` `effortless` `intuitive` `powerful`
`delve` `tapestry` `realm` `landscape` `journey` `curated` `bespoke` `synergy`
`best-in-class` `next-level` `world-class` `simply` `just` `easily`

Also delete: "It's not just X, it's Y." "In today's fast-paced world." "Whether you're a
X or a Y." "The best part?" Rhetorical questions used as headings.

If a sentence would survive being pasted into any other product's site, it says nothing.

## Formatting

- Sentence case for headings and buttons. Not Title Case, not ALL CAPS.
- No exclamation marks. One per product, saved for something that earns it.
- Emoji only where they carry meaning the reader expects. Not as decoration or bullets.
- Oxford comma. Consistent date and number formats.
- Contractions. "Don't" not "do not."

## Before shipping

- [ ] Read it aloud — anything you wouldn't say out loud gets rewritten
- [ ] Every button describes its outcome
- [ ] Every error says what to do next
- [ ] No word from the delete list
- [ ] Names for concepts are consistent across the whole product
- [ ] Would this read as written by a person with an opinion?
