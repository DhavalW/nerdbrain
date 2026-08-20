# Stack & Architecture

Load when: starting a project, picking tools, or any question shaped like "should this be
client or server", "will this scale", "what will this cost".

## Concrete choices live in the template menus

Architectures (where code, data, and trust live) are templates in `architectures/`;
stacks (the tools that fill the shape) in `stacks/`; visual positions in `themes/`. They
are chosen per project at the decision checkpoint, per `core.md` — relevant options
presented with tradeoffs, and custom always available. A menu with nothing in it yet means
propose from first principles and capture what shipped.

This pack carries what stays true across all of them: the client-first bias, the
free-tier discipline, and how to present the decision.

## Client-first architecture

**Default: computation and data live in the browser.** Server-side work costs money and
adds failure modes. Push work to the client whenever it makes sense.

Do on the client:

- Filtering, sorting, searching, pagination over a dataset the user already has
- Aggregation, charting, stats, derived values
- Parsing, formatting, validation, diffing, image resizing, PDF generation
- Caching in IndexedDB / localStorage / Cache API
- Anything that could be recomputed instead of stored

Do at build time (free, cached at the edge, zero runtime cost):

- Content rendering, feed generation, sitemaps, search indexes
- Anything derived from data that only changes when you deploy

Only put on a server what genuinely cannot run elsewhere:

- **Secrets.** An API key in client code is a published API key. No exceptions, no obfuscation.
- **Trust.** Anything the user must not be able to forge: payment verification, license
  validation, quota enforcement, permission checks.
- **Shared writes.** State multiple users read and write.
- **Third-party calls blocked by CORS** or that require a server-side redirect.
- **Webhooks.** Someone else's server has to reach yours.

If you're putting something server-side, be able to say which of those five it is.
If it isn't one of them, move it to the client.

### Then put only that part there

Server-side is a decision about *where*, not about *how much*. Ship the piece that had to
be there and leave the judgement on the client: the proxy fetches and returns, the upload
handler stores and hands back a key, the webhook receiver verifies and enqueues. Rules
that live in a module the client imports stay testable without a runtime and change
without a deploy.

Trust is the exception, and it swallows the rule whole. When the reason for the server is
that the user must not be able to forge the answer — quota, licence, payment, permission —
the decision *is* the thing being protected, and a client-side copy of it is a suggestion.

Neither half is a law. It's the question to ask straight after "does this need a server at
all", and the answer belongs in the decision log.

## Free-tier discipline

Assume budget is zero until told otherwise.

- Design so the free tier is the *steady state*, not a trial you grow out of in a week.
- Know the limit that will bite first. Usually it's writes, or bandwidth, or build minutes,
  and it is rarely storage.
- Prefer static + client compute over per-request server compute. Static requests are
  effectively free; compute is metered.
- Cache aggressively. A cache hit is a request you don't pay for.
- Batch writes. Per-write limits are usually the tightest thing on a free plan.
- When a design would blow a free tier, say so **before** building it, with the number.
- **Card-on-file is its own axis, separate from the bill.** Some free tiers still want card
  details to enable — a cost in itself (`profile.md`); flag it in the options rather than
  quietly picking the card-free tool and never naming the other.

**Verify current limits before relying on them.** Free tiers change, and stale numbers in
an architecture doc are worse than none. Check the vendor's pricing page at decision time
(see `research.md`). Rough shape as of writing, to know what to look up:

- **Static hosting:** requests usually unmetered, builds usually capped per month
- **Edge functions:** a daily request cap and a CPU-time-per-invocation cap
- **Key-value stores:** reads generous, **writes are the tight one**
- **Object storage:** watch egress pricing, and whether it wants a card on file
- **Serverless SQL:** a storage cap and a daily rows-read cap
- **Managed app instances:** one free instance, sleeps when idle, capped disk
- GitHub Actions: monthly minutes, free for public repos

## Presenting a stack decision

Never propose one option. Give 2–3 real combinations and a recommendation:

```
Option A — <name>
  Stack:      <what>
  Cost:       free to ~<N> users, then <what breaks and what it costs>
  Complexity: <build effort, maintenance burden>
  Ceiling:    <where it stops working>
  Lock-in:    <how hard to leave>
  Best when:  <condition>

Option B — ...
Option C — ...

Recommendation: <one>, because <the deciding factor for this specific project>.
```

Then **stop and wait for a choice.** Do not start building the recommended one.

Present this inside the single upfront decision checkpoint, written into the reply
(`planning.md`), and hold there until the user has had time to decide — not as a mid-task
interruption, and not as a prompt that expires into a default.

Make the options genuinely different. Three flavors of the same architecture is not a
choice. Vary the thing that actually matters: client-only vs backend, static vs dynamic,
managed vs self-hosted.

## Data model rules

- Model the domain, not the screens. Screens change.
- Denormalize deliberately, not accidentally, and write down why.
- Every collection needs access rules from day one, not "later" (see `security.md`).
- Design migrations to be reversible.
- Don't store what you can derive, unless deriving is provably slow.
