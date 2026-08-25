# AGENTS.md

Instructions for any coding agent working in this repo. `CLAUDE.md` is the full version;
this is the same protocol in short, for agents that don't read that file.

## Before any task: sync the fork with the original

`DhavalW/nerdbrain` is the original. If `origin` is anything else, this clone is a fork and
may be missing upstream commits — including ones added after the fork was made.

Run `tools/fork-sync.sh check` at session start and at the start of each new task. On
`behind:N`, run `tools/fork-sync.sh sync` and carry on. On `fetch-failed`, say so in a line
and start the task anyway. On `upstream-mismatch`, ask which repo is the original.

On `conflict` or `dirty-overlap`, never resolve it on your own judgement. Run
`tools/fork-sync.sh plan` for both sides of every clash, then put it to the user file by
file in plain language: what each side was trying to do, the two or three ways to reconcile
them that fit, what each one costs, and your recommendation. Wait for an answer. Then carry
it out — `tools/fork-sync.sh resolve FILE=upstream|fork|manual ...`, hand-merge the `manual`
ones to the agreed shape and nothing more, `git add`, then `resolve --continue`. The sync is
done when `check` says `in-sync`, not when the merge commits. `resolve --abort` puts
everything back if the chosen approach turns out to be impossible.

The sync is one-way and history-preserving: upstream `main` only, merge never rebase, no
force-push, no push to the original, and no merging over uncommitted work. `CLAUDE.md` has
the reasoning and the manual fallback.
