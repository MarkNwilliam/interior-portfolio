"""Headless warm-minimal interior renders for the portfolio.

Run:
  /Applications/Blender.app/Contents/MacOS/Blender -b --python blender/render_rooms.py
"""
import bpy
import math
import os
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDERS = os.path.join(ROOT, "blender", "renders")
os.makedirs(RENDERS, exist_ok=True)


def srgb(hex_color):
    h = hex_color.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (*out, 1.0)


def clear():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras):
        for item in list(block):
            if item.users == 0:
                block.remove(item)


def mat(name, color, rough=0.6, metal=0.0, emission=None, strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = srgb(color)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if emission:
        for key in ("Emission Color", "Emission"):
            if key in bsdf.inputs:
                bsdf.inputs[key].default_value = srgb(emission)
                break
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = strength
    return m


def box(name, size, loc, material, rot=(0, 0, 0), bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = (size[0], size[1], size[2])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    if bevel:
        mod = o.modifiers.new("soft", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    return o


def cyl(name, radius, depth, loc, material, rot=(0, 0, 0), vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot
    )
    o = bpy.context.object
    o.name = name
    o.data.materials.append(material)
    return o


def cone(name, r1, r2, depth, loc, material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(
        vertices=32, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot
    )
    o = bpy.context.object
    o.name = name
    o.data.materials.append(material)
    return o


def sphere(name, radius, loc, material, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=radius, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    o.data.materials.append(material)
    return o


def plane(name, size, loc, material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = (size[0], size[1], 1)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    return o


def area(name, loc, target, energy, size, color=(1.0, 0.92, 0.82)):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = energy
    data.shape = "RECTANGLE"
    data.size = size
    data.color = color
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    look_at(obj, target)
    return obj


def point(name, loc, energy, color=(1.0, 0.75, 0.5), radius=0.08):
    data = bpy.data.lights.new(name, "POINT")
    data.energy = energy
    data.color = color
    data.shadow_soft_size = radius
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    return obj


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def camera(loc, target, lens=34):
    data = bpy.data.cameras.new("Camera")
    data.lens = lens
    obj = bpy.data.objects.new("Camera", data)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    look_at(obj, target)
    bpy.context.scene.camera = obj
    return obj


def palette():
    return {
        "cream": mat("Cream", "#f1e9dc", 0.85),
        "cream_deep": mat("Cream deep", "#e4d8c6", 0.8),
        "oak": mat("Oak", "#b98d5f", 0.55),
        "oak_dark": mat("Oak dark", "#8a643f", 0.6),
        "charcoal": mat("Charcoal", "#3b3631", 0.7),
        "sage": mat("Sage", "#8f9c88", 0.9),
        "terracotta": mat("Terracotta", "#b06a4f", 0.85),
        "linen": mat("Linen", "#ddd2c0", 0.95),
        "white": mat("Warm white", "#f5f1e8", 0.9),
        "brass": mat("Brass", "#b08d57", 0.3, 0.85),
        "floor": mat("Floor", "#a97c50", 0.5),
        "leaf": mat("Leaf", "#5f7355", 0.8),
        "glass": mat("Window light", "#f7efe0", 0.4, 0.0, "#fff3dd", 1.5),
        "lamp": mat("Lamp shade", "#f3e6cf", 0.6, 0.0, "#ffd9a0", 4.0),
        "art1": mat("Art 1", "#c9a98a", 0.9),
        "art2": mat("Art 2", "#7d8b7c", 0.9),
    }


def art_frame(name, loc, rot, w, h, canvas_mat, p, wall_y=None):
    box(name + " frame", (w, 0.03, h), loc, p["oak_dark"], rot=rot)
    if wall_y is not None:
        box(name + " canvas", (w - 0.06, 0.012, h - 0.06),
            (loc[0], wall_y, loc[2]), canvas_mat, rot=rot)


def plant(name, loc, scale, p):
    cyl(name + " pot", 0.11 * scale, 0.22 * scale, (loc[0], loc[1], loc[2] + 0.11 * scale), p["terracotta"])
    for i, (dx, dy, dz, s) in enumerate([
        (0.0, 0.0, 0.36, 1.0), (0.09, 0.03, 0.42, 0.85), (-0.08, 0.04, 0.40, 0.8),
        (0.03, -0.09, 0.38, 0.75), (-0.03, 0.09, 0.44, 0.7),
    ]):
        sphere(name + " leaf %d" % i, 0.1 * scale * s,
               (loc[0] + dx * scale, loc[1] + dy * scale, loc[2] + dz * scale),
               p["leaf"], scale=(1.0, 0.75, 1.25))
    cyl(name + " stem", 0.012 * scale, 0.38 * scale,
        (loc[0], loc[1], loc[2] + 0.24 * scale), p["oak_dark"])


def bookshelf(name, loc, rot_z, p):
    w, h, d = 1.15, 1.7, 0.32
    box(name + " back", (w, 0.03, h), (loc[0], loc[1] + d / 2 - 0.02, loc[2] + h / 2), p["oak_dark"], rot=(0, 0, rot_z))
    for i in (-1, 1):
        box(name + " side", (0.04, d, h), (loc[0] + i * (w / 2), loc[1], loc[2] + h / 2), p["oak"], rot=(0, 0, rot_z))
    for k in range(4):
        z = loc[2] + 0.06 + k * 0.42
        box(name + " shelf", (w, d, 0.035), (loc[0], loc[1], z), p["oak"], rot=(0, 0, rot_z))
        x = -w / 2 + 0.08
        idx = 0
        while x < w / 2 - 0.1:
            bw = 0.035 + 0.015 * ((idx + k) % 3)
            bh = 0.22 + 0.06 * ((idx + k) % 4)
            color = ["terracotta", "sage", "cream_deep", "charcoal", "oak_dark"][(idx + k) % 5]
            box(name + " book", (bw, 0.18, bh), (loc[0] + x, loc[1], z + bh / 2 + 0.02), p[color], rot=(0, 0, rot_z))
            x += bw + 0.012
            idx += 1


def armchair(name, loc, rot_z, p):
    box(name + " seat", (0.78, 0.72, 0.20), (loc[0], loc[1], 0.42), p["linen"], rot=(0, 0, rot_z), bevel=0.06)
    box(name + " back", (0.78, 0.16, 0.62), (loc[0], loc[1] + 0.30, 0.68), p["linen"], rot=(math.radians(-8), 0, rot_z), bevel=0.06)
    box(name + " cushion", (0.60, 0.14, 0.34), (loc[0], loc[1] + 0.16, 0.60), p["sage"], rot=(math.radians(-10), 0, rot_z), bevel=0.07)
    for i in (-1, 1):
        box(name + " arm", (0.14, 0.72, 0.34), (loc[0] + i * 0.36, loc[1], 0.53), p["cream_deep"], rot=(0, 0, rot_z), bevel=0.05)


def rug(name, loc, w, d, material):
    box(name, (w, d, 0.015), (loc[0], loc[1], 0.008), material, bevel=0.004)


def setup_render(cam_loc, cam_target, lens, path, samples=28):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.filepath = path
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.exposure = -1.1
    try:
        scene.view_settings.look = "AgX - Medium High Contrast"
    except Exception:
        pass
    camera(cam_loc, cam_target, lens)
    world = bpy.data.worlds.new("World")
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = srgb("#cfc3b2")
    bg.inputs[1].default_value = 0.45
    scene.world = world


def room(w, d, p):
    plane("Floor", (w, d), (0, 0, 0), p["floor"])
    box("Back wall", (w, 0.12, 2.9), (0, d / 2, 1.45), p["cream"])
    box("Side wall", (0.12, d, 2.9), (-w / 2, 0, 1.45), p["cream"])
    box("Ceiling", (w, d, 0.08), (0, 0, 2.86), p["white"])


def window(name, loc, w, h, p):
    box(name + " glow", (w, h, 0.02), (loc[0], loc[1] + 0.02, loc[2]), p["glass"])
    box(name + " frame top", (w + 0.1, 0.07, 0.07), (loc[0], loc[1], loc[2] + h / 2), p["white"])
    box(name + " frame bottom", (w + 0.1, 0.07, 0.07), (loc[0], loc[1], loc[2] - h / 2), p["white"])
    for i in (-1, 1):
        box(name + " frame side", (0.07, 0.07, h), (loc[0] + i * w / 2, loc[1], loc[2]), p["white"])
    box(name + " mullion", (0.045, 0.06, h), (loc[0], loc[1], loc[2]), p["white"])


def reading_nook():
    clear()
    p = palette()
    room(5.0, 4.0, p)
    rug("Rug", (0.1, 0.1), 2.4, 1.9, p["cream_deep"])
    window("Window", (0.9, 1.94, 1.65), 1.5, 1.6, p)
    area("Window key", (0.9, 1.75, 1.8), (0.0, -0.2, 0.9), 480, 2.2, (1.0, 0.9, 0.78))
    area("Fill", (-1.0, -1.2, 2.5), (0.2, 0.6, 0.8), 120, 3.0, (1.0, 0.95, 0.9))
    point("Warm corner", (-2.0, 1.4, 2.1), 70, (1.0, 0.72, 0.45), 0.1)

    armchair("Chair", (-1.15, 0.35), math.radians(28), p)
    rug("Chair throw", (-1.15, 0.35), 1.5, 1.3, p["sage"])
    cyl("Table top", 0.28, 0.05, (0.0, 0.95, 0.52), p["oak"])
    cyl("Table stem", 0.035, 0.48, (0.0, 0.95, 0.25), p["brass"])
    cyl("Table base", 0.16, 0.03, (0.0, 0.95, 0.02), p["brass"])
    cyl("Vase", 0.055, 0.2, (0.0, 0.95, 0.65), p["terracotta"])
    sphere("Vase bloom", 0.07, (0.0, 0.95, 0.82), p["sage"], scale=(1, 1, 1.2))

    cyl("Lamp pole", 0.018, 1.55, (-2.05, -0.2, 0.78), p["charcoal"])
    cone("Lamp shade", 0.24, 0.12, 0.3, (-2.05, -0.2, 1.58), p["lamp"])
    point("Lamp light", (-2.05, -0.2, 1.5), 60, (1.0, 0.68, 0.4), 0.12)
    cyl("Lamp base", 0.16, 0.03, (-2.05, -0.2, 0.015), p["charcoal"])

    bookshelf("Shelf", (-2.35, 0.4, 0.0), math.radians(90), p)
    plant("Plant", (2.05, 1.5, 0.0), 1.35, p)
    art_frame("Art A", (-1.55, 1.92, 1.85), (math.radians(90), 0, 0), 0.55, 0.7, p["art1"], p, wall_y=1.985)
    box("Art C frame", (0.42, 0.03, 0.52), (1.9, 1.985, 1.9), p["oak_dark"], rot=(math.radians(90), 0, 0))
    box("Art C canvas", (0.36, 0.012, 0.46), (1.9, 1.997, 1.9), p["art2"], rot=(math.radians(90), 0, 0))

    setup_render((3.9, -3.1, 1.65), (-0.35, 0.35, 1.05), 33,
                 os.path.join(RENDERS, "reading-nook.png"))


def dining_corner():
    clear()
    p = palette()
    room(5.0, 4.2, p)
    rug("Dining rug", (0.0, 0.15), 2.8, 2.0, p["cream_deep"])
    window("Window", (0.6, 2.04, 1.7), 1.7, 1.7, p)
    area("Window key", (0.6, 1.85, 1.85), (0.0, -0.2, 0.9), 520, 2.4, (1.0, 0.9, 0.78))
    area("Fill", (-1.4, -1.4, 2.5), (0.3, 0.5, 0.8), 110, 3.0, (1.0, 0.95, 0.9))
    point("Pendant light", (0.0, 0.15, 2.02), 85, (1.0, 0.72, 0.45), 0.15)

    box("Table top", (1.9, 0.95, 0.06), (0.0, 0.15, 0.75), p["oak"], bevel=0.01)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl("Table leg", 0.035, 0.72, (sx * 0.8, 0.15 + sy * 0.34, 0.36), p["oak_dark"])
    for i, (x, y, rz) in enumerate([(-0.62, -0.62, 0), (0.62, -0.62, 0), (-0.62, 0.92, 180), (0.62, 0.92, 180)]):
        box("Chair seat %d" % i, (0.44, 0.44, 0.05), (x, y, 0.46), p["oak"], rot=(0, 0, math.radians(rz)), bevel=0.01)
        box("Chair back %d" % i, (0.44, 0.05, 0.48), (x, y + (0.19 if rz == 0 else -0.19), 0.72), p["oak"], rot=(0, 0, math.radians(rz)), bevel=0.01)
        for lx, ly in [(-0.18, -0.18), (0.18, -0.18), (-0.18, 0.18), (0.18, 0.18)]:
            cyl("Chair leg %d" % i, 0.018, 0.46, (x + lx, y + ly, 0.23), p["oak_dark"])

    cyl("Pendant cord", 0.008, 0.72, (0.0, 0.15, 2.46), p["charcoal"])
    cone("Pendant shade", 0.24, 0.09, 0.22, (0.0, 0.15, 2.05), p["lamp"])

    cyl("Vase tall", 0.07, 0.32, (0.0, 0.15, 0.94), p["terracotta"])
    sphere("Branch", 0.12, (0.05, 0.15, 1.18), p["sage"], scale=(0.7, 0.7, 1.3))

    box("Sideboard", (1.5, 0.4, 0.62), (-1.85, 1.05, 0.31), p["oak"], bevel=0.015)
    box("Sideboard top", (1.54, 0.44, 0.03), (-1.85, 1.05, 0.635), p["oak_dark"])
    cyl("Bowl", 0.13, 0.09, (-1.55, 1.05, 0.7), p["cream"])
    plant("Plant", (2.05, 1.55, 0.0), 1.25, p)

    box("Art frame", (0.9, 0.035, 0.6), (1.5, 2.07, 1.8), p["oak_dark"])
    box("Art canvas", (0.82, 0.012, 0.52), (1.5, 2.09, 1.8), p["art2"])

    setup_render((3.95, -3.2, 1.68), (-0.15, 0.2, 1.05), 35,
                 os.path.join(RENDERS, "dining-corner.png"))


reading_nook()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "blender", "reading-nook.blend"))
bpy.ops.render.render(write_still=True)
print("Rendered reading nook")

dining_corner()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "blender", "dining-corner.blend"))
bpy.ops.render.render(write_still=True)
print("Rendered dining corner")
