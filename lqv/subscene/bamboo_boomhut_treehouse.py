"""Sub-render: bamboo boomhut treehouse typology in isolation.

Bypasses ``base.run()`` because the camera must clip out to 20 km — parcel-scale
clip_end (feedback_subscene_clip_end). The asset is hosted by 3 lapacho trunks
+ a 4th stair-tower trunk; camera framed at z=4 m (deck level) from 14 m.
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv import cameras
from lqv.subscene import base

ASSET = 'bamboo_boomhut_treehouse'


def main():
    scene, cfg = base.setup(ASSET)
    base.place_neutral_ground('grass')

    from lqv.typologies.bamboo_boomhut_treehouse import build_bamboo_boomhut_treehouse
    build_bamboo_boomhut_treehouse(origin=(0.0, 0.0, 0.0))

    cam = cameras.make_view_camera(
        cfg,
        target=(0.0, 0.0, 4.0),
        distance=14.0,
        height=6.0,
        lens=28.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.setup_world(scene, cfg.variant)
    return base.save_subrender(scene, ASSET, cfg)


if __name__ == '__main__':
    main()
