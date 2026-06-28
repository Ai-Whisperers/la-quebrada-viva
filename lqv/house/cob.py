"""Sculpted U-plan cob house with interior courtyard and lapacho-timber corredor."""
from __future__ import annotations

import math
import random

import bmesh
import bpy

from ..geometry import new_object_from_bmesh
from ..materials import MAT, assign

# Module-level so build_window_emission can reuse the same coordinates as the
# Boolean cutouts. (x, y, z, sx, sy, sz, normal_axis) — normal is the wall axis
# the cutout extends through.
WINDOW_SPECS = [
    (-4.0, -2.25, 2.1, 1.0, 1.4, 1.2, 'y'),  # south wall, west arm (faces corredor)
    ( 4.0, -2.25, 2.1, 1.0, 1.4, 1.2, 'y'),  # south wall, east arm (faces corredor)
    ( 6.25, 2.0, 2.1, 1.4, 1.0, 1.2, 'x'),   # east external wall, mid-arm
    (-6.25, 2.0, 2.1, 1.4, 1.0, 1.2, 'x'),   # west external wall, mid-arm
]


def build_cob_house():
    """U-shaped sculpted cob house on the upper terrace platform.

    Footprint (in metres, origin = approximate centroid):
        - Two long arms running east-west, 12 m long, 4 m wide
        - Connected by a south wing 10 m wide × 4 m deep
        - Opens north (toward escarpment), creating a U whose courtyard faces
          the escarpment for cool-air drainage intake
        - Wall height 2.7 m above the 0.6 m raised stone foundation
    """
    foundation_h = 0.6
    wall_h = 2.7
    wall_thick = 0.5

    objs = []

    # ---- Raised stone foundation perimeter ----
    # Rule 1 (no right angles in cob walls): build the U as a wobbled, rounded
    # polyline traced around the sharp-cornered control points below. Each sharp
    # corner is replaced by a quarter-arc with small jitter so the wall outline
    # reads as a hand-built sculpted blob rather than a CAD rectangle.
    corner_control = [
        (-6.0, -2.0), (-6.0, 6.0), (-2.0, 6.0), (-2.0, 0.0),
        (2.0, 0.0),   (2.0, 6.0),  (6.0, 6.0),  (6.0, -2.0),
    ]

    def _round_polyline(corners, corner_radius=0.8, arc_segments=5, edge_segments=6, wobble=0.06,
                        undulate_amp=0.0, undulate_freq=2.0):
        """Trace a closed polyline with rounded corners and slight outward jitter.
        Concave vs convex corners are detected via signed cross-product so the
        notch at (-2,0) / (2,0) of the U-plan rounds inward smoothly.

        undulate_amp adds a low-frequency outward swell along the perimeter — dissolves
        the perception of a polygon into a sculpted blob. Applied after wobble so the
        two stack: low-freq swell + per-vertex jitter."""
        n = len(corners)
        pts = []
        # Determine overall winding to know what "convex" means for this polygon
        signed_area = 0.0
        for i in range(n):
            x1, y1 = corners[i]
            x2, y2 = corners[(i + 1) % n]
            signed_area += (x2 - x1) * (y2 + y1)
        cw = signed_area > 0
        for i in range(n):
            prev = corners[(i - 1) % n]
            cur = corners[i]
            nxt = corners[(i + 1) % n]
            # Vectors along the two edges meeting at this corner
            v1x, v1y = cur[0] - prev[0], cur[1] - prev[1]
            v2x, v2y = nxt[0] - cur[0], nxt[1] - cur[1]
            l1 = math.hypot(v1x, v1y) or 1.0
            l2 = math.hypot(v2x, v2y) or 1.0
            u1x, u1y = v1x / l1, v1y / l1
            u2x, u2y = v2x / l2, v2y / l2
            # Corner points: pull back from cur along incoming edge, then forward along outgoing
            start = (cur[0] - u1x * corner_radius, cur[1] - u1y * corner_radius)
            end = (cur[0] + u2x * corner_radius, cur[1] + u2y * corner_radius)
            # Determine concavity: cross product of (v1 → v2)
            cross = v1x * v2y - v1y * v2x
            concave = (cross > 0) if cw else (cross < 0)
            # Arc centre: perpendicular offset from `cur` by corner_radius along the
            # inward bisector (concave) or outward bisector (convex)
            bx = -u1y - (-u2y)
            by = u1x - u2x
            bl = math.hypot(bx, by) or 1.0
            bx, by = bx / bl, by / bl
            if not cw:
                bx, by = -bx, -by
            sign = 1.0 if concave else -1.0
            cx = cur[0] + bx * corner_radius * sign
            cy = cur[1] + by * corner_radius * sign
            a_start = math.atan2(start[1] - cy, start[0] - cx)
            a_end = math.atan2(end[1] - cy, end[0] - cx)
            # Pick the shorter sweep direction
            da = a_end - a_start
            while da > math.pi:
                da -= math.tau
            while da < -math.pi:
                da += math.tau
            # Emit straight-edge interpolation from previous corner's `end` to this `start`
            if pts:
                prev_end = pts[-1]
                for k in range(1, edge_segments):
                    t = k / edge_segments
                    ex = prev_end[0] + (start[0] - prev_end[0]) * t
                    ey = prev_end[1] + (start[1] - prev_end[1]) * t
                    ex += random.uniform(-wobble, wobble)
                    ey += random.uniform(-wobble, wobble)
                    pts.append((ex, ey))
            pts.append(start)
            for k in range(1, arc_segments):
                t = k / arc_segments
                a = a_start + da * t
                ax = cx + corner_radius * math.cos(a) + random.uniform(-wobble, wobble)
                ay = cy + corner_radius * math.sin(a) + random.uniform(-wobble, wobble)
                pts.append((ax, ay))
            pts.append(end)
        # Close: edge from last end back to first start
        first = pts[0]
        last = pts[-1]
        for k in range(1, edge_segments):
            t = k / edge_segments
            ex = last[0] + (first[0] - last[0]) * t
            ey = last[1] + (first[1] - last[1]) * t
            ex += random.uniform(-wobble, wobble)
            ey += random.uniform(-wobble, wobble)
            pts.append((ex, ey))
        if undulate_amp > 0.0:
            cx = sum(p[0] for p in corners) / len(corners)
            cy = sum(p[1] for p in corners) / len(corners)
            swelled = []
            phase = random.uniform(0.0, math.tau)
            for px, py in pts:
                dx, dy = px - cx, py - cy
                dist = math.hypot(dx, dy) or 1.0
                nx, ny = dx / dist, dy / dist
                theta = math.atan2(dy, dx)
                swell = math.sin(theta * undulate_freq + phase) * undulate_amp
                swelled.append((px + nx * swell, py + ny * swell))
            pts = swelled
        return pts

    foundation_points = _round_polyline(
        corner_control, corner_radius=1.6, arc_segments=8, edge_segments=6,
        wobble=0.22, undulate_amp=0.35, undulate_freq=3.0,
    )

    def make_extruded_perimeter(points, name, z_base, height, thick, mat, displace_strength=0.05):
        # Build a closed polyline curve, convert to mesh, give it thickness via solidify,
        # extrude up via screw not appropriate — we'll just build a bmesh directly
        bm = bmesh.new()
        bottom = [bm.verts.new((x, y, z_base)) for x, y in points]
        top = [bm.verts.new((x, y, z_base + height)) for x, y in points]
        n = len(points)
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new([bottom[i], bottom[j], top[j], top[i]])
        bm.normal_update()
        obj = new_object_from_bmesh(name, bm)
        # Solidify outward to give wall thickness
        sol = obj.modifiers.new('Sol', 'SOLIDIFY')
        sol.thickness = thick
        sol.offset = -1.0
        sub = obj.modifiers.new('Sub', 'SUBSURF')
        sub.levels = 3
        sub.render_levels = 4
        tex = bpy.data.textures.new(name + 'Tex', type='CLOUDS')
        tex.noise_scale = 4.0
        disp = obj.modifiers.new('Disp', 'DISPLACE')
        disp.texture = tex
        disp.strength = displace_strength
        smooth = obj.modifiers.new('Smooth', 'SMOOTH')
        smooth.factor = 0.6
        smooth.iterations = 3
        assign(obj, mat)
        return obj

    foundation = make_extruded_perimeter(
        foundation_points, 'Foundation', 0.0, foundation_h, 0.75,
        MAT['sandstone'], displace_strength=0.14,
    )
    objs.append(foundation)

    # ---- Cob walls — same perimeter, on top of the foundation ----
    cob_walls = make_extruded_perimeter(
        foundation_points, 'CobWalls', foundation_h, wall_h, wall_thick,
        MAT['lime_wash'], displace_strength=0.22,
    )
    objs.append(cob_walls)

    # Window openings — Boolean cutouts through the lime-washed cob walls.
    # Cutout extents on the wall-normal axis (1.4m) intentionally exceed
    # wall_thick (0.5) + max displace (0.22) on both sides so the cut clears
    # the displaced surface without leaving slivers. Each opening gets a
    # lapacho-timber sill below it — the most legible vernacular cue for a
    # deep adobe window from the hero camera distance.
    for i, (x, y, z, sx, sy, sz, normal) in enumerate(WINDOW_SPECS):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
        cut = bpy.context.active_object
        cut.name = f'WindowCut_{i}'
        cut.scale = (sx, sy, sz)
        bpy.ops.object.transform_apply(scale=True)
        cut.hide_render = True
        cut.display_type = 'WIRE'
        boolean = cob_walls.modifiers.new(f'WindowBool_{i}', 'BOOLEAN')
        boolean.operation = 'DIFFERENCE'
        boolean.object = cut
        # The EXACT solver misreads the solidified open-ribbon wall (winding/
        # non-manifold) and collapses the mesh to a fragment — walls vanished
        # from renders entirely. FAST is stable here; cut after Solidify but
        # before Subsurf so the opening gets rounded (suits rule 1 anyway).
        boolean.solver = 'FAST'
        cob_walls.modifiers.move(len(cob_walls.modifiers) - 1, 1 + i)
        objs.append(cut)
        sill_z = z - sz / 2 + 0.03
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, sill_z))
        sill = bpy.context.active_object
        sill.name = f'WindowSill_{i}'
        if normal == 'y':
            sill.scale = (0.95, 0.62, 0.06)
        else:
            sill.scale = (0.62, 0.95, 0.06)
        bpy.ops.object.transform_apply(scale=True)
        assign(sill, MAT['lapacho_timber'])
        objs.append(sill)

    # ---- Roof — low-pitched, 90 cm overhang on all sides, lapacho timber + sod ----
    # Rule 5: ≥0.9m overhang past the actual sculpted perimeter. Sample the perimeter
    # to find the real extents (organic blob can push 0.5–0.6m beyond control points).
    perim_min_x = min(p[0] for p in foundation_points) - 0.9
    perim_max_x = max(p[0] for p in foundation_points) + 0.9
    perim_min_y = min(p[1] for p in foundation_points) - 0.9
    perim_max_y = max(p[1] for p in foundation_points) + 0.9
    roof_min_x, roof_max_x = perim_min_x, perim_max_x
    roof_min_y, roof_max_y = perim_min_y, perim_max_y
    roof_z = foundation_h + wall_h
    roof_pitch_h = 0.9  # rise of the low-pitched roof

    bm = bmesh.new()
    # Two-slope (north-south) low pitch — ridge runs east-west across the south wing
    v0 = bm.verts.new((roof_min_x, roof_min_y, roof_z))
    v1 = bm.verts.new((roof_max_x, roof_min_y, roof_z))
    v2 = bm.verts.new((roof_max_x, roof_max_y, roof_z))
    v3 = bm.verts.new((roof_min_x, roof_max_y, roof_z))
    v_ridge_s = bm.verts.new((0.0, roof_min_y + 1.5, roof_z + roof_pitch_h))
    v_ridge_n = bm.verts.new((0.0, roof_max_y - 1.5, roof_z + roof_pitch_h))
    # South slope
    bm.faces.new([v0, v1, v_ridge_s])
    # North slope
    bm.faces.new([v2, v3, v_ridge_n])
    # West slope
    bm.faces.new([v0, v_ridge_s, v_ridge_n, v3])
    # East slope
    bm.faces.new([v1, v2, v_ridge_n, v_ridge_s])
    roof = new_object_from_bmesh('Roof', bm)
    sol = roof.modifiers.new('Sol', 'SOLIDIFY')
    sol.thickness = 0.18
    sol.offset = 1.0
    assign(roof, MAT['sod_canopy'])
    objs.append(roof)

    # Lapacho-timber rafters peeking out below the roof — beams running across the U arms
    for x in (-5.0, -3.0, 3.0, 5.0):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 2.0, roof_z - 0.1))
        beam = bpy.context.active_object
        beam.name = f'Rafter_{x:+.1f}'
        beam.scale = (0.15, 9.5, 0.15)
        bpy.ops.object.transform_apply(scale=True)
        assign(beam, MAT['lapacho_timber'])
        objs.append(beam)

    # ---- Corredor — covered gallery wrapping the south face ----
    # Posts along south frontage at x = -5, -2.5, 0, 2.5, 5
    corredor_z = foundation_h
    # Posts bumped from 0.12 → 0.18 radius — at hero cam distance (~28m, 28mm)
    # the original posts were a 1px sliver and read as cracks rather than columns.
    for x in (-5.5, -3.0, 0.0, 3.0, 5.5):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.18, depth=wall_h, location=(x, -3.5, corredor_z + wall_h / 2),
        )
        post = bpy.context.active_object
        post.name = f'CorredorPost_{x:+.1f}'
        assign(post, MAT['lapacho_timber'])
        objs.append(post)
    # Corredor roof — flat extension of the main roof southward 1.5 m
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -2.75, roof_z))
    cor_roof = bpy.context.active_object
    cor_roof.name = 'CorredorRoof'
    cor_roof.scale = (12.0, 1.5, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    sol = cor_roof.modifiers.new('Sol', 'SOLIDIFY')
    sol.thickness = 0.08
    assign(cor_roof, MAT['lapacho_timber'])
    objs.append(cor_roof)


def build_window_emission(variant: str):
    """Variant C only — glowing planes inside each WINDOW_SPECS opening.

    Reads as warm interior lamps through the cob cutouts. Plane sits at the
    cutout centre (between inner/outer wall faces), sized 0.85× the opening
    so the framing stays legible. Not Boolean-cut by the wall — the wall's
    DIFFERENCE modifier only operates on cob_walls geometry.
    """
    if variant != 'C':
        return []
    objs = []
    for i, (x, y, z, sx, sy, sz, normal) in enumerate(WINDOW_SPECS):
        bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, z))
        plane = bpy.context.active_object
        plane.name = f'WindowGlow_{i}'
        if normal == 'y':
            plane.rotation_euler = (math.radians(90), 0, 0)
            plane.scale = (sx * 0.85, sz * 0.85, 1.0)
        else:
            plane.rotation_euler = (math.radians(90), 0, math.radians(90))
            plane.scale = (sy * 0.85, sz * 0.85, 1.0)
        bpy.ops.object.transform_apply(rotation=True, scale=True)
        assign(plane, MAT['window_glow'])
        objs.append(plane)
    return objs
