# site

The landing page for `nerdbrain.midhrami.com`. One self-contained `index.html` — no build
step, no dependencies, nothing to install. Fonts come from Google Fonts and degrade to a
system stack if they don't load.

## Deploying

Any static host serves it as-is. Point the host at this directory:

- **Cloudflare Pages** — connect the repo, build command empty, output directory `site`.
- **GitHub Pages** — Settings → Pages → deploy from a branch, folder `/site`, then add
  `nerdbrain.midhrami.com` as the custom domain and a `CNAME` file beside `index.html`.
- **Netlify** — publish directory `site`, no build command.

## Editing

Colors are CSS custom properties on `:root`, with a light-mode override under
`prefers-color-scheme`. Change those and the whole page follows.

Keep the benefit cards ordered by impact on the reader — that order is the page's argument,
not a layout choice.
