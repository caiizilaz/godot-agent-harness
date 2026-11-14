# CX-3 — Towers and combat

**Agent:** Codex · **Base:** `main` · **Branch:** `agent/cx-3-td-combat` · **Effort:** medium

## Context
Tower targeting and damage as a pure step over plain data, so it needs no scene and no map.

## Contract
`TowerKinds` and `Combat` (static, no state)

| Function | Returns | Notes |
|---|---|---|
| `TowerKinds.stats(kind: String)` | `Dictionary` | keys `cost:int`, `range:float` (cells), `damage:int`, `cooldown:int` (ticks), `splash:float` (cells, 0 = single target). `arrow`: cost 50, range 2.5, damage 5, cooldown 10, splash 0. `cannon`: cost 100, range 2.0, damage 12, cooldown 30, splash 1.0. Unknown kind returns `{}` |
| `Combat.step(towers: Array[Dictionary], enemies: Array[Dictionary])` | `Array[Dictionary]` | mutates `enemies[i].hp` and `towers[i].cooldown`; returns events `{"tower": int, "enemy": int, "damage": int}` in tower order |

Input shapes: tower = `{"kind": String, "pos": Vector2, "cooldown": int}`; enemy = `{"id": int, "pos": Vector2, "hp": int, "progress": float}` (`progress` = distance walked along the path).

## Do
- Tests first (`tests/test_td_combat.gd`): out of range does nothing; in range hits; cooldown blocks the next shot and counts down one per step; target is the enemy with the highest `progress` in range (tie: lowest `id`); splash hits every enemy within `splash` of the target; dead enemies (hp <= 0) are never targeted; same input gives same events.
- Do not remove dead enemies; the simulation does that.

## Owns
- `scripts/core/TowerKinds.gd`
- `scripts/core/Combat.gd`
- `tests/test_td_combat.gd`
- `docs/agents/reports/CX-3.md`

## Done when
Every contract row is tested; lint and tests green.

## Out of scope
Gold, lives, placement, waves, scenes.
