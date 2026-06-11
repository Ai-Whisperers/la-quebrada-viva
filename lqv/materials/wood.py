"""Wood-family materials: lapacho timber/bark, pindo and mango trunks, bamboo."""
from __future__ import annotations

from lqv.materials._palette import COL, hex_to_rgb
from lqv.materials._shaders import principled, textured_principled


def build(MAT: dict) -> None:
    """Populate MAT with wood-family entries.

    Builder calls + parameters are byte-identical to the pre-split monolith;
    do not retune without re-rendering the 18 finals at 85e86aa.
    """
    MAT['lapacho_timber'] = principled(
        'LapachoTimber', COL['lapacho_timber'], roughness=0.55,
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
