"""Earth-family materials: lime wash, cob, laterite, sandstone, moss, stream bed."""
from __future__ import annotations

from lqv.materials._palette import COL, hex_to_rgb
from lqv.materials._shaders import (
    add_noise_displacement,
    add_secondary_color_variation,
    principled,
    textured_principled,
)


def build(MAT: dict) -> None:
    """Populate MAT with earth-family entries.

    Beauty pass 2026-06-14: lime_wash and cob_raw upgraded from flat principled
    + noise bump to full PBR (beige_wall_002 / damaged_plaster) tinted toward
    the cob palette. Supersedes the 85e86aa byte-freeze (user-authorized;
    escritura beauty sprint).
    """
    MAT['lime_wash'] = textured_principled(
        'LimeWash', 'beige_wall_002',
        uv_scale=1.0 / 2.0,
        tint_color=COL['cob_lime_white'], tint_fac=0.55,
        roughness_bias=+0.08,
        displacement_strength=0.04,
        normal_strength=1.0,
    )
    MAT['cob_raw'] = textured_principled(
        'CobRaw', 'damaged_plaster',
        uv_scale=1.0 / 2.5,
        tint_color=COL['cob_raw'], tint_fac=0.50,
        roughness_bias=+0.05,
        displacement_strength=0.10,
        normal_strength=1.4,
    )
    # Ground PBR per asset_plan.md §C.2. Tint multiplies the Diffuse toward
    # the brief palette so Paraguayan laterite reads warm-red regardless of
    # the Poly Haven source plate.
    MAT['laterite'] = textured_principled(
        'Laterite', 'aerial_mud_1',
        uv_scale=1.0 / 8.0,  # 8m tile across hero camera frame
        tint_color=COL['laterite_dry'], tint_fac=0.65,
        displacement_strength=0.04,
    )
    # Anti-corduroy: break the single-tile UV stripe with a 2.5m-period
    # secondary color blend. Non-clobbering helper preserves the PBR diffuse.
    add_secondary_color_variation(
        MAT['laterite'],
        scale=2.5,
        color_a=hex_to_rgb('#8B3A1F'),
        color_b=hex_to_rgb('#A85832'),
        mix_fac=0.35,
    )
    MAT['sandstone'] = textured_principled(
        'Sandstone', 'dry_riverbed_rock',
        uv_scale=1.0 / 4.0,  # ~4m tile so boulder grain reads at hero distance
        tint_color=COL['sandstone_lit'], tint_fac=0.30,
        displacement_strength=0.06,
        normal_strength=1.2,
    )
    MAT['moss'] = textured_principled(
        'Moss', 'aerial_grass_rock',
        uv_scale=1.0 / 6.0,
        tint_color=COL['moss_wet'], tint_fac=0.35,
        displacement_strength=0.03,
    )
    MAT['stream_bed'] = textured_principled(
        'StreamBed', 'dry_riverbed_rock',
        uv_scale=1.0 / 3.0,
        tint_color=hex_to_rgb('#5A4E3C'), tint_fac=0.40,
        displacement_strength=0.04,
    )
    MAT['terracotta_tile'] = add_noise_displacement(
        principled('TerracottaTile', COL['terracotta_tile'], roughness=0.62),
        scale=24.0, strength=0.025,
    )
    MAT['concrete_slab_108'] = add_noise_displacement(
        principled('ConcreteSlab108', COL['concrete_slab_108'], roughness=0.78),
        scale=18.0, strength=0.015,
    )
