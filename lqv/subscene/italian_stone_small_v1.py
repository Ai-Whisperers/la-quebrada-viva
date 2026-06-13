"""Sub-render: italian stone small v1 typology in isolation.

Bypasses ``base.run()`` so we can:
  * frame the south-facing front door from the 3/4-front hero angle,
  * tune the camera ``clip_end`` for the parcel-scale HDRI sun pass.
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv import cameras
from lqv.subscene import base

ASSET = 'italian_stone_small_v1'


if __name__ == '__main__':
    from lqv.typologies.italian_stone_small_v1 import build_italian_stone_small_v1

    scene, cfg = base.setup(ASSET)
    base.place_neutral_ground('laterite')
    build_italian_stone_small_v1(origin=(0.0, 0.0, 0.0))

    cam = cameras.subscene_camera(
        target=(0.0, 0.0, 1.4),
        distance=10.0,
        height=4.0,
        lens=28.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.setup_world(scene, cfg.variant)
    base.save_subrender(scene, ASSET, cfg)
