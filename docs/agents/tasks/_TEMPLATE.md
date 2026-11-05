# <ID> — <title>

**Agent:** Codex | Antigravity · **Base:** `main` · **Branch:** `agent/<id>-<slug>` · **Effort:** low | medium | high

<!-- Effort: low = data/docs/generators · medium = default · high = touches a hot file other tasks also want -->

## Context
One or two sentences: why this exists and who consumes it.

## Contract
<!-- Required when a CX task and an AG task meet at the same data. The CX brief owns it;
     the AG brief copies this section word for word. Neither side renames or adds keys. -->
`<Producer>.<func>(...) -> Dictionary`

| Key | Type | Example | Notes |
|---|---|---|---|
| `kind` | `String` | `"attack"` | one of `attack`, `skill`, … |

Contract test: `tests/test_<thing>_contract.gd` (written by the CX side first) asserts every key and type above.

## Do
- Tests first.

## Owns
- `path/to/file.gd`
- New `tests/test_<thing>.gd` (the runner finds it automatically)
- `docs/agents/reports/<ID>.md`

## Done when
Measurable acceptance criteria. All suites green.

## Out of scope
What Claude or another task handles.
