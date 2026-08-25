# Anti-AI-Tells

Load when: producing anything a human will judge — UI, copy, code, docs, commits.

The problem isn't that AI-generated work is bad. It's that it's *recognizable*: the same
defaults, reached for every time, in the absence of a real decision. Recognizable reads as
low-effort, and low-effort reads as untrustworthy.

The cure is always the same: **make a specific decision for this specific project and
carry it through.**

## In writing

Structural tells:
- Every section the same length, every list exactly three items
- Bold-lead bullets in rigid `**Thing** — explanation` format throughout
- A summary paragraph restating what was just said
- "Let's dive in", "In conclusion", "It's worth noting that"
- Balanced hedging on everything, so nothing is ever asserted
- The "not just X, but Y" construction
- Rhetorical question as a section heading
- Relentless triads: "faster, simpler, and more reliable"

Lexical tells: see the delete list in `copy.md`.

Do instead: vary sentence and section length. Assert things. Let a list be two items or
seven if that's how many there are. Include the specific detail only someone who did the
work would know.

## In UI and visual design

The house style to avoid:
- Purple→blue (or teal→indigo) gradient, dark hero, glow behind the headline
- Generic geometric sans at near-uniform sizes with no real hierarchy
- Three feature cards in a row, each with an icon, a bold heading, two lines of grey text
- Glassmorphism: translucent card, blur, 1px light border, on a blurred blob background
- Emoji standing in for an icon set
- Same border-radius on every element, every corner
- Everything centered, everything the same width, generous uniform padding
- Fake logo strips, "trusted by", invented testimonials
- A stat row of three round numbers with no source
- Floating gradient orbs

None of these are individually wrong. Together they're a fingerprint.

Do instead: pick one organizing idea and commit (see `design.md`). Vary rhythm — sections
should not all be the same height. Let some things be asymmetric. Use a real icon set. Give
neutrals a temperature. Make the type scale actually jump.

## In code

- Comments narrating the obvious: `// loop through the items`
- A docstring on every function including the trivial ones, in identical shape
- Defensive try/catch around things that can't throw
- Abstraction invented for a single use case
- Names like `data`, `result`, `handleData`, `processItem` — or `utils.ts` holding 40
  unrelated things
- Config objects with every option set to its default
- A `README.md` scaffolded with empty sections
- Placeholder content left in: `John Doe`, `example@example.com`, `Lorem ipsum`,
  `TODO: implement`
- Emoji in commit messages, section headers, and console output
- Uniform, exhaustive error handling that treats every failure identically

Do instead: comment the surprising parts only. Name things after the domain. Let simple
functions be simple. Handle the errors that actually happen. Use real-looking sample data.

## The test

Look at the finished thing and ask:

1. Could this be for any other product with a find-and-replace?
2. Is there one detail that shows someone actually thought about *this* problem?
3. Does anything here reflect a decision that a different competent person would have made
   differently?

If 1 is yes and 2 is no, it's generic. Go back and make one real decision.

## Note

This is about defaults, not prohibitions. If a gradient hero is genuinely right for the
brand, use it deliberately and say why. The failure mode is reaching for it *because it's
the default*.
