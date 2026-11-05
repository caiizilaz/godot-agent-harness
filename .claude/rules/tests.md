---
paths:
  - "tests/**"
---

# Tests

- One suite per `tests/test_<thing>.gd`, `extends RefCounted`, each `func test_*() -> String` returns `""` on pass.
- Never edit `tests/run_tests.gd` to register a suite; it discovers `tests/test_*.gd`. `tools/lint.sh` rejects a `SUITES` list.
- While working, run only what you touched: `tools/test.sh test_a test_b`.
- Determinism: seed every RNG; strip wall-clock fields (ids, timestamps) before comparing snapshots.
- Time budgets run on slow shared CI runners: give `CI=true` more room and put the measured time in the failure.
- Never delete or loosen a failing test to go green; find out why it fails.
