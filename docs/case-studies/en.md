<!-- content-revision: 1; source: th -->
# Lessons from TKR and HMP

TKR combines a Godot client with a TypeScript server. HMP uses Godot and headless tests. These SPACE8 LABS game projects informed this workflow.

Keep logic testable, define explicit contracts, assign one writer to shared hot files, inspect rendered output for player-visible changes, and bound diagnostic logs.

This edition separates the process runner from Godot and adds a generic command adapter. Unity/Unreal support and end-to-end token savings are not established. See benchmarks/protocol.md and results.json for measurement limits.
