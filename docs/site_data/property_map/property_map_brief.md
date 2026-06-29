---
name: property_map_brief
description: Composite property map v1 (2026-06-28) over the 30.9 ha Mbopicua polygon — Wesley's KML boundary + Sentinel-2 NDVI 4-class canopy (10 m, single-date 2026-05-12) + Copernicus 30 m DEM D8 hydrography (15 LineStrings, threshold ≥30 cells) + OSM buildings (9 polygons all south of polygon, 0 on-property) + Camino a Escobar road + 2 farmland polygons + NDWI=0 % open water + 14-row photo-verification register.
metadata:
  type: project
---

# Property map brief — La Quebrada Viva (Phase-0 §12 v1, canonical)

> Composite satellite + DEM + OSM map of the 30.9 ha buildable Mbopicua
> cluster (Wesley's KML polygon, scope-locked at T+1, 2026-06-28).
> Frozen at 300 dpi as `property_map.png` and packaged as the v1 baseline
> from which the [[property_map_v2_brief]] data spine derives. All
> layers are remote-sensed; ground-truth via Wesley's 2026-07-27 →
> 2026-08-27 intake window. Canonical reference for the deck "Where the
> 30.9 ha sit" pair + the digital-twin Mbopicua mesh AOI.

## Headline

- **Polygon scope-locked** to the **30.9 ha Mbopicua cluster** from Wesley's KML — the buildable subset of the 62 ha boleto-privado purchase. Polygon is the canonical AOI for every downstream brief and sub-render.
- **Zero on-property structures** per OSM Overpass + MS Open Buildings ML pass. The nearest neighbour building sits ~196 m S of the polygon centroid (17 m² shed-scale, untagged); all 9 OSM-mapped buildings cluster along `Camino a Escobar` south and SE of the polygon.
- **Zero open water inside the polygon** at 10 m S-2 single-date snapshot (NDWI median −0.83, 0 % open-water bins). Triple-confirmed by [[sentinel1_brief]] VV = −8.33 dB and [[jrc_gsw_brief]] zero polygon cells across 1984-2021 — see Cross-check.
- **Canopy is dense and continuous** — 4-class S-2 NDVI surface, single date `S2B_21JVM_20260512_0_L2A` (2026-05-12 autumn mid-flush). The bare/sparse classes hug the SW boundary along the stream corridor; the mid/dense bins cover the interior. Cross-confirms [[hansen_gfc_brief]] 82.1 % treecover2000 + [[mapbiomas_paraguay_brief]] 80.6→84.0 % native forest gain.
- **15 stream LineStrings** entering N/NE and exiting SW low corner, derived from Cop30 D8 flow-accumulation at threshold ≥30 cells (~2.7 ha catchment). All segments are DEM-derived, classed *permanent vs seasonal* only by joint inference from [[sentinel1_brief]] VV ratio + [[jrc_gsw_brief]] zero-water — never photo-confirmed. R01 (photo + EXIF-GPS) gates classification per segment.
- **Camino a Escobar** is the only OSM road, `highway=unclassified, surface=unpaved`, 2-lane dirt, running E-W along the southern polygon margin. Two `landuse=farmland` polygons sit SW of the polygon — neighbour pasture, not on-property.
- **Individual tree positions are NOT shipped.** R35 (drone LiDAR or sub-1 m NICFI + DeepForest) gates the candidate-to-stem promotion; the 86-species candidate list lives in [[atlantic_forest_trees_brief]].

## Pull parameters

| Field | Value |
| --- | --- |
| Polygon source | Wesley van de Camp's KML, hand-digitized 2026-06-27 from boleto cadastral overlay |
| Polygon area | 30.9 ha (Mbopicua cluster — buildable subset of 62 ha boleto purchase) |
| Polygon CRS (vector) | EPSG:4326 |
| Composite raster CRS | EPSG:32721 (UTM 21S) |
| Sentinel-2 scene | `S2B_21JVM_20260512_0_L2A` (Element84 Earth Search STAC) |
| S-2 acquisition date | 2026-05-12 (autumn / *otoño* mid-flush, single-date snapshot) |
| S-2 resolution | 10 m B02/B03/B04/B08 → NDVI / NDWI |
| NDVI bins | 4 classes: bare (<0.30), sparse (0.30-0.60), mid (0.60-0.85), dense (>0.85) |
| NDWI water threshold | 0 (no polygon cells positive) |
| DEM source | Copernicus 30 m GLO-30 via OpenTopography API (`OPENTOPOGRAPHY_API_KEY` in `.env.local`) |
| Hydrography algorithm | D8 flow-direction + flow-accumulation, threshold ≥30 cells (~2.7 ha catchment) |
| Hydrography output | 15 LineStrings, EPSG:4326 |
| OSM Overpass query | `building=*`, `highway=*`, `landuse=*`, `natural=*` within polygon bbox + 2 km buffer |
| OSM pull date | 2026-06-28 |
| OSM building count | 9 polygons (all S of polygon, none inside) |
| OSM road | 1 LineString — `Camino a Escobar` (`highway=unclassified, surface=unpaved`) |
| OSM farmland | 2 polygons (SW of polygon) |
| Composite output | `property_map.png`, 300 dpi |
| Driver | `scripts/build_property_map.py` |
| Pure-numpy helper | `scripts/analyze_stream.py` (D8 flow-routing, shared with hydrography sub-render) |

## Layer manifest — what shipped in v1

| Layer | Files | Status | Confidence |
| --- | --- | --- | --- |
| Polygon boundary | `vector/property_polygon.geojson` | ✅ canonical (Wesley KML) | High |
| Canopy classes (4-bin NDVI) | `raster/canopy_classes.tif` + `quicklooks/canopy_classes.png` | 🛰️ derived | Mid (autumn single-date) |
| Hydrography (D8 streams) | `vector/hydrography_dem.geojson` + `quicklooks/hydrography_dem.png` | 🛰️ derived | Mid (DEM-only, no photo) |
| Open water (NDWI) | `raster/ndwi.tif` + `quicklooks/ndwi.png` | 🛰️ derived | High (cross-confirmed S1+JRC) |
| Buildings (OSM) | `vector/buildings_osm.geojson` | 🛰️ partial | Low (OSM coverage is sparse) |
| Buildings (ML) | deferred to [[infrastructure_brief]] | 🛰️ deferred | n/a |
| Road | `vector/roads_osm.geojson` | 🛰️ derived | Mid |
| Farmland (neighbour) | `vector/natural_osm.geojson` (landuse subset) | 🛰️ derived | Mid |
| Individual trees | NOT shipped | 📷 deferred R35 | n/a |
| Composite render | `property_map.png` (300 dpi) | ✅ frozen | High (geometry) |
| Photo verification register | `photo_verification.md` (14 rows) | 🛰️ pending photos | n/a |

## Cross-check with other briefs

| Source | Claim | property_map agrees? |
| --- | --- | --- |
| [[sentinel2_brief]] | NDVI floor 0.728 wall-to-wall 2020-2025, single-date 2026-05-12 mean +0.917 | Yes — canopy_dense + canopy_mid bins cover >90 % polygon interior; sparse/bare classes restricted to SW stream corridor |
| [[sentinel1_brief]] | VV −8.33 dB, VH −14.09 dB, VV−VH +5.76 dB closed-canopy signature, no flooded patches | Yes — radar rules out open water under canopy that NDWI single date cannot see |
| [[jrc_gsw_brief]] | Zero polygon cells with any water occurrence 1984-2021 across all 4 layers | Yes — historical surface-water absence over the full Landsat era; the NDWI 0 % single-date claim is now era-wide |
| [[hansen_gfc_brief]] | 82.1 % treecover2000 mean; 0.63 ha cumulative loss 2001-2024; 0 gain | Yes — the canopy_dense + canopy_mid bins corroborate the 82 % baseline; the SW stream-corridor sparse/bare zone aligns with the 4-event Hansen loss footprint |
| [[mapbiomas_paraguay_brief]] | Native forest 80.6 % (1985) → 84.0 % (2023), Δ +3.4 pp; 297 stable-forest px | Yes — canopy bins reflect the persistent dense-forest mosaic Mapbiomas tracked back to 1985 |
| [[landsat_brief]] | 41-yr NDVI mean +0.696, peak +0.782 in 2024 | Yes — single-date 2026-05-12 NDVI mean +0.917 is consistent with the 2024 peak and the recent 5-yr greening trend |
| [[hydrogeology_brief]] | Dry-channel signature on the SW corridor at the time of survey | Yes — DEM streams are real geomorphic channels but flow seasonally; sparse/bare canopy bins along the corridor reflect intermittent scouring |
| [[gbif_brief]] | 50 dense-canopy avian species, 0 mammals (sampling artefact) | Consistent — closed-canopy habitat predicted by canopy_dense + canopy_mid bins |
| [[client_photos_brief]] | 14-row shot register at `client_photos/2026-06_post_escritura/index.md` rows 4-17 | Yes — `photo_verification.md` enumerates the 1-to-1 cross-ref for every derived feature in v1 |
| [[infrastructure_brief]] | MS Open Buildings: 737 polygons / 59 947 m² in AOI ±1 km, nearest 196 m S | Yes — extends OSM's 9 polygons with the ML pass; both confirm 0 on-property structures |
| [[atlantic_forest_trees_brief]] | 86 candidate species within 25 km; *Trichilia catigua* 61 occ, lapacho 1 occ | Compatible — the canopy_dense bins are the spatial substrate over which the species candidate list could resolve at sub-1 m |

## Engineering implications

- **The polygon is the canonical AOI for every downstream Phase-1 deliverable** — siting, layout, viewshed, drainage, restaurant placement, cabin clusters. All sub-renders inherit the boundary from `vector/property_polygon.geojson`. Never re-digitize from the 62 ha boleto; the 30.9 ha buildable cluster is the scope-lock.
- **Buildings: 0 on-property, 9 OSM south, 737 ML in the AOI ring.** Phase-1 site layout starts from a clean slate; no demolition, no relocation, no respect-existing constraints inside the polygon. Wesley's photo intake (shot-list rows 11-12) gates a definitive "vacant" claim — if any photo turns up an untagged shed, cabin, gate-house or pump-house, the v1 composite gets a `photo_anchored.geojson` extension layer at promotion time.
- **Surface water: triple-zero (S2 NDWI + S1 VV + JRC 1984-2021).** The Phase-1 designed water feature (pool / pond / salto enhancement) is a **green-field design**, not a historical restoration. No regulatory complication around modifying a pre-existing wetland under MADES wetlands protection (the polygon is non-wetland under the historical 30 m record). Designed-feature siting is free; downstream of [[hydrogeology_brief]] flow-routing for catchment.
- **Streams: 15 D8 LineStrings, threshold ≥30 cells.** This is a DEM-derived approximation, not a photo-confirmed channel network. Per-segment permanence requires (a) wet-vs-dry-season S-1 SAR comparison (Tier-0 free, gated on dry-season Sentinel-1 pull) + (b) photo + EXIF-GPS at the salto axis + footbridge crossings (shot-list rows 9-10, 16). Until then, classify all 15 segments as **seasonal/ephemeral** for legal claims, **permanent** only when joint S-1 dry-season VV stays below −15 dB.
- **Camino a Escobar is the only access** — Phase-1 internal access tracks (shot-list row 17) are invisible to OSM and to 10 m Sentinel-2. Drone SfM at 5-10 cm GSD (Tier-1 unlock) or NICFI 4.77 m basemaps (Tier-0, user-side signup) are the only paths to a per-track polyline before the photo intake.
- **Canopy classes are an autumn-mid-flush single-date snapshot.** The 4-bin NDVI surface is the *spatial pattern* at one moment, not the long-term mean. For multi-decade canopy claims defer to [[landsat_brief]] (41 yr) + [[mapbiomas_paraguay_brief]] (39 yr) + [[hansen_gfc_brief]] (24 yr). For seasonal canopy dynamics defer to the S-2 timeseries 2020-2025 (12 scenes) summarized in [[property_map_v2_brief]] §I.
- **Cross-CRS bookkeeping is the failure mode.** All vectors are EPSG:4326; rasters and composite are EPSG:32721 (UTM 21S). Any new layer must explicitly re-project on read or write; the `scripts/build_property_map.py` driver enforces this at composite time. New sub-renders inheriting from this brief MUST set `cam.data.clip_end >> 100 m` (parcel scale) per [[feedback_subscene_clip_end]].
- **For the Wesley-side deck**, the property_map composite is the *only* page that lets a non-engineer see all 8 layers stacked on the polygon at once. It's the cognitive anchor; every other brief reads as detail-of-detail. Keep `property_map.png` at 300 dpi and the 8-row TL;DR table prominent.

## Sub-render typology

- `lqv/subscene/property_canopy_classes.py` — polygon outline + 4-bin NDVI ramp (yellow→dark-green) over the 32721 raster; canonical "what's growing where" page.
- `lqv/subscene/property_hydrography.py` — polygon outline + 15 D8 LineStrings + NDWI heat as backdrop; load-bearing "no open water + DEM streams" infographic.
- `lqv/subscene/property_neighbour_buildings.py` — polygon outline + 9 OSM buildings + 737 MS Open Buildings (semitransparent) + 196 m nearest-neighbour annotation; addresses "no on-property structures" claim.
- `lqv/subscene/property_road_and_landuse.py` — polygon outline + `Camino a Escobar` + 2 farmland polygons + landuse fill; addresses "neighbour land use" claim (shot-list row 14).
- `lqv/subscene/property_composite.py` — driver-level orchestrator producing the canonical `property_map.png` at 300 dpi (re-emits v1 baseline byte-for-byte until v2 rolls).
- `lqv/subscene/property_photo_overlay.py` — DEFERRED until photo intake; will plot EXIF-GPS waypoints over the v1 composite once the 14-row register flips 🛰️ → ✅.
- `lqv/subscene/property_individual_trees.py` — DEFERRED until R35 (drone LiDAR) or NICFI + DeepForest unlock; will plot per-stem polygons with species ID from the [[atlantic_forest_trees_brief]] candidate pool.

## Provenance

- **Wesley KML polygon:** hand-digitized 2026-06-27 from boleto cadastral overlay; canonical scope-lock recorded in [[decisions_log]] 2026-06-28.
- **Sentinel-2 scene:** `S2B_21JVM_20260512_0_L2A` pulled from Element84 Earth Search STAC, no auth, B02/B03/B04/B08 bands → NDVI + NDWI computed in `scripts/build_property_map.py`.
- **Copernicus GLO-30 DEM:** OpenTopography REST `globaldem` endpoint, AOI bbox, API key `OPENTOPOGRAPHY_API_KEY` in `.env.local` (never committed).
- **D8 hydrography:** pure-numpy implementation in `scripts/analyze_stream.py`, shared between hydrography sub-render and v1 composite driver. Threshold ≥30 cells (≈2.7 ha catchment) chosen to surface the salto-axis tributaries without flooding the map with rills.
- **OSM Overpass:** API call dated 2026-06-28, polygon bbox + 2 km buffer, `building=*` / `highway=*` / `landuse=*` / `natural=*` selectors. No auth.
- **Composite render:** `scripts/build_property_map.py` → matplotlib 300 dpi → `property_map.png`. Reproducible from scratch given the KML + the API keys + the OSM Overpass mirror state on 2026-06-28.
- **License:** All inputs CC-BY-4.0 or public domain (Wesley KML is internal). Composite output inherits the most-restrictive upstream (CC-BY-4.0 — citation in [[license_obligations]]).

## Carry-forward gaps

- **R01 (stream permanence)** — per-segment classification of the 15 D8 LineStrings as permanent / seasonal / ephemeral. Gated on (a) dry-season Sentinel-1 SAR pull (Tier-0 free) + (b) EXIF-GPS photo at salto + footbridge + boundary crossings (shot-list rows 9-10, 16).
- **R35 (individual trees)** — per-stem polygons with species ID. Gated on drone LiDAR + ALS (Tier-3 paid, ~$4-9 k) OR NICFI 4.77 m + DeepForest (Tier-1 free, user-side NICFI signup).
- **Photo-anchored layer** — once Wesley's 2026-07-27 → 2026-08-27 intake window closes, the 14-row register at `photo_verification.md` flips status; any untagged on-property structures, salto features, or internal access tracks become a new `vector/photo_anchored.geojson` layer that re-renders into the composite.
- **v2 baseline** — [[property_map_v2_brief]] is the indexed data spine pulled from this v1 baseline. It adds 41-year Landsat NDVI history, 6-month S1 SAR, multi-decade Mapbiomas + Hansen forest tracking, triple-confirmed water absence, SoilGrids profile, 86-species Atlantic Forest pool, 25 km biodiversity envelope, MS Open Buildings reach, and 50 km comparables ring. v1 stays canonical for the polygon-clip composite PNG.
- **Drone SfM at 5-10 cm GSD** — replaces both the Cop30 DEM hydrography and the OSM road as the high-LOD on-property surface model. Aligns with the user's LOD directive (high LOD on-property, lower LOD on surroundings). Tier-1 unlock, user-side drone flight or contractor.
- **Mapillary streetside imagery** — along `Camino a Escobar` for the boundary-eye-level view; token gated on user-side signup. Listed in [[deferred_data]].
- **Internal track polylines** — invisible to all current sensors; only photo intake (shot-list row 17) or drone SfM resolves.

## Cross-references

- [[property_map_v2_brief]] — indexed v2 spine with 13 batches (A-K‴), 86-species pool, 437-species biodiversity envelope, MS Open Buildings reach.
- [[sentinel2_brief]] — single-date scene + 6-yr timeseries underpinning canopy classes + NDWI.
- [[sentinel1_brief]] — 14-scene RTC γ⁰ VV/VH confirming closed-canopy + no flood patches.
- [[landsat_brief]] — 41-yr 30 m NDVI history giving the multi-decade canopy floor.
- [[jrc_gsw_brief]] — 1984-2021 surface-water zero-confirmation across all 4 JRC layers.
- [[hansen_gfc_brief]] — 24-yr treecover2000 baseline + stand-replacement loss tally.
- [[mapbiomas_paraguay_brief]] — 39-yr land-cover trajectory + native-forest gain.
- [[canopy_height_brief]] — Meta CHM 1 m mean 10.9 m canopy height (corroborates closed-canopy bins).
- [[hydrogeology_brief]] — flow-routing context for the 15 D8 stream LineStrings.
- [[infrastructure_brief]] — MS Open Buildings + OSM building extension to the 9-polygon OSM set.
- [[atlantic_forest_trees_brief]] — 86-species candidate pool that resolves to per-stem at sub-1 m.
- [[biodiversity_25km_brief]] — GBIF 437 spp + iNaturalist 727 obs + 0 IUCN-threatened in the 25 km envelope.
- [[comparables_brief]] — 50 km comparables ring + WDPA / OSM protected-area context.
- [[soilgrids_brief]] — 250 m soil profile (pH 5.3, clay-increasing argillic horizon).
- [[client_photos_brief]] — 14-row shot register at `client_photos/2026-06_post_escritura/index.md`; photo_verification.md is the 1-to-1 cross-ref.
- [[post_escritura_site_knowledge]] §3 — T+1 knowledge-pack narrative of the polygon scope-lock.
- [[decisions_log]] 2026-06-28 — polygon scope-lock decision.
- [[research_gaps]] R01 (stream permanence), R35 (individual trees).
- [[feedback_subscene_clip_end]] — sub-render `cam.data.clip_end` must bypass 100 m default at parcel scale.

Generated 2026-06-29 (T+2 post-escritura).
