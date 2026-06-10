"""Pindo palm (Syagrus romanzoffiana) — plumose drooping fronds."""
from __future__ import annotations

import math
import random

import bpy

from ..geometry import add_subdiv_displace
from ..materials import MAT, assign


def add_pindo_palm(x, y, scale=1.0):
    """Pindo palm with drooping plumose fronds — NOT coconut, NOT date palm.

    Fronds are bezier splines (crown → mid-arc raised → tip drooped) extruded
    via curve bevel_depth. This reads as plumose drooping silhouette rather
    than the stiff radial cube-spikes the toy build used.
    """
    trunk_h = 7.0 * scale
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.18 * scale, depth=trunk_h, location=(x, y, trunk_h / 2),
    )
    trunk = bpy.context.active_object
    trunk.name = f'PindoTrunk_{x:.0f}_{y:.0f}'
    add_subdiv_displace(trunk, levels=2, noise_scale=18.0, strength=0.025, smooth=False)
    # Retained leaf bases — Syagrus trunks carry diamond-tile scars from
    # shed fronds. Overlay a finer-scale CLOUDS displace so the silhouette
    # reads as scarred bark, not smooth pipe. No subdiv pass — reuses the
    # mesh density from the first add_subdiv_displace call.
    tex_scars = bpy.data.textures.new(trunk.name + 'LeafBases', type='CLOUDS')
    tex_scars.noise_scale = 0.55
    disp_scars = trunk.modifiers.new('DispLeafBases', 'DISPLACE')
    disp_scars.texture = tex_scars
    disp_scars.strength = 0.035
    assign(trunk, MAT['pindo_trunk'])

    crown_z = trunk_h
    parts = [trunk]

    curve_data = bpy.data.curves.new(name=f'PindoFrondsCurve_{x:.0f}_{y:.0f}', type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = 0.035 * scale
    curve_data.bevel_resolution = 2
    curve_data.resolution_u = 8
    curve_data.use_fill_caps = True

    n_fronds = 14
    frond_length = 2.7 * scale
    for i in range(n_fronds):
        ang = (i / n_fronds) * math.tau + random.uniform(-0.10, 0.10)
        cx, cy = math.cos(ang), math.sin(ang)
        rise = 0.35 + random.uniform(-0.06, 0.06)
        droop = 1.15 + random.uniform(-0.18, 0.18)
        flen = frond_length * random.uniform(0.92, 1.08)
        mid_r = flen * 0.55

        spline = curve_data.splines.new(type='BEZIER')
        spline.bezier_points.add(2)
        pts = spline.bezier_points
        pts[0].co = (x, y, crown_z)
        pts[1].co = (x + cx * mid_r, y + cy * mid_r, crown_z + rise * scale)
        pts[2].co = (x + cx * flen, y + cy * flen, crown_z - droop * scale)
        for p in pts:
            p.handle_left_type = 'AUTO'
            p.handle_right_type = 'AUTO'

    curve_obj = bpy.data.objects.new(f'PindoFronds_{x:.0f}_{y:.0f}', curve_data)
    bpy.context.collection.objects.link(curve_obj)
    assign(curve_obj, MAT['pindo_frond'])
    parts.append(curve_obj)
    return parts
