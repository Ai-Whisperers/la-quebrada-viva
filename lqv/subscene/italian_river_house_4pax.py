"""Sub-render: italian river house (2-story, 4-pax) typology in isolation.

Bypasses ``base.run()`` so we can set a parcel-scale ``camera.clip_end`` and
add a small river plane on the north side of the house (the loggia side).
See ``memory/feedback_subscene_clip_end.md`` for the gotcha.
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import bpy

from lqv import cameras
from lqv.materials import MAT, assign
from lqv.subscene import base

ASSET = 'italian_river_house_4pax'


def _river_plane():
    """~20 m × 8 m water plane on the north (river) face of the house."""
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0.0, 9.0, 0.02))
    plane = bpy.context.active_object
    plane.name = 'IRH_RiverSurface'
    plane.scale = (20.0, 8.0, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    water = MAT.get('water_reflective') or MAT.get('stream_bed')
    if water is not None:
        assign(plane, water)
    return plane


def _build():
    from lqv.typologies.italian_river_house_4pax import (
        build_italian_river_house_4pax,
    )
    build_italian_river_house_4pax(origin=(0.0, 0.0, 0.0))


def main():
    scene, cfg = base.setup(ASSET)

    # Neutral laterite ground (40 m square)
    base.place_neutral_ground(material_key='laterite', size=40.0)

    # River plane on the loggia (north) side
    _river_plane()

    # Build the typology
    _build()

    # Hero camera: 3/4 view of loggia + river + arched base
    cam = cameras.subscene_camera(
        target=(0.0, 1.5, 2.8),
        distance=14.0,
        height=6.0,
        lens=28.0,
    )
    scene.camera = cam
    # Parcel-scale safety — base.run() defaults to 1000 m; we go far past that
    # in case the HDRI/sun horizon needs to be visible from a low camera.
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.setup_world(scene, cfg.variant)
    base.save_subrender(scene, ASSET, cfg)


if __name__ == '__main__':
    main()
