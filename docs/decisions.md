# Decision log

Design and process decisions with their reasons. Change one by adding a new entry; never delete the old one.

## Index (read this first, then grep `## Dnn`)

| ID | One-line summary |
|---|---|
| D1 | Agents and roles: Claude integrates, Codex does logic + tests, Antigravity does visuals |
| D2 | The game is a simple tower defense: one fixed path, two tower kinds, five waves, deterministic fixed-tick simulation |

Adding a decision = adding a row here too (`tests/test_decisions_index.gd` checks).

## D1 — Agents and roles (template default)

- **Claude Code** integrates: writes briefs, owns shared files, merges every branch, keeps the board true.
- **Codex** gets work that tests can judge: rules, data, AI, generators.
- **Antigravity** gets work that needs eyes: screens, art review, asset research, images.
- Why: each tool works where it is strongest, and only one agent ever writes the shared files.

## D2 — The game: simple tower defense

- **Genre:** single-path tower defense on a 12×7 grid. Enemies walk a fixed path of waypoints; the player spends gold on towers placed on non-path cells. Reach the end = lose a life; 0 lives = lose; clear wave 5 = win.
- **Scope:** 2 tower kinds (`arrow` single target, `cannon` splash), 3 enemy kinds (`grunt`, `runner`, `tank`), 5 waves, one map. No upgrades, no save files, no audio in v1.
- **Simulation:** pure code in `scripts/core/`, fixed tick of 20 per second, no `randi()` or wall-clock time, so every rule is testable headless and runs are reproducible. Scenes only draw a snapshot Dictionary and forward input.
- **Why:** it splits cleanly into logic Codex can prove with tests (path, waves, targeting, economy), visuals Antigravity can judge by eye (board, towers, enemies, HUD), and wiring Claude owns. Small enough to finish, large enough to exercise every part of the harness.
- Chosen by the user on 2026-11-09 ("td แบบง่าย").
