"""Brick/clay-family materials: red brick, castle brick, clay block, clay plaster.

PBR sets fetched into ``assets/textures/<asset_id>/`` via
``scripts/download_assets.sh``. Each material follows the standard Poly Haven
slot naming consumed by :func:`lqv.materials._shaders.textured_principled`
(Diffuse / nor_gl / Rough / AO / Displacement 4k JPGs). UV scale is the
default 1.0 — these read as wall panels at conversation distance.
"""
from __future__ import annotations

from lqv.materials._shaders import textured_principled


def build(MAT: dict) -> None:
    """Populate MAT with brick/clay-family entries.

    No tint — Poly Haven plates already sit in the warm-earth band that
    matches the Paraguayan palette, so an additional tint would push the
    brick reads toward laterite and lose the brick identity.
    """
    MAT['red_brick'] = textured_principled(
        'RedBrick', 'red_brick_03',
        uv_scale=1.0,
        displacement_strength=0.04,
        normal_strength=1.2,
    )
    MAT['castle_brick'] = textured_principled(
        'CastleBrick', 'castle_brick_02_red',
        uv_scale=1.0,
        displacement_strength=0.05,
        normal_strength=1.3,
    )
    MAT['clay_block'] = textured_principled(
        'ClayBlock', 'clay_block_wall',
        uv_scale=1.0,
        displacement_strength=0.04,
        normal_strength=1.1,
    )
    MAT['clay_plaster'] = textured_principled(
        'ClayPlaster', 'clay_plaster',
        uv_scale=1.0,
        displacement_strength=0.02,
        normal_strength=1.0,
    )
