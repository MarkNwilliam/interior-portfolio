"""Render diagnostic views of the interior scenes for visual QA."""
import bpy
import os
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = "/tmp/inspect"
os.makedirs(OUT, exist_ok=True)


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def shot(name, loc, target, lens, samples=12):
    scene = bpy.context.scene
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens = lens
    cam = bpy.data.objects.new(name, cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = loc
    look_at(cam, target)
    scene.camera = cam
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 800
    scene.render.resolution_y = 600
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.exposure = -0.5
    scene.render.filepath = os.path.join(OUT, name + ".png")
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)
    print("SHOT", name)


rooms = {
    "reading-nook": [
        ("reading-overall", (3.9, -3.1, 1.65), (-0.35, 0.35, 1.05), 33),
        ("reading-chair", (0.6, -1.5, 1.10), (-1.15, 0.35, 0.55), 55),
        ("reading-chair-side", (-0.1, -2.0, 1.15), (-1.15, 0.35, 0.55), 45),
        ("reading-shelf", (-0.4, -1.3, 1.30), (-2.25, 0.4, 0.90), 40),
        ("reading-high", (2.8, -3.0, 5.0), (-0.2, 0.3, 0.8), 38),
    ],
    "dining-corner": [
        ("dining-overall", (3.95, -3.2, 1.68), (-0.15, 0.2, 1.05), 35),
        ("dining-chairs", (1.6, -2.4, 1.30), (0.0, 0.3, 0.70), 45),
        ("dining-chairs-low", (-0.4, -2.4, 0.90), (0.0, 0.2, 0.65), 40),
        ("dining-high", (2.8, -3.3, 5.2), (-0.1, 0.3, 0.8), 38),
    ],
}

for room, shots in rooms.items():
    bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "blender", room + ".blend"))
    for obj in list(bpy.data.objects):
        if obj.name == "Ceiling":
            bpy.data.objects.remove(obj, do_unlink=True)
    for args in shots:
        shot(*args)
