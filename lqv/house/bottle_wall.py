"""Bottle wall — embedded in the east arm of the U."""
from __future__ import annotations

import math
import random

import bpy

from ..materials import MAT, assign


def build_bottle_wall():
    """Cluster of paired-bottle glass cylinders set into the east wall section.

    Approximation: each "bottle pair" is a horizontal glass cylinder spanning
    the 50 cm wall thickness, coloured by random selection from the bottle
    palette. Pattern is an organic cluster, not a grid.
    """
    wall_x = 6.0  # outer face of east arm
    z_base = 0.6 + 0.8  # 80 cm above the foundation
    bottle_mats = [
        MAT['glass_bottle_cobalt'], MAT['glass_bottle_amber'],
        MAT['glass_bottle_green'],  MAT['glass_bottle_brown'],
    ]
    objs = []
    # Cluster sample positions — organic, around a 2 m wide × 1.5 m tall patch
    cluster_centres = [(0.0, 0.0), (-0.7, 0.4), (0.8, 0.3), (-0.4, -0.5), (0.5, -0.6), (0.0, 0.9)]
    for cx, cz in cluster_centres:
        for _ in range(random.randint(6, 11)):
            jitter_y = cx + random.gauss(0.0, 0.35)
            jitter_z = z_base + cz + random.gauss(0.0, 0.25)
            if abs(jitter_y) > 1.4:
                continue
            bpy.ops.mesh.primitive_cylinder_add(
                radius=0.04, depth=0.55,
                location=(wall_x, 2.0 + jitter_y, jitter_z),
                rotation=(0.0, math.radians(90), 0.0),
            )
            b = bpy.context.active_object
            b.name = 'Bottle'
            assign(b, random.choice(bottle_mats))
            objs.append(b)
    return objs
