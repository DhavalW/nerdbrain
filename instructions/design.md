# Visual Design

Load when: anything visual. Theming, layout, "make it look good", brand.

Goal: work that looks like a designer made specific decisions for this specific product.
Not a template with the colors changed.

## Start from a position

Before any CSS, decide and state in one line: **what should this feel like, and to whom?**

"Precise and dense, for people who live in it all day." "Warm and quiet, for people doing
this once a month." "Loud and confident, because we're the challenger."

Everything downstream — type, spacing, color, motion — serves that sentence. A design with
no position defaults to the generic house style, which is the thing to avoid.

If a theme template was chosen at the checkpoint (`themes/`, see `core.md`), its position
*is* the position: design within its systems, and record any deviation where the choice
was recorded rather than drifting silently.

## Have one idea

The memorable interfaces have a single organizing idea, executed consistently:
one striking typeface, an unusual layout structure, a distinctive color relationship,
a consistent motion signature, an editorial grid, real texture.

Pick one. Commit to it everywhere. Keep the rest quiet so it can carry.
Three competing ideas read as noise, and no ideas read as a template.

## Systems, not decisions

- **Type scale:** one ratio, ~5 sizes, applied without exception. Two families maximum,
  and one is usually better. Choose faces with an actual point of view over the current
  default geometric sans.
- **Space scale:** one base unit, multiples only. Most amateur-looking layouts are
  inconsistent spacing, not bad taste.
- **Color:** one strong accent, a neutral ramp, plus semantic states. Neutrals should be
  tinted toward the accent rather than pure gray — that alone lifts a design out of default.
- **Radius, shadow, border:** pick a coherent set. Sharp and flat, or soft and layered.
  Not both.
- **Motion:** one duration scale, one easing curve, one philosophy. Motion should explain
  what changed, not decorate.

## Rules

- **Contrast over uniformity.** Real hierarchy needs real size and weight jumps.
  16/18/20/24 is mush. 14/16/24/48 has structure.
- **Whitespace is structural.** Uneven spacing is the tell of no system. Related things
  close, unrelated things far, and the gap sizes are from the scale.
- **Alignment is not optional.** Everything lines up to something. A visible grid, even
  an unusual one, beats an invisible one.
- **Constrain measure.** 60–75 characters for body text. Full-width paragraphs are unread
  paragraphs.
- **Dark mode is a design, not an inversion.** Pure black and pure white both hurt. Shadows
  don't work the same. Adjust saturation.
- **Details carry it:** focus rings that match the system, selection colors, custom
  scrollbars where appropriate, considered empty states, real favicons, correct `::marker`.
- **Test dense and sparse.** A design that only works with perfect content is broken.
  Check long names, missing images, one item, two hundred items.

## What to avoid

The current defaults that make work look machine-made — see `anti-ai-tells.md` for the
full list. The short version: purple-to-blue gradient on a dark hero, generic geometric
sans at uniform sizes, glassmorphic cards in a three-up grid, emoji as iconography, rounded
corners on everything at the same radius, centered everything, a floating gradient blob.

Not because these are ugly, but because they're the *default*, and default is the opposite
of the goal.

## Reference well

Look at what's actually good and steal the *structure*, not the surface: how the space is
divided, where the contrast lands, what got left out. Copying a look produces pastiche;
copying a decision-making pattern produces original work.

## Checklist

- [ ] Can you state the design's position in one sentence?
- [ ] Is there one organizing idea, and is it applied consistently?
- [ ] Are type and space genuinely on a scale?
- [ ] Do the neutrals have a temperature?
- [ ] Does the hierarchy work in a squint test?
- [ ] Does it survive real content, both sparse and dense?
- [ ] Dark mode designed, not inverted?
- [ ] Would this be identifiable without the logo?
