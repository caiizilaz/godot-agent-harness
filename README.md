# Godot Agent Harness

A small, tested setup for building a Godot 4.7 game with several AI coding agents at once:
**Claude Code** integrates, **Codex** writes logic and tests, **Antigravity** handles visuals.
Each agent works in its own git worktree, edits only the files its brief owns, and nothing merges
without the headless test suite passing.

It came out of a real game project where three agents shipped 100+ PRs in a few days. Everything here
fixed a problem that actually happened; nothing is here "in case".

> ภาษาไทย: ชุดตั้งต้นสำหรับทำเกม Godot 4.7 ด้วย AI หลายตัวพร้อมกัน (Claude Code รวมงาน, Codex ทำตรรกะ+เทสต์,
> Antigravity ทำงานภาพ) แต่ละตัวทำงานใน worktree ของตัวเอง แก้เฉพาะไฟล์ที่บรีฟให้ และรวมงานได้เมื่อเทสต์ผ่านเท่านั้น

## What you get

| Piece | What it stops |
|---|---|
| `tools/test.sh` | Godot crashing mid-import and the suite then logging one error for 10+ minutes. Retries the import, checks every imported file exists, caps time and log size. |
| `tests/run_tests.gd` | Agents editing the same "list of suites" lines. Finds `tests/test_*.gd` itself, counts SCRIPT ERRORs as failures, shards for CI (`TEST_SHARD=2/4`). |
| `tools/lint.sh` + `.githooks/pre-commit` | Lint passing locally and failing in CI. Pinned gdlint in a cached venv, run on staged files. |
| `tools/shot.sh` | "Tests are green" on a screen nobody looked at. Runs a scene in a real window, saves a PNG, fails on runtime errors or a blank frame. |
| `docs/engine-reference/godot/` | Agents writing Godot 4.3 APIs. Breaking changes and renamed APIs for 4.4 → 4.7. |
| `docs/agents/STATUS.md` + `tests/test_status_board.gd` | A task board that lies. CI fails if a merged task stays on the board, a task is blocked on finished work, or a brief link is dead. |
| `docs/decisions.md` + `tests/test_decisions_index.gd` | Agents reading 40 KB of decisions. One-line index at the top; CI keeps it complete. |
| `tools/agents/new-worktree.sh` | Two agents in one checkout. One task = one worktree = one branch, imported and ready to test. |
| `tools/ci/flaky.sh` | Re-running red CI until it passes. Lists tests that failed across recent runs. |
| `CLAUDE.md`, `AGENTS.md`, `.claude/rules/`, `.agent/` | Each agent getting the rules it needs: Claude Code (integrator, path-scoped rules), Codex (`AGENTS.md`), Antigravity (`.agent/rules` + `/start-task`, `/finish-task`). |

## Start

Needs Godot 4.7 on `PATH` as `godot` (or set `GODOT=/path/to/godot`), Python 3, and `gh` for the CI helper.

```bash
gh repo create my-game --template caiizilaz/godot-agent-harness --private --clone
cd my-game
git config core.hooksPath .githooks
tools/lint.sh && tools/test.sh        # 5/5 passed on a fresh clone
tools/shot.sh main shots/main.png     # opens a window, saves the frame
```

Then:

1. Replace `scripts/core/Score.gd`, `scripts/Main.gd` and `scenes/Main.tscn` with your game; keep rules in pure code so tests can run them.
2. Set your Godot version in `.github/workflows/tests.yml` (`GODOT_VERSION`) and `docs/engine-reference/godot/VERSION.md`.
3. Write your own decisions into `docs/decisions.md` (keep the index row for each).
4. Hand out work: write a brief from `docs/agents/tasks/_TEMPLATE.md`, add a row to `STATUS.md`, and tell the agent:
   `Read AGENTS.md and docs/agents/tasks/CX-1.md, then do the task.`

The example task `CX-1` is ready to try with Codex.

## How a task flows

```
user decides ─▶ Claude writes brief + STATUS row ─▶ agent: new-worktree.sh → work → tests → report → commit
      ▲                                                                                        │
      └──── Claude: merge origin/main into branch, read diff, PR, merge on green, archive ◀──────┘
```

Details in [docs/agents/README.md](docs/agents/README.md). Rules per agent: [CLAUDE.md](CLAUDE.md), [AGENTS.md](AGENTS.md).

## Using only one agent

Everything still works with Claude Code alone: skip the briefs and the board, keep `tools/`, `tests/`,
`docs/engine-reference/` and the checks in `CLAUDE.md`.

## Compared with bigger frameworks

Frameworks such as [Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) model a whole
studio (49 agents, 74 skills). This harness is the opposite bet: few files, enforced by tests rather than prose,
and built for different AI tools working side by side. The Godot engine reference here comes from that project (MIT).

## License

MIT. `docs/engine-reference/godot` is MIT from Claude-Code-Game-Studios; see its licence file.
