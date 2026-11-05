#!/usr/bin/env bash
# Create an isolated worktree for one agent task (AGENTS.md "Where you work").
#   tools/agents/new-worktree.sh CX-1 [base-branch]
# Reads the branch name from docs/agents/tasks/<ID>.md, puts the worktree in
# ../<repo>-worktrees/<ID>, and imports the Godot project so tests run straight away.
set -euo pipefail

id="${1:?usage: new-worktree.sh <TASK-ID> [base-branch]}"
base="${2:-${AGENT_BASE:-origin/main}}"
repo="$(git rev-parse --show-toplevel)"
brief="$repo/docs/agents/tasks/$id.md"

# Branch from the remote tip, not the local main: a stale base is how old branches kept
# merging the removed SUITES list back in.
# A fresh local clone with no remote yet branches from local main instead.
if git -C "$repo" remote get-url origin >/dev/null 2>&1; then
  git -C "$repo" fetch -q origin
elif [ "$base" = "origin/main" ]; then
  base=main
fi
# Lint staged GDScript on every commit in every worktree (hooks path is shared by all worktrees).
git -C "$repo" config core.hooksPath .githooks
[ -f "$brief" ] || { echo "no brief: $brief" >&2; exit 1; }

branch="$(grep -o 'agent/[a-z0-9-]*' "$brief" | head -1)"
[ -n "$branch" ] || { echo "no 'agent/...' branch in $brief" >&2; exit 1; }

# Agents need the rules inside their checkout; refuse a base that predates them.
git -C "$repo" cat-file -e "$base:AGENTS.md" 2>/dev/null \
  || { echo "$base has no AGENTS.md yet: commit the agent setup to $base first" >&2; exit 1; }

dest="$(dirname "$repo")/$(basename "$repo")-worktrees/$id"
if [ -d "$dest" ]; then
  echo "exists: $dest"
else
  if git -C "$repo" show-ref --verify --quiet "refs/heads/$branch"; then
    git -C "$repo" worktree add "$dest" "$branch"
  else
    git -C "$repo" worktree add -b "$branch" "$dest" "$base"
  fi
  # Retries the import when Godot crashes on a fresh .godot (see tools/test.sh).
  "$dest/tools/test.sh" --import-only || echo "warning: godot import failed in $dest" >&2
fi
echo "$dest"
