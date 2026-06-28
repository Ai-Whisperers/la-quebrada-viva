"""Gallery batch: multi-angle renders of every REAL asset builder.

The 14 typology + amenity modules under `lqv/typologies/` and `lqv/amenities/`
are still forward-declaration stubs (`raise NotImplementedError`). Until they
are extracted from `_archive/build_scene.py.pre-refactor.bak`, this gallery
covers what actually has implemented geometry today:

- Cob house stack: cob_walls, services, tatakua, bottle_wall
- Site landscape: escarpment, stream, terraces
- Flora: lapacho_tree, mango, pindo_palm, tree_fern, bamboo_clump, agave, anthurium
- Effects: canopy_volume, fireflies, valley_mist, window_emission

Per-asset RNG isolation comes from `base.setup(asset)` (SHA-256[:4] derive).
Output goes to `renders/sub/runs/<RENDER_RUN_ID>_<asset>_<view>/<variant>.png`
mirrored to `renders/sub/latest/<asset>_<view>_<variant>.png`.

Usage (headless Blender):
    RENDER_RUN_ID=20260611_gallery_real RENDER_VARIANT=B RENDER_SAMPLES=64 \
        RENDER_RES=preview blender -b -P scripts/render_models_gallery.py
"""
from __future__ import annotations

import os
import shutil
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv import cameras, render
from lqv.subscene import base


_PHOTOREAL_FLORA = os.environ.get('RENDER_FLORA_PHOTOREAL', '0') == '1'


def _b_cob_walls():
    from lqv.house import build_cob_house
    build_cob_house()


def _b_services():
    from lqv.house import build_cob_house, build_services
    build_cob_house()
    build_services()


def _b_tatakua():
    from lqv.house import build_tatakua
    build_tatakua()


def _b_bottle_wall():
    from lqv.house import build_bottle_wall, build_cob_house
    build_cob_house()
    build_bottle_wall()


def _b_escarpment():
    from lqv.site import build_escarpment
    build_escarpment()


def _b_stream():
    from lqv.site import build_stream
    build_stream()


def _b_terraces():
    from lqv.site import build_terraces
    build_terraces()


def _b_lapacho():
    if _PHOTOREAL_FLORA:
        from lqv.flora.photoreal import add_lapacho_photoreal
        add_lapacho_photoreal(0.0, 0.0, scale=1.0, flowering=True)
    else:
        from lqv.flora import add_lapacho
        add_lapacho(0.0, 0.0, scale=1.0, flowering=True)


def _b_mango():
    if _PHOTOREAL_FLORA:
        from lqv.flora.photoreal import add_mango_photoreal
        add_mango_photoreal(0.0, 0.0, scale=1.0)
    else:
        from lqv.flora import add_mango
        add_mango(0.0, 0.0, scale=1.0)


def _b_pindo():
    # No Poly Haven CC0 equivalent; Sketchfab CC-BY path blocked by dead MCP.
    from lqv.flora import add_pindo_palm
    add_pindo_palm(0.0, 0.0, scale=1.0)


def _b_tree_fern():
    if _PHOTOREAL_FLORA:
        from lqv.flora.photoreal import add_tree_fern_photoreal
        add_tree_fern_photoreal(0.0, 0.0, scale=1.0)
    else:
        from lqv.flora import add_tree_fern
        add_tree_fern(0.0, 0.0, scale=1.0)


def _b_bamboo():
    # No Poly Haven CC0 equivalent; Sketchfab CC-BY path blocked by dead MCP.
    from lqv.flora import add_bamboo_clump
    add_bamboo_clump(0.0, 0.0, scale=1.0)


def _b_agave():
    from lqv.flora import add_agave
    add_agave(0.0, 0.0, scale=1.0)


def _b_anthurium():
    if _PHOTOREAL_FLORA:
        from lqv.flora.photoreal import add_anthurium_photoreal
        add_anthurium_photoreal(0.0, 0.0, scale=1.0)
    else:
        from lqv.flora import scatter_anthuriums
        scatter_anthuriums(spots=[(0.0, 0.0, 0.4, 1.0)])


def _b_canopy_volume():
    from lqv.lighting import build_canopy_volume
    build_canopy_volume()


def _b_fireflies():
    from lqv.flora import scatter_fireflies
    scatter_fireflies(n=80, variant=os.environ.get('RENDER_VARIANT', 'A').upper())


def _b_valley_mist():
    from lqv.lighting import build_valley_mist
    build_valley_mist(os.environ.get('RENDER_VARIANT', 'A').upper())


def _b_window_emission():
    from lqv.house import build_cob_house, build_window_emission
    build_cob_house()
    build_window_emission(os.environ.get('RENDER_VARIANT', 'A').upper())


# (asset, build_fn, target, distance, height, lens, with_ground, ground_material)
MANIFEST = [
    # ===== Cob house stack =====
    ('cob_walls',       _b_cob_walls,       (0.0,  2.0, 1.8), 10.0, 4.0, 28.0, True,  'laterite'),
    ('services',        _b_services,        (0.0,  0.0, 2.2), 10.0, 4.0, 35.0, True,  'laterite'),
    ('tatakua',         _b_tatakua,         (-5.5, -4.5, 0.7), 3.5, 1.6, 50.0, True,  'laterite'),
    ('bottle_wall',     _b_bottle_wall,     (6.0,  2.0, 1.8),  4.5, 2.0, 50.0, True,  'laterite'),
    # ===== Site landscape =====
    ('escarpment',      _b_escarpment,      (0.0, 20.0, 8.0), 40.0, 12.0, 50.0, False, None),
    ('stream',          _b_stream,          (11.0,-14.0,-0.2),12.0, 4.0, 35.0, False, None),
    ('terraces',        _b_terraces,        (0.0, -6.0, 0.5), 14.0, 5.0, 35.0, True,  'laterite'),
    # ===== Flora =====
    ('lapacho_tree',    _b_lapacho,         (0.0,  0.0, 3.0),  8.0, 3.5, 35.0, True,  'grass'),
    ('mango',           _b_mango,           (0.0,  0.0, 3.0),  8.0, 3.5, 35.0, True,  'grass'),
    ('pindo_palm',      _b_pindo,           (0.0,  0.0, 3.5),  7.0, 3.0, 35.0, True,  'grass'),
    ('tree_fern',       _b_tree_fern,       (0.0,  0.0, 1.6),  4.5, 2.0, 50.0, True,  'grass'),
    ('bamboo_clump',    _b_bamboo,          (0.0,  0.0, 2.5),  5.5, 2.5, 35.0, True,  'grass'),
    ('agave',           _b_agave,           (0.0,  0.0, 0.4),  2.5, 1.0, 50.0, True,  'laterite'),
    ('anthurium',       _b_anthurium,       (0.0,  0.0, 0.4),  2.5, 1.2, 50.0, True,  'laterite'),
    # ===== FX volumes =====
    ('canopy_volume',   _b_canopy_volume,   (0.0,  0.0, 4.0), 12.0, 5.0, 35.0, True,  'grass'),
    ('fireflies',       _b_fireflies,       (0.0,  0.0, 1.5),  8.0, 2.5, 35.0, True,  'grass'),
    ('valley_mist',     _b_valley_mist,     (0.0, 10.0, 2.0), 20.0, 4.0, 35.0, True,  'grass'),
    ('window_emission', _b_window_emission, (0.0,  0.0, 1.5),  8.0, 2.4, 35.0, True,  'laterite'),
]

VIEWS = ('front', 'side', 'top')


def _view_location(view: str, target, distance: float, height: float):
    tx, ty, _tz = target
    if view == 'front':
        return (tx + distance, ty - distance, height)
    if view == 'side':
        return (tx + distance * 1.2, ty, height)
    if view == 'top':
        return (tx, ty - distance * 0.6, height + distance * 0.9)
    raise ValueError(f"unknown view {view!r}")


def main():
    asset_filter = os.environ.get('RENDER_ASSETS', '').strip()
    allow = {a.strip() for a in asset_filter.split(',') if a.strip()} if asset_filter else None
    manifest = [m for m in MANIFEST if allow is None or m[0] in allow]
    if allow is not None:
        missing = allow - {m[0] for m in manifest}
        if missing:
            print(f"[gallery] WARN unknown assets in RENDER_ASSETS filter: {sorted(missing)}")
    total = len(manifest) * len(VIEWS)
    idx = 0
    failures = []
    for asset, build_fn, target, distance, height, lens, with_ground, ground_mat in manifest:
        for view in VIEWS:
            idx += 1
            print(f"\n[gallery] ({idx}/{total}) {asset} / {view}")
            try:
                scene, cfg = base.setup(asset)
                if with_ground:
                    base.place_neutral_ground(material_key=ground_mat)
                build_fn()
                base.setup_world(scene, cfg.variant)

                loc = _view_location(view, target, distance, height)
                cam = cameras.add_camera(
                    f'Cam_{asset}_{view}',
                    location=loc,
                    look_at=target,
                    lens=lens,
                )
                scene.camera = cam
                cam.data.clip_end = 20000.0

                if cfg.variant == 'A':
                    scene.view_settings.exposure = -0.2
                elif cfg.variant == 'B':
                    scene.view_settings.exposure = 0.3
                else:
                    scene.view_settings.exposure = 0.6

                out_dir = os.path.join(
                    base.SUBRENDER_RUNS_DIR, f"{base.run_id()}_{asset}_{view}"
                )
                os.makedirs(out_dir, exist_ok=True)
                out = os.path.join(out_dir, f"{cfg.variant}.png")
                scene.render.filepath = out

                if cfg.skip_render:
                    print(f"[gallery] SKIP render (RENDER_SKIP=1) — would write {out}")
                else:
                    render.run(scene)
                    print(f"[gallery] wrote {out}")
                    os.makedirs(base.SUBRENDER_LATEST_DIR, exist_ok=True)
                    latest = os.path.join(
                        base.SUBRENDER_LATEST_DIR,
                        f"{asset}_{view}_{cfg.variant}.png",
                    )
                    shutil.copy2(out, latest)
            except Exception as e:
                print(f"[gallery] FAIL {asset}/{view}: {e}")
                failures.append(f"{asset}/{view}: {e}")
                import traceback
                traceback.print_exc()

    print(f"\n[gallery] done — {total - len(failures)}/{total} succeeded")
    if failures:
        print("[gallery] failures:")
        for f in failures:
            print(f"  - {f}")


if __name__ == '__main__':
    main()
