# Godot Agent Harness

A small, tested setup for building a Godot 4.7 game with several AI coding agents at once:
**Claude Code** integrates, **Codex** writes logic and tests, **Antigravity** handles visuals.
Each agent works in its own git worktree, edits only the files its brief owns, and nothing merges
without the headless test suite passing.

It came out of a real game, [KLAP CHAT: Reroll Protocol](#built-for-a-real-game-klap-chat-reroll-protocol), where three
agents merged 133 PRs in four days. Everything here fixed a problem that actually happened; nothing is here "in case".

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

**Needs:** Godot 4.7 on `PATH` as `godot` (or `GODOT=/path/to/godot`), Python 3.11+, `bash` and `perl`; the `gh` CLI
only for `tools/ci/flaky.sh` and the template command below.

| Platform | Status |
|---|---|
| macOS | Used daily by the project this came from; every command below was run here. |
| Linux | CI runs the headless suite on `ubuntu-latest` and is green on GitHub (lint and tests; not the screenshot step, which needs a display). `tools/shot.sh` needs a display; on a headless machine try `xvfb-run -a tools/shot.sh ...` (not tested here). |
| Windows | Not supported natively (bash scripts). Use WSL. |

```bash
gh repo create my-game --template caiizilaz/godot-agent-harness --private --clone
cd my-game
git config core.hooksPath .githooks
tools/lint.sh && tools/test.sh        # 9/9 passed on a fresh clone
tools/shot.sh main shots/main.png     # opens a window, saves the frame
```

Then:

1. Replace `scripts/core/Score.gd`, `scripts/Main.gd` and `scenes/Main.tscn` with your game; keep rules in pure code so tests can run them.
2. Pick your Godot version once, in `tools/ci/godot-version.txt` (exact, e.g. `4.7.2`). CI installs exactly that, with the
   download's SHA-512 checked. `tests/test_engine_version.gd` fails until `project.godot`, `docs/engine-reference/godot/VERSION.md`
   and the installed editor agree.
3. Write your own decisions into `docs/decisions.md` (keep the index row for each).
4. Hand out work: write a brief from `docs/agents/tasks/_TEMPLATE.md`, add a row to `STATUS.md`, then tell the agent:
   - **Codex:** `Read AGENTS.md and docs/agents/tasks/CX-1.md, then do the task.`
   - **Antigravity:** open the repo as the workspace and run `/start-task AG-1` (workflows are in `.agent/workflows/`).
   - **Claude Code:** it reads `CLAUDE.md` by itself; ask it to merge the agent's branch when the report arrives.

The example task `CX-1` is ready to try with Codex.

### Board prefixes

`tests/test_status_board.gd` only recognises task ids that start with `AG-`, `CX-` or `C-`. A row with any other prefix
(say `GM-4`) is **ignored, not flagged**. To use your own, edit the one list `ID_PREFIXES` at the top of that file and
use the same prefixes in `STATUS.md` and the brief file names.

### If GitHub Actions does not start

A job that dies in two seconds with "recent account payments have failed" is a billing problem, not your code.
Run `tools/lint.sh && tools/test.sh` on the branch merged with `origin/main`, say so in the PR, and merge on that.
(`CLAUDE.md` makes this the integrator's rule.)

### ภาษาไทย: เริ่มใช้งาน

- **ต้องมี:** Godot 4.7 (คำสั่ง `godot`), Python 3.11+, bash, perl · macOS ใช้ได้เต็มที่ · Linux: CI รันเทสต์แบบ headless ผ่านบน GitHub แล้ว (ส่วน `tools/shot.sh` ต้องมีหน้าจอ) · Windows ใช้ผ่าน WSL
- **สร้างโปรเจกต์:** `gh repo create my-game --template caiizilaz/godot-agent-harness --private --clone` แล้วรัน `git config core.hooksPath .githooks`
- **เช็กว่าพร้อม:** `tools/lint.sh && tools/test.sh` ควรได้ 6/6 · `tools/shot.sh main shots/main.png` เปิดหน้าต่างเกมแล้วเซฟภาพ
- **สั่ง agent:** เขียนบรีฟจาก `docs/agents/tasks/_TEMPLATE.md` และเพิ่มแถวใน `STATUS.md`
  - Codex: `Read AGENTS.md and docs/agents/tasks/CX-1.md, then do the task.`
  - Antigravity: เปิด repo เป็น workspace แล้วพิมพ์ `/start-task AG-1`
  - Claude Code: อ่าน `CLAUDE.md` เอง สั่งให้รวม branch เมื่อ agent ส่งรายงาน
- **รหัสงานที่เทสต์บอร์ดรู้จัก:** `AG-`, `CX-`, `C-` เท่านั้น ถ้าใช้ prefix อื่นต้องแก้ `ID_PREFIXES` ในไฟล์ `tests/test_status_board.gd` ไม่งั้นแถวนั้นจะถูกข้ามเงียบๆ
- **ถ้า GitHub Actions ไม่เริ่มทำงานและขึ้นเรื่องการจ่ายเงิน:** ไม่ใช่บั๊กของโค้ด ให้รัน lint กับเทสต์ในเครื่องแทน แล้วระบุใน PR

## How a task flows

```
user decides ─▶ Claude writes brief + STATUS row ─▶ agent: new-worktree.sh → work → tests → report → commit
      ▲                                                                                        │
      └──── Claude: merge origin/main into branch, read diff, PR, merge on green, archive ◀──────┘
```

Details in [docs/agents/README.md](docs/agents/README.md). Rules per agent: [CLAUDE.md](CLAUDE.md), [AGENTS.md](AGENTS.md).

## Built for a real game: KLAP CHAT: Reroll Protocol

This harness was extracted from the project that made it necessary: **KLAP CHAT: Reroll Protocol**, a Thai-mythology
turn-based strategy roguelite growing into a 3v3 MOBA, made in Godot with Claude Code, Codex and Antigravity working
in parallel. The game is in development and its source repository is private; its public pages (in Thai first):

- Website: <https://klapchat.pages.dev/>
- Facebook: <https://www.facebook.com/KlapChatGame/>

What that project looked like when this was written (counted from its git history, 5 Nov 2026):

| | |
|---|---|
| Merged PRs | 133, between 1 and 5 November 2026 |
| Commits | about 715; about 105 carry `Agent: codex`, about 104 `Agent: antigravity`, the rest are Claude Code's |
| Tests | 801 headless tests in 166 suites, all passing locally when the last PR merged |

What went wrong along the way, and the piece that now stops it:

| What happened | Fix in this repo |
|---|---|
| Godot crashed mid-import and the suite then printed one error for 10+ minutes | `tools/test.sh` |
| Parallel branches kept conflicting on the hand-written list of test suites | `tests/run_tests.gd` finds suites itself |
| The task board said tasks were `ready` after they merged, and `blocked` on work that was finished | `tests/test_status_board.gd` |
| One test compared two runs that started a second apart; another had a 90 s budget that slow CI runners missed | the determinism and CI-time rules in `.claude/rules/tests.md`, and `tools/ci/flaky.sh` |
| GitHub Actions stopped on a billing problem while PRs kept merging | the local-verification rule in `CLAUDE.md` |
| A screen passed every test and nobody had looked at it | `tools/shot.sh` |
| The CI workflow pointed at a version file that had not been copied into the template | `tests/test_engine_version.gd` now checks CI only names files that exist |

The last row happened while writing this README: the new test failed on the template itself.

## Using only one agent

Everything still works with Claude Code alone: skip the briefs and the board, keep `tools/`, `tests/`,
`docs/engine-reference/` and the checks in `CLAUDE.md`.

## Compared with bigger frameworks

Frameworks such as [Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) model a whole
studio (49 agents, 74 skills). This harness is the opposite bet: few files, enforced by tests rather than prose,
and built for different AI tools working side by side. The Godot engine reference here comes from that project (MIT).

## License

MIT. `docs/engine-reference/godot` is MIT from Claude-Code-Game-Studios; see its licence file.
