#!/usr/bin/env bash
# Run a scene in a real window, save a screenshot, and report runtime errors. A change the
# player can see is not done until it was looked at in the running game (CLAUDE.md "Checks");
# headless tests cannot tell a menu drawn off-screen from a correct one.
#
#   tools/shot.sh                                   # main scene -> shots/main.png
#   tools/shot.sh res://scenes/Main.tscn shots/menu.png 3
#   SHOT_RES=1280x720 tools/shot.sh main shots/small.png
#
# Exits non-zero when the scene logs SCRIPT ERROR / ERROR, the PNG is missing, or the frame is
# one flat colour (nothing rendered; checked in capture.gd). Needs a display: run it on your machine, not in CI.
set -uo pipefail

GODOT="${GODOT:-godot}"
scene="${1:-main}"
out="${2:-shots/$(basename "${scene%.tscn}").png}"
wait="${3:-1.5}"
res="${SHOT_RES:-1920x1080}"

cd "$(dirname "$0")/.." || exit 1
mkdir -p "$(dirname "$out")"
tools/test.sh --import-only || exit 1

log="$(mktemp "${TMPDIR:-/tmp}/shot.XXXXXX")"
perl -e 'alarm shift; exec @ARGV' 120 "$GODOT" --path . --resolution "$res" \
	-s tools/godot/capture.gd -- "$scene" "$out" "$wait" >"$log" 2>&1
status=$?

# Count only what the scene logged while it ran: everything after CAPTURE_OK is Godot's
# shutdown noise (leaked resources, allocator pages), not a problem in the game.
errors="$(awk '/CAPTURE_OK/{exit} {print}' "$log" \
	| command grep -E 'SCRIPT ERROR|^ERROR|CAPTURE_FAIL' | sort | uniq -c | sort -rn | head -20)"
if [ -n "$errors" ]; then
	echo "runtime errors (count, message):"
	echo "$errors"
fi
if [ "$status" -ne 0 ] || [ ! -s "$out" ]; then
	echo "FAIL no screenshot (exit $status). Log: $log" >&2
	exit 1
fi
command grep -h 'CAPTURE_OK' "$log"
[ -z "$errors" ]
