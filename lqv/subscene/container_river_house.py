"""Sub-render: container river house (single 20 ft, riverside cantilever).

Bypasses ``base.run()`` so we can:
  * place a small water-surface plane on the +X side (river stand-in),
  * tune the camera offset / clip_end for the bank-side framing.
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

ASSET = 'container_river_house'


def _place_river(width: float = 14.0, length: float = 24.0,
                 x_offset: float = 6.0, z_drop: float = -0.4):
    """Small water plane on the +X side to read as 'river bank' edge."""
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(x_offset, 0.0, z_drop))
    obj = bpy.context.active_object
    obj.name = 'CRH_River'
    obj.scale = (width, length, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mat = MAT.get('water_reflective') or MAT.get('pool_water') or MAT.get('stream_bed')
    if mat is not None:
        assign(obj, mat)
    return obj


if __name__ == '__main__':
    from lqv.typologies.container_river_house import build_container_river_house

    scene, cfg = base.setup(ASSET)
    base.place_neutral_ground('laterite')
    _place_river()
    build_container_river_house(origin=(0.0, 0.0, 0.0))

    cam = cameras.make_view_camera(
        cfg,
        target=(0.0, 0.0, 1.8),
        distance=12.0,
        height=4.0,
        lens=28.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.setup_world(scene, cfg.variant)
    base.save_subrender(scene, ASSET, cfg)
