"""
La Quebrada Viva — scene builder for Blender Cycles.

Thin driver: wires the `lqv/` package modules in the order the legacy monolith
ran them. All scene-building lives in `lqv/`. The pre-refactor monolith is
kept at `_archive/build_scene.py.pre-refactor.bak` as the byte-identity reference.

Run headless:

    blender --background --python build_scene.py

Override via environment:
    RENDER_VARIANT=A|B          (default A — winter golden hour with lapacho bloom)
    RENDER_CAM=hero|stream_up|terrace|cliff|dusk|petal_macro   (default hero)
    RENDER_SAMPLES=128|256|512  (default 128 — preview; raise for finals)
    RENDER_RES=preview|final|hero (or 720|1080|1440; default preview = 1280x720)
    RENDER_SKIP=1               build the scene, save .blend, do not render

    Preview renders (RENDER_RES=preview|720) write to renders/_preview_<variant>_<cam>.png
    (underscore-prefixed, gitignored). Other resolutions write to renders/<variant>_<cam>.png.

Coordinate convention: +Y is geographic north (toward escarpment / warm face in
Southern Hemisphere), -Y is south (downhill, glade, stream view), +X is east.
House origin sits on the upper terrace platform.
"""
from __future__ import annotations

import os
import random
import sys

# Blender's --background mode doesn't add the script directory to sys.path.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from lqv import config, engine, materials, render, lighting, cameras, flora
from lqv.site import build_escarpment, build_ground, build_terraces, build_stream
from lqv.house import build_cob_house, build_bottle_wall, build_tatakua, build_services


def main():
    cfg = config.parse()
    print(f"[build] variant={cfg.variant} cam={cfg.cam_name} samples={cfg.samples} res={cfg.res_x}x{cfg.res_y}")

    scene = engine.reset_scene()
    engine.setup_cycles(scene, cfg)
    engine.setup_render_output(scene, cfg)
    engine.setup_color_management(scene)

    # Materials need a fresh bpy.data, populate after reset_scene.
    materials.build_materials()

    # Pixel-identity invariant: seed AFTER materials (no random in material
    # build) and BEFORE the first build_* that calls random.* — preserves the
    # monolith's RNG draw order.
    random.seed(config.SEED)

    build_escarpment()
    build_ground()
    build_terraces()
    build_cob_house()
    build_bottle_wall()
    build_tatakua()
    build_stream()
    # Rule 7/9/10 service props. Slotted after build_stream so the pelton
    # housing at the weir is already in the scene as a paired reference.
    # All deterministic — preserves the RNG draw order for flora.populate.
    build_services()

    flowering = (cfg.variant == 'A')
    flora.populate(flowering_lapacho=flowering)
    if flowering:
        flora.scatter_lapacho_petals(n=100)
    # Scene-completeness detail. Appended AFTER scatter_lapacho_petals so the
    # petal RNG draw stays byte-identical to the pre-Phase-6 baseline; grass
    # tufts and anthurium epiphytes consume RNG state that is otherwise unused.
    flora.scatter_grass_tufts(n=80)
    flora.scatter_anthuriums()

    lighting.setup_world_and_sun(scene, cfg.variant)
    lighting.build_canopy_volume(skip=cfg.is_preview)
    lighting.build_valley_mist(cfg.variant, skip=cfg.is_preview)
    cams = cameras.build_cameras()

    cam_name = cfg.cam_name
    if cam_name not in cams:
        print(f"[build] WARNING: unknown camera {cam_name!r}, falling back to 'hero'")
        cam_name = 'hero'
    scene.camera = cams[cam_name]

    scene.view_settings.exposure = -0.2 if cfg.variant == 'A' else 0.3
    scene.render.filepath = cfg.output_path

    render.save_blend(config.BLEND_PATH)

    if cfg.skip_render:
        print('[render] skipped (RENDER_SKIP=1)')
    else:
        render.run(scene)


main()
