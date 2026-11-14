# CX-1 — Tower defense map

**Agent:** Codex · **Base:** `main` · **Branch:** `agent/cx-1-td-map` · **Effort:** low

## Context
Game is a simple tower defense (D2 in `docs/decisions.md`). The map is the grid and the enemy path; every other rule asks it where things are.

## Contract
`TdMap` (`class_name TdMap extends RefCounted`, static functions, no state)

| Function | Returns | Notes |
|---|---|---|
| `TdMap.SIZE` | `Vector2i(12, 7)` | const, cells |
| `TdMap.waypoints()` | `Array[Vector2i]` | the one fixed path, corner to corner, first = entry, last = exit; consecutive points share a row or column |
| `TdMap.is_path(cell: Vector2i)` | `bool` | true for every cell the path covers |
| `TdMap.can_build(cell: Vector2i, occupied: Array[Vector2i])` | `bool` | in bounds, not path, not in `occupied` |
| `TdMap.length()` | `float` | path length in cells |
| `TdMap.position_at(distance: float)` | `Vector2` | cell-centre coordinates (cell (0,0) centre = (0.5, 0.5)); clamps to entry and exit |

## Do
- Tests first (`tests/test_td_map.gd`): bounds, path continuity, `can_build` on path/off-grid/occupied, `position_at` at 0, mid-corner, length and past the end.
- The path must be long enough to have at least 3 turns.

## Owns
- `scripts/core/TdMap.gd`
- `tests/test_td_map.gd`
- `docs/agents/reports/CX-1.md`

## Done when
Every contract row is tested; `tools/lint.sh && tools/test.sh` green.

## Out of scope
Enemies, towers, waves, scenes.
