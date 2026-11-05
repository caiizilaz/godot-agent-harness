# How the agents work together

1. The user decides **what**. The integrator (Claude Code) writes a brief from
   [tasks/_TEMPLATE.md](tasks/_TEMPLATE.md) and adds a row to [STATUS.md](STATUS.md).
2. An agent runs `tools/agents/new-worktree.sh <ID>`, works only in that worktree and only on the brief's **Owns**,
   runs the checks, writes a report from [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md), commits, and stops.
3. The integrator merges `origin/main` into the branch, reads the diff, opens the PR, merges on green CI,
   and moves the row, brief and report to the archive in that PR.

Split work by strength: logic → Codex, visuals → Antigravity, shared/hot files and integration → Claude.
Two agents never own the same file at the same time. When a logic task and a visual task meet at the same
data, the logic brief owns a `## Contract` and the visual brief copies it word for word.
