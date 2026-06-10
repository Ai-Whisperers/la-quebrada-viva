"""World shader, sun lamp, and bounded canopy Volume Scatter cube."""
from __future__ import annotations

import math
import os

import bpy


# Poly Haven CC0 HDRIs fetched by scripts/download_assets.sh. If the file is
# missing the world falls back to the procedural Nishita sky so the renderer
# still works on a fresh clone.
_HDRI_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'assets', 'hdris',
)
_HDRI_BY_VARIANT = {
    'A': ('kiara_1_dawn_4k.exr', 0.8),
    'B': ('misty_pines_4k.exr', 1.4),
}


def setup_world_and_sun(scene, variant: str):
    """Build the world shader and sun lamp for Variant A or B.

    World env: real-world HDRI from `assets/hdris/` if present, else Nishita
    procedural sky. The explicit Sun lamp stays in both paths — HDRIs give
    ambient + sky color but the directional rakes/shadows come from the lamp.
    """
    world = bpy.data.worlds.new('World')
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputWorld')
    bg = nt.nodes.new('ShaderNodeBackground')

    if variant == 'A':
        sun_energy = 5.5
        sun_color = (1.0, 0.78, 0.48, 1.0)
        sun_angle_deg = 1.5
        sun_rot = (math.radians(77), 0, math.radians(-22))
        sky_strength_fallback = 0.35
        sky_kwargs = dict(
            sun_elevation=math.radians(13),
            sun_rotation=math.radians(-22),
            sun_intensity=0.0,
        )
    elif variant == 'B':
        sun_energy = 0.5
        sun_color = (0.85, 0.88, 0.95, 1.0)
        sun_angle_deg = 8.0
        sun_rot = (math.radians(55), 0, math.radians(80))
        sky_strength_fallback = 1.4
        sky_kwargs = dict(
            sun_elevation=math.radians(35),
            sun_rotation=math.radians(80),
            sun_intensity=0.1,
        )
    else:
        raise ValueError(f'Unknown variant {variant!r}')

    hdri_name, hdri_strength = _HDRI_BY_VARIANT[variant]
    hdri_path = os.path.join(_HDRI_DIR, hdri_name)
    if os.path.isfile(hdri_path):
        env = nt.nodes.new('ShaderNodeTexEnvironment')
        env.image = bpy.data.images.load(hdri_path, check_existing=True)
        # Rotate HDRI Z so its painted sun aligns with the directional sun
        # lamp's azimuth — otherwise reflections + ambient direction disagree.
        mapping = nt.nodes.new('ShaderNodeMapping')
        tex_coord = nt.nodes.new('ShaderNodeTexCoord')
        mapping.inputs['Rotation'].default_value[2] = -sky_kwargs['sun_rotation']
        nt.links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
        nt.links.new(mapping.outputs['Vector'], env.inputs['Vector'])
        nt.links.new(env.outputs['Color'], bg.inputs['Color'])
        bg.inputs['Strength'].default_value = hdri_strength
    else:
        sky = nt.nodes.new('ShaderNodeTexSky')
        sky.sky_type = 'NISHITA'
        sky.air_density = 1.0
        sky.dust_density = 1.0
        sky.ozone_density = 1.0
        for attr, val in sky_kwargs.items():
            setattr(sky, attr, val)
        bg.inputs['Strength'].default_value = sky_strength_fallback
        nt.links.new(sky.outputs['Color'], bg.inputs['Color'])

    # Sub-canopy light shafts come from LOCAL volume domains (cube around the
    # canopy + cube around the corredor bottle-wall sight line), not the world
    # volume — wiring Volume Scatter to world.Volume creates an unbounded
    # scattering medium that, with finite volume_bounces, blacks out the image.

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


def build_valley_mist(variant: str, skip: bool = False):
    """B-only ground-hugging mist cube along the gorge.

    Sits below the canopy volume (canopy z range ≈ 4–14) so the two domains
    don't overlap and double-scatter. Centered on the stream (x≈11) and
    extending the gorge length (-25 ≤ y ≤ +5). Higher density + lower
    anisotropy than the canopy gives a diffuse fog read rather than god rays.
    """
    if variant != 'B' or skip:
        return None
    cx, cy, cz = 11.0, -10.0, 0.3
    sx, sy, sz = 8.0, 30.0, 2.0
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, cz))
    dom = bpy.context.active_object
    dom.name = 'ValleyMistDomain'
    dom.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    dom.display_type = 'WIRE'
    dom.hide_select = True

    mat = bpy.data.materials.new('ValleyMist')
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    vs = nt.nodes.new('ShaderNodeVolumeScatter')
    vs.inputs['Density'].default_value = 0.04
    vs.inputs['Anisotropy'].default_value = 0.3
    nt.links.new(vs.outputs['Volume'], out.inputs['Volume'])
    if dom.data.materials:
        dom.data.materials[0] = mat
    else:
        dom.data.materials.append(mat)
    return dom
