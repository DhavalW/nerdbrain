# Browser Extensions

Load when: building a Chrome / Firefox / Edge extension.

Assume Manifest V3 unless told otherwise. Verify current store policy before submitting —
review rules change and rejections are expensive in wall-clock time (see `../research.md`).

## Architecture

Four contexts, and confusing them is the main source of bugs:

| Context | Can reach | Cannot reach |
|---|---|---|
| Service worker (background) | Extension APIs, network | The DOM, `window` |
| Content script | Page DOM, some extension APIs | Page's JS variables (isolated world) |
| Popup / options / side panel | Extension APIs | Persists — it's destroyed on close |
| Injected page script | Page's JS variables | Extension APIs |

**The service worker is ephemeral.** It gets killed, routinely, whenever the browser feels
like it. Nothing may live in a module-level variable and be expected to survive.

- All state goes in `chrome.storage`. No exceptions.
- Register listeners synchronously at the top level, not inside an async callback — the
  worker restarts by dispatching an event, and a listener registered later won't exist yet.
- Use `chrome.alarms`, never `setTimeout`, for anything past ~30 seconds.
- Long operations need to survive a restart. Make them resumable.

**Popups are destroyed on close.** Any state a user expects to persist goes to storage on
change, not on close.

**Content scripts share the DOM but not the JS context.** To reach page variables you must
inject a script into the page's world, and then you're talking to untrusted code — treat
anything from the page as hostile input (see `../security.md`).

## Permissions

Permissions drive both review friction and install-time drop-off. Every one costs you users.

- Request the minimum that works. Justify each in the store listing.
- Prefer `activeTab` over host permissions. Prefer optional permissions requested in
  context over broad grants at install.
- `<all_urls>` and `tabs` trigger scrutiny. Avoid unless genuinely needed.
- Ask for new permissions at the moment they're needed, explaining why, not on first run.

## Store review

The rejections that actually happen:

- **Remote code execution.** No loading and running remote JS. Everything ships in the
  package. This includes CDN scripts, `eval`, and remotely-fetched templates that execute.
- **Permissions with no visible use.** If it's in the manifest, something in the product
  must obviously need it.
- **Undisclosed data collection.** The privacy disclosure has to match actual behavior.
- **Single-purpose violation.** One extension, one job.
- **Description mismatch.** What the listing says must be what it does.

Assume review latency of days, and that a rejection resets it. Get it right the first time.

## Practical rules

- **Fail invisibly on the page.** Your content script running on someone's banking site
  must never break it. Wrap in try/catch, namespace everything, never assume a selector
  exists, never redefine globals.
- **Sites change.** Any selector-based scraping needs a graceful failure path and ideally a
  remotely-updatable config (data, not code).
- **Storage:** `sync` for small settings, `local` for anything real. `sync` has tight
  per-item and total quotas — check them before designing around it.
- **Message passing** between contexts is async and can fail if the other end is gone.
  Handle the rejection.
- **Test the update path.** Users update from an old version with old stored data. Version
  your storage schema and migrate it.
- **Cross-browser:** Firefox uses `browser.*` with promises, Chrome `chrome.*` with
  callbacks, and manifest fields differ. Use a polyfill or a thin shim from the start —
  retrofitting is worse.

## Security

The extension has more privilege than the page. That makes it a target.

- Never inject page-supplied content as HTML. XSS in an extension is a serious escalation.
- Never trust messages from content scripts without checking the sender.
- Keep the CSP strict. Don't relax it to make a library work — replace the library.
- No API secrets in the bundle. An extension package is trivially unpacked; assume every
  string in it is public.

## Checklist

- [ ] No state in service-worker module scope
- [ ] Listeners registered synchronously at top level
- [ ] Alarms, not timeouts, for anything long
- [ ] Permissions minimal and each one justified
- [ ] No remote code
- [ ] Content script cannot break the host page
- [ ] Storage schema versioned with a migration path
- [ ] Tested as a fresh install and as an upgrade
- [ ] Privacy disclosure matches actual behavior
