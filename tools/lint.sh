#!/usr/bin/env bash
# Run the same pinned gdlint as CI. Installs it once into a cache venv, so agents never
# need gdtoolkit on PATH and never lint with a different version than CI.
#
#   tools/lint.sh              # lint everything CI lints
#   tools/lint.sh a.gd b.gd    # lint only these files (the pre-commit hook uses this)
set -euo pipefail

cd "$(dirname "$0")/.."
VENV="${GDLINT_VENV:-${XDG_CACHE_HOME:-$HOME/.cache}/godot-agent-gdlint}"
REQS=tools/ci/requirements.txt

if [ ! -x "$VENV/bin/gdlint" ] || ! cmp -s "$REQS" "$VENV/requirements.txt"; then
	python3 -m venv "$VENV"
	"$VENV/bin/pip" install -q --disable-pip-version-check -r "$REQS"
	cp "$REQS" "$VENV/requirements.txt"
fi

# tests/run_tests.gd discovers suites on disk; a hand-listed suite array is the old merge-conflict hotspot.
if grep -qE 'res://tests/test_|\bSUITES\b' tests/run_tests.gd; then
	echo "tests/run_tests.gd must not list suites by hand (it auto-discovers tests/test_*.gd)" >&2
	exit 1
fi

if [ "$#" -gt 0 ]; then
	"$VENV/bin/gdlint" "$@"
else
	# Lint whichever of the usual folders exist, so a fresh template and a grown project both work.
	dirs=()
	for d in scripts scenes components tests tools addons/custom; do [ -d "$d" ] && dirs+=("$d"); done
	"$VENV/bin/gdlint" "${dirs[@]}"
fi
