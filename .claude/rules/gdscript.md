---
paths:
  - "**/*.gd"
---

# GDScript

- Godot 4.7. Unsure an API, signal or setting exists? Grep `docs/engine-reference/godot/` first.
- Tabs, static types everywhere (`var x: float`, `-> void`, typed arrays and dictionaries).
- `##` doc comment on every class and public func: say why, cite the decision (`D1`).
- Game rules in pure `RefCounted`/static code so tests can run them headless; scenes only present.
- `tools/lint.sh <files>` before committing; the pre-commit hook runs it on staged `.gd`.
