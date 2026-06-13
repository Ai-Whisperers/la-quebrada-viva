"""Sub-render: 4-elevation Dutch renders for any typology.

Renders front/back/left/right orthographic-ish elevations at 0 deg tilt, lens=50,
distance auto-fit to mesh bbox * 1.4. Bypasses ``base.run()`` because:
  * we need 4 cameras per build, not 1
  * clip_end must be 20000 m (parcel-scale safety per feedback_subscene_clip_end)
  * exposure is pinned to A (-0.2) so all four elevations read consistently

Output: renders/sub/runs/<RENDER_RUN_ID>_elevation_dutch_<typology>/{front,back,left,right}.png
Mirror: renders/sub/latest/elevation_dutch_<typology>_{front,back,left,right}.png

Typology/amenity is selected via ELEVATION_TYPOLOGY env var. Dispatch order:
  * <slug> in lqv.typologies        -> lqv.typologies.<slug>.build_<slug>(origin=(0,0,0))
  * eco_retreat_modern_oasis        -> lqv.amenities.eco_retreat_modern_oasis.build_eco_retreat_modern_oasis()
  * other amenities (labrisa_lounge, eco_pool, floating_dining) -> lqv.amenities.<slug>.build(variant='A')

Note: cob_bottle_lqv has its own sub-render driver at
``lqv.subscene.cob_bottle_lqv`` and is intentionally absent from both the
TYPOLOGIES tuple and this elevation dispatcher.
"""
from __future__ import annotations

import importlib
import math
import os
import shutil
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import bpy
from mathutils import Vector

from lqv import cameras, render
from lqv.subscene import base


ELEVATIONS = ('front', 'back', 'left', 'right')

# Fallback box if a typology builds nothing (which would mean a NotImplementedError
# anyway, but we want a sane number rather than a divide-by-zero camera).
_MIN_DIM = 4.0


_AMENITIES = ('labrisa_lounge', 'eco_pool', 'floating_dining', 'eco_retreat_modern_oasis')


def _resolve_build(typology: str):
    """Return a callable that builds the typology or amenity at origin.

    Dispatch precedence:
      lqv.typologies.<slug>  -> build_<slug>(origin=(0,0,0))
      eco_retreat_modern_oasis -> build_eco_retreat_modern_oasis()
      other amenities        -> build(variant='A')
    """
    if typology in _AMENITIES:
        mod = importlib.import_module(f'lqv.amenities.{typology}')
        if typology == 'eco_retreat_modern_oasis':
            fn = getattr(mod, 'build_eco_retreat_modern_oasis')
            return lambda: fn()
        fn = getattr(mod, 'build')
        return lambda: fn(variant='A')

    mod = importlib.import_module(f'lqv.typologies.{typology}')
    fn = getattr(mod, f'build_{typology}')
    # All typology builders accept origin=(0,0,0); some also take parent/variant
    # as kwargs with defaults, so we only pass origin.
    return lambda: fn(origin=(0.0, 0.0, 0.0))


def _compute_mesh_bbox():
    """World-space AABB across every MESH object except the SubrenderGround.

    Returns (center: Vector, size: Vector). Falls back to a _MIN_DIM cube
    centered at origin if no mesh geometry exists.
    """
    mins = [math.inf, math.inf, math.inf]
    maxs = [-math.inf, -math.inf, -math.inf]
    found = False
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        if obj.name == 'SubrenderGround':
            continue
        if obj.hide_render:
            continue
        mw = obj.matrix_world
        for corner in obj.bound_box:
            wc = mw @ Vector(corner)
            if wc.x < mins[0]: mins[0] = wc.x
            if wc.y < mins[1]: mins[1] = wc.y
            if wc.z < mins[2]: mins[2] = wc.z
            if wc.x > maxs[0]: maxs[0] = wc.x
            if wc.y > maxs[1]: maxs[1] = wc.y
            if wc.z > maxs[2]: maxs[2] = wc.z
        found = True

    if not found:
        return Vector((0.0, 0.0, _MIN_DIM * 0.5)), Vector((_MIN_DIM, _MIN_DIM, _MIN_DIM))

    center = Vector((
        (mins[0] + maxs[0]) * 0.5,
        (mins[1] + maxs[1]) * 0.5,
        (mins[2] + maxs[2]) * 0.5,
    ))
    size = Vector((
        max(maxs[0] - mins[0], _MIN_DIM),
        max(maxs[1] - mins[1], _MIN_DIM),
        max(maxs[2] - mins[2], _MIN_DIM),
    ))
    return center, size


def _camera_location(elevation: str, center: Vector, distance: float):
    """Camera at 0 deg tilt: same Z as bbox center, offset on horizontal axis."""
    cx, cy, cz = center.x, center.y, center.z
    if elevation == 'front':
        return (cx, cy - distance, cz)
    if elevation == 'back':
        return (cx, cy + distance, cz)
    if elevation == 'left':
        return (cx - distance, cy, cz)
    if elevation == 'right':
        return (cx + distance, cy, cz)
    raise ValueError(f"unknown elevation {elevation!r}")


def render_typology(typology: str) -> dict:
    """Render the 4 Dutch elevations for ``typology``.

    Returns {'ok': [elevs...], 'fail': {elev: err_str, ...}, 'run_dir': str}.
    Continues on per-elevation errors so a partial result is still useful for
    the deck builder.
    """
    asset = f'elevation_dutch_{typology}'
    print(f"\n[elev] === {typology} ===")

    # One scene per typology — build once, then re-aim the camera per elevation.
    scene, cfg = base.setup(asset)
    base.place_neutral_ground('laterite')

    build_fn = _resolve_build(typology)
    build_fn()

    base.setup_world(scene, cfg.variant)

    # Pin exposure to A so all four elevations read identically regardless of
    # the variant env var.
    scene.view_settings.exposure = -0.2

    center, size = _compute_mesh_bbox()
    max_dim = max(size.x, size.y, size.z)
    distance = max_dim * 1.4
    print(f"[elev] {typology} bbox center={tuple(round(v,2) for v in center)} "
          f"size={tuple(round(v,2) for v in size)} distance={distance:.2f}")

    run_folder = os.path.join(
        base.SUBRENDER_RUNS_DIR, f"{base.run_id()}_{asset}"
    )
    os.makedirs(run_folder, exist_ok=True)
    os.makedirs(base.SUBRENDER_LATEST_DIR, exist_ok=True)

    ok = []
    fail = {}
    target = (center.x, center.y, center.z)
    for elev in ELEVATIONS:
        try:
            loc = _camera_location(elev, center, distance)
            cam = cameras.add_camera(
                f'Cam_elev_{typology}_{elev}',
                location=loc,
                look_at=target,
                lens=50.0,
            )
            cam.data.clip_end = base.PARCEL_CLIP_END_M
            scene.camera = cam

            out = os.path.join(run_folder, f"{elev}.png")
            scene.render.filepath = out

            if cfg.skip_render:
                print(f"[elev] SKIP {typology}/{elev} (RENDER_SKIP=1) — would write {out}")
                ok.append(elev)
                continue

            render.run(scene)
            latest = os.path.join(
                base.SUBRENDER_LATEST_DIR,
                f"elevation_dutch_{typology}_{elev}.png",
            )
            shutil.copy2(out, latest)
            print(f"[elev] wrote {out}  ->  {latest}")
            ok.append(elev)
        except Exception as e:
            print(f"[elev] FAIL {typology}/{elev}: {e}")
            import traceback
            traceback.print_exc()
            fail[elev] = str(e)

    return {'ok': ok, 'fail': fail, 'run_dir': run_folder}


if __name__ == '__main__':
    typology = os.environ.get('ELEVATION_TYPOLOGY', '').strip()
    if not typology:
        print("[elev] ERROR: set ELEVATION_TYPOLOGY=<slug>")
        sys.exit(2)
    result = render_typology(typology)
    print(f"\n[elev] {typology}: ok={result['ok']} fail={list(result['fail'].keys())}")
    if result['fail']:
        sys.exit(1)
