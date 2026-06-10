"""Geometry helpers — bmesh-to-object and procedural displacement stack."""
from __future__ import annotations

import bpy


def new_object_from_bmesh(name, bm):
    mesh = bpy.data.meshes.new(name + 'Mesh')
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def add_subdiv_displace(obj, levels=3, noise_scale=6.0, strength=0.18, smooth=True):
    sub = obj.modifiers.new('Subdiv', 'SUBSURF')
    sub.levels = levels
    sub.render_levels = levels
    tex = bpy.data.textures.new(obj.name + 'Noise', type='CLOUDS')
    tex.noise_scale = noise_scale
    disp = obj.modifiers.new('Disp', 'DISPLACE')
    disp.texture = tex
    disp.strength = strength
    if smooth:
        smooth_mod = obj.modifiers.new('Smooth', 'SMOOTH')
        smooth_mod.factor = 0.5
        smooth_mod.iterations = 2
