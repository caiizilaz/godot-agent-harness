## Headless test runner: godot --headless --script tests/run_tests.gd [-- test_name ...]
## Names after -- run only those suites (with or without .gd); none runs every suite.
extends SceneTree

## Every tests/test_*.gd is a suite. Found on disk rather than listed, so parallel agent
## branches never edit the same lines of this file (it was the top merge-conflict hotspot).
const TESTS_DIR: String = "res://tests"


## Sorted so the run order is stable across machines and file systems.
static func discover_suites() -> Array[String]:
	var suites: Array[String] = []
	for file: String in DirAccess.get_files_at(TESTS_DIR):
		if file.begins_with("test_") and file.ends_with(".gd"):
			suites.append(TESTS_DIR + "/" + file)
	suites.sort()
	return suites


## Keeps the suites named in wanted ("test_shop" or "test_shop.gd"); empty keeps all.
static func select_suites(suites: Array[String], wanted: PackedStringArray) -> Array[String]:
	if wanted.is_empty():
		return suites
	var picked: Array[String] = []
	for path: String in suites:
		var file: String = path.get_file()
		if file in wanted or file.get_basename() in wanted:
			picked.append(path)
	return picked


## TEST_SHARD="2/4" keeps every 4th suite starting at the 2nd, so CI can run the suite as
## parallel jobs. Together the shards cover each suite exactly once; unset or malformed keeps all.
static func shard_suites(suites: Array[String], spec: String) -> Array[String]:
	var parts: PackedStringArray = spec.split("/")
	if parts.size() != 2 or not parts[0].is_valid_int() or not parts[1].is_valid_int():
		return suites
	var index: int = parts[0].to_int()
	var count: int = parts[1].to_int()
	if count < 1 or index < 1 or index > count:
		return suites
	var picked: Array[String] = []
	for i: int in suites.size():
		if i % count == index - 1:
			picked.append(suites[i])
	return picked


## Counts engine/script errors so a test that crashes fails even if it returned "".
class ErrorCounter:
	extends Logger
	var count: int = 0

	func _log_error(_function: String, _file: String, _line: int, _code: String, _rationale: String,
			_editor_notify: bool, _error_type: int, _script_backtraces: Array[ScriptBacktrace]) -> void:
		count += 1


var _ran: bool = false
var _errors: ErrorCounter = ErrorCounter.new()


## Suites run on the first frame (not _init) so the root is inside the tree and nodes that
## suites spawn get _enter_tree/_ready.
func _process(_delta: float) -> bool:
	if not _ran:
		_ran = true
		_run_suites()
	return false


func _run_suites() -> void:
	OS.add_logger(_errors)
	var failures: int = 0
	var total: int = 0
	var suites: Array[String] = shard_suites(
			select_suites(discover_suites(), OS.get_cmdline_user_args()), OS.get_environment("TEST_SHARD"))
	if suites.is_empty():
		printerr("FAIL no suites found in ", TESTS_DIR, " matching ", OS.get_cmdline_user_args())
		quit(1)
		return
	for path: String in suites:
		print("== ", path.get_file())
		var script: GDScript = load(path) as GDScript
		if script == null or not script.can_instantiate():
			failures += 1
			total += 1
			printerr("FAIL could not load suite ", path)
			continue
		var suite: RefCounted = script.new()
		for method: Dictionary in suite.get_method_list():
			var name: String = method["name"]
			if not name.begins_with("test_"):
				continue
			total += 1
			var errors_before: int = _errors.count
			var returned: Variant = suite.call(name)
			var error: String = returned if returned is String else ""
			if _errors.count > errors_before or not returned is String:
				error = "test raised an error (see SCRIPT ERROR above)"
			if error.is_empty():
				print("PASS ", name)
			else:
				failures += 1
				printerr("FAIL ", name, ": ", error)
	print("%d/%d passed" % [total - failures, total])
	quit(1 if failures > 0 else 0)
