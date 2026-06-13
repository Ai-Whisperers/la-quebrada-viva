"""Sub-render driver — bamboo river house typology over a river surface.

This driver bypasses ``base.run()`` because the asset sits over a ~30 m
river plane which would otherwise be clipped at the default 100 m camera
``clip_end`` and only the HDRI sky would render. The parcel-scale clip_end
gotcha (see ``memory/feedback_subscene_clip_end.md``) applies here.
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


ASSET = 'bamboo_river_house'

# River surface dimensions (m). Long axis along Y matches the house orientation.
_RIVER_LENGTH_Y = 30.0
_RIVER_WIDTH_X = 12.0
_RIVER_Z = 0.0


def _add_river_surface():
    """Build a flat water surface under the house, replacing the central patch
    of the neutral ground plane. Slightly larger than the platform footprint
    to read as a real river bed."""
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0.0, 0.0, _RIVER_Z + 0.02))
    plane = bpy.context.active_object
    plane.name = 'BRH_RiverSurface'
    plane.scale = (_RIVER_WIDTH_X, _RIVER_LENGTH_Y, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    water = MAT.get('pool_water') or MAT.get('water_reflective')
    if water is not None:
        assign(plane, water)
    return plane


def _add_bank_strip():
    """Bank strip (north side) where the suspended walkway lands — gravel/laterite."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 9.5, 0.5))
    bank = bpy.context.active_object
    bank.name = 'BRH_Bank'
    bank.scale = (16.0, 6.0, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mat = MAT.get('laterite') or MAT.get('stream_bed')
    if mat is not None:
        assign(bank, mat)
    return bank


def main():
    scene, cfg = base.setup(ASSET)
    base.place_neutral_ground(material_key='laterite', size=80.0)
    _add_river_surface()
    _add_bank_strip()

    from lqv.typologies.bamboo_river_house import build_bamboo_river_house
    build_bamboo_river_house(origin=(0.0, 0.0, 0.0))

    cam = cameras.subscene_camera(
        target=(0.0, 0.0, 1.8),
        distance=14.0,
        height=4.5,
        lens=28.0,
    )
    scene.camera = cam
    # Parcel-scale clip_end gotcha — must be set explicitly because the river
    # plane + bank extend well past Blender's default 100 m clip distance.
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.setup_world(scene, cfg.variant)
    return base.save_subrender(scene, ASSET, cfg)


if __name__ == '__main__':
    main()
