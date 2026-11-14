#!/usr/bin/env bash
# Compatibility wrapper; bounded core checks process status and engine evidence.
set -euo pipefail
cd "$(dirname "$0")/.."
if [ "${1:-}" = "--import-only" ]; then
  shift
  exec python3 tools/harness.py godot import "$@"
fi
exec python3 tools/harness.py godot test "$@"
