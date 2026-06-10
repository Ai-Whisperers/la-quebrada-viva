"""World shader, sun lamp, and bounded canopy Volume Scatter cube."""
from __future__ import annotations

import math

import bpy


def setup_world_and_sun(scene, variant: str):
    """Build the world shader and sun lamp for Variant A or B."""
    world = bpy.data.worlds.new('World')
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputWorld')
    bg = nt.nodes.new('ShaderNodeBackground')
    sky = nt.nodes.new('ShaderNodeTexSky')
    sky.sky_type = 'NISHITA'
    sky.air_density = 1.0
    sky.dust_density = 1.0
    sky.ozone_density = 1.0

    # Sub-canopy light shafts come from LOCAL volume domains (cube around the
    # canopy + cube around the corredor bottle-wall sight line), not the world
    # volume — wiring Volume Scatter to world.Volume creates an unbounded
    # scattering medium that, with finite volume_bounces, blacks out the image.

    if variant == 'A':
        # Winter golden hour, sun NNW low and warm. Elevation pulled from 20°
        # → 13° so the light rakes across the laterite + cob west face instead
        # of hitting from near-midday. Sky strength dropped so the sun reads as
        # the dominant directional source rather than a hot ambient flood.
        sky.sun_elevation = math.radians(13)
        sky.sun_rotation = math.radians(-22)  # NNW = -22.5° from north
        sky.sun_intensity = 0.0  # kill sky sun disk; explicit Sun lamp below provides directional light
        bg.inputs['Strength'].default_value = 0.35
        sun_energy = 5.5
        sun_color = (1.0, 0.78, 0.48, 1.0)
        sun_angle_deg = 1.5
        sun_rot = (math.radians(77), 0, math.radians(-22))
    elif variant == 'B':
        # Morning overcast — diffuse, slight blue cast
        sky.sun_elevation = math.radians(35)
        sky.sun_rotation = math.radians(80)
        sky.sun_intensity = 0.1
        bg.inputs['Strength'].default_value = 1.4
        sun_energy = 0.5
        sun_color = (0.85, 0.88, 0.95, 1.0)
        sun_angle_deg = 8.0  # diffuse, no hard shadows
        sun_rot = (math.radians(55), 0, math.radians(80))
    else:
        raise ValueError(f'Unknown variant {variant!r}')

    nt.links.new(sky.outputs['Color'], bg.inputs['Color'])
    nt.links.new(bg.outputs['Background'], out.inputs['Surface'])

    bpy.ops.object.light_add(type='SUN', location=(0, 0, 30))
    sun = bpy.context.active_object
    sun.name = 'Sun'
    sun.data.energy = sun_energy
    sun.data.color = sun_color[:3]
    sun.data.angle = math.radians(sun_angle_deg)
    sun.rotation_euler = sun_rot
    return sun


def build_canopy_volume(skip: bool = False):
    """Local bounded Volume Scatter cube — produces sub-canopy atmospheric depth
    (god rays through the forest) without the unbounded world-volume blackout.

    Density is intentionally low because the camera looks through up to 30m of
    medium and CPU volume sampling is expensive.

    Pass skip=True for preview renders — the volume domain doubles the CPU
    sampling cost on previews where the soft-shaft effect isn't visible
    anyway. Finals keep it.
    """
    if skip:
        return None
    cx, cy, cz = 0.0, -8.0, 9.0
    sx, sy, sz = 36.0, 42.0, 10.0
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, cz))
    dom = bpy.context.active_object
    dom.name = 'CanopyVolumeDomain'
    dom.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    dom.display_type = 'WIRE'
    dom.hide_select = True

    mat = bpy.data.materials.new('CanopyVolume')
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    vs = nt.nodes.new('ShaderNodeVolumeScatter')
    vs.inputs['Density'].default_value = 0.010
    vs.inputs['Anisotropy'].default_value = 0.6
    nt.links.new(vs.outputs['Volume'], out.inputs['Volume'])
    if dom.data.materials:
        dom.data.materials[0] = mat
    else:
        dom.data.materials.append(mat)
    return dom
