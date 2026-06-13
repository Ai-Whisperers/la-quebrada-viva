"""Sub-render: italian stone small v2 (side-loggia 2BR) in isolation.

Bypasses ``base.run()`` so we can:
  * frame the south face + east loggia together from the SE 3/4 hero angle,
  * tune the camera ``clip_end`` so the parcel-scale HDRI sun pass renders
    properly (default 100 m clip cuts the sky out at this scale).

Default ``RENDER_RUN_ID`` is set to ``phase_e_italian_stone_small_v2_20260612``
when the caller doesn't pin one; this groups the A/B/C variants of the v2
batch in a single run folder under ``renders/sub/runs/``.
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

ASSET = 'italian_stone_small_v2'

os.environ.setdefault('RENDER_RUN_ID', 'phase_e_italian_stone_small_v2_20260612')


if __name__ == '__main__':
    # Re-set the default run id AFTER importing base (which captured _RUN_ID at
    # module load). The base module reads RENDER_RUN_ID lazily via run_dir().
    import lqv.subscene.base as _b
    _b._RUN_ID = os.environ['RENDER_RUN_ID']

    from lqv.typologies.italian_stone_small_v2 import build_italian_stone_small_v2

    scene, cfg = base.setup(ASSET)
    # Re-seed AFTER materials.build_materials() per project plan, BEFORE
    # any build_* call — keeps the per-asset RNG stream stable across runs.
    random.seed(int(os.environ.get('SEED', '20260609')))

    base.place_neutral_ground('laterite')
    build_italian_stone_small_v2(origin=(0.0, 0.0, 0.0))

    cam = cameras.subscene_camera(
        target=(1.5, 0.0, 1.6),  # bias east so loggia stays in frame
        distance=12.0,
        height=4.5,
        lens=28.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.setup_world(scene, cfg.variant)
    base.save_subrender(scene, ASSET, cfg)
