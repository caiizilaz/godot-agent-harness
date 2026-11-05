## The Godot version must be the same everywhere it is written down, or agents trust a reference for
## the wrong engine: project.godot, the installed editor, CI, and docs/engine-reference.
extends RefCounted

const WORKFLOW_PATH: String = "res://.github/workflows/tests.yml"
## The one place CI and tools/ci/setup_godot.py read the exact version from ("4.7.2").
const VERSION_FILE_PATH: String = "res://tools/ci/godot-version.txt"
const SETUP_SCRIPT_PATH: String = "res://tools/ci/setup_godot.py"
const VERSION_DOC_PATH: String = "res://docs/engine-reference/godot/VERSION.md"


## "4.7" from the editor running this suite; everything else is compared against it.
func _installed_minor() -> String:
	var info: Dictionary = Engine.get_version_info()
	return "%d.%d" % [int(info.major), int(info.minor)]


## project.godot, tools/ci/godot-version.txt (what CI installs) and VERSION.md all name the installed minor
## version, and CI only points at files that exist.
func test_version_matches_everywhere() -> String:
	var minor: String = _installed_minor()
	var problems: PackedStringArray = []
	var features: PackedStringArray = ProjectSettings.get_setting("application/config/features")
	if not minor in features:
		problems.append("project.godot features %s do not include the installed %s" % [str(features), minor])
	var pinned: String = FileAccess.get_file_as_string(VERSION_FILE_PATH).strip_edges()
	if not pinned.begins_with(minor + "."):
		problems.append("tools/ci/godot-version.txt is '%s', installed is %s" % [pinned, minor])
	# Dot-folders are hidden from res://, so read the workflow by its real path.
	var workflow: String = FileAccess.get_file_as_string(ProjectSettings.globalize_path(WORKFLOW_PATH))
	for needed: String in ["tools/ci/godot-version.txt", "tools/ci/setup_godot.py"]:
		if not workflow.contains(needed):
			problems.append("tests.yml does not use %s" % needed)
	if not FileAccess.file_exists(SETUP_SCRIPT_PATH):
		problems.append("tools/ci/setup_godot.py is missing but tests.yml runs it")
	var doc: String = FileAccess.get_file_as_string(VERSION_DOC_PATH)
	if not doc.contains("| **Engine Version** | Godot %s" % minor):
		problems.append("docs/engine-reference/godot/VERSION.md does not say Godot %s" % minor)
	return "" if problems.is_empty() else "Godot version drift: " + "; ".join(problems)
