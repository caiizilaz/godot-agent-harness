# Claude Code entry point

Read [AGENTS.md](AGENTS.md) for canonical task rules and [role profiles](docs/workflows/profiles.md).
Claude Code may be the integrator, implementer or reviewer according to the task assignment.
The following integration guidance applies only when you are the designated integrator.
Tool availability and verified results determine role assignment, not a fixed provider ranking.

## One worktree per session

The main checkout stays on `main`: read, fetch and `git worktree add` only. Never switch branches,
commit or reset there. Any change happens in `../<repo>-worktrees/claude-<slug>` (branch from `origin/main`);
remove the worktree after merge.

## Checks

```bash
python3 tools/harness.py check
```

- `tools/test.sh test_a test_b` runs only those suites while you work; CI runs everything in 4 shards.
- A change the player can see is not done on green tests: run `tools/shot.sh <res://scene.tscn|main> shots/<name>.png`,
  look at the PNG, attach it to the PR. It fails on runtime errors and blank frames. Needs a display, not CI.
- Unsure an engine API exists in 4.7? Grep `docs/engine-reference/godot/` before writing it.
- A test that fails once and passes on rerun is a bug: `tools/ci/flaky.sh` lists them. Fix, don't rerun forever.

## Merging

- Green CI = merge it yourself, except PRs that change `docs/decisions.md` content: those need the user's words.
- CI red on `main` = merge nothing else; the first PR fixes `main`.
- Before merging an agent branch: merge `origin/main` into it and read `git diff origin/main...<branch>` for lines
  that undo fixes already on `main`.
- Moving a task to done = move its STATUS row to `STATUS_ARCHIVE.md` and its brief/report to `docs/agents/archive/`
  in the same PR. `test_status_board` fails otherwise.
- If CI cannot run (billing, outage), run `python3 tools/harness.py check` on the branch merged with `origin/main`
  and say so in the PR before merging.
