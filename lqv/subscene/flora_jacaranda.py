"""Sub-render: photoreal jacaranda_tree against neutral laterite.

Mirrors hobbit_house.py: bypass base.run() so we can set clip_end=20000
after camera assignment (parcel-scale gotcha) and loop A/B/C per invocation.
"""
from __future__ import annotations

import os
import random
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import bpy

from lqv import cameras, config
from lqv.subscene import base

ASSET = 'flora_jacaranda'


def _place_jacarandas():
    if os.environ.get('RENDER_FLORA_PHOTOREAL', '0') != '1':
        return
    from lqv.flora.photoreal import (
        _append_object_from_blend,
        _scale_to_height,
        JACARANDA_BLEND,
        TARGET_HEIGHTS,
    )

    # Hero tree centered, scaled to ~12 m (mid jacaranda height).
    hero = _append_object_from_blend(JACARANDA_BLEND)
    hero.location = (0.0, 0.0, 0.0)
    hero.rotation_euler = (0.0, 0.0, random.uniform(0.0, 6.283))
    _scale_to_height(hero, 12.0)

    # 50% chance of a second smaller specimen offset to NE for compositional weight.
    if random.random() < 0.5:
        second = _append_object_from_blend(JACARANDA_BLEND)
        second.location = (4.5 + random.uniform(-0.4, 0.4),
                           3.2 + random.uniform(-0.4, 0.4), 0.0)
        second.rotation_euler = (0.0, 0.0, random.uniform(0.0, 6.283))
        _scale_to_height(second, 9.5)


def _render_variant(variant: str):
    os.environ['RENDER_VARIANT'] = variant
    cfg = config.parse()
    scene, cfg = base.setup(ASSET, cfg)
    base.place_neutral_ground('laterite')
    _place_jacarandas()

    cam = cameras.subscene_camera(
        target=(0.0, 0.0, 4.0),
        distance=22.0,
        height=8.0,
        lens=35.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.setup_world(scene, cfg.variant)
    base.save_subrender(scene, ASSET, cfg)


if __name__ == '__main__':
    for v in ('A', 'B', 'C'):
        _render_variant(v)
