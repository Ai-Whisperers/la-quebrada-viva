"""Sub-render: bamboo wigwam lodge (single 2 PAX glamping cone).

Bypasses ``base.run()`` so we can:
  * pin ``cam.data.clip_end = base.PARCEL_CLIP_END_M`` BEFORE ``render.run(scene)`` (parcel-
    scale clip-gotcha — see ``feedback_subscene_clip_end`` memory),
  * scatter a couple of small Guadua clumps around the lodge so the eye reads
    "bamboo grows here" rather than "thatched cone on bare grass".
"""
from __future__ import annotations

import os
import random
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


from lqv import cameras
from lqv.subscene import base

ASSET = 'bamboo_wigwam_lodge'


def _scatter_companion_bamboo(seed: int) -> None:
    """Drop 3 small Guadua clumps in a loose halo behind / beside the lodge.

    Kept procedural even when ``RENDER_FLORA_PHOTOREAL=1`` — bamboo has no CC0
    photoreal proxy in the Poly Haven catalog (see ``flora/photoreal.py`` note).
    """
    try:
        from lqv.flora.bamboo import add_bamboo_clump
    except Exception:
        return
    rng = random.Random(seed ^ 0x7A2B11)
    placements = (
        (-3.6, -2.4, 1.0),
        (-2.8,  3.2, 0.9),
        ( 4.0,  2.6, 1.1),
    )
    for x, y, scale in placements:
        jitter_x = x + rng.uniform(-0.25, 0.25)
        jitter_y = y + rng.uniform(-0.25, 0.25)
        add_bamboo_clump(jitter_x, jitter_y, n=rng.randint(6, 9), scale=scale)


if __name__ == '__main__':
    from lqv.typologies.bamboo_wigwam_lodge import build_bamboo_wigwam_lodge

    scene, cfg = base.setup(ASSET)

    # Neutral ground — laterite reads as cleared yard around the cone, which
    # is more honest for a glamping pad than full canopy grass.
    base.place_neutral_ground('laterite')

    # Pin RNG AFTER setup (materials already built inside base.setup) and
    # BEFORE the first build_*, per project RNG invariant.
    asset_seed = base.derive_seed(ASSET, cfg.variant) if hasattr(base, 'derive_seed') else 20260612
    random.seed(asset_seed)

    build_bamboo_wigwam_lodge(origin=(0.0, 0.0, 0.0), variant=cfg.variant)
    _scatter_companion_bamboo(asset_seed)

    cam = cameras.subscene_camera(
        target=(0.0, 0.0, 2.0),
        distance=11.0,
        height=4.5,
        lens=28.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M   # parcel-scale clip gotcha

    base.setup_world(scene, cfg.variant)
    base.save_subrender(scene, ASSET, cfg)
