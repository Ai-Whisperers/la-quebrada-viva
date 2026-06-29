# Photo verification cross-ref — property map (T+1, 2026-06-28)

> Keys the 14 derived feature-claims in `property_map.png` to specific shot-list rows in `docs/site_data/client_photos/2026-06_post_escritura/index.md`. Status legend: 🛰️ derived, awaiting verification · 📷 photo required to verify or refute · ✅ photo-verified · ❌ refuted by sat/OSM, photo still required to rule out untagged structures.

Wesley's intake window is **2026-07-27 → 2026-08-27** (see `docs/CLIENT.md` open-items §6). EXIF GPS sidecars are required for each frame; without GPS, none of the 🛰️ rows can be promoted to ✅.

## Cross-reference table

| # | Feature class | Source / derivation | Status | Photo-intake shot-list row | Resolution upon photo arrival |
|---|---|---|---|---|---|
| 1 | `canopy_dense` (NDVI > 0.85) | Sentinel-2 `S2B_21JVM_20260512_0_L2A`, 10 m, bin 4 | 🛰️ | shot-list **row 4 — "interior canopy"** + **row 5 — "secondary forest understorey"** | EXIF-GPS photo inside any dense polygon → ✅; if photo shows pasture/clearing → reclassify polygon, update `canopy_classes.tif` |
| 2 | `canopy_mid` (NDVI 0.60–0.85) | Same, bin 3 | 🛰️ | shot-list **row 5 — secondary forest** + **row 6 — transition strip** | Same as row 1 |
| 3 | `canopy_sparse` (NDVI 0.30–0.60) | Same, bin 2 | 🛰️ | shot-list **row 7 — open / sparse stripe** (SW boundary along stream) | Photo confirming pasture/scrub/erosion → ✅; if photo shows full canopy → S2 date drift, reclassify |
| 4 | `canopy_bare` (NDVI < 0.30) | Same, bin 1 | 🛰️ | shot-list **row 8 — clearings / bare patches** | Photo of bare soil / road / building footprint → ✅ |
| 5 | `stream_chain_S` (south-flowing main channel exiting SW) | COP30 DEM D8 flow-accum ≥ 30 cells, longest source-to-sink chain | 🛰️ | shot-list **row 9 — "main stream / arroyo"** with EXIF GPS at the polygon-edge crossing | EXIF GPS within 30 m of D8 line → ✅ (and tag *permanent* vs *seasonal* vs *dry*); >30 m offset → re-derive at higher DEM resolution (R35 / drone) |
| 6 | `stream_chain_E` (eastern tributary) | Same | 🛰️ | shot-list **row 10 — "tributary / second creek"** | Same as row 5 |
| 7 | `building_SE_cluster_1` (3 OSM polygons clustered SE of polygon along road) | OpenStreetMap Overpass 2026-06-28, `building=*` | 🛰️ | shot-list **row 11 — "neighbour structures along Camino a Escobar"** | Photo confirming neighbour buildings → ✅; photo missing → leave 🛰️ (low priority — neighbours, not on-property) |
| 8 | `building_SE_cluster_2` (3 OSM polygons mid-SE) | Same | 🛰️ | shot-list row 11 | Same as row 7 |
| 9 | `building_SE_cluster_3` (3 OSM polygons SW corner) | Same | 🛰️ | shot-list row 11 | Same as row 7 |
| 10 | `building_inside_polygon` (any structure on-property) | OpenStreetMap returns **0 buildings inside polygon** | ❌ refuted by OSM | shot-list **row 12 — "any existing structures on-property"** (cabin, shed, tool store, gate-house, pump-house) | Photo of any on-property structure → ❌ flipped to ✅ + new feature added to `buildings_osm.geojson` extension layer (OSM-untagged); zero photos and Wesley confirms vacant → ❌ → ✅ "confirmed vacant" |
| 11 | `road_Camino_a_Escobar` (1 OSM LineString, `highway=unclassified`, unpaved, 2-lane) | OpenStreetMap Overpass 2026-06-28 | 🛰️ | shot-list **row 13 — "access road approaching property"** with EXIF GPS at SW corner crossing | Photo of road with GPS → ✅ + confirm surface (unpaved/paved/gravel) and condition |
| 12 | `farmland_SW_1+2` (2 OSM `landuse=farmland` polygons SW of polygon) | OpenStreetMap Overpass 2026-06-28 | 🛰️ | shot-list **row 14 — "neighbouring land use"** (looking SW from boundary) | Photo of pasture/crops → ✅; abandoned scrub → update tag |
| 13 | `NDWI_zero_water_check` (no open water inside polygon) | Sentinel-2 NDWI median -0.83, 0 % open water | 🛰️ confirms baseline | shot-list **row 15 — "any standing water / pool / spring"** (cross-property walk) | Any standing-water photo → flip "no permanent water" → "has feature X at GPS" + update `post_escritura_site_knowledge.md` §3 |
| 14 | `salto_natural_pool` + `internal_road_existence` (rumoured features, not in OSM/S2/DEM) | Not derivable from satellite at this resolution | 📷 photo-required | shot-list **row 16 — "Salto / natural pool if present"** + **row 17 — "internal access tracks / paths"** | Any photo of a salto/pool/internal track → ✅ + new feature added to a `vector/photo_anchored.geojson` layer (created on photo arrival) |

## Promotion workflow (when photos drop)

1. Move raw JPGs/HEICs into `docs/site_data/client_photos/2026-06_post_escritura/raw/`.
2. Rename per the shot-list `index.md` convention.
3. Extract EXIF GPS sidecars (`exiftool -gps:all -j > <name>.json`).
4. Per row above, plot the EXIF coordinate against the relevant GeoJSON layer in QGIS / `geopandas`.
5. Update this table's **Status** column with the new state (🛰️ → ✅ / ❌).
6. If any row flips, append a corresponding entry to `docs/DECISIONS.md` (date-stamped 2026-XX-XX) noting the satellite-derived claim that was refuted/confirmed.
7. If any new feature is added (untagged building, salto, internal track), create / extend `docs/site_data/property_map/vector/photo_anchored.geojson` and re-render `property_map.png` with the new layer.

## What stays 🛰️ even after photos

R35 (drone LiDAR for individual tree positions) remains on hold regardless of photo arrival — ground photos can confirm canopy *classes* but cannot count *stems*. Tree-by-tree positioning waits for sub-1 m imagery or drone LiDAR per `docs/RESEARCH_GAPS.md` R35.

Related:
- `docs/site_data/property_map/index.md` (layer manifest + honesty caveats)
- `docs/site_data/client_photos/2026-06_post_escritura/index.md` (shot list + intake checklist)
- `docs/DECISIONS.md` 2026-06-28 (polygon scope-lock, outreach pause)
- `docs/RESEARCH_GAPS.md` R01, R35
