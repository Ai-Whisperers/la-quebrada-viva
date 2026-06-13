"""Prop materials: anodized steel, PV cover glass, steel mesh, window glow, firefly.

PV cover glass lives here (not glass.py) because it tracks the Rule-9 PV array
prop group rather than the bottle-glass tinted-transmission family.
"""
from __future__ import annotations

from lqv.materials._palette import COL, hex_to_rgb
from lqv.materials._shaders import principled


def build(MAT: dict) -> None:
    """Populate MAT with prop-family entries.

    Builder calls + parameters are byte-identical to the pre-split monolith;
    do not retune without re-rendering the 18 finals at 85e86aa.
    """
    MAT['steel_anodized'] = principled(
        'SteelAnodized', hex_to_rgb('#2A2A2C'), roughness=0.42, metallic=0.92, ior=1.45,
    )
    MAT['pv_glass'] = principled(
        'PvGlass', hex_to_rgb('#0A1A2A'), roughness=0.12, metallic=0.0, ior=1.5,
    )
    MAT['steel_mesh'] = principled(
        'SteelMesh', hex_to_rgb('#3A3A3D'), roughness=0.32, metallic=0.85, ior=1.45, alpha=0.55,
    )
    MAT['window_glow'] = principled(
        'WindowGlow', hex_to_rgb('#FFC76A'), roughness=0.5,
        emission_color=hex_to_rgb('#FFB252'), emission_strength=12.0,
    )
    MAT['firefly'] = principled(
        'Firefly', hex_to_rgb('#FFFF80'),
        emission_color=hex_to_rgb('#E6FF80'), emission_strength=80.0,
    )
    MAT['rope_natural'] = principled(
        'RopeNatural', COL['rope_natural'], roughness=0.88,
    )
