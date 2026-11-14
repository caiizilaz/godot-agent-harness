# Measurement protocol

The included pilot measures **tool correctness and wrapper overhead**, not AI productivity.
Run `python3 benchmarks/pilot.py` from the repository. It compares the pre-overhaul wrapper
at the recorded base commit with the current wrapper using the same fake Godot executable.
Three repetitions per case/arm alternate order; include every failed run. The three cases are
healthy execution, import failure, and nonzero suite exit after a passing summary.
Use identical fixtures and acceptance (healthy succeeds; failures fail), and record elapsed time,
exit code, accepted outcome, runtime and platform. No paid calls occur. Tokens and human effort
are null because this experiment does not observe them. Do not market this as token savings.

A future end-to-end agent study must use fresh sessions, identical starting revisions and
acceptance tests, the same model/settings per matched pair, and alternate order. At least three
repetitions each for rule changes, runtime/import bugs and client/server contracts. Include setup,
review/handoff, retries and failures; report completion/regressions, median/range and missing data.
Do not spend on model APIs without an approved budget. Only publish savings after quality gates
are preserved. The current task has no independent model-session usage instrumentation.
