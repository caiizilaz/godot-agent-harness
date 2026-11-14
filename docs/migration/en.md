<!-- content-revision: 1; source: th -->
# Adopt in an existing project

Use a separate branch/worktree and record existing check results. Do not replace the project’s AGENTS.md.

Create harness.json in your project root using examples/typescript/harness.json as the schema example. Set argv to your existing test/lint/build commands and cwd to an internal directory. Invoke this harness checkout’s tools/harness.py with --config /absolute/project/harness.json.

Dry run: inspect, then doctor, before check executes commands. No game file moves or existing command changes are required. Roll back by removing only the added harness.json and using the original commands. Never remove unrelated files or user caches.
