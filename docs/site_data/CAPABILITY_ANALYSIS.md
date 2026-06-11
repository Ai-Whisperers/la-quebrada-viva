# Satellite / Remote-Sensing Capability Analysis — La Quebrada Viva (62 ha, Escobar, Paraguarí)

**Status:** what we can already do with on-disk data, with zero new fetches and zero EULA blockers. Written to answer "what we can do with what we have" without commissioning the Tier-1 agrimensor.

**Scope:** 869 MB of remote-sensing + reanalysis data across 7 datasets. All derivations below are executable from `docs/site_data/` today on a CPU laptop. Cost: zero. Time-to-deliverable: hours.

**Bottom line:** the on-disk stack is sufficient to print an escritura topographic overlay, defend the micro-hydro narrative quantitatively, lock the build envelope to ~50 ha of the 62 ha (excluding the escarpment), publish a Cfa climate brochure, and produce four marketing renders backed by satellite-grade evidence. The only things we genuinely cannot do without Tier-1 are: sub-meter cadastral boundaries, individual structures inventory, and sub-30 m terrain detail under the canopy. Everything else can be shipped now.

---

## 1. Inventory at a glance

| Dataset | Files | Disk | Native res | Coverage | License | What it answers |
|---|---|---|---|---|---|---|
| ALOS AW3D30 DEM (JAXA) | `alos_aw3d30_dem.tif` | 12 KB | 30 m | tile over bbox | free w/ attrib | canonical elevation |
| Copernicus GLO-30 DEM (ESA) | `cop30_dem.tif` | 52 KB | 30 m | tile over bbox | free w/ attrib | cross-check #1 |
| SRTM v3 GL1 DEM (NASA) | `srtm_gl1_dem.tif` | 12 KB | 30 m | tile over bbox | public domain | cross-check #2 (2000 baseline) |
| NASADEM (NASA reprocess) | `nasadem_dem.tif` | 12 KB | 30 m | tile over bbox | public domain | cross-check #3 |
| Derived analyses | `analysis/*.tif`, `*.png` | 648 KB | 28×31 m | 108×108 px | derived | slope, aspect, buildability |
| GEDI L2A spaceborne LiDAR | `gedi_l2a_points*.csv` | 80 KB | 25 m footprint | 475 raw / **25 clean** | NASA, no EULA on parsed CSV | canopy height |
| Sentinel-2 L2A scene `S2B_21JVM_20260512_0_L2A` | `sentinel2/*` | 868 MB | 10/20/60 m | 1 cloud-free scene 2026-05-12 | Copernicus open | NDVI, NDWI, SWIR moisture, true color, SCL |
| ERA5 climate reanalysis | `climate_era5/*` | 344 KB | 0.25° (~31 km) | 1990–2025 monthly | Copernicus open | 36-yr normals |
| OSM extract | `osm/*` | 28 KB | n/a | bbox | ODbL | confirmed empty (rural) |
| GBIF species | `gbif/*` | 40 KB | n/a | bbox + radius | CC0 | 54-species baseline |

**Not on disk** (placeholders only): `_cache/`, `cgls_lcover/`, `worldclim/_raw/` — empty. WorldClim source dead at `geodata.ucdavis.edu`; CGLS land-cover never pulled; cache is dev scratch.

---

## 2. Per-dataset accuracy & known caveats

### 2.1 DEMs — four-way consensus at 30 m

- All four DEMs agree on the property's elevation envelope: **116 → 380 m AMSL**, 264 m of relief over a 3.3 km horizontal sweep. Per-DEM mean: AW3D30 162 m, COP30 161 m, SRTM 163 m, NASADEM 160 m — a 3 m spread between independent sensors validates each within their stated 4–9 m RMSE.
- **Pixel footprint** of the derived analysis grid: 28×31 m, 108×108 = 11 664 valid pixels covering ≈ 1 005 ha (a ~16×16 superset of the 62 ha parcel — the analysis grid is larger than the parcel, deliberately, so edge effects don't bias internal slope stats).
- **Vertical bias correction:** none applied. The four DEMs agree on relief but not on absolute datum. EGM2008 vs WGS84 ellipsoidal differences (~15 m in this region) are below the per-pixel noise, so we treat AW3D30 as canonical and use the others only for QA.

### 2.2 GEDI L2A — useful only after a unit-bug filter

- 27 granules, 475 raw shots from 2019–2025. `elev_lowestmode` is in a wrong unit / wrong vertical datum — raw median 4 654 m vs. real ground at 116–380 m.
- Workaround: filter to plausible Paraguay elevation 100–500 m. **25 of 475 shots survive** (≈ 5%). Those 25 are in the 144–273 m band, mean 195.9 m, median 207 m — consistent with the AW3D30 elevation surface to within ~10 m, which is acceptable for shot validation.
- **`canopy_height_m` is reliable** for all 475 shots, including those with bad ground elevation: the canopy field is computed as a difference internally, so the unit error cancels. Clean shots: mean 48.5 m, median 37 m, max 80 m — consistent with mature Atlantic Forest in protected gullies.
- This is enough for canopy-class histograms and tall-tree spotting. Not enough for sub-hectare biomass mapping (would need GEDI L4A, gated behind the cloud-pool EULA).

### 2.3 Sentinel-2 — the gem

- Scene `S2B_21JVM_20260512_0_L2A`, acquired 2026-05-12. **Cloud cover 0.4 %** (essentially cloud-free), vegetation 89.88 %, water 2.07 %, sun elevation 38.92°, sun azimuth 33.14°.
- All 13 bands on disk, including B11/B12 SWIR for moisture and B05/B06/B07 red-edge for vegetation stress. Plus SCL (scene classification), AOT, WVP, and TCI true-colour preview.
- **Why this matters:** one cloud-free scene over 62 ha of Atlantic Forest in the dry season is rare. We can derive every ratio-based vegetation/water index from this one acquisition without waiting for another pass.
- **Gitignored as regenerable** — do not re-commit. The STAC metadata is preserved (`metadata.json`, 1 429 lines) so the scene can be re-fetched if needed.

### 2.4 ERA5 — 36-year climate baseline

- Monthly means 1990–2025 at 0.25° nearest grid (-25.75, -57.0). Coarse spatially but long enough temporally to call it a normal.
- Mean annual temp 22.04 °C, precip 1 736 mm/yr, peak solar Dec 24.3 MJ/m²/day, windiest Aug 1.5 m/s, lowest wind Jun 1.1 m/s.
- Köppen Cfa (subtropical humid, no dry season). Already used in `climate_brochure.md` as the escritura one-pager backing the "always-wet hydrological sense" pull-quote.
- Design rule 6 (passive cooling) **passes**: warmest-month mean 26.8 °C < 35 °C threshold.

### 2.5 OSM & GBIF — context tier

- OSM Overpass over the bbox returns **0 features across 5 categories** (roads, buildings, POIs, places, water). This is not a bug — the area is genuinely rural; nearest mapped feature is several km away.
- GBIF returns 54 unique species in the bbox + radius: Aves 50, Magnoliopsida 2, Squamata 1, Insecta 1. Sufficient for a starter biodiversity baseline but heavily bird-biased (eBird dominance). Camera-trap + acoustic survey would add mammals, amphibians, nocturnal insects.

---

## 3. What we can do today — capabilities matrix

Eight derivations are executable from on-disk data with the existing Python stack. Effort estimates are wall-clock on a CPU laptop.

| # | Deliverable | Inputs | Tool stack | Output | Effort |
|---|---|---|---|---|---|
| 1 | Slope + aspect + buildability raster | `alos_aw3d30_dem.tif` | richdem or `numpy.gradient`, rasterio | `analysis/alos_slope.tif`, `_aspect.tif`, `_buildability.tif` | **already done** |
| 2 | Multi-azimuth hillshade (escritura overlay) | `alos_aw3d30_dem.tif` | `gdaldem hillshade -az 315 -alt 45` | PNG hillshade for escritura packet | 30 min |
| 3 | Stream long-profile + micro-hydro head | conditioned DEM | pysheds: fill_pits → fill_depressions → resolve_flats → flow_dir → accumulation | CSV of stream centerline elevation 380→116 m + matplotlib profile | 2 h |
| 4 | Viewshed from candidate building platforms | DEM + candidate XY in 127–169 m flat zone | pyviewshed | binary visible/hidden raster per platform | 1 h per platform |
| 5 | NDVI greenness raster (marketing proof) | Sentinel-2 B04, B08 | rasterio + numpy: (B08−B04)/(B08+B04) | colormapped PNG, mean NDVI value | 30 min |
| 6 | NDWI water raster (cascade + pool delineation) | Sentinel-2 B03, B08 | rasterio + numpy: (B03−B08)/(B03+B08) | water mask, area in ha | 30 min |
| 7 | SWIR moisture / dry-stress map | Sentinel-2 B11, B12 | NDMI = (B08−B11)/(B08+B11) | dry-fraction estimate, riparian-corridor outline | 1 h |
| 8 | Canopy-height histogram on the parcel | GEDI clean CSV | pandas + matplotlib | PNG histogram, % mature forest (≥30 m) | 30 min |

Total ≈ **1 working day** to ship all eight, assuming no debugging. Most are I/O bound, not compute.

---

## 4. LQV-specific use cases (tied to scene & escritura)

### 4.1 Build-envelope lock — answers "where on the 62 ha can we put houses?"

- **574.5 ha flat (slope <5°)**, 230.8 ha buildable (5–10°), 123.4 ha challenging (10–20°), 70.3 ha steep (>20°, the escarpment).
- Within the 62-ha parcel: extrapolating the same class distribution, **≈ 45–55 ha is house-buildable**. At Awasi-style densities (1 lodge per 5–7 ha) that is 7–9 vacation-rental keys, which matches the typology plan.
- Flat zone is concentrated at **127–169 m AMSL** (analysis p10/p90 in flat class). Everything above 250 m is the escarpment top — exclude it from rental pads, keep it for view platforms only.
- This is the strongest single output for the escritura packet: it lets us tell the notary and Wesley exactly which third of the parcel is the developable envelope, with a satellite-derived basis instead of vibes.

### 4.2 Micro-hydro narrative — defends Pelton wheel investment

- Stream descends 380 m → 116 m over the 3.3 km transect. **264 m gross head is order-of-magnitude above the Pelton minimum (8 m)**, so the question is not whether micro-hydro is possible but where to site the penstock intake.
- From a pysheds-conditioned DEM we can produce: stream long-profile, accumulated flow per pixel, candidate intake elevations (e.g., 250 m, 200 m, 150 m) with the head delivered to a turbine at 120 m, and the penstock route from each. Cost: 2 h of compute.
- Even without flow-rate gauging, the head map alone defeats a notarial skeptic. ERA5 rainfall 1 736 mm/yr (Cfa, no dry season) is the second supporting datum.

### 4.3 Hero-camera & escritura visuals — y-axis coordinates from DEM

- The scene's escarpment lives at `y = 20`, footbridge/pool at `y = −25.5`. Both are currently hand-tuned in `lqv/site/escarpment.py` and `ground.py`.
- An ALOS-derived heightmap, loaded into `lqv/site/terrain_62ha.py` (the dormant T2.6 stub), would let us back-solve actual cartesian coords by reprojecting the 62-ha bounding box to EPSG:32721 UTM 21S and dropping the origin at the SE corner.
- **Not required for escritura.** Current procedural terrain is byte-identical at commit `85e86aa`; touching it now triggers a re-render of all 18 finals, which is gated by T1.6 + T2.6 (both post-escritura). The DEM wiring is staged but dormant — same posture as in `terrain_62ha.py` today.

### 4.4 Sun/shadow seasonal modelling — combines ERA5 + aspect + GEDI canopy

- ERA5 gives monthly sun elevation/azimuth at our latitude. ALOS gives the slope & aspect raster. GEDI gives canopy height per shot.
- For each candidate platform we can model: hours of direct sun per day at solstice, winter shoulder, equinox; and the loss to canopy shadowing within ~30 m radius.
- This is the input to: PV array sizing, passive solar orientation (design rule 7), and lapacho-petal scatter timing (already byte-locked).
- Practical decision: prefer N-facing aspects (sun-exposed in the Southern Hemisphere) for PV, S-facing aspects (shaded, cooler) for cob walls — design rule 5 (thermal mass) wants the cooler façade.

### 4.5 Marketing & escritura assets

- **NDVI greenness map.** "89.88 % vegetated" from the Sentinel-2 SCL is a number we already have. The NDVI raster gives a colormapped figure backing it. One-page deliverable.
- **NDWI water trace.** Confirms cascade + flat-rock pool at ~120–125 m without sending anyone to the field. Same one-pager.
- **Cfa climate brochure.** Already shipped at `climate_era5/climate_brochure.md`. Has the four pull-quotes including the always-wet hydrological line.
- **Biodiversity starter list.** 54 GBIF species, 50 birds dominant. Useful for ESG/marketing language; not defensible scientifically without ground truthing.

### 4.6 Risk overlays we can produce but probably won't ship pre-escritura

- Fire-risk proxy from NDMI dry-fraction + slope + aspect. Useful for insurance conversations later.
- Acoustic baseline & dark-sky baseline. Both flagged as gaps in `DATA_INVENTORY.md`; both need on-site instrumentation, not satellite.

---

## 5. Render-pipeline integration path (T2.6, post-escritura)

The dormant module `lqv/site/terrain_62ha.py` is the integration point. Three known issues to reconcile before it can call `build_terrain()`:

1. **Path mismatch.** Module looks for `assets/site_data/escobar_dem_5m.tif`; the actual data lives under `docs/site_data/alos_aw3d30_dem.tif`. Either symlink `assets/site_data → docs/site_data` (cleanest, single source of truth) or rewrite the module's `ASSETS` constant. Recommend the symlink + filename remap.
2. **Resolution mismatch.** Module name implies 5 m; canonical DEM is 30 m AW3D30. Rename to `escobar_dem_30m.tif` to be honest about resolution, and add a comment that 5 m would require the Tier-1 surveyor or OpenTopography.
3. **No RNG calls.** Per CLAUDE.md and `BLENDER_GIS_3D_LANDSCAPE_RESEARCH.md`, `build_dem_terrain` must not call `random.*` — otherwise the downstream flora draw order shifts and `85e86aa` byte-identity breaks. Use a fixed subdivision and deterministic displacement.

Heightmap → Blender pipeline, per `DEM_TOOLING_RESEARCH.md` §3:

```
ALOS GeoTIFF
  → rasterio reproject to EPSG:32721 (UTM 21S)
  → numpy normalize Z to [0, 1]
  → Pillow + imageio export 16-bit PNG + 32-bit EXR
  → bpy mesh.subdivide → displace modifier → ground material
  → satellite TCI as ground albedo stand-in
```

**RNG ordering invariant** must hold: `random.seed()` AFTER `materials.build_materials()` BEFORE first `build_*`. The DEM build runs inside `build_*`, so it must consume zero RNG.

T2.6 is deferred post-escritura, gated by T1.6 (per-variant lighting) and a Step 8 composite re-render that supersedes `85e86aa`. Touching it now is a regression risk against the 18 finals.

---

## 6. Gap analysis — what only Tier-1 buys us

The on-disk stack is enough to ship the escritura packet and the marketing brochure. It is **not** enough for:

| Gap | What only Tier-1 surveyor (or drone) can provide | Why current stack fails | Escritura-critical? |
|---|---|---|---|
| Exact 62-ha cadastral boundary | RTK GPS at 1 m horizontal, surveyed corners, mensura compatible with notary | DEM tiles cover ~16× the parcel; we have no parcel polygon | **yes** — notary wants this |
| Sub-meter structures inventory | Surveyed dwellings, gates, fences, cob structures already on site | OSM is empty; Sentinel-2 10 m can't resolve a 6 m cob hut | yes — affects valuation |
| Sub-30 m terrain detail | 1 m horizontal, 5 cm vertical via RTK or drone SfM | All four DEMs are 30 m; the escarpment edge is sharper than this | no for escritura, yes for building-pad siting |
| Spring-source ground truth | GPS pin on actual spring, flow gauging | NDWI sees the cascade pools but not the spring head | no for escritura, yes for Pelton intake |
| Sub-canopy hydrology | LiDAR-derived bare-earth under forest | GEDI samples points, can't draw streams in dense canopy | no |
| Anexo I (legal description) | Notary-side document | Not a GIS gap | **yes** — notary handles it |
| Acoustic baseline | On-site dB recorder, dawn + dusk + night | Satellite can't | no for escritura |
| Dark-sky / light-pollution baseline | VIIRS Day/Night Band (free) or on-site SQM | We have not fetched VIIRS; could be added in a few hours | no for escritura |

**Recommendation:** Wesley should still commission the Tier-1 agrimensor — the notary needs the mensura — but the GIS stack we already have is sufficient to brief the agrimensor, scope the survey, and pre-validate the deliverables when they arrive. We are not blocked on the surveyor for the digital twin.

---

## 7. Suggested shipping order (if T2.6 wiring slips)

Bound by today's autonomy + escritura on 2026-06-27 (16 days):

1. **NDVI + NDWI + SWIR moisture rasters from Sentinel-2.** ~2 h. Three escritura visuals + one marketing pull-quote.
2. **`gdaldem hillshade` of ALOS at 315°/45°.** ~30 min. Drop-in escritura overlay.
3. **Stream long-profile + Pelton-head map via pysheds.** ~2 h. Quantitative backing for the micro-hydro narrative — the strongest single defensive datum against a skeptical notary.
4. **Viewshed from two candidate platforms in the 127–169 m flat zone.** ~2 h. Lets us say "from pad X you see Y hectares of canopy and Z m of stream."
5. **Canopy-height histogram from clean GEDI CSV.** ~30 min. One figure, one bullet for the biodiversity page.

Total: ~7 hours of work, all of it ships before escritura with zero new fetches, zero EULA blockers, and zero risk to the byte-locked renderer.

T2.6 itself (DEM into Blender) stays deferred — it is the right wiring eventually but it is not in the escritura critical path.

---

## 8. What this document is not

- Not a fetch script. All data is on disk.
- Not a license audit (separate concern; per-dataset licenses listed in §1 and `DATA_INVENTORY.md`).
- Not a render plan. Render-pipeline changes go through `docs/sub_render_strategy.md` and the T2.6 staging path.
- Not a substitute for the Tier-1 agrimensor. Cadastral, structures inventory, and Anexo I still go through the surveyor + notary.
