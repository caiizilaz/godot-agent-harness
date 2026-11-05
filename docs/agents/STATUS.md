<!-- The integrator (Claude) updates this file alone. Agents grep only their row and its Depends on:
     grep -E '\[(CX-1|AG-1)\]' docs/agents/STATUS.md docs/agents/STATUS_ARCHIVE.md
     One short line per task (what + what is left). Merged = move the row to STATUS_ARCHIVE.md in the same PR
     (tests/test_status_board.gd checks). -->
# Agent board

`ready` can start · `blocked` waits on Depends on · `doing` · `review` waiting for the integrator or the user · `merged`

### Codex

| ID | Task | Depends on | Status |
|---|---|---|---|
| [CX-1](tasks/CX-1.md) | Example: replace `Score.combo_multiplier` with your first real rule + suite | — | ready |

### Antigravity

| ID | Task | Depends on | Status |
|---|---|---|---|

### Claude Code

| ID | Task | Depends on | Status |
|---|---|---|---|
