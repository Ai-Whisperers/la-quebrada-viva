# Infrastructure brief — La Quebrada Viva (Phase-0 §12 v1)

> Built-environment census within 1 km of the 30.9 ha Mbopicua parcel
> polygon. Combines Microsoft Global ML Building Footprints + Google Open
> Buildings into a single AOI±1 km layer. Establishes the **neighbour
> density baseline** that frames how isolated the parcel actually is.

## Headline

- **737 buildings** in the AOI±1 km ring (W −57.0600 / E −57.0100, S −25.6340 / N −25.5860 — 5.0 × 5.3 km centred on the parcel).
- **Σ footprint 59 947 m² = 5.99 ha** of built area — 0.23 % of the ~26.5 km² AOI window.
- **Nearest neighbour 196 m** from the parcel centroid (−57.03492, −25.60898) with a 17 m² footprint — consistent with a single rural dwelling, not a village edge.
- **100 % Microsoft ML, 0 % Google** — the Google Open Buildings v3 release (Africa + South Asia + South-East Asia + Latin America) covers Paraguay but the S2-tile query returned empty in this AOI (most likely Mbopicua falls inside an MS-only release window).
- **Heights unavailable** — every MS feature has `ms_height_m = −1.0`. Height needs to come from `make_chm.py` (Meta CHM 1 m) or an OSM overlay.
- **Density:** 737 features / 26.5 km² ≈ **27.8 buildings/km²** — sparse rural, vs. ~1500 buildings/km² for Asunción centre.

## Footprint distribution (Microsoft Global ML, n=737)

| Stat | Value |
| --- | ---: |
| Min | 10.9 m² |
| Max | 1 466.5 m² |
| Mean | 81.3 m² |
| Median | 58.6 m² |
| P25 | 31.6 m² |
| P75 | 97.6 m² |
| P95 | 209.6 m² |
| Σ | 59 947 m² |

Binned:

| Band | Count | Share |
| --- | ---: | ---: |
| 0–20 m² | 65 | 8.8 % |
| 20–50 m² | 253 | 34.3 % |
| 50–100 m² | 245 | 33.2 % |
| 100–200 m² | 134 | 18.2 % |
| 200–500 m² | 34 | 4.6 % |
| 500+ m² | 6 | 0.8 % |

Reads as the expected smallholder-rural shape: most footprints are 30–100 m² (single rooms / kitchens / smallholder houses), a long tail of 200+ m² (compound / outbuilding), and only six structures >500 m² (likely tinglados / agricultural sheds).

## Microsoft ML confidence (n=737)

| Stat | Value |
| --- | ---: |
| Min | 0.510 |
| Max | 1.000 |
| Mean | 0.972 |
| Median | (high) |

The MS confidence floor is 0.51 (its publication threshold); the mean is 0.972, i.e. the layer is dominated by high-confidence detections. Anything below 0.6 should be flagged before display.

## Nearest neighbour to parcel centroid

| Source | Distance | Centroid (lon, lat) | Footprint | Notes |
| --- | ---: | --- | ---: | --- |
| ms_global_ml | 196 m | −57.03492, −25.60898 | 17 m² | Smallest band — likely outbuilding / shed, not a residence |

196 m is the **closest any neighbour gets to the parcel centroid**, not to the polygon boundary. Per parcel polygon geometry (8 vertices, 30.9 ha), the nearest building could be sub-100 m from the edge — worth a manual sanity pass before the deck claims "isolated."

## Provenance

| Layer | Source | Access | Status |
| --- | --- | --- | --- |
| `ms_buildings.geojson` | Microsoft Global ML Building Footprints | quadkey 210301312 (z=9) | landed |
| `buildings_combined.geojson` | MS only (Google returned 0) | merged | landed |
| Google Open Buildings v3 | S2-tile API | tile list `(none)` returned | empty for AOI |
| Overture Maps | DuckDB / GeoParquet | requires DuckDB install | **deferred** |
| OSM buildings | Overpass | `docs/site_data/property_map/` | already harvested in v1 |

MS source: https://github.com/microsoft/GlobalMLBuildingFootprints — v2 release, model `model_141321212`.

## Engineering implications

- **Sub-render baseline confirmed sparse-rural**: 27.8 buildings/km² over a 5 km buffer means the parcel sits in genuinely low-density countryside. The deck claim of "isolated rural setting" is structurally true (just confirm by polygon-edge distance).
- **Footprints can drive a low-poly "neighbour" scatter** for any establishing wide. Use the 65 + 253 sub-50 m² features as `lqv/subscene/neighbours_low_density.py` cubes/prisms at the geojson centroid; ignore them inside the parcel polygon.
- **Heights are missing.** Pull the Meta CHM 1 m raster ([[canopy_chm_brief]]) for tree heights and use it as a proxy where buildings sit under canopy. For exposed roofs, fall back to OSM `building:levels` if present; otherwise default to 3.0 m single-story.
- **MS-only coverage** is a known issue for rural PY — flag in the deck that "0 Google Open Buildings detections in this AOI" is data-availability, not "no buildings in those zones."
- **Overture pull is gated** on DuckDB+GeoParquet — Overture is essentially the union of MS + Google + OSM, so the marginal yield over what we already have is small. Postpone to Phase-1 if at all.

## Sub-render typology

- `lqv/subscene/neighbour_density_map.py` — 5 × 5 km cube field of MS centroids extruded to 3 m default height (height-from-CHM upgrade pending), parcel polygon outline + 196 m nearest-neighbour pin.
- `lqv/subscene/footprint_histogram.py` — bar chart of 6-bin footprint distribution for the deck appendix.
- `lqv/subscene/nearest_neighbour_marker.py` — 30 m polygon-tight sub-render with the closest 5 footprints colour-mapped by distance.

## Carry-forward gaps

- **Polygon-edge distance** (currently centroid-distance) — recompute with shapely `polygon.distance(point)` to verify "no building inside or adjacent to" the parcel.
- **Height attribution** — join MS centroids to Meta CHM 1 m max-z to assign per-building heights; fallback to `osm building:levels`.
- **Overture pull** — DuckDB install + GeoParquet `s3://overturemaps-us-west-2/release/2026-05/theme=buildings/*` query; defer to Phase-1.
- **Google Open Buildings re-attempt** — current run returned 0 features. Verify the S2-tile coverage by hand (Google publishes a `release_2026_v3.geojson` coverage layer).
- **OSM diff** — cross-check with `docs/site_data/property_map/` OSM buildings to flag any MS feature missing from OSM (or vice versa).

## Cross-references

- [[post_escritura_site_knowledge]] — published parcel polygon geometry.
- [[canopy_chm_brief]] — Meta CHM 1 m for building-height attribution.
- [[extended_aoi_brief]] — 5 km buffer terrain context.
- [[property_map_brief]] — OSM-side built environment (existing v1 layer).
- [[sentinel2_brief]] — S-2 classifier flags 2.07 % water and 89.88 % vegetation, leaving ~8 % bare/built — bigger than the 0.23 % MS footprint share because the classifier also catches roads + bare soil.
