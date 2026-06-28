"""Stone terraces — three sandstone retaining walls stepped down toward the glade."""
from __future__ import annotations

import bpy

from ..geometry import add_subdiv_displace
from ..materials import MAT, assign


def build_terraces():
    """Three sandstone retaining walls stepped down toward the glade."""
    objs = []
    for i in range(3):
        z_base = 1.2 - i * 0.6  # upper terrace highest
        y_front = -2.0 - i * 4.0  # each terrace face is downhill of the last
        # Top platform plane
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, y_front + 2.0, z_base))
        plat = bpy.context.active_object
        plat.name = f'TerracePlatform{i}'
        plat.scale = (24.0, 8.0, 1.0)
        bpy.ops.object.transform_apply(scale=True)
        sub = plat.modifiers.new('Sub', 'SUBSURF')
        sub.levels = 4
        sub.render_levels = 5
        tex = bpy.data.textures.new(f'TerrTex{i}', type='CLOUDS')
        tex.noise_scale = 5.0
        disp = plat.modifiers.new('Disp', 'DISPLACE')
        disp.texture = tex
        disp.strength = 0.06
        assign(plat, MAT['laterite'])
        objs.append(plat)

        # Front retaining wall (drystack sandstone face)
        wall_h = 0.6
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, y_front, z_base - wall_h / 2))
        wall = bpy.context.active_object
        wall.name = f'TerraceWall{i}'
        wall.scale = (24.0, 0.5, wall_h)
        bpy.ops.object.transform_apply(scale=True)
        add_subdiv_displace(wall, levels=4, noise_scale=8.0, strength=0.12)
        assign(wall, MAT['sandstone'])
        objs.append(wall)
    return objs
