"""Shared sub-render setup — engine wiring, per-asset RNG seed, neutral ground.

The setup mirrors `build_scene.py` ordering: reset → cycles → output → color
management → materials → seed. Drivers add their asset(s) AFTER `setup()`
returns. The seed is derived per (asset, variant) via SHA-256 so two drivers
cannot accidentally couple their RNG streams.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import os
import random
import shutil
import sys

# Blender --background does not put the project root on sys.path. Drivers
# import via `from lqv.subscene import base`, so the root must come first.
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import bpy

from lqv import cameras, config, engine, lighting, materials, provenance, render
from lqv.materials import MAT, assign

SUBRENDER_DIR = os.path.join(config.RENDERS_DIR, 'sub')
SUBRENDER_RUNS_DIR = os.path.join(SUBRENDER_DIR, 'runs')
SUBRENDER_LATEST_DIR = os.path.join(SUBRENDER_DIR, 'latest')

# ---------------------------------------------------------------------------
# Camera clipping
# ---------------------------------------------------------------------------
# Default house-scale ``clip_end`` is 1000 m. Parcel-scale sub-renders (digital
# twin, drone fly-around, ridge composites at the 62-ha extent) need to see
# >12 km of terrain past the camera or the back-half clips into HDRI sky. The
# old fix was every driver hardcoding ``cam.data.clip_end = 20000`` after
# bypassing ``base.run()``. Centralising the constant prevents one driver from
# drifting to 5000 m and silently truncating the ridge line.
# See: feedback_subscene_clip_end.
PARCEL_CLIP_END_M: float = 20000.0
HOUSE_CLIP_END_M: float = 1000.0

# ---------------------------------------------------------------------------
# X-ray render override
# ---------------------------------------------------------------------------
# Default opaque set for ``apply_xray_override``: structure + services + glass
# stay solid so the bones of the house read; cob/earthen infill and roof
# materials go translucent so the viewer can see through the exterior shell.
# Names listed but not yet in the MAT registry (micro_hydro_turbine, lifepo4_rack,
# cistern_shell, mosquito_mesh, plumbing, fireplace_stack) are kept here as a
# forward-compatible superset — slot lookup short-circuits on missing names.
# See HOUSE_IMAGERY_SHOTLIST §5.4.
XRAY_OPAQUE_MATERIALS: frozenset[str] = frozenset({
    # structural timber + bamboo
    'bamboo', 'bamboo_culm', 'bamboo_leaf',
    'lapacho_timber', 'lapacho_bark',
    'mango_trunk', 'pindo_trunk',
    # metal + mesh + services
    'steel_anodized', 'steel_mesh',
    'metal_black', 'concrete_grey',
    'micro_hydro_turbine', 'lifepo4_rack',
    'cistern_shell', 'mosquito_mesh', 'plumbing', 'fireplace_stack',
    # water (pool/river surfaces must keep their shader to read as liquid)
    'pool_water', 'water_reflective', 'stream_bed',
    # glass (bottles + PV) — already translucent shaders; second swap muddies them
    'pv_glass',
    'glass_bottle_amber', 'glass_bottle_brown',
    'glass_bottle_cobalt', 'glass_bottle_green',
    # emissive accents that carry the dusk read
    'window_glow', 'firefly', 'lantern_paper_warm',
})

_XRAY_MAT_NAME = 'MAT_xray_override'

# ---------------------------------------------------------------------------
# RENDER_RUN_ID policy
# ---------------------------------------------------------------------------
# The runs/ folder gets one subdir per (run_id, asset) tuple. If every Blender
# invocation generates a fresh timestamp, the batch ends up in 3 different
# folders and the review/composite scripts can't group A/B/C variants. Default
# now: require RENDER_RUN_ID. Escape hatch: LQV_ALLOW_TIMESTAMP_RUN_ID=1 for
# one-off exploratory shots.
_ENV_RUN_ID = os.environ.get('RENDER_RUN_ID')
if _ENV_RUN_ID:
    _RUN_ID = _ENV_RUN_ID
elif os.environ.get('LQV_ALLOW_TIMESTAMP_RUN_ID') == '1':
    _RUN_ID = _dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    print(
        f'[lqv.subscene.base] WARN RENDER_RUN_ID unset, '
        f'LQV_ALLOW_TIMESTAMP_RUN_ID=1 set — using timestamp {_RUN_ID}. '
        f'A/B/C variants started in separate Blender processes will land '
        f'in different folders. See docs/render-runs.md.',
        file=sys.stderr,
    )
else:
    raise RuntimeError(
        'RENDER_RUN_ID env var is required to group sub-render variants. '
        'Set RENDER_RUN_ID=<your_batch_id> blender ... (recommended) or '
        'set LQV_ALLOW_TIMESTAMP_RUN_ID=1 for one-off exploratory shots. '
        'See docs/render-runs.md.'
    )

# ---------------------------------------------------------------------------
# Variant exposure / view-transform profiles
# ---------------------------------------------------------------------------
# A=interior/dawn, B=neutral/inspection, C=hero/dusk. Centralised so a tweak
# to the punchy hero look doesn't require touching 18 driver files. Drivers
# that want fully custom view settings can still override post-``save``.
VARIANT_PROFILES: dict[str, dict] = {
    'A': {'exposure': -0.2, 'gamma': 1.0, 'note': 'interior / dawn, slightly under'},
    'B': {'exposure': 0.3,  'gamma': 1.0, 'note': 'neutral mid-day inspection'},
    'C': {'exposure': 0.6,  'gamma': 1.0, 'note': 'hero / golden hour, punchy'},
}


def run_id() -> str:
    return _RUN_ID


def run_dir(asset: str) -> str:
    """renders/sub/runs/<run_id>_<asset>/ — created on demand."""
    suffix = os.environ.get('RENDER_RUN_TAG', '')
    folder = f"{_RUN_ID}_{asset}" + (f"_{suffix}" if suffix else "")
    path = os.path.join(SUBRENDER_RUNS_DIR, folder)
    os.makedirs(path, exist_ok=True)
    return path


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


def place_neutral_ground(material_key: str = 'moss', size: float = 60.0):
    """Flat ground plane so the asset isn't floating in the void.

    Default `moss` (aerial_grass_rock texture) reads as Paraguayan campo
    instead of the prior `laterite` (which renders as a stripe-pattern
    cardboard slab). Default 60 m square gives the camera 30 m of context
    in every direction so the asset doesn't sit on a postage stamp.

    Parcel-scale callers should bypass ``run()`` and set their own ground
    plus clip_end explicitly (see ``feedback_subscene_clip_end``).
    """
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0.0, 0.0, 0.0))
    ground = bpy.context.active_object
    ground.name = 'SubrenderGround'
    mat = MAT.get(material_key)
    if mat is not None:
        assign(ground, mat)
    return ground


def add_context_flora(center=(0.0, 0.0, 0.0), inner_radius_m: float = 6.0,
                      outer_radius_m: float = 22.0, count: int = 18,
                      seed: int | None = None):
    """Scatter a halo of small flora around the asset for visual context.

    Inner radius keeps flora off the building footprint; outer radius
    keeps them within the 60 m ground plane. Uses the project's flora
    modules (agave, fern, anthurium) so the look matches the broader
    scenes. Bamboo clumps are deliberately omitted — they're large and
    occlude the hero subject at house-scale framing.
    """
    from lqv.flora import agave, anthurium, fern

    rng = random.Random(seed)
    cx, cy, _ = center
    placed = 0
    attempts = 0
    while placed < count and attempts < count * 4:
        attempts += 1
        angle = rng.uniform(0.0, 6.283185)
        r = rng.uniform(inner_radius_m, outer_radius_m)
        x = cx + r * _cos(angle)
        y = cy + r * _sin(angle)
        choice = rng.random()
        try:
            if choice < 0.45:
                fern.add_tree_fern(x, y, scale=rng.uniform(0.4, 0.7))
            elif choice < 0.80:
                agave.add_agave(x, y, scale=rng.uniform(0.5, 0.9))
            else:
                anthurium._add_rosette(x, y, 0.0, scale=rng.uniform(0.4, 0.7))
        except Exception as exc:
            print(f"[subscene] context flora skipped at ({x:.1f},{y:.1f}): {exc}")
            continue
        placed += 1
    print(f"[subscene] context flora placed: {placed}/{count}")


def _cos(a: float) -> float:
    import math
    return math.cos(a)


def _sin(a: float) -> float:
    import math
    return math.sin(a)


def _build_xray_material(alpha: float = 0.15):
    mat = bpy.data.materials.get(_XRAY_MAT_NAME)
    if mat is None:
        mat = bpy.data.materials.new(_XRAY_MAT_NAME)
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    tree = mat.node_tree
    tree.nodes.clear()
    out = tree.nodes.new('ShaderNodeOutputMaterial')
    transp = tree.nodes.new('ShaderNodeBsdfTransparent')
    transp.inputs['Color'].default_value = (0.92, 0.90, 0.86, 1.0)
    principled = tree.nodes.new('ShaderNodeBsdfPrincipled')
    principled.inputs['Base Color'].default_value = (0.78, 0.74, 0.66, 1.0)
    principled.inputs['Roughness'].default_value = 0.7
    mix = tree.nodes.new('ShaderNodeMixShader')
    # Fac=0 → Principled (opaque), Fac=1 → Transparent. alpha=0.15 means
    # 15% of the original surface remains; 85% transparent.
    mix.inputs['Fac'].default_value = 1.0 - alpha
    tree.links.new(principled.outputs['BSDF'], mix.inputs[1])
    tree.links.new(transp.outputs['BSDF'], mix.inputs[2])
    tree.links.new(mix.outputs['Shader'], out.inputs['Surface'])
    return mat


def apply_xray_override(scene, asset_collection=None,
                        except_materials: set[str] | None = None,
                        alpha: float = 0.15):
    """Swap exterior-wall materials for a Transparent BSDF (alpha=0.15).

    Preserves Boolean cutters and lighting. Excludes materials in
    ``except_materials`` (defaults to :data:`XRAY_OPAQUE_MATERIALS`) so
    structure + services stay opaque. Operates on every mesh in
    ``asset_collection`` (default: every mesh in ``scene``). Stashes the
    original material reference on ``obj['_lqv_xray_orig_<slot>']`` so a
    paired :func:`clear_xray_override` can restore symmetry if the scene
    is reused. See HOUSE_IMAGERY_SHOTLIST §5.4.
    """
    if except_materials is None:
        except_materials = set(XRAY_OPAQUE_MATERIALS)
    xray_mat = _build_xray_material(alpha=alpha)

    if asset_collection is None:
        objects = [o for o in scene.objects if o.type == 'MESH']
    else:
        objects = [o for o in asset_collection.all_objects if o.type == 'MESH']

    swapped = 0
    for obj in objects:
        for i, slot in enumerate(obj.material_slots):
            mat = slot.material
            if mat is None or mat.name == _XRAY_MAT_NAME:
                continue
            if mat.name in except_materials:
                continue
            obj[f'_lqv_xray_orig_{i}'] = mat.name
            slot.material = xray_mat
            swapped += 1
    print(f"[xray] swapped {swapped} material slots → transparent (alpha={alpha})")
    return swapped


def clear_xray_override(scene, asset_collection=None):
    """Restore materials swapped by :func:`apply_xray_override`. Safe no-op
    if the override was never applied."""
    if asset_collection is None:
        objects = [o for o in scene.objects if o.type == 'MESH']
    else:
        objects = [o for o in asset_collection.all_objects if o.type == 'MESH']
    restored = 0
    for obj in objects:
        for i, slot in enumerate(obj.material_slots):
            key = f'_lqv_xray_orig_{i}'
            if key not in obj.keys():
                continue
            orig_name = obj[key]
            orig = bpy.data.materials.get(orig_name)
            if orig is not None:
                slot.material = orig
                restored += 1
            del obj[key]
    print(f"[xray] restored {restored} material slots")
    return restored


def setup_world(scene, variant: str):
    """Reuse the project sun + HDRI so each sub-render reads under the same
    light the composite uses. Volumes skipped — sub-renders are 128 samples
    and the canopy/mist domains double CPU cost without helping a close shot.
    """
    lighting.setup_world_and_sun(scene, variant)


def save_subrender(scene, asset: str, cfg) -> str:
    """Write to renders/sub/runs/<run_id>_<asset>/<variant>.png and run.

    Also mirrors to renders/sub/latest/<asset>_<variant>.png (overwriting) so a
    quick-look location always exists, and copies into the legacy flat path at
    renders/sub/<asset>_<variant>.png for back-compat with existing scripts.

    Returns the run-folder path. Honors cfg.skip_render — useful for framework
    smoke tests (build the scene, don't burn samples).
    """
    run_folder = run_dir(asset)
    view = getattr(cfg, 'view', 'hero3q')
    view_tag = '' if view == 'hero3q' else f"_{view}"
    out = os.path.join(run_folder, f"{cfg.variant}{view_tag}.png")
    scene.render.filepath = out

    profile = VARIANT_PROFILES.get(cfg.variant, VARIANT_PROFILES['C'])
    scene.view_settings.exposure = profile['exposure']
    scene.view_settings.gamma = profile.get('gamma', 1.0)

    if cfg.skip_render:
        print(f"[subscene:{asset}] skipped (RENDER_SKIP=1) — would write {out}")
        return out

    if view == 'xray':
        apply_xray_override(scene)

    render.run(scene)
    print(f"[subscene:{asset}] wrote {out}")

    # CC-TOOL.8: embed git SHA + RNG seed + tracked LQV_* env vars into the
    # PNG itself, then drop a JSON sidecar for catalogue scripts. Mirrors
    # below run AFTER injection so the latest/ + legacy copies carry the
    # provenance too. Injection failures must not block the render save.
    try:
        meta = provenance.collect(
            asset=asset, variant=cfg.variant, view=view,
            seed=derive_seed(asset, cfg.variant),
            extra={'run_id': _RUN_ID, 'samples': cfg.samples,
                   'res': f'{cfg.res_x}x{cfg.res_y}'},
        )
        provenance.inject_into_png(out, meta)
        provenance.write_sidecar(out, meta)
    except Exception as exc:  # noqa: BLE001 — provenance must never fail a render
        print(f"[subscene:{asset}] provenance injection failed: {exc}",
              file=sys.stderr)

    os.makedirs(SUBRENDER_LATEST_DIR, exist_ok=True)
    latest = os.path.join(SUBRENDER_LATEST_DIR, f"{asset}_{cfg.variant}{view_tag}.png")
    shutil.copy2(out, latest)
    legacy = os.path.join(SUBRENDER_DIR, f"{asset}_{cfg.variant}{view_tag}.png")
    shutil.copy2(out, legacy)
    print(f"[subscene:{asset}] mirrored → {latest}")
    return out


def run(asset: str, build_fn, camera_target=(0.0, 0.0, 1.0),
        camera_distance: float = 6.0, camera_height: float = 2.4,
        camera_lens: float = 35.0, with_ground: bool = True,
        ground_material: str = 'moss',
        with_context_flora: bool = True,
        context_flora_count: int = 18,
        clip_end: float = HOUSE_CLIP_END_M):
    """Standard sub-render entry point.

    `build_fn()` is called after setup + neutral ground placement, with the
    RNG already seeded for (asset, variant). It must add the asset to the
    live scene; return value is ignored.

    ``clip_end`` is applied to the camera after creation. Default 1000 m
    covers house-scale assets with breathing room; parcel-scale callers
    should bypass ``run()`` entirely (see ``feedback_subscene_clip_end``).
    """
    scene, cfg = setup(asset)
    if with_ground:
        place_neutral_ground(material_key=ground_material)
    build_fn()
    if with_ground and with_context_flora:
        add_context_flora(
            center=(camera_target[0], camera_target[1], 0.0),
            seed=derive_seed(asset, cfg.variant),
            count=context_flora_count,
        )
    setup_world(scene, cfg.variant)
    cam = cameras.make_view_camera(
        cfg, target=camera_target, distance=camera_distance,
        height=camera_height, lens=camera_lens,
    )
    cam.data.clip_end = clip_end
    scene.camera = cam
    return save_subrender(scene, asset, cfg)
