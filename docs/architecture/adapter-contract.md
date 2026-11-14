# Adapter contract v1

Config has exactly `schema_version: 1` and nonempty `checks: array`.
Each check has exactly `id: string` (unique lowercase slug), `adapter: command|godot`,
`argv: nonempty string[]`, `cwd: relative string`, `required: boolean`,
`timeout: positive finite number` (seconds), `log_cap: positive integer` (bytes).
Unknown keys/versions fail before execution. Paths cannot traverse or escape via symlinks.
Config commands are trusted executable code; inspect/doctor do not run them.

Result has exactly these fields:

| Field | Type | Meaning |
|---|---|---|
| schema_version | integer = 1 | consumer compatibility |
| status | passed / failed / skipped | required skipped fails aggregate |
| exit_code | integer or null | null when no process starts |
| reason | string | completed, nonzero_exit, timeout, log_limit, interrupted, engine-specific error |
| duration_seconds | number | monotonic elapsed time, not deterministic game state |
| log | absolute string | bounded local diagnostic file |
| artifacts | string[] | fresh output paths |
| tests | null or {passed: integer, total: integer} | null for unparsed generic commands |

Godot argv begins with import, test or capture. Test arguments are suite names.
Capture arguments: scene (main or res://...), output relative path, wait seconds.
Godot exact stable version must match tools/ci/godot-version.txt.
Process nonzero always fails regardless of success text; SCRIPT ERROR fails Godot checks.
Generic commands use their exit code; test counts remain unknown. Optional failure still fails;
only explicitly skipped optional checks are permitted. POSIX process groups are terminated on exit.
Native Windows is rejected; WSL/Linux CI verification is separate from local macOS evidence.
