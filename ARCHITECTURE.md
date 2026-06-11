# lqv/ package architecture

`build_scene.py` is a 93-line driver that wires these modules **in a fixed order** (see Code invariants in CLAUDE.md — the order is load-bearing because of RNG seeding). All scene content lives here; interactive blender-mcp edits are regenerated away on the next headless build.

## Top-level modules

| Module | Builds / owns | Key facts |
|---|---|---|
| `lqv/config.py` | Env-var parsing → `Config` dataclass | `SEED = 20260609`; `PROJECT_DIR` hardcoded absolute path; `RES_PRESETS` preview/720, final/1080, hero/1440 — **unknown RENDER_RES silently falls back to preview**; output naming: previews `renders/_preview_<V>_<cam>.png`, finals `renders/<V>_<cam>.png` |
| `lqv/engine.py` | Cycles setup | `engine='CYCLES'` (:15), GPU autodetect OPTIX→CUDA→HIP→METAL→ONEAPI→CPU, denoiser OPTIX/OIDN, bounces 12/12/8/4, **caustics on** (needed for bottle wall), PNG RGBA 16-bit, AgX + "AgX - Punchy" |
| `lqv/geometry.py` | Shared helpers | `new_object_from_bmesh`, `add_subdiv_displace(levels=3, noise_scale=6.0, strength=0.18)` |
| `lqv/materials.py` | All ~20 materials | `COL` hex palette; global string-keyed `MAT` dict registry; version-guarded Principled sockets (**silently skips transmission/SSS on old Blender — would invisibly kill glass + water**); 4 bottle glasses (transmission 1.0, IOR 1.52); two-layer pool water (volume absorption density 1.6) |
| `lqv/lighting.py` | Sky, sun, atmosphere | Nishita sky + explicit Sun. Variant A: elevation **13° (deliberate, vs brief's 20°)**, NNW, warm 5.5W. Variant B: 35°, cool 0.5W, soft. **Anything else raises ValueError — after the full scene build.** `build_canopy_volume`: bounded 36×42×10m scatter cube, skipped on previews |
| `lqv/cameras.py` | All 6 cameras | `hero` (28mm, (18,−33,2.4)→(10,−20,0.1)), `stream_up` (35mm), `terrace` (28mm), `cliff` (24mm), `dusk` (35mm low), `petal_macro` (85mm @ 0.4m) |
| `lqv/render.py` | Save + render | `save_blend` (overwrites scene.blend), `run` |

## Subpackages

| Module | Builds | Notes |
|---|---|---|
| `lqv/site/escarpment.py` | 80×50m cliff plane at **y=20** | Moved south to back the hero frame — coupled to camera aim |
| `lqv/site/ground.py` | 120m displaced laterite plane | |
| `lqv/site/terraces.py` | 3 stepped terraces, sandstone retaining walls | z = 1.2 − i·0.6 |
| `lqv/site/stream.py` | Stream bed, pool (r5.5 @ (11,−22)), 3 cascade boulder clusters, footbridge | Footbridge at **y=−25.5** to clear hero sightline; pool water z tuned for volume absorption |
| `lqv/house/cob.py` | Foundation, cob walls (8-pt U-plan, `_round_polyline` organic rounding), windows (Boolean `WindowCut_*` cutters — hidden, live), sod roof (bbox **±0.9m overhang**), rafters, corredor (5 posts r0.18) | Largest module (~290 lines); heavy RNG |
| `lqv/house/bottle_wall.py` | 6 clusters × 6–11 glass bottles at wall_x=6.0 | |
| `lqv/house/tatakua.py` | Dome oven r0.9 at (−5.5,−4.5) | |
| `lqv/flora/__init__.py` | `populate()`: 5 pindo, 3 lapacho, 4 mango, 4 ferns, 5 bamboo, 5 agave | Foreground lapacho at (−3,−10) for petal carpet |
| `lqv/flora/pindo.py` | 7m trunk + 14 bezier drooping fronds | Plumose droop per species spec |
| `lqv/flora/lapacho.py` | Trunk + limbs, flowering (pink puffballs) or leafed; `scatter_lapacho_petals` | Known issue: trunk uses `MAT['mango_trunk']` |
| `lqv/flora/mango.py` | Trunk + 6 displaced icospheres | |
| `lqv/flora/fern.py` | 2.8m trunk + 6 frond ellipsoids | Reuses `MAT['pindo_trunk']` |
| `lqv/flora/bamboo.py` | Leaning culm clumps + leaf masses | `scatter_grass_tufts(n=80)` exists but is **not wired into the driver yet** |
| `lqv/flora/agave.py` | 14-blade rosettes | |
| `lqv/flora/fireflies.py` | ~80 firefly emission spheres scattered on corredor + lower terrace | Variant C only; warm yellow-green emission, low-strength point sources; placed AFTER `random.seed()` so per-cam regeneration stays deterministic |

### Variant C additions (2026-06-10) — already in code, listed for navigation

- `lqv/lighting.py` — Variant C branch (cool moonlight + low blue sky strength, exposure +0.6 set in `build_scene.py`). The "Anything else raises ValueError" note above predates C and is now stale; C is a valid variant.
- `lqv/house/cob.py:build_window_emission` — warm window-glow emission planes positioned inside the hidden `WindowCut_*` cutouts so windows read as lit-from-within on Variant C only.
- `lqv/flora/fireflies.py` — see Subpackages row above.

## Coordinate convention

+Y = geographic north (escarpment, warm face — Southern Hemisphere), −Y = south (glade, stream view), +X = east. House origin on the upper terrace platform.

## Fragility — read before editing

1. **RNG draw order**: nearly every builder consumes `random.*`. Inserting, removing, or reordering any random call changes every downstream object placement. The seed is set once in `build_scene.py` after materials, before the first builder.
2. **`bpy.context.active_object` after `bpy.ops`** is used everywhere — safe headless single-threaded; do not call builders from event handlers or modified contexts.
3. **Positional coupling web** (comment-only, nothing enforces it): hero cam aim (10,−20) ↔ pool (11,−22) ↔ footbridge y=−25.5 ↔ escarpment y=20 ↔ dropped north mango spots ↔ corredor post radius. Moving one means re-checking the hero preview.
4. **`main()` runs at import** in `build_scene.py` (no `__main__` guard) — never `import build_scene`.
5. **Exposure ordering**: `setup_color_management` sets exposure 0.0, then the driver overwrites per variant. Keep that order.
6. **Validation is late or silent**: bad `RENDER_VARIANT` crashes only after the full build; bad `RENDER_RES` silently gives 720p; unknown camera warns and falls back to hero. Check your env vars before a long run.

## Known divergences from the brief (deliberate — do not "fix" without checking STATUS.md)

- Variant A sun elevation 13° not 20° (looked better; commented in lighting.py).
- Hero camera 2.4m / 28mm vs brief's 0.6m / 35mm.
- Laterite primary `#C4522A` is slightly outside the documented photo range (warmer read under AgX).

## Cross-references (additive 2026-06-10)

This file is the navigation entry for the `lqv/` Python package; multiple docs *point at* this file for code-location lookups but the reverse pointers were missing. Closed here without modifying the module tables, fragility list, or known-divergences block above.

- `CLAUDE.md` §"Document map" — names this file as the read-before-editing-code authority + lists code invariants (RNG seed ordering, MAT registry, hidden `WindowCut_*` cutters, positional coupling web) that this file's Fragility section enforces. The two files together are the contract: CLAUDE.md says *why* the invariant exists; this file says *which module enforces it*.
- `STATUS.md` — current render manifest + open-task ledger; pairs with the module table above to answer "which builder produced the artefact that's now on disk."
- `docs/SESSION_LOG.md` — narrative log of the 2026-06-10 mega-session including Variant C implementation. The "Variant C additions" block at §"Variant C additions (2026-06-10)" above is the code-side index; SESSION_LOG is the decision-side index for the same work.
- `docs/asset_plan.md` §C + §G (Cross-references) — Phase 8 asset-import plan that lands inside `lqv/asset_loader.py` (planned module, not yet in the table above). When that module is added, the table will need a new row; until then asset_plan §G is the forward-looking pointer.
- `docs/external_assets.md` §Cross-references — Sketchfab + Poly Haven download log; `USE_EXTERNAL_FLORA` flag location is documented there as targeting this package's flora subpackage.
- `docs/license_obligations.md` — Variant C procedural-recipe carve-out names the three code paths (`lqv/lighting.py` Variant C branch, `lqv/house/cob.py:build_window_emission`, `lqv/flora/fireflies.py`) listed in the §"Variant C additions" block above; the two docs must stay in sync.
- `docs/wesley_deliverable_bundle.md` §Cross-references — Tier-2 USB/cloud bundle includes "`lqv/*` Python package as a zipped reference"; this file is the navigation aid the bundle recipient (Wesley + future maintainers) uses to read that zip.
- `CREDITS.md` + `LICENSE_BUNDLE.md` — per-asset attribution + per-license summary; the procedural-recipe Variant C additions add zero new attribution rows, which both docs explicitly note. The §"Variant C additions" block above is the reciprocal source-of-truth for that "zero new third-party assets" claim.
- `docs/research/README.md` (Phase 7.5 research synthesis) — 10 design rules + 80-repo catalogue. The Fragility section above is the code-side enforcement of design rules 1 (no right angles in cob — bmesh + subdiv + displacement only), 4 (raised foundation — `lqv/house/cob.py`), 5 (wide overhangs — sod roof bbox ±0.9m), 8 (cultural Paraguay first — corredor module + tatakua module).
- `_archive/build_scene.py.pre-refactor.bak` — pre-refactor monolith; reference only, never edit or import. Listed here so readers tracing module ancestry know where the historical version lives without grepping for it.
