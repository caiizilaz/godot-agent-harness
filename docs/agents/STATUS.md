<!-- The integrator (Claude) updates this file alone. Agents grep only their row and its Depends on:
     grep -E '\[(CX-1|AG-1)\]' docs/agents/STATUS.md docs/agents/STATUS_ARCHIVE.md
     One short line per task (what + what is left). Merged = move the row to STATUS_ARCHIVE.md in the same PR
     (tests/test_status_board.gd checks). -->
# Agent board

`ready` can start · `blocked` waits on Depends on · `doing` · `review` waiting for the integrator or the user · `merged`

### Codex

| ID | Task | Depends on | Status |
|---|---|---|---|
| [CX-1](tasks/CX-1.md) | TD map: grid, path, can_build, position_at (+ suite) | — | ready |
| [CX-2](tasks/CX-2.md) | Enemy kinds and 5 waves as pure data (+ suite) | — | ready |
| [CX-3](tasks/CX-3.md) | Tower kinds and combat step: targeting, cooldown, splash (+ suite) | — | ready |
| [CX-4](tasks/CX-4.md) | Economy: gold, lives, sell value (+ suite) | — | ready |
| [CX-5](tasks/CX-5.md) | TdSim: fixed-tick game tying CX-1..4, snapshot contract | CX-1, CX-2, CX-3, CX-4 | blocked |

### Antigravity

| ID | Task | Depends on | Status |
|---|---|---|---|
| [AG-1](tasks/AG-1.md) | BoardView + HUD drawn from a snapshot, preview scene | — | ready |

### Claude Code

| ID | Task | Depends on | Status |
|---|---|---|---|
| C-1 | Main scene: TdSim loop, tower placement input, BoardView hookup | CX-5, AG-1 | blocked |
