# CX-OVERHAUL — SPACE8 LABS harness overhaul

**Agent:** Codex · **Base:** `main` · **Branch:** `codex/space8-harness-overhaul`

## Context
The owner explicitly authorized implementing the entire agreed overhaul plan on 2026-11-14.
This umbrella brief materializes that authorization without modifying other task briefs or the board.
The main checkout remains unchanged. No push, shared-branch merge or deployment.

## Owns
- `tools/harness/**`, `tools/harness.py`, `tools/tests/**`, `tools/docs/**`
- `tools/test.sh`, `tools/shot.sh`, `tools/agents/new-worktree.sh`
- `tests/test_engine_version.gd`, `.github/workflows/tests.yml`
- `harness.json`, `examples/typescript/**`, `benchmarks/**`
- `docs/overhaul/**`, `docs/architecture/**`, `docs/workflows/**`, `docs/quickstart/**`
- `docs/migration/**`, `docs/troubleshooting/**`, `docs/case-studies/**`, `docs/release-readiness.md`
- `docs/agents/tasks/CX-OVERHAUL.md`, `docs/agents/reports/CX-OVERHAUL.md`
- `README.md`, `AGENTS.md`, `CLAUDE.md` (role portability updates explicitly included in owner-approved overhaul)
- `website-patch/**` (reviewable changes for the separate non-Git SPACE8 LABS project)

## Contract
`docs/architecture/adapter-contract.md` specifies schema v1. Tests precede implementation.

## Done when
Regression cases cannot report false success; generic and Godot adapters work;
worktrees validate identity; examples/docs cover TH/EN/zh-Hans; local website changes
and evidence are delivered; unavailable measurements are explicitly marked, never fabricated.

## Baseline
2026-11-14: existing Godot suite 6/6; pinned gdlint passed in isolated worktree.
