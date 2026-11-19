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


def _set(node, name, value):
    if name in node.inputs:
        node.inputs[name].default_value = value


def mat(name, color, rough=0.6, metal=0.0, emission=None, strength=0.0,
        grain=0.0, grain_scale=6.0, grain_contrast=0.35, micro=0.0,
        weave=0.0, coat=0.0, sheen=0.0, vary=0.05):
    """Principled BSDF with procedural grain, micro-bump, fabric sheen and
    non-uniform roughness, so surfaces read as real rather than flat plastic."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    base = srgb(color)
    _set(bsdf, "Base Color", base)
    _set(bsdf, "Roughness", rough)
    _set(bsdf, "Metallic", metal)
    if emission:
        _set(bsdf, "Emission Color", srgb(emission))
        _set(bsdf, "Emission", srgb(emission))
        _set(bsdf, "Emission Strength", strength)
    if coat:
        _set(bsdf, "Coat Weight", coat)
        _set(bsdf, "Coat Roughness", 0.12)
    if sheen:
        _set(bsdf, "Sheen Weight", sheen)
        _set(bsdf, "Sheen Roughness", 0.35)

    if grain or weave or micro or vary:
        tex = nt.nodes.new("ShaderNodeTexCoord")
        mp = nt.nodes.new("ShaderNodeMapping")
        nt.links.new(tex.outputs["Object"], mp.inputs["Vector"])

    if vary or micro or weave:
        nz = nt.nodes.new("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = 900.0 if weave else 26.0
        nz.inputs["Detail"].default_value = 6.0
        nz.inputs["Roughness"].default_value = 0.6
        nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
        if vary:
            mr = nt.nodes.new("ShaderNodeMapRange")
            mr.inputs["To Min"].default_value = max(0.0, rough - vary)
            mr.inputs["To Max"].default_value = min(1.0, rough + vary)
            nt.links.new(nz.outputs["Fac"], mr.inputs["Value"])
            nt.links.new(mr.outputs["Result"], bsdf.inputs["Roughness"])
        if micro or weave:
            bump = nt.nodes.new("ShaderNodeBump")
            bump.inputs["Strength"].default_value = weave if weave else micro
            nt.links.new(nz.outputs["Fac"], bump.inputs["Height"])
            nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

    if grain:
        wv = nt.nodes.new("ShaderNodeTexWave")
        wv.wave_type = "BANDS"
        wv.bands_direction = "Y"
        wv.inputs["Scale"].default_value = grain_scale
        wv.inputs["Distortion"].default_value = 9.0
        wv.inputs["Detail"].default_value = 5.0
        if "Detail Scale" in wv.inputs:
            wv.inputs["Detail Scale"].default_value = 1.4
        nt.links.new(mp.outputs["Vector"], wv.inputs["Vector"])
        rmp = nt.nodes.new("ShaderNodeValToRGB")
        dark = tuple(c * (1.0 - grain_contrast) for c in base[:3]) + (1.0,)
        rmp.color_ramp.elements[0].position = 0.28
        rmp.color_ramp.elements[0].color = dark
        rmp.color_ramp.elements[1].position = 0.72
        rmp.color_ramp.elements[1].color = base
        nt.links.new(wv.outputs["Fac"], rmp.inputs["Fac"])
        nt.links.new(rmp.outputs["Color"], bsdf.inputs["Base Color"])
        if not (micro or weave):
            bump = nt.nodes.new("ShaderNodeBump")
            bump.inputs["Strength"].default_value = 0.12
            nt.links.new(wv.outputs["Fac"], bump.inputs["Height"])
            nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return m


def rot_xy(x, y, angle):
    c, s = math.cos(angle), math.sin(angle)
    return (x * c - y * s, x * s + y * c)


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
        "cream": mat("Cream", "#f1e9dc", 0.92, micro=0.04),
        "cream_deep": mat("Cream deep", "#e4d8c6", 0.88, sheen=0.35, vary=0.06),
        "oak": mat("Oak", "#b98d5f", 0.5, grain=1, grain_scale=7.0, coat=0.16, vary=0.05),
        "oak_dark": mat("Oak dark", "#8a643f", 0.55, grain=1, grain_scale=7.0, coat=0.08, vary=0.05),
        "charcoal": mat("Charcoal", "#3b3631", 0.62, vary=0.06),
        "sage": mat("Sage", "#8f9c88", 0.92, sheen=0.5, weave=0.25, vary=0.05),
        "terracotta": mat("Terracotta", "#b06a4f", 0.85, micro=0.06, vary=0.05),
        "linen": mat("Linen", "#ddd2c0", 0.95, sheen=0.6, weave=0.3, vary=0.05),
        "white": mat("Warm white", "#f5f1e8", 0.9, micro=0.03, vary=0.05),
        "brass": mat("Brass", "#b08d57", 0.28, 0.85, vary=0.08),
        "floor": mat("Floor", "#a97c50", 0.45, grain=1, grain_scale=5.5, coat=0.14, vary=0.05),
        "leaf": mat("Leaf", "#5f7355", 0.8, micro=0.05),
        "sprig": mat("Sprig green", "#7c8b6a", 0.85, micro=0.05),
        "appliance": mat("Appliance", "#f2f0ea", 0.28, coat=0.4, vary=0.03),
        "counter": mat("Counter stone", "#ece4d6", 0.3, coat=0.25, micro=0.02, vary=0.04),
        "glass": mat("Window light", "#f7efe0", 0.4, 0.0, "#fff3dd", 2.2),
        "outside": mat("Outside green", "#93a184", 0.9, 0.0, "#8ea079", 0.5),
        "lamp": mat("Lamp shade", "#f3e6cf", 0.6, 0.0, "#ffd9a0", 4.0),
        "art1": mat("Art 1", "#c9a98a", 0.9, micro=0.03),
        "art2": mat("Art 2", "#7d8b7c", 0.9, micro=0.03),
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


def sprig(name, loc, scale, p):
    # a slender vase with a few leafy stems: reads as a small table plant
    cyl(name + " vase", 0.05 * scale, 0.24 * scale,
        (loc[0], loc[1], loc[2] + 0.12 * scale), p["terracotta"])
    top = loc[2] + 0.24 * scale
    for i, (dx, dy, tilt, dz, s) in enumerate([
        (0.00, 0.00, 0.0, 0.26, 1.00), (0.05, 0.02, 0.30, 0.22, 0.88),
        (-0.05, 0.03, -0.32, 0.21, 0.85), (0.02, -0.05, 0.14, 0.19, 0.80),
        (-0.02, -0.04, -0.14, 0.17, 0.74),
    ]):
        cyl(name + " stem %d" % i, 0.006 * scale, dz * scale,
            (loc[0] + dx * scale, loc[1] + dy * scale, top + dz * scale / 2),
            p["leaf"], rot=(tilt, 0, 0), vertices=8)
        for j in range(3):
            f = 0.35 + 0.3 * j
            sphere(name + " leaf %d-%d" % (i, j), 0.055 * scale * s,
                   (loc[0] + dx * scale * f + (0.02 if j % 2 else -0.02) * scale,
                    loc[1] + dy * scale * f, top + dz * scale * f),
                   p["sprig"], scale=(0.6, 0.6, 1.6))


def bookshelf(name, loc, rot_z, p):
    w, h, d = 1.15, 1.7, 0.32

    def part(label, size, lx, ly, lz, material, bevel=0.0):
        wx, wy = rot_xy(lx, ly, rot_z)
        return box(name + " " + label, size, (loc[0] + wx, loc[1] + wy, loc[2] + lz),
                   material, rot=(0, 0, rot_z), bevel=bevel)

    part("back", (w, 0.03, h), 0, d / 2 - 0.02, h / 2, p["oak_dark"])
    for i in (-1, 1):
        part("side", (0.04, d, h), i * (w / 2), 0, h / 2, p["oak"])
    for k in range(4):
        z = 0.06 + k * 0.42
        part("shelf", (w, d, 0.035), 0, 0, z, p["oak"])
        x = -w / 2 + 0.08
        idx = 0
        while x < w / 2 - 0.1:
            bw = 0.035 + 0.015 * ((idx + k) % 3)
            bh = 0.22 + 0.06 * ((idx + k) % 4)
            color = ["terracotta", "sage", "cream_deep", "charcoal", "oak_dark"][(idx + k) % 5]
            part("book", (bw, 0.18, bh), x, 0, z + bh / 2 + 0.02, p[color])
            x += bw + 0.012
            idx += 1


def armchair(name, loc, rot_z, p):
    def part(label, size, lx, ly, lz, material, tilt=0.0, bevel=0.0):
        wx, wy = rot_xy(lx, ly, rot_z)
        return box(name + " " + label, size, (loc[0] + wx, loc[1] + wy, lz),
                   material, rot=(tilt, 0, rot_z), bevel=bevel)

    # 450 mm seat top, 580 mm seat depth, 880 mm overall width, 870 mm back top
    part("seat", (0.64, 0.58, 0.14), 0, 0, 0.38, p["linen"], bevel=0.05)
    part("back", (0.64, 0.12, 0.42), 0, 0.24, 0.66, p["linen"], tilt=math.radians(-10), bevel=0.05)
    part("cushion", (0.50, 0.12, 0.32), 0, 0.14, 0.60, p["sage"], tilt=math.radians(-12), bevel=0.06)
    for i in (-1, 1):
        part("arm", (0.12, 0.62, 0.20), i * 0.34, 0, 0.53, p["cream_deep"], bevel=0.04)
    for lx, ly in [(-0.25, -0.21), (0.25, -0.21), (-0.25, 0.21), (0.25, 0.21)]:
        wx, wy = rot_xy(lx, ly, rot_z)
        cyl(name + " leg", 0.024, 0.31, (loc[0] + wx, loc[1] + wy, 0.155), p["oak_dark"], vertices=20)


def rug(name, loc, w, d, material, z=0.008):
    box(name, (w, d, 0.015), (loc[0], loc[1], z), material, bevel=0.004)


def setup_render(cam_loc, cam_target, lens, path, samples=64):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 8
    scene.cycles.diffuse_bounces = 4
    scene.cycles.glossy_bounces = 4
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.filepath = path
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.exposure = -0.9
    try:
        scene.view_settings.look = "AgX - Medium High Contrast"
    except Exception:
        pass
    cam = camera(cam_loc, cam_target, lens)
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = (Vector(cam_target) - Vector(cam_loc)).length
    cam.data.dof.aperture_fstop = 7.1
    world = bpy.data.worlds.new("World")
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = srgb("#d9cdbb")
    bg.inputs[1].default_value = 0.6
    scene.world = world
    sun_data = bpy.data.lights.new("Sun", "SUN")
    sun_data.energy = 2.2
    sun_data.angle = math.radians(2.0)
    sun_data.color = (1.0, 0.95, 0.86)
    sun = bpy.data.objects.new("Sun", sun_data)
    bpy.context.collection.objects.link(sun)
    sun.location = (cam_loc[0] + 0.6, cam_loc[1] - 1.8, cam_loc[2] + 2.2)
    look_at(sun, cam_target)


def room(w, d, p):
    plane("Floor", (w, d), (0, 0, 0), p["floor"])
    box("Back wall", (w, 0.12, 2.9), (0, d / 2, 1.45), p["cream"])
    box("Side wall", (0.12, d, 2.9), (-w / 2, 0, 1.45), p["cream"])
    box("Ceiling", (w, d, 0.08), (0, 0, 2.86), p["white"])


def window(name, loc, w, h, p):
    face = loc[1]
    # pane reads as "outside": soft daylight above, muted greenery below
    box(name + " sky", (w, 0.02, h * 0.62), (loc[0], face - 0.02, loc[2] + h * 0.19), p["glass"])
    box(name + " outside", (w, 0.02, h * 0.38), (loc[0], face - 0.019, loc[2] - h * 0.31), p["outside"])
    box(name + " frame top", (w + 0.12, 0.09, 0.09), (loc[0], face - 0.05, loc[2] + h / 2), p["oak_dark"])
    box(name + " frame bottom", (w + 0.12, 0.09, 0.09), (loc[0], face - 0.05, loc[2] - h / 2), p["oak_dark"])
    box(name + " sill", (w + 0.22, 0.14, 0.05), (loc[0], face - 0.08, loc[2] - h / 2 - 0.05), p["cream"])
    for i in (-1, 1):
        box(name + " frame side", (0.09, 0.09, h + 0.09), (loc[0] + i * w / 2, face - 0.05, loc[2]), p["oak_dark"])
    box(name + " mullion", (0.05, 0.07, h), (loc[0], face - 0.05, loc[2]), p["oak_dark"])


def reading_nook():
    clear()
    p = palette()
    room(5.0, 4.0, p)
    rug("Rug", (-0.5, 0.15), 2.6, 2.0, p["cream_deep"])
    window("Window", (0.9, 1.94, 1.7), 1.7, 1.7, p)
    area("Window key", (0.9, 1.75, 1.9), (0.0, -0.2, 0.9), 480, 2.4, (1.0, 0.9, 0.78))
    area("Fill", (-1.0, -1.2, 2.5), (0.2, 0.6, 0.8), 120, 3.0, (1.0, 0.95, 0.9))
    point("Warm corner", (-1.85, -0.25, 1.5), 60, (1.0, 0.72, 0.45), 0.1)

    armchair("Chair", (-1.15, 0.35), math.radians(28), p)
    rug("Chair throw", (-1.15, 0.35), 1.5, 1.3, p["sage"], z=0.024)

    # 545 mm side table, 450 mm top, within arm's reach of the chair
    cyl("Table top", 0.225, 0.035, (-0.55, 0.55, 0.5275), p["oak"])
    cyl("Table stem", 0.03, 0.48, (-0.55, 0.55, 0.27), p["brass"])
    cyl("Table base", 0.14, 0.025, (-0.55, 0.55, 0.0125), p["brass"])
    sprig("Table sprig", (-0.55, 0.55, 0.545), 0.85, p)

    cyl("Lamp pole", 0.016, 1.55, (-1.85, -0.25, 0.775), p["charcoal"])
    cone("Lamp shade", 0.22, 0.11, 0.3, (-1.85, -0.25, 1.58), p["lamp"])
    point("Lamp light", (-1.85, -0.25, 1.48), 60, (1.0, 0.68, 0.4), 0.12)
    cyl("Lamp base", 0.15, 0.025, (-1.85, -0.25, 0.0125), p["charcoal"])

    bookshelf("Shelf", (-2.26, 0.4, 0.0), math.radians(90), p)
    plant("Plant", (2.05, 1.5, 0.0), 1.35, p)
    art_frame("Art A", (-1.55, 1.925, 1.5), (0, 0, 0), 0.55, 0.7, p["art1"], p, wall_y=1.907)
    box("Art C frame", (0.42, 0.03, 0.52), (1.9, 1.925, 1.5), p["oak_dark"])
    box("Art C canvas", (0.36, 0.012, 0.46), (1.9, 1.907, 1.5), p["art2"])

    setup_render((3.9, -3.1, 1.65), (-0.35, 0.35, 1.05), 33,
                 os.path.join(RENDERS, "reading-nook.png"))


def dining_corner():
    clear()
    p = palette()
    room(5.0, 4.2, p)
    rug("Dining rug", (0.0, 0.15), 2.8, 2.2, p["cream_deep"])
    window("Window", (0.6, 2.04, 1.7), 1.7, 1.7, p)
    area("Window key", (0.6, 1.85, 1.9), (0.0, -0.2, 0.9), 520, 2.4, (1.0, 0.9, 0.78))
    area("Fill", (-1.4, -1.4, 2.5), (0.3, 0.5, 0.8), 110, 3.0, (1.0, 0.95, 0.9))
    point("Pendant light", (0.0, 0.15, 1.55), 85, (1.0, 0.72, 0.45), 0.15)

    # 1800 x 900 mm table, 750 mm top; seats 450 mm -> 300 mm thigh clearance
    box("Table top", (1.8, 0.9, 0.06), (0.0, 0.15, 0.72), p["oak"], bevel=0.01)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl("Table leg", 0.035, 0.69, (sx * 0.75, 0.15 + sy * 0.31, 0.345), p["oak_dark"])
    # chairs at 450 mm, 190 mm back offset, 900 mm pull-out behind
    for i, (x, y, rz) in enumerate([(-0.6, -0.55, 0), (0.6, -0.55, 0), (-0.6, 0.85, 180), (0.6, 0.85, 180)]):
        box("Chair seat %d" % i, (0.44, 0.44, 0.05), (x, y, 0.425), p["oak"], rot=(0, 0, math.radians(rz)), bevel=0.01)
        box("Chair back %d" % i, (0.44, 0.05, 0.45), (x, y + (-0.19 if rz == 0 else 0.19), 0.675), p["oak"], rot=(0, 0, math.radians(rz)), bevel=0.01)
        for lx, ly in [(-0.18, -0.18), (0.18, -0.18), (-0.18, 0.18), (0.18, 0.18)]:
            cyl("Chair leg %d" % i, 0.017, 0.45, (x + lx, y + ly, 0.225), p["oak_dark"], vertices=20)

    # pendant 750 mm above the tabletop, shade about half the table width
    cyl("Pendant cord", 0.008, 1.14, (0.0, 0.15, 2.29), p["charcoal"])
    cone("Pendant shade", 0.22, 0.09, 0.22, (0.0, 0.15, 1.61), p["lamp"])

    sprig("Table sprig", (0.0, 0.15, 0.75), 1.1, p)

    box("Sideboard", (1.4, 0.4, 0.62), (-1.62, 1.82, 0.31), p["oak"], bevel=0.015)
    box("Sideboard top", (1.44, 0.44, 0.03), (-1.62, 1.82, 0.635), p["oak_dark"])
    cyl("Bowl", 0.12, 0.08, (-1.3, 1.82, 0.68), p["cream"])
    plant("Plant", (2.05, 1.55, 0.0), 1.25, p)

    box("Art frame", (0.9, 0.035, 0.6), (1.5, 2.022, 1.5), p["oak_dark"])
    box("Art canvas", (0.82, 0.012, 0.52), (1.5, 2.004, 1.5), p["art2"])

    setup_render((3.95, -3.2, 1.68), (-0.15, 0.2, 1.05), 35,
                 os.path.join(RENDERS, "dining-corner.png"))


def living_room():
    clear()
    p = palette()
    room(5.2, 4.2, p)
    rug("Living rug", (-0.45, 0.55), 3.4, 2.6, p["cream_deep"])
    window("Window", (1.45, 2.04, 1.7), 1.4, 1.7, p)
    area("Window key", (1.45, 1.85, 1.9), (0.0, -0.1, 0.9), 540, 2.2, (1.0, 0.9, 0.78))
    area("Fill", (-1.7, -1.5, 2.5), (0.4, 0.6, 0.9), 120, 3.2, (1.0, 0.95, 0.9))
    point("Floor lamp light", (2.05, 1.65, 1.5), 55, (1.0, 0.7, 0.45), 0.1)

    # 2.1 m three-seat sofa: 900 mm deep, 450 mm seat top, 910 mm back
    box("Sofa base", (2.1, 0.9, 0.34), (-0.45, 1.35, 0.17), p["cream_deep"], bevel=0.04)
    for sx in (-1, 1):
        box("Sofa arm", (0.16, 0.9, 0.32), (-0.45 + sx * 0.97, 1.35, 0.50), p["cream_deep"], bevel=0.05)
    box("Sofa back", (2.1, 0.18, 0.62), (-0.45, 1.71, 0.60), p["cream_deep"], bevel=0.05)
    for i, dx in enumerate((-0.445, 0.445)):
        box("Sofa cushion %d" % i, (0.86, 0.62, 0.11), (-0.45 + dx, 1.24, 0.395), p["linen"], bevel=0.05)
    for i, dx in enumerate((-0.70, 0.0, 0.70)):
        box("Sofa pillow %d" % i, (0.34, 0.12, 0.34), (-0.45 + dx, 1.56, 0.55), p["sage"],
            rot=(math.radians(-8), 0, 0), bevel=0.06)

    # coffee table 400 mm high, 450 mm clear of the sofa, 900 mm walkway beyond
    box("Coffee top", (1.1, 0.6, 0.05), (-0.45, 0.15, 0.375), p["oak"], bevel=0.01)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl("Coffee leg", 0.035, 0.35, (-0.45 + sx * 0.48, 0.15 + sy * 0.24, 0.175),
                p["oak_dark"], vertices=20)
    box("Books", (0.28, 0.20, 0.04), (-0.72, 0.10, 0.42), p["terracotta"])
    box("Books two", (0.24, 0.17, 0.03), (-0.71, 0.11, 0.455), p["sage"], rot=(0, 0, math.radians(8)))
    cyl("Bowl", 0.10, 0.07, (-0.10, 0.18, 0.435), p["cream"])

    armchair("Armchair", (1.55, 0.55), math.radians(-120), p)
    cyl("Side table top", 0.20, 0.03, (1.55, -0.30, 0.49), p["oak"])
    cyl("Side table stem", 0.025, 0.46, (1.55, -0.30, 0.245), p["brass"])
    cyl("Side table base", 0.13, 0.02, (1.55, -0.30, 0.01), p["brass"])

    cyl("Floor lamp pole", 0.016, 1.55, (2.05, 1.65, 0.775), p["charcoal"])
    cone("Floor lamp shade", 0.22, 0.11, 0.30, (2.05, 1.65, 1.58), p["lamp"])
    cyl("Floor lamp base", 0.15, 0.025, (2.05, 1.65, 0.0125), p["charcoal"])

    plant("Plant", (-2.20, 1.62, 0.0), 1.3, p)
    # artwork centred at 1.5 m, the hanging height at eye level
    box("Art frame", (1.25, 0.03, 0.72), (-0.45, 2.025, 1.52), p["oak_dark"])
    box("Art canvas", (1.19, 0.012, 0.66), (-0.45, 2.007, 1.52), p["art1"])

    setup_render((3.75, -3.35, 1.62), (-0.40, 0.55, 0.90), 32,
                 os.path.join(RENDERS, "oak-and-light.png"))


def quiet_quarters():
    clear()
    p = palette()
    room(4.4, 4.2, p)
    rug("Bedroom rug", (0.2, 0.45), 2.8, 2.0, p["cream_deep"])
    window("Window", (1.70, 2.04, 1.70), 0.9, 1.3, p)
    area("Window key", (1.20, 1.85, 1.7), (0.0, -0.1, 1.0), 420, 2.0, (1.0, 0.9, 0.78))
    area("Fill", (-1.6, -1.4, 2.5), (0.4, 0.6, 0.9), 125, 3.2, (1.0, 0.95, 0.9))
    point("Bedside glow", (1.34, 1.75, 0.78), 45, (1.0, 0.7, 0.45), 0.1)

    # 1.6 x 2.0 m bed, 540 mm mattress top, 600 mm clear at both sides
    box("Bed frame", (1.70, 2.00, 0.30), (0.20, 1.00, 0.17), p["oak_dark"], bevel=0.02)
    box("Mattress", (1.60, 1.94, 0.22), (0.20, 1.00, 0.43), p["linen"], bevel=0.03)
    box("Duvet", (1.62, 1.45, 0.10), (0.20, 0.72, 0.55), p["white"], bevel=0.03)
    box("Duvet fold", (1.62, 0.35, 0.09), (0.20, 1.42, 0.58), p["cream_deep"], bevel=0.03)
    for i, dx in enumerate((-0.40, 0.40)):
        box("Pillow %d" % i, (0.62, 0.36, 0.16), (0.20 + dx, 1.72, 0.66), p["white"],
            rot=(math.radians(-14), 0, 0), bevel=0.06)
    for i in range(9):
        box("Headboard slat %d" % i, (0.07, 0.03, 1.00), (-0.62 + i * 0.205, 1.96, 0.62), p["oak"])
    box("Headboard rail", (1.80, 0.06, 1.10), (0.20, 2.005, 0.63), p["oak_dark"], bevel=0.01)

    # 450 x 400 mm nightstands, 500 mm high, within reach of the mattress
    for i, x in enumerate((-0.94, 1.34)):
        box("Nightstand %d" % i, (0.45, 0.40, 0.50), (x, 1.75, 0.25), p["oak"], bevel=0.015)
        cyl("Bedside lamp base %d" % i, 0.05, 0.03, (x, 1.75, 0.515), p["brass"])
        cyl("Bedside lamp stem %d" % i, 0.012, 0.24, (x, 1.75, 0.64), p["brass"])
        cone("Bedside shade %d" % i, 0.13, 0.07, 0.18, (x, 1.75, 0.85), p["lamp"])

    # 600 mm deep sliding wardrobe on the left wall, 1.2 m clear of the bed
    box("Wardrobe", (0.60, 1.80, 2.20), (-1.835, 0.55, 1.10), p["oak"], bevel=0.01)
    box("Wardrobe door A", (0.03, 0.88, 2.15), (-1.525, 0.10, 1.10), p["oak_dark"])
    box("Wardrobe door B", (0.03, 0.88, 2.15), (-1.520, 0.99, 1.10), p["oak_dark"])
    for i, y in enumerate((0.50, 0.59)):
        box("Wardrobe handle %d" % i, (0.02, 0.02, 0.34), (-1.500, y, 1.10), p["brass"])

    box("Bench cushion", (1.20, 0.40, 0.12), (0.20, -0.55, 0.39), p["sage"], bevel=0.03)
    for i, (dx, dy) in enumerate(((-0.52, -0.14), (0.52, -0.14), (-0.52, 0.14), (0.52, 0.14))):
        cyl("Bench leg %d" % i, 0.02, 0.33, (0.20 + dx, -0.55 + dy, 0.165),
            p["oak_dark"], vertices=16)

    plant("Plant", (-1.75, -1.55, 0.0), 1.15, p)
    setup_render((3.40, -3.35, 1.55), (0.0, 0.75, 0.95), 30,
                 os.path.join(RENDERS, "quiet-quarters.png"))


def warm_kitchen():
    clear()
    p = palette()
    room(4.8, 3.8, p)
    window("Window", (0.85, 1.84, 1.75), 0.9, 0.9, p)
    area("Window key", (0.85, 1.70, 1.8), (0.1, 0.0, 0.9), 480, 2.0, (1.0, 0.9, 0.78))
    area("Fill", (-1.6, -1.6, 2.5), (0.4, 0.5, 0.9), 115, 3.0, (1.0, 0.95, 0.9))
    point("Island light", (0.50, -0.32, 1.72), 75, (1.0, 0.72, 0.45), 0.18)

    # 900 mm worktops, 600 mm deep; work triangle about 1.6 / 1.5 / 2.7 m
    box("Base run", (4.40, 0.60, 0.85), (0.0, 1.52, 0.425), p["oak"], bevel=0.01)
    box("Worktop run", (4.50, 0.62, 0.05), (0.0, 1.51, 0.875), p["counter"], bevel=0.005)
    box("Upstand", (4.50, 0.03, 0.10), (0.0, 1.82, 0.95), p["counter"])

    box("Fridge", (0.70, 0.68, 1.95), (-1.75, 1.44, 0.975), p["appliance"], bevel=0.02)
    box("Fridge seam", (0.66, 0.01, 0.02), (-1.75, 1.095, 1.26), p["charcoal"])
    box("Fridge handle", (0.03, 0.04, 0.50), (-1.47, 1.09, 1.55), p["brass"])

    box("Range", (0.62, 0.62, 0.90), (-0.10, 1.50, 0.45), p["charcoal"], bevel=0.01)
    box("Cooktop", (0.60, 0.50, 0.02), (-0.10, 1.52, 0.905), p["charcoal"])
    for i, (dx, dy) in enumerate(((-0.16, -0.12), (0.16, -0.12), (-0.16, 0.12), (0.16, 0.12))):
        cyl("Burner %d" % i, 0.07, 0.015, (-0.10 + dx, 1.52 + dy, 0.922),
            p["oak_dark"], vertices=20)
    box("Oven door", (0.56, 0.02, 0.42), (-0.10, 1.185, 0.42), p["oak_dark"])
    box("Oven handle", (0.50, 0.03, 0.03), (-0.10, 1.16, 0.66), p["brass"])

    box("Sink", (0.56, 0.42, 0.16), (0.95, 1.51, 0.82), p["charcoal"])
    cyl("Tap", 0.015, 0.30, (0.95, 1.74, 1.03), p["brass"], vertices=16)
    cyl("Tap spout", 0.012, 0.20, (0.95, 1.65, 1.16), p["brass"],
        rot=(math.radians(90), 0, 0), vertices=16)

    box("Hood", (0.60, 0.45, 0.18), (-0.10, 1.58, 1.75), p["appliance"], bevel=0.02)
    box("Hood chimney", (0.22, 0.22, 0.92), (-0.10, 1.70, 2.30), p["appliance"])
    box("Upper cabinet L", (1.20, 0.35, 0.72), (-1.55, 1.66, 1.86), p["oak"], bevel=0.01)
    box("Upper cabinet R", (0.40, 0.35, 0.72), (1.65, 1.66, 1.86), p["oak"], bevel=0.01)

    # 2.2 x 0.9 m island, 900 mm top, 1.1 m aisle to the back run
    box("Island base", (2.20, 0.90, 0.85), (0.50, -0.32, 0.425), p["oak"], bevel=0.01)
    box("Island top", (2.30, 1.00, 0.06), (0.50, -0.32, 0.88), p["counter"], bevel=0.01)
    cyl("Island bowl", 0.14, 0.08, (0.30, -0.32, 0.95), p["terracotta"])
    box("Cutting board", (0.42, 0.28, 0.03), (1.05, -0.28, 0.925), p["oak_dark"])

    # counter stools at 650 mm seat height
    for i, x in enumerate((-0.05, 0.50, 1.05)):
        cyl("Stool seat %d" % i, 0.17, 0.05, (x, -1.08, 0.625), p["oak"], vertices=24)
        for lx, ly in ((-0.11, -0.11), (0.11, -0.11), (-0.11, 0.11), (0.11, 0.11)):
            cyl("Stool leg %d" % i, 0.012, 0.60, (x + lx, -1.08 + ly, 0.30),
                p["charcoal"], vertices=12)
        box("Stool back %d" % i, (0.30, 0.03, 0.22), (x, -1.24, 0.80), p["oak"], bevel=0.01)

    # pendants 750 mm above the island top
    for i, x in enumerate((-0.05, 0.50, 1.05)):
        cyl("Pendant cord %d" % i, 0.006, 1.02, (x, -0.32, 2.35), p["charcoal"], vertices=12)
        cone("Pendant shade %d" % i, 0.15, 0.05, 0.18, (x, -0.32, 1.75), p["lamp"])

    plant("Herb pot", (1.9, 1.51, 0.90), 0.6, p)
    setup_render((3.30, -3.30, 1.70), (0.15, 0.55, 1.00), 30,
                 os.path.join(RENDERS, "warm-kitchen.png"))


ROOMS = [
    ("reading-nook", reading_nook),
    ("dining-corner", dining_corner),
    ("oak-and-light", living_room),
    ("quiet-quarters", quiet_quarters),
    ("warm-kitchen", warm_kitchen),
]

for name, build in ROOMS:
    only = [s for s in os.environ.get("ROOMS_ONLY", "").split(",") if s]
    if only and name not in only:
        continue
    build()
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "blender", name + ".blend"))
    bpy.ops.render.render(write_still=True)
    print("Rendered", name)
