# Astro content stack

For content-shaped sites: blogs, docs, marketing, portfolios. Ships HTML, not a framework
runtime.

## The pieces

| Layer | Tool | Why this one |
|---|---|---|
| Framework | Astro | Content collections with typed schemas; zero JS by default; islands when needed |
| Content | Markdown/MDX in the repo | Versioned with the code, no CMS to run, agent-editable |
| Hosting | Cloudflare Pages, GitHub-wired | Static output at the edge, previews per branch |
| Interactivity | Astro islands — Alpine or Preact per island | Pay for JS only where a component earns it |
| Dynamic edge | Pages Functions (sparingly) | Forms, redirects with logic — the static-plus-functions jobs |

## Serves architectures

Static-first by construction: `../architectures/static-plus-functions.md` when there's any
dynamic edge, plain static when there isn't. Embedded tools on content pages follow
`../architectures/client-only.md`.

## Wiring

- Content collections defined with schemas; a malformed frontmatter field fails the build,
  not the page (`../types/static-site.md`).
- Build generates sitemap, RSS, OG images, and the search index — runtime generates
  nothing.
- Content edits deploy like code: commit → build → live. A rebuild webhook covers any
  external content source.

## Tradeoffs

- Strong: performance ceiling of the web (it's files), SEO-native, cheapest possible
  serving, content workflows agents handle well.
- Weak: anything session-shaped fights the model; heavy interactivity means many islands,
  and at some point that's an app pretending to be a site.
- Ceiling: when most pages need per-user rendering, you've left content-land — switch
  architecture rather than bolting SSR onto everything.

## Cost

Effectively zero at any realistic traffic; the only metered pieces are build minutes and
whatever Functions you added. First limit to bite: monthly build cap if content churns
hard (`../platforms/cloudflare.md`).

## Best practices

- Zero-JS is the default; each island is a deliberate exception with a named reason.
- Slugs are forever — a changed URL is a permanent redirect, set the same day.
- The full checklist lives in `../types/static-site.md`; this stack is its natural home.
