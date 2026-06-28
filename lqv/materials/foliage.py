"""Foliage materials: sod canopy, generic canopy, lapacho leaves/flowers,
pindo/fern fronds, agave blade, anthurium leaf.

Backlit leaves use SSS so the Variant-A sun-through-canopy read holds.
"""
from __future__ import annotations

from lqv.materials._palette import COL, hex_to_rgb
from lqv.materials._shaders import add_noise_displacement, principled


def build(MAT: dict) -> None:
    """Populate MAT with foliage-family entries.

    Builder calls + parameters are byte-identical to the pre-split monolith;
    do not retune without re-rendering the 18 finals at 85e86aa.
    """
    MAT['sod_canopy'] = add_noise_displacement(
        principled('SodRoof', COL['canopy_lit'], roughness=0.95, sheen=0.15),
        scale=10.0, strength=0.06,
    )
    MAT['canopy'] = principled('Canopy', COL['canopy_deep'], roughness=0.85)
    MAT['lapacho_leaf'] = principled('LapachoLeaf', COL['canopy_lit'], roughness=0.7)
    MAT['lapacho_flower'] = principled(
        'LapachoFlower', COL['lapacho_bloom'], roughness=0.55,
        sss=(0.2, (0.6, 0.2, 0.4)),
    )
    MAT['pindo_frond'] = principled('PindoFrond', hex_to_rgb('#3D5828'), roughness=0.75)
    MAT['fern_frond'] = principled('FernFrond', hex_to_rgb('#4A6A28'), roughness=0.75)
    MAT['agave_blade'] = principled(
        'AgaveBlade', COL['agave'], roughness=0.55,
        sss=(0.1, (0.5, 0.6, 0.4)),
    )
    MAT['anthurium_leaf'] = principled(
        'AnthuriumLeaf', hex_to_rgb('#2E4A1E'), roughness=0.42,
        sss=(0.08, (0.4, 0.55, 0.3)),
    )
    MAT['palm_thatch'] = add_noise_displacement(
        principled('PalmThatch', COL['palm_thatch'], roughness=0.88, sheen=0.25),
        scale=18.0, strength=0.04,
    )
