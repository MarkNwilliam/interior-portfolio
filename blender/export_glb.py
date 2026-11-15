"""Export the interior scenes as web-ready GLB models (ceiling removed).

Run:
  /Applications/Blender.app/Contents/MacOS/Blender -b --python blender/export_glb.py
"""
import bpy
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = os.path.join(ROOT, "assets", "models")
os.makedirs(MODELS, exist_ok=True)

for name in ("reading-nook", "dining-corner", "oak-and-light", "quiet-quarters", "warm-kitchen"):
    blend = os.path.join(ROOT, "blender", name + ".blend")
    out = os.path.join(MODELS, name + ".glb")
    bpy.ops.wm.open_mainfile(filepath=blend)
    for obj in list(bpy.data.objects):
        if obj.name == "Ceiling":
            bpy.data.objects.remove(obj, do_unlink=True)
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.export_scene.gltf(
        filepath=out,
        export_format="GLB",
        use_selection=False,
        export_apply=True,
        export_cameras=False,
        export_lights=False,
        export_yup=True,
        export_animations=False,
    )
    print("Exported", out, os.path.getsize(out), "bytes")
