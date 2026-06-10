"""Stream channel descending from north (cliff base) to south-east."""
from __future__ import annotations

import math
import random

import bpy

from ..geometry import add_subdiv_displace
from ..materials import MAT, assign


def build_stream():
    """Stream channel descending from north (cliff base) to south-east.

    A simple channel carved into the ground via a flat-rock pool at the
    south end, with three cascade drops upstream.
    """
    objs = []
    # Stream bed — flat plane below water level. The subdiv+displace under
    # opaque-ish water never showed through anyway, so we eat the cost saving.
    bpy.ops.mesh.primitive_plane_add(size=1, location=(11.0, -6.0, -0.5))
    bed = bpy.context.active_object
    bed.name = 'StreamBed'
    bed.scale = (4.0, 40.0, 1.0)
    bed.rotation_euler = (0, 0, math.radians(-12))
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    assign(bed, MAT['stream_bed'])
    objs.append(bed)

    # Flat-rock pool — wider section at the south end. Pool bed pushed deeper
    # (-0.55) and water disc raised (-0.10) so volume absorption has actual
    # depth to attenuate through, instead of reading as a thin tinted film.
    bpy.ops.mesh.primitive_cylinder_add(radius=5.5, depth=0.3, location=(11.0, -22.0, -0.55))
    pool_bed = bpy.context.active_object
    pool_bed.name = 'PoolBed'
    add_subdiv_displace(pool_bed, levels=3, noise_scale=2.0, strength=0.12)
    assign(pool_bed, MAT['sandstone'])
    objs.append(pool_bed)

    # Water surface — flat plane covering the channel + pool, at z = -0.18
    bpy.ops.mesh.primitive_plane_add(size=1, location=(11.5, -10.0, -0.18))
    water = bpy.context.active_object
    water.name = 'StreamWater'
    water.scale = (4.5, 32.0, 1.0)
    water.rotation_euler = (0, 0, math.radians(-12))
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    assign(water, MAT['pool_water'])
    objs.append(water)

    # Pool water disc — sits ~0.45m above the deepened bed for visible depth
    bpy.ops.mesh.primitive_cylinder_add(radius=5.2, depth=0.04, location=(11.0, -22.0, -0.10))
    pool_water = bpy.context.active_object
    pool_water.name = 'PoolWater'
    assign(pool_water, MAT['pool_water'])
    objs.append(pool_water)

    # Three cascade boulder clusters
    for i, y in enumerate((-2.0, -8.0, -14.0)):
        for k in range(3):
            bpy.ops.mesh.primitive_ico_sphere_add(
                radius=random.uniform(0.4, 0.8),
                location=(11.0 + random.uniform(-1.5, 1.5), y + random.uniform(-0.8, 0.8),
                          -0.2 + random.uniform(0.0, 0.3)),
                subdivisions=3,
            )
            b = bpy.context.active_object
            b.name = f'CascadeBoulder_{i}_{k}'
            b.scale = (random.uniform(0.9, 1.3), random.uniform(0.9, 1.3), random.uniform(0.7, 1.0))
            bpy.ops.object.transform_apply(scale=True)
            assign(b, MAT['sandstone'])
            objs.append(b)

    # Footbridge moved south of the pool (y=-25.5 instead of -19) so it no
    # longer occludes the pool from Cam_Hero. Cam looks NW from (18,-33) toward
    # (10,-20), so a bridge at y=-19 sits dead-centre over the hero pool.
    for x_off in (-0.18, 0.18):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(11.0 + x_off, -25.5, 0.25))
        beam = bpy.context.active_object
        beam.name = f'BridgeBeam_{x_off:+.2f}'
        beam.scale = (0.12, 6.0, 0.1)
        bpy.ops.object.transform_apply(scale=True)
        assign(beam, MAT['lapacho_timber'])
        objs.append(beam)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(11.0, -25.5, 0.32))
    deck = bpy.context.active_object
    deck.name = 'BridgeDeck'
    deck.scale = (1.0, 6.0, 0.04)
    bpy.ops.object.transform_apply(scale=True)
    assign(deck, MAT['lapacho_timber'])
    objs.append(deck)

    return objs
