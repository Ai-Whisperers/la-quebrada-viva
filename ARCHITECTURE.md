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
