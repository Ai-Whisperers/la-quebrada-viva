# Building footprints — MS + Google Open Buildings (AOI ±1 km)

AOI bbox W-57.0600 S-25.6340 E-57.0100 N-25.5860 (polygon ±1.0 km)
Centroid: `-57.0355, -25.6073`

## Counts

| Source | Buildings | Σ footprint m² |
|---|---:|---:|
| ms_global_ml | 737 | 59947 |
| **TOTAL** | **737** | **59947** |

## Nearest building to polygon centroid (per source)

| Source | Distance (km) | Centroid (lon, lat) | Footprint m² |
|---|---:|---|---:|
| ms_global_ml | 0.196 | `-57.03492, -25.60898` | 17 |

## Provenance

- MS quadkeys queried (z=9): `210301312`
- MS quadkeys with data returned: `210301312`
- Google S2 tiles queried: `(none)`
- Overture buildings: **deferred** — requires DuckDB/GeoParquet
  (Overture's building theme is largely the merge of MS + Google + OSM;
  OSM buildings already harvested in v1 at `docs/site_data/property_map/`.)

Generated: 2026-06-29 04:24 UTC
