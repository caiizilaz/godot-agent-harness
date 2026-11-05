## The table at the top of docs/decisions.md is what agents read first, so it must list every decision.
extends RefCounted


## Every "## Dnn" heading has a "| Dnn |" row in the index, and the index lists no missing decision.
func test_index_lists_every_decision() -> String:
	var text: String = FileAccess.get_file_as_string("res://docs/decisions.md")
	var headings: Dictionary = {}
	for hit: RegExMatch in RegEx.create_from_string("(?m)^## (D\\d+) ").search_all(text):
		headings[hit.get_string(1)] = true
	var rows: Dictionary = {}
	for hit: RegExMatch in RegEx.create_from_string("(?m)^\\| (D\\d+) \\|").search_all(text):
		rows[hit.get_string(1)] = true
	if headings.is_empty():
		return "no decisions found"
	var problems: PackedStringArray = []
	for id: String in headings:
		if not rows.has(id):
			problems.append("%s has no index row" % id)
	for id: String in rows:
		if not headings.has(id):
			problems.append("index row %s has no section" % id)
	return "" if problems.is_empty() else "decisions.md index: " + "; ".join(problems)
