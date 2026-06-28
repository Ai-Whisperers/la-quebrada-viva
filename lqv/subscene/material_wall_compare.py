"""Sub-render: brick / clay material wall A/B/C compare.

A 4-up of 1.2 m × 2.4 m vertical panels (single-leaf wall scale, no
gables/openings) standing 1.5 m apart along +X so the camera at
``(distance, -distance, height)`` rakes across all four reads simultaneously.

Panels left-to-right:

* ``red_brick`` — Poly Haven ``red_brick_03``, hot terracotta
* ``castle_brick`` — Poly Haven ``castle_brick_02_red``, older / mossier
* ``clay_block`` — Poly Haven ``clay_block_wall``, unfired earth block
* ``clay_plaster`` — Poly Haven ``clay_plaster``, smooth finish coat

Lighting is the standard project sun + HDRI per variant so the same panel
reads differently across A/B/C (dawn / midday / dusk). This is the use-case
the spec wants tested — judging the brick + clay band against the lighting
states the parcel will actually see.

Bypasses :func:`lqv.subscene.base.run` because the camera needs an explicit
``clip_end = 20000`` and the +X axis layout is wider than the default
neutral-ground centred composition.
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

ASSET = 'material_wall_compare'

PANEL_W = 1.2
PANEL_H = 2.4
PANEL_T = 0.18
PANEL_SPACING = 1.5  # gap between adjacent panel centres minus PANEL_W

# Order matters — left-to-right read across the 4-up.
WALL_MATERIALS = ('red_brick', 'castle_brick', 'clay_block', 'clay_plaster')


def _build_panel(x: float, mat_key: str, index: int) -> bpy.types.Object:
    """Stand a single 1.2 × 2.4 × 0.18 m panel at ``(x, 0, PANEL_H/2)``.

    Panels are simple cubes — the brick/clay texture set carries the visual
    weight via diffuse + normal + roughness + displacement. Centre Z at
    ``PANEL_H/2`` so the base sits on the ground plane.
    """
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0.0, PANEL_H / 2.0))
    obj = bpy.context.active_object
    obj.name = f'WallCompare_Panel_{index:02d}_{mat_key}'
    obj.scale = (PANEL_W, PANEL_T, PANEL_H)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mat = MAT.get(mat_key)
    if mat is not None:
        assign(obj, mat)
    else:
        print(f"[material_wall_compare] MAT['{mat_key}'] missing — panel left unshaded")
    return obj


def _place_wall_row():
    """Stand four panels along +X, centred about the origin.

    Panel centre-to-centre = ``PANEL_W + PANEL_SPACING``. Row is centred so
    the camera target at ``(0, 0, 1.2)`` lands in the middle of the row.
    """
    pitch = PANEL_W + PANEL_SPACING
    total_span = pitch * (len(WALL_MATERIALS) - 1)
    start_x = -total_span / 2.0
    for i, key in enumerate(WALL_MATERIALS):
        _build_panel(start_x + i * pitch, key, i)


if __name__ == '__main__':
    scene, cfg = base.setup(ASSET)
    base.place_neutral_ground('laterite')
    _place_wall_row()
    base.setup_world(scene, cfg.variant)

    cam = cameras.make_view_camera(
        cfg,
        target=(0.0, 0.0, 1.2),
        distance=10.0,
        height=1.5,
        lens=35.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.save_subrender(scene, ASSET, cfg)
