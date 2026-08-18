# Security

Load when: auth, sessions, payments, uploads, PII, permissions, secrets, or any endpoint
the public can reach.

Scope: the things that actually get exploited in small apps. Not a compliance checklist.

## Secrets

- Client-side code is public. Anything shipped to the browser is disclosed, including
  values in env vars that get inlined at build time. Know which of your env vars are public
  (`PUBLIC_*`, `VITE_*`, `NEXT_PUBLIC_*` — all public by definition).
- A third-party key that must stay private forces a server-side proxy. That's one of the
  few legitimate reasons to run server code (see `stack-and-architecture.md`).
- Never commit `.env`. Check `.gitignore` before the first commit, not after.
- If a secret is ever committed, it is burned. Rotate it. Removing the commit is not enough.
- Never print a secret in logs, errors, or debug output.

## Authorization

The most common real-world hole: the client is asked nicely not to do something.

- Authorize on the server, per request, for every request. UI that hides a button is UX,
  not security.
- Check ownership, not just authentication. "Logged in" is not "allowed to read record 47".
- Deny by default. New collection, new route, new field: locked until deliberately opened.
- Never trust a client-supplied ID, role, price, quantity, or user_id. Re-derive from the
  session.
- Watch for IDOR: sequential IDs plus a missing ownership check is the classic bug.

For PocketBase specifically, this is all API rules — see `platforms/pocketbase.md`.

## Input

- Validate at the boundary: type, range, length, format, allowed values.
- Parameterize queries. Never build SQL or a filter expression by string concatenation
  with user input.
- Escape on output, per context (HTML, attribute, URL, JS). Framework auto-escaping is
  good; `dangerouslySetInnerHTML` / `x-html` / `@html` bypass it. Sanitize before those.
- Cap sizes: request body, upload, array length, string length, pagination limit.
- Uploads: validate real content type not just the extension, cap size, generate your own
  filename, serve from a separate origin or with `Content-Disposition: attachment`.

## When something you ship fetches a URL it was handed

**Scope: code that goes live, reachable by strangers.** Not the fetching you do while
working. A URL the person you are working with asks you to open is a request from a
colleague, not an attack, and nothing below applies to it: read their localhost, their
staging box, their internal hostname, whatever they point you at.

An endpoint that takes a URL and fetches it is a door into everything your server can
reach. Guard every hop, not the first one.

- **Allowlist the scheme** (http, https) and the **port** (80, 443). Otherwise you have
  shipped a port scanner with `file:` support.
- **Refuse private, loopback, link-local, multicast and CGNAT addresses.**
  `169.254.169.254` is the cloud metadata endpoint and the one that hands over credentials.
- **Refuse hostnames with no dot**, and `.local`, `.internal`, `.lan`, `.home`.
- **Follow redirects by hand**, three hops at most, re-checking each one. `redirect:
  'follow'` lets a public URL bounce you somewhere private in a single step.
- **Cap the body while reading it**, not after. Cap the URL count and the timeout too.
- **Identify the fetcher** in the user agent, with a URL that explains what it is.
- **Rate-limit it.** Yours is the IP address the target sees getting hammered.

Two things the checklist won't cover. **DNS rebinding** — the hostname resolves public
when you check it and private when you fetch it — needs resolve-then-connect-by-IP, which
most edge runtimes don't offer; say so in the docs instead of implying it's handled. And
**your own origin**: a worker fetching a hostname routed back to itself never reaches an
origin and times out, so read those through the platform's asset binding instead.

## Sessions and auth

- Long random tokens from a CSRF-safe generator. Never roll your own crypto or your own
  password hashing.
- Cookies: `HttpOnly`, `Secure`, `SameSite`. Tokens in `localStorage` are readable by any
  XSS on the page.
- Rate-limit login, signup, password reset, and anything that sends email or costs money.
- Password reset tokens: single use, short expiry, invalidated on use.
- Don't leak account existence in login or reset responses.
- Log out means the token stops working server-side, not just gets deleted client-side.

## Money and quotas

- Never trust a price, plan, or quantity from the client. Look it up server-side.
- Verify webhook signatures. An unverified webhook endpoint is an open API.
- Make webhook handlers idempotent — they get retried and delivered twice.
- Enforce quotas server-side. A client-side limit is a suggestion.

## Exposure

- CORS: name the origins. `*` on an authenticated endpoint is a hole.
- Errors to the user are generic; details go to the log.
- No stack traces, framework versions, or internal paths in production responses.
- Check what your admin/dashboard routes are exposed on. The default is often "everyone".

## Before shipping

- [ ] `.env` gitignored, no secrets in history
- [ ] Every collection/route has an explicit access rule
- [ ] Ownership checked, not just authentication
- [ ] Rate limits on auth, email, and paid actions
- [ ] Uploads constrained and served safely
- [ ] Webhooks signature-verified and idempotent
- [ ] CORS scoped
- [ ] Dependency audit run
