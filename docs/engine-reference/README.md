# Engine reference

What changed in Godot after the models' training data (roughly 4.3). Before using an API, signal, node or
project setting you are not sure exists in 4.7, grep here first:

- `godot/breaking-changes.md` — 4.3 → 4.7, one section per version, highest risk first
- `godot/deprecated-apis.md` — old name → new name
- `godot/current-best-practices.md` — patterns that changed, CLI flags that look like checks but are not
- `godot/modules/*.md` — animation, audio, input, navigation, networking, physics, rendering, ui

`grep -rn "AnimationMixer" docs/engine-reference/godot` beats reading it all. If a note disagrees with code
that passes `tools/test.sh`, the passing code wins; fix the note.

Source: [Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios)
`docs/engine-reference/godot` at commit `05ad7c8`, MIT (`LICENSE-claude-code-game-studios`). Changed: the
installed-version field in `VERSION.md` and two references to that framework's own commands.

## When you change Godot version

1. Write the new exact version in `tools/ci/godot-version.txt`. `tests/test_engine_version.gd` then names everything that
   still says the old one (`project.godot` features, `godot/VERSION.md`, the editor you run).
2. Look at the source project's `docs/engine-reference/godot` at its newest commit. Copy sections for versions newer than
   the ones you have, keep its MIT licence file, and update the commit hash above.
3. Edit `godot/VERSION.md`: engine version, release date, and the line saying which version is installed.
4. If an API note disagrees with code that passes `tools/test.sh`, trust the passing code and fix the note.

