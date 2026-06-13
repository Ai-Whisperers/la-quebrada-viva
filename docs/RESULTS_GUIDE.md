# RESULTS_GUIDE — La Quebrada Viva visual index

This is the single page where you can see every render the project has produced. It is grouped by category, newest at top, with file paths so you can open any image directly.

Project: **62-ha Paraguay parcel, Escobar (Paraguarí dept.).** Render engine: Blender 4.2.3 LTS Cycles CPU. Color: AgX Punchy + OIDN denoise. Master seed `SEED=20260609`.

Variants `A / B / C` are the three lighting moods we ship for every scene:

| Variant | Mood | Exposure offset |
|---|---|---|
| A | Cooler / shadow-heavy | −0.2 EV |
| B | Neutral hero | +0.3 EV |
| C | Warmer / golden-hour | +0.6 EV |

---

## 1. Composite finals — 18 frames (`85e86aa`, byte-frozen)

These are the master beauty shots of the housing scheme. **18 frames = 6 cameras × 3 variants.** All under `renders/` at the repo root.

| Camera | Subject | A | B | C |
|---|---|---|---|---|
| `hero` | The full site reveal — escarpment, house, stream | `renders/A_hero.png` | `renders/B_hero.png` | `renders/C_hero.png` |
| `dusk` | Same composition at golden hour with window emission | `renders/A_dusk.png` | `renders/B_dusk.png` | `renders/C_dusk.png` |
| `cliff` | Looking out from the escarpment face toward the valley | `renders/A_cliff.png` | `renders/B_cliff.png` | `renders/C_cliff.png` |
| `stream_up` | Eye-level along the stream, footbridge framing | `renders/A_stream_up.png` | `renders/B_stream_up.png` | `renders/C_stream_up.png` |
| `terrace` | Cob house terrace approach with lapacho overhang | `renders/A_terrace.png` | `renders/B_terrace.png` | `renders/C_terrace.png` |
| `petal_macro` | Close-up of fallen lapacho petals on the ground | `renders/A_petal_macro.png` | `renders/B_petal_macro.png` | `renders/C_petal_macro.png` |

**What the geometry is made of:** The `_archive/build_scene.py.pre-refactor.bak` monolith builds the actual composite — it pulls from cob house components, site landscape (escarpment, stream, terraces), flora (lapacho, mango, pindo, tree fern, bamboo, agave, anthurium), and FX (canopy volume, fireflies, valley mist, window emission). All 14 typology / amenity modules (`adobe_courtyard`, `bamboo_pavilion`, `cob_bottle_lqv`, `rammed_earth_loft`, `shipping_container_eco`, `straw_bale_cottage`, `timber_tree_cabin`, `underground_dome`, `parking_arrival`, `equestrian_zone`, `pool_wellness`, `reception_shop`, `event_lawn`, `microhydro_centre`) are still forward declarations that `raise NotImplementedError` — they exist as shells under `lqv/typologies/` and `lqv/amenities/` waiting for extraction.

---

## 2. Digital twin terrain — photoreal (T-DT.10, in flight)

The 62-ha digital twin of the actual parcel, using ALOS-DEM elevation + Sentinel-2 albedo + Poly Haven CC0 assets (qwantani sunset HDRI, cracked red ground PBR, jacaranda trees, mossy rocks, hero boulders).

Driver: `lqv/subscene/terrain_62ha_photoreal.py`. Output: `renders/sub/runs/20260611_dt_run_photoreal_*/`.

| View | A | B | C |
|---|---|---|---|
| Birdseye (top-down survey) | `…_birdseye/A.png` | `…_birdseye/B.png` | `…_birdseye/C.png` |
| Plan (orthographic-style) | `…_plan/A.png` | `…_plan/B.png` | `…_plan/C.png` |
| Oblique (3/4 hero) | `…_oblique/A.png` | `…_oblique/B.png` | `…_oblique/C.png` |

Latest-mirror shortcuts: `renders/sub/latest/terrain_62ha_photoreal_{A,B,C}.png` (oblique view).

**What you're seeing:** Heightmap is real ALOS World 3D 30 m DEM for the parcel bounds. Surface PBR is `cracked_red_ground_4k` blended with `muddy_tracks_4k` keyed on stream proximity. Sentinel-2 albedo lays a tint layer on top so the spatial color signature matches what satellites actually saw. Trees: 70 jacaranda scatters with min spacing 22 m and stream-avoid radius 28 m. Rocks: 36 mossy rocks near the stream + 7 hero boulders at bends and the pool spot.

---

## 3. Digital twin terrain — earlier iterations (kept for history)

Per the "KEEP OLD IMAGES" rule, every previous attempt is preserved.

| Run | What was different | Folder |
|---|---|---|
| `20260611_dt_run` (v1) | Initial ALOS + Sentinel-2 albedo, no trees/rocks | `renders/sub/runs/20260611_dt_run_terrain_62ha_{birdseye,plan,oblique}/` |
| `20260611_dt_run_v2` | Added stream overlay + parcel boundary | `…_dt_run_v2_…` |
| `20260611_dt_run_v3_hd` | Higher-resolution parcel focus, less mountain backdrop | `…_dt_run_v3_hd_…` |
| `20260611_dt_run_v4_polish` | Color grade + arrow markers | `…_dt_run_v4_polish_…` |
| `20260611_dt_run_v5` | Stylized terrain redesign — got feedback that it "still looks bad" | `…_dt_run_v5_…` |
| `20260611_dt_run_v5_arrowfix` | Arrow placement patch | `…_dt_run_v5_arrowfix_…` |
| `20260611_dt_run_v5_smoke` | Smoke probe before photoreal pivot | `…_dt_run_v5_smoke_…` |
| `20260611_030400_…__legacy` | Earliest birdseye probe | `…_030400_terrain_62ha_birdseye__legacy/` |
| `smoke_test_20260611_…` | RNG/driver smoke | `…/smoke_test_20260611_terrain_62ha_birdseye/` |

v5 was the cartoon-style render that prompted the user to ask if we could "download assets instead of modeling" — that question triggered the T-DT.10 photoreal pivot above.

---

## 4. Gallery of real builders — 54 frames (`20260611_gallery_real`)

Multi-angle (front / side / top) renders of every asset module that actually has implemented geometry. **18 builders × 3 views = 54 frames** at 1280×720, 64 samples.

Output pattern: `renders/sub/runs/20260611_gallery_real_<asset>_<view>/B.png` (variant B = neutral hero).

### 4.1 Cob house stack
| Asset | What it is | front | side | top |
|---|---|---|---|---|
| `cob_walls` | Massive cob walls, monolithic | `…cob_walls_front/B.png` | `…cob_walls_side/B.png` | `…cob_walls_top/B.png` |
| `services` | Kitchen / bath bumps and pipes | `…services_front/B.png` | `…services_side/B.png` | `…services_top/B.png` |
| `tatakua` | Paraguayan clay oven dome | `…tatakua_front/B.png` | `…tatakua_side/B.png` | `…tatakua_top/B.png` |
| `bottle_wall` | Embedded glass bottle accent wall | `…bottle_wall_front/B.png` | `…bottle_wall_side/B.png` | `…bottle_wall_top/B.png` |

### 4.2 Site landscape
| Asset | What it is | front | side | top |
|---|---|---|---|---|
| `escarpment` | The cliff face that backs the parcel | `…escarpment_front/B.png` | `…escarpment_side/B.png` | `…escarpment_top/B.png` |
| `stream` | The water-line + bank geometry | `…stream_front/B.png` | `…stream_side/B.png` | `…stream_top/B.png` |
| `terraces` | Stepped landform below the house | `…terraces_front/B.png` | `…terraces_side/B.png` | `…terraces_top/B.png` |

### 4.3 Flora
| Asset | What it is | front | side | top |
|---|---|---|---|---|
| `lapacho_tree` | Tabebuia in flowering mode (pink) | `…lapacho_tree_front/B.png` | `…lapacho_tree_side/B.png` | `…lapacho_tree_top/B.png` |
| `mango` | Procedural mango tree | `…mango_front/B.png` | `…mango_side/B.png` | `…mango_top/B.png` |
| `pindo_palm` | Native Paraguayan palm | `…pindo_palm_front/B.png` | `…pindo_palm_side/B.png` | `…pindo_palm_top/B.png` |
| `tree_fern` | Tropical understory tree fern | `…tree_fern_front/B.png` | `…tree_fern_side/B.png` | `…tree_fern_top/B.png` |
| `bamboo_clump` | Mixed-height bamboo group | `…bamboo_clump_front/B.png` | `…bamboo_clump_side/B.png` | `…bamboo_clump_top/B.png` |
| `agave` | Spike-leaf succulent | `…agave_front/B.png` | `…agave_side/B.png` | `…agave_top/B.png` |
| `anthurium` | Epiphyte rosette (single sample) | `…anthurium_front/B.png` | `…anthurium_side/B.png` | `…anthurium_top/B.png` |

### 4.4 FX volumes
| Asset | What it is | front | side | top |
|---|---|---|---|---|
| `canopy_volume` | Soft volumetric haze under tree canopy | `…canopy_volume_front/B.png` | `…canopy_volume_side/B.png` | `…canopy_volume_top/B.png` |
| `fireflies` | 80 emissive point lights, variant-tinted | `…fireflies_front/B.png` | `…fireflies_side/B.png` | `…fireflies_top/B.png` |
| `valley_mist` | Low-elevation fog band along the stream | `…valley_mist_front/B.png` | `…valley_mist_side/B.png` | `…valley_mist_top/B.png` |
| `window_emission` | Warm cob-house interior emission @ dusk | `…window_emission_front/B.png` | `…window_emission_side/B.png` | `…window_emission_top/B.png` |

Each frame uses an isolated RNG (per-asset SHA-256[:4] derive on `SEED`), so seed jitter never propagates between assets. A neutral ground plane (laterite or grass per asset) is placed under most builders so they don't float in void. The escarpment, stream, and valley_mist frames run without ground because they generate their own.

---

## 5. How to read everything together

- **For the housing concept presentation**: open `renders/{A,B,C}_hero.png` for the master shot, then `…_dusk.png` for the same composition at golden hour, then `…_terrace.png`, `…_stream_up.png`, `…_cliff.png` as supporting angles. `…_petal_macro.png` is the texture macro.
- **For the parcel land-survey presentation**: open `renders/sub/latest/terrain_62ha_photoreal_{A,B,C}.png` for the most recent oblique hero, then `renders/sub/runs/20260611_dt_run_photoreal_terrain_62ha_photoreal_birdseye/{A,B,C}.png` for top-down, and `…_plan/{A,B,C}.png` for the ortho-plan style.
- **For module verification** (sanity-checking that geometry exists): open `renders/sub/runs/20260611_gallery_real_<asset>_<view>/B.png`.
- **For "how did we get here"**: the v1 → v5 terrain folders in §3 show every iteration; the cartoon-look v5 is what triggered the photoreal asset pivot.

## 6. Known gaps

- **14 typology + amenity modules are stubs.** `adobe_courtyard`, `bamboo_pavilion`, `cob_bottle_lqv`, `rammed_earth_loft`, `shipping_container_eco`, `straw_bale_cottage`, `timber_tree_cabin`, `underground_dome`, `parking_arrival`, `equestrian_zone`, `pool_wellness`, `reception_shop`, `event_lawn`, `microhydro_centre` all `raise NotImplementedError`. Geometry needs extraction from `_archive/build_scene.py.pre-refactor.bak`. They are not in the gallery because there is nothing to render.
- **Composite re-render with per-variant lighting** (Step 8 of `docs/sub_render_strategy.md` §10) is deferred until after the escritura.
- **MCP socket is dead.** Hyper3D-generated lapacho and mbocayá variants are blocked; manual asset import path (`bpy.data.libraries.load(link=False)`) is the workaround.
- **Variant coverage in the gallery.** This run captures variant B only. Re-run with `RENDER_VARIANT=A` and `RENDER_VARIANT=C` if A/C gallery coverage is needed; the folder layout already separates by view so the same paths accept A.png / C.png alongside the existing B.png.
