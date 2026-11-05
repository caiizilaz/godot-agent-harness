## Agents decide what to start from docs/agents/STATUS.md rows alone (AGENTS.md: grep your row and its
## Depends on), so a row that is merged, archived twice or blocked on finished work misleads them.
extends RefCounted

const STATUS_PATH: String = "res://docs/agents/STATUS.md"
const ARCHIVE_PATH: String = "res://docs/agents/STATUS_ARCHIVE.md"
const AGENTS_DIR: String = "res://docs/agents"


## The live board and the archive agree, and every linked brief exists.
func test_live_board_matches_archive_and_briefs() -> String:
	var problems: PackedStringArray = _problems(
		FileAccess.get_file_as_string(STATUS_PATH), FileAccess.get_file_as_string(ARCHIVE_PATH), _brief_exists)
	return "" if problems.is_empty() else "STATUS.md: %s (move finished rows and their brief/report to the archive in the same PR)" % "; ".join(problems)


## Each stale-row rule fires on a fixture, and a clean board passes.
func test_stale_rows_are_detected() -> String:
	var archive: String = "| [AG-1](archive/tasks/AG-1.md) | done | — | merged |\n| C-5 | done | — | merged |\n"
	var any_brief: Callable = func(_path: String) -> bool: return true
	var no_brief: Callable = func(_path: String) -> bool: return false
	var clean: String = "| ID | งาน | Depends on | สถานะ |\n|---|---|---|---|\n| C-7 | wire | AG-1 (merged), GLB จากผู้ใช้ | blocked |\n| C-8 | next | C-5 (merged), PR #3 | ready |\n"
	if not _problems(clean, archive, any_brief).is_empty():
		return "clean board flagged: %s" % str(_problems(clean, archive, any_brief))
	var cases: Dictionary = {
		"| C-9 | x | — | merged (PR #4) |": "C-9 is merged",
		"| C-5 | x | — | review |": "C-5 is also in STATUS_ARCHIVE",
		"| C-9 | x | AG-1, C-5 (merged) | blocked |": "C-9 is blocked only on merged work",
		"| C-9 | x | — | ready |\n| C-9 | y | — | ready |": "C-9 is listed twice",
		"| [AG-2](tasks/AG-2.md) | x | — | ready |": "AG-2 links missing brief tasks/AG-2.md",
	}
	for row: String in cases:
		var exists: Callable = no_brief if row.contains("AG-2") else any_brief
		var found: PackedStringArray = _problems(row, archive, exists)
		if not str(cases[row]) in found:
			return "missed '%s', got %s" % [cases[row], str(found)]
	return ""


func _brief_exists(relative: String) -> bool:
	return FileAccess.file_exists(AGENTS_DIR.path_join(relative))


func _problems(board: String, archive: String, brief_exists: Callable) -> PackedStringArray:
	var problems: PackedStringArray = []
	var archived: Dictionary = {}
	for row: Dictionary in _rows(archive):
		archived[row.id] = true
	var seen: Dictionary = {}
	for row: Dictionary in _rows(board):
		var id: String = row.id
		if seen.has(id):
			problems.append("%s is listed twice" % id)
		seen[id] = true
		var status: String = row.status
		if status.begins_with("merged"):
			problems.append("%s is merged: move the row to STATUS_ARCHIVE.md" % id)
		elif archived.has(id):
			problems.append("%s is also in STATUS_ARCHIVE" % id)
		if status.begins_with("blocked") and _blocked_only_on_archived(row.depends, archived):
			problems.append("%s is blocked only on merged work" % id)
		var link: String = row.link
		if not link.is_empty() and not bool(brief_exists.call(link)):
			problems.append("%s links missing brief %s" % [id, link])
	# Strip the hint suffixes so the fixture test can match the stable prefix of each message.
	var stable: PackedStringArray = []
	for problem: String in problems:
		stable.append(problem.get_slice(":", 0))
	return stable


## A blocked row is stale when every dependency is a task id already in the archive and nothing
## else (a user hand-off such as "GLB จากผู้ใช้") is left in the cell.
func _blocked_only_on_archived(depends: String, archived: Dictionary) -> bool:
	var ids: RegEx = RegEx.create_from_string("\\b(?:AG|CX|C)-\\d+[a-z]?\\b")
	var found: Array[RegExMatch] = ids.search_all(depends)
	if found.is_empty():
		return false
	for hit: RegExMatch in found:
		if not archived.has(hit.get_string()):
			return false
	var rest: String = ids.sub(depends, "", true)
	rest = RegEx.create_from_string("\\(merged\\)|PR #\\d+|[\\s,·—()-]").sub(rest, "", true)
	return rest.is_empty()


## Table rows whose first cell is a task id: "| [AG-90](tasks/AG-90.md) | ... |" or "| C-19 | ... |".
func _rows(text: String) -> Array[Dictionary]:
	var row_start: RegEx = RegEx.create_from_string("^\\|\\s*(?:\\[((?:AG|CX|C)-\\d+[a-z]?)\\]\\(([^)]+)\\)|((?:AG|CX|C)-\\d+[a-z]?))\\s*\\|")
	var rows: Array[Dictionary] = []
	for line: String in text.split("\n"):
		var head: RegExMatch = row_start.search(line)
		if head == null:
			continue
		var cells: PackedStringArray = line.trim_prefix("|").trim_suffix("|").split("|")
		if cells.size() < 4:
			continue
		var id: String = head.get_string(1) if not head.get_string(1).is_empty() else head.get_string(3)
		rows.append({"id": id, "link": head.get_string(2), "depends": cells[cells.size() - 2].strip_edges(),
			"status": cells[cells.size() - 1].strip_edges()})
	return rows
