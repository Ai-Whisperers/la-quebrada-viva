# Protected areas + comparables — 50 km buffer (Phase-0 §12.D)

Centroid: `-57.0355, -25.6073` (La Quebrada Viva)
Buffer: 50 km radius (BBOX W=-57.5350 S=-26.0578 E=-56.5360 N=-25.1568)

## Counts by source

| Source | Records |
| --- | ---: |
| WDPA (Protected Planet REST) | 0 |
| OSM Overpass (gap-fill) | 5 |
| **TOTAL within 50 km** | **5** |

## 10 nearest

| # | Source | Name | Designation | IUCN | Dist (km) | Reported area (km²) |
| ---: | --- | --- | --- | --- | ---: | ---: |
| 1 | osm_overpass | Noche Con. Bosques Embrujados | — | — | 3.73 | — |
| 2 | osm_overpass | Noche Con. Bosques Embrujados | — | — | 3.73 | — |
| 3 | osm_overpass | Distrito de Escobar | — | — | 4.03 | — |
| 4 | osm_overpass | Monumento Natural Cerro Koi | nature_reserve | — | 48.13 | — |
| 5 | osm_overpass | Monumento Natural Cerro Chororî | nature_reserve | — | 49.26 | — |

## Context

- The property sits in the southern lowland fringe of the **Bosque Atlántico del Alto Paraná** (BAAPA) ecoregion.
- Relevant Paraguay national-level instruments: **SINASIP** (Sistema Nacional de Áreas Silvestres Protegidas) via MADES.
- Nearby cross-border reference: Argentine provincial reserves in Misiones / Corrientes also visible in this radius.
- WDPA REST records lack polygon geometry; for true GIS overlays pull the WDPA monthly shapefile download.

## Known gaps

- **WDPA REST returned HTTP 401** (both PRY and ARG, page 1). The Protected Planet `/v3/protected_areas/search` endpoint now requires a `token=` query param (free, register at protectedplanet.net → `PROTECTEDPLANET_API_KEY`, then re-run). For now, all 5 records come from OSM Overpass gap-fill.
- OSM Overpass returned 10 elements in the buffer bbox; 5 passed the haversine 50 km filter. Duplicate "Noche Con. Bosques Embrujados" is a relation + way pair for the same reserve (OSM tag-relation duplication, kept verbatim — dedupe by name + centroid is a follow-up).
- The two Monumento Natural sites (Cerro Koi, Cerro Chororî) are at the 50 km edge — comparables only, not adjacent.
