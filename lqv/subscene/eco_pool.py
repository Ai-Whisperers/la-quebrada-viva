"""Sub-render: Eco Pool amenity (bamboo + stone wellness pool).

Bypasses :func:`lqv.subscene.base.run` so we can place the camera exactly at
the Wesley-brief coordinates and pin ``cam.data.clip_end`` to 20 km — the
default 100 m / 1000 m clips truncate parcel-scale shots and return only the
HDRI (``feedback_subscene_clip_end``). Pattern mirrors
:mod:`lqv.subscene.labrisa_lounge` so the rest of the Phase F batch reads
identically.
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv import cameras
from lqv.subscene import base

ASSET = 'eco_pool'

# Pin the run id so A/B/C variants of this batch land in the same folder even
# across multiple Blender invocations. Can be overridden by the caller env.
os.environ.setdefault('RENDER_RUN_ID', 'phase_f_eco_pool_20260613')


if __name__ == '__main__':
    from lqv.amenities.eco_pool import build as build_eco_pool

    scene, cfg = base.setup(ASSET)
    base.place_neutral_ground(material_key='grass')
    build_eco_pool(location=(0.0, 0.0, 0.0), variant=cfg.variant)
    base.setup_world(scene, cfg.variant)

    # Exact Wesley camera placement — `subscene_camera()` formula would
    # produce (+14, -14, 5.5) which slips the brief, so we bind directly.
    cam = cameras.add_camera(
        name='SubsceneCamera_EcoPool',
        location=(14.0, -10.0, 5.5),
        look_at=(0.0, 0.0, 1.0),
        lens=28.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.save_subrender(scene, ASSET, cfg)
