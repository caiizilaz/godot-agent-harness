#!/usr/bin/env bash
# Import the project, then run the headless suite. Use this instead of calling godot directly.
#
# Why a script: on a fresh worktree Godot 4.7 can segfault halfway through --import (seen
# reimporting a font) and still leave a .godot/ behind. The suite then runs against
# missing assets and logs the same error millions of times, which looks like a hang (10+ min,
# 9 GB log). This script checks every imported file exists, retries the import, and caps the
# suite's run time and log size so a broken run fails fast.
#
#   tools/test.sh              # import, then run all suites
#   tools/test.sh test_shop test_i18n   # only these suites (seconds, not minutes)
#   tools/test.sh --import-only
#   GODOT=~/godot/godot tools/test.sh
set -uo pipefail

GODOT="${GODOT:-godot}"
IMPORT_TRIES="${IMPORT_TRIES:-3}"
SUITE_TIMEOUT="${SUITE_TIMEOUT:-600}"    # seconds; CI's whole run is ~2.5 min
LOG_CAP_BYTES="${LOG_CAP_BYTES:-50000000}"

cd "$(dirname "$0")/.." || exit 1
LOG_DIR="$(mktemp -d "${TMPDIR:-/tmp}/godot-test.XXXXXX")"

# Every dest_files entry in a *.import file must exist under .godot/imported.
missing_imports() {
	find . -name '*.import' -not -path './.godot/*' -print0 \
		| xargs -0 command grep -h '^dest_files=' \
		| command grep -o 'res://[^"]*' \
		| while read -r res; do [ -e "./${res#res://}" ] || echo "$res"; done
}

# Kills the command after $1 seconds. Perl ships on macOS and Ubuntu; coreutils timeout does not on macOS.
with_timeout() {
	local secs="$1"; shift
	perl -e 'alarm shift; exec @ARGV' "$secs" "$@"
}

import_project() {
	local try missing
	for ((try = 1; try <= IMPORT_TRIES; try++)); do
		with_timeout 600 "$GODOT" --headless --path . --import >"$LOG_DIR/import.log" 2>&1
		missing="$(missing_imports | wc -l | tr -d ' ')"
		if ! command grep -q 'Program crashed' "$LOG_DIR/import.log" && [ "$missing" = 0 ]; then
			return 0
		fi
		echo "import try $try: crashed or $missing imported files missing; clearing .godot and retrying" >&2
		rm -rf .godot
	done
	echo "FAIL import did not complete after $IMPORT_TRIES tries (log: $LOG_DIR/import.log)" >&2
	return 1
}

# Always import: it picks up new or changed assets and takes seconds when nothing changed.
import_project || exit 1
[ "${1:-}" = "--import-only" ] && exit 0

# head -c stops the log at the cap; godot then dies on SIGPIPE instead of filling the disk.
with_timeout "$SUITE_TIMEOUT" "$GODOT" --headless --path . -s tests/run_tests.gd -- "$@" 2>&1 \
	| head -c "$LOG_CAP_BYTES" >"$LOG_DIR/suite.log"

command grep -E '^FAIL' "$LOG_DIR/suite.log" | head -50
summary="$(command grep -E '^[0-9]+/[0-9]+ passed$' "$LOG_DIR/suite.log" | tail -1)"
script_errors="$(command grep -c 'SCRIPT ERROR' "$LOG_DIR/suite.log")"
echo "${summary:-no summary line (timed out, crashed or hit the log cap)}, $script_errors SCRIPT ERROR. Log: $LOG_DIR/suite.log"

if [ -z "$summary" ]; then
	exit 1
fi
passed="${summary%%/*}"
rest="${summary#*/}"
total="${rest%% *}"
[ "$passed" = "$total" ]
