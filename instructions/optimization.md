# Optimization

Load when: performance, bundle size, SEO, accessibility, or infra cost is in scope.

## Order of operations

1. Measure. Guessing which thing is slow is usually wrong.
2. Fix the biggest thing.
3. Measure again.
4. Stop when it's fast enough. "Fast enough" is a real state.

Never optimize on a hunch, and never trade readability for a speedup you haven't confirmed.

## Performance

**Loading**
- Ship less JavaScript. It is almost always the problem.
- Static and prerendered by default; hydrate only what's interactive.
- Code-split on routes, and lazy-load anything below the fold or behind an interaction.
- Images: modern format, sized correctly, `width`/`height` set, lazy below the fold, eager
  for the LCP element.
- Self-host fonts, subset them, `font-display: swap`, and preload the one that matters.
- Audit the bundle before adding a dependency. Check what a date library or icon set really
  costs (see `engineering.md`).

**Runtime**
- Virtualize long lists. Anything over a few hundred rows.
- Debounce input handlers, throttle scroll and resize.
- Batch DOM reads and writes; don't interleave them.
- Cache derived values, and cache network responses.
- Web Worker for anything that would block the main thread past a frame.

**Core Web Vitals**
- LCP: usually the hero image or a blocking font. Preload it.
- CLS: reserve space for images, ads, embeds, and async content.
- INP: long tasks on the main thread. Break them up.

## SEO

Only relevant for public content — skip for apps behind a login.

- Server-rendered or static HTML. Content that only exists after JS runs is a risk.
- One `<h1>`, real heading hierarchy, semantic elements.
- Unique `<title>` and meta description per page, written for a human.
- Canonical URLs. Consistent trailing-slash and www policy.
- Open Graph and Twitter card tags with a real image.
- Structured data (JSON-LD) matching the content type. Only for what's actually on the page.
- `sitemap.xml` and `robots.txt`, generated at build.
- Descriptive URL slugs. Internal links with meaningful anchor text.
- Fast, mobile-first, accessible — these are ranking inputs, not separate work.
- Content depth beats keyword density. Answer the question the search was asking.

For keyword and volume data, see `platforms/keywords-everywhere.md`.

## Accessibility

Not an optimization, but it lives on the same audits. Full rules in `ux-user.md`.
Minimum before shipping: keyboard path, visible focus, labels, alt text, 4.5:1 contrast,
semantic landmarks, and a run through an automated checker (which catches maybe a third of
real issues — still worth it).

## Cost

Costs scale with **requests and writes**, rarely with storage. Optimize accordingly.

- Cache at every layer: browser, CDN, edge, application. A cache hit costs nothing.
- Long `max-age` on hashed static assets, `stale-while-revalidate` on HTML.
- Batch writes. Per-write quotas are the tightest limit on most free tiers.
- Move work to build time or to the client (see `stack-and-architecture.md`).
- Don't poll. Use realtime, webhooks, or back off hard.
- Set an alert before the free tier ends, not after the bill arrives.

## Checklist

- [ ] Measured before and after
- [ ] JS bundle justified, no accidental large dependency
- [ ] Images sized, modern format, dimensions set
- [ ] No layout shift on load
- [ ] Meta, canonical, OG, sitemap present on public pages
- [ ] Keyboard and contrast pass
- [ ] Caching headers set deliberately
- [ ] Free-tier headroom known
