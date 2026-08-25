# Static Sites, Blogs & Landing Pages

Load when: marketing site, blog, docs site, portfolio, landing page.

Default shape: **a content-oriented static generator on a CDN host with git deploys.**
Content in Markdown with a typed schema. Zero JS shipped unless a component genuinely needs
it. Pick the specific tools at the checkpoint (`../stack-and-architecture.md`).

Also load: `../optimization.md` (SEO section), `../copy.md`, `../design.md`.

## Principles

- **Static by default.** Everything that can be built at build time is. Server rendering
  is a fallback, not a starting point.
- **Zero JS is the baseline.** Add interactivity per-island, deliberately. A blog post that
  ships a framework runtime is a design failure.
- **Content is data.** Schema-validated frontmatter, so a broken post fails the build
  instead of the page.

## Structure

- Content collections with a typed schema. Required fields enforced at build.
- Slugs are permanent. Changing one means a redirect, forever.
- Layouts compose: base → page type → page. Don't copy `<head>` around.
- Draft/publish state honored at build, with drafts visible in dev only.
- Generate at build: sitemap, RSS, tag and archive pages, OG images, search index.

## Every page needs

- Unique `<title>` and meta description, written for a human, not stuffed
- Canonical URL
- OG and Twitter tags with a real image (generate per-post at build)
- Correct heading hierarchy, one `<h1>`
- JSON-LD matching the page type (Article, Product, FAQ) where it applies

## Performance

Static sites have no excuse for being slow.

- No layout shift. Set image dimensions.
- Self-host and subset fonts. Preload the one used above the fold.
- Optimize images at build. Modern formats, responsive `srcset`, lazy below the fold.
- Inline critical CSS if the framework doesn't already.
- Target: fast on a mid-range phone on a slow connection, not on your laptop.

## Content

Follow `../copy.md`. Specifically for marketing pages:

- Lead with the specific outcome, not the category. "Cut invoice approval to one day," not
  "Streamline your workflow."
- One clear action per page. Competing CTAs mean neither gets clicked.
- Show the actual product early. A real screenshot beats an illustration.
- No fake social proof. No invented testimonials, no fabricated logo strip, no made-up
  numbers. If there's nothing to show, show the product instead.
- Answer the objection the reader actually has: price, lock-in, migration, "does it work
  with X."

## Things that get forgotten

- 404 page that's designed and useful
- RSS feed, and a link to it
- Redirects when URLs change
- `robots.txt` correct for production — never ship staging's `Disallow: /`
- Favicon set, web manifest, theme color
- Dark mode that respects system preference and remembers an override
- Print stylesheet, for anything anyone would print
- Analytics that respects privacy, if any at all

## Checklist

- [ ] Zero JS on pages that don't need it
- [ ] Content schema enforced at build
- [ ] Meta, canonical, OG, JSON-LD per page
- [ ] Sitemap and RSS generated
- [ ] Images optimized, dimensions set, no CLS
- [ ] 404 designed
- [ ] robots.txt correct for prod
- [ ] Fast on a mid-range phone
