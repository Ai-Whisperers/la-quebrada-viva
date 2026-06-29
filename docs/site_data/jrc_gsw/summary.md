# JRC Global Surface Water v1.4 (1984–2021) — Phase-0 §12.E

Centroid `-57.0355, -25.6073` — buffer 50.0 km
AOI bbox: W-57.5350 S-26.0578 E-56.5360 N-25.1568
Source tile: `60W_20S` from `https://storage.googleapis.com/global-surface-water/downloads2021`

## Layers pulled

| Layer | AOI valid cells | AOI nonzero % | Polygon valid cells | Polygon nonzero % | Polygon max |
| --- | ---: | ---: | ---: | ---: | ---: |
| occurrence | 14401584 | 1.74 | 446 | 0.00 | 0 |
| seasonality | 14401584 | 1.70 | 446 | 0.00 | 0 |
| recurrence | 14401584 | 2.11 | 446 | 0.00 | 0 |
| transitions | 14401584 | 2.11 | 446 | 0.00 | 0 |

## Interpretation for La Quebrada Viva polygon

- **Surface water inside polygon: 0 cells with any historical water occurrence.** JRC GSW agrees with the Sentinel-2 NDWI finding (`property_map/index.md`): no permanent or seasonal open water inside the 30.9 ha polygon at 30 m resolution.
- Polygon seasonality max: **0 months/year** (mean 0.00).
- Polygon recurrence max: **0%** of years with at least one water observation (mean 0.00%).

## Transitions histogram (1984→2021)

| Class | Description | AOI cells | Polygon cells |
| ---: | --- | ---: | ---: |
| 0 | No change / no data | 14097894 | 446 |
| 1 | Permanent water (1984–2021) | 136469 | 0 |
| 2 | New permanent (became permanent) | 5191 | 0 |
| 3 | Lost permanent (was permanent, lost) | 3154 | 0 |
| 4 | Seasonal water (both periods) | 2056 | 0 |
| 5 | New seasonal (became seasonal) | 96296 | 0 |
| 6 | Lost seasonal (was seasonal, lost) | 3752 | 0 |
| 7 | Seasonal → Permanent | 1149 | 0 |
| 8 | Permanent → Seasonal | 3178 | 0 |
| 9 | Ephemeral permanent | 948 | 0 |
| 10 | Ephemeral seasonal | 51497 | 0 |

## Files

```
docs/site_data/jrc_gsw/
├── occurrence_aoi_50km.tif   occurrence_polygon.tif   occurrence.png
├── seasonality_aoi_50km.tif  seasonality_polygon.tif  seasonality.png
├── recurrence_aoi_50km.tif   recurrence_polygon.tif   recurrence.png
├── transitions_aoi_50km.tif  transitions_polygon.tif  transitions.png
└── summary.md
```

## Caveats

- JRC GSW v1.4 ends 2021. For 2022–2025 monthly water dynamics, pull
  JRC Monthly History via GEE (`JRC/GSW1_4/MonthlyHistory`).
- Resolution is 30 m — sub-pixel water (< ~900 m² puddles, narrow
  arroyos < 30 m wide) is invisible. The polygon's `arroyo` features
  visible on canopy NDVI/DEM hydrography sit below this resolution
  threshold and correctly read as zero here. This is a *coarse-scale*
  confirmation that no perennial pond/lake exists on-property — not a
  micro-hydrology layer.
- For micro-hydrology use the DEM-derived flow-accum hydrography
  (`property_map/vector/hydrography_dem.geojson`) and pending drone SfM
  + NDWI sub-pixel work in `property_map_v2_data_sources.md` §3.
