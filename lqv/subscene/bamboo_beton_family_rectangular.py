"""Sub-render: Bamboo + Beton Family Rectangular (~110 m², 4-bed rectangle).

Bypasses ``base.run()`` so we can:
  * pin ``cam.data.clip_end = base.PARCEL_CLIP_END_M`` (parcel-scale gotcha — the 1000 m
    default of ``base.run()`` clips the HDRI ground horizon and returns
    only an HDRI frame),
  * tune the camera for a south-east oblique composition that reads BOTH
    the north concrete service spine (high eave, 3.6 m, kitchen + 2 bath +
    laundry) AND the south bamboo porch (low eave, 2.4 m, 9 Guadua posts
    + palm-thatch overhang + lapacho ring beam) in the same frame.

Camera at ``(+14, -14, 6.0)`` looking at ``(0, -1.5, 1.5)`` — target
shifted ~1.5 m south so the porch reads as the foreground and the spine /
shed-roof slope reads as the background mass. 24 mm lens — wider than the
v30 28 mm driver because the 17 m long axis needs a generous field of
view to capture the full E-W run with a 60 cm margin on each gable end.

Three companion Guadua clumps land north of the building to soften the
concrete spine in the background (consistent with the curved sibling's
companion vegetation, but placed differently to suit the rectangular
massing).

Driver writes to
``renders/sub/runs/<RENDER_RUN_ID>_bamboo_beton_family_rectangular/<V>.png``
and mirrors to
``renders/sub/latest/bamboo_beton_family_rectangular_<V>.png``.
Default ``RENDER_RUN_ID`` =
``phase_e_bamboo_beton_family_rectangular_20260612`` (only used if the
caller does not pin one via env).
"""
from __future__ import annotations

import math
import os
import random
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

os.environ.setdefault('RENDER_RUN_ID', 'phase_e_bamboo_beton_family_rectangular_20260612')

import bpy  # noqa: F401  — kept for parity with sibling drivers

from lqv import cameras
from lqv.subscene import base

ASSET = 'bamboo_beton_family_rectangular'


def _companion_guadua_clumps(seed_salt: int = 0) -> None:
    """Place 3 Guadua clumps north of the building to soften the spine
    backdrop. Each clump is 5-9 culms in a 1.2 m radius cluster.

    Falls back silently if the bamboo helper cannot be imported (consistent
    with the in-typology fallback strategy).
    """
    try:
        from lqv.house.bamboo_frame import build_bamboo_culm
    except Exception:
        return

    rng = random.Random(20260609 ^ seed_salt)
    # 3 clump centres north of the building (Y >> 0), straddling the long axis.
    centres = [
        (-6.0, +6.0),
        (+0.0, +7.5),
        (+6.5, +6.2),
    ]
    for i, (cx, cy) in enumerate(centres):
        n_culms = rng.randint(5, 9)
        for j in range(n_culms):
            theta = rng.uniform(0.0, 2.0 * math.pi)
            r = rng.uniform(0.05, 1.2)
            px = cx + r * math.cos(theta)
            py = cy + r * math.sin(theta)
            base_z = 0.0
            top_z = rng.uniform(5.0, 8.5)
            # Slight lean off vertical to suggest clump habit.
            lean_x = rng.uniform(-0.2, 0.2)
            lean_y = rng.uniform(-0.2, 0.2)
            tip = (px + lean_x, py + lean_y, top_z)
            try:
                build_bamboo_culm(
                    p_start_xyz=(px, py, base_z),
                    p_end_xyz=tip,
                    diameter_m=rng.uniform(0.06, 0.10),
                    taper_ratio=0.85,
                    segments=10,
                    material='bamboo',
                    name=f'GuaduaClump_{i}_{j:02d}',
                )
            except Exception:
                # A single failed culm should not abort the render.
                continue


if __name__ == '__main__':
    from lqv.typologies.bamboo_beton_family_rectangular import (
        build_bamboo_beton_family_rectangular,
    )

    scene, cfg = base.setup(ASSET)
    base.place_neutral_ground('laterite', size=60.0)
    build_bamboo_beton_family_rectangular(origin=(0.0, 0.0, 0.0), variant=cfg.variant)
    _companion_guadua_clumps(seed_salt=ord(cfg.variant[0]) if cfg.variant else 0)

    cam = cameras.make_view_camera(
        cfg,
        target=(0.0, -1.5, 1.5),
        distance=14.0,
        height=6.0,
        lens=24.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.setup_world(scene, cfg.variant)
    base.save_subrender(scene, ASSET, cfg)
