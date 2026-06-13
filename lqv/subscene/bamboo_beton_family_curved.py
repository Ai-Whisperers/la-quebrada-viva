"""Sub-render: Bamboo + Beton Family Curved (~110 m², crescent 4-bed).

Bypasses ``base.run()`` so we can:
  * pin ``cam.data.clip_end = base.PARCEL_CLIP_END_M`` (parcel-scale gotcha — the 1000 m
    default of ``base.run()`` clips the HDRI ground horizon and returns
    only an HDRI frame),
  * tune the camera for an oblique SE composition that reads BOTH the
    concave porch line (with bamboo posts + curtains + low palm-thatch eave)
    AND the convex concrete back (with high spine + clerestories) in the
    same frame.

Camera at ``(+18, -18, 6.0)`` looking at ``(0, -2, 1.5)`` — target shifted
~2 m south (into the courtyard) so the crescent reads end-on rather than
flat. 24 mm lens — wider than the v30 28 mm driver because the 14 m outer
radius needs the field of view to fit the whole arc with breathing room
for the curtain bay textiles to be readable.

Driver writes to
``renders/sub/runs/<RENDER_RUN_ID>_bamboo_beton_family_curved/<V>.png`` and
mirrors to ``renders/sub/latest/bamboo_beton_family_curved_<V>.png``.
Default ``RENDER_RUN_ID`` = ``phase_e_bamboo_beton_family_curved_20260612``
(only used if the caller does not pin one via env).
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

os.environ.setdefault('RENDER_RUN_ID', 'phase_e_bamboo_beton_family_curved_20260612')

import bpy  # noqa: F401  — kept for parity with sibling drivers

from lqv import cameras
from lqv.subscene import base

ASSET = 'bamboo_beton_family_curved'


if __name__ == '__main__':
    from lqv.typologies.bamboo_beton_family_curved import (
        build_bamboo_beton_family_curved,
    )

    scene, cfg = base.setup(ASSET)
    base.place_neutral_ground('laterite', size=60.0)
    build_bamboo_beton_family_curved(origin=(0.0, 0.0, 0.0), variant=cfg.variant)

    cam = cameras.subscene_camera(
        target=(0.0, -2.0, 1.5),
        distance=18.0,
        height=6.0,
        lens=24.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.setup_world(scene, cfg.variant)
    base.save_subrender(scene, ASSET, cfg)
