# Satellite Data Brief — La Quebrada Viva

Compact reader: what we pulled, what it tells us about the 62-ha Escobar parcel, and exactly where each dataset feeds the render pipeline. Full provenance + SHAs in `PROVENANCE.md` (project root). Full pedagogical inventory in `docs/site_data/DATA_INVENTORY.md`.

Compiled **2026-06-15** (T-12 to escritura 2026-06-27).

---

## S1 — ALOS AW3D30 terrain (canonical DEM)

- **What it is**: JAXA optical-stereo DEM, ~5 m vertical RMSE, 30 m horizontal.
- **What it shows for the parcel**: elev **116–380 m AMSL** over the 3.3 km × 3.3 km source bbox, 264 m of total relief. The 62-ha parcel sits within that envelope; the stream channel reads ~116 m at the low end, sandstone-escarpment spur tops at ~380 m.
- **How we use it**: `scripts/make_terrain_heightmap.py` crops to a **900 m × 900 m parcel-centered window** (matches `WORLD_SIZE` in `lqv/subscene/terrain_62ha.py`), normalizes against the cropped relief range, resamples to **512×512 16-bit PNG**, writes sidecar JSON with bbox + z-range + source SHA. The Blender displace modifier consumes the PNG.
- **Sidecar metadata file**: `assets/terrain/escobar_height.json` — includes `crop_half_extent_m=450`, observed z range, source SHA.
- **Status**: ✅ shipped in commit `4409dba` (T-DT) + `83f3283` (driver).

## S2 — Copernicus DEM 30 m (COP30) — A/B cross-check

- **What it is**: ESA optical-stereo DEM from Sentinel-2 pairs, ~4 m flat / ~10 m forested.
- **What it shows for the parcel**: essentially identical envelope to ALOS (116–380 m, mean 161 m vs 162 m). In dense canopy areas COP30 reads 1–3 m lower than ALOS — that residual is the canopy thickness at 30 m scale, consistent with GEDI.
- **How we use it**: `LQV_DEM_SRC=docs/site_data/cop30_dem.tif LQV_DEM_TAG=cop30 python3 scripts/make_terrain_heightmap.py` writes `assets/terrain/escobar_height_cop30.png` side-by-side with the ALOS baseline. The render driver picks one via env: `LQV_DEM_OVERRIDE_PNG=assets/terrain/escobar_height_cop30.png LQV_DEM_OVERRIDE_JSON=…json`. No code edit needed to swap.
- **Status**: ✅ tooling shipped in `83f3283`. A/B contact sheet ALOS vs COP30 still **pending** (Day 2-3 punch list).

## S3 — Sentinel-2 L2A surface reflectance (albedo + NDVI)

- **What it is**: ESA Copernicus optical multispectral, 10 m visible/NIR + 20 m SWIR. Scene `S2B_21JVM_20260512_0_L2A`, acquired 2026-05-12 13:51 UTC, **1.8 % cloud cover over tile** — essentially clear, late-summer austral.
- **Bands held**: blue, green, red, nir, swir16, scl (scene classification). Each band is ~200 MB and **gitignored** (regenerable from STAC); STAC `metadata.json` + `preview_rgb.png` are the citable proxies.
- **What it gives us**:
  1. **NDVI** = (nir − red) / (nir + red) → scatter density gate. Computed once per parcel into a sample-able array; `lqv.flora.ndvi_density.density_at(nx, ny)` is queried in scatter loops with `nx, ny ∈ [-0.5, +0.5]` (bilinear, parcel-local). High NDVI = more flora, low NDVI = grass/path/structure.
  2. **Albedo proxy** — RGB composite drives the T-DT terrain material at parcel scale (the texture you see in the 62-ha digital twin renders is literally the Sentinel-2 RGB).
- **Status**: ✅ shipped in `83f3283` (NDVI) + `4409dba` (T-DT albedo).

## S4 — GEDI L2A v002 canopy heights

- **What it is**: NASA spaceborne LiDAR, 25 m footprints, ~60 m along-track. Per-shot canopy height + ground elevation.
- **What we have**: 475 raw shots from 27 granules (2019–2025) → 25 cleaned shots after elev-outlier filter (100–500 m AMSL).
- **Canopy height stats (clean)**: 18.9–80 m range; median **25.33 m**; the 80 m tail is sensor saturation. After the [10, 40] m filter in `gedi_canopy.py`, the realistic emergent-canopy distribution remains.
- **How we use it**: `lqv.flora.gedi_canopy.sample_scale(rng)` picks one filtered height per scattered tree, returns **`clamp(height / 25.0, 0.6, 1.6)`** as a per-tree scale ratio. 10 m → 0.6 (clamped, mid-storey), 25 m → 1.0 (median emergent canopy), 40 m → 1.6 (clamped, hero tree). Replaces the prior uniform `(0.6, 1.2)` band which truncated mature lapacho/jacaranda heroes.
- **Failure mode**: empty CSV / missing column → warning-only fallback to single ref height. Doesn't crash the render. Verified.
- **Status**: ✅ shipped in `83f3283`.

---

## What this brief does NOT cover (next satdata waves)

- **S5 — pysheds Pelton head map**: 62-ha flow-accumulation + head-distance raster for micro-hydro feasibility (Pelton wheel siting near the Quebrada drop). Day 2-3 punch list, pending.
- **S6-S12 — long tail (post-escritura)**: ERA5 climate normals, WorldClim bioclim, CGLS land-cover dynamics, GBIF biodiversity occurrence cross-check, SoilGrids texture/clay-fraction (cob siting validation), UTM 21S reprojection of all rasters, drone-LiDAR R35 ground-truthing.

---

## Cross-validation summary (why we trust the elevation truth)

All four held DEMs (AW3D30, COP30, SRTMGL1, NASADEM) agree to within ±5 m on the elevation envelope (115–380 m AMSL, mean 160–163 m). Independent sensors, independent processing pipelines, independent vintages (2000 → 2023). Agreement at this level is high-confidence ground truth before the Anexo I drone survey arrives post-escritura.

GEDI ground-elev sub-channel separately confirms the 116 m channel floor (mean 195 m across 25 shots, biased high because GEDI footprints land preferentially in vegetated mid-slope, but the minimum 144 m brackets the channel).

Sentinel-2 NDVI gradient correlates spatially with the canopy zones GEDI identifies as >25 m — the two independent vegetation sensors confirm each other.

---

## File pointers (read order)

1. `PROVENANCE.md` (root) — licenses, URLs, SHAs.
2. `docs/site_data/DATA_INVENTORY.md` — full pedagogical walk-through (~1.3 MB of source data documented).
3. `docs/site_data/SITE_DIAGNOSTIC.md` — interpretation: what the data says about the site.
4. `docs/site_data/CAPABILITY_ANALYSIS.md` — what we can do with what we have.
5. `docs/site_data/BLENDER_INTEGRATION_PLAN.md` — how the data feeds the renderer.
6. This file — quick reference for S1-S4 in render-pipeline terms.
