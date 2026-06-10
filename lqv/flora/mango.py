"""Mango — dominant canopy, dense dark-green rounded crown."""
from __future__ import annotations

import bpy

from ..geometry import add_subdiv_displace
from ..materials import MAT, assign


def add_mango(x, y, scale=1.0):
    """Mango — dominant canopy, dense dark-green rounded crown.
    Crown is a cluster of overlapping displaced ico_spheres so the silhouette
    reads as foliage mass rather than a single billiard ball.
    """
    trunk_h = 6.0 * scale
    bpy.ops.mesh.primitive_cylinder_add(radius=0.45 * scale, depth=trunk_h, location=(x, y, trunk_h / 2))
    trunk = bpy.context.active_object
    trunk.name = f'MangoTrunk_{x:.0f}_{y:.0f}'
    add_subdiv_displace(trunk, levels=2, noise_scale=12.0, strength=0.05, smooth=False)
    assign(trunk, MAT['mango_trunk'])
    parts = [trunk]

    base_z = trunk_h + 3.0 * scale
    cluster = [
        (0.0, 0.0, 0.5, 5.0),
        (1.6, 0.0, 0.9, 3.4),
        (-1.5, 0.4, 0.6, 3.6),
        (0.3, 1.7, 1.2, 3.2),
        (0.1, -1.8, 0.7, 3.5),
        (0.6, 0.3, 2.1, 2.8),
    ]
    for ox, oy, oz, r in cluster:
        bpy.ops.mesh.primitive_ico_sphere_add(
            radius=r * scale,
            location=(x + ox * scale, y + oy * scale, base_z + oz * scale),
            subdivisions=3,
        )
        ball = bpy.context.active_object
        ball.name = f'MangoCrownPart_{x:.0f}_{y:.0f}'
        ball.scale = (1.0, 1.0, 0.85)
        bpy.ops.object.transform_apply(scale=True)
        add_subdiv_displace(ball, levels=1, noise_scale=2.5, strength=0.55)
        assign(ball, MAT['canopy'])
        parts.append(ball)
    return parts
