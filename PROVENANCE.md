# Data Provenance — La Quebrada Viva

All upstream geospatial datasets used in the 62-ha digital twin and downstream renders. License + URL + retrieval date + SHA-256 per file. Bbox `W -57.045, S -25.645, E -57.015, N -25.615` (≈3.3 km × 3.3 km centered on parcel) unless noted.

Last verified: **2026-06-15** (T-12 to escritura).

---

## 1. ALOS World 3D 30 m (AW3D30) — canonical DEM

- **File**: `docs/site_data/alos_aw3d30_dem.tif` (Int16, EPSG:4326, 108×108 px)
- **Source**: JAXA, distributed via OpenTopography
- **URL**: https://portal.opentopography.org/raster?opentopoID=OTALOS.112016.4326.2
- **License**: **CC-BY 4.0** (JAXA Open Data, redistribution permitted with attribution)
- **Attribution**: "© JAXA — ALOS World 3D 30 m (AW3D30) v3.2, via OpenTopography"
- **Acquisition**: PRISM 2006–2011, v3.2 release 2023
- **Vertical accuracy**: ~5 m RMSE (best of the four DEMs cross-checked)
- **Retrieved**: 2026-06-10
- **SHA-256**: `56fdae2daa4a5f10b9040a7bd3b07647c177de058bdca8a27ca8e23799d06b3d`
- **Used by**: `scripts/make_terrain_heightmap.py` → `assets/terrain/escobar_height.png` (parcel displace), `lqv/subscene/terrain_62ha_photoreal.py` (T-DT)

## 2. Copernicus DEM 30 m (GLO-30, COP30) — A/B cross-check

- **File**: `docs/site_data/cop30_dem.tif` (Float32, EPSG:4326, 108×108 px)
- **Source**: ESA Copernicus Programme, distributed via OpenTopography
- **URL**: https://portal.opentopography.org/raster?opentopoID=OTSDEM.032021.4326.3
- **License**: **CC-BY 4.0** (Copernicus DEM 2019 license, free use with attribution)
- **Attribution**: "© ESA Copernicus DEM 2019 (GLO-30), via OpenTopography"
- **Acquisition**: 2018–2021 Sentinel-2 optical stereo composite
- **Vertical accuracy**: ~4 m flat, ~10 m forested/steep
- **Retrieved**: 2026-06-10
- **SHA-256**: `10e6459cd89319176ef8218c1f644e67dd38a38b7f603061b71f41c1604fed00`
- **Used by**: A/B comparison rendering via `LQV_DEM_SRC=docs/site_data/cop30_dem.tif LQV_DEM_TAG=cop30 python3 scripts/make_terrain_heightmap.py` → `assets/terrain/escobar_height_cop30.png`; render-time override `LQV_DEM_OVERRIDE_PNG`

## 3. Sentinel-2 L2A — surface reflectance / albedo / NDVI

- **Files**: `docs/site_data/sentinel2/S2B_21JVM_20260512_0_L2A_{blue,green,red,nir,swir16,scl}.tif` (UTM 21S, 10 m for visible/NIR, 20 m for SWIR/SCL) + `metadata.json` + `preview_rgb.png`
- **Tile**: 21JVM (MGRS), scene `S2B_21JVM_20260512_0_L2A`
- **Source**: ESA Copernicus / Sentinel Hub via Element-84 Earth-Search STAC
- **URL**: https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a (STAC); raw bands on `s3://sentinel-cogs/sentinel-s2-l2a-cogs/21/J/VM/2026/5/S2B_21JVM_20260512_0_L2A/`
- **License**: **CC-BY 4.0** (Copernicus Open Data, free use with attribution to "European Commission/ESA")
- **Attribution**: "Contains modified Copernicus Sentinel data 2026"
- **Acquisition**: 2026-05-12 13:51 UTC, cloud cover 1.8 % over tile
- **Scene bbox** (full tile, not cropped): W -58.002, S -26.308, E -56.902, N -25.313 — parcel sits inside
- **Retrieved**: 2026-06-10
- **SHA-256 (red band, representative)**: `87a3c3e0fa1117a9a9a1e5e7fdb5365e090ccb57e2362fd5b94536673fe17c68`
- **Files NOT committed**: `.tif` band rasters are gitignored (200 MB each); the STAC `metadata.json` + `preview_rgb.png` are committed as the citable proxy
- **Used by**: `lqv/flora/ndvi_density.py` (NDVI from `(nir-red)/(nir+red)` → scatter density gate), albedo overlay in T-DT

### 3a. Satellite-overlay A/B/C visual cross-check (rendered 2026-06-18)

Three-variant sub-render holding the canonical ALOS DEM constant and swapping only the satellite-derived albedo layer, so the citation in §3 lands on a renderable artifact (not just a band raster). Same camera, same lighting, same procedural PBR base; the only varying knob is the satellite multiply.

- **Variants** (via `LQV_ALBEDO_*` env hooks in `lqv/subscene/terrain_62ha_photoreal.py`):
  - `bare` — `LQV_ALBEDO_DISABLE=1`, no satellite overlay (procedural base only)
  - `s2rgb` — default, Sentinel-2 L2A surface-reflectance RGB × 0.55 `MIX_RGB` MULTIPLY
  - `ndvi` — `LQV_ALBEDO_OVERRIDE_PNG=assets/terrain/escobar_ndvi.png` (NDVI false-colour, green = dense canopy) × 0.55 MULTIPLY
- **Orchestrator**: `scripts/render_satellite_overlay_ab.py` (run_id `satellite_overlay_ab_20260618`, 3 × oblique preview @ 1280×720, Cycles CPU 32 samples, serialized per [[feedback-render-parallelism]]; `LQV_ALLOW_CPU_FALLBACK=1` default since the host has no GPU compute backend). Observed wall clock ~49 s / variant, ~4.3 GB RSS / process.
- **Composer**: `scripts/contact_sheet_satellite_overlay_ab.py` — single-row 3-panel sheet, DEM stats caption pulled from canonical `assets/terrain/escobar_height.json`.

Cross-check artifacts:

- `docs/site_data/satellite_overlay_ab_contact.png` — 3-panel oblique-render contact sheet (~368 KB, **CC-BY 4.0**). SHA-256 `3c70b8f19998463225c00ce3ad65b9887b265ef15e87ec575576ce96a341cfc2`. Sidecar `docs/site_data/satellite_overlay_ab_contact.png.meta.json` carries `render_run_id`, `overlay_modes`, `sentinel2_tile`, `dem_source_sha256` + `render_config` block.
- Per-variant oblique renders under `renders/sub/runs/satellite_overlay_ab_20260618_terrain_62ha_photoreal_oblique_{bare,s2rgb,ndvi}/A.png` (gitignored — derived, re-rendered from canonical bands + heightmap on demand).
- DEM held fixed at ALOS AW3D30 sha256 `56fdae2daa4a5f10b9040a7bd3b07647c177de058bdca8a27ca8e23799d06b3d` across all three panels (single varying axis: the satellite albedo). Reads as "same DEM, same camera, same lighting; the only knob turned is the satellite-derived colour."

## 4. GEDI L2A v002 — canopy height / ground elevation

- **Files**: `docs/site_data/gedi_l2a_points.csv` (475 raw shots, 27 granules 2019-2025) + `gedi_l2a_points_clean.csv` (25 cleaned)
- **Source**: NASA LP DAAC, GEDI L2A v002 product
- **URL**: https://lpdaac.usgs.gov/products/gedi02_av002/ (product page); granules via NASA Earthdata Search (https://search.earthdata.nasa.gov/search?fpj=GEDI)
- **License**: **Public domain** (NASA / USGS data, no copyright restrictions) — citable as NASA recommendation
- **Citation**: "Dubayah, R., et al. (2021). GEDI L2A Elevation and Height Metrics Data Global Footprint Level V002. NASA EOSDIS LP DAAC. https://doi.org/10.5067/GEDI/GEDI02_A.002"
- **Acquisition**: 2019–2025 spaceborne LiDAR, 25 m footprints, ~60 m along-track
- **Cleaning**: elev outlier filter 100–500 m AMSL → 25 valid shots; canopy column `canopy_height_m_final` filtered to [10, 40] m window (drops sensor-saturation reads at ~80 m)
- **Retrieved**: 2026-06-10
- **SHA-256 (clean)**: `1b6e705dcd79ade8060b0836fbd26df2d70c4081d9352ae277dc1e55b2909dfc`
- **Used by**: `lqv/flora/gedi_canopy.py` → per-tree scale ratio `clamp(h/25, 0.6, 1.6)`; applied in scatter routines

## 5. OpenStreetMap — Quebrada hydrography + roads + POIs

- **Files**: `docs/site_data/osm/{roads,buildings,pois,water,places}.geojson` + `osm_summary.txt`
- **Source**: OpenStreetMap contributors via Overpass API
- **URL**: https://overpass-api.de/api/interpreter (Overpass QL queries)
- **License**: **ODbL 1.0** (Open Database License) — share-alike on derived databases; rendered tiles/maps are CC-BY-SA-compatible. ⚠️ **Note**: ODbL is *not* CC0/CC-BY 4.0. We only use OSM as positional reference for the Quebrada channel centerline (single derived line), not as a redistributed database, so we stay outside the share-alike trigger. **Do not bundle the raw `.geojson` files into licensed deliverables to Wesley** — extract the channel polyline as a numpy array and re-license the derived geometry as project IP.
- **Attribution**: "© OpenStreetMap contributors, ODbL 1.0"
- **Retrieved**: 2026-06-10 (Overpass query window flagged 0 features for all five layers — empty bbox for OSM at this site; positional Quebrada centerline was hand-traced from Sentinel-2 RGB instead, see `lqv/site/terrain_dsl.py` `_incise_channel`)
- **SHA-256 (water)**: `9ecdafe2ce4c617b6be7420a06e6918223f34a6f429bfe957ee733c49d03be4d`
- **Used by**: positional cross-check only; the rendered creek geometry is procedural

## 6. Cross-validation DEMs (4-way A/B/C/D cross-check rendered 2026-06-18)

- `docs/site_data/srtm_gl1_dem.tif` — SRTM v3 GL1 (NASA, public domain), SHA-256 `a1560be58498b610c21b31b48d6caea400a5e2b628922f1b28b84849ffa1380c`
- `docs/site_data/nasadem_dem.tif` — NASADEM (NASA, public domain)

Both retrieved 2026-06-10 from OpenTopography in the same batch as AW3D30/COP30. All four were baked to `assets/terrain/escobar_height{,_cop30,_srtm,_nasadem}.png` via `scripts/make_terrain_heightmap.py` (16-bit normalized PNG + JSON sidecar) and rendered through the canonical 62-ha photoreal sub-renderer (`lqv/subscene/terrain_62ha_photoreal.py`) via the `LQV_DEM_OVERRIDE_PNG` / `LQV_DEM_OVERRIDE_JSON` env hooks. Orchestrator: `scripts/render_dem_ab.py` (run_id `dem_ab_20260618`, 4 × oblique preview @ 1280×720, Cycles CPU 32 samples, serialized per [[feedback-render-parallelism]]).

Cross-check artifacts:

- `docs/site_data/dem_ab_oblique_contact.png` — 4-panel oblique-render contact sheet (1088×900, ~537 KB, **CC-BY 4.0**), composed by `scripts/contact_sheet_dem_ab_oblique.py` from the 4 per-DEM oblique renders + their JSON sidecars. SHA-256 `a9803f383c84202a85c46d635df3ffdd7895ef517b162f93a9f0eaa0478f15b8`.
- `docs/site_data/dem_ab_contact.png` — 4-panel heightmap-PNG contact sheet (companion, encodes-only check).
- Per-DEM oblique renders under `renders/sub/runs/dem_ab_20260618_terrain_62ha_photoreal_oblique_{alos,cop30,srtm,nasadem}/A.png` (gitignored — derived, re-rendered from canonical heightmaps on demand).

Observed agreement (62-ha cropped window, derived from the four `assets/terrain/escobar_height*.json` sidecars):

| DEM     | min (m) | max (m) | mean (m) | sha256 (head) |
|---------|---------|---------|----------|---------------|
| ALOS    | 128.0   | 171.0   | 139.6    | `56fdae2daa4a5f10…` |
| COP30   | 125.1   | 163.0   | 138.1    | `10e6459cd8931917…` |
| SRTM    | 127.0   | 160.0   | 141.0    | `a1560be58498b610…` |
| NASADEM | 125.0   | 157.0   | 138.4    | `96daebbe1bce032f…` |

Spreads: **mean elevation within 2.9 m** across all four sensors (138.1 – 141.0 m AMSL); **min-elevation within 3.0 m**; **peak-elevation spread 14.0 m** between ALOS (171.0 m, optical stereo reads canopy tops) and NASADEM (157.0 m, modern void-filled SRTM reads ground) — consistent with each sensor's published RMSE and the known canopy-vs-ground sensor split. The oblique-render contact sheet confirms this stats-level agreement is also **visually indistinguishable** to a notary inspecting the displaced + SUBSURF + lit mesh: the choice of DEM does not change the rendered parcel appearance under our camera framing and lighting.

---

## License gate

Project deliverables to Wesley van de Camp are licensed **CC0** (procedural code, derived geometry) or **CC-BY 4.0** (renders, BoQ, docs). No CC-BY-SA, no CC-BY-NC. The OSM ODbL share-alike risk is contained per §5 above.

## Retrieval reproducibility

Re-pull commands and the OpenTopography API key live in `docs/site_data/CAPABILITY_ANALYSIS.md` and `docs/site_data/DEM_TOOLING_RESEARCH.md`. All bboxes and granule IDs in this file are sufficient to re-fetch the exact same data byte-for-byte from upstream as of 2026-06-15.
