# Changelog

## 0.2.0 (2026-11-05)

- Fixed: the CI workflow read `tools/ci/godot-version.txt` and ran `tools/ci/setup_godot.py`, neither of which was in the template.
  Both are added; `setup_godot.py` checks the SHA-512 of the Godot download.
- Added `tests/test_engine_version.gd`: project settings, CI version file, engine reference and installed editor must agree.
- Board task-id prefixes are one list (`ID_PREFIXES` in `tests/test_status_board.gd`) instead of a regex repeated in two places.
- README: supported platforms, a Thai quick start, how to brief Antigravity and Claude Code, what to do when Actions will not start,
  a case study of the game this came from, and the real problems each piece fixed.
- Added `CONTRIBUTING.md`, this changelog, an issue template, and steps for updating the engine reference.

## 0.1.0 (2026-11-05)

First public version: test runner, lint and pre-commit hook, `tools/shot.sh`, worktree script, board and decision tests,
Godot 4.7 engine reference, agent rule files.
