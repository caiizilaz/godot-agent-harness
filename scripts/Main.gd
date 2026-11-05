## Example main scene: draws a title so tools/shot.sh has something to capture.
extends Control


func _ready() -> void:
	var background: ColorRect = ColorRect.new()
	background.color = Color(0.07, 0.08, 0.12)
	background.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(background)
	var title: Label = Label.new()
	title.text = "Godot Agent Harness\ncombo x%.1f at 5 hits" % Score.combo_multiplier(5)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 48)
	title.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(title)
