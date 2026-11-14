<!-- content-revision: 1; source: th -->
# Start with SPACE8 LABS harness

Requires Python 3.11+, Git, the exact Godot version in tools/ci/godot-version.txt, and Node 22.18+ for TypeScript. Targets macOS/Linux; use WSL on Windows. Native Windows is unverified.

Run from the repository root. Expect Godot 6/6, three TypeScript tests, and the current tooling checks. Doctor checks executable availability without running configured commands. Inspect the JSON at the Evidence path.

Beginner: modify one score rule and its test. Solo: use a short brief and worktree without extra agents. Team: declare ownership/dependencies and assign one integrator for hot files.

```sh
python3 tools/harness.py inspect
python3 tools/harness.py doctor
python3 tools/harness.py check
# Generic example, no Godot required:
python3 tools/harness.py --config examples/typescript/harness.json check
# Existing compatibility entry points:
tools/test.sh test_score
tools/shot.sh main shots/main.png
```
