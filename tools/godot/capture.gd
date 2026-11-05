## Opens a scene in a real window, waits, and saves what the player would see (not part of the suite).
## Use tools/shot.sh, which also imports first and fails on runtime errors or a blank frame.
##   godot --path . --resolution 1920x1080 -s tools/godot/capture.gd -- <res://scene.tscn|main> <out.png> [seconds]
extends SceneTree


func _initialize() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	var scene_path: String = args[0] if args.size() > 0 else "main"
	if scene_path == "main":
		scene_path = str(ProjectSettings.get_setting("application/run/main_scene"))
	var out: String = args[1] if args.size() > 1 else "capture.png"
	var wait: float = float(args[2]) if args.size() > 2 else 1.5
	var packed: PackedScene = load(scene_path) as PackedScene
	if packed == null:
		printerr("CAPTURE_FAIL cannot load scene ", scene_path)
		quit(1)
		return
	root.add_child(packed.instantiate())
	await create_timer(wait).timeout
	# Two frames after the timer so the last draw has reached the viewport texture.
	await process_frame
	await process_frame
	var image: Image = root.get_viewport().get_texture().get_image()
	if _is_flat(image):
		printerr("CAPTURE_FAIL frame is one flat colour: nothing rendered")
		quit(1)
		return
	if image.save_png(ProjectSettings.globalize_path(out) if out.begins_with("res://") else out) != OK:
		printerr("CAPTURE_FAIL cannot write ", out)
		quit(1)
		return
	print("CAPTURE_OK ", out, " ", image.get_width(), "x", image.get_height())
	quit()


## Samples a 16x16 grid: one colour everywhere means the camera, scene or draw never happened.
func _is_flat(image: Image) -> bool:
	var first: Color = image.get_pixel(0, 0)
	for y: int in 16:
		for x: int in 16:
			var pixel: Color = image.get_pixel(x * (image.get_width() - 1) / 15, y * (image.get_height() - 1) / 15)
			if not pixel.is_equal_approx(first):
				return false
	return true
