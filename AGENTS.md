# AGENTS.md

Instructions for any coding agent working in this repo. `CLAUDE.md` is the full version;
this is the same protocol in short, for agents that don't read that file.

## Before any task: sync the fork with the original

`DhavalW/nerdbrain` is the original. If `origin` is anything else, this clone is a fork and
may be missing upstream commits — including ones added after the fork was made.

Run `tools/fork-sync.sh check` at session start and at the start of each new task. On
`behind:N`, run `tools/fork-sync.sh sync` and carry on. On `conflict`, `dirty-overlap` or
`upstream-mismatch`, stop, lay out the options in the reply, and wait for the user to
choose — never resolve a conflict on your own judgement. On `fetch-failed`, say so in a line
and start the task anyway.

The sync is one-way and history-preserving: upstream `main` only, merge never rebase, no
force-push, no push to the original, and no merging over uncommitted work. `CLAUDE.md` has
the reasoning and the manual fallback.
