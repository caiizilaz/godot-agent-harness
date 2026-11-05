#!/usr/bin/env bash
# List tests that failed in recent CI runs, so a flaky test is fixed instead of re-run forever.
# A test failing on several different branches, or on a run whose rerun passed, is flaky or
# broke main; one failing on a single branch is usually that branch's own bug.
#
#   tools/ci/flaky.sh          # last 40 runs
#   tools/ci/flaky.sh 100
set -euo pipefail

limit="${1:-40}"
tmp="$(mktemp)"
gh run list --limit "$limit" --json databaseId,headBranch,conclusion,attempt \
	--jq '.[] | select(.conclusion == "failure" or .attempt > 1) | "\(.databaseId) \(.headBranch)"' \
	| while read -r run branch; do
		# --attempt 1 keeps the failed first try of a run that passed on rerun.
		gh run view "$run" --attempt 1 --log-failed 2>/dev/null \
			| command grep -oE 'FAIL test_[A-Za-z0-9_]+' | sort -u \
			| sed "s|^FAIL |$branch |" || true
	done >"$tmp"

if [ ! -s "$tmp" ]; then
	echo "no failing tests in the last $limit runs"
	exit 0
fi
echo "failures  branches  test"
awk '{fails[$2]++; key=$2 SUBSEP $1; if (!(key in seen)) {seen[key]=1; branches[$2]++}}
	END {for (t in fails) printf "%8d  %8d  %s\n", fails[t], branches[t], t}' "$tmp" | sort -rn
rm -f "$tmp"
