# Dense utilitarian

## Position

A precision instrument for people who live in it: maximize signal per screen, minimize
ceremony. For operators, analysts, admins — users who chose this tool and use it daily.

## The one idea

**Density is respect.** More rows, more columns, more state visible at once; hierarchy
comes from weight, alignment, and tabular discipline instead of whitespace.

## Systems

- **Type:** one workhorse sans (system stack is fine) at 13–14px UI baseline; a monospace
  for IDs, numbers, timestamps, code — used *everywhere* numbers align. Scale is flat by
  design: 13/14/16/20; weight (400/550/650) does the differentiating.
- **Space:** 4px base. Row heights 32–36px, compact paddings, but *ruthlessly consistent*
  — density without a grid is clutter.
- **Color:** cool neutral ramp; one functional accent; a full, tested semantic set
  (success/warn/error/info) doing real work, never decorative. Dark mode is first-class —
  this audience lives in it; verify every contrast pair there too.
- **Surfaces:** radius 2–4px; 1px borders and background-tint bands structure tables and
  panels; shadows for overlays only.
- **Motion:** ~100ms fades at most. State changes snap; nothing may move data the eye is
  tracking.

## Feels like / never

- Feels like: a trading terminal, a cockpit, well-made dev tools.
- Never: hero sections, marketing whitespace, oversized headings, skeleton theater on
  fast queries, hiding columns to look "clean." If it's information, show it.

## Fits

Admin panels (`../ux-admin.md` is this theme's behavioral twin), dashboards, internal
tools, data products, power-user B2B. Wrong voice for onboarding-heavy consumer products
or anything used monthly by novices.

## Pairs with

`../architectures/baas-client.md` apps on `../stacks/default-free-tier.md`; keyboard
shortcuts and bulk actions are part of the theme, not extras.
