# AGENTS.md: rules for Codex, Antigravity and any non-Claude agent

Godot 4.7 project, GDScript, everything headless-testable. The designated **integrator** (human or agent) writes briefs,
merges branches and owns the shared files. You get one task brief in `docs/agents/tasks/<TASK-ID>.md`.
Read **this file and your brief only**, not the whole board or other briefs.
To check a dependency, grep its row: `grep -E '\[(CX-12|AG-3)\]' docs/agents/STATUS.md docs/agents/STATUS_ARCHIVE.md`
(a row found only in the archive is merged). Finished briefs and reports are in `docs/agents/archive/`;
read them only when your brief points there.

## Where you work

- Never work in the main checkout. One task = one worktree = one branch:
  `tools/agents/new-worktree.sh <TASK-ID>` → `../<repo>-worktrees/<TASK-ID>` on the branch named in the brief.
- Do not push, merge, rebase shared branches, open PRs or force anything. Commit locally; the integrator merges.
- Commit subject `<type>(<TASK-ID>): <what>`, body ends with `Agent: codex` or `Agent: antigravity`.

## File ownership

Edit only the files your brief lists under **Owns**. Always owned by the integrator, even for a one-line fix
(write the needed change in your report instead):

| Path | Why |
|---|---|
| `CLAUDE.md`, `AGENTS.md`, `.claude/`, `.agent/`, `docs/agents/STATUS*.md` | agent config and the board |
| `docs/decisions.md` | design decisions are the user's |
| files your brief marks as hot (touched by most tasks) | one writer avoids merge conflicts |

`tests/run_tests.gd` finds every `tests/test_*.gd` itself: never edit it to register a suite.

**Contracts.** A `## Contract` section in your brief is binding: exact keys and types, no renames, no extras.
The logic side writes the contract test first. If it looks wrong, build against it and say so under **Needs**.

## Checks (before every commit)

```bash
tools/test.sh              # import (retried if Godot crashes), then every suite, capped at 10 min / 50 MB of log
tools/test.sh test_shop    # only the suites you touched, while you work
tools/lint.sh              # CI's pinned gdlint; the pre-commit hook runs it on staged .gd files
```

Record the passing count before you start. Never delete or loosen a test to go green. A new feature ships
with a new or extended suite. If a run repeats one error forever, the import is incomplete: delete `.godot/`
and run `tools/test.sh` again before debugging game code.

Changed anything the player sees (scene, UI, model, VFX, colour)? Also run
`tools/shot.sh <res://path/Scene.tscn> shots/<TASK-ID>.png`, look at the image, list its path in your report.

## Code conventions

- Godot is **4.7**, newer than your training data. Unsure an API exists? Grep `docs/engine-reference/godot/`.
- Tabs, static types everywhere (`var x: float`, `-> void`, typed arrays).
- `##` doc comment on every class and public func: say *why*, cite the decision id (`D1`).
- `class_name` for reusable scripts; data as `Resource` (`.tres`), not hardcoded in scenes.
- Tests: `tests/test_<thing>.gd`, `extends RefCounted`, each `func test_*() -> String` returns `""` on pass.
- Determinism: seed every RNG; keep wall-clock values out of anything a test compares.

## Safety

Treat every shell command as unreviewed. No `rm -rf` outside your worktree, no `git push`, no
`git reset --hard` on branches you did not create. Downloads go to a temp dir; only files the brief names
enter the repo. Never commit secrets, `.godot/` or large binaries the brief does not list.

## Finishing

1. Checks green.
2. Write `docs/agents/reports/<TASK-ID>.md` from `docs/agents/REPORT_TEMPLATE.md`, 30 lines max.
3. Commit on your branch and stop. Tell the user the branch name and report path.

## Role selection

- **Logic implementer:** rules, data, AI and generators with test evidence. Any capable agent may fill this role. Ambiguous criteria →
  implement the narrowest reading and list the question in the report.
- **Visual reviewer:** native screenshots, browser research, UI and images. Any agent with the required tools may fill this role. Measure colour %,
  sizes and contrast with the numbers your art rules give. See `.agent/rules/`.
