"""Sub-render: Floating Dining amenity.

Bypasses :func:`lqv.subscene.base.run` so we can pin the camera ``clip_end``
explicitly (per ``feedback_subscene_clip_end`` — the default 100 m clip
truncates the back-of-frame on parcel-scale shots and renders nothing but
HDRI). Pattern lifted from :mod:`lqv.subscene.labrisa_lounge`.

The amenity itself already drops its 14 × 10 m reflective water plane, so we
do NOT call ``base.place_neutral_ground`` — a laterite plane at z=0 would
clash with the water plane and kill the float read.
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import bpy  # noqa: F401  (imported for side-effects via lqv.cameras)

from lqv import cameras
from lqv.subscene import base

ASSET = 'floating_dining'


if __name__ == '__main__':
    from lqv.amenities.floating_dining import build as build_floating_dining

    scene, cfg = base.setup(ASSET)
    # Intentionally skip place_neutral_ground — the amenity's own water plane
    # (14 × 10 m) is the visible ground surface. Adding laterite at z=0 would
    # poke through and break the reflection.
    build_floating_dining(location=(0.0, 0.0, 0.0), variant=cfg.variant)

    # Camera: brief calls for location (+12, -12, 4.5) target (0, 0, 1.6).
    # subscene_camera places at (tx+distance, ty-distance, height) so the
    # (distance=12, height=4.5) pair satisfies that exactly.
    cam = cameras.subscene_camera(
        target=(0.0, 0.0, 1.6),
        distance=12.0,
        height=4.5,
        lens=35.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.setup_world(scene, cfg.variant)
    base.save_subrender(scene, ASSET, cfg)
