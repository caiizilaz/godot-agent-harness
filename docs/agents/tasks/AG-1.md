# AG-1 — Board and HUD visuals

**Agent:** Antigravity · **Base:** `main` · **Branch:** `agent/ag-1-td-board-view` · **Effort:** medium

## Context
Draw the game from a snapshot. You never touch game rules; you get a plain Dictionary and render it. Test with fake snapshots until CX-5 lands.

## Contract
The snapshot table from CX-5, word for word:

| Key | Type | Example |
|---|---|---|
| `enemies` | `Array[Dictionary]` | `{"id": 3, "kind": "grunt", "pos": Vector2(2.5, 0.5), "hp": 10, "max_hp": 12}` |
| `towers` | `Array[Dictionary]` | `{"kind": "arrow", "cell": Vector2i(4, 2)}` |
| `path` | `Array[Vector2i]` | corner to corner waypoints |
| `size` | `Vector2i` | `Vector2i(12, 7)` |
| `gold` | `int` | 100 |
| `lives` | `int` | 20 |
| `wave` | `int` | 0..5 |
| `state` | `String` | `"idle"`, `"running"`, `"won"`, `"lost"` |

Cell size is 96 px; `pos` is in cell units.

## Do
- `BoardView.render(snapshot: Dictionary) -> void` draws grid, path, towers (two kinds, clearly different), enemies (three kinds, with an HP bar) and a HUD (gold, lives, wave, state banner for won/lost). Code-drawn shapes or simple generated images are fine; keep colours in one palette constant.
- `scenes/td/BoardPreview.tscn` shows a hard-coded sample snapshot with every kind visible, for `tools/shot.sh`.
- Run `tools/shot.sh res://scenes/td/BoardPreview.tscn shots/ag-1.png`, look at it, attach it to your report. Check at 1280x720 too (`SHOT_RES=1280x720`).

## Owns
- `scripts/view/BoardView.gd`
- `scenes/td/BoardPreview.tscn` and `scripts/view/BoardPreview.gd`
- `docs/agents/reports/AG-1.md`

## Done when
Screenshot shows all kinds, readable at both sizes, no runtime errors; lint and tests green.

## Out of scope
Input handling, game rules, `Main.tscn`.
