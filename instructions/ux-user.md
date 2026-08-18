# User-Facing UX

Load when: building any screen an end user sees.

Visual style is `design.md`. Words are `copy.md`. This is behavior.

## Principles

- **The user did not come here to use your app.** They came to get something done. Every
  screen either advances that or is in the way.
- **Show the thing, not the chrome around the thing.** Content first, controls second.
- **The first run decides everything.** Empty state is the most-seen screen in most apps
  and usually the least designed.
- **Reduce decisions.** A default that's right 80% of the time beats a choice.

## Rules

**Every state, every time**
Loading, empty, error, partial, success. Missing states are the single most common gap.
- Loading: skeletons that match final layout, not a centered spinner that shifts everything.
- Empty: say what goes here and give the one button that creates it. Never a bare "No items."
- Error: what happened, whether it's their fault, what to do, and a way to retry.

**Feedback**
- Every action gets a response inside 100ms, even if the work takes longer.
- Optimistic updates where the operation nearly always succeeds — with a real rollback path.
- Never leave the user wondering whether their click registered.
- Long operations: show progress, not a spinner. Say what's happening.

**Forms**
- Validate on blur, not on every keystroke. Never surface an error for a field they haven't
  finished.
- Errors sit next to the field, in plain language, saying how to fix it.
- Preserve input on failure. Losing a filled form is unforgivable.
- Disable submit while submitting. Guard against double-submit server-side too.
- Ask for the minimum. Every field costs you completions.
- Correct format types (`email`, `tel`, `numeric`), autocomplete attributes, real labels.

**Long lists**
- A screen where the user manages more than twenty of their own things — saved items,
  uploads, orders — follows the twenty-row line in `ux-admin.md`: search, filter, sort, a
  cap that says what it is holding back, and selection with bulk actions where the rows
  have actions. Being an end user does not make deleting 200 things one at a time fine.

**Navigation**
- The user always knows where they are, how they got there, and how to get back.
- Back button works. Deep links work. Refresh doesn't lose state.
- Put state that matters in the URL: filters, tabs, search, pagination.

**Destructive actions**
- Undo beats confirm. Confirm only when undo is impossible.
- Confirmation dialogs name the specific thing being deleted.
- Never make the destructive option the default-focused button.

**Mobile**
- Design at 375px first. Desktop is the easy case.
- Touch targets 44px minimum, with spacing between them.
- Nothing important behind hover — hover doesn't exist on touch.
- Watch for the keyboard covering the input and the submit button.

**Accessibility** (non-negotiable, not a phase-two item)
- Keyboard-reachable, in a sensible order, with a visible focus ring. Never `outline: none`
  without a replacement.
- Real semantic elements. A `<div onclick>` is not a button.
- Labels on inputs. Alt text on meaningful images, empty alt on decorative ones.
- 4.5:1 contrast on body text. Check it, don't eyeball it.
- Respect `prefers-reduced-motion`.
- Never encode meaning in color alone.

**Performance is UX**
- Content visible fast beats content complete slowly.
- Reserve space for async content. Layout shift feels broken.
- Above-the-fold works before JS finishes where the stack allows it.

## Checklist

- [ ] All five states designed for every async view
- [ ] Works at 375px
- [ ] Full keyboard path, visible focus
- [ ] Form errors recoverable, input preserved
- [ ] Destructive actions undoable or clearly confirmed
- [ ] Refresh and back button don't break anything
- [ ] Nothing important announced by color alone
