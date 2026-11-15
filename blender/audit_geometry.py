"""Geometry QA for the interior scenes: wall clearance, coplanar rugs, art depth."""
import bpy
import os
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOUNDS = {
    "reading-nook": (-2.44, 2.55, -2.08, 1.94),
    "dining-corner": (-2.44, 2.55, -2.08, 2.04),
    "oak-and-light": (-2.54, 2.65, -2.08, 2.04),
    "quiet-quarters": (-2.14, 2.25, -2.08, 2.04),
    "warm-kitchen": (-2.34, 2.45, -1.88, 1.84),
}
WALLS = {"Back wall", "Side wall", "Floor", "Ceiling"}


def wbox(obj):
    pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    return (Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts))),
            Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts))))


def overlap(a, b):
    lo = Vector((max(a[0].x, b[0].x), max(a[0].y, b[0].y), max(a[0].z, b[0].z)))
    hi = Vector((min(a[1].x, b[1].x), min(a[1].y, b[1].y), min(a[1].z, b[1].z)))
    d = hi - lo
    return 0.0 if min(d) <= 0 else d.x * d.y * d.z


for room, (x0, x1, y0, y1) in BOUNDS.items():
    bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "blender", room + ".blend"))
    print("\n==", room, "==")
    walls = {o.name: wbox(o) for o in bpy.data.objects if o.name in WALLS}
    problems = 0
    for o in bpy.data.objects:
        if o.type != "MESH":
            continue
        lo, hi = wbox(o)
        out = []
        if lo.x < x0 - 0.015: out.append("x %.3f" % lo.x)
        if hi.x > x1 + 0.015: out.append("x %.3f" % hi.x)
        if lo.y < y0 - 0.015: out.append("y %.3f" % lo.y)
        if hi.y > y1 + 0.025: out.append("y %.3f" % hi.y)
        if lo.z < -0.015: out.append("z %.3f" % lo.z)
        if out and o.name not in WALLS:
            print("OUTSIDE", o.name, ", ".join(out)); problems += 1
        if o.name not in WALLS:
            for wn, wb in walls.items():
                vol = overlap((lo, hi), wb)
                if vol > 0.0005:
                    print("WALL HIT", o.name, wn, "%.4f m3" % vol); problems += 1
    rugs = [(o.name, wbox(o)) for o in bpy.data.objects if "Rug" in o.name or "throw" in o.name]
    for i in range(len(rugs)):
        for j in range(i + 1, len(rugs)):
            vol = overlap(rugs[i][1], rugs[j][1])
            if vol > 0.00001:
                print("RUG OVERLAP", rugs[i][0], rugs[j][0], "%.5f" % vol); problems += 1
    for o in bpy.data.objects:
        if o.name.startswith("Art") or "Chair back" in o.name:
            lo, hi = wbox(o)
            print("CHECK", o.name, "size", tuple(round(v, 3) for v in (hi - lo)), "y", round(lo.y, 3), "to", round(hi.y, 3))
    print("issues:", problems)
