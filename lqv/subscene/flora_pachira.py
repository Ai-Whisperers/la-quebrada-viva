"""Sub-render: photoreal pachira_aquatica_01 specimen on laterite.

Mirrors hobbit_house.py: bypass base.run() so we can set clip_end=20000
after camera assignment and loop A/B/C per invocation.
"""
from __future__ import annotations

import os
import random
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


from lqv import cameras, config
from lqv.subscene import base

ASSET = 'flora_pachira'


def _place_pachira():
    if os.environ.get('RENDER_FLORA_PHOTOREAL', '0') != '1':
        return
    from lqv.flora.photoreal import (
        PACHIRA_BLEND,
        _append_object_from_blend,
        _scale_to_height,
    )

    hero = _append_object_from_blend(PACHIRA_BLEND)
    hero.location = (0.0, 0.0, 0.0)
    hero.rotation_euler = (0.0, 0.0, random.uniform(0.0, 6.283))
    _scale_to_height(hero, 4.0)  # mid pachira height (3-5 m range)


def _render_variant(variant: str):
    os.environ['RENDER_VARIANT'] = variant
    cfg = config.parse()
    scene, cfg = base.setup(ASSET, cfg)
    base.place_neutral_ground('laterite')
    _place_pachira()

    cam = cameras.subscene_camera(
        target=(0.0, 0.0, 1.8),
        distance=10.0,
        height=3.5,
        lens=35.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.setup_world(scene, cfg.variant)
    base.save_subrender(scene, ASSET, cfg)


if __name__ == '__main__':
    for v in ('A', 'B', 'C'):
        _render_variant(v)
