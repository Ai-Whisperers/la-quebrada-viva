"""Shared sub-render setup — engine wiring, per-asset RNG seed, neutral ground.

The setup mirrors `build_scene.py` ordering: reset → cycles → output → color
management → materials → seed. Drivers add their asset(s) AFTER `setup()`
returns. The seed is derived per (asset, variant) via SHA-256 so two drivers
cannot accidentally couple their RNG streams.
"""
from __future__ import annotations

import hashlib
import os
import random
import sys

# Blender --background does not put the project root on sys.path. Drivers
# import via `from lqv.subscene import base`, so the root must come first.
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import bpy

from lqv import cameras, config, engine, lighting, materials, render
from lqv.materials import MAT, assign

SUBRENDER_DIR = os.path.join(config.RENDERS_DIR, 'sub')


def derive_seed(asset: str, variant: str) -> int:
    """SHA-256(SEED:asset:variant) → 32-bit int. Per-asset isolation."""
    blob = f"{config.SEED}:{asset}:{variant}".encode()
    return int.from_bytes(hashlib.sha256(blob).digest()[:4], 'big')


def setup(asset: str, cfg=None):
    """Build an empty scene with engine + materials + per-asset RNG seed.

    Returns (scene, cfg). Driver builds its asset against the live bpy.data
    after this returns; the MAT registry is populated and the RNG is seeded.
    """
    if cfg is None:
        cfg = config.parse()
    print(
        f"[subscene:{asset}] variant={cfg.variant} "
        f"samples={cfg.samples} res={cfg.res_x}x{cfg.res_y}"
    )

    scene = engine.reset_scene()
    engine.setup_cycles(scene, cfg)
    engine.setup_render_output(scene, cfg)
    engine.setup_color_management(scene)

    materials.build_materials()

    random.seed(derive_seed(asset, cfg.variant))
    return scene, cfg


def place_neutral_ground(material_key: str = 'laterite', size: float = 20.0):
    """Flat ground plane so the asset isn't floating in the void."""
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0.0, 0.0, 0.0))
    ground = bpy.context.active_object
    ground.name = 'SubrenderGround'
    mat = MAT.get(material_key)
    if mat is not None:
        assign(ground, mat)
    return ground


def setup_world(scene, variant: str):
    """Reuse the project sun + HDRI so each sub-render reads under the same
    light the composite uses. Volumes skipped — sub-renders are 128 samples
    and the canopy/mist domains double CPU cost without helping a close shot.
    """
    lighting.setup_world_and_sun(scene, variant)


def save_subrender(scene, asset: str, cfg) -> str:
    """Point the render output at renders/sub/<asset>_<variant>.png and run.

    Returns the output path. Honors cfg.skip_render — useful for framework
    smoke tests (build the scene, don't burn samples).
    """
    os.makedirs(SUBRENDER_DIR, exist_ok=True)
    out = os.path.join(SUBRENDER_DIR, f"{asset}_{cfg.variant}.png")
    scene.render.filepath = out

    if cfg.variant == 'A':
        scene.view_settings.exposure = -0.2
    elif cfg.variant == 'B':
        scene.view_settings.exposure = 0.3
    else:
        scene.view_settings.exposure = 0.6

    if cfg.skip_render:
        print(f"[subscene:{asset}] skipped (RENDER_SKIP=1) — would write {out}")
    else:
        render.run(scene)
        print(f"[subscene:{asset}] wrote {out}")
    return out


def run(asset: str, build_fn, camera_target=(0.0, 0.0, 1.0),
        camera_distance: float = 6.0, camera_height: float = 2.4,
        camera_lens: float = 35.0, with_ground: bool = True,
        ground_material: str = 'laterite'):
    """Standard sub-render entry point.

    `build_fn()` is called after setup + neutral ground placement, with the
    RNG already seeded for (asset, variant). It must add the asset to the
    live scene; return value is ignored.
    """
    scene, cfg = setup(asset)
    if with_ground:
        place_neutral_ground(material_key=ground_material)
    build_fn()
    setup_world(scene, cfg.variant)
    cam = cameras.subscene_camera(
        target=camera_target,
        distance=camera_distance,
        height=camera_height,
        lens=camera_lens,
    )
    scene.camera = cam
    return save_subrender(scene, asset, cfg)
