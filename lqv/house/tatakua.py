"""Tatakuá — domed clay oven on the south wall."""
from __future__ import annotations

import bmesh
import bpy

from ..geometry import add_subdiv_displace
from ..materials import MAT, assign, principled


def build_tatakua():
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

    # Small arched opening (a darker rectangle for the firebox mouth)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-5.5, -5.32, 0.45))
    mouth = bpy.context.active_object
    mouth.name = 'TatakuaMouth'
    mouth.scale = (0.35, 0.1, 0.4)
    bpy.ops.object.transform_apply(scale=True)
    assign(mouth, principled('TatakuaMouth', (0.02, 0.01, 0.01, 1), roughness=1.0))

    return [dome, mouth]
