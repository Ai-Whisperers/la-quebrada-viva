"""Wood-family materials: lapacho timber/bark, pindo and mango trunks, bamboo."""
from __future__ import annotations

from lqv.materials._palette import COL, hex_to_rgb
from lqv.materials._shaders import (
    add_secondary_color_variation,
    principled,
    textured_principled,
)


def build(MAT: dict) -> None:
    """Populate MAT with wood-family entries.

    Beauty pass 2026-06-14: lapacho_timber upgraded from flat principled to
    full PBR (old_planks_02) tinted toward the heartwood palette. Supersedes
    the 85e86aa byte-freeze (user-authorized; escritura beauty sprint).
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
    MAT['bamboo'] = principled('Bamboo', hex_to_rgb('#8AA055'), roughness=0.7)
