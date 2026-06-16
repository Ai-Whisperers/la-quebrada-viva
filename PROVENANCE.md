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

## 6. Cross-validation DEMs (held as reference, not used in render)

- `docs/site_data/srtm_gl1_dem.tif` — SRTM v3 GL1 (NASA, public domain)
- `docs/site_data/nasadem_dem.tif` — NASADEM (NASA, public domain)

Both retrieved 2026-06-10 from OpenTopography in the same batch as AW3D30/COP30. Used to confirm ±5 m elevation agreement across four independent sensors before locking AW3D30 as canonical.

---

## License gate

Project deliverables to Wesley van de Camp are licensed **CC0** (procedural code, derived geometry) or **CC-BY 4.0** (renders, BoQ, docs). No CC-BY-SA, no CC-BY-NC. The OSM ODbL share-alike risk is contained per §5 above.

## Retrieval reproducibility

Re-pull commands and the OpenTopography API key live in `docs/site_data/CAPABILITY_ANALYSIS.md` and `docs/site_data/DEM_TOOLING_RESEARCH.md`. All bboxes and granule IDs in this file are sufficient to re-fetch the exact same data byte-for-byte from upstream as of 2026-06-15.
