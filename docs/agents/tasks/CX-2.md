# CX-2 — Enemy kinds and waves

**Agent:** Codex · **Base:** `main` · **Branch:** `agent/cx-2-td-waves` · **Effort:** low

## Context
Data for what spawns and when. Pure functions so a wave can be asserted tick by tick.

## Contract
`EnemyKinds` and `Waves` (static, no state)

| Function | Returns | Notes |
|---|---|---|
| `EnemyKinds.stats(kind: String)` | `Dictionary` | keys `hp:int`, `speed:float` (cells/s), `reward:int` (gold), `leak:int` (lives lost at exit). Kinds: `grunt`, `runner`, `tank`. Unknown kind returns `{}` |
| `Waves.COUNT` | `int` | 5 |
| `Waves.spawns(wave: int, tick: int)` | `Array[String]` | kinds that appear on exactly this tick of wave `wave` (1-based, tick 0 = wave start; tick rate is 20 per second) |
| `Waves.total_enemies(wave: int)` | `int` | must equal the sum of `spawns` over all ticks |
| `Waves.last_spawn_tick(wave: int)` | `int` | after this tick nothing more spawns |

## Do
- Tests first (`tests/test_td_waves.gd`): each kind has all four keys with positive values; wave sizes grow; `total_enemies` equals the summed `spawns` for all 5 waves; out-of-range wave returns empty; wave 5 contains a `tank`.
- No randomness: same input, same output.

## Owns
- `scripts/core/EnemyKinds.gd`
- `scripts/core/Waves.gd`
- `tests/test_td_waves.gd`
- `docs/agents/reports/CX-2.md`

## Done when
Every contract row is tested; lint and tests green.

## Out of scope
Movement along the path, damage, gold, scenes.
