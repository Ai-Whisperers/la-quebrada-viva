"""Sub-render: house-scale terrain DSL smoke test.

Phase B done-criterion driver. Instantiates an 80 m x 60 m parcel with one
hill, one creek, one river, two tree scatters, and one house pad. Asserts
``Terrain.validate_geo()`` returns ``[]`` before rendering.

Critical: this driver bypasses ``base.run()`` because parcel-scale shots need
``cam.data.clip_end`` >> default 100 m, or the render returns only the HDRI
(memory ``feedback_subscene_clip_end``). We call ``base.setup()`` directly,
build the terrain, wire the camera by hand, set ``clip_end = 20000.0`` on the
camera data, then ``base.save_subrender()``.
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


from lqv import cameras
from lqv.site.terrain_dsl import Terrain
from lqv.subscene import base

ASSET = 'terrain_house_scale'


def _build_smoke_terrain() -> Terrain:
    """80 m x 60 m smoke parcel; origin centered so x in [-40, 40], y in [-30, 30]."""
    t = Terrain(width_m=80.0, depth_m=60.0, cell_m=0.5,
                origin=(-40.0, -30.0), z_clip_end=20000.0)

    # Hill east of center — the "behind the house" ridge.
    t.hill(center=(15.0, 10.0), radius_m=18.0, height_m=4.0, falloff='gaussian')

    # Creek descends from the hill flank toward the river.
    t.creek(
        polyline=[(12.0, 18.0), (8.0, 8.0), (4.0, -2.0), (0.0, -12.0)],
        width_m=1.5, depth_m=0.4, bed_material='river_cobble',
    )

    # River along the south edge (the single-river invariant).
    t.river(
        polyline=[(-38.0, -22.0), (-10.0, -20.0), (20.0, -19.0), (38.0, -22.0)],
        width_m=8.0, depth_m=1.2, bed_material='river_sand',
    )

    # Two scatters: lapacho on the upper slope, mango on the mid-flat.
    t.tree_scatter(
        polygon=[(-30.0, 5.0), (-10.0, 8.0), (-12.0, 25.0), (-32.0, 22.0)],
        species='lapacho', density_per_ha=120.0, jitter=0.4, seed=4221,
    )
    t.tree_scatter(
        polygon=[(20.0, -5.0), (35.0, -5.0), (35.0, 8.0), (20.0, 8.0)],
        species='mango', density_per_ha=80.0, jitter=0.35, seed=4222,
    )

    # One house pad — 8 m x 6 m rectangle, snap='pad', on the mid-flat
    # west of the creek (clear of the scatters' AABBs).
    t.place_house(
        footprint=((-4.0, -3.0), (4.0, -3.0), (4.0, 3.0), (-4.0, 3.0)),
        xy=(-8.0, -5.0), rotation_deg=15.0, snap='pad', pad_size_m=1.5,
    )
    return t


def main():
    scene, cfg = base.setup(ASSET)
    # No neutral ground — the terrain mesh IS the ground.
    terrain = _build_smoke_terrain()

    issues = terrain.validate_geo()
    if issues:
        raise SystemExit(
            f"[subscene:{ASSET}] validate_geo() failed: {issues!r}"
        )
    print(f"[subscene:{ASSET}] validate_geo() OK")

    # Camera FIRST so to_blender() can lift clip_end on it.
    cam = cameras.make_view_camera(
        cfg,
        target=(0.0, 0.0, 1.5),
        distance=70.0,
        height=22.0,
        lens=28.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M  # explicit, per feedback_subscene_clip_end

    terrain.to_blender()

    # Verify clip_end survived (to_blender() also lifts it, redundant guard).
    assert cam.data.clip_end >= terrain.z_clip_end, (
        f"clip_end={cam.data.clip_end} < z_clip_end={terrain.z_clip_end}"
    )

    base.setup_world(scene, cfg.variant)
    base.save_subrender(scene, ASSET, cfg)


if __name__ == '__main__':
    main()
