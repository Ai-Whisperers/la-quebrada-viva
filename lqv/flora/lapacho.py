"""Lapacho (Handroanthus impetiginosus) — variant-aware: bare+pink vs leafed.

Preserves the monolith's MAT['mango_trunk'] keying (Tier 2 fix candidate).
"""
from __future__ import annotations

import math
import random

import bpy
from mathutils import Vector

from ..geometry import add_subdiv_displace
from ..materials import MAT, assign


def add_lapacho(x, y, scale=1.0, flowering=True):
    """Lapacho — variant-aware. flowering=True: bare branches + pink bloom."""
    trunk_h = 9.0 * scale
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.35 * scale, depth=trunk_h, location=(x, y, trunk_h / 2),
    )
    trunk = bpy.context.active_object
    trunk.name = f'LapachoTrunk_{x:.0f}_{y:.0f}'
    add_subdiv_displace(trunk, levels=2, noise_scale=14.0, strength=0.04, smooth=False)
    assign(trunk, MAT['mango_trunk'])
    parts = [trunk]

    crown_z = trunk_h
    # Sparse branching — three main limbs
    for i in range(5):
        ang = (i / 5) * math.tau + random.uniform(-0.2, 0.2)
        length = (2.5 + random.uniform(-0.6, 0.6)) * scale
        end_x = x + math.cos(ang) * length
        end_y = y + math.sin(ang) * length
        end_z = crown_z + random.uniform(1.0, 2.0) * scale
        # Make a stretched cylinder approximating the limb
        mid = ((x + end_x) / 2, (y + end_y) / 2, (crown_z + end_z) / 2)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08 * scale, depth=length * 1.5, location=mid)
        limb = bpy.context.active_object
        limb.name = f'LapachoLimb_{i}'
        # Point the limb from trunk top to its end
        dx, dy, dz = end_x - x, end_y - y, end_z - crown_z
        limb.rotation_mode = 'XYZ'
        limb.rotation_euler = Vector((dx, dy, dz)).to_track_quat('Z', 'Y').to_euler()
        assign(limb, MAT['mango_trunk'])
        parts.append(limb)

        if flowering:
            # Hot-pink puffballs at limb tips
            for _ in range(3):
                ox = end_x + random.uniform(-0.5, 0.5)
                oy = end_y + random.uniform(-0.5, 0.5)
                oz = end_z + random.uniform(-0.4, 0.4)
                bpy.ops.mesh.primitive_ico_sphere_add(radius=0.5 * scale, location=(ox, oy, oz), subdivisions=2)
                puff = bpy.context.active_object
                puff.name = 'LapachoFlowerCluster'
                assign(puff, MAT['lapacho_flower'])
                parts.append(puff)
        else:
            # Leafed crown — 2–3 overlapping displaced balls per limb so silhouette
            # reads as foliage mass rather than a smooth icosphere.
            for _ in range(random.randint(2, 3)):
                jx = end_x + random.uniform(-0.6, 0.6) * scale
                jy = end_y + random.uniform(-0.6, 0.6) * scale
                jz = end_z + random.uniform(-0.3, 0.5) * scale
                r = random.uniform(1.1, 1.5) * scale
                bpy.ops.mesh.primitive_ico_sphere_add(radius=r, location=(jx, jy, jz), subdivisions=3)
                crown = bpy.context.active_object
                crown.name = 'LapachoCrown'
                crown.scale = (1.0, 1.0, 0.75)
                bpy.ops.object.transform_apply(scale=True)
                add_subdiv_displace(crown, levels=1, noise_scale=3.0, strength=0.45)
                assign(crown, MAT['lapacho_leaf'])
                parts.append(crown)

    return parts


def scatter_lapacho_petals(n=400, area_radius=12.0):
    """Small pink discs scattered on the laterite ground for Variant A."""
    bpy.ops.mesh.primitive_plane_add(size=0.12, location=(0, 0, 0.02))
    proto = bpy.context.active_object
    proto.name = 'PetalProto'
    proto.hide_render = True
    assign(proto, MAT['lapacho_flower'])

    parts = []
    for _ in range(n):
        # Cluster more densely under the foreground lapacho at (-3, -10)
        if random.random() < 0.55:
            x = -3 + random.gauss(0, 3.5)
            y = -10 + random.gauss(0, 3.5)
        else:
            x = random.uniform(-area_radius, area_radius)
            y = random.uniform(-area_radius, area_radius)
        z = 0.02 + random.uniform(0, 0.02)
        bpy.ops.mesh.primitive_plane_add(size=0.12, location=(x, y, z))
        p = bpy.context.active_object
        p.name = 'Petal'
        p.rotation_euler = (0, 0, random.uniform(0, math.tau))
        p.scale = (random.uniform(0.7, 1.3), random.uniform(0.7, 1.3), 1.0)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        assign(p, MAT['lapacho_flower'])
        parts.append(p)
    return parts
