# Land + Parcel

**Sources:**
- Ivan's LQV repo (62 ha Escobar, Paraguarí)
- LQV render pipeline + ALOS DEM + Sentinel-2 + GEDI data
- Escritura `0081129` (signed 2026-06-27)
- LQV tag `escritura-2026-06-27`

**Date:** 2026-06-30
**Status:** Ivan's data is from earlier work. Wes needs to confirm + add specific data from his own working files.

---

## 1. What's Confirmed (from LQV repo + escritura)

| Field | Value | Source |
|---|---|---|
| Land size | **62 ha** | LQV repo, prior work |
| Location | **Escobar, Paraguarí, Paraguay** | LQV repo, prior work |
| Centroid (approx) | ~26°36'S, 56°51'W (Paraguarí region) | LQV repo |
| Distance from Asunción | ~120 km SE | LQV repo |
| Ownership | **Wesley van de Camp + Thijs 75/25** | escritura `0081129` |
| Escritura status | **Signed 2026-06-27** | LQV tag `escritura-2026-06-27` |
| Topography | Mixed: 116-380m elevation, ~80% buildable, 264m relief | LQV `docs/site_data/SITE_DIAGNOSTIC.md` |
| Existing water | Stream + creek through the parcel | LQV render `lqv/site/stream.py` |
| Existing road access | Last 7km dirt road from main route | LQV `docs/site_data_spike.md` |
| Climate | Sub-tropical, wet season Nov-Mar, dry May-Oct | LQV `docs/site_data/climate_era5/` |
| Soil (regional) | Red laterite, sandy loam, well-draining | LQV `docs/site_data/SITE_DIAGNOSTIC.md` |
| Vegetation | Atlantic Forest edge (mature canopy up to 74m) | LQV `docs/site_data/` |

---

## 2. What's NOT Yet Confirmed (gaps Wes needs to fill)

| Field | Status | Action |
|---|---|---|
| Exact centroid coordinates (lat/lon) | LQV has approx | Confirm from escritura |
| Property boundaries (exact polygon) | LQV has KML | Verify with surveyor |
| Topographic survey (cm-accurate) | Not done | Phase 1 infra task |
| Soil tests (load-bearing) | Not done | Phase 1 infra task |
| Water table depth | Not tested | Phase 1 infra task (well drilling) |
| Mineral rights (sub-soil) | TBD | Check escritura |
| Forest cover % | ~82% canopy (Hansen GFC) | Verify on-ground |
| Adjacent land ownership | TBD | Wes can ask neighbors |
| Zoning restrictions | TBD | Municipalidad de Escobar visit |
| Indigenous/community rights | TBD | INDI survey |

---

## 3. Ivan's Render Pipeline Outputs (already done)

Ivan has built a 3D render of the site using:

- **ALOS DEM** (30m resolution, free) — elevation
- **Sentinel-2 L2A** (10m optical, free) — vegetation, NDVI
- **GEDI L2A** — canopy height (with some data quality issues, see LQV `docs/site_data/SITE_DIAGNOSTIC.md`)
- **OSM Overpass** — buildings, roads, water features (within 5km radius)
- **Hansen GFC** — forest cover change 2001-2024 (82% canopy, 0.63 ha loss 2001-24)
- **JRC Global Surface Water 1984-2021** — water bodies
- **MapBiomas Paraguay 1985-2023** — land cover
- **MOD11A2 1km LST 2015-2024** — temperature
- **ERA5 1990-2025** — climate
- **SoilGrids 2.0** — soil pH, OC, clay, sand, silt, BD at 3 depths
- **GBIF 25km** — biodiversity records
- **iNat 5km** — plant observations
- **Meta CHM 1m** — canopy height (at 6 sample points)

**Outputs:**
- 3D terrain model: `docs/site_data/dem/` (ALOS + 30m DEM)
- Canopy classification: `docs/site_data/canopy_classes.geojson` (4 NDVI bins, 61 polygons)
- Hydrography: `docs/site_data/hydrography_dem.geojson` (15 stream segments)
- Biodiversity: `docs/site_data/gbif_-25.6073_-57.0355_30km.csv` (300 records)
- Site diagnostic: `docs/site_data/SITE_DIAGNOSTIC.md` (full summary)
- 62-ha digital twin render: `lqv/subscene/terrain_62ha.py` (18 hero renders shipped)

---

## 4. The 3DGS Pipeline (Ivan's WIP)

Wes's 5 phone videos → COLMAP → gsplat → 3DGS model → Three.js viewer

**Status:** Pipeline ready (Vast.ai + COLMAP + gsplat + Three.js viewer). Blocked on Wes's captures.

**If Wes delivers the captures, this gives:**
- High-fidelity 3D model of the actual quebrada
- Visual reference for Phase 1 cabin placement
- VR walkthrough for investors before any cabin is built
- Base for the buyer-experience stack (B01, B04)

**See:** `docs/ideas/buyer_experience/b07_phone_capture_pipeline_(luma_self-host).md`

---

## 5. Critical Open Items (Wes action)

### Before Phase 1 infra can start:

1. **Topographic survey** — geodesist quote (~$2-5k)
2. **Soil tests** — load-bearing + drainage + contamination
3. **Well drilling quotes** — 50/100/150m depth options
4. **ANDE office visit** — 3-phase upgrade quote for Phase 1 load
5. **Municipalidad de Escobar visit** — permits + zoning confirmation
6. **MADES environmental permit** — required for water extraction + wastewater discharge
7. **Insurance broker quotes (3)** — for completed infrastructure (per Insight #3)
8. **Boundary verification** — exact property lines, adjacent owners

### Before Phase 1 cabin build can start:

1. **Cabin placement decision** (B02 + B03 + S06) — where do the 30 cabins go?
2. **Road + utility routing** — from main entry to each cabin cluster
3. **Master cabin placement plan** — including the 6 different style clusters

### Before first guest can book:

1. **Permits + insurance** — binding
2. **Manager + staff hired** — 27 staff per the model
3. **Cuisine + activity programming** — fleshed out
4. **Booking system** — direct + OTA integration
5. **Photos + video** — for marketing

---

## 6. Cross-Reference: LQV Site-Specifics Catalog

Ivan's LQV catalog has 7 site-specifics ideas:
- S01: Cabernet village concept (clustered houses)
- S02: Eco positioning (NOT "ecopark" — politically loaded)
- S03: Locate depot on terrain
- S04: Moestuin piketten with GPS
- S05: Water drainage locations
- S06: Locate 13 typology-house positions (via VR + site vision)
- S07: Neighbors selling higher ground (research)

**See:** `docs/ideas/site_specifics/` (7 ideas, 12-section format)

---

## 7. Source

- **Ivan's site data:** `docs/site_data/` (full ALOS + Sentinel-2 + GEDI corpus)
- **Ivan's render pipeline:** `lqv/subscene/terrain_62ha.py` + `lqv/site/` modules
- **Ivan's terrain_62ha_photoreal:** `lqv/subscene/terrain_62ha_photoreal.py` (v5, with sat imagery)
- **Escritura:** `escritura-2026-06-27` tag, `0081129` commit
- **LQV render catalogue:** `docs/render_catalogue/` (926 renders, 53 assets)

**Tracked in:** LQV catalog `docs/ideas/site_specifics/` (7 ideas)
