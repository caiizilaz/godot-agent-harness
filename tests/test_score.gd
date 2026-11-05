## Example suite: every tests/test_*.gd is found by tests/run_tests.gd; each test_* returns "" on pass.
extends RefCounted


func test_single_hit_has_no_bonus() -> String:
	return "" if is_equal_approx(Score.combo_multiplier(1), 1.0) else "1 hit should be x1.0"


func test_combo_grows_then_caps_at_double() -> String:
	if not is_equal_approx(Score.combo_multiplier(5), 1.4):
		return "5 hits should be x1.4, got %s" % Score.combo_multiplier(5)
	return "" if is_equal_approx(Score.combo_multiplier(50), 2.0) else "long combos must cap at x2.0"
