"""Wood-family materials: lapacho timber/bark, pindo and mango trunks, bamboo."""
from __future__ import annotations

import bpy

from lqv.materials._palette import COL, hex_to_rgb
from lqv.materials._shaders import (
    add_secondary_color_variation,
    principled,
    textured_principled,
)


def _add_bamboo_node_rings(mat, ring_color, ring_spacing=0.30, ring_width=0.022):
    """Stamp dark node rings onto a culm material at fixed Z intervals via shader.

    Uses world Position.Z → fract(Z/spacing) → step → mix; preserves any existing
    Base Color link so it composes with `add_secondary_color_variation`. No RNG —
    the material contract bans randomness here (see test_rng_invariants).
    """
    nt = mat.node_tree
    bsdf = nt.nodes.get('Principled BSDF')

    geom = nt.nodes.new('ShaderNodeNewGeometry')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(geom.outputs['Position'], sep.inputs['Vector'])

    div = nt.nodes.new('ShaderNodeMath')
    div.operation = 'DIVIDE'
    div.inputs[1].default_value = ring_spacing
    nt.links.new(sep.outputs['Z'], div.inputs[0])

    frac = nt.nodes.new('ShaderNodeMath')
    frac.operation = 'FRACT'
    nt.links.new(div.outputs['Value'], frac.inputs[0])

    thresh = nt.nodes.new('ShaderNodeMath')
    thresh.operation = 'GREATER_THAN'
    thresh.inputs[1].default_value = 1.0 - (ring_width / ring_spacing)
    nt.links.new(frac.outputs['Value'], thresh.inputs[0])

    mix = nt.nodes.new('ShaderNodeMixRGB')
    mix.blend_type = 'MIX'
    mix.inputs['Color2'].default_value = ring_color
    base = bsdf.inputs['Base Color']
    if base.is_linked:
        link = base.links[0]
        src = link.from_socket
        nt.links.remove(link)
        nt.links.new(src, mix.inputs['Color1'])
    else:
        mix.inputs['Color1'].default_value = base.default_value
    nt.links.new(thresh.outputs['Value'], mix.inputs['Fac'])
    nt.links.new(mix.outputs['Color'], base)
    # Slight roughness bump at the ring — fibres are dryer/rougher at nodes.
    rough_mix = nt.nodes.new('ShaderNodeMath')
    rough_mix.operation = 'MULTIPLY_ADD'
    rough_mix.inputs[1].default_value = 0.12
    rough_mix.inputs[2].default_value = bsdf.inputs['Roughness'].default_value
    nt.links.new(thresh.outputs['Value'], rough_mix.inputs[0])
    nt.links.new(rough_mix.outputs['Value'], bsdf.inputs['Roughness'])
    return mat


def build(MAT: dict) -> None:
    """Populate MAT with wood-family entries.

    Beauty pass 2026-06-14: lapacho_timber upgraded from flat principled to
    full PBR (old_planks_02) tinted toward the heartwood palette. Supersedes
    the 85e86aa byte-freeze (user-authorized; escritura beauty sprint).

    Beauty pass 2026-06-15: bamboo split into culm/leaf/grass. Old single
    `bamboo` material (olive principled BSDF) read as ivory marshmallow on
    ivory toothpick under the warm HDRI. New: warm tan-yellow Guadua culm
    with shader-driven dark node rings every 30 cm; chlorophyll-green leaf
    with SSS; separate grass material. `bamboo` kept as alias for any caller
    we haven't migrated yet.
    """
    MAT['lapacho_timber'] = textured_principled(
        'LapachoTimber', 'old_planks_02',
        uv_scale=1.0 / 2.4,
        tint_color=COL['lapacho_timber'], tint_fac=0.40,
        roughness_bias=-0.05,
        displacement_strength=0.02,
        normal_strength=1.2,
    )
    # Non-clobbering: preserves the textured_principled PBR diffuse via a
    # MixRGB (Color blend), unlike the deprecated add_color_variegation.
    add_secondary_color_variation(
        MAT['lapacho_timber'],
        scale=3.0,
        color_a=hex_to_rgb('#7A3A1F'),
        color_b=hex_to_rgb('#3A1A0A'),
        mix_fac=0.18,
    )
    # Bark for the living trunk + limbs — tree_bark_03 PBR set tinted toward
    # the lapacho_bark palette. uv_scale ~1/0.6 gives one tile every ~60cm,
    # matched to the 40cm-diameter trunk so bark grain reads at hero distance.
    MAT['lapacho_bark'] = textured_principled(
        'LapachoBark', 'tree_bark_03',
        uv_scale=1.0 / 0.6,
        tint_color=COL['lapacho_bark'], tint_fac=0.25,
        displacement_strength=0.02,
        normal_strength=1.4,
    )
    MAT['pindo_trunk'] = principled('PindoTrunk', hex_to_rgb('#6A6258'), roughness=0.85)
    MAT['mango_trunk'] = principled('MangoTrunk', hex_to_rgb('#3A2A1E'), roughness=0.9)

    # Guadua angustifolia mature culm: warm tan-yellow #C9B265, low roughness
    # with slight sheen (waxy cuticle), longitudinal mottling, dark node bands.
    MAT['bamboo_culm'] = principled(
        'BambooCulm', hex_to_rgb('#C9B265'),
        roughness=0.42, sheen=0.25,
    )
    add_secondary_color_variation(
        MAT['bamboo_culm'],
        scale=4.0,
        color_a=hex_to_rgb('#C9B265'),
        color_b=hex_to_rgb('#9E8848'),
        mix_fac=0.22,
    )
    _add_bamboo_node_rings(
        MAT['bamboo_culm'],
        ring_color=hex_to_rgb('#3E2A14'),
        ring_spacing=0.35,
        ring_width=0.045,
    )

    # Chlorophyll-green lanceolate leaf with subsurface translucency so backlit
    # leaves don't read as black silhouettes. SSS weight matches anthurium_leaf.
    MAT['bamboo_leaf'] = principled(
        'BambooLeaf', hex_to_rgb('#4A7A2A'),
        roughness=0.55, sheen=0.15,
        sss=(0.10, (0.50, 0.62, 0.30)),
    )

    # Separate grass material so `scatter_grass_tufts` no longer paints the
    # foreground in the same olive principled as the (former) bamboo culms.
    MAT['grass_blade'] = principled(
        'GrassBlade', hex_to_rgb('#6B8A38'),
        roughness=0.72,
        sss=(0.05, (0.40, 0.55, 0.25)),
    )

    # Back-compat: any caller still asking for MAT['bamboo'] gets the culm
    # material. Leaves/grass paths in the rewritten clump go via the new keys.
    MAT['bamboo'] = MAT['bamboo_culm']
