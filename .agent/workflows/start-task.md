---
description: Start a task in its own worktree (usage: /start-task AG-3)
---

1. Read `AGENTS.md` and `docs/agents/tasks/<TASK-ID>.md` only.
2. Grep the task's row and its **Depends on** rows in `docs/agents/STATUS.md` and `docs/agents/STATUS_ARCHIVE.md`. If it is not `ready`, or a dependency is not merged, stop and tell the user.
// turbo
3. Run `tools/agents/new-worktree.sh <TASK-ID>` from the main checkout. It prints the worktree path.
4. Switch the workspace to that path. All further commands run there.
// turbo
5. Baseline: `tools/test.sh` and note the pass count.
6. Restate the brief's **Owns**, **Done when** and **Out of scope** in 3–5 lines, then begin.
