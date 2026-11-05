# Contributing

This is a harness, not a game: keep everything here free of any one game's names, art and rules.

1. Fix or add one thing per PR. Say what problem it stops, and how you saw the problem happen.
2. Run `tools/lint.sh && tools/test.sh` before pushing; they are what CI runs. Add or extend a suite in `tests/` for
   any behaviour you change (`tests/test_<thing>.gd`, `extends RefCounted`, each `test_*` returns `""` on pass).
3. Never edit `tests/run_tests.gd` to register a suite, and never loosen a test to go green.
4. Keep docs honest: if you could not run something (Windows, a headless Linux display), say "not tested", not "works".
5. Changed a script an agent calls? Update `AGENTS.md` and `CLAUDE.md` in the same PR.

Bug reports: say your OS, `godot --version`, the exact command and its output.
