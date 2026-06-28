# Post-Escritura Site Knowledge — La Quebrada Viva

> Site-knowledge package compiled **2026-06-28** (T+1 post-escritura). Combines Wesley's hand-drawn parcel polygon (shared via Google Earth on 2026-06-28) with every open-data layer we already hold for the AOI. Designed to be client-presentable as-is and to seed the conversation that will arrive with Wesley's on-site photos.
>
> Frozen escritura render bundle (SHA-256 `9ce96b8…724a53c`) untouched.

---

## 0. TL;DR

- Wesley dropped an 8-vertex polygon over the buildable northern Mbopicua cluster: **30.9 ha projected** (UTM 21S), centroid `(-57.0355, -25.6073)`. This is a **subset of the 62.57 ha legal total** (6 fincas across Mbopicua + Ybyraty); it represents the contiguous, build-relevant northern slice.
- Pin "escobar wes" at `(-57.0337, -25.6114)` elev **166.3 m AMSL** sits near the polygon's low end — almost certainly a **quebrada / stream-bottom reference**, not the ridge.
- Topography on Copernicus DEM (30 m): elevation **157.9–231.5 m**, 73.5 m relief inside the polygon, median slope **14.2 %**, **71.6 % of area faces S/SW**.
- **Buildability**: 4.28 ha unrestricted (slope < 8 %), 12.76 ha mild (8–15 %), 13.87 ha terrace-required (15–30 %), 0.09 ha unbuildable (> 30 %). The buildable headroom is real but constrained — **roughly 4 cabanas at unrestricted slope, scaling to ~12 if mild slope is permitted**.
- **Forest cover**: Sentinel-2 NDVI median **0.917**, 97.4 % of pixels above 0.6 → essentially **wall-to-wall mature Atlantic Forest**, no detected clearings, no standing water inside the polygon. Nearby GEDI shot reads **27.7 m canopy**.
- Padron match (legal title ↔ polygon) is narrowed to two candidate triples that both sum to 30.35 ha; final disambiguation needs the Catastro cadastral shapes (R02).

---

## 1. What Wesley shared

### 1.1 KML polygon — "escobar property"

- **8 vertices**, closed back to start, in `EPSG:4326`.
- **Projected area (UTM 21S, EPSG:32721)**: **30.915 ha**.
- **Centroid**: `(-57.035502, -25.607336)`.
- **Bounding box**: lon `[-57.03844, -57.02929]`, lat `[-25.61172, -25.60506]`.
- **Span**: ~920 m E–W × ~740 m N–S (roughly trapezoidal, narrowing to the south).
- Persisted at `docs/site_data/escobar_property_polygon.kml` + tooling-friendly mirror `docs/site_data/escobar_property_polygon.geojson`.

### 1.2 KML pin — "escobar wes"

- `(-57.03365675, -25.61138884)` elev **166.336 m AMSL**.
- Sits near the **southern edge** of the polygon at the **low elevation end** of the parcel.
- Reads as the kind of point an owner would drop while standing on the parcel: low ground, near the stream-line, easy access from the road.

### 1.3 Forest screenshot

- Aerial / Google Earth view of dense closed canopy — **no visible clearings, no roads through the interior, no structures**.
- Consistent with Sentinel-2 reading (NDVI 0.917 median).

---

## 2. Polygon ↔ legal title — padron hypothesis

The escritura covers 6 fincas (62.57 ha). Wesley's polygon at 30.9 ha can match at most **3 of the 6**. With only padron areas (no cadastral shapes yet), two candidate triples both sum to 30.35 ha:

| Hypothesis | Fincas | Padrones | Areas (ha) | Sum |
|---|---|---|---|---|
| **A** | 1604 + 699 + 453 | 1827 + 840 + 629 | 2.52 + 13.21 + 14.62 | **30.35 ha** |
| **B** | 1604 + 950 + 453 | 1827 + 1096 + 629 | 2.52 + 13.21 + 14.62 | **30.35 ha** |

Both hypotheses are entirely in **Mbopicua**, share fincas 1604 (the small connector) and 453 (the largest at 14.62 ha), and differ only on whether finca 699 or 950 (each 13.21 ha) is the third. Polygon area is 0.55 ha larger than the legal sum — well within DEM-projection rounding for 30 ha at 30 m resolution.

Both hypotheses **exclude finca 697** (838, 9.04 ha Mbopicua — the largest single Mbopicua piece) and **finca 298** (454, 9.97 ha Ybyraty — geographically separate from Mbopicua). Those ~19 ha live outside Wesley's polygon and are the rest of the 62.57 ha legal package.

**Action**: needs the **cadastral shapes** (Catastro, or Anexo I rumbos/linderos) to disambiguate A vs B. Until then, treat the polygon as "the contiguous buildable Mbopicua cluster ~30 ha; remaining ~32 ha is split between the larger isolated Mbopicua piece and the Ybyraty parcel."

---

## 3. Topography — what the parcel looks like under the canopy

Computed against the **Copernicus DEM (COP30)** clipped to the extended AOI (the original AOI bbox cut off the polygon — re-fetched into `docs/site_data/extended_aoi/`).

### 3.1 Elevation envelope (inside polygon, ~360 cells)

| Stat | Value |
|---|---|
| Min | 157.9 m |
| P25 | 184.7 m |
| Median | 199.1 m |
| P75 | 213.4 m |
| Max | 231.5 m |
| **Relief** | **73.5 m** |

Wesley's pin at 166.3 m sits at roughly **P4** — almost at the bottom of the parcel. That's a strong tell that the pin marks the **stream / quebrada-side access point**, not a building site or the ridge.

### 3.2 Slope distribution (% grade)

| Stat | Value |
|---|---|
| Median | 14.2 % |
| P75 | 18.9 % |
| P90 | 23.0 % |
| Max | 30.2 % |

**Buildability classes**:

| Class | Slope range | Area (ha) | % of polygon |
|---|---|---|---|
| **Flat (unrestricted)** | 0–8 % | **4.28** | 13.8 % |
| **Mild (light grading)** | 8–15 % | **12.76** | 41.2 % |
| **Terrace-required** | 15–30 % | **13.87** | 44.8 % |
| Unbuildable | > 30 % | 0.09 | 0.3 % |

Reads as **classic quebrada rolling terrain**: a small share of true flat ground, lots of working slope. **Phase-1 cabanas (4–6 units) fit comfortably in the 4.28 ha flat band** with siting headroom to spare. Pushing to a larger Phase-2/3 program would need terracing on the 13.87 ha mid-band — buildable, just with capex on stone retaining walls (already in the LQV vernacular).

### 3.3 Aspect (which direction slopes face)

| Direction | % of polygon |
|---|---|
| S | 38.4 % |
| SW | 33.2 % |
| E | 12.1 % |
| NE | 5.5 % |
| W | 5.0 % |
| SE | 4.2 % |
| NW | 1.4 % |
| N | 0.2 % |

**71.6 % of the polygon faces S/SW**. In the southern hemisphere those are the **cool, sun-averted faces** — better thermal comfort for buildings (passive cooling friendlier in 35 °C summers), but **suboptimal for PV array siting**. PV should target the 17.6 % E/NE faces (sunrise-side, gets the morning sun before peak heat). Concentrate guest sleeping rooms on S/SW; concentrate the energy plant and the corredor's daytime social zone where it can catch the morning sun.

### 3.4 Quicklook

Three-panel summary map at `docs/site_data/extended_aoi/polygon_quicklook.png`:
1. Elevation + hillshade with polygon overlay and pin.
2. Buildability classes coloured (flat/mild/terrace/no-go).
3. Text panel: key stats, slope/aspect/buildability tables, cross-references.

---

## 4. Forest cover, water, surface materials

### 4.1 Sentinel-2 L2A (2026-05-12, late austral autumn, 1.8 % cloud)

Inside the polygon (3,270 cells on 10 m bands, polygon reprojected to UTM 21S):

| Metric | Value | Reading |
|---|---|---|
| **NDVI median** | **0.917** | Mature closed-canopy forest |
| **NDVI P25 / P75** | 0.890 / 0.937 | Very tight — uniformly forested |
| **Pixels with NDVI > 0.6** | **97.4 %** | Forest cover wall-to-wall |
| **Pixels with NDVI < 0.2** | **0.0 %** | No bare soil / no built surfaces |
| **NDWI (McFeeters) > 0** | 0.0 % | **No open water surface** detected |

**What this means for the client**: Wesley's polygon is **virtually 100 % closed-canopy Atlantic Forest** as of 2026-05-12, with **no detected clearings, no built structures, no open water**. The forest is real, recent, and dense. There is no "field" inside this polygon to subdivide — every cabana built here is a tree-canopy clearing decision. Restoration narrative is *defensible*; the project starts from intact canopy, not degraded land.

### 4.2 GEDI L2A spaceborne LiDAR

- **0 shots inside the polygon** (small target, sparse GEDI sampling).
- **1 nearby shot ~500 m SW**: canopy height **27.7 m**.
- LQV-wide GEDI canopy distribution (cleaned, 25 shots): median **25.3 m**, range 18.9–80 m (80 m tail is sensor saturation).

Reading: emergent canopy on Wesley's polygon is consistent with **mature secondary Atlantic Forest**, ~25–28 m tall, with the usual lapacho / cedro / mango hero-tree distribution.

### 4.3 OSM / GIS context (already on file)

- `docs/site_data/osm/` holds buildings, roads, water, places, POIs for the AOI.
- Cross-checked: the OSM road network does **not** pass through Wesley's polygon — closest road runs to the south, consistent with the pin being the access point.

---

## 5. Climate envelope (ERA5 1990–2025, project center)

Already integrated in the LQV climate brochure; re-stated here for the client deliverable:

| Metric | Value |
|---|---|
| Annual mean temp | **22.0 °C** |
| Annual precip | **1,736 mm/yr** (range 1,172–2,509) |
| Warmest month | Jan, 26.8 °C |
| Coolest month | Jul, 16.6 °C |
| Wet months (> 100 mm) | 10 of 12 |
| Dry months (< 50 mm) | none |
| Peak solar | Dec, 24.3 MJ/m²/day |
| Windiest month | Aug, 1.5 m/s |
| Köppen | **Cfa humid subtropical** |

**Design rule 6 (passive cooling up to ~35 °C) holds**: warmest monthly mean is 26.8 °C, well within the passive-cooling band. AC is supplementary only.

Dengue / standing-water risk is real (Cfa wet, wet 10 months/yr). The "no standing water" design rule is non-negotiable; cistern stainless-mesh seals carry over directly.

---

## 6. What we **don't** know from open data — and which client photos close it

| Gap | Why open data can't tell us | What a photo closes |
|---|---|---|
| **Stream presence + flow** | NDWI saw no open water — but canopy shadows the stream from satellite. We can't confirm year-round flow vs ephemeral. | Photos of the actual quebrada at the low end (~166 m elevation, near the pin) — wet/dry sections, width, bed material |
| **Existing structures** | NDVI saw no clearings, but a small cob/timber house under canopy is invisible to 10 m S-2. | Any standing structures, ruins, foundations, prior owner's improvements |
| **Road / access** | OSM shows the nearest road south of the polygon. Internal trails not mapped. | The actual driveway, gate, internal paths, vehicle access points |
| **Terrace edges + escarpment** | DEM at 30 m flattens sharp drops < ~3 m. A 2 m sandstone bench reads as smooth slope. | Photos of any escarpments, natural terraces, exposed bedrock, boulder fields |
| **Plant species ID** | Sentinel-2 sees "forest"; we can't ID lapacho vs cedro vs mango from spectra alone. | Close-ups of dominant tree species — bark, leaves, fruits, flowers if any |
| **View corridors** | DEM tells us elevation; the satellite tells us canopy density. We can't tell from above which directions have *cleared sightlines* through the canopy. | Photos taken from candidate cabana sites looking outward |
| **Existing infrastructure** | Open data has no electric/water hookups. | Power poles, water meters, well-heads, septic, fence lines |
| **Stone / soil texture** | DEM gives slope, not lithology. | Exposed rock, soil colour, dug pits if any |
| **Neighbouring activity** | OSM places nearby. Adjacent fincas' use (pasture, plantation, forest) not visible. | Photos of property edges and what's on the other side |
| **Microclimate signals** | ERA5 grid is 25 km; we don't see cool-air drainage, frost pockets, fog lines. | Morning / evening photos showing fog, dew patterns, where it's coolest |

**Pre-staged intake folder**: `docs/site_data/client_photos/2026-06_post_escritura/` (created next, Task #6).

---

## 7. Open-data inventory used to build this brief

| Layer | Source | Resolution | Status |
|---|---|---|---|
| Wesley's polygon | KML 2026-06-28 | 8 vertices | `docs/site_data/escobar_property_polygon.{kml,geojson}` |
| DEM (canonical) | Copernicus GLO-30 | 30 m | `docs/site_data/extended_aoi/cop30_dem.tif` |
| DEM A/B | ALOS AW3D30 (JAXA) | 30 m | `docs/site_data/extended_aoi/alos_aw3d30_dem.tif` |
| DEM A/C | SRTM v3 GL1 | 30 m | `docs/site_data/extended_aoi/srtm_gl1_dem.tif` |
| DEM A/D | NASADEM | 30 m | `docs/site_data/extended_aoi/nasadem_dem.tif` |
| Slope (derived) | numpy.gradient on COP30 | 30 m | `extended_aoi/cop30_slope_pct.tif` |
| Aspect (derived) | numpy.gradient on COP30 | 30 m | `extended_aoi/cop30_aspect_deg.tif` |
| Sentinel-2 L2A | `S2B_21JVM_20260512_0_L2A` | 10 m (vis/NIR) | `docs/site_data/sentinel2/` |
| GEDI L2A canopy | NASA, 27 granules | 25 m footprints | `docs/site_data/gedi_l2a_points_clean.csv` |
| ERA5 climate | Copernicus, 1990–2025 | 0.25° monthly | `docs/site_data/climate_era5/` |
| OSM context | Overpass, AOI clip | vector | `docs/site_data/osm/` |
| Quicklook map | this analysis | 1200×800 | `extended_aoi/polygon_quicklook.png` |

Original AOI bbox (`docs/site_data/aoi_62ha.geojson`, north `-25.615`) **cut off ~364 m of the polygon's northern edge**. Extended AOI (`docs/site_data/aoi_62ha_extended.geojson`, north `-25.595`, schema 1.1) added 2.2 km north and now contains the polygon. The frozen escritura bundle (commit `85e86aa`, SHA-256 `9ce96b8…724a53c`) is **untouched** — original AOI + DEMs preserved byte-identically; the extended set lives in a parallel directory.

---

## 8. Cross-references

- `docs/site_data/satdata_brief.md` — the satdata reader the render pipeline was built against. This doc is the **client-facing companion** with Wesley's polygon as the new anchor.
- `docs/contract_summary.md` — 6 fincas table, prices, seña, escritura timing.
- `docs/MASTER_BRIEF.md` — overall LQV master brief.
- `docs/RESEARCH_GAPS.md` — R02 (Anexo I / cadastral shapes) is the explicit unblock for the padron-hypothesis disambiguation (§2 above).
- `docs/CLIENT.md` — Wesley + Thijs ownership context.
- `docs/site_data/aoi_62ha_extended.geojson` — extended AOI bbox (schema 1.1) used for all rasters in `extended_aoi/`.
- `docs/site_data/extended_aoi/polygon_quicklook.png` — 3-panel quicklook map.

---

*Compiled 2026-06-28 (T+1 post-escritura) by AI Whisperers. Frozen escritura render bundle untouched. Next: wire client photo intake folder + index template, then update RESEARCH_GAPS with photo-driven gap closures.*
