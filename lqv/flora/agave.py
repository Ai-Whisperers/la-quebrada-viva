"""Agave americana — colonizing lower terraces, NOT a designed succulent garden."""
from __future__ import annotations

import math

import bpy

from ..materials import MAT, assign


def add_agave(x, y, scale=1.0):
    parts = []
    n_blades = 14
    for i in range(n_blades):
        ang = (i / n_blades) * math.tau
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.3 * scale))
        b = bpy.context.active_object
        b.name = 'AgaveBlade'
        b.scale = (0.06 * scale, 0.7 * scale, 0.04 * scale)
        bpy.ops.object.transform_apply(scale=True)
        b.location = (
            x + math.cos(ang) * 0.35 * scale,
            y + math.sin(ang) * 0.35 * scale,
            0.3 * scale,
        )
        b.rotation_euler = (math.radians(-30), 0, ang)
        assign(b, MAT['agave_blade'])
        parts.append(b)
    return parts
