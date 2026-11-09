# CX-4 — Economy and lives

**Agent:** Codex · **Base:** `main` · **Branch:** `agent/cx-4-td-economy` · **Effort:** low

## Context
Gold and lives as a small value object the simulation owns. Replaces nothing yet; `Score` stays until C-1.

## Contract
`Economy` (`class_name Economy extends RefCounted`)

| Member | Type | Notes |
|---|---|---|
| `gold` | `int` | starts 100 |
| `lives` | `int` | starts 20 |
| `can_afford(cost: int)` | `bool` | |
| `spend(cost: int)` | `bool` | false and no change when short |
| `earn(amount: int)` | `void` | negative amount is ignored |
| `sell_value(cost: int)` | `int` | 70% of cost, rounded down |
| `leak(amount: int)` | `void` | lives never below 0 |
| `is_dead()` | `bool` | lives == 0 |

## Do
- Tests first (`tests/test_td_economy.gd`): start values, spend success and failure, negative earn, sell_value for 50 and 100, lives floor at 0, `is_dead`.

## Owns
- `scripts/core/Economy.gd`
- `tests/test_td_economy.gd`
- `docs/agents/reports/CX-4.md`

## Done when
Every contract row is tested; lint and tests green.

## Out of scope
Costs of towers, rewards of enemies (they live in CX-2/CX-3), scenes.
