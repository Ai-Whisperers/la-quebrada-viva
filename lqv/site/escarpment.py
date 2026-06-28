"""Sandstone escarpment — heavy displaced wall, north backdrop."""
from __future__ import annotations

import math

import bpy

from ..materials import MAT, assign


def build_escarpment():
    """Heavy displaced wall, ~50 m tall, ~80 m wide. Positioned so the cliff
    actually reads behind the house from Cam_Hero (looking NW toward y=-20):
    pulled south to y=20 so it occupies the hero's upper-third backdrop instead
    of being a thin strip lost beyond the canopy.
    """
    width, height = 80.0, 50.0
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 20.0, height / 2))
    cliff = bpy.context.active_object
    cliff.name = 'Escarpment'
    cliff.scale = (width, 1.0, height)
    cliff.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(scale=True, rotation=True)

    sub = cliff.modifiers.new('Sub', 'SUBSURF')
    sub.levels = 4
    sub.render_levels = 4
    tex = bpy.data.textures.new('EscarpNoise', type='CLOUDS')
    tex.noise_scale = 3.0
    disp = cliff.modifiers.new('Disp', 'DISPLACE')
    disp.texture = tex
    disp.strength = 4.0
    disp.direction = 'NORMAL'

    tex2 = bpy.data.textures.new('EscarpFine', type='CLOUDS')
    tex2.noise_scale = 0.5
    disp2 = cliff.modifiers.new('DispFine', 'DISPLACE')
    disp2.texture = tex2
    disp2.strength = 0.5

    assign(cliff, MAT['sandstone'])
    return cliff
