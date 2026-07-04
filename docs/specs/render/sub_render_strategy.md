# Sub-Render Strategy — Per-Asset Isolation First, Whole Scene Last

Architectural shift proposed by Wesley/Ivan during the 2026-06-10 session: instead of building, iterating on, and re-rendering the whole `build_scene.py` monolith every time we touch any single asset, we build many **sub-renders** first — each one renders a single asset/typology/amenity/component in isolation — and only at the end do we composite the whole scene with all approved assets in place.

This file is the design doc for that shift. Implementation tasks originally landed in the Tier-1 (T1.1) and Tier-2 (T2.1) slices of the archived upgrade plan at `docs/_archive/2026-06-1X/UPGRADE_PLAN.md`; critique context lives at `docs/_archive/2026-06-1X/CRITIQUE_2026-06-10.md` §§2, 4. The status quo (monolithic `build_scene.py`) is not deleted — it remains the final composite path. Sub-renders are an additive iteration layer beneath it.

---

## 1. Why

The monolithic `build_scene.py` is fragile in three ways the sub-render approach fixes:

1. **Iteration cost**. A change to one petal field requires a full scene rebuild + 256-512 sample render to validate. With a sub-render, the same iteration is seconds-to-minutes on the isolated asset.
2. **Parallel work**. The 14 dormant stubs (8 typologies + 6 amenities) can be developed in parallel because each one only needs its own sub-render driver. Today they sit dormant because nobody wants to integrate them into the monolith and risk breaking byte-identity.
3. **Per-asset validation**. The 10 design rules (`lqv/util/ten_rules_check.py`) can be audited per-asset before composition. Today the audit runs (or doesn't) on the whole scene, where rule violations are easy to miss in the noise.

The trade-off: sub-renders **do not catch composition bugs** — light leak, occlusion issues, shadow interactions between assets. Those still require the final composite pass. So sub-renders are a development accelerator, not a replacement for the composite render.

---

## 2. Directory layout

```
lqv/
  subscene/
    __init__.py
    base.py              # shared setup: reset → cycles → output → color → materials → camera → render
    cob_walls.py         # builds isolated cob walls + ground plane + HDRI
    bottle_wall.py
    tatakuá.py
    lapacho_corredor.py
    footbridge.py
    escarpment.py
    stream.py
    terraces.py
    lapacho_tree.py
    pindo_palm.py
    mango.py
    tree_ferns.py
    bamboo_clump.py
    agave.py
    anthurium.py
    fireflies.py
    petal_carpet.py
    typology_adobe_courtyard.py
    typology_timber_tree_cabin.py
    typology_cob_bottle_lqv.py
    typology_underground_dome.py
    typology_rammed_earth_loft.py
    typology_shipping_container_eco.py
    typology_straw_bale_cottage.py
    typology_bamboo_pavilion.py
    amenity_parking_arrival.py
    amenity_equestrian_zone.py
    amenity_pool_wellness.py
    amenity_reception_shop.py
    amenity_event_lawn.py
    amenity_microhydro_centre.py
renders/
  sub/
    cob_walls_A.png
    cob_walls_B.png
    cob_walls_C.png
    ...
```

About 28 sub-render targets. Each driver is ~30-60 lines.

---

## 3. Driver template

Every sub-render driver follows the same skeleton (codified in `lqv/subscene/base.py`):

```python
from lqv import engine, materials, config, cameras, render
from lqv.subscene.base import (
    setup_isolated_scene,
    place_neutral_ground,
    save_subrender,
)

ASSET_NAME = "cob_walls"

def build():
    cfg = config.parse()
    setup_isolated_scene(cfg)                 # reset + cycles + output + color
    materials.build_materials()               # full MAT registry — required for any asset
    place_neutral_ground(material="dirt_neutral")
    cameras.make_view_camera(cfg, target=(0, 0, 1.5), distance=8.0, height=2.5, lens=50.0)
    from lqv.house.cob import build_cob_walls
    build_cob_walls(parent=None)              # build only this asset
    save_subrender(ASSET_NAME, cfg.variant)

if __name__ == "__main__":
    build()
```

Invocation: `blender --background --python -m lqv.subscene.cob_walls`, or via the proposed `make sub ASSET=cob_walls`.

Default render settings for sub-renders:
- **Samples**: 128 (vs 256/512 for finals).
- **Resolution**: 1280×720 (vs 1920×1080 / 2560×1440 for finals).
- **Denoise**: OIDN.
- **Variant**: A/B/C selectable via `RENDER_VARIANT` so atmospheric reads can be previewed per asset.

A complete sub-render should finish in **2-5 minutes on CPU** per asset per variant. The full 28-asset × 3-variant matrix is ~28 × 3 × 3 min = 4.2 hours of CPU time, runnable overnight.

---

## 3.5 Camera-view axis (`RENDER_VIEW`)

The sub-render protocol has two orthogonal axes: **variant** (`RENDER_VARIANT=A|B|C` — lighting / season) and **view** (`RENDER_VIEW=…` — camera framing). The variant axis is documented in §3 above; this section defines the view axis introduced in the 2026-06-26 "Camera helpers v0 → v1" / "Sub-render protocol v1 → v2" CHANGELOG entries.

### 3.5.1 Default and dispatcher

Default `RENDER_VIEW=hero3q` (`lqv/config.py:59`). The single public entry point is:

```python
cameras.make_view_camera(cfg, target=(x, y, z), distance=D, height=H, lens=F)
```

`make_view_camera` is defined in `lqv/cameras.py` and replaces the older `cameras.subscene_camera(target=…)` private helper. The dispatcher reads `cfg.view` and constructs an appropriate `bpy.types.Camera` (perspective, ortho elevation, ortho plan, ortho section, interior wide, or xray cutaway) — callers pass their own framing intent (`target`, `distance`, `height`, `lens`) and the dispatcher decides projection / clipping / placement per view.

### 3.5.2 Value set

The protocol v2 core set (enforced by `cfg.view`'s `VALID_VIEWS`):

| `RENDER_VIEW` | Projection | Use |
|---|---|---|
| `hero3q` | perspective ¾ | default sales / catalogue shot |
| `elevation` | ortho | facade study, BoQ measurement |
| `plan` | ortho top-down | site / floor plan |
| `section` | ortho cutaway | structural / fit-out reads |
| `interior` | perspective wide | furnished interior (uses `lqv/furniture.furnish_interior(...)`) |
| `xray` | perspective + override | wireframe / transparency reveal (uses `apply_xray_override`) |

`docs/HOUSE_IMAGERY_SHOTLIST.md §5.1` lists a wider catalogue-export set for downstream tooling — `hero | elev_n | elev_e | elev_s | elev_w | plan | section_long | section_cross | xray | interior_main | interior_sleep | detail` — which collapses to the core set above for the sub-render driver layer.

### 3.5.3 Bypass-pattern drivers

Parcel-scale drivers (62-ha terrain, escarpment, panoramic flora plates, etc.) bypass `subscene.base.run()` because they require `cam.data.clip_end >> 100 m` (see memory `feedback_subscene_clip_end`: `PARCEL_CLIP_END_M = 20000.0`, `HOUSE_CLIP_END_M = 1000.0`). 22 such drivers were migrated from the old `cameras.subscene_camera(...)` direct call to `cameras.make_view_camera(cfg, …)` so they honour `RENDER_VIEW` consistently with the asset-scale drivers.

### 3.5.4 Interior furnishing (`view=interior`)

`lqv/furniture.py` provides `furnish_interior(col, *, footprint_w, footprint_l, origin_xy, floor_z, pax, style, variant, name_prefix)`. 15 typology drivers (P1.B.1) call this when `cfg.view == 'interior'`. Styles `bamboo | lapacho | stone | cob | container` map to per-typology furniture kits; lantern emission is variant-keyed `{A: 0.0, B: 0.6, C: 1.0}` so interior reads pick up the dusk-to-night gradient of the lighting axis.

### 3.5.5 Xray override (`view=xray`)

`lqv/subscene/base.py` defines `apply_xray_override(scene)` plus the `XRAY_OPAQUE_MATERIALS` frozenset allowlist. When `cfg.view == 'xray'`, every material slot not in the allowlist is swapped to a transparent-BSDF override so structural elements (cob walls, terrain, foundation plinth) stay opaque while skin / cladding / fenestration goes transparent for cutaway reads.

### 3.5.6 Output filename pattern

Sub-renders extend the run-folder pattern from `feedback_render_run_folders`:

```
renders/sub/runs/<RENDER_RUN_ID>_<asset>[_<tag>]/<variant>_<view>.png
```

with the standard mirror to `latest/` and the legacy flat back-compat path `renders/sub/<asset>_<variant>.png` preserved for `RENDER_VIEW=hero3q` (the default). Non-default views always go through the run-folder pattern only; the flat path is reserved for the default-view invariant.

---

## 4. RNG invariant per sub-render

Each sub-render derives its seed from `config.SEED` (the project master seed, 20260609) and an asset-specific hash:

```python
import hashlib, random
def derive_seed(asset_name: str, variant: str) -> int:
    base = f"{config.SEED}:{asset_name}:{variant}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(base).digest()[:4], "big")
random.seed(derive_seed(ASSET_NAME, cfg.variant))
```

Properties:
- **Per-asset determinism**: re-running the same sub-render produces byte-identical output.
- **No cross-asset RNG bleed**: changing the petal driver does not perturb the cob-wall driver.
- **Final composite preserves the existing `build_scene.py` invariant** unchanged. Sub-renders are siblings, not modifications.

`lqv/util/random_audit.py` (currently dormant) gets wired in here as the sub-render-end audit step.

---

## 5. Composite stage (the final scene)

After all sub-renders pass review, the final composite proceeds via the **existing** `build_scene.py` flow — unchanged in invariants, unchanged in seed order, unchanged in `MAT` registry. The sub-render approach does not modify the composite. It only adds confidence that each piece behaves correctly in isolation.

Optionally we can add a `lqv/composite/checklist.py` that verifies each asset present in the composite has a passing sub-render on disk, raising a `MissingSubrenderError` if not. This makes the sub-render layer enforceable.

---

## 6. Sub-render queue (28 targets)

### 6.1 House components (5)
1. `cob_walls` — Rule 1, sculpted blob geometry, `lqv/house/cob.py`.
2. `bottle_wall` — colored glass bottle inserts, embedded mass.
3. `tatakuá` — clay oven, fire clearance to validate.
4. `lapacho_corredor` — wraparound veranda, Rule 5 overhangs.
5. `footbridge` — y=−25.5 positional coupling.

### 6.2 Landscape (5)
6. `escarpment` — y=20 positional coupling, sculpted heightfield.
7. `stream` — flat-rock pool, Rule 3 dengue-compliant.
8. `terraces` — sandstone-moss surfaces.
9. `petal_carpet` — Rule 4 + Task #1 defect target.
10. `fireflies` — Variant C only, ~80 emission spheres.

### 6.3 Flora (7)
11. `lapacho_tree` — Variant A bare + pink, Variant B leafed.
12. `pindo_palm` — drooping fronds (NOT coconut).
13. `mango` — dense rounded crown.
14. `tree_ferns` — riparian, 2-4 m.
15. `bamboo_clump` — Guadua/Chusquea, clumping not running.
16. `agave` — colonizing lower terraces.
17. `anthurium` — epiphytic on stream-side trunks.

### 6.4 Typologies (8 — dormant stubs to activate)
18-25. `adobe_courtyard`, `timber_tree_cabin`, `cob_bottle_lqv`, `underground_dome`, `rammed_earth_loft`, `shipping_container_eco`, `straw_bale_cottage`, `bamboo_pavilion`.

### 6.5 Amenities (6 — dormant stubs to activate)
26-31. `parking_arrival`, `equestrian_zone`, `pool_wellness`, `reception_shop`, `event_lawn`, `microhydro_centre`.

(That's 31 not 28; the original estimate underestimated flora. Track 31 in STATUS.md.)

---

## 7. Acceptance criteria per sub-render

A sub-render is "approved" when:
1. It renders without error.
2. `lqv/util/ten_rules_check.py` returns no violations attributable to this asset.
3. `lqv/util/material_audit.py` confirms no `KeyError` paths in `MAT[]` access.
4. The frame is visually consistent with the brief (`docs/MASTER_BRIEF.md`).
5. The RNG-derived seed is logged and reproducible.

Failures are tracked in `STATUS.md` as sub-tasks under #36-#39.

---

## 8. Composite-final acceptance (unchanged)

The final 18-render matrix (A/B/C × 6 cams) remains the deliverable. After sub-render adoption:
- Re-rendering the final 18 is **scheduled**, not triggered per-iteration.
- The petal defect (Task #1) becomes safe to fix because the petal sub-render isolates the bug; once fixed, the final hero/petal_macro frames can be re-rendered with confidence.
- The renderer byte-identity invariant moves from "all 18 finals at `85e86aa`" to "all 18 finals from a labelled composite tag".

---

## 9. Why not just render asset previews?

This approach already exists in art tooling (Blender's "asset preview"). Why a new framework?
- Asset previews don't run our `MAT` registry, our HDRI strategy, or our materials variegation.
- Asset previews don't enforce the 10 design rules.
- Asset previews don't produce reproducible RNG.
- The sub-render is **a real render of the real asset in the real project pipeline**, just constrained to one asset. It is a higher-fidelity check than an asset preview.

---

## 10. Sequencing

Recommended execution order (originally dovetailed with the archived plan at `docs/_archive/2026-06-1X/UPGRADE_PLAN.md`):

1. T1.1 — build `lqv/subscene/base.py` + first 3 drivers (`cob_walls`, `bottle_wall`, `tatakuá`).
2. Validate isolation works; iterate on the template if seam issues appear.
3. Add the 5 landscape drivers.
4. Add the 7 flora drivers.
5. Activate the 8 typology stubs through their sub-render drivers.
6. Activate the 6 amenity stubs.
7. (T2.6) Wire `lqv/site/terrain_62ha.py` so typology placement validates against real DEM.
8. Composite re-render of the 18-frame matrix.

This sequence keeps the renderer byte-identity preserved through step 7. Only step 8 supersedes `85e86aa`.

---

## Cross-references

- `docs/_archive/2026-06-1X/CRITIQUE_2026-06-10.md` §2, §4 — the fragility this fixes (archived).
- `docs/_archive/2026-06-1X/UPGRADE_PLAN.md` Tier 1 T1.1, Tier 2 T2.1 — original execution scheduling (archived; sub-render framework now landed).
- `CLAUDE.md` "Critique-derived standing rules" #1 — sub-render-first as default workflow.
- `lqv/engine.py` — the setup primitives `base.py` will re-use.
- `lqv/materials.py` — `MAT` registry, mandatory for every sub-render.
- `lqv/cameras.py` — `make_view_camera(cfg, target, distance, height, lens)` dispatcher (§3.5).
- `lqv/furniture.py` — `furnish_interior(...)` for `view=interior` drivers (§3.5.4).
- `lqv/subscene/base.py` — `apply_xray_override` + `XRAY_OPAQUE_MATERIALS` allowlist (§3.5.5).
- `lqv/util/ten_rules_check.py` — per-asset rule audit.
- `lqv/util/random_audit.py` — per-asset RNG audit.
- `build_scene.py` — composite path, unchanged by this strategy.
- `STATUS.md` §4 — Tasks #36-#39 cover the sub-render queue.
- `docs/HOUSE_IMAGERY_SHOTLIST.md` §5.1 — wider catalogue-export view set (§3.5.2).
- `docs/SESSION_LOG.md` tick 21 — landing audit.
- `docs/MASTER_BRIEF.md` §13-14 — variants + design rules each sub-render must respect.
