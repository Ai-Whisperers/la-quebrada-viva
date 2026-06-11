"""Bamboo (Guadua/Chusquea) — clumping along stream, NOT running."""
from __future__ import annotations

import math
import random

import bpy

from ..geometry import add_subdiv_displace
from ..materials import MAT, assign


def add_bamboo_clump(x, y, n=8, scale=1.0):
    """Guadua-style clumping bamboo. Each culm is a leaning cylinder; the upper
    two-thirds get a few flattened ellipsoid leaf-mass blobs so the clump silhouette
    reads as foliage, not bare poles. The leaf blobs are intentionally cheap — at
    distance the only thing that matters is that the silhouette isn't sticks.
    """
    parts = []
    for _ in range(n):
        ox = x + random.uniform(-0.5, 0.5)
        oy = y + random.uniform(-0.5, 0.5)
        h = random.uniform(5.0, 8.0) * scale
        lean_x = random.uniform(-0.08, 0.08)
        lean_y = random.uniform(-0.08, 0.08)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04 * scale, depth=h, location=(ox, oy, h / 2))
        c = bpy.context.active_object
        c.name = 'BambooCulm'
        c.rotation_euler = (lean_x, lean_y, 0)
        assign(c, MAT['bamboo'])
        parts.append(c)
        # Leaf-mass blobs clustered in the upper crown. Densify so adjacent blobs
        # overlap into a continuous foliage mass — at hero distance widely-spaced
        # ellipsoids read as "beads on a stick".
        n_blobs = random.randint(9, 13)
        for j in range(n_blobs):
            t = 0.55 + (j / max(n_blobs - 1, 1)) * 0.42  # 0.55–0.97 of culm height
            jitter_x = random.uniform(-0.45, 0.45) * scale
            jitter_y = random.uniform(-0.45, 0.45) * scale
            lz = h * t
            lx = ox + jitter_x + lean_y * lz
            ly = oy + jitter_y - lean_x * lz
            r = random.uniform(0.5, 0.75) * scale
            bpy.ops.mesh.primitive_ico_sphere_add(radius=r, location=(lx, ly, lz), subdivisions=2)
            leaf = bpy.context.active_object
            leaf.name = 'BambooLeafMass'
            leaf.scale = (1.0, 1.0, 0.55)
            leaf.rotation_euler = (
                random.uniform(-0.4, 0.4),
                random.uniform(-0.4, 0.4),
                random.uniform(0, math.tau),
            )
            bpy.ops.object.transform_apply(scale=True, rotation=True)
            add_subdiv_displace(leaf, levels=1, noise_scale=4.0, strength=0.18)
            assign(leaf, MAT['bamboo'])
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
            assign(blade, MAT['bamboo'])
            parts.append(blade)
    return parts
