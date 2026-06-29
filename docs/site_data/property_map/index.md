# Property map — La Quebrada Viva (T+1, 2026-06-28)

> Satellite + DEM + OSM-derived map of the 30.9 ha buildable Mbopicua cluster (Wesley's KML polygon). **All layers are remote-sensed and pending photo verification** from Wesley's promised on-site intake (window 2026-07-27 → 2026-08-27).

## TL;DR

| Layer | Source | Status |
|---|---|---|
| Property boundary | Wesley's KML (`escobar_property_polygon.geojson`) | ✅ canonical AOI (DECISIONS.md 2026-06-28) |
| Canopy density | Sentinel-2 `S2B_21JVM_20260512_0_L2A` NDVI, 10 m, 4 bins | 🛰️ derived — pending photo verify |
| Streams / creeks | Copernicus 30 m DEM, D8 fill-pits + flow-accum, threshold 30 cells (~2.7 ha catchment) | 🛰️ derived — pending photo verify |
| Buildings | OpenStreetMap (Overpass fetch 2026-06-28) | 🛰️ derived — 9 polygons, **all south of polygon** (neighbours, not on-property) |
| Road | OpenStreetMap — `Camino a Escobar` (unpaved, 2-lane, oneway=no) | 🛰️ derived — 1 LineString |
| Natural/landuse | OpenStreetMap — `landuse=farmland` ×2 | 🛰️ derived |
| Open water (NDWI) | Sentinel-2 — NDWI median -0.83, **0 % open water in polygon** | 🛰️ confirms "no permanent water" inside |
| **Individual trees** | — | ⛔ **DEFERRED** — 10 m S2 cannot identify crowns; needs R35 drone LiDAR or sub-1 m imagery |

## Files

```
docs/site_data/property_map/
├── property_map.png                       # composite, 300 dpi, UTM 21S axes
├── index.md                               # this file
├── photo_verification.md                  # 14-row shot-list cross-ref
├── vector/
│   ├── buildings_osm.geojson              # 9 polygons (EPSG:4326)
│   ├── roads_osm.geojson                  # 1 LineString — Camino a Escobar
│   ├── natural_osm.geojson                # 2 farmland polygons
│   ├── canopy_classes.geojson             # NDVI 4-class polygons
│   └── hydrography_dem.geojson            # 15 stream LineStrings (D8 traced)
├── raster/
│   └── canopy_classes.tif                 # int8, EPSG:32721, nodata=0
└── quicklooks/
    ├── canopy.png                         # NDVI classes alone
    └── water.png                          # DEM hydrography alone
```

## Honesty caveats

1. **Individual tree positions are NOT shipped.** Sentinel-2 at 10 m resolution shows aggregate canopy density, not stems. The 4 NDVI bins (`<0.30 bare`, `0.30–0.60 sparse`, `0.60–0.85 mid`, `>0.85 dense`) describe a *surface*, not a *count*. R35 (drone LiDAR / sub-1 m imagery) remains on hold pending photos — see `docs/RESEARCH_GAPS.md` R35.
2. **No Google Earth Engine pull.** No GEE service-account auth is configured in `.env.local`. Substitutes used: free Sentinel-2 L2A via the S2B tile already on disk (`docs/site_data/sentinel2/`, gitignored), Copernicus 30 m DEM via OpenTopography (key in `.env.local`, not committed), OSM via Overpass.
3. **All derived layers are pending Wesley's on-site photos.** The intake window is 2026-07-27 → 2026-08-27 (`docs/CLIENT.md` open-items §6). The 14-row shot list at `docs/site_data/client_photos/2026-06_post_escritura/index.md` is what re-anchors these layers; cross-ref in `photo_verification.md`.
4. **OSM coverage is sparse here.** This bbox returns only **9 buildings + 1 road (`Camino a Escobar`) + 2 farmland polygons + 0 water**. Untagged structures (Wesley's own cabins/sheds, gates, fences, paths) are not in OSM — they will appear only after photos. The 9 OSM buildings sit *south of* the polygon — they read as **neighbour structures along the road, not on-property buildings**. The polygon currently shows zero on-property OSM-mapped buildings.
5. **Streams are DEM-derived, not photo-confirmed.** D8 flow accumulation at 30 m grid catches valley bottoms but cannot tell us whether a given line is a permanent creek, a seasonal arroyo, or a dry erosion channel. NDWI = 0 % open water inside the polygon (`docs/post_escritura_site_knowledge.md` §3) is consistent with seasonal-only flow. Wesley's photos with EXIF GPS will let us promote individual segments from 🛰️ to ✅.
6. **Cross-CRS bookkeeping.** All vector GeoJSON ships in EPSG:4326 (CRS84) for portability. The composite PNG and `canopy_classes.tif` are in EPSG:32721 (UTM 21S, 10 m / 30 m) for meter-scale axes and a clean scale bar.
7. **The composite uses Sentinel-2 from 2026-05-12 (Autumn / Otoño).** Phenological mid-Autumn green-flush captures peak NDVI; January / late-summer imagery would show drier sparse-class expansion in the open ridge corridor. We don't average across dates yet — single-date snapshot.

## Method

```
Wesley KML polygon (4326) ─┐
                           ├─→ buildings_osm.geojson  (Overpass: building=*)
Overpass API (lz4) ────────┼─→ roads_osm.geojson      (Overpass: highway=*)
                           └─→ natural_osm.geojson    (Overpass: natural=*, landuse=farmland)

Sentinel-2 NDVI (32721) ───→ digitize 4 bins ──→ canopy_classes.{tif,geojson} + canopy.png
COP30 DEM (4326) ──────────→ fill_pits ─→ d8_flow_dir ─→ flow_accum
                                                        ├─→ threshold ≥ 30 cells
                                                        └─→ trace source-to-sink → hydrography_dem.geojson + water.png

ALL LAYERS ────────────────→ matplotlib composite (hillshade base, EPSG:32721)
                              ├─ polygon boundary (white-on-black)
                              ├─ canopy alpha=0.55
                              ├─ streams steelblue
                              ├─ buildings red fill
                              ├─ road tan dashed
                              ├─ farmland hatched
                              ├─ 200 m scale bar + N arrow
                              └─→ property_map.png @ 300 dpi
```

Driver: `scripts/build_property_map.py`. Reusable pure-numpy hydrography pattern shared with `scripts/analyze_stream.py`.

## What this map can and cannot answer

**Can answer:**
- *"Where in the polygon is canopy densest? Where is the open ridge corridor?"* → dense-canopy class covers most of the surface; sparse stripe runs the SW boundary (the stream-bottom edge).
- *"Where do streams enter the polygon and where do they exit?"* → multiple headwater segments in the N/NE feed two main channels exiting the SW low corner.
- *"Are there any OSM-mapped buildings on the property?"* → no. The 9 OSM buildings sit south of the polygon along `Camino a Escobar`.
- *"What's the nearest mapped road?"* → `Camino a Escobar`, OSM-tagged `highway=unclassified, surface=unpaved, lanes=2, oneway=no`, running E-W just south of the polygon and dipping in slightly at the SW corner.
- *"Is there permanent open water inside the polygon?"* → no (NDWI = 0 %).

**Cannot answer (needs photos):**
- Individual tree positions, species mix, age structure → R35 / drone LiDAR.
- Whether DEM-traced streams are permanent, seasonal, or ephemeral.
- Existence and position of: gates, fences, on-property cabins, sheds, paths, the rumoured Salto / natural pool, internal access tracks.
- Soil exposure under dense canopy.
- Any cultural features (graves, shrines, boundary markers).

Cross-ref: `photo_verification.md` keys the 14-row shot list to specific layer claims.

Related:
- `docs/DECISIONS.md` 2026-06-28 · Polygon scope-lock
- `docs/post_escritura_site_knowledge.md` §3 (NDVI / NDWI) and §6 (gap matrix)
- `docs/RESEARCH_GAPS.md` R01, R35
- `docs/site_data/client_photos/2026-06_post_escritura/index.md` (14-row shot list)
