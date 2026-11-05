---
description: Finish a task — verify, screenshot, report, commit locally (no push)
---

1. Run `/verify`. Do not continue unless it is green.
2. If the task changes anything the player sees, run `tools/shot.sh <scene> shots/<TASK-ID>.png` and look at the image.
3. `git diff --stat origin/main...HEAD`: every touched file must be under the brief's **Owns**. Revert anything else.
4. Write `docs/agents/reports/<TASK-ID>.md` from `docs/agents/REPORT_TEMPLATE.md` (30 lines max).
5. Commit `<type>(<TASK-ID>): <what>`, body ends with `Agent: antigravity`. Do not push, merge or open a PR.
