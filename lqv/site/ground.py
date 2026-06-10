"""Ground plane — Atlantic Forest floor + glade."""
from __future__ import annotations

import bpy

from ..materials import MAT, assign


def build_ground():
    bpy.ops.mesh.primitive_plane_add(size=120, location=(0, 0, 0))
    g = bpy.context.active_object
    g.name = 'Ground'
    sub = g.modifiers.new('Sub', 'SUBSURF')
    sub.levels = 5
    sub.render_levels = 6
    tex = bpy.data.textures.new('GroundNoise', type='CLOUDS')
    tex.noise_scale = 8.0
    disp = g.modifiers.new('Disp', 'DISPLACE')
    disp.texture = tex
    disp.strength = 0.35
    assign(g, MAT['laterite'])
    return g
