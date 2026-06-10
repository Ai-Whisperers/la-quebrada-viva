"""Lapacho (Handroanthus impetiginosus) — variant-aware: bare+pink vs leafed."""
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
    assign(trunk, MAT['lapacho_bark'])
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
        assign(limb, MAT['lapacho_bark'])
        parts.append(limb)

        if flowering:
            # Trumpet flowers per limb tip — narrow calyx (radius1) → wide mouth
            # (radius2) along a randomly tilted axis. Replaces the earlier
            # icosphere puffballs so the silhouette reads as Handroanthus
            # trumpets, not pink cotton balls.
            for _ in range(4):
                ox = end_x + random.uniform(-0.5, 0.5)
                oy = end_y + random.uniform(-0.5, 0.5)
                oz = end_z + random.uniform(-0.4, 0.4)
                bpy.ops.mesh.primitive_cone_add(
                    vertices=12,
                    radius1=0.04 * scale,
                    radius2=0.18 * scale,
                    depth=0.30 * scale,
                    location=(ox, oy, oz),
                )
                flower = bpy.context.active_object
                flower.name = 'LapachoFlower'
                # Tilt the cone so its open mouth (top) faces outward+down,
                # mimicking gravity-hung trumpets. Random roll around the
                # outward axis avoids the cluster looking lattice-aligned.
                outward = Vector((ox - x, oy - y, -0.3))
                flower.rotation_mode = 'XYZ'
                flower.rotation_euler = outward.to_track_quat('Z', 'Y').to_euler()
                flower.rotation_euler.z += random.uniform(0, math.tau)
                assign(flower, MAT['lapacho_flower'])
                parts.append(flower)
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
    """Small pink discs scattered on the laterite ground for Variant A.

    Ground has a CLOUDS displace of strength 0.35, so a fixed z carpets
    the air in troughs and buries petals in crests. Raycast the evaluated
    ground mesh per petal to anchor them on the actual surface.
    """
    # Force the depsgraph to evaluate Ground's Displace modifier before we
    # build the BVH — otherwise FromObject reads the flat base mesh and every
    # petal lands at z=0 (buried in crests / floating over troughs).
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    ground = bpy.data.objects.get('Ground')
    bvh = None
    if ground is not None:
        from mathutils.bvhtree import BVHTree
        ground_eval = ground.evaluated_get(depsgraph)
        bvh = BVHTree.FromObject(ground_eval, depsgraph)

    def ground_z(x, y):
        if bvh is None:
            return 0.0
        hit, _normal, _idx, _dist = bvh.ray_cast(
            (x, y, 10.0), (0.0, 0.0, -1.0),
        )
        return hit.z if hit is not None else 0.0

    bpy.ops.mesh.primitive_plane_add(size=0.12, location=(0, 0, 0.02))
    proto = bpy.context.active_object
    proto.name = 'PetalProto'
    proto.hide_render = True
    assign(proto, MAT['lapacho_flower'])

    parts = []
    for _ in range(n):
        # Cluster densely under the foreground lapacho at (-3, -10). σ=1.2 keeps
        # 86% of cluster petals within 2.5m — needed for Cam_PetalMacro's tight
        # ~43cm frame at 85mm to actually show petals, not just laterite.
        if random.random() < 0.75:
            x = -3 + random.gauss(0, 1.2)
            y = -10 + random.gauss(0, 1.2)
        else:
            x = random.uniform(-area_radius, area_radius)
            y = random.uniform(-area_radius, area_radius)
        z = ground_z(x, y) + random.uniform(0.005, 0.025)
        bpy.ops.mesh.primitive_plane_add(size=0.12, location=(x, y, z))
        p = bpy.context.active_object
        p.name = 'Petal'
        # Small X/Y tilt so petals don't read as flat cardstock — fallen
        # petals settle at angles against soil bumps.
        p.rotation_euler = (
            random.uniform(-0.25, 0.25),
            random.uniform(-0.25, 0.25),
            random.uniform(0, math.tau),
        )
        p.scale = (random.uniform(0.7, 1.3), random.uniform(0.7, 1.3), 1.0)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        assign(p, MAT['lapacho_flower'])
        parts.append(p)
    return parts
