"""Shader builder primitives — Principled BSDF, noise displacement, PBR.

All thematic submodules (earth/wood/foliage/glass/props) build their materials
on top of these helpers. No randomness is permitted here — the no-RNG-in-
materials contract is asserted by tests/test_rng_invariants.py.
"""
from __future__ import annotations

import os

import bpy

_TEX_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'assets', 'textures',
)


def _load_image(path: str):
    if not os.path.isfile(path):
        return None
    return bpy.data.images.load(path, check_existing=True)


def principled(name, base_color, roughness=0.7, metallic=0.0, ior=1.45,
               transmission=0.0, alpha=1.0, sss=None, sheen=0.0,
               emission_color=None, emission_strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = base_color
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['IOR'].default_value = ior
    if 'Transmission Weight' in bsdf.inputs:
        bsdf.inputs['Transmission Weight'].default_value = transmission
    bsdf.inputs['Alpha'].default_value = alpha
    if sss is not None and 'Subsurface Weight' in bsdf.inputs:
        bsdf.inputs['Subsurface Weight'].default_value = sss[0]
        if 'Subsurface Radius' in bsdf.inputs:
            bsdf.inputs['Subsurface Radius'].default_value = sss[1]
    if 'Sheen Weight' in bsdf.inputs:
        bsdf.inputs['Sheen Weight'].default_value = sheen
    if emission_color is not None:
        bsdf.inputs['Emission Color'].default_value = emission_color
        bsdf.inputs['Emission Strength'].default_value = emission_strength
    return m


def add_noise_displacement(mat, scale=8.0, strength=0.02):
    """Bump-shader noise on a material for fine surface variation."""
    nt = mat.node_tree
    bsdf = nt.nodes.get('Principled BSDF')
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = scale
    noise.inputs['Detail'].default_value = 8.0
    noise.inputs['Roughness'].default_value = 0.6
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = strength
    nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    return mat


def add_color_variegation(mat, scale, lit_color, dark_color, mix_fac=0.5):
    """Mix lit/dark base colors via a low-frequency noise so the surface reads
    as variegated rock/cob rather than one flat tone.

    NOTE: this helper *clobbers* any existing Base Color link, which destroys
    textured materials built with `textured_principled`. Use
    `add_secondary_color_variation` for textured materials.
    """
    nt = mat.node_tree
    bsdf = nt.nodes.get('Principled BSDF')
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = scale
    noise.inputs['Detail'].default_value = 4.0
    noise.inputs['Roughness'].default_value = 0.55
    mix = nt.nodes.new('ShaderNodeMixRGB')
    mix.inputs['Color1'].default_value = lit_color
    mix.inputs['Color2'].default_value = dark_color
    mix.inputs['Fac'].default_value = mix_fac
    nt.links.new(noise.outputs['Fac'], mix.inputs['Fac'])
    nt.links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])
    return mat


def add_secondary_color_variation(mat, scale, color_a, color_b, mix_fac=0.5):
    """Non-clobbering variegation: preserves an existing Base Color link by
    reinjecting it through a MixRGB (Color blend), with `color_b` tugged in
    proportional to a low-frequency noise. Falls back to `color_a` as Color1
    when Base Color is not already linked. Mirrors the `_tint_foliage_pink`
    pattern in lqv/flora/photoreal.py."""
    nt = mat.node_tree
    bsdf = nt.nodes.get('Principled BSDF')
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = scale
    noise.inputs['Detail'].default_value = 4.0
    noise.inputs['Roughness'].default_value = 0.55
    mix = nt.nodes.new('ShaderNodeMixRGB')
    mix.blend_type = 'COLOR'
    mix.inputs['Fac'].default_value = mix_fac
    mix.inputs['Color2'].default_value = color_b
    base = bsdf.inputs['Base Color']
    if base.is_linked:
        link = base.links[0]
        src_socket = link.from_socket
        nt.links.remove(link)
        nt.links.new(src_socket, mix.inputs['Color1'])
    else:
        mix.inputs['Color1'].default_value = color_a
    nt.links.new(noise.outputs['Fac'], mix.inputs['Fac'])
    nt.links.new(mix.outputs['Color'], base)
    return mat


def textured_principled(name, asset_id, uv_scale=1.0, tint_color=None, tint_fac=0.0,
                        roughness_bias=0.0, displacement_strength=0.05,
                        normal_strength=1.0):
    """PBR material built from a Poly Haven texture set in assets/textures/<asset_id>/.

    Wires Diffuse (optionally tinted toward `tint_color` via MULTIPLY mix),
    nor_gl, Rough, AO-into-base-color, and true Displacement on Material Output.
    Falls back to a flat principled tint if any diffuse map is missing — keeps
    the build resilient on a fresh clone before scripts/download_assets.sh runs.
    """
    base = tint_color if tint_color is not None else (0.5, 0.5, 0.5, 1.0)
    m = principled(name, base, roughness=0.9)
    nt = m.node_tree
    bsdf = nt.nodes.get('Principled BSDF')

    asset_dir = os.path.join(_TEX_DIR, asset_id)
    diff = _load_image(os.path.join(asset_dir, f'{asset_id}_Diffuse_4k.jpg'))
    if diff is None:
        return m

    norm = _load_image(os.path.join(asset_dir, f'{asset_id}_nor_gl_4k.jpg'))
    rough = _load_image(os.path.join(asset_dir, f'{asset_id}_Rough_4k.jpg'))
    ao = _load_image(os.path.join(asset_dir, f'{asset_id}_AO_4k.jpg'))
    disp = _load_image(os.path.join(asset_dir, f'{asset_id}_Displacement_4k.jpg'))

    # World-space Position from the Geometry node — gives true metric tiling
    # (uv_scale=1/8 ⇒ one tile per 8m), unlike Generated/UV which normalize to
    # the bounding box and would stretch one tile across the whole ground.
    geom = nt.nodes.new('ShaderNodeNewGeometry')
    mapping = nt.nodes.new('ShaderNodeMapping')
    mapping.inputs['Scale'].default_value = (uv_scale, uv_scale, uv_scale)
    nt.links.new(geom.outputs['Position'], mapping.inputs['Vector'])

    diff_node = nt.nodes.new('ShaderNodeTexImage')
    diff_node.image = diff
    nt.links.new(mapping.outputs['Vector'], diff_node.inputs['Vector'])
    base_socket = diff_node.outputs['Color']

    if ao is not None:
        ao.colorspace_settings.name = 'Non-Color'
        ao_node = nt.nodes.new('ShaderNodeTexImage')
        ao_node.image = ao
        nt.links.new(mapping.outputs['Vector'], ao_node.inputs['Vector'])
        ao_mul = nt.nodes.new('ShaderNodeMixRGB')
        ao_mul.blend_type = 'MULTIPLY'
        # Cycles already computes its own AO from geometry; texture-baked AO is
        # just a low-frequency cavity hint. Keep contribution gentle.
        ao_mul.inputs['Fac'].default_value = 0.2
        nt.links.new(base_socket, ao_mul.inputs['Color1'])
        nt.links.new(ao_node.outputs['Color'], ao_mul.inputs['Color2'])
        base_socket = ao_mul.outputs['Color']

    if tint_color is not None and tint_fac > 0.0:
        tint = nt.nodes.new('ShaderNodeMixRGB')
        # Plain MIX (linear interpolation) — holds the brief palette luminance
        # while keeping texture variation via the inverse fac toward diffuse.
        tint.blend_type = 'MIX'
        tint.inputs['Fac'].default_value = tint_fac
        tint.inputs['Color2'].default_value = tint_color
        nt.links.new(base_socket, tint.inputs['Color1'])
        base_socket = tint.outputs['Color']

    nt.links.new(base_socket, bsdf.inputs['Base Color'])

    if norm is not None:
        norm.colorspace_settings.name = 'Non-Color'
        norm_node = nt.nodes.new('ShaderNodeTexImage')
        norm_node.image = norm
        nt.links.new(mapping.outputs['Vector'], norm_node.inputs['Vector'])
        nm = nt.nodes.new('ShaderNodeNormalMap')
        nm.inputs['Strength'].default_value = normal_strength
        nt.links.new(norm_node.outputs['Color'], nm.inputs['Color'])
        nt.links.new(nm.outputs['Normal'], bsdf.inputs['Normal'])

    if rough is not None:
        rough.colorspace_settings.name = 'Non-Color'
        rough_node = nt.nodes.new('ShaderNodeTexImage')
        rough_node.image = rough
        nt.links.new(mapping.outputs['Vector'], rough_node.inputs['Vector'])
        if roughness_bias != 0.0:
            add = nt.nodes.new('ShaderNodeMath')
            add.operation = 'ADD'
            add.inputs[1].default_value = roughness_bias
            add.use_clamp = True
            nt.links.new(rough_node.outputs['Color'], add.inputs[0])
            nt.links.new(add.outputs['Value'], bsdf.inputs['Roughness'])
        else:
            nt.links.new(rough_node.outputs['Color'], bsdf.inputs['Roughness'])

    if disp is not None and displacement_strength > 0.0:
        disp.colorspace_settings.name = 'Non-Color'
        disp_node = nt.nodes.new('ShaderNodeTexImage')
        disp_node.image = disp
        nt.links.new(mapping.outputs['Vector'], disp_node.inputs['Vector'])
        disp_shader = nt.nodes.new('ShaderNodeDisplacement')
        disp_shader.inputs['Scale'].default_value = displacement_strength
        disp_shader.inputs['Midlevel'].default_value = 0.5
        nt.links.new(disp_node.outputs['Color'], disp_shader.inputs['Height'])
        out_node = nt.nodes.get('Material Output')
        if out_node is not None:
            nt.links.new(disp_shader.outputs['Displacement'], out_node.inputs['Displacement'])

    return m


def assign(obj, material):
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)
