# Admin & Config UX

Load when: building anything an admin, operator, or installer touches — settings, setup,
dashboards, integrations, back office.

The admin is a user too, usually a stressed one, often not the developer.

## ASK ME (mandatory)

When the app — or any part of it — requires setup or configuration by an admin or
equivalent:

1. **If there's no admin UI, ask whether one is wanted.**
2. **If there is (or will be) an admin UI, ask whether it should include a dedicated
   setup-checklist section** that:
   - checks for the necessary configuration,
   - can be manually refreshed in place (without a full page reload) where possible,
   - and gives friendly, admin-appropriate hints and handholding so the app ends up
     correctly set up.

These questions belong in the upfront decision checkpoint (`core.md`, `planning.md`) —
harvest them during planning, not when you reach the admin screens mid-build.

## The setup checklist, when wanted

Each item shows:

- **State** — done / not done / broken / not applicable. Distinguish "not configured yet"
  from "configured and failing." They need different responses.
- **What it's for** — one line, in the admin's language. Not "SMTP_HOST unset" but
  "Email isn't configured, so password resets won't send."
- **How to fix it** — the actual next step, deep-linked to the exact screen where possible.
  If it's an external dashboard, link to it and name the setting.
- **Live re-check** — a refresh control on the item and on the whole list. Re-run the real
  check, in place, showing a result. Never just re-render cached state.

Rules:

- Checks are **real probes**, not "is the env var non-empty". Send the test email. Make the
  API call. Verify the webhook is reachable.
- Order by dependency, and gate what can't be checked yet ("configure the API key first").
- Show overall readiness at a glance: `4 of 6 complete`, plus what's blocking launch.
- Distinguish **required to function** from **recommended**. Don't show a red badge for
  something optional.
- Persist last-checked time. Stale results should look stale.
- Never leak a secret back into the UI. Show `sk_live_••••4821`, never the full value.

## The config file

Often the only admin surface there is, and it is read by a human with an editor open.

**It carries its full shape, always.** Every field the schema knows is written out in the
committed file, unset values as explicit `null` — never left to a schema default, never
collapsed to a bare `null` block. A knob that exists only in the schema can't be found,
read, or changed without reverse-deriving the file from the code. So adding a defaulted
field is a two-part change, schema and file in the same commit, and it gates cleanly:
parsing a committed config must not add anything to it.

The cost is that a block being present no longer means the feature is on. Ask whatever
resolves the config that question, never the raw file — the reading that silently flips
when a shape is filled in is the one already shipped somewhere.

## Admin UI generally

**Density over whitespace.** Admins scan tables, not hero sections. Show more rows.
Compact by default with an option to expand.

**Never hide destructive consequences.** "Delete this plan" must say what happens to the
340 users on it. Show the number. Make them type the name for the truly irreversible ones.

**Twenty rows is the line.** Any list that can pass twenty items to manage or approve gets
search, filter, sort, and a draw cap that says what it is holding back. If its rows have an
action, it gets selection and bulk actions on top — an admin doing something 200 times one
at a time is a design failure, and so is a queue that quietly renders its first forty rows.
Judge on what the list will hold in a year, not on what the seed data holds today: the
inbox nobody can face was built when it was empty.

Then keep the bulk path honest. Select-all means everything the filter matched, not just
what is drawn; the button states the count and, if it spends money or reaches people, the
amount; anything the backend would refuse comes out of the batch by name, before one
refusal aborts the other forty.

**Everything is filterable, sortable, searchable, and exportable.** CSV export is not a
nice-to-have; it's how admins do the thing you didn't build.

**Show the system's actual state.** Queue depth, last sync, error counts, recent failures,
version. When something goes wrong the admin should be able to see it in your UI rather
than asking you.

**Audit trail.** Who changed what, when, and from what to what. Retrofitting this is
painful, so add it when you add the settings.

**Errors are diagnostic here.** Unlike end-user errors, an admin wants the detail: the
status code, the response body, the failing field, the request ID. Give it to them, in a
collapsed block.

**Config changes need a dry run** where possible: preview what will change before applying.

**Safe defaults.** A fresh install should be in a working, locked-down state, not a broken
or wide-open one.

## Checklist

- [ ] Asked about the admin UI and the setup checklist
- [ ] Config files carry every field the schema knows, unset values as explicit `null`
- [ ] Every required config has a real probe, not a presence check
- [ ] Each check has plain-language purpose, fix instruction, and in-place refresh
- [ ] Required vs recommended distinguished
- [ ] Secrets masked on display
- [ ] Destructive actions state their blast radius with real numbers
- [ ] Every list that can pass 20 rows has search, filter, sort and a stated draw cap
- [ ] Lists with row actions have selection and bulk actions; the button states the count
- [ ] Tables export
- [ ] Errors show diagnostic detail
- [ ] Settings changes are audited
