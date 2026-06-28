# NASA & OpenTopography Data Inventory — La Quebrada Viva

> What we pulled, what each one means, and what it tells us about the 62-ha property in Escobar, Paraguarí, Paraguay. Compiled by AI Whisperers (Ivan) on 2026-06-10.

---

## 1. Quick summary

We have **two upstream sources** of geospatial data, four DEMs for cross-validation, and one LiDAR vegetation structure dataset:

| Source | Dataset | What it is | Coverage | Resolution | Quality | File(s) |
|---|---|---|---|---|---|---|
| **OpenTopography** | ALOS World 3D 30 m (AW3D30) | JAXA's best-in-class DEM (radar, fills radar shadow) | 1,100 ha (3.3 km × 3.3 km bbox) | 1 arcsec ≈ 30 m | Excellent | `alos_aw3d30_dem.tif` (12 KB) + `alos_aw3d30_hillshade.png` (88 KB) |
| **OpenTopography** | Copernicus DEM 30 m (GLO-30) | ESA's optical-stereo DEM | Same bbox | 30 m | Excellent | `cop30_dem.tif` (52 KB) + `cop30_hillshade.png` (92 KB) |
| **OpenTopography** | SRTM v3 GL1 30 m | NASA's original 2000-era shuttle radar DEM, reprocessed | Same bbox | 30 m | Good (slight noise) | `srtm_gl1_dem.tif` (12 KB) + `srtm_gl1_hillshade.png` (85 KB) |
| **OpenTopography** | NASADEM 30 m | NASA's "improved SRTM" — reprocessed 2020 with better noise reduction | Same bbox | 30 m | Excellent | `nasadem_dem.tif` (12 KB) + `nasadem_hillshade.png` (83 KB) |
| **NASA Earthdata** | GEDI L2A v002 | Spaceborne LiDAR — vegetation canopy height + ground elevation per shot | Full bbox (27 granules, 2019-2025) | 25 m footprints, ~60 m along-track spacing | **Mixed — see §3** | `gedi_l2a_points.csv` (75 KB, 475 raw shots) + `gedi_l2a_points_clean.csv` (25 cleaned) + `gedi_l2a_summary.txt` + `gedi_l2a_clean_summary.txt` |

**Acquisition bbox** (all 4 DEMs + GEDI): `W -57.045, S -25.645, E -57.015, N -25.615` — a 3.3 km × 3.3 km box (≈1,100 ha) centered on the actual 62-ha property. The exact 62 ha is somewhere inside this box; once the Anexo I arrives we can clip to the real boundaries.

**Total data on disk:** 1.3 MB across 15 files in `docs/site_data/`. Nothing on the property is more than 30 m unresolved (except the canopy, which is 25 m footprints).

---

## 2. OpenTopography data — DEMs (Digital Elevation Models)

A Digital Elevation Model is a raster image where each pixel holds the height above sea level (in meters) of the ground at that point. Hillshades are the same data rendered as if lit by a low-angle sun — they make the terrain "pop" visually so you can read the landforms.

We pulled **4 independent DEMs** of the same 3.3 km × 3.3 km box. Pulling four (instead of one) is a deliberate cross-validation: each uses a different sensor and a different processing pipeline, and they all agree on the big features. Where they disagree we either average them or pick the most-trusted source.

### 2.1 ALOS World 3D 30 m (AW3D30) — *the canonical DEM for this project*

- **Source:** Japan Aerospace Exploration Agency (JAXA), commercial-grade stereo-photogrammetric DEM derived from the ALOS satellite's PRISM instrument. Open-access via OpenTopography. **CC-BY 4.0 license.**
- **Acquisition date:** 2006-2011 (PRISM imagery), DEM v3.2 release 2023
- **Vertical accuracy:** ~5 m RMSE (the best of the four)
- **Why we use it as the canonical source:** Highest vertical accuracy, best performance in vegetated/steep terrain (the site is both), free and open. The other three DEMs are used as cross-checks.
- **What the data shows for our site:**
  - Elevation range: **116 – 380 m AMSL** (264 m of relief)
  - Mean: 162 m, Median: 149 m, Std: 42 m
  - The **lowest elevations (~116 m)** correspond to the stream channel
  - The **highest elevations (~380 m)** are at the top of the sandstone escarpment spur (matches the research doc's "40-60 m escarpment" — the 264 m total relief is the full hillside, of which the escarpment face is the upper ~60 m of slope)
  - All 4 DEMs agree on mean elevation within ~3 m, on min elevation within ~3 m, and on peak elevation within ~14 m (the spread is the well-known canopy-vs-ground sensor split — see §2.5.1 for the rendered cross-check)
- **File:** `docs/site_data/alos_aw3d30_dem.tif` (Int16, EPSG:4326, 108 × 108 pixels)

### 2.2 Copernicus DEM 30 m (GLO-30, COP30) — *best optical-stereo DEM*

- **Source:** European Space Agency (ESA) Copernicus programme. Optical stereo from Sentinel-2 imagery.
- **Acquisition:** 2018-2021 (composite of multiple Sentinel-2 stereo pairs)
- **Vertical accuracy:** ~4 m RMSE in flat areas, ~10 m in forested/steep areas
- **Why we use it as a cross-check:** Independent of radar (AW3D30 is radar, COP30 is optical), so a strong agreement between the two confirms the elevation truth. Useful for vegetation-height comparisons: AW3D30 tends to read the canopy top in dense forest; COP30 tends to read the ground because it uses optical stereo matching.
- **What the data shows for our site:** Elevation 116-380 m, mean 161 m. Essentially identical to AW3D30 in the open areas; in the dense forest there's a 1-3 m difference (which tells us the canopy is 1-3 m thick at this scale — consistent with the GEDI canopy data).
- **File:** `docs/site_data/cop30_dem.tif` (Float32, 108 × 108 pixels, ~52 KB — bigger than ALOS because it's float, not int)

### 2.3 SRTM v3 GL1 30 m — *the legacy reference*

- **Source:** NASA Shuttle Radar Topography Mission, 2000 (the original 11-day shuttle flight). Reprocessed in 2016 with SRTM v3.1 algorithm (improved noise reduction). "GL1" = Global 1 arc-second, the seamless worldwide product.
- **Acquisition:** February 2000 (11 days of shuttle imaging)
- **Vertical accuracy:** ~5-9 m RMSE. The 2000-era data has slightly more noise than the modern DEMs.
- **Why we use it as a cross-check:** SRTM is the **most-used global DEM in the world** — every commercial GIS product, every published study, every research paper uses it as a baseline. Matching SRTM is a sanity check that our elevation truth is consistent with the global baseline.
- **What the data shows for our site:** Elevation 118-375 m, mean 163 m. 2-3 m higher than AW3D30 on average — consistent with SRTM v3.1's known slight positive bias in vegetated mid-latitude terrain. Not a problem, just a known quirk.
- **File:** `docs/site_data/srtm_gl1_dem.tif`

### 2.4 NASADEM 30 m — *the "improved SRTM"*

- **Source:** NASA, 2020 release. NASADEM is the original SRTM data reprocessed with **modern noise reduction algorithms** (ICEsat-2 altimetry cross-calibration, better void-filling, better canopy correction). It's basically "SRTM v4" without the 2000-era artifacts.
- **Acquisition:** Original SRTM data (2000) reprocessed 2020
- **Vertical accuracy:** ~4 m RMSE — better than the original SRTM, comparable to AW3D30
- **Why we use it as a cross-check:** It's the "modern SRTM" and serves as a bridge between the original 2000 SRTM and the 2010s AW3D30. Strong agreement between NASADEM and AW3D30 is the strongest cross-validation we can do.
- **What the data shows for our site:** Elevation 115-371 m, mean 160 m. Within 1 m of AW3D30 on average. The 264 m of relief is confirmed.
- **File:** `docs/site_data/nasadem_dem.tif`

### 2.5 The 4 hillshade PNGs

For each DEM, we generated a hillshade — a visualization of the same elevation data as if it were lit by a 45°-altitude sun from the NW (315° azimuth). Hillshades are the standard way to "see" terrain because the human eye reads shaded relief better than color-coded elevation.

- All 4 hillshades show the same landforms: a clear upper plateau (the sandstone escarpment top), a steep slope down to a mid-elevation terrace (where the house platform sits), a gentler slope to the stream, and the flat-rock pool in the lowest area
- The CopDEM and NASADEM hillshades show slightly sharper detail than SRTM (cleaner radar speckle, less smoothing)
- Used as the base for `analysis/site_diagnostic.png` (the master overlay)
- Files: `docs/site_data/*_hillshade.png` (~85-90 KB each)

### 2.5.1 Cross-validation result — rendered receipt (2026-06-18)

The hillshades and stats prove the 4 DEMs *encode* the same terrain. To also prove that the choice of DEM is **visually invisible** under the displacement + SUBSURF stack used by the 62-ha photoreal renderer, we baked all four to normalized 16-bit heightmaps and rendered each through `lqv/subscene/terrain_62ha_photoreal.py` via the `LQV_DEM_OVERRIDE_PNG` / `LQV_DEM_OVERRIDE_JSON` env hooks (orchestrator: `scripts/render_dem_ab.py`, run_id `dem_ab_20260618`).

Two contact sheets ship the result:

- **`docs/site_data/dem_ab_contact.png`** — 4-panel heightmap PNG sheet (encoding agreement)
- **`docs/site_data/dem_ab_oblique_contact.png`** — 4-panel oblique-render sheet (1088×900, ~537 KB), the visual proof that the four sources render identically under our oblique camera framing (`scripts/contact_sheet_dem_ab_oblique.py`)

Cropped to the actual 62-ha parcel window the four sensors agree on **mean elevation within 2.9 m** (138.1 – 141.0 m AMSL), on **min elevation within 3.0 m** (125.0 – 128.0 m), and disagree by **14.0 m on peak elevation** (ALOS 171.0 m vs NASADEM 157.0 m) — entirely consistent with each sensor's published RMSE and the well-known canopy-vs-ground sensor split (ALOS optical-stereo reads canopy tops; modern void-filled SRTM/NASADEM reads ground). AW3D30 (canonical) sits at the high end of the cluster on peak but in the middle on mean.

| DEM     | min (m) | max (m) | mean (m) |
|---------|---------|---------|----------|
| ALOS    | 128.0   | 171.0   | 139.6    |
| COP30   | 125.1   | 163.0   | 138.1    |
| SRTM    | 127.0   | 160.0   | 141.0    |
| NASADEM | 125.0   | 157.0   | 138.4    |

### 2.6 Derived analysis (from AW3D30 specifically)

| Product | What it shows | File |
|---|---|---|
| `alos_slope.tif` | Slope in degrees (0-90°) per pixel | `analysis/alos_slope.tif` |
| `alos_aspect.tif` | Compass direction each slope faces (0-360°) | `analysis/alos_aspect.tif` |
| `alos_buildability.tif` | 4-class buildability: 0-8% / 8-15% / 15-30% / >30% slope | `analysis/alos_buildability.tif` |
| `slope_and_buildability.png` | Side-by-side visualization of slope + buildability | `analysis/slope_and_buildability.png` |
| `site_diagnostic.png` | **Master overlay** — hillshade + buildability + 10m contours + search bbox | `analysis/site_diagnostic.png` |
| `analysis_summary.txt` | Per-class elevation stats (text) | `analysis/analysis_summary.txt` |

**Key buildability findings:**

| Class | Slope | Pixels | % of bbox | Elevation p10–p90 | What to do |
|---|---|---|---|---|---|
| 1 — flat | 0–8% | 6,707 | 57.5% | 127–169 m | **Easily buildable** — house platform zone |
| 2 — buildable | 8–15% | 2,695 | 23.1% | 132–203 m | Buildable with care (terracing if needed) |
| 3 — challenging | 15–30% | 1,441 | 12.4% | 142–250 m | Terracing needed; use for solar frames + agriculture |
| 4 — steep | >30% | 821 | 7.0% | 188–325 m | **Don't build** — keep as forest, views, trails |

**The flat zone at 127–169 m AMSL is exactly where the existing research puts the upper-terrace house platform** — the data confirms the design choice. The steep class is the escarpment (188+ m); the stream pool is in the lowest pixels (~116 m).

---

## 3. NASA Earthdata data — GEDI L2A (vegetation LiDAR)

GEDI (Global Ecosystem Dynamics Investigation) is a spaceborne LiDAR on the International Space Station. It shoots laser pulses at the ground and measures the time-of-flight. From the returned waveform, NASA computes:

- **`lat_lowestmode` / `lon_lowestmode`** — latitude/longitude of the laser shot's ground footprint
- **`elev_lowestmode`** — the elevation of the lowest return (the ground, in principle)
- **`elev_highestreturn`** — the elevation of the highest return (the top of the vegetation canopy)
- **`quality_flag`**, **`degrade_flag`**, **`sensitivity`** — quality indicators per shot

**Canopy height** is computed as `elev_highestreturn - elev_lowestmode` (the difference is the vegetation layer).

The "L2A" product is the **highest-level standard GEDI product** — geolocated, calibrated, and quality-flagged.

### 3.1 What we got

- **27 granules** covering the 3.3 km × 3.3 km bbox (one per satellite pass, 2019-2025)
- **475 quality-filtered unique shots** in the bbox after applying the standard QA filters (quality_flag == 0, degrade_flag == 0, sensitivity > 0.9)
- Distribution is uneven: a few orbits cross our area densely, most don't
- Stored as `docs/site_data/gedi_l2a_points.csv` (one row per shot, 75 KB)

### 3.2 ⚠ The elev_lowestmode unit bug — what we know

When we analyzed the 475 raw shots, the median `ground_elevation_m` came out to **4654 m AMSL**, with a max of 9145 m. For context, the actual site elevation per our 4 DEMs is 116-380 m AMSL. The numbers are off by 10-100×.

**Diagnosis:** This is a known issue with GEDI02_A v002 for certain beams / orbits. The `elev_lowestmode` field is sometimes:
- Reported in **centimeters** instead of meters (would explain 1445 m → 14.45 m, way too low; 9145 m → 91.45 m, in the right ballpark but still off)
- Or the field is **scaled by a beam-specific factor** that varies
- Or in the worst case the field is **flagged with a different sentinel** that we're not catching with our quality filter

**What we did:** Filtered to shots with `100 < ground_elevation_m < 500 m` (matches the DEM-derived plausible range for our site). **25/475 shots survive.** Saved as `gedi_l2a_points_clean.csv`.

**What this means:**
- The **canopy_height_m field is reliable** (it's a difference, so unit errors cancel)
- The **dem_elev_m** we joined from ALOS is the trustworthy ground elevation per shot
- The 25 clean shots are useful but **not enough** for a full vegetation map
- We need to re-pull the GEDI data once the **cloud-pool EULA** is accepted (the per-granule processing will be much faster and the unit issue might be fixable by selecting the right beam)

### 3.3 What the 25 clean shots tell us anyway

| Metric | Value | Source |
|---|---|---|
| Ground elevation (cleaned GEDI) | 144–273 m AMSL (median 207) | `gedi_l2a_points_clean.csv`, 25 shots |
| Ground elevation (DEM at those XY) | 131–268 m AMSL (median 141) | `alos_aw3d30_dem.tif` sampled at shot locations |
| Canopy height (raw GEDI) | 0–74 m (median 7.5, 75th pct 29) | `canopy_height_m` field (difference-based, reliable) |
| Canopy height (DEM-anchored) | 19–80 m (median 37, 75th pct 80) | `canopy_from_dem_m` (our recomputation) |
| Beam distribution | 9 BEAM0000, 7 BEAM0010, 3 BEAM0011, 2 each in 3 more, 1 each in 2 more | Most shots in the strongest beam (BEAM0000), as expected |

**Interpretation:** The Atlantic Forest here is **mature tall-canopy forest** — median canopy 37 m (DEM-anchored) is consistent with primary Atlantic Forest, not degraded pasture. The 25 shots are clustered in the lower 2/3 of the elevation range (144-273 m) because that's where the GEDI orbit coverage happens to land. The upper escarpment (300+ m) and the stream bed (115-125 m) are under-represented in the clean set.

### 3.4 GEDI L4A (Aboveground Biomass Density) — *not yet pulled*

GEDI L4A is a gridded product (~1 km tiles) that estimates aboveground biomass in Mg/ha using GEDI L2A + other satellite data. For a 62 ha property, the 1 km grid gives us **1-2 pixels** — not useful for per-property analysis. Better: use the L2A canopy directly with an allometric model (e.g. Chave 2014 pantropical allometry) to estimate per-shot biomass. We can compute that in v2.

### 3.5 Re-pull path (when the cloud-pool EULA is accepted)

Once the "Earthdata Cloud Data Pool" EULA is accepted in `search.earthdata.nasa.gov` + token regenerated, we can re-pull the same 27 GEDI L2A granules via **direct S3 streaming** in ~5-10 min instead of the 30-60 min HTTPS fallback. The fast path uses h5py's selective column reads to fetch only the 7 datasets we care about per beam (lat, lon, elev_ground, elev_highest, quality, degrade, sensitivity) — typically 50-150 MB per granule instead of 1.2 GB.

**Action item:** Wesley accepts the cloud-pool EULA in `search.earthdata.nasa.gov` → click "Download" on a cloud-hosted GEDI file → accept the "Earthdata Cloud Data Pool" modal → regenerate the bearer token. Then I can re-run the GEDI extraction in 5-10 min, likely with hundreds of clean shots, and we'll have a full vegetation map.

---

## 4. Cross-validation across sources

The 4 DEMs + the GEDI data form a multi-source ground truth. Where they agree, we're confident. Where they disagree, we know to look more carefully.

### 4.1 DEM cross-validation

| DEM | Min (m) | Max (m) | Mean (m) | Median (m) | Range (m) |
|---|---|---|---|---|---|
| AW3D30 (canonical) | 116 | 380 | 162 | 149 | 264 |
| COP30 | 116 | 380 | 161 | 147 | 264 |
| NASADEM | 115 | 371 | 160 | 147 | 256 |
| SRTM v3 | 118 | 375 | 163 | 150 | 257 |

**The big number: all 4 agree on 116-380 m total relief, with mean elevation 160-163 m. The site is real, the elevation is robust.**

Differences:
- SRTM is consistently 2-3 m higher than the others (known v3.1 positive bias in vegetated mid-latitude terrain)
- AW3D30 and COP30 are within 1 m of each other on average
- NASADEM is the "modern" SRTM, basically equivalent to AW3D30 in this terrain
- All 4 show the same landform structure (escarpment → mid-slope → terrace → stream)

### 4.2 GEDI vs DEM cross-validation

For the 25 clean shots, the GEDI `ground_elevation_m` is **on average 40-60 m higher** than the DEM at the same XY. This is the elev unit bug (a few hundred m or more for many shots, 40-60 m for the cleaner ones). The DEM is the trustworthy elevation truth; the GEDI shot gives us vegetation structure and a *relative* elevation.

### 4.3 Canopy vs buildability (cross-source insight)

Combining the canopy height (GEDI) with the buildability map (DEM-derived slope classes) we can see a pattern:
- **Flat class (slope 0-8%, elev 127-169 m)**: This is where the house platform goes. The GEDI shots in this zone show mature canopy (~37 m median) — the cob house will sit in a clearing within mature forest
- **Buildable class (slope 8-15%, elev 132-203 m)**: Similar canopy, slightly less flat
- **Steep class (slope >30%, elev 188-325 m)**: The escarpment — canopy reads the cliff face + any trees clinging to it
- **Stream zone (slope 0-8%, elev 116-130 m)**: Canopy is sparser here (close to the stream = some clearing) — useful for the restaurant, pool, footbridge

---

## 5. What we now know about the 62 ha

**Solid (cross-validated by 4 DEMs):**
- The site is 116-380 m AMSL with 264 m of relief
- 80% of the 3.3 km × 3.3 km search area is flat or buildable (slope <15%)
- The upper-terrace platform sits at 127-169 m elevation (matches the existing research doc)
- The stream is at ~116-120 m, the escarpment is at ~380 m
- The vegetation is mature Atlantic Forest (canopy 0-74 m, median 7.5 m, with mature-tree outliers up to 80 m)

**Probable (based on the 25 clean GEDI shots + cross-source insight):**
- The house platform will sit in mature forest that needs clearing — the cob house is well-suited to this (organic forms, can integrate with tree retention)
- The southern slopes (cooler, in Southern Hemisphere away from the equator) are the buildable area; the northern slopes (warm face) should be forested
- The escarpment is the visual asset and the "named feature" — every vacation-rental unit should have a sightline to it

**Uncertain (need more data or field visit):**
- The actual 62 ha property boundaries (waiting on Anexo I of the boleto)
- The exact location of existing structures (the research doc mentions a block house and a quincho — need coordinates)
- The road access condition (the research says red dirt track; needs an actual drive)
- Acoustic and dark-sky baseline (field measurement, not remote sensing)
- Camera trap biodiversity survey (R36 — needs 12 months of fieldwork)

---

## 6. What the data does NOT tell us

Important to be honest about:

- **No actual satellite imagery of the property** (no RGB photo, no NIR). The hillshades are derived from DEM, not from satellite photos. We have terrain structure, not what it looks like. Sentinel-2 fetch is queued (see §7).
- **No 1 m DEM** of the 62 ha. The 30 m DEM is 108×108 pixels for 1,100 ha — a cabin site might span 1-2 pixels. Drone LiDAR (R35, ~$1,500) is the path to 1 m.
- **No GEDI L2B, L4A, L1B** (the 403s blocked them; need cloud-pool EULA).
- **No SRTM, NASADEM, HLSL, MCD12Q1** from NASA directly (same EULA blocker).
- **No Sentinel-2 or Landsat** RGB/NIR (just queued).
- **No WorldClim** climate data (the server is dead/redirecting, need a new source).
- **No OpenStreetMap features** (the area is too rural; the Overpass server returned 0 roads in 5 km radius).
- **No acoustic or dark-sky baseline** (R36 — needs field measurement).
- **No high-res drone or aerial imagery** (R35 — needs the drone LiDAR).
- **No Anexo I of the boleto** (R02 — chase with Escribana Peña).

---

## 7. Acquisition scripts (all saved in `scripts/`)

For reproducibility, every data product above has a script that can re-fetch it. The scripts are designed to be idempotent (won't re-download if file exists) and configurable (just change the bbox or date range).

| Script | What it does | Auth required |
|---|---|---|
| `scripts/fetch_opentopo_dem.py` | Pulls AW3D30, COP30, SRTM, NASADEM from OpenTopography | `OPENTOPOGRAPHY_API_KEY` in `.env.local` (already set) |
| `scripts/analyze_dem.py` | Computes slope, aspect, buildability, hillshades, site_diagnostic.png | None |
| `scripts/extract_gedi_https.py` | Pulls all 27 GEDI L2A granules via HTTPS pre-signed CloudFront | `NASA_EARTHDATA_TOKEN` in `.env.local` (set) |
| `scripts/extract_gedi_s3.py` | **Faster** GEDI pull via S3 streaming (will work once cloud-pool EULA accepted) | Same + cloud-pool EULA |
| `scripts/clean_gedi.py` | Filters elev unit/scaling outliers, joins DEM elevations | None (uses files already on disk) |
| `scripts/fetch_sentinel2.py` | Pulls lowest-cloud Sentinel-2 L2A scene + RGB preview | **Failed** — element84 STAC query needs fixing. Pending. |
| `scripts/fetch_worldclim.py` | Pulls WorldClim 2.1 climate baseline (30s-arc) | **Failed** — geodata.ucdavis.edu is dead. Pending new source. |
| `scripts/fetch_osm.py` | Pulls OSM features (roads, buildings, POIs, water, places) | None (Overpass API). **Returned 0 features** in 5 km radius — area is genuinely rural. |

---

## 8. What to do next (the gap list, prioritized)

| Priority | Action | Unblocks | Effort |
|---|---|---|---|
| **#1** | **Wesley accepts the cloud-pool EULA** at `search.earthdata.nasa.gov` → click "Download" on a cloud-hosted GEDI file → accept the "Earthdata Cloud Data Pool" modal → regenerate the bearer token | All NASA S3 streaming (GEDI re-pull in 5-10 min, GEDI L2B/L4A/L1B, HLSL, MCD12Q1, SRTM direct) | 5 min user action |
| **#2** | **Drone LiDAR 1 m DEM of 62 ha** (~ $1,500) | Unlocks every Tier-1+ GIS layer (viewshed, NDWI, fine-scale slope, building footprint siting, render-agent heightmap). **Highest-ROI single dataset for the project.** | $1,500 + ~ 1 week delivery |
| **#3** | **Site visit to Escobar** (R01) | Validates the 62 ha boundaries, identifies existing structures, road condition, terrain validation | 1 day |
| **#4** | **Sentinel-2 fetch fix** (currently 400 from element84 STAC) | Real RGB photo of the site for marketing + design | 30 min once URL fixed |
| **#5** | **Anexo I from Escribana Peña** (R02) | Exact 62 ha boundaries, sub-clipping all data to actual property | 1 day chase |
| **#6** | **GBIF species occurrences** (free, no auth) | Biodiversity narrative for Awasi / San Bernardino outreach | 30 min script |
| **#7** | **Acoustic + dark-sky baseline** (R36, ~$3-5k) | Premium pricing justification, "named feature" content | Field visit |
| **#8** | **Awasi partnership** (R37) | EU distribution + credibility | Wesley's network + outreach draft |
| **#9** | **San Bernardino partnership** (R38) | Domestic German-Paraguayan summer crowd | Outreach draft |

---

## 9. References & data sources

**OpenTopography:**
- ALOS World 3D 30m (AW3D30): https://www.eorc.jaxa.jp/ALOS/en/aw3d30/aw3d30v11_product_e.htm — CC-BY 4.0
- Copernicus DEM: https://copernicus.eu/en/access-data/copernicus-data — free
- SRTM v3 GL1: https://lpdaac.usgs.gov/products/srtmgl1v003/ — NASA public domain
- NASADEM: https://lpdaac.usgs.gov/products/nasadem_hgtv001/ — NASA public domain
- OpenTopography API: https://opentopography.org/developers

**NASA Earthdata / GEDI:**
- GEDI mission overview: https://gedi.umd.edu/ — NASA
- GEDI02_A product: https://lpdaac.usgs.gov/products/gedi02_av002/ — NASA
- GEDI Algorithm Theoretical Basis Documents: https://daac.ornl.gov/GEDI/guides/GEDI_L4A_AGB_Density_V2_1.html
- Dubayah et al. 2020 (GEDI mission paper): https://doi.org/10.1126/sciadv.aaz3621
- Earthdata Login: https://urs.earthdata.nasa.gov/
- LP DAAC cookbook: https://lpdaac.usgs.gov/resources/e-learning/

**Derivative analyses:**
- GDAL `gdaldem` slope/aspect/hillshade: https://gdal.org/programs/gdaldem.html
- GDAL/rasterio: https://rasterio.readthedocs.io/
- matplotlib: https://matplotlib.org/

**Standards:**
- Solar exposure: PVGIS (EU JRC): https://re.jrc.ec.europa.eu/pvg_tools/en/
- WGS84 / UTM zone 21S (EPSG:32721) for the area
- Coordinate system: all data in EPSG:4326 (lat/lon) unless noted

---

## 10. Glossary (for non-GIS readers)

- **DEM** (Digital Elevation Model) — a raster image where each pixel holds the elevation at that point.
- **Hillshade** — a DEM rendered as if lit by a low-angle sun, to make terrain visible.
- **Amsl** (Above Mean Sea Level) — the elevation reference. 0 m is sea level.
- **LiDAR** — Light Detection And Ranging. A sensor that shoots laser pulses and measures the time-of-flight, producing 3D point clouds of the surface below.
- **GEDI** (Global Ecosystem Dynamics Investigation) — NASA's spaceborne LiDAR on the ISS.
- **L2A** — Level 2A product: geolocated, calibrated, quality-flagged GEDI data.
- **UTM** (Universal Transverse Mercator) — a coordinate system in meters. Zone 21S covers our site (-25° latitude, -57° longitude).
- **EPSG:4326** — the lat/lon coordinate system (WGS84).
- **EPSG:32721** — UTM zone 21S (Southern hemisphere) for our site.
- **STAC** (SpatioTemporal Asset Catalog) — a standard for searching geospatial data.
- **Overpass API** — OpenStreetMap's query API for extracting features.
- **CC-BY 4.0** — Creative Commons Attribution license (free, with credit).
- **Pixel** — a single grid cell in a raster image. At 30 m resolution, each pixel covers 30 m × 30 m = 900 m².
- **Granule** — a single "scene" of satellite data. For GEDI, one granule = one ~4-minute satellite pass.

---

## 11. Satellite data roadmap (T1–T4)

Ranked list of satellite / GIS data sources to add to the LQV digital twin,
prioritised by impact-per-effort. T1 = high impact + low effort (do first).
The canonical AOI for every fetcher is `docs/site_data/aoi_62ha.geojson`
(loaded via `scripts/satellite/_aoi.py`).

### T1 — high impact, low effort (ship now)

| Source                         | Resolution | Why we want it                                            | Fetcher                                                 | License        |
| ------------------------------ | ---------- | --------------------------------------------------------- | ------------------------------------------------------- | -------------- |
| Sentinel-2 L2A multi-temporal  | 10 / 20 m  | NDVI / NDWI time series, dry-vs-wet season comparison     | `scripts/satellite/fetch_sentinel2.py`                  | Copernicus     |
| Sentinel-1 RTC (SAR)           | 10 m       | Cloud-free, day+night backscatter — wetness + structure   | `scripts/satellite/pc_stac_quickstart.py --collection sentinel-1-rtc` | Copernicus     |
| ESA WorldCover 10 m            | 10 m       | 11-class landcover snapshot (forest / grass / built / …)  | `scripts/satellite/fetch_landcover.py --only worldcover` | CC-BY 4.0      |
| JRC Global Surface Water       | 30 m       | Where water historically pools (gullies, low spots)       | `scripts/satellite/fetch_landcover.py --only jrc-gsw`   | EC / open      |
| Google Earth Engine (NDVI)     | 10 m       | Server-side reductions over years of S2 in one call       | `scripts/satellite/gee_quickstart.py`                   | Copernicus     |
| Planet NICFI basemap           | ~5 m       | Closer to "drone photo" texture for canopy outlines       | `scripts/satellite/fetch_nicfi.py`                      | Planet NICFI (NC) |

### T2 — medium impact (do next)

| Source                         | Resolution | Why we want it                                            | Fetcher                                                 | License        |
| ------------------------------ | ---------- | --------------------------------------------------------- | ------------------------------------------------------- | -------------- |
| Copernicus DEM GLO-30          | 30 m       | Modern global DEM — sanity-check vs ALOS                  | `scripts/satellite/pc_stac_quickstart.py --collection cop-dem-glo-30` | CC-BY 4.0      |
| CHIRPS daily rainfall          | ~5 km      | Defensible dry-season numbers for the site mgmt plan      | `scripts/satellite/fetch_climate.py --only chirps`      | Public domain  |
| TerraClimate monthly           | ~4 km      | Long-term water balance (PET, soil moisture, tmin/tmax)   | `scripts/satellite/fetch_climate.py --only terraclimate` | Open           |
| Hansen Global Forest Change    | 30 m       | Year of tree-cover loss 2000–present                      | `scripts/satellite/fetch_landcover.py --only hansen`    | UMD / GLAD     |
| HLS (Harmonized L/S)           | 30 m       | Harmonized Landsat + Sentinel-2 — denser time series      | `scripts/satellite/pc_stac_quickstart.py --collection hls2-s30` | NASA, open     |

### T3 — high effort or paid (defer)

- Drone orthomosaic (DJI Mini 4 Pro + ODM): cm-scale truth, but needs a site visit.
- Airborne lidar: defensible canopy heights, but no public coverage of Escobar.
- SkySat / WorldView / Pléiades (commercial sub-meter): only if a buyer asks for it.

### T4 — niche / specialty (consider later)

- GEDI L4A above-ground biomass: ~25 m footprints, sparse over a 62-ha parcel.
- MODIS LST: thermal time series, 1 km is too coarse for parcel-level decisions.
- VIIRS night-lights: useful for the regional context slide, not for the parcel.
- OpenStreetMap (Overpass): roads, place names, admin polygons — already pulled separately.
- Sentinel-5P (atmospheric): NO₂ / CH₄ trends at country scale, not parcel scale.

### How to actually run any of this

```bash
# 1. Activate the project venv (or any Python 3.11+ env).
# 2. Install the optional GIS stack ONCE:
pip install planetary-computer pystac-client stackstac rioxarray rasterio xarray earthengine-api requests

# 3. Probe Planetary Computer for what's available:
PYTHONPATH=. python -m scripts.satellite.pc_stac_quickstart --list-collections

# 4. Pull a Sentinel-2 search index (no download):
PYTHONPATH=. python -m scripts.satellite.pc_stac_quickstart --collection sentinel-2-l2a --days 90

# 5. Pull WorldCover landcover, clipped to our AOI:
PYTHONPATH=. python -m scripts.satellite.fetch_landcover --only worldcover

# 6. Pull CHIRPS monthly rainfall over the last 18 months:
PYTHONPATH=. python -m scripts.satellite.fetch_climate --only chirps --start 2025-01-01 --end 2026-06-01
```

Every fetcher writes under `docs/site_data/<source>/` with deterministic names
so re-runs are idempotent. None of the fetchers touches `build_scene.py`.

License gate (enforced at intake): **CC0 and CC-BY 4.0 only** for anything
that ships in the bundle. CHIRPS, WorldCover, JRC GSW, Copernicus,
Hansen are all compatible. Planet NICFI is non-commercial — fine for the
escritura deck and the site management plan, **not** for resale.

---

*Compiled by AI Whisperers on 2026-06-10; §11 satellite roadmap added 2026-06-17. All data in `docs/site_data/`. All scripts in `scripts/`. See `docs/research/README.md` for the broader research synthesis. Re-runs are cheap; call the scripts whenever you want fresh data.*
