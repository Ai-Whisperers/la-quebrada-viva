"""Sub-render: Bamboo + Beton 28 m² (§3.10, hybrid 1 PAX solo unit).

Smaller sibling of ``bamboo_beton_30``. Bypasses ``base.run()`` for the same
reason — pin ``cam.data.clip_end = base.PARCEL_CLIP_END_M`` so the parcel-scale gotcha
(default 1000 m clip clipping terrain → HDRI-only frame) doesn't fire.

Camera at ``(+sin θ · 11, -cos θ · 11, 4.0)`` looking at ``(0, 0, 1.4)`` —
closer + lower than v30 because this is a smaller building and we want the
1 PAX intimacy + the long 8 m porch face to dominate the frame. 28 mm lens.

Output:
  * ``renders/sub/runs/<RENDER_RUN_ID>_bamboo_beton_28/<V>.png``
  * mirrored to ``renders/sub/latest/bamboo_beton_28_<V>.png``
  * legacy flat at ``renders/sub/bamboo_beton_28_<V>.png``

If ``RENDER_RUN_ID`` is not set, defaults to ``phase_e_bamboo_beton_28_20260612``
to keep this typology's batch grouped with the rest of Phase E wave 2.
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# Default RENDER_RUN_ID for this typology before importing base (base reads env at import).
os.environ.setdefault('RENDER_RUN_ID', 'phase_e_bamboo_beton_28_20260612')

import bpy  # noqa: F401  — kept for parity with sibling drivers

from lqv import cameras
from lqv.subscene import base

ASSET = 'bamboo_beton_28'


if __name__ == '__main__':
    from lqv.typologies.bamboo_beton_28 import build_bamboo_beton_28

    scene, cfg = base.setup(ASSET)
    base.place_neutral_ground('laterite')
    build_bamboo_beton_28(origin=(0.0, 0.0, 0.0), variant=cfg.variant)

    cam = cameras.make_view_camera(
        cfg,
        target=(0.0, 0.0, 1.4),
        distance=11.0,
        height=4.0,
        lens=28.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.setup_world(scene, cfg.variant)
    base.save_subrender(scene, ASSET, cfg)
