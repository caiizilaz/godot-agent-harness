---
trigger: always_on
---

# Antigravity workspace rules

1. `AGENTS.md` at the repo root is the source of truth. Read it at the start of every conversation; this file only adds Antigravity specifics.
2. Never work in the main checkout. Run `/start-task <TASK-ID>`; it creates your worktree. Open that folder as the workspace and write every file under it.
3. Your tasks are the `AG-*` briefs in `docs/agents/tasks/`. Never pick up `CX-*` or integrator work.
4. Auto-exec is on. Before any command that deletes, moves outside the worktree, touches git remotes or installs software, stop and ask the user.
5. Visual reviews are measured, not vibes: report colour coverage %, sizes and contrast against the numbers in your art rules.
6. Finish with `/finish-task`. Do not push or open PRs.
