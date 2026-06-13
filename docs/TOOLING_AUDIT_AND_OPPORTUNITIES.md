# Tooling Audit & Improvement Opportunities — La Quebrada Viva

> Single source-of-truth document inventorying **everything the project currently uses** (Blender features, addons, satellite/geo data, models, code, scripts, third-party deps) and **everything it could plausibly adopt next** from the Blender 4.2 LTS feature set, the wider Cycles/EEVEE ecosystem, and the open-data GIS/asset universe.
>
> Companion to `docs/MASTER_BRIEF.md` (design rules), `docs/ARCHITECTURE.md` (code structure), `docs/site_data/DATA_INVENTORY.md` (geo data details), `LICENSE_BUNDLE.md` (license posture), `CREDITS.md` (per-asset attribution).
>
> Compiled by AI Whisperers (Ivan + Claude). Last updated 2026-06-13.

---

## 0. TL;DR — current state vs. headroom

**Current state.** Blender 4.2.3 LTS Cycles GPU, single addon (`blender_mcp`), AgX Punchy view transform, 12-bounce caustics, ~50 sub-render drivers, 13 typologies + 4 amenities shipped, 37 GB of CC0 / CC-BY 4.0 assets across 30 HDRIs / 121 PBR texture sets / 181 model packs / 266 `.blend` files / 2,055 raw image files, BoQ totals **$268,685.45 / Gs. 1,961 M**, 23 final renders + 609 sub-renders on disk, full DEM stack (ALOS / COP30 / NASADEM / SRTM), Sentinel-2 albedo, GEDI L2A canopy points, ERA5 climate, WorldClim bioclim, Copernicus CGLS land cover, GBIF species, OSM features.

**Biggest headroom.** Zero `GeometryNode*` calls in `lqv/` — every scatter is procedural Python via `bpy.data.objects` linking. No EEVEE Next, no Cycles Light Tree, no Adaptive Subdivision, no Mantaflow fluid, no particle systems, no light groups, no compositor LUT/grade, no Asset Browser catalogues, no OSL shaders, no USD/glTF export. The renderer at `85e86aa` is byte-frozen, so the headroom is in *additive* features (sub-renders, post-pipe, asset workflow, data-driven scatter) rather than core engine swaps.

**Top 5 deltas that would change render quality most**, ranked by effort-to-impact:
1. **Geometry Nodes scatter** (small effort, large impact) — pre-existing `lqv/flora/gn_scatter.py` skeleton + flora photoreal modules give the on-ramp; 10–100× speedup for petal/fern/anthurium clouds.
2. **Cycles Light Tree + light groups** (tiny effort, medium impact) — one flag + Cryptomatte AOV per fixture; lets us regrade Labrisa Lounge's 12 lanterns without re-rendering.
3. **NDVI-driven scatter density from Sentinel-2** (medium effort, large impact) — the data is already on disk under `docs/site_data/sentinel2/`; just needs a sampler in `lqv/flora`.
4. **Compositor LUT + per-variant grade nodes** (small effort, medium impact) — replaces the current per-variant differentiation done only at sun-angle level.
5. **Mantaflow Fluid on the creek + cascade weir** (medium-large effort, large impact for hero shots) — currently flat planes with normal-map displacement; a baked Mantaflow domain on the 80 m creek reach would carry every river/creek subscene.

The other 15 opportunities below are smaller but cumulatively change the project from "Blender 2.93 with new caustics" to "Blender 4.2 LTS using its actual feature surface".

---

## 1. Software stack — what's installed and how it's wired

### 1.1 Core

| Layer | Tool | Version | Where pinned |
|---|---|---|---|
| Renderer | Blender Cycles | 4.2.3 LTS (build 2024-10-14) | `lqv/engine.py:setup_cycles` |
| Viewport / GPU | OPTIX → CUDA → HIP → METAL → ONEAPI fallback chain | autodetected | `lqv/engine.py` `for backend in (...)` |
| Color | AgX view transform + "AgX - Punchy" look + exposure 0 | n/a | `lqv/engine.py:setup_color_management` |
| Denoiser | OPTIX on GPU+OPTIX, OPENIMAGEDENOISE otherwise; inputs = RGB + Albedo + Normal | n/a | `lqv/engine.py` denoiser branch |
| Python | system `python3` ≥ 3.11 | `pyproject.toml requires-python = ">=3.11"` | top-level `pyproject.toml` |
| Lint | ruff | py311 target, line 100, E/F/I/B/UP rules | `pyproject.toml [tool.ruff]` |
| Test | pytest | `make test` | `tests/` |
| Build | Make | targets: `smoke preview final finals sub audit lint test pdf boq deck` | `Makefile` |

### 1.2 Blender addons

**One addon enabled**: `blender_mcp` — `addon_utils.enable('blender_mcp', default_set=True, persistent=True)`. Currently the MCP socket is dead, so the addon is loaded but inert. **No other addon is enabled** — not Node Wrangler, not Animation Nodes, not BlenderKit, not the bundled Sapling Tree Gen, not Real Snow, not the Asset Browser snap-shot helpers. This is the single largest unrealised feature surface in the project (see §7).

### 1.3 Python deps (third-party, imported by `lqv/` or `scripts/`)

Resolved by grep over `lqv/` and `scripts/` import statements:

- `bpy`, `bmesh`, `mathutils` — Blender internal
- `numpy` — heightfield math, DEM resampling, scatter jitter
- `rasterio` (with `transform`, `warp`, `windows`) — DEM read/reproject, hillshade
- `h5py` — GEDI L2A `.h5` granule extraction
- `cdsapi` — ERA5 reanalysis pulls
- `python-dotenv` (`dotenv`) — `.env` parsing for OpenTopography / Copernicus API keys
- `Pillow` (`PIL`) — escritura deck assembly, swatch tiles, JPEG q=85 progressive
- `matplotlib` — DEM/Sentinel-2 quick-look plots, hillshade colour ramps
- `reportlab` (`Platypus`) — A4 landscape PDF composer for `wesley_brief_onepager.pdf`, `boq_rollup.pdf`, `escritura_deck_v1..v5.pdf`
- `pandoc` (via `subprocess`) — Markdown → PDF fallback before reportlab path
- Standard library used heavily: `pathlib`, `csv`, `json`, `xml.etree`, `urllib.request`, `concurrent.futures` (asset downloader pool of 8), `dataclasses`, `argparse`.

### 1.4 External CLI tools assumed present

- `gdal` (`gdalinfo`, `gdalwarp`, `gdaldem`) — DEM reprojection + hillshade
- `pandoc` + a LaTeX engine (one-pager PDF fallback path)
- `pdftotext` (`poppler-utils`) — escritura deck verification sweep
- `convert` / `magick` (ImageMagick) — texture set conversions when ambientCG ships TIFF
- `gh` — GitHub remote (T0.1 done, repo at `Ai-Whisperers/la-quebrada-viva` private)
- `git`, GNU `find`, `grep`, `du` — repo hygiene

---

## 2. Blender feature usage — what we touch today

### 2.1 Cycles engine config (`lqv/engine.py`)

```text
scene.cycles.device                    GPU (auto-fallback CPU)
scene.cycles.samples                   128 (env: RENDER_SAMPLES)
scene.cycles.use_denoising             True
scene.cycles.denoiser                  OPTIX | OPENIMAGEDENOISE
scene.cycles.denoising_input_passes    RGB_ALBEDO_NORMAL
scene.cycles.max_bounces               12
scene.cycles.transmission_bounces      12
scene.cycles.glossy_bounces            8
scene.cycles.volume_bounces            4
scene.cycles.transparent_max_bounces   12
scene.cycles.caustics_reflective       True   ← unusual, kept for jacuzzi + glass-bowl pendants
scene.cycles.caustics_refractive       True   ← unusual, kept for cascade-weir + creek surface
```

Resolutions: `preview 1280×720`, `final 1920×1080`, `hero 2560×1440`. Output `PNG RGBA 16-bit`.

### 2.2 Color pipeline

`view_transform = 'AgX'` + `look = 'AgX - Punchy'` + `exposure = 0.0` — the 4.2 LTS punchy preset is enabled and never overridden per-variant. Nothing downstream of Cycles output touches colour except the per-asset compositor (which is currently a passthrough).

### 2.3 Shader nodes actually used (grep over `lqv/materials/_shaders.py`)

`ShaderNodeTexImage` (Diffuse/Roughness/Normal/Displacement/AO), `ShaderNodeBsdfPrincipled` (implicit via `node_groups`), `ShaderNodeMapping`, `ShaderNodeMixRGB`, `ShaderNodeNormalMap`, `ShaderNodeBump`, `ShaderNodeDisplacement`, `ShaderNodeNewGeometry`, `ShaderNodeMath`, `ShaderNodeTexNoise`. **Not used**: OSL nodes, Vector Curves, Color Mix RGB, Voronoi, Wave, Brick, Magic, Checker, Gradient — all Blender procedural textures are absent.

### 2.4 Geometry pipeline

100% procedural Python via `bpy.ops.mesh.primitive_*_add`, `bmesh` operators, and `bpy.data.objects` linking. **Zero `GeometryNodes` modifiers anywhere in `lqv/`** (confirmed by `grep -r "node_groups\|GeometryNode" lqv/` → empty). Subdivision Surface modifiers used selectively in house parts; no Adaptive Subdivision, no displacement-via-shader-displacement.

### 2.5 Particle systems / physics

**Not used**. No `bpy.data.particles`, no Mantaflow domains, no cloth/soft-body sim, no rigid-body, no hair systems. Petal scatter for `scatter_lapacho_petals*` is done as instanced mesh copies, not a particle system.

### 2.6 World / lighting

HDRI rotation per-variant exists in env-var control surface (`RENDER_VARIANT=A|B|C`), but the actual world setup uses one HDRI per sub-render call site, not a rotation matrix. Sun lamp + 1-3 area lamps per scene typical. **No light groups, no Cycles light tree, no light linking.**

### 2.7 Compositor

The compositor is a passthrough on all sub-renders — `Render Layers → Composite`. No tone-mapping nodes, no LUT, no grade ramp, no glare, no defocus, no Cryptomatte split, no AOV merge. The AgX Punchy view transform does all the colour work.

### 2.8 Cameras + framing

Custom `lqv/cameras/__init__.py` ladder: `hero / stream_up / terrace / cliff / dusk / petal_macro` for the parcel-scale renders + per-asset `subscene_camera()` helper. The subscene camera is the one that needs `clip_end = base.PARCEL_CLIP_END_M = 20000.0` to avoid HDRI-only renders (per `feedback_subscene_clip_end`).

---

## 3. Asset inventory — 37 GB on disk

### 3.1 Top-line counts

| Category | Count | Format |
|---|---|---|
| HDRIs (`.exr` 4K) | **30** | `assets/hdris/<id>_4k.exr` |
| PBR texture sets | **121** | `assets/textures/<id>/{diff,nor_gl,rough,disp,ao}_4k.{jpg,png}` |
| Model packs | **181** | `assets/models/<id>/<id>.{blend,glb,fbx}` |
| `.blend` files (resolved) | **266** | scattered across `assets/` and `assets/sketchfab/` |
| Raw image files | **2,055** | maps + reference photos |
| **Total disk** | **37 GB** | (mostly 4K EXR HDRIs + 4K PBR maps) |

### 3.2 HDRI roster (Poly Haven CC0, 4K EXR)

`kiara_1_dawn`, `misty_pines`, `qwantani_dusk_2`, `qwantani_sunset_puresky`, `autumn_field_puresky`, `kloppenheim_02_puresky`, `bambanani_sunset`, `kloofendal_48d_partly_cloudy_puresky`, `satara_night`, `shanghai_bund` and ~20 more queued via `download_polyhaven_assets.py`. The `_puresky` variants are sun-included (drive Cycles sun via the HDRI itself).

### 3.3 Texture roster (Poly Haven + ambientCG, all CC0)

Grounds: `aerial_mud_1`, `aerial_grass_rock`, `aerial_rocks_02`, `aerial_sand`, `aerial_beach_01`, `aerial_asphalt_01`, `aerial_ground_rock`, `bicolour_gravel`, `brown_mud` + 4 variants (`_02`, `_03`, `_dry`, `_leaves_01`, `_rocks_01`), `cracked_red_ground`, `muddy_tracks`, `forest_floor`, `burned_ground_01`.

Cliff/rock: `dry_riverbed_rock`, `cliff_side`, `rock_face`, `rock_wall_10`, `lichen_rock`, `gray_rocks`.

Walls: `clay_block_wall`, `clay_plaster`, `brick_4`, `brick_floor`, `brick_pavement`, `brick_wall_001/003/006/08/11/13`, `broken_brick_wall`, `brown_brick_02`, `beam_wall_01`, `beige_wall_001/002`, `blue_plaster_weathered`, `box_profile_metal_sheet`.

Wood/bark: `dark_wood`, `wood_floor_deck`, `tree_bark_03`, `palm_tree_bark`, `bark_platanus`, `bark_brown_01/02`, `bark_willow`, `bark_willow_02`, `brown_planks_03/05/09`.

(Full list in `assets/textures/` — 121 directories, complete inventory in `docs/ASSETS_INVENTORY.csv`.)

### 3.4 Model roster (sample of 181)

Vegetation: `fir_tree_01`, `grass_medium_02`, `flower_empodium`, `anthurium_botany_01`, `periwinkle_plant`, `shrub_03`, `flower_stinkkruid`, `root_cluster_01`.

Rocks: `coast_land_rocks_04`, `namaqualand_boulder_02`.

Containers/props: `metal_jerrycan_green`, `metal_jug`, `brass_vase_03`, `lantern_chandelier_01`, `planter_box_01`, `wooden_bucket_01`, `barrel_stove`, `old_tyre`, `large_castle_door`.

Tools: `measuring_tape_01`, `bench_vice_01`, `sledgehammer_01`, `trowel_01`.

(All Poly Haven CC0 except 11 attributed Sketchfab CC-BY 4.0 per `CREDITS.md`. Hard exclusions in `LICENSE_BUNDLE.md` §3.)

### 3.5 Asset acquisition scripts

`scripts/download_polyhaven_assets.py` — CONCURRENCY=8, TIMEOUT=120, TEXTURE_MAPS=`["Diffuse","nor_gl","Rough","Displacement","AO"]`, TEXTURE_RES_FALLBACK=`["4k","8k","2k","1k"]`. Pulls from `https://api.polyhaven.com` + `https://dl.polyhaven.org/file/ph-assets/`.

`scripts/download_ambientcg_assets.py` — same pattern, ambientCG CC0 blanket.

`scripts/download_assets.sh` — orchestrator that calls both with the canonical asset list.

---

## 4. Geo / satellite data inventory

Full details in `docs/site_data/DATA_INVENTORY.md` (1,200 lines). Top-line summary:

### 4.1 DEMs (4 cross-validated, all 30 m)

| Dataset | Source | RMSE | Use |
|---|---|---|---|
| **ALOS AW3D30** (canonical) | JAXA PRISM stereo, 2006-2011 | ~5 m | `lqv/site/terrain_62ha.py` heightfield |
| COP30 (GLO-30) | ESA Sentinel-2 optical stereo, 2018-2021 | ~4 m | cross-check, canopy diff |
| NASADEM | NASA reprocessed SRTM, 2020 | ~4 m | cross-check |
| SRTM v3 GL1 | NASA shuttle radar, 2000 | ~5-9 m | legacy reference |

All four cover the same `W -57.045 / S -25.645 / E -57.015 / N -25.615` 3.3 km × 3.3 km bbox around Escobar, Paraguarí. Each has a paired hillshade PNG (45° altitude, 315° azimuth NW sun).

Derived from ALOS: `alos_slope.tif`, `alos_aspect.tif`, `alos_buildability.tif` (4-class slope buckets), `site_diagnostic.png` master overlay.

### 4.2 Vegetation

`gedi_l2a_points.csv` — 475 raw LiDAR shots from 27 GEDI granules (2019-2025), filtered to 25 clean shots with `quality_flag=1`, `degrade_flag=0`, `sensitivity > 0.95`. Canopy height = `elev_highestreturn − elev_lowestmode`.

`sentinel2/` — Sentinel-2 L2A surface reflectance bands B02/B03/B04/B08 (10 m) + B11/B12 (20 m), plus a baked `terrain_albedo.png` (already used in the 62-ha render) and the unrealised NDVI / EVI products that `make_vegetation_indices.py` can derive on demand.

`worldclim/` — 19 bioclim variables (WorldClim 2.1, 30 arc-sec ~1 km).

`climate_era5/` — ERA5 hourly reanalysis for the bbox (temp, precip, wind, solar).

`cgls_lcover/` — Copernicus CGLS Global Land Cover 100 m (15 cover classes).

`gbif/` — GBIF species occurrence dump within 5 km of the parcel.

`osm/` — OpenStreetMap features (roads, buildings, waterways).

### 4.3 Geo acquisition scripts

`fetch_opentopo_dem.py`, `fetch_sentinel2.py`, `fetch_vegetation_3d.py`, `extract_gedi*.py` (3 variants: HTTPS, S3, generic), `clean_gedi.py`, `fetch_era5_climate.py`, `fetch_worldclim.py`, `fetch_copernicus_lcover.py`, `fetch_gbif_species.py`, `fetch_osm.py`. Plus the analysis scripts: `analyze_dem.py`, `analyze_assets.py`, `analyze_era5_climate.py`, `analyze_stream.py`, `make_hillshades.py`, `make_terrain_albedo.py`, `make_terrain_heightmap.py`, `make_vegetation_indices.py`.

---

## 5. `lqv/` code inventory

### 5.1 Top-level modules

```
lqv/
├── amenities/         4 amenities (labrisa_lounge, eco_pool, floating_dining, eco_retreat_modern_oasis) + _grammar.py
├── animation/         turntable, equirectangular pano
├── asset_loader/      shared blend-link helpers
├── boq/               Bill of Quantities walker
├── cameras/           hero/stream_up/terrace/cliff/dusk/petal_macro + subscene_camera helper
├── config/            env-var control surface (RENDER_VARIANT etc.)
├── engine.py          Cycles + AgX + denoiser setup
├── finance/           USD↔PYG FX, cost rollups
├── flora/             agave anthurium bamboo fern fireflies groundcover lapacho mango pindo sapling_bridge + photoreal.py + gn_scatter.py (skeleton)
├── geometry/          mesh decompose, boolean cutter helpers
├── house/             bamboo_frame bottle_wall cob corredor_props mesh_decompose services stone_wall tatakua window_cones window_specs yard_props
├── lighting/          (empty — opportunity area, see §7)
├── materials/         _palette.py _shaders.py bricks earth foliage glass props wood
├── output/            equirectangular, save helpers
├── render/            queue, status check
├── restaurant/        dining_hall garden_deck kitchen
├── site/              base.py escarpment ground section_view site_plan stream terraces terrain_62ha terrain_dsl
├── subscene/          48 sub-render drivers (see §5.2)
├── typologies/        13 buildable house typologies (see §5.3)
└── util/              material_audit random_audit sun_check ten_rules_check
```

### 5.2 Sub-render driver count

`ls lqv/subscene/*.py` → **48 drivers** (one per buildable asset + utility drivers like `terrain_house_scale`, `material_swatch`, `flora_clump`). Pattern is the sub-render-first workflow per `feedback_sub_render_first`: `base.setup → place_neutral_ground → build → cameras.subscene_camera → cam.data.clip_end = PARCEL_CLIP_END_M → base.setup_world → base.save_subrender`.

Output convention (per `feedback_render_run_folders`): `renders/sub/runs/<RENDER_RUN_ID>_<asset>[_<tag>]/<variant>.png` mirrored to `renders/sub/latest/` and a legacy flat path.

### 5.3 13 typologies

Defined in `lqv/typologies/__init__.py:TYPOLOGIES`. Per Phase C reconciliation: `hobbit_house`, `italian_stone_small_v1`, `italian_stone_small_v2`, `italian_river_house_4pax`, `container_river_house`, `bamboo_river_house`, `bamboo_boomhut_treehouse`, `bamboo_container_4pax`, `bamboo_wigwam_lodge`, `bamboo_beton_30`, `bamboo_beton_28`, `bamboo_beton_family_curved`, `bamboo_beton_family_rectangular`. Plus reference-only `cob_bottle_lqv` built via top-level `build_scene.py` (not a buildable typology).

Each emits a `MATERIAL_TAKEOFF: dict[str, dict]` consumed by `lqv/boq.py`.

### 5.4 4 amenities

`labrisa_lounge`, `eco_pool`, `floating_dining`, `eco_retreat_modern_oasis`. Share `lqv/amenities/_grammar.py` (cascade weir, stepping stones, glass-bowl pendants, boulder seats).

### 5.5 Render output state

- **23 final renders** under `renders/*.png` (last 18 finals at `85e86aa` — A/B/C × 6 cams).
- **609 sub-renders** under `renders/sub/runs/` + `renders/sub/latest/`.

### 5.6 Render entry points

- `build_scene.py` (top-level) — frozen at `85e86aa`, do not touch.
- `scripts/render_preview.sh / render_final.sh / render_all_finals.sh` — wrappers around `blender --background --python build_scene.py`.
- `scripts/render_models_gallery.py` — gallery loop for the 13 typologies + 4 amenities.
- `scripts/render_elevations_all.py` — 4 elevations × 13 typologies = 52 PNGs.
- `scripts/render_terrain_62ha_photoreal*.sh` — variants v3_hd / v4_polish / v5_arrowfix / v5.
- `Makefile` targets: `make preview / final / finals / sub / smoke / audit / pdf / boq / deck`.

### 5.7 Audit + smoke

`lqv/util/random_audit` — RNG seed audit (SEED=20260609, must follow `materials.build_materials()` and precede first `build_*`).

`lqv/util/material_audit` — confirms every mesh has a non-default material slot.

`lqv/util/sun_check` — sanity-checks sun azimuth/elevation against latitude.

`lqv/util/ten_rules_check` — verifies the 10 Master-Brief design rules.

`scripts/smoke_test.sh` — full-scene build without render, then `ten_rules_check`.

---

## 6. Scripts inventory (40 files, grouped)

**Analysis** (5): `analyze_assets.py`, `analyze_dem.py`, `analyze_era5_climate.py`, `analyze_stream.py`, `asset_manifest_check.py`.

**Asset acquisition** (4): `download_ambientcg_assets.py`, `download_assets.sh`, `download_polyhaven_assets.py`, `stamp_license_stubs.py`.

**Geo fetch** (10): `clean_gedi.py`, `extract_gedi_https.py`, `extract_gedi_s3.py`, `extract_gedi.py`, `fetch_copernicus_lcover.py`, `fetch_era5_climate.py`, `fetch_gbif_species.py`, `fetch_opentopo_dem.py`, `fetch_osm.py`, `fetch_sentinel2.py`, `fetch_vegetation_3d.py`, `fetch_worldclim.py`.

**Terrain + raster prep** (4): `make_hillshades.py`, `make_terrain_albedo.py`, `make_terrain_heightmap.py`, `make_vegetation_indices.py`.

**Render** (8): `check_gpu.sh`, `render_all_finals.sh`, `render_elevations_all.py`, `render_final.sh`, `render_models_gallery.py`, `render_preview.sh`, `render_queue.py`, `render_status_check.py`, `render_terrain_62ha_photoreal{.sh, _v3_hd.sh, _v4_polish.sh, _v5_arrowfix.sh, _v5.sh}` (5 variants), `smoke_test.sh`.

**Build / PDF** (4): `build_boq.py`, `build_escritura_deck.py`, `build_terrain_62ha_blend.py`, `build_wesley_onepager_pdf.py`.

**Infra** (2): `mcp_daemon.py` (NEVER STAGE), `test_stac.py`.

---

## 7. Improvement opportunities — what we could adopt next

Each item below has: **what / why / on-ramp / effort / risk / status**. Ranked into three tiers.

### Tier 1 — high impact, low effort (do these next)

#### 7.1 Geometry Nodes scatter migration

**What.** Port the Python-driven scatter in `lqv/flora/*.py` to Geometry Nodes trees built once and applied as modifiers. Density driven by an input attribute (NDVI, slope, distance-from-creek) instead of hand-tuned per-call loops.

**Why.** GN scatter runs on GPU and instances at draw time — 10–100× faster than `bpy.data.objects.new + collection.objects.link` loops. Lapacho petal scatter (~5,000 instances per sub-render) is the obvious first target; ferns + anthurium clouds + `groundcover.py` next.

**On-ramp.** `lqv/flora/gn_scatter.py` already exists as a skeleton — wire it up. The pattern is `Distribute Points on Faces (density attr) → Rotate Instances (random_value(-pi, pi)) → Scale Instances (random_value(0.7, 1.3)) → Set Position (z = noise) → Instance on Points (collection)`.

**Effort.** 1-2 days for the first three flora types.

**Risk.** Petal count for `scatter_lapacho_petals*` is part of the byte-frozen renderer at `85e86aa` — must port without touching that scatter. Solution: build GN variants of the *other* flora first, leave the lapacho scatter as-is until Step 8 re-render unfreezes the renderer.

**Status.** Pending. Highest ROI.

#### 7.2 Cycles Light Tree

**What.** Single flag: `scene.cycles.use_light_tree = True` (default in 4.2 for many-light scenes but must be confirmed on subscenes).

**Why.** Labrisa Lounge has ~12 lantern lamps; Eco Pool has 6 underwater LEDs; floating dining has 8 candle proxies. Without light tree, every sample evaluates every light. With it, Cycles builds a BVH over lights and importance-samples by power × inverse-distance. Render time on those three amenities drops ~30–40%.

**On-ramp.** One line in `lqv/engine.py:setup_cycles`. Worth a per-asset benchmark first to confirm not slower on single-sun scenes.

**Effort.** 30 minutes.

**Risk.** None. Toggleable per-scene.

**Status.** Pending.

#### 7.3 Light groups + Cryptomatte AOVs

**What.** Tag each lamp with a light group; render a Cryptomatte object/material AOV; let the compositor scale per-group contribution.

**Why.** Re-grade lantern colour temperature (2700 K → 2400 K, etc.) for Variant B without re-rendering. Same for candle warmth, sun strength, fill bounce.

**On-ramp.** `view_layer.use_pass_cryptomatte_object = True`, `light.cycles.lightgroup = "lanterns"`. Compositor `Cryptomatte` node + `Mix` per group.

**Effort.** 1 day for the framework, then ~10 min per asset to tag.

**Risk.** Adds AOV passes → bigger EXR files. Acceptable for finals.

**Status.** Pending.

#### 7.4 Compositor LUT + per-variant grade nodes

**What.** Add a compositor node group `LQV_Grade` with: per-variant Curves (RGB + per-channel) → ASC-CDL slope/offset/power → 3D LUT slot. Per-variant grades baked into a `.cube` LUT in `docs/finance/` (or `docs/grades/`).

**Why.** Currently A/B/C variants differ only by sun angle and HDRI rotation. A grade pass lets Variant A be "cool dawn", Variant B be "warm dusk", Variant C be "high-noon clear" without touching the scene.

**On-ramp.** `bpy.context.scene.use_nodes = True`, build the node group in `lqv/output/compositor.py` (new file).

**Effort.** Half a day.

**Risk.** Must not double-apply grade if AgX Punchy already pushes the look. Bake reference patches first.

**Status.** Pending. Links to `#17 T1.6`.

#### 7.5 NDVI-driven scatter density

**What.** Sample `docs/site_data/sentinel2/B08` and `B04`, compute `NDVI = (B08 − B04) / (B08 + B04)`, project onto the 62 ha heightfield UV. Pass as an attribute to the GN scatter (7.1).

**Why.** Currently scatter densities are hand-tuned uniform. NDVI knows where the real forest is — places anthuriums in the riparian zone, agave on the dry plateau, ferns in the gorge.

**On-ramp.** `scripts/make_vegetation_indices.py` already computes NDVI. Need a `lqv/site/ndvi_sampler.py` that takes a `(lat, lon)` and returns NDVI ∈ [-1, 1].

**Effort.** 1 day (sampler + GN attribute wiring).

**Risk.** Sentinel-2 is 10 m — won't resolve sub-meter scatter detail. Use as low-frequency density, multiply by Perlin noise for high-frequency variation.

**Status.** Pending.

### Tier 2 — medium impact, medium effort

#### 7.6 Mantaflow Fluid on creek + cascade weir

**What.** Bake a Mantaflow liquid domain over the 80 m creek reach (or just the 4 m cascade weir + 8 m pool for hero shots). Replace the current flat-plane + normal-map approach in `lqv/site/stream.py` and `lqv/amenities/_grammar.py:cascade_weir`.

**Why.** The creek is the centrepiece of the parcel and shows in every "river" typology + Labrisa Lounge + Eco Pool. Photoreal moving water in the hero shots is a step-change in believability.

**On-ramp.** Cache to `assets/sim/creek/`, 250 frames per variant, viscosity ≈ 0.1, surface tension ≈ 0.05. Bake offline once, link via Alembic.

**Effort.** 2-3 days (sim takes overnight; tuning takes a day; integration takes half a day).

**Risk.** Sim file sizes (~5-10 GB cache). Mitigated by keeping the cache out of git (`assets/sim/` in `.gitignore`) and shipping a low-res preview cache for repro.

**Status.** Pending. Big-win item for the escritura deck cover render.

#### 7.7 Particle systems for petal fall + dust

**What.** Replace `lqv/scatter_lapacho_petals*` (post Step 8) with a real particle system using lapacho petals as instance object, gravity + wind force fields, collision deflector on terrain.

**Why.** The current scatter is a static scatter of petals on the ground. A particle system gives mid-air petals + animation pass for the turntable + per-frame randomness that prevents the obvious "scatter pattern" tell.

**On-ramp.** Particle settings: type=emitter, lifetime=120, count=2000, physics=newtonian, gravity=0.4, brownian=0.2, drag=0.3, wind_force_field at site.

**Effort.** 1 day.

**Risk.** Cannot land until Step 8 unfreezes `build_scene.py`.

**Status.** Blocked by `#18 Step 8`.

#### 7.8 Volumetrics — extend valley_mist driver

**What.** The valley_mist driver exists; volumes are not used in sub-renders (intentional, to keep sub-render times under 30 s). For the final composite (Variant B = dusk), add a low-density principled volume in the gorge ($0.005$ density, $5 m$ anisotropy 0.6) lit by the sun lamp.

**Why.** Dusk Variant B is currently dry on atmospherics. A mist pass would carry the depth cue from foreground rocks → mid-ground house → background escarpment far stronger than fog colour-mix in the compositor.

**On-ramp.** `lqv/site/valley_mist.py` driver exists. Add per-variant guard so only Variant B (or env var `RENDER_VOLUMETRICS=1`) enables it.

**Effort.** Half a day.

**Risk.** Adds ~30% render time per frame. Worth it on 18 finals.

**Status.** Pending. Folds into `#18 Step 8`.

#### 7.9 Asset Browser catalogues

**What.** Build `assets/_catalog/lqv.blend` with marked-asset versions of every house part, every flora prototype, every material. Drag-and-drop into any scene in interactive Blender.

**Why.** Currently the only way to put a `tatakua` wall in a new scene is to import the module and call `build_tatakua_wall()`. With a catalogue, an interactive user (Wesley reviewing) can pull it from the Asset Browser sidebar.

**On-ramp.** `bpy.ops.asset.mark`, `bpy.ops.asset.assign_action` per object, save catalogues in a `.cats.txt` file at the catalogue root.

**Effort.** 1 day.

**Risk.** None.

**Status.** Pending. Useful for client review sessions, not for headless renders.

#### 7.10 OSL shaders for procedural Paraguayan materials

**What.** Three OSL shaders that procedural-Python can't easily express:
1. **Red-laterite weathering** — distance-from-up-edge → reddish-orange runoff streaks.
2. **Tatakua bone-soot** — UV-driven soot accumulation in the lattice gaps, weighted by occlusion AO.
3. **Palm-thatch silver-grey UV ageing** — per-strand age noise driving a Diffuse → Grey ramp.

**Why.** These are Paraguay-specific looks that aren't on Poly Haven. OSL is the right place for procedurals tied to mesh attributes.

**On-ramp.** `cycles.shading_system = 'OSL'`, write three `.osl` files in `lqv/materials/osl/`, load via `ShaderNodeScript(filepath=...)`. OSL is CPU-only on Cycles, so guard usage behind a per-asset toggle.

**Effort.** 2 days (one per shader, plus tuning).

**Risk.** OSL forces CPU render. Use only for materials whose look genuinely needs it; keep wood/brick/clay on standard nodes.

**Status.** Pending. Tier-2 because looks-impactful but bounded.

#### 7.11 Sapling Tree Gen for lapacho variation

**What.** Enable bundled `add_curve_sapling` addon, generate 5 lapacho variants (different trunk taper / branch density / canopy shape), seed-vary at scatter time.

**Why.** Current `lqv/flora/lapacho.py` builds one lapacho geometry; the hero render visibly repeats it. Sapling Tree Gen would give per-instance variation without authoring each tree manually.

**On-ramp.** `addon_utils.enable("add_curve_sapling")`, `bpy.ops.curve.tree_add(...)`, bake to mesh, store in `assets/_trees/lapacho/var{1..5}.blend`.

**Effort.** 1 day.

**Risk.** None.

**Status.** Pending.

#### 7.12 Adaptive Subdivision + displacement

**What.** Apply Adaptive Subdivision modifier to cob walls + river bed + terrace surfaces with displacement driven by texture (already on disk) instead of pre-baked mesh detail.

**Why.** Cob walls in `lqv/house/cob.py` currently use subdivision + bump. Adaptive subdiv with displacement gets actual silhouette detail at render time, with auto-LOD based on screen-space pixel size.

**On-ramp.** `obj.modifiers.new('subsurf', 'SUBSURF')` + `mod.subdivision_type = 'CATMULL_CLARK'` + `mod.use_adaptive_subdivision = True` + set displacement input in material.

**Effort.** Half a day (per material that needs it).

**Risk.** Increases memory + render time. Use only on hero-pose materials.

**Status.** Pending.

### Tier 3 — useful but lower priority

#### 7.13 EEVEE Next preview pipeline

**What.** Add `scripts/render_eevee_preview.sh` using EEVEE Next (4.2 LTS) for ~10× faster preview iteration.

**Why.** Currently `make preview` = Cycles 128 samples. EEVEE Next at the same quality preset takes 5-15 s/frame vs. 60-120 s/frame for Cycles preview.

**On-ramp.** `scene.render.engine = 'BLENDER_EEVEE_NEXT'`, screen-space reflections + raytraced shadows + light bake.

**Effort.** Half a day to get to "looks close enough for camera framing".

**Risk.** EEVEE Next ≠ Cycles. Use only for camera blocking, never for finals.

**Status.** Pending.

#### 7.14 Baked lighting / shadow caches

**What.** Bake static lighting (sun + HDRI bounce) on the terrain mesh into a vertex colour layer; bake AO on house parts into a texture; use as base layer in materials.

**Why.** ~30% sample-count reduction for sub-renders on assets with heavy AO contribution.

**On-ramp.** `bpy.ops.object.bake(type='AO')`, save to `assets/_baked/<asset>_ao.png`, swap material slot to use baked map.

**Effort.** 1 day.

**Risk.** Bakes are static — must rebake if mesh changes. Manage via a `--rebake` flag in subscene drivers.

**Status.** Pending.

#### 7.15 USD / glTF export

**What.** `make export-usd` + `make export-gltf` targets that write `assets/_export/lqv.usdz` and `assets/_export/lqv.gltf` from a stripped scene.

**Why.** Wesley can drag the `.usdz` into Apple Quick Look on iPhone; the `.gltf` runs in a `<model-viewer>` element on the project landing page. Both are zero-install for him.

**On-ramp.** `bpy.ops.wm.usd_export(filepath=...)`, `bpy.ops.export_scene.gltf(filepath=...)`. Strip volumetrics + sims first (USD spec doesn't carry them).

**Effort.** 1 day.

**Risk.** USD shader translation is lossy for OSL nodes (7.10). Glb size on a typology can hit 100 MB without LOD.

**Status.** Pending. Big client UX win.

#### 7.16 Bake-to-Vertex-Colour for BoQ swatches

**What.** Bake the diffuse texture of every BoQ material to a vertex colour layer on a 1 m³ swatch cube; render the swatch grid (12 swatches per page).

**Why.** Currently `boq_rollup.pdf` references material names; with rendered swatches, Wesley can match what he's specifying with what he's seeing.

**On-ramp.** `bpy.ops.object.bake(type='DIFFUSE')` into vertex colours, render 12 swatches → grid → page.

**Effort.** 1 day.

**Risk.** None.

**Status.** Pending.

#### 7.17 Real Snow / Real Camera / Photographer addons

**What.** Three community addons (all on the BlenderMarket / GitHub):
- **Real Snow** — procedural snow drift on top of geometry (not relevant here, the parcel has no snow — skip).
- **Real Camera** — physical-camera params (focal length, f-stop, shutter, ISO) bound to exposure. Useful for matching reference photo exposure to render.
- **Photographer 5** — same idea, more polish; also handles lighting setups.

**Why.** Currently camera FOV is set in degrees with no tie to lens/sensor. Real Camera gives the "use a 35mm lens at f/5.6" workflow.

**On-ramp.** GitHub releases. **Both are paid addons** for the polished versions; CC0-equivalent free versions exist (`Camera Calibrator`).

**Effort.** Half a day to wire up Camera Calibrator (free).

**Risk.** License. Paid versions violate the CC0-first stance — stick with free equivalents.

**Status.** Pending. Low priority.

#### 7.18 Multi-resolution sculpting on hobbit_house berm

**What.** Apply Multires modifier to the hobbit_house berm + the terraces, sculpt organic micro-detail (roots, footpaths, grass tufts) at level 4.

**Why.** Pure procedural displacement looks too uniform; hand-sculpted detail at hero-scale matters.

**On-ramp.** Multires + Sculpt Mode in interactive Blender; bake to displacement texture, ship texture + low-res mesh in `assets/_sculpts/`.

**Effort.** 1-2 days (this is hand work).

**Risk.** Can't fully automate. Acceptable.

**Status.** Pending. Lowest priority.

#### 7.19 Animation Nodes / Crowd sim for proxy figures

**What.** Add walking-scale human proxies on terraces + dining areas. Animation Nodes gives a fast crowd sim; alternatively reuse Mixamo CC0 figures via `assets/sketchfab/<crowd_uid>/`.

**Why.** Scale cue. Empty buildings look like dollhouses.

**On-ramp.** 2-3 mid-poly CC0 humans + IK rig + walk cycle path-constrained.

**Effort.** 2 days.

**Risk.** Mixamo isn't strictly CC0; verify per-figure. Sketchfab CC-BY 4.0 path works.

**Status.** Pending. Low priority but big "feels alive" win.

#### 7.20 Hydra / Karma / OctaneRender swap

**What.** Render-delegate swap to test alternative renderers.

**Why.** Sanity check on light transport; comparison for hero shots.

**On-ramp.** Karma free via Houdini Indie; Hydra delegate plugin for Blender 4.2.

**Effort.** 2 days first time, low after.

**Risk.** Hydra MaterialX translation is lossy.

**Status.** Pending. Curiosity-driven, not Wesley-driving.

---

## 8. Data we have but underuse

| Data | What it could drive | Current use | Headroom |
|---|---|---|---|
| Sentinel-2 B02-B12 | NDVI scatter density (7.5), EVI for tree vigour, water mask, dry-season albedo shift | Only baked albedo PNG | Large |
| GEDI canopy heights | Per-tree height for `lqv/flora/lapacho.py` + `mango.py` placement | Stored, not consumed | Medium |
| WorldClim bioclim 1-19 | Per-month sun intensity / colour-temp / precipitation drive for variant selection | Not used in renderer | Medium |
| ERA5 hourly reanalysis | Sun-angle table for a specific date+time (e.g. escritura day 2026-06-27 at 14:00 local) | Not used | Small but slick |
| Copernicus CGLS land cover | Mask for tree_scatter polygon (forest only, not pasture) | Not used | Medium |
| GBIF species | Species choice for `flora/*` (use *Tabebuia heptaphylla*, not generic "tree") | Not used | Small |
| OSM features | Existing trail / fence / waterway layout | Not used | Small |
| 4 cross-DEM stack | Confidence map for `terrain_62ha` heightfield | Only ALOS used | Small |

The most under-used piece is Sentinel-2 — we already paid the API cost to pull it and it can drive both 7.5 NDVI scatter and a real per-month seasonal variant.

---

## 9. Asset universe we haven't tapped

CC0 / CC-BY 4.0 only (per `LICENSE_BUNDLE.md`):

- **Poly Haven HDRIs not yet pulled** — sunny tropical sites (e.g. `kloofendal_43d_clear`, `pretoria_gautrain`, `qwantani_dusk_2` already in, but `cape_hill` + `industrial_sunset_puresky` + `sunrise_meadow` would help Variant A "dawn over the gorge").
- **Poly Haven textures not yet pulled** — `gravel_concrete`, `paving_stones_99`, `wet_concrete`, `corrugated_iron`, `weathered_iron_sheets` for outbuildings; `aerial_grass_rock_03`, `aerial_grass_rock_06` for terrace covers.
- **ambientCG** — same blanket CC0; gap-fill where Poly Haven doesn't have what we need (red-laterite specific, broken terracotta tile).
- **3DScans.com** — CC0 photoscan boulders, perfect for the cascade weir and stream stones.
- **Quaternius** — CC0 low-poly props (people, vehicles) for scale cueing.
- **Kenney.nl** — CC0 props.
- **Polyhaven Models 4.0+** — recently added moss-on-rock and lichen-on-bark variants.

We currently have 30 HDRIs and 121 texture sets; the working ceiling under our license posture is probably ~80 HDRIs + ~300 texture sets without diminishing returns.

---

## 10. Render pipeline gaps

### 10.1 No AOV passes

Currently `view_layer.use_pass_*` flags are at default (Combined + Z). Should turn on at minimum: Diffuse Direct/Indirect/Color, Glossy Direct/Indirect/Color, Transmission, Volume Direct/Indirect, Normal, Mist, Cryptomatte Object/Material.

Cost: ~3× output filesize. Benefit: any post-render colour tweak doable in the compositor.

### 10.2 No render queue UI

`scripts/render_queue.py` exists; not surfaced. A `make queue` target + simple TUI showing the 18-frame final state (queued/running/done/failed) would help during the escritura push.

### 10.3 No render-status JSON

`scripts/render_status_check.py` checks; doesn't emit a machine-readable status file. Useful for a "is the final composite ready for the deck" gate in `build_escritura_deck.py`.

### 10.4 No bake-the-floor caching

Subscene drivers regenerate the neutral ground from scratch every call. Caching `place_neutral_ground` to a `.blend` link would save ~5 s per sub-render × 600 sub-renders = ~50 min.

---

## 11. Code quality gaps

- `lqv/lighting/` directory exists but is empty. Lighting decisions are scattered across `lqv/subscene/*.py` and per-typology builders. Centralising into `lqv/lighting/{key,fill,sun,hdri}.py` would let us drive Variant A/B/C from one place instead of mirroring sun config in 48 drivers.
- `lqv/materials/_palette.py` is the colour palette source. Should be the single source for grade nodes too (7.4) — currently grade is implicit in AgX Punchy.
- `tests/` directory exists; coverage is on the audit utils + smoke. No tests for `lqv/boq.py` arithmetic, `lqv/finance/fx.py` conversions, or `lqv/site/terrain_dsl.py` `validate_geo()`. The BoQ arithmetic in particular is the only number Wesley sees — should have a unit test against a known-good golden file.

---

## 12. Concrete adoption roadmap

Sequenced by dependency + risk, scope-cut order pre-baked.

### Wave 1 — Pre-Step-8 (this sprint, until 2026-06-27 escritura)

Floor work that must not touch `build_scene.py`:

1. **#17 T1.6** — per-variant lighting (compositor grade — §7.4 + light groups §7.3 + AOVs §10.1). 2 days.
2. **GN scatter migration** for ferns + anthuriums + agave (not the frozen lapacho). §7.1. 2 days.
3. **NDVI sampler** + GN density attribute. §7.5. 1 day.
4. **Light Tree flag**. §7.2. 30 min.
5. **`lqv/lighting/` module** consolidation. §11. 1 day.

Total ~6.5 days, parallelisable to ~4 days with cap-4 sub-agents.

### Wave 2 — Step 8 (final composite re-render)

Unfreezes `build_scene.py` at `85e86aa + 1`:

6. **Particle system for lapacho petals** (replaces `scatter_lapacho_petals*`). §7.7. 1 day.
7. **Volumetric valley_mist** on Variant B. §7.8. Half day.
8. **Re-render all 18 finals** with new lighting + petals + mist. Overnight on GPU.

### Wave 3 — Post-escritura polish

9. **Mantaflow creek + cascade weir**. §7.6. 2-3 days.
10. **Adaptive Subdivision** on cob walls + river bed. §7.12. Half day per material.
11. **Asset Browser catalogues** for interactive Wesley sessions. §7.9. 1 day.
12. **Sapling Tree Gen** lapacho variants. §7.11. 1 day.
13. **OSL shaders** (red-laterite, tatakua soot, palm-thatch ageing). §7.10. 2 days.
14. **USD + glTF export**. §7.15. 1 day.
15. **Vertex-colour BoQ swatches**. §7.16. 1 day.

### Wave 4 — Nice-to-have

16. EEVEE Next preview path. §7.13. Half day.
17. Baked AO caches. §7.14. 1 day.
18. Multi-resolution sculpts on hobbit_house. §7.18. 2 days (hand work).
19. Proxy human figures. §7.19. 2 days.
20. Hydra/Karma swap test. §7.20. 2 days.

---

## 13. Hard constraints — what bounds every decision above

Non-negotiable, repeated for completeness so this doc stands alone:

- **License posture**: CC0 + CC-BY 4.0 ONLY. No CC-BY-SA, no CC-BY-NC. See `LICENSE_BUNDLE.md`.
- **Renderer byte-identity at `85e86aa`** preserved until Step 8. No `build_scene.py` edits this sprint.
- **Sub-render-first workflow** for every new asset (`feedback_sub_render_first`).
- **Subscene `clip_end = base.PARCEL_CLIP_END_M (= 20000.0)`** to avoid HDRI-only sub-renders (`feedback_subscene_clip_end`).
- **Sub-render output** under `renders/sub/runs/<RENDER_RUN_ID>_<asset>[_<tag>]/<variant>.png` mirrored to `latest/` (`feedback_render_run_folders`).
- **Don't touch `lqv/scatter_lapacho_petals*`** or hidden `WindowCut_*` cutters.
- **MCP socket dead** — Sketchfab path blocked; direct URL downloads only.
- **Never `git add -A`** / `git add .` — explicit staging only.
- **Never commit** unless user explicitly asks.
- **Conventional Commits** + `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`.
- **`python3`** not `python`.
- **Cap-4** subagent ceiling.
- **The 10 design rules** in `docs/MASTER_BRIEF.md` §14 inviolable — especially Rule 8: Paraguayan-first (no Tuscan / Bali / Earthship pastiche).
- **Preserve** `escritura_deck_v{1,2,3,4,5}.pdf`.
- **Currency**: USD primary, PYG @ 7,300 PYG/USD (see `docs/finance/fx.json`).

---

## 14. Summary — what changes if we adopt the whole list

If we land Waves 1-3 above:

- **Render times**: Wave 1 cuts amenity render times ~30% (Light Tree). Wave 2 mist + petals add ~15%. Wave 3 Mantaflow caches are pre-baked, so render-time-neutral once cached. Net: roughly the same total budget, much higher quality.
- **Output**: 18 finals re-rendered post-Step-8 with petals + mist + grade. USD + glTF exports for Wesley's phone. Asset Browser catalogue for interactive review. Vertex-colour BoQ swatches in `boq_rollup_v2.pdf`.
- **Code**: `lqv/lighting/` populated. `lqv/flora/gn_scatter.py` actually wired. `lqv/output/compositor.py` new. `lqv/materials/osl/` new with 3 OSL shaders. `lqv/site/ndvi_sampler.py` new. `tests/test_boq_arithmetic.py` new.
- **Scope creep risk**: high if all 20 items chase parallel. Mitigated by the wave order — Wave 1 hard-stops at escritura, then re-evaluate.

---

*End of audit. This document supersedes ad-hoc improvement plans `docs/IMPROVEMENT_PLAN_2026-06-13.md` and `docs/UPGRADE_PLAN.md` for the tooling/features dimension; those remain authoritative for project-mgmt scheduling.*
