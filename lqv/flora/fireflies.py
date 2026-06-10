"""Variant C fireflies — bounded random emission points over the corredor + lower terrace."""
from __future__ import annotations

import random

import bpy

from ..materials import MAT, assign


def scatter_fireflies(n: int = 80, variant: str = 'A'):
    """Variant C only. Two zones:
      - corredor airspace: x ∈ [-6, 6], y ∈ [-4, -2]
      - lower terrace / stream approach: x ∈ [-8, 8], y ∈ [-8, -4]

    z ∈ [1.0, 2.5] keeps them between head-height and roof-eave. Each is a
    tiny UV-sphere with MAT['firefly'] (emission_strength=80). The total is
    split 1:2 corredor:terrace so the corredor doesn't read as a swarm.

    Must be called AFTER scatter_anthuriums to preserve the project's RNG
    draw order (CLAUDE.md invariant #1).
    """
    if variant != 'C':
        return []
    objs = []
    n_corredor = max(1, n // 3)
    n_terrace = n - n_corredor
    zones = [
        (n_corredor, (-6.0, 6.0), (-4.0, -2.0)),
        (n_terrace, (-8.0, 8.0), (-8.0, -4.0)),
    ]
    idx = 0
    for count, (xmin, xmax), (ymin, ymax) in zones:
        for _ in range(count):
            x = random.uniform(xmin, xmax)
            y = random.uniform(ymin, ymax)
            z = random.uniform(1.0, 2.5)
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=0.025, segments=8, ring_count=4, location=(x, y, z),
            )
            fly = bpy.context.active_object
            fly.name = f'Firefly_{idx:03d}'
            assign(fly, MAT['firefly'])
            objs.append(fly)
            idx += 1
    return objs
