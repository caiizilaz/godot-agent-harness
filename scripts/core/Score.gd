## Example game rule kept pure so it is testable headless. Replace with your own; see D1.
class_name Score
extends RefCounted


## Each hit after the first adds 10% damage, capped at double, so long combos pay but cannot snowball.
static func combo_multiplier(hits: int) -> float:
	if hits <= 1:
		return 1.0
	return minf(1.0 + 0.1 * float(hits - 1), 2.0)
