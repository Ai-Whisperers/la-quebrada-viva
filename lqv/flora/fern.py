"""Tree ferns (Cyathea) — riparian, 2–4 m tall, 1.5 m+ fronds."""
from __future__ import annotations

import math

import bpy

from ..materials import MAT, assign


def add_tree_fern(x, y, scale=1.0):
    trunk_h = 2.8 * scale
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.12 * scale, depth=trunk_h, location=(x, y, trunk_h / 2),
    )
    trunk = bpy.context.active_object
    trunk.name = f'TreeFernTrunk_{x:.1f}_{y:.1f}'
    assign(trunk, MAT['pindo_trunk'])
    # Crown of 6 arching fronds approximated as flattened ellipsoids
    parts = [trunk]
    for i in range(6):
        ang = (i / 6) * math.tau
        end_x = x + math.cos(ang) * 1.3 * scale
        end_y = y + math.sin(ang) * 1.3 * scale
        bpy.ops.mesh.primitive_ico_sphere_add(
            radius=0.4 * scale, location=(end_x, end_y, trunk_h + 0.1), subdivisions=2,
        )
        f = bpy.context.active_object
        f.name = 'FernFrond'
        f.scale = (2.0, 0.25, 0.15)
        f.rotation_euler = (0, math.radians(-15), ang)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        assign(f, MAT['fern_frond'])
        parts.append(f)
    return parts
