# CX-5 — Tower defense simulation

**Agent:** Codex · **Base:** `main` · **Branch:** `agent/cx-5-td-sim` · **Effort:** high

## Context
Ties CX-1..4 into one deterministic fixed-tick game. This is what scenes read and what C-1 and AG-1 build on.

## Contract
`TdSim` (`class_name TdSim extends RefCounted`)

| Member | Returns | Notes |
|---|---|---|
| `place_tower(kind: String, cell: Vector2i)` | `bool` | needs `TdMap.can_build`, a known kind and enough gold; spends the cost |
| `sell_tower(cell: Vector2i)` | `bool` | refunds `Economy.sell_value` |
| `start_next_wave()` | `bool` | false while a wave is running or after wave 5 |
| `step()` | `void` | one tick: spawn, move along the path, `Combat.step`, reward dead enemies, leak enemies that reach the exit, check win/lose |
| `state()` | `String` | `"idle"`, `"running"`, `"won"`, `"lost"` |
| `snapshot()` | `Dictionary` | below |

`snapshot()` keys (AG-1 copies this table; do not rename or add keys):

| Key | Type | Example |
|---|---|---|
| `enemies` | `Array[Dictionary]` | `{"id": 3, "kind": "grunt", "pos": Vector2(2.5, 0.5), "hp": 10, "max_hp": 12}` |
| `towers` | `Array[Dictionary]` | `{"kind": "arrow", "cell": Vector2i(4, 2)}` |
| `path` | `Array[Vector2i]` | `TdMap.waypoints()` |
| `size` | `Vector2i` | `Vector2i(12, 7)` |
| `gold` | `int` | 100 |
| `lives` | `int` | 20 |
| `wave` | `int` | 0 before the first wave, then 1..5 |
| `state` | `String` | `"idle"` |

Contract test: `tests/test_td_snapshot_contract.gd` (write it first) asserts every key and type above.

## Do
- Tests first (`tests/test_td_sim.gd`): placing/selling and gold; an unattended wave 1 leaks lives; a fixed defence of arrows clears wave 1 with no lives lost; wave 5 cleared means `won`; lives 0 means `lost`; two runs with the same inputs give equal snapshots at tick 500.
- No `randi()`, no wall-clock time, no scene nodes.

## Owns
- `scripts/core/TdSim.gd`
- `tests/test_td_sim.gd`
- `tests/test_td_snapshot_contract.gd`
- `docs/agents/reports/CX-5.md`

## Done when
Contract and sim tests pass; lint and tests green.

## Out of scope
Scenes, input, drawing. If a balance number makes the game unwinnable or trivial, say so under **Needs**; do not retune the kinds yourself.
