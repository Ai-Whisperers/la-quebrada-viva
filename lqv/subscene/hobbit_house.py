"""Sub-render: Hobbit House typology (earth-bermed half-buried dwelling).

Bypasses ``base.run()`` so we can:
  * use a grass neutral ground (the structure sits in a hillside, not laterite),
  * set ``cam.data.clip_end`` explicitly above 100 m (parcel-scale-safe),
  * scatter green-roof plantings (anthuriums + tree fern) around the berm
    via the photoreal CC0 importers.
"""
from __future__ import annotations

import os
import random
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import bpy

from lqv import cameras
from lqv.subscene import base

ASSET = 'hobbit_house'


def _scatter_green_roof_planting():
    """Anthuriums + tree fern scattered across the berm + green roof.

    Photoreal imports are heavy; we keep counts low (5-8 anthuriums, 1-2 ferns)
    so the sub-render stays under the 60 s preview budget. RENDER_FLORA_PHOTOREAL
    gate is honoured — when off, skip entirely (the procedural fallback would
    pull in builders that aren't in scope here).
    """
    if os.environ.get('RENDER_FLORA_PHOTOREAL', '0') != '1':
        return
    from lqv.flora.photoreal import add_anthurium_photoreal, add_tree_fern_photoreal

    # Anthurium ring around the back of the berm, tucked just behind the dome.
    n_anth = random.randint(5, 8)
    for i in range(n_anth):
        # Distribute around a ~3.6 m radius arc on the +Y (back) side.
        t = (i + 0.5) / n_anth
        angle = 0.2 + t * 2.7  # radians, mostly behind the dome
        rx = 3.4 + random.uniform(-0.3, 0.3)
        x = rx * (1.0 - 2.0 * t) * 0.5 + random.uniform(-0.4, 0.4)
        y = 2.4 + random.uniform(-0.6, 0.6)
        z = 1.6 + random.uniform(-0.2, 0.4)
        try:
            obj = add_anthurium_photoreal(x=x, y=y, scale=1.0)
            obj.location = (x, y, z)
        except SystemExit:
            return  # missing asset — silently skip rather than abort

    # Tree fern at the SE corner of the berm — reads as wild planting.
    try:
        add_tree_fern_photoreal(x=3.2, y=1.6, scale=1.0)
    except SystemExit:
        pass


if __name__ == '__main__':
    from lqv.typologies.hobbit_house import build_hobbit_house

    scene, cfg = base.setup(ASSET)
    base.place_neutral_ground('laterite')  # grass not in MAT; laterite reads as earth
    build_hobbit_house(origin=(0.0, 0.0, 0.0))
    _scatter_green_roof_planting()

    # Camera from SE, looking at the south-facing round door at 1.4 m crown.
    cam = cameras.subscene_camera(
        target=(0.0, 0.0, 1.4),
        distance=9.0,
        height=4.0,
        lens=28.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.setup_world(scene, cfg.variant)
    base.save_subrender(scene, ASSET, cfg)
