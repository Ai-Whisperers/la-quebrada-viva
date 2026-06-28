"""Sub-render: Eco Retreat / Modern Oasis amenity.

Wesley brief, Phase F (2026-06-13). Bypasses :func:`lqv.subscene.base.run` so
that the camera's ``clip_end`` can be explicitly raised to 20 km — the
default Blender clip_end of 100 m otherwise truncates the back-of-frame and
renders only the HDRI for parcel-scale shots (see
``memory/feedback_subscene_clip_end.md``).

Camera per brief: location (+16, -16, +7), aimed at (0, 0, 1.5), 28 mm lens.
"""
from __future__ import annotations

import os
import random
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import bpy  # noqa: F401  (ensure Blender Python is in scope before lqv imports)

from lqv import cameras, materials
from lqv.subscene import base

ASSET = 'eco_retreat_modern_oasis'


if __name__ == '__main__':
    # Pin the render-run identifier so all variants for this asset cluster in
    # the same `renders/sub/runs/phase_f_eco_retreat_20260613_*` folder unless
    # the caller already exported their own RENDER_RUN_ID.
    os.environ.setdefault('RENDER_RUN_ID', 'phase_f_eco_retreat_20260613')

    scene, cfg = base.setup(ASSET)
    base.place_neutral_ground(material_key='grass')

    # `base.setup` already calls `materials.build_materials()` and seeds the
    # RNG via `derive_seed(asset, variant)`. Re-do both defensively so the
    # asset's MATERIAL_TAKEOFF/build path is independent of upstream changes
    # to the helper — re-seeding with the same key is byte-identity safe.
    materials.build_materials()
    random.seed(base.derive_seed(ASSET, cfg.variant))

    from lqv.amenities.eco_retreat_modern_oasis import (
        build_eco_retreat_modern_oasis,
    )

    build_eco_retreat_modern_oasis(location=(0.0, 0.0, 0.0))

    base.setup_world(scene, cfg.variant)

    cam = cameras.make_view_camera(
        cfg,
        target=(0.0, 0.0, 1.5),
        distance=16.0,
        height=7.0,
        lens=28.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.save_subrender(scene, ASSET, cfg)
