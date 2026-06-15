"""Bamboo (Guadua/Chusquea) — clumping along stream, NOT running."""
from __future__ import annotations

import math
import random

import bpy
import mathutils

from ..materials import MAT, assign


def _anchor_origin_at_base(obj, base_world):
    """Move object origin to a world-space point. Used so culm leans pivot from
    the rhizome, not the midpoint — without this the clump looks like X-shaped
    crossed sticks instead of a fan."""
    scene = bpy.context.scene
    prev_cursor = tuple(scene.cursor.location)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    scene.cursor.location = base_world
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    scene.cursor.location = prev_cursor


def add_bamboo_clump(x, y, n=18, scale=1.0):
    """Guadua angustifolia clumping bamboo.

    Each culm is a tapered cone (8-15 cm base → ~50% of that at the tip) with
    shader-driven dark node rings every 30 cm. Multi-age height distribution:
    mostly mature 8-14 m culms, some adolescent 4-7 m, occasional 2-3 m new
    shoots (leafless). Lanceolate leaf clusters in the upper crown — many small
    flat leaves per cluster instead of one icosphere "blob" — so the silhouette
    reads as foliage rather than beads on a stick.

    Culms are base-anchored (origin at z=0) and leaned outward from the clump
    centre to produce the characteristic Guadua fan.
    """
    parts = []
    for _ in range(n):
        # Multi-age distribution: 75% mature, 23% adolescent, 2% new shoot.
        # New-shoot probability dropped from 5% — leafless 2-3 m culms read as
        # ivory dashes at the clump edge and clutter the hero silhouette.
        r = random.random()
        if r < 0.75:
            h = random.uniform(8.0, 14.0) * scale
            r_base = random.uniform(0.045, 0.060) * scale
            mature = True
        elif r < 0.98:
            h = random.uniform(4.0, 7.0) * scale
            r_base = random.uniform(0.032, 0.045) * scale
            mature = True
        else:
            h = random.uniform(2.0, 3.0) * scale
            r_base = random.uniform(0.022, 0.032) * scale
            mature = False  # new shoots haven't leafed yet
        r_tip = r_base * random.uniform(0.45, 0.60)

        # Clamp to ±1.2 m / σ=0.55: tighter than v3 (±1.6 / 0.75). The 50 mm
        # lens at 14 m distance frames ~10 m wide, so ±1.2 m keeps the clump
        # to ~24% of frame width — reads as one cohesive Guadua stand.
        ox = x + max(-1.2, min(1.2, random.gauss(0.0, 0.55))) * scale
        oy = y + max(-1.2, min(1.2, random.gauss(0.0, 0.55))) * scale

        # Radial outward lean for fan silhouette + small random jitter.
        dx, dy = ox - x, oy - y
        rad_dist = math.hypot(dx, dy)
        if rad_dist > 1e-4:
            ang = math.atan2(dy, dx)
        else:
            ang = random.uniform(0.0, math.tau)
        outward = random.uniform(0.06, 0.14)
        # rotation_euler.x tilts +Z toward -Y (RHS), rotation_euler.y tilts toward +X.
        lean_y = math.cos(ang) * outward + random.uniform(-0.04, 0.04)
        lean_x = -math.sin(ang) * outward + random.uniform(-0.04, 0.04)

        bpy.ops.mesh.primitive_cone_add(
            radius1=r_base, radius2=r_tip, depth=h,
            vertices=12, location=(ox, oy, h / 2),
        )
        c = bpy.context.active_object
        c.name = 'BambooCulm'
        _anchor_origin_at_base(c, (ox, oy, 0.0))
        c.rotation_euler = (lean_x, lean_y, 0.0)
        assign(c, MAT['bamboo_culm'])
        parts.append(c)

        if not mature:
            continue

        # Build the culm's actual local→world rotation so leaf positions track
        # the lean exactly. The approximate `sin(lean)*lz` form leaked leaves
        # 20-40 cm sideways at 12 m height — read as floating debris.
        rot = mathutils.Euler((lean_x, lean_y, 0.0), 'XYZ').to_matrix()
        base_world = mathutils.Vector((ox, oy, 0.0))

        # Lanceolate leaf clusters in the upper crown — ~6-8 clusters per
        # culm, each ~18-24 leaves packed tight (±0.14 m radial). Density per
        # mature culm ~110-190; per clump (n=20) ~2k-3k leaves. Cycles CPU
        # eats that in ~30-40 s at 720p.
        n_clusters = random.randint(6, 8)
        for j in range(n_clusters):
            t = 0.55 + (j / max(n_clusters - 1, 1)) * 0.42  # 0.55–0.97
            lz = h * t
            cluster_world = base_world + rot @ mathutils.Vector((0.0, 0.0, lz))

            n_leaves = random.randint(18, 24)
            for _ in range(n_leaves):
                # Leaf jitter in CULM-LOCAL coords, then rotated into world —
                # keeps the cluster tied to the culm axis even at extreme lean.
                local_off = mathutils.Vector((
                    random.uniform(-0.14, 0.14) * scale,
                    random.uniform(-0.14, 0.14) * scale,
                    random.uniform(-0.10, 0.10) * scale,
                ))
                lp = cluster_world + rot @ local_off
                bpy.ops.mesh.primitive_ico_sphere_add(
                    radius=0.22 * scale,
                    location=tuple(lp),
                    subdivisions=2,
                )
                leaf = bpy.context.active_object
                leaf.name = 'BambooLeaf'
                # Lanceolate aspect: long along Y, narrow X, very thin Z.
                leaf.scale = (0.28, 1.0, 0.06)
                leaf.rotation_euler = (
                    random.uniform(-0.55, 0.55),
                    random.uniform(-0.55, 0.55),
                    random.uniform(0.0, math.tau),
                )
                bpy.ops.object.transform_apply(scale=True, rotation=True)
                assign(leaf, MAT['bamboo_leaf'])
                parts.append(leaf)
    return parts


def scatter_grass_tufts(n=80, x_range=(-18.0, 22.0), y_range=(-26.0, 4.0)):
    """Small grass tufts to break up the barren laterite foreground.

    Each tuft is a tiny cluster of squashed icospheres at slight z jitter so
    the silhouette reads as a clump rather than a single bead. Density biases
    toward the hero foreground (south of y=-10) and toward bamboo culm bases.
    """
    parts = []
    bamboo_bases = [(7.5, -4), (14.5, -3), (8.0, -14), (15.0, -10), (17.5, -16)]
    for _ in range(n):
        r = random.random()
        if r < 0.35:
            # Cluster around a bamboo base — Work 7 satisfied here too
            bx, by = random.choice(bamboo_bases)
            x = bx + random.gauss(0, 0.8)
            y = by + random.gauss(0, 0.8)
        elif r < 0.75:
            # Hero foreground laterite
            x = random.uniform(5.0, 20.0)
            y = random.uniform(-25.0, -12.0)
        else:
            x = random.uniform(*x_range)
            y = random.uniform(*y_range)
        # 3–5 little blades per tuft
        for _ in range(random.randint(3, 5)):
            ox = x + random.uniform(-0.12, 0.12)
            oy = y + random.uniform(-0.12, 0.12)
            h = random.uniform(0.10, 0.22)
            bpy.ops.mesh.primitive_ico_sphere_add(
                radius=0.05, location=(ox, oy, h / 2), subdivisions=1,
            )
            blade = bpy.context.active_object
            blade.name = 'GrassTuft'
            blade.scale = (0.35, 0.35, h / 0.05)
            blade.rotation_euler = (
                random.uniform(-0.2, 0.2),
                random.uniform(-0.2, 0.2),
                random.uniform(0, math.tau),
            )
            bpy.ops.object.transform_apply(scale=True, rotation=True)
            assign(blade, MAT['grass_blade'])
            parts.append(blade)
    return parts
