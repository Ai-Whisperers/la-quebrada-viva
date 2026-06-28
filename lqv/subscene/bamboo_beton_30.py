"""Sub-render: Bamboo + Beton 30 m² (§3.10, hybrid 2 PAX couple unit).

Bypasses ``base.run()`` so we can:
  * pin ``cam.data.clip_end = base.PARCEL_CLIP_END_M`` (parcel-scale gotcha — the 1000 m
    default of ``base.run()`` clips terrain backdrops and returns an HDRI-only
    frame),
  * tune target / distance / lens for the SE oblique that catches both the
    bamboo south porch + the polished-concrete service spine on the rear.

Camera at ``(+12, -12, 4.5)`` looking at ``(0, 0, 1.6)`` (eye-level on the
porch deck, slightly above the lapacho door header), 28 mm lens — wide enough
to bring the full 6 m × 5 m footprint into frame with breathing room for the
90 cm south overhang to read as a porch eave.

Driver writes to ``renders/sub/runs/<RENDER_RUN_ID>_bamboo_beton_30/<V>.png``
and mirrors to ``renders/sub/latest/bamboo_beton_30_<V>.png``.
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import bpy  # noqa: F401  — kept for parity with sibling drivers

from lqv import cameras
from lqv.subscene import base

ASSET = 'bamboo_beton_30'


if __name__ == '__main__':
    from lqv.typologies.bamboo_beton_30 import build_bamboo_beton_30

    scene, cfg = base.setup(ASSET)
    base.place_neutral_ground('laterite')
    build_bamboo_beton_30(origin=(0.0, 0.0, 0.0), variant=cfg.variant)

    cam = cameras.make_view_camera(
        cfg,
        target=(0.0, 0.0, 1.6),
        distance=12.0,
        height=4.5,
        lens=28.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.setup_world(scene, cfg.variant)
    base.save_subrender(scene, ASSET, cfg)
