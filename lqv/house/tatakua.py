"""Tatakuá — domed clay oven on the south wall (Rule 8 cultural detail)."""
from __future__ import annotations

import math

import bmesh
import bpy

from ..geometry import add_subdiv_displace
from ..materials import MAT, assign, principled


def build_tatakua():
    parts = []

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.9, location=(-5.5, -4.5, 0.9))
    dome = bpy.context.active_object
    dome.name = 'Tatakua'
    # Flatten the bottom by scaling Z and clipping (we'll just slice)
    dome.scale = (1.0, 1.0, 0.85)
    bpy.ops.object.transform_apply(scale=True)
    bm = bmesh.new()
    bm.from_mesh(dome.data)
    bm.faces.ensure_lookup_table()
    to_remove = [v for v in bm.verts if v.co.z < 0.0]
    bmesh.ops.delete(bm, geom=to_remove, context='VERTS')
    bm.to_mesh(dome.data)
    bm.free()
    add_subdiv_displace(dome, levels=3, noise_scale=10.0, strength=0.04)
    assign(dome, MAT['cob_raw'])
    parts.append(dome)

    # Small arched opening (a darker rectangle for the firebox mouth)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-5.5, -5.32, 0.45))
    mouth = bpy.context.active_object
    mouth.name = 'TatakuaMouth'
    mouth.scale = (0.35, 0.1, 0.4)
    bpy.ops.object.transform_apply(scale=True)
    assign(mouth, principled('TatakuaMouth', (0.02, 0.01, 0.01, 1), roughness=1.0))
    parts.append(mouth)

    # Chimney — cob cylinder rising from the dome apex. Dome apex sits at
    # z ≈ 0.9 + 0.9*0.85 ≈ 1.665, so seat the chimney base just below it.
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.12, depth=0.80, location=(-5.5, -4.5, 2.00),
    )
    chimney = bpy.context.active_object
    chimney.name = 'TatakuaChimney'
    add_subdiv_displace(chimney, levels=2, noise_scale=10.0, strength=0.02)
    assign(chimney, MAT['cob_raw'])
    parts.append(chimney)
    # Chimney lip — a fired-clay torus reading as a smoke-blackened collar.
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.14, minor_radius=0.03, location=(-5.5, -4.5, 2.42),
    )
    lip = bpy.context.active_object
    lip.name = 'TatakuaChimneyLip'
    assign(lip, principled('TatakuaChimneyLip', (0.05, 0.03, 0.02, 1), roughness=0.95))
    parts.append(lip)

    # Ash door — small lapacho-timber hatch on the north (back) side of the
    # dome, opposite the mouth. Lets the oven read as a working tatakuá.
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-5.5, -3.68, 0.30))
    ash_door = bpy.context.active_object
    ash_door.name = 'TatakuaAshDoor'
    ash_door.scale = (0.22, 0.10, 0.22)
    bpy.ops.object.transform_apply(scale=True)
    assign(ash_door, MAT['lapacho_timber'])
    parts.append(ash_door)

    # Firewood pile beside the oven — short stack of lapacho logs aligned
    # along +X. Two-row pyramidal stack so the silhouette reads as wood,
    # not as fenceposts. Hardcoded positions — no random.*.
    log_specs = (
        (-3.95, -5.05, 0.08, 0.085, 0.85),
        (-3.95, -4.85, 0.08, 0.085, 0.85),
        (-3.95, -4.65, 0.08, 0.085, 0.85),
        (-3.95, -4.95, 0.24, 0.075, 0.80),
        (-3.95, -4.75, 0.24, 0.075, 0.80),
        (-3.95, -4.85, 0.38, 0.070, 0.75),
    )
    for i, (lx, ly, lz, lr, ld) in enumerate(log_specs):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=lr, depth=ld, location=(lx, ly, lz),
        )
        log = bpy.context.active_object
        log.name = f'TatakuaFirewood_{i}'
        log.rotation_euler = (0, math.radians(90), 0)
        bpy.ops.object.transform_apply(rotation=True)
        assign(log, MAT['lapacho_timber'])
        parts.append(log)

    return parts
