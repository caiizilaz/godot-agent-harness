#!/usr/bin/env bash
# Capture must produce a new artifact; old files never satisfy the check.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 tools/harness.py godot capture "$@"
