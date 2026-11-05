# Decision log

Design and process decisions with their reasons. Change one by adding a new entry; never delete the old one.

## Index (read this first, then grep `## Dnn`)

| ID | One-line summary |
|---|---|
| D1 | Agents and roles: Claude integrates, Codex does logic + tests, Antigravity does visuals |

Adding a decision = adding a row here too (`tests/test_decisions_index.gd` checks).

## D1 — Agents and roles (template default)

- **Claude Code** integrates: writes briefs, owns shared files, merges every branch, keeps the board true.
- **Codex** gets work that tests can judge: rules, data, AI, generators.
- **Antigravity** gets work that needs eyes: screens, art review, asset research, images.
- Why: each tool works where it is strongest, and only one agent ever writes the shared files.
