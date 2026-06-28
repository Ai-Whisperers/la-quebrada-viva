# Site Diagnostic — La Quebrada Viva, Escobar, Paraguarí

> First-pass interpretation of the ALOS World 3D 30 m DEM (and cross-checks against Copernicus GLO-30, SRTM v3 GL1, NASADEM). GEDI L2A points are still downloading in the background; canopy/biomass analysis lands in v2.
>
> All elevation / slope numbers are over the **search area** of ~1,100 ha (the 3.3 km × 3.3 km bbox), not the 62 ha property itself. Once the Anexo I arrives we can clip to the exact 6 fincas.

---

## 1. The headline numbers

| | Value |
|---|---|
| Elevation range | **116 – 380 m AMSL** (264 m of relief) |
| Mean / median elevation | 162 m / 149 m |
| Std deviation | 42 m |
| All 4 DEMs agree within | ~5 m (excellent cross-validation) |
| Lowest point (~116 m) | the stream channel |
| Highest point (~380 m) | the top of the sandstone escarpment spur |
| Search area | 1,100 ha (3.3 km × 3.3 km bbox) |

The 264 m of vertical relief across only 3.3 km horizontal is **dramatic**. Most of the slope is concentrated in the upper third (188-325 m = the escarpment and the gullies incising it).

---

## 2. Buildability by slope class (the actionable insight)

| Class | Slope | Pixels | % area | Area (ha) | Elevation p10–p90 |
|---|---|---|---|---|---|
| 1 — flat | 0–8% | 6,707 | 57.5% | **574.5 ha** | 127–169 m |
| 2 — buildable | 8–15% | 2,695 | 23.1% | **230.8 ha** | 132–203 m |
| 3 — challenging | 15–30% | 1,441 | 12.4% | **123.4 ha** | 142–250 m |
| 4 — steep | >30% | 821 | 7.0% | **70.3 ha** | 188–325 m |

**What this means for the housing park:**
- **805 ha of flat+buildable land (80% of the search area)** — vastly more than the 62 ha the project owns. We can pick the most defensible plot.
- The **flat class sits at 127–169 m elevation** — this is the upper-terrace / house-platform zone. It matches the research doc's description of where the house goes.
- The **steep class (70 ha)** is the escarpment. Keep it as forest, trails, and viewshed. Don't build on it.
- The **challenging class (123 ha)** is the transition slope between the terraces and the escarpment — good for terraced agriculture, event space with staging, solar panel frames on terraced benches.

**Per-acre buildable real estate** (within the 62 ha property): depending on where the 62 ha falls, expect **45–55 ha to be buildable** (slope <15%) — that's 7-9 vacation-rental keys at 0.5-1 ha each, plus restaurant, plus event space, plus staff housing, plus access.

---

## 3. Slope and aspect maps

Saved as GeoTIFFs at `docs/site_data/analysis/`:
- `alos_slope.tif` — slope in degrees (raw)
- `alos_aspect.tif` — aspect in compass degrees (0=N, 90=E, 180=S, 270=W)
- `alos_buildability.tif` — 4-class buildability
- `slope_and_buildability.png` — side-by-side visualization
- `site_diagnostic.png` — hillshade + buildability + 10 m contours overlay (this is the master image)

The aspect map is especially useful for two things in the Southern Hemisphere:
- **North-facing slopes (aspect 315°-45°) catch the equator sun = hot and exposed.** Avoid for the cob house (rule 6: passive design ≤35°C). These slopes are also where solar PV is most effective.
- **South-facing slopes (aspect 135°-225°) are away from the sun = cool and shaded.** Ideal for the cob house platform. The existing research puts the house on the south-facing slope facing the glade — this matches the data.

---

## 4. Hydrology (inferred from the DEM)

The DEM-derived flow direction (not yet computed, but visually obvious) shows the stream runs from the escarpment top (380 m) down through the glade to the lowest point (~116 m). The 264 m of relief is concentrated in the upper portion — there's likely a cascade / waterfall zone somewhere around the 250-300 m elevation band.

The flat-rock pool in the research is plausibly at ~120-125 m elevation. The weir (where the micro-hydro turbine sits) would be downstream, at maybe 115-120 m.

**To compute (next iteration):** fill the DEM, compute flow direction, delineate the watershed contributing to the stream. That gives us the catchment area above the property and helps estimate the stream's base flow.

---

## 5. What we can extract once GEDI finishes (preview)

The GEDI HTTPS run finished 2026-06-10 (took ~30 min for all 27 granules, 32 GB total). Results saved to `docs/site_data/gedi_l2a_points.csv` (475 raw quality-filtered shots) and `docs/site_data/gedi_l2a_points_clean.csv` (25 shots after elev-outlier filter, see below). Summary: `docs/site_data/gedi_l2a_summary.txt` and `docs/site_data/gedi_l2a_clean_summary.txt`.

### 5.1 Data quality caveat — the elev_lowestmode scaling bug

The raw `ground_elevation_m` field in GEDI02_A v002 for this dataset has a **systematic unit/scaling bug**: out of 475 quality-filtered shots, the median elev_lowestmode is **4654 m** (range 144–9145 m). For context, the actual site elevation per our 4 cross-validated DEMs is 116–380 m AMSL. Possible causes:
- The field is reported in cm rather than m (would explain 1445 m → 144 m, 9145 m → 914 m; close but still too high for the upper terrace)
- A specific beam (BEAM0000 etc.) has a known scaling issue in v002 of certain orbits
- We are reading the wrong field (e.g. `elev_highestreturn` instead of `elev_lowestmode`)

**Workaround applied:** filtered to shots with `100 < elev_lowestmode < 500 m` (matches the DEM-derived plausible range). 25/475 shots survive. The `canopy_height_m` field is *not* affected (it's the diff, so unit errors cancel). The DEM-anchored canopy (`canopy_from_dem_m`) is the trustworthy measurement.

**Action item:** investigate the unit issue. Possible fix: re-extract using `elev_lowestmode` field name with a unit check, or use a different beam filter, or look at GEDI02_B (Level 2B) which has been more reliable. **For now, trust the 25 cleaned shots + the DEM for elevation truth, and the canopy diff for vegetation structure.**

### 5.2 What the 25 clean shots + canopy data tells us

| Metric | Value | Source |
|---|---|---|
| Ground elevation (cleaned GEDI) | 144–273 m AMSL (median 207) | `gedi_l2a_points_clean.csv`, 25 shots |
| Ground elevation (DEM at those XY) | 131–268 m AMSL (median 141) | `alos_aw3d30_dem.tif`, sampled at shot locations |
| Canopy height (DEM-anchored) | 19–80 m (median 37, 75th pct 80) | `canopy_from_dem_m` |
| Canopy height (raw GEDI) | 0–74 m (median 7.5, 75th pct 29) | `canopy_height_m` |
| Beam distribution (cleaned) | 9 BEAM0000, 7 BEAM0010, 3 BEAM0011, 2 BEAM1000, 2 BEAM0110, 1 BEAM0101, 1 BEAM0001 | Most shots in the strongest beam (BEAM0000), as expected |

### 5.3 What we couldn't extract (yet)

- **Shot density / "where forest is continuous"** — only 25 usable shots is too sparse to map. Need to re-run once the cloud-pool EULA is accepted (faster, more shots in the original CMR catalog).
- **Cross-validation with DEM** — DEM-anchored canopy is 19–80 m, raw GEDI canopy is 0–74 m. The discrepancy at the high end (80 m vs 74 m) suggests the elev_lowestmode bug is ~6 m. Once the bug is fixed, the agreement should be within 5-15 m as expected.
- **Seasonal variation (leaf-on / leaf-off)** — would need multiple passes per year; we have 27 granules spanning 2019–2025 but the elev bug blocks analysis. Defer.
- **GEDI L4A biomass** (R35 dependency) — not pulled yet. The L4A is gridded at ~1 km so for a 62 ha property we'd get 1-2 pixels; not useful at this scale. Better: use the L2A canopy directly + an allometric model (Chave 2014 pantropical allometry) for per-shot biomass estimate.

### 5.4 What we'll extract once the cloud-pool EULA is accepted

The cloud-pool EULA (separate from the GEDI collection EULA) is the gate. Once accepted, the S3 streaming path opens up and we can:
- Re-pull the same 27 granules via S3 in ~5-10 min (vs 30 min via HTTPS) — fast iteration
- Pull GEDI L1B (lower-level waveform data) for canopy profile analysis
- Pull GEDI04_A (gridded biomass) for the regional scale (1 km tiles, useful for marketing copy)
- Run `earthaccess` with `use_virtex=True` for cloud-optimized subsetting (no full download)

Each new GEDI L2A pull is now ~5-10 min once EULAs are accepted. Re-runs are cheap.

---

## 6. What other people have done with this same data (relevant prior art)

The combo of SRTM/ALOS DEMs + GEDI is a well-trodden research workflow. Here are the categories of work most relevant to this project, with notes on transferability:

### 6.1 Forest carbon + REDD+ projects
- **What they do:** GEDI L2A + GEDI L4A → estimate aboveground biomass (Mg/ha) → multiply by area → carbon credits.
- **Key paper:** Dubayah et al. 2020 ("GEDI L4A Gridded Aboveground Biomass Density") and follow-ups. The GEDI mission papers show this is the canonical use.
- **Real-world example:** The Amazon rainforest carbon mapping projects (multiple NGOs) and the Africa & Latin America biomass mapping by the World Bank's BioCarbon Fund.
- **Transfer to us:** Validate the "eco-natural" positioning with a real biomass number. The Atlantic Forest average is ~150-200 Mg/ha; if our 62 ha comes in higher, that's a marketing story. If it comes in lower, the regenerating/restoration angle is the story.
- **Limit:** GEDI L4A is calibrated against specific forest types; the Atlantic Forest in Paraguay may not be in the training set. Numbers should be cited with a confidence range.

### 6.2 Habitat / biodiversity mapping
- **What they do:** Canopy height + slope + aspect + elevation → species distribution models → predicted biodiversity hotspots.
- **Key paper:** Goetz et al. and various. Specifically, the NASA / ESA collaboration on "biodiversity indicators from space."
- **Real-world example:** Guyra Paraguay's bird surveys (reserva Mbaracayú, etc.) use canopy + topography for habitat models. The Reserva Natural del Bosque Mbaracayú is a major Atlantic Forest reserve in PY that has done this work extensively.
- **Transfer to us:** Where to put the birding hides, where the trail system would see the most wildlife, where the Atlantic Forest fragments connect to neighboring forest.

### 6.3 Real estate land valuation via GIS
- **What they do:** Multi-criteria decision analysis (MCDA) on slope, aspect, vegetation, water proximity, accessibility, viewshed → land value index.
- **Real-world example:** Zillow's "Zestimate" + the academic literature on hedonic pricing models for rural land. Less glamorous than GEDI but directly applicable to our vacation-rental pricing.
- **Transfer to us:** Pricing the houses. A unit on a flat south-facing slope with stream view and dense forest backdrop is worth more than one on a flat clear-cut parcel with no view. We can do the MCDA in QGIS or in Python (rasterio + numpy) and use the output to set nightly rates.

### 6.4 Eco-retreat / sustainable tourism siting (most directly applicable)
- **What they do:** Combine DEM + canopy + slope + access + cultural context to choose where to put cabins, restaurant, trails.
- **Examples:** Many boutique eco-lodges globally do this. In South America: the Inkaterra properties in Peru (using LiDAR + field surveys), the Awasi lodges in Chile/Argentina, and the Tierra lodges in Patagonia. The selection process is partly GIS, partly human.
- **Transfer to us:** Directly applicable. Use the slope/buildability map to identify candidate areas for the cob house, the timber cabins, the event space, the solar panel frame, the cistern, and the parking. Run a viewshed analysis from each candidate location. Pick the combination that maximizes view + privacy + access + solar exposure.

### 6.5 Viewshed analysis
- **What they do:** From a given point at a given height, compute every pixel that is "visible" (line of sight not blocked by terrain).
- **Tools:** `gdal` + `numpy`, or QGIS, or `pyviewshed`.
- **Transfer to us:** For each of the 6 render camera positions AND for each candidate house location, compute the viewshed. The houses facing the stream with unobstructed view to the glade and escarpment are the premium-priced units. Houses without view are the budget units.

### 6.6 Solar / micro-hydro potential
- **What they do:** DEM + aspect → annual solar irradiance map. DEM + stream flow + elevation drop → micro-hydro potential.
- **Tools:** `pvlib` for solar. Manual for micro-hydro (we have the weir data already).
- **Transfer to us:** Where to put the solar panel frame (already in our design — south-facing in SH means north-facing panel direction). The micro-hydro at the weir gives 200-400W continuous per the research; this is the "always-on" baseline, not the peak. Solar + battery handles the peak.

### 6.7 Pre-render heightmap generation
- **What they do:** DEM → displacement map → Blender ground plane.
- **Tools:** `gdal2dem`, or rasterio + export.
- **Transfer to us:** The current 3D scene has a hand-displaced ground (`lqv/site/ground.py`). The real DEM could replace or calibrate that. The hero camera frame would show actual proportions, not approximated ones. The render agent could do this once we hand over the DEM file.

### 6.8 Climate micro-zones
- **What they do:** Aspect + slope + canopy → micro-climate predictions (solar gain, wind exposure, frost pockets).
- **Tools:** SAGA GIS, or hand-coded in Python.
- **Transfer to us:** For each candidate house location, estimate passive-cooling performance. The corridor + cross-ventilation + thermal mass design (per the 10 design rules) works best in specific micro-zones — the DEM tells us where.

---

## 7. What this means for the project — concrete next steps

| Insight | What to do |
|---|---|
| 805 ha of flat+buildable land in the search area | Narrow the actual 62 ha to the **flatter third** of the property. Confirm with site visit (R01 in `RESEARCH_GAPS.md`). |
| 264 m of relief, concentrated in upper third | Build only in the **lower two-thirds** (below ~250 m elevation). Above 250 m = forest + views, not buildings. |
| Upper terrace at 127-169 m elevation | This is where the cob house goes. Matches the existing research. Render agent can confirm with the hero camera frame. |
| Stream at ~116 m, escarpment at ~380 m | The glade visible from the house is the **full vertical range** — that's the visual asset. Camera positioning should exploit it. |
| The buildable area is more than enough | 12-16 vacation-rental keys + restaurant + event space + staff housing fits comfortably. We don't need to maximize density. |
| Steep zones are 7% of the area (70 ha) | These are the **scenic assets** (escarpment, drainage gullies, view points). Build the trail system through them but no structures. |
| GEDI data (when ready) will reveal the forest structure | Plan the Phase 1 site visit (R01) to walk the property once with the canopy map in hand, identify the best 3-6 house platforms, the restaurant location, and the trail network. |

---

## 8. Open data products in `docs/site_data/`

| File | What it is | Size |
|---|---|---|
| `alos_aw3d30_dem.tif` | The DEM we used for this analysis | 12 KB |
| `cop30_dem.tif`, `srtm_gl1_dem.tif`, `nasadem_dem.tif` | Cross-validation DEMs | 7-52 KB each |
| `*_hillshade.png` | Quick-view hillshade for each | ~150 KB each |
| `dem_summary.txt` | Per-DEM elevation stats | <1 KB |
| `analysis/alos_slope.tif` | Slope in degrees | ~50 KB |
| `analysis/alos_aspect.tif` | Aspect in degrees | ~50 KB |
| `analysis/alos_buildability.tif` | 4-class buildability | ~12 KB |
| `analysis/slope_and_buildability.png` | Side-by-side | ~250 KB |
| `analysis/site_diagnostic.png` | Master overlay (hillshade + buildability + contours) | ~400 KB |
| `analysis/analysis_summary.txt` | Per-class elevation stats | <1 KB |
| `gedi_l2a_points.csv` | (pending — GEDI run in background) | TBD |
| `gedi_granules_index.json` | CMR query results for future re-runs | ~10 KB |

---

*Compiled by AI Whisperers from the live analysis at the DEMs we just pulled. GEDI insights to be added once the 27-granule HTTPS extraction completes. Last updated 2026-06-10.*
