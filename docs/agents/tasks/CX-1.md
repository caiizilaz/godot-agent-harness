# CX-1 — first real rule

**Agent:** Codex · **Base:** `main` · **Branch:** `agent/cx-1-first-rule` · **Effort:** low

## Context
The template ships `Score.combo_multiplier` as an example. Replace it with the first rule of your game.

## Do
- Tests first: extend `tests/test_score.gd` with the new rule's cases.

## Owns
- `scripts/core/Score.gd`
- `tests/test_score.gd`
- `docs/agents/reports/CX-1.md`

## Done when
New cases pass, `tools/lint.sh && tools/test.sh` green.

## Out of scope
UI and scenes.
