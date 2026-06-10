"""Anthurium plowmanii — bird's-nest epiphyte rosettes on riparian trunks."""
from __future__ import annotations

import math
import random

import bpy

from ..geometry import add_subdiv_displace
from ..materials import MAT, assign


def _add_rosette(x, y, z, scale=1.0, n_leaves=6):
    """One epiphyte rosette: squashed sphere base + n strappy leaf planes."""
    parts = []

    # Rosette base — a small flattened UV sphere reading as the cupped
    # bird's-nest centre where leaves emerge.
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.10 * scale, segments=10, ring_count=6, location=(x, y, z),
    )
    base = bpy.context.active_object
    base.name = f'AnthuriumBase_{x:.1f}_{y:.1f}'
    base.scale = (1.0, 1.0, 0.45)
    bpy.ops.object.transform_apply(scale=True)
    assign(base, MAT['anthurium_leaf'])
    parts.append(base)

    base_ang_offset = random.uniform(0.0, math.tau)
    for i in range(n_leaves):
        leaf_len = (0.75 + random.uniform(-0.10, 0.15)) * scale
        leaf_w = (0.16 + random.uniform(-0.02, 0.03)) * scale
        ang = base_ang_offset + (i / n_leaves) * math.tau + random.uniform(-0.18, 0.18)
        tilt = math.radians(random.uniform(28.0, 58.0))
        cx, cy = math.cos(ang), math.sin(ang)
        # Leaf centre sits half-length along the radial, tipped upward by tilt.
        lcx = x + cx * (leaf_len * 0.5) * math.cos(tilt)
        lcy = y + cy * (leaf_len * 0.5) * math.cos(tilt)
        lcz = z + (leaf_len * 0.5) * math.sin(tilt) + 0.05 * scale

        bpy.ops.mesh.primitive_cube_add(size=1, location=(lcx, lcy, lcz))
        leaf = bpy.context.active_object
        leaf.name = f'AnthuriumLeaf_{x:.1f}_{y:.1f}_{i}'
        leaf.scale = (leaf_len, leaf_w, 0.012 * scale)
        bpy.ops.object.transform_apply(scale=True)
        # Yaw the leaf so its long axis points outward; pitch up by tilt.
        leaf.rotation_euler = (0.0, -tilt, ang)
        bpy.ops.object.transform_apply(rotation=True)
        add_subdiv_displace(leaf, levels=2, noise_scale=2.5, strength=0.012, smooth=True)
        assign(leaf, MAT['anthurium_leaf'])
        parts.append(leaf)

    return parts


def scatter_anthuriums(spots=None):
    """Mount epiphyte rosettes on a hardcoded list of riparian trunks.

    `spots` is a list of (x, y, mount_z, scale) tuples — defaults to the
    lapacho/mango trunks bordering the stream. Each spot gets a small jitter
    so the rosettes don't read as identical clones.

    RNG-order note: must be called after the existing flora.populate +
    scatter_lapacho_petals draws so it doesn't perturb their positions.
    """
    if spots is None:
        # x, y match the lapacho/mango spots in flora.populate; mount_z sits
        # mid-trunk; scale varies with tree scale.
        spots = [
            (-3.0, -10.0, 3.2, 1.10),   # lapacho — hero foreground left
            (8.0, -14.0, 3.0, 1.05),    # lapacho — mid stream
            (-18.0, 0.0, 4.0, 1.00),    # mango — far west
            (22.0, -22.0, 4.0, 1.05),   # mango — far southeast
        ]
    parts = []
    for x, y, z, s in spots:
        jx = x + random.uniform(-0.06, 0.06)
        jy = y + random.uniform(-0.06, 0.06)
        n = random.randint(5, 7)
        parts += _add_rosette(jx, jy, z, scale=s, n_leaves=n)
    return parts
