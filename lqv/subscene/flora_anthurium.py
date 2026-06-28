"""Sub-render: photoreal anthurium_botany_01 cluster (3-5) on laterite.

Mirrors hobbit_house.py: bypass base.run() so we can set clip_end=20000
after camera assignment and loop A/B/C per invocation.
"""
from __future__ import annotations

import math
import os
import random
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


from lqv import cameras, config
from lqv.subscene import base

ASSET = 'flora_anthurium'


def _place_anthurium_cluster():
    if os.environ.get('RENDER_FLORA_PHOTOREAL', '0') != '1':
        return
    from lqv.flora.photoreal import (
        ANTHURIUM_BLEND,
        TARGET_HEIGHTS,
        _append_object_from_blend,
        _scale_to_height,
    )

    n = random.randint(3, 5)
    base_h = TARGET_HEIGHTS['anthurium']  # ~0.5 m
    for i in range(n):
        # Loose ring of radius 0.25-0.45 m around origin.
        angle = (i / n) * 2.0 * math.pi + random.uniform(-0.3, 0.3)
        radius = random.uniform(0.20, 0.45)
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        obj = _append_object_from_blend(ANTHURIUM_BLEND)
        obj.location = (x, y, 0.0)
        obj.rotation_euler = (0.0, 0.0, random.uniform(0.0, 6.283))
        _scale_to_height(obj, base_h * random.uniform(0.85, 1.15))


def _render_variant(variant: str):
    os.environ['RENDER_VARIANT'] = variant
    cfg = config.parse()
    scene, cfg = base.setup(ASSET, cfg)
    base.place_neutral_ground('laterite')
    _place_anthurium_cluster()

    cam = cameras.make_view_camera(
        cfg,
        target=(0.0, 0.0, 0.4),
        distance=2.5,
        height=1.2,
        lens=50.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.setup_world(scene, cfg.variant)
    base.save_subrender(scene, ASSET, cfg)


if __name__ == '__main__':
    for v in ('A', 'B', 'C'):
        _render_variant(v)
