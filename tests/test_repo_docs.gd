## Agents follow the paths written in the rule files, so a renamed script or moved doc that the rules
## still mention sends them to a file that is not there. Also: scripts agents run must stay executable.
extends RefCounted

## Files whose backticked paths agents are told to follow.
const DOC_PATHS: Array[String] = [
	"CLAUDE.md", "AGENTS.md", "README.md", "CONTRIBUTING.md",
	".claude/rules/agent-board.md", ".claude/rules/gdscript.md", ".claude/rules/tests.md",
	".agent/rules/antigravity.md", ".agent/workflows/start-task.md",
	".agent/workflows/finish-task.md", ".agent/workflows/verify.md",
]
## Only paths under these roots are checked; "shots/", "../" and bare words are ignored.
const ROOTS: Array[String] = [
	"tools/", "docs/", "tests/", "scripts/", "scenes/", ".claude/", ".agent/", ".github/", ".githooks/",
]
const EXECUTABLES: Array[String] = [
	"tools/test.sh", "tools/lint.sh", "tools/shot.sh", "tools/agents/new-worktree.sh",
	"tools/ci/flaky.sh", ".githooks/pre-commit",
]


func _root() -> String:
	return ProjectSettings.globalize_path("res://")


## A backticked token that names a concrete repo file (no placeholder, glob or trailing slash).
func _is_checkable(token: String) -> bool:
	for bad: String in ["<", ">", "*", " ", "$", "{", "..", "://"]:
		if bad in token:
			return false
	if token.ends_with("/"):
		return false
	for root: String in ROOTS:
		if token.begins_with(root):
			return true
	return false


func _backticked(text: String) -> PackedStringArray:
	var found: PackedStringArray = []
	var re: RegEx = RegEx.new()
	re.compile("`([^`\\n]+)`")
	for m: RegExMatch in re.search_all(text):
		var token: String = m.get_string(1)
		if _is_checkable(token) and not token in found:
			found.append(token)
	return found


## Every concrete path the rule files mention exists.
func test_documented_paths_exist() -> String:
	var problems: PackedStringArray = []
	for doc: String in DOC_PATHS:
		var abs_doc: String = _root().path_join(doc)
		if not FileAccess.file_exists(abs_doc):
			problems.append("%s is listed in this test but missing" % doc)
			continue
		for token: String in _backticked(FileAccess.get_file_as_string(abs_doc)):
			if not FileAccess.file_exists(_root().path_join(token)) and not DirAccess.dir_exists_absolute(_root().path_join(token)):
				problems.append("%s mentions %s which does not exist" % [doc, token])
	return "" if problems.is_empty() else "; ".join(problems)


## The path extractor ignores placeholders, globs and non-repo paths, and keeps real ones.
func test_path_extraction_rules() -> String:
	var text: String = "`tools/test.sh` `tests/test_*.gd` `docs/agents/reports/<TASK-ID>.md` `shots/a.png` `tools/x.sh --flag` `docs/agents/`"
	var got: PackedStringArray = _backticked(text)
	return "" if got == PackedStringArray(["tools/test.sh"]) else "extracted %s" % str(got)


## Scripts that agents and the hook run directly keep their executable bit.
func test_scripts_are_executable() -> String:
	var problems: PackedStringArray = []
	for path: String in EXECUTABLES:
		var abs_path: String = _root().path_join(path)
		if not FileAccess.file_exists(abs_path):
			problems.append("%s missing" % path)
		elif FileAccess.get_unix_permissions(abs_path) & 64 == 0:  # 64 = owner-execute bit (0o100)
			problems.append("%s is not executable" % path)
	return "" if problems.is_empty() else "; ".join(problems)
