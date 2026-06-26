"""Sub-render: Labrisa Lounge amenity (creek-through bamboo pavilion).

Bypasses :func:`lqv.subscene.base.run` so we can pin the camera ``clip_end``
explicitly (per ``feedback_subscene_clip_end`` — the default 100 m clip
truncates the back-of-frame on parcel-scale shots and renders nothing but
HDRI). Pattern lifted from
:mod:`lqv.subscene.container_river_house`.
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

ASSET = 'labrisa_lounge'


def _place_creek_water(width: float = 14.0, length: float = 1.4, z: float = 0.04):
    """Thin reflective water strip beneath the deck cut-out.

    The lounge builder already drops a glass slab into the creek channel; this
    underplane reads through the gap and gives the cascade weir something to
    spill onto.
    """
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0.0, 0.0, z))
    obj = bpy.context.active_object
    obj.name = 'LabrisaCreek_Water'
    obj.scale = (width, length, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mat = MAT.get('water_reflective') or MAT.get('pool_water') or MAT.get('stream_bed')
    if mat is not None:
        assign(obj, mat)
    return obj


if __name__ == '__main__':
    from lqv.amenities.labrisa_lounge import build as build_labrisa_lounge

    scene, cfg = base.setup(ASSET)
    base.place_neutral_ground('laterite')
    _place_creek_water()
    build_labrisa_lounge(location=(0.0, 0.0, 0.0), variant=cfg.variant)

    cam = cameras.make_view_camera(
        cfg,
        target=(0.0, 0.0, 1.6),
        distance=14.0,
        height=5.0,
        lens=28.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.setup_world(scene, cfg.variant)
    base.save_subrender(scene, ASSET, cfg)
