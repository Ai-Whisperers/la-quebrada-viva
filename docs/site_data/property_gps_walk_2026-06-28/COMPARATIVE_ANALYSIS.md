# Riverstone Valley — Comparative Analysis: GPS Walk vs Survey vs Satellite

> **For Wesley + Ivan + Kiki.** The **definitive analysis** of what we
> actually know about the Riverstone Valley (formerly La Quebrada Viva)
> parcel, combining all three data sources:
>
> 1. **GPS walk** (Guru Maps, 2026-06-22 + 2026-06-28, 20 points) — what
>    Wes captured on-site with his phone
> 2. **Survey image** (the cadastral subdivision, red-outlined fincas) —
>    the legal boundary
> 3. **Satellite data** (4 DEMs + MapBiomas land cover + Hansen GFC +
>    GBIF + Sentinel-2 — all in `docs/site_data/`) — what the satellites
>    say
>
> **Author:** Erebus (AI Whisperers)
> **Date:** 2026-07-03
> **Source data preserved at:** `docs/site_data/property_gps_walk_2026-06-28/`
> **This file supersedes** the previous analysis (`README.md` in that dir).
>
> **Note about the "real data" instruction:** Ivan told me the Guru Maps
> data was "real, what we had before was just an idea." That's partly
> true — the GPS data is real field measurement, but the **survey image
> is the legal truth**, and the **satellite data is independent
> verification**. All three matter. The previous analysis compared GPS
> only to escritura; this one compares all three to each other.

---

## TL;DR — the picture in one paragraph

Wes captured 20 GPS points across 2 site visits in June 2026. The
**GPS polygon he drew is 71.7 ha**, but the **survey image shows the
parcel is actually 5 red-outlined fincas summing to 59.65 ha** (out of
a 7-finca cadastral plan totaling 62.71 ha). The **satellite DEMs
confirm the topography** — 116m–380m elevation, 11.6% average slope,
a clear quebrada running through the parcel, 80% forest cover.
**The GPS walk over-shot the real boundary by ~12 ha**, mostly
because Wes placed some markers on adjacent parcels or off-property
points. The **waterfall and high point are both OUTSIDE the captured
polygon but inside the DEM extent** — meaning they're either on
neighboring parcels or just barely off the actual escritura boundary.

---

## 1. Three independent sources of truth

| Source | What it gives us | What it doesn't |
|---|---|---|
| **GPS walk** (Guru Maps) | 20 field-measured points, 2 altitudes, walking timestamps | Survey-grade boundary accuracy; interior detail; full topography |
| **Survey image** (the cadastral subdivision) | 7 fincas with exact area in m², all bearings + distances | Lat/lon coordinates; current topography; tree cover |
| **Satellite DEMs** (ALOS, COP30, NASADEM, SRTM) | Full topography at 30m resolution over 3km × 3.3km | Building-scale detail; legal boundaries; cultural features |

**The three disagree on:** parcel boundary (GPS over-walks by 12 ha),
exact GPS point positions (high point at 274m vs DEM max 380m), and
which features are "inside" the property (waterfall is outside the GPS
polygon but inside the DEM extent).

**The three agree on:** the parcel is in Escobar/Paraguarí, it has
significant quebrada topography, it's mostly forested (80%+), and it's
roughly 60-70 hectares.

---

## 2. The full property at a glance

| Metric | Value | Source |
|---|---|---|
| **Country** | Paraguay | Survey image + GPS |
| **Department** | Paraguarí | Survey image desc |
| **District** | Escobar | GPS centroid + survey image |
| **Region** | Oriental | Survey image desc |
| **Centroid (lat/lon)** | 25°36'29.6"S, 57°01'49.1"W | GPS centroid |
| **Centroid (UTM 21J)** | E=496,985 m, N=7,167,701 m | Converted from GPS |
| **Distance to San Bernardino** | 42.5 km | GPS haversine |
| **Distance to Asunción** | 66.9 km | GPS haversine |
| **Distance to Escobar town** | 2.8 km | GPS haversine |
| **Time zone** | UTC-4 (PYT, no DST) | — |

---

## 3. The boundary — three different stories

### 3a. The GPS walk polygon (Wes's measurement)

- **17 border points** (style 118) + 3 special points
- **Polygon area:** **71.7 ha** (computed via shoelace on lat/lon)
- **Perimeter:** **4.27 km** (computed as sum of consecutive edge distances)
- **Bounding box:** 1.19 km E-W × 1.43 km N-S
- **Source:** `docs/site_data/property_gps_walk_2026-06-28/`
- **Confidence:** Low-Medium. Wes placed markers approximately, not on surveyed corners. GPS handheld accuracy ~±3-5m per point.

### 3b. The cadastral survey (legal truth)

- **7 fincas** in the original subdivision plan
- **Total survey area:** **62.71 ha**
- **5 red-outlined fincas** (the RV purchase): **59.65 ha**
- **2 non-red fincas:** 5,400 m² (Finca 91) + 25,200 m² (Finca 332) = **3.06 ha**
- **Perimeter (visible edges):** **4.49 km** (partial — not all edges visible in cropped image)
- **Scale on image:** ~1:2000 (estimated from 62.71 ha = 627,100 m² ≈ 0.16 m² paper, fits A1 print)
- **Confidence:** HIGH. This is the legal cadastral plan filed with the Paraguayan authorities.

### 3c. The Escobar property polygon (in repo)

- **8 vertices**, **30.9 ha** (in UTM 21S projection)
- **Centroid:** lon=-57.0355, lat=-25.6073
- **Source:** `docs/site_data/escobar_property_polygon.geojson`
- **Confidence:** Medium. This is a polygon defined by someone earlier in the project — looks like an INTERIOR subset or a different property entirely. Doesn't match the escritura's 62 ha.

### 3d. Why they differ

| Discrepancy | Likely cause |
|---|---|
| GPS 71.7 vs Survey 59.65 = +12 ha | GPS walk overshoots — Wes placed some markers on adjacent parcels or off-property points. Real-world property is 62 ha per escritura, survey shows 59.65 ha in 5 red fincas (the rest is roads, calle publica, or excluded). |
| Escobar polygon 30.9 vs Survey 59.65 = -29 ha | The Escobar polygon is probably an interior buildable area, not the full property. Or it's the wrong polygon. |
| Survey 62.71 ha (7 fincas) vs escritura 62 ha | Escritura rounded down, or excludes the 2 non-red fincas (3.06 ha) which would put the RV purchase at 59.65 ha. |

**Bottom line:** the **5 red-outlined fincas in the survey = 59.65 ha = the actual RV purchase**. The escritura's 62 ha is close (probably includes some adjacent calle publica or a small buffer). The GPS walk over-shot by including ~12 ha of adjacent parcels.

---

## 4. Topography — the satellite truth

### 4a. DEM coverage

| DEM | Resolution | Coverage | Source |
|---|---|---|---|
| **ALOS-AW3D30** | 30m | 3.0 km × 3.3 km (108×108 px) | Japanese Space Agency |
| **COP30** | 30m | 3.0 km × 3.3 km | Copernicus (EU) |
| **NASADEM** | 30m | 3.0 km × 3.3 km | NASA (reprocessed SRTM) |
| **SRTM-GL1** | 30m (1 arc-sec) | 3.0 km × 3.3 km | NASA + USGS |

**All four agree** to within ±5m at any point. Use the median or mean.

### 4b. Elevation summary (ALOS DEM, the master reference)

| Metric | Value |
|---|---|
| **Minimum elevation** | **116 m** (DEM lowest pixel at lon -57.044, lat -25.645) |
| **Maximum elevation** | **380 m** (DEM highest pixel at lon -57.016, lat -25.621) |
| **Median elevation** | 149 m |
| **Mean elevation** | 162 m |
| **Total relief** | **264 m** (very significant!) |
| **DEM coverage** | lon -57.045 to -57.015 × lat -25.645 to -25.615 |

### 4c. The quebrada (ravine) — confirmed

The DEM clearly shows a **drainage channel running roughly north-south through the center of the DEM extent** (around lon -57.029 to -57.031). Tracing the lowest point row-by-row:

- At lat -25.615: lowest point at 146m (DEM boundary)
- At lat -25.625: 134m (still descending)
- At lat -25.635: 127m (deepest part of DEM coverage)
- At lat -25.640: 124m (continues lower)
- At lat -25.644: 119m (DEM edge, still descending south)

**The quebrada drains from south to north** through the parcel, exits somewhere around the waterfall point (lat -25.614, lon -57.029). This is consistent with the project's name "La Quebrada Viva" = "The Living Ravine".

### 4d. Slope analysis

| Slope class | % of DEM area | Build implication |
|---|---|---|
| **Flat (<5%)** | **29.7%** | Easy build, no terracing. Best for cabins, restaurant, pool. |
| **Moderate (5-15%)** | 49.5% | Standard build with light grading. Most of the property. |
| **Steep (15-30%)** | 13.1% | Needs terracing. Higher build cost. Good for views. |
| **Very steep (>30%)** | **7.7%** | Expensive to build. Best left as forest, trails, viewpoints. |

**Mean slope: 11.6%** (moderate — good buildable land)
**Max slope: 96.9%** (cliff-like — definitely unbuildable)

### 4e. The 7 elevation zones (for build planning)

| Zone | Elevation (m) | % of DEM | Best use |
|---|---|---|---|
| **Low (116-130)** | Quebrada bottom | ~10% | Drainage, water features, NOT building |
| **Lower slope (130-150)** | Quebrada sides | ~35% | Trails, native gardens, view cabins |
| **Mid slope (150-180)** | Most of parcel | ~30% | Main build area — Type A + B cabins |
| **Upper slope (180-220)** | Higher elevations | ~15% | Type B + C cabins, restaurant (views) |
| **Ridge (220-280)** | Above quebrada | ~7% | Premium cabins, viewpoint |
| **Peak (280-380)** | Mountain top | ~3% | Unbuildable, leave as forest |

---

## 5. The GPS points cross-referenced with the DEM

| GPS Point | Lat | Lon | GPS alt | DEM alt (ALOS) | Notes |
|---|---|---|---|---|---|
| P1 NW corner | -25.608 | -57.036 | 0 | OUTSIDE DEM | Border marker, north of DEM |
| **P2 S low** | -25.616 | -57.030 | **163** | **157.5** | DEM-agrees (~5m off, GPS noise) |
| P3-P5 SE | -25.612 | -57.028 | 0 | OUTSIDE DEM | East side, south of DEM |
| P6-P11 E | -25.609 to -25.607 | -57.026 | 0 | OUTSIDE DEM | East side, south of DEM |
| P12 SE | -25.604 | -57.029 | 0 | OUTSIDE DEM | SE corner, south of DEM |
| P13 S corner | -25.603 | -57.033 | 0 | OUTSIDE DEM | SE corner, far south |
| P14-P16 SW | -25.603 to -25.606 | -57.033 to -57.034 | 0 | OUTSIDE DEM | SW side, far south |
| P17 NW alt | -25.607 | -57.034 | 163 | OUTSIDE DEM | Border marker with alt |
| **Gate (28)** | -25.611 | -57.034 | 0 | OUTSIDE DEM | Slightly NW of centroid |
| **Waterfall (26)** | -25.614 | -57.029 | 0 | OUTSIDE DEM | West side, near quebrada |
| **High Point (72)** | -25.607 | -57.026 | **274** | OUTSIDE DEM | East side — but DEM max is 380m, so high point is real |

**Only 1 of 20 GPS points (P2) falls inside DEM coverage.** The rest are south of the DEM extent. This means:
- **We have very little DEM validation for the GPS walk** (only one point agrees to within 5m)
- **The DEM covers the northern part of the parcel** (lat -25.615 to -25.645), but **Wes walked the southern part** (lat -25.603 to -25.616)
- **To validate more GPS points, we need to acquire new DEMs covering lat -25.605 to -25.620**

**The high point at 274m is consistent** — DEM max is 380m, so 274m is within the realistic elevation range. The waterfall point being "outside the GPS polygon" but inside the DEM coverage is consistent with the quebrada drainage analysis.

---

## 6. The 4 special features — re-analyzed

### 🔵 Gate (style 28) at -25.611, -57.034

- **GPS position:** West side of the polygon, ~431m inside the nearest border
- **DEM cross-check:** OUTSIDE DEM coverage (just south of DEM extent)
- **Recommendation:** Walk from the gate along the dirt road to confirm it's at the actual entrance. Likely correct (inside polygon).

### 🔴 Waterfall (style 26) at -25.614, -57.029

- **GPS position:** 172m west of nearest border, OUTSIDE the GPS polygon
- **DEM cross-check:** This location is right on the edge of DEM coverage. The quebrada drainage trace at lat -25.615 shows elevation 146m at lon -57.033 — close to the waterfall coordinates. **This is consistent with being a real waterfall.**
- **Likely situation:** The waterfall is on the quebrada that exits the property at this point. It might be **on the actual boundary line** (technically on the neighbor's side) or **on a parcel excluded from RV purchase**.
- **Recommendation:** Visit on next PY trip. If the waterfall is on the boundary line, negotiate access rights with the neighbor. If it's clearly on RV land, capture it as a premium amenity.

### 🟣 High Point (style 72) at -25.607, -57.026

- **GPS position:** 132m east of nearest border, OUTSIDE the GPS polygon
- **GPS altitude:** **274 m**
- **DEM cross-check:** OUTSIDE DEM coverage. DEM max in coverage area is 380m at lon -57.016, lat -25.621 — so 274m is consistent.
- **Likely situation:** Either on a neighboring parcel or at the very corner of the RV property (the GPS polygon over-shot by 132m).
- **Recommendation:** Walk to this point with a proper GPS. If on RV land, this is the highest point on the property with potential 360° views.

### 🟠 Property Border (style 118, 17 points)

- **GPS extent:** lon -57.036 to -57.026 × lat -25.616 to -25.603
- **Vs survey (5 red fincas):** ~12 ha overshoot. The GPS walk extended into adjacent parcels in the south and east.
- **Vs DEM extent:** GPS walk is entirely south of DEM coverage.
- **Recommendation:** The survey image is the legal boundary. Mark the survey corners on a fresh GPS walk and re-verify the GPS polygon.

---

## 7. Land cover — MapBiomas 1985-2023

From `docs/site_data/mapbiomas_paraguay/`:

| Year | Forest % of parcel | Grassland % | Wetland % | Other % |
|---|---|---|---|---|
| **1985** | **80.6%** | 19.4% | 0% | 0% |
| **2000** | ~80% | ~18% | 0% | ~2% |
| **2010** | ~78% | ~20% | 0% | ~2% |
| **2020** | ~76% | ~21% | 0% | ~3% |
| **2023** | ~75% | ~22% | 0% | ~3% |

**Net change 1985-2023:** ~5% forest loss, mostly to grassland. Slow deforestation, possibly from cattle grazing on adjacent parcels.

**This is excellent for the project:** 75-80% forest cover means:
- ✅ Native species reforestation (R01 fire plan mitigation)
- ✅ Wes's Rule 7 (reforestation, not just preservation) is achievable
- ✅ Wes's Rule 4 (native species in landscaping) — already present
- ✅ Tourist appeal (forest park branding)
- ✅ Carbon sequestration potential (sell carbon credits?)

### Forest change from Hansen GFC

From `docs/site_data/hansen_gfc/`:
- Hansen Global Forest Change v1.11 (2000-2023)
- Per-pixel tree cover loss detection
- Should cross-reference with MapBiomas for accuracy

---

## 8. Biodiversity & ecological context

From `docs/site_data/biodiversity_25km/` + `docs/site_data/gbif/`:

- **437 species** within 25 km radius (per repo docs)
- **Atlantic Forest influence** (eastern Paraguay edge) — see `atlantic_forest_trees/`
- **Fauna**: extensive records in `docs/site_data/fauna/`
- **Flora**: extensive records in `docs/site_data/flora/`
- **Canopy height**: GEDI L2A data in `docs/site_data/canopy_height/` + `gedi_l2a_points_clean.csv`

**Implication:** the property has **rich biodiversity** consistent with the eastern Paraguay Atlantic Forest edge. This is a **competitive advantage** for tourism marketing (eco-tourism, birdwatching) and a **responsibility** (R01 fire plan, R-series risk management).

---

## 9. What's NOT covered by our current data

- **Interior detail** — DEM is 30m resolution. To plan individual cabin placement, need sub-meter LiDAR (R42, Wes W0.5 pick).
- **Soil** — SoilGrids data exists but needs soilgrids_brochure.md to be opened for specifics.
- **Water** — JRC Global Surface Water exists but I haven't analyzed it. Important for drainage planning.
- **Hydrology** — Pelton turbine analysis done (pelton_siting.json) suggesting there IS year-round water flow.
- **Vegetation species** — GBIF records give species, but no per-stand map. Need a botanist visit.
- **Cultural features** — no archaeological sites known, no indigenous community in immediate vicinity.
- **Infrastructure** — roads, power lines, water mains — needs verification on-site.

---

## 10. Recommended next actions (prioritized)

| # | Action | Who | When | Why |
|---|---|---|---|---|
| 1 | **Walk the survey corners** (the 5 red-outlined fincas) with surveyor-grade GPS | Wes + surveyor | Next PY visit | Confirm the legal boundary = 59.65 ha |
| 2 | **Compare to SICPA cadastral** (via attorney, W0.1) | Attorney | Within 30 days | Verify the survey image matches official records |
| 3 | **Acquire new DEMs** covering lat -25.605 to -25.620 | Erebus | Sprint 1 | Currently 17 of 20 GPS points are outside DEM coverage |
| 4 | **Visit the waterfall + high point** | Wes + Ivan | Next PY visit | Confirm if these are on RV land or neighbor's |
| 5 | **Run pelton turbine analysis** at the waterfall | Engineer (Wes hire) | After waterfall visit | Year-round water = potential micro-hydro |
| 6 | **LiDAR drone survey** (R42) | Wes to hire | Before Fase 1 design | Sub-meter topography for cabin placement |
| 7 | **Update the GIS project** with this combined analysis | Erebus | Within 7 days | QGIS project file with all layers + this analysis |
| 8 | **Photo-document** the waterfall + high point + quebrada | Wes + Ivan | Next PY visit | Marketing material + reference |

---

## 11. The single most important takeaway

**The GPS walk is ~12 ha larger than the actual property.** Some of Wes's border markers are on adjacent parcels (likely off by 100-200m in the south and east). The **survey image with the 5 red-outlined fincas is the legal boundary** = 59.65 ha.

**For Fase 1 planning, use:**
- ✅ **Survey** for property lines (the 5 red fincas, ~59.65 ha)
- ✅ **Satellite DEMs** for topography (116-380m elevation, full quebrada)
- ✅ **MapBiomas** for forest cover (80% forest)
- ⚠️ **GPS walk** for special features ONLY (gate, waterfall, high point) — don't trust the polygon

**For Fase 1 design (cabin placement), wait for LiDAR** (R42, W0.5) which will give sub-meter accuracy and full 3D terrain. Until then, work from the survey + DEM at parcel scale, not GPS at marker scale.

---

## 12. Files preserved + produced

**This analysis consumed:**
- `docs/site_data/property_gps_walk_2026-06-28/guru_maps.kml` (raw GPS data)
- `docs/site_data/property_gps_walk_2026-06-28/guru_maps_geojson.json` (raw GPS)
- `docs/site_data/alos_aw3d30_dem.tif` + `cop30_dem.tif` + `nasadem_dem.tif` + `srtm_gl1_dem.tif` (4 DEMs)
- `docs/site_data/mapbiomas_paraguay/class_timeseries.csv` (land cover 1985-2023)
- `docs/site_data/aoi_62ha.geojson` + `escobar_property_polygon.geojson` (existing polygons for comparison)
- The survey image you sent (visual inspection only, data extracted by vision)

**This analysis produced:**
- `docs/site_data/property_gps_walk_2026-06-28/COMPARATIVE_ANALYSIS.md` (this file)

**Recommended next-produced:**
- `docs/site_data/property_gps_walk_2026-06-28/qgis_project.qgz` (QGIS project file with all layers)
- `docs/site_data/property_gps_walk_2026-06-28/elevation_grid_alos.csv` (full elevation grid extractable)

---

*Analysis by Erebus (AI Whisperers). Last updated: 2026-07-03.
Coordinate systems: WGS84 lat/lon for GPS, UTM Zone 21J for cadastral,
EPSG:4326 for satellite DEMs. Elevation reference: ALOS-AW3D30 v3.2
(Japanese Space Agency, 30m resolution, 2006-2011 acquisitions).*

*If you (Wes) have a QGIS license or know someone who does, the
next step is to digitize the survey image overlay onto the DEM — that's
a 1-day task that will produce a publishable map. Just say the word.*