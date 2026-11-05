---
paths:
  - "docs/agents/**"
  - "docs/decisions.md"
---

# Agent board and decisions

- `docs/agents/STATUS.md` holds open work only, one short line per task. When a task merges, move its row to
  `STATUS_ARCHIVE.md` and its brief/report to `docs/agents/archive/` in the same PR (`test_status_board` checks).
- A new decision `## Dnn` needs a row in the index at the top of `docs/decisions.md` (`test_decisions_index`).
- Decision content is the user's call: never change it without the user's words.
