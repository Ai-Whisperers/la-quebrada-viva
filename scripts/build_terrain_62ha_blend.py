"""Build the 62-ha digital twin scene and save it as a .blend.

Headless build → save → quit. Run once, then open the saved file in
GUI Blender to fly around the parcel:

    blender --background --python scripts/build_terrain_62ha_blend.py
    blender renders/sub/terrain_62ha_scene.blend

Creates all three cameras (birdseye / plan / oblique) so the GUI user can
switch between views via Camera -> Switch Active (Ctrl+0).
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import datetime as _dt

# lqv.subscene.base requires RENDER_RUN_ID (see docs/render-runs.md).
# This script only saves a .blend; no images get written to the runs/
# tree, but the import path still triggers the env check. Default to a
# stable, recognisable id so the rare case where the saved scene drives
# a follow-up sub-render lands in a sensibly-named folder.
os.environ.setdefault(
    "RENDER_RUN_ID",
    "build_terrain_62ha_" + _dt.datetime.now().strftime("%Y%m%d"),
)

import bpy

from lqv import cameras
from lqv.subscene import base, terrain_62ha as t62


def main() -> str:
    os.environ.setdefault("RENDER_SKIP", "1")
    os.environ.setdefault("RENDER_VARIANT", "B")

    scene, cfg = base.setup("terrain_62ha")
    t62._build()
    base.setup_world(scene, cfg.variant)
    t62._setup_neutral_world(scene)

    primary = None
    fallback = None
    for view_key, view in t62._CAM_VIEWS.items():
        cam = cameras.add_camera(
            f"Cam_{view_key}",
            location=view["location"],
            look_at=view["look_at"],
            lens=view["lens"],
        )
        if view["ortho"] is not None:
            cam.data.type = "ORTHO"
            cam.data.ortho_scale = view["ortho"]
        cam.data.clip_start = 1.0
        cam.data.clip_end = base.PARCEL_CLIP_END_M
        if view_key == "oblique":
            primary = cam
        elif view_key == "birdseye" and fallback is None:
            fallback = cam
    scene.camera = primary or fallback

    # Configure 3D viewport defaults across all screens so the GUI opens with:
    #  • far-clip extended to 20 km (default 1 km would clip the 3 km parcel)
    #  • locked to the oblique camera view (cinematic default for v4 polish)
    #  • shading set to RENDERED so AgX-graded Cycles preview shows live, with
    #    cob/water/foliage PBR materials visible instead of emission markers
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type != "VIEW_3D":
                continue
            for space in area.spaces:
                if space.type != "VIEW_3D":
                    continue
                space.clip_start = 1.0
                space.clip_end = 20000.0
                space.shading.type = "RENDERED"
                if space.region_3d is not None:
                    space.region_3d.view_perspective = "CAMERA"

    out = os.path.join(_PROJECT_ROOT, "renders", "sub", "terrain_62ha_scene.blend")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print(f"[build_terrain_62ha_blend] saved {out}")
    return out


if __name__ == "__main__":
    main()
