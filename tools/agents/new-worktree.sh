#!/usr/bin/env bash
# Validates identity before reuse. --offline avoids fetch; --skip-import supports generic projects.
set -euo pipefail
cd "$(dirname "$0")/../.."
exec python3 tools/harness/worktree.py "$@"
