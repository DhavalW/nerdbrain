# Web Apps

Load when: interactive app, dashboard, SPA, PWA — anything with real client state.

Default shape: a **no-build library** for light interactivity, a **real framework** when
state is genuinely complex, a **managed backend** behind it, a **CDN host** in front. Pick
the specific tools at the checkpoint — see `../stack-and-architecture.md` before
committing.

Also load: `../ux-user.md`, `../engineering.md`, `../security.md`.

## Client-first

Per `../stack-and-architecture.md`: pull the dataset the user is entitled to, then do the
work locally. Filtering, sorting, searching, aggregating, and charting over a few thousand
records is faster in the browser than a round trip, and free.

Server only for secrets, trust, shared writes, CORS-blocked calls, and webhooks.

## State

Four kinds, and conflating them causes most app bugs:

| Kind | Lives in | Example |
|---|---|---|
| Server state | A cache with invalidation | Records from the API |
| URL state | The URL | Filters, tab, page, search, selected item |
| Session state | Memory | Is this modal open |
| Persistent local | localStorage / IndexedDB | Theme, draft, sidebar width |

Rules:
- Anything the user would expect to survive a refresh or be shareable goes in the URL.
- Server state is a cache, not your source of truth. It goes stale. Plan invalidation.
- Don't mirror server state into local state — you'll get two versions of the truth.
- Persist drafts as they're typed. Losing typed input is unforgivable.

## Data

- Every fetch: loading, empty, error, success. All four (see `../ux-user.md`).
- Optimistic updates where success is near-certain, with a real rollback and a visible
  failure message.
- Deduplicate concurrent identical requests.
- Cancel requests when the component that wanted them unmounts.
- Paginate or virtualize anything unbounded.
- Realtime subscriptions beat polling on both freshness and cost, where the backend has
  them.

## Offline and flaky networks

Decide explicitly whether this matters. If it does:

- Cache the shell, queue writes, sync on reconnect, show connection state.
- Conflict policy chosen up front: last-write-wins, merge, or ask. Don't discover it later.

If it doesn't: detect offline and say so clearly instead of silently failing.

## Routing

- Real URLs for real screens. Deep-linkable, refreshable, back-button-correct.
- Lazy-load routes.
- Guard authenticated routes on the client for UX and on the server for security.
- Preserve scroll position on back.

## The forgotten cases

- Two tabs open at once
- Session expiry mid-action — recover, don't dump them at a login screen having lost work
- Very long text, very large numbers, missing avatars, one-item lists, 10,000-item lists
- Timezones. Store UTC, display local, be explicit about which is which.
- A slow network. Test with throttling on, not just on localhost.

## Checklist

- [ ] Client-side compute where it makes sense
- [ ] URL carries the shareable state
- [ ] All four async states, every view
- [ ] Drafts survive a refresh
- [ ] Long lists virtualized
- [ ] Session expiry handled without data loss
- [ ] Works on a throttled connection
- [ ] Auth guarded on both sides
