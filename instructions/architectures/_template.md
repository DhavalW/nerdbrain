# <Architecture name>

Capture format for an architectural style — especially one proven in a shipped app. Copy,
fill in, add an inventory line in `../index.md`. Keep it under ~80 lines.

An architecture template says **where code, data, and trust live**. Concrete tools belong
in `../stacks/`; the two compose, so name compatible stacks rather than restating them.

---

## Shape

A Mermaid diagram plus 3–5 lines: what runs where, what talks to what, where the data
lives at rest and in flight.

## Trust boundaries

What the client is allowed to decide, what the server must decide, what is verifiable vs
merely hidden. The security posture in one paragraph.

## Fits when / avoid when

- Fits: <the project shapes this serves well>
- Avoid: <the honest disqualifiers — write these first>

## Cost profile

What scales with users, what stays flat, which free-tier limit bites first.

## Best practices

The rules specific to *this* architecture — additive to the topic packs, never replacing
them. The things you learned shipping it: ordering constraints, failure modes, the
mistake you made once.

## Proven in

Apps where this shipped successfully, with one line on any deviation that mattered.
(This section is why captured templates beat textbook ones.)

## Compatible stacks

Which `../stacks/` templates serve this architecture, and any that clash.
