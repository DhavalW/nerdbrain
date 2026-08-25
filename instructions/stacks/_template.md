# <Stack name>

Capture format for a tech stack — a concrete, named combination of tools that has shipped
together. Copy, fill in, add an inventory line in `../index.md`. Keep it under ~80 lines.

A stack template names **the tools and how they wire together**. Where code and trust
live is the architecture (`../architectures/`); a stack serves one or more architectures.

---

## The pieces

| Layer | Tool | Why this one |
|---|---|---|
| Frontend | | |
| Backend / data | | |
| Hosting / deploy | | |
| Extras | | |

## Serves architectures

Which `../architectures/` templates this stack implements well; any it fights.

## Wiring

The non-obvious integration points: how deploys flow, where env vars live, what talks to
what and over which protocol. The half-day of setup knowledge, written down.

## Tradeoffs

- Strong: <what this combination is genuinely best at>
- Weak: <what it fights you on — write these honestly>
- Ceiling: <where it stops working and what the exit path is>

## Cost

What's free, what's metered, which limit bites first, verified when (`../research.md`).

## Best practices

Stack-specific rules, additive to the packs: version pins that matter, config that isn't
obvious, the integration bug you only hit once.

## Proven in

Apps shipped on this stack, one line each, with deviations noted.
