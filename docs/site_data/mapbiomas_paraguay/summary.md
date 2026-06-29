# Mapbiomas Paraguay Collection 2 (1985–2023) — Phase-0 §12.11

Centroid `-57.0355, -25.6073` — buffer 50.0 km
AOI bbox: W-57.5350 S-26.0578 E-56.5360 N-25.1568
Source: `https://storage.googleapis.com/mapbiomas-public/initiatives/paraguay/collection_2/` (EPSG:4326, uint8, 30 m, 256×256 COG)
Years pulled: 1985–2023 (39 annual rasters)

## Per-decade polygon native-forest fraction

| Year | Native forest % | Forest+plant % | Pasture % | Agriculture % |
| ---: | ---: | ---: | ---: | ---: |
| 1985 | 80.6 | 80.6 | 0.0 | 0.0 |
| 1995 | 80.1 | 80.1 | 0.5 | 0.0 |
| 2005 | 79.1 | 79.1 | 2.4 | 0.0 |
| 2015 | 81.9 | 81.9 | 2.6 | 0.0 |
| 2023 | 84.0 | 84.0 | 1.8 | 0.0 |

## Interpretation for La Quebrada Viva polygon

- **Native forest fraction (classes 3 + 6) 1985 → 2023:** 80.6% → 84.0% (Δ +3.4 pp).
- **Polygon footprint at 30 m:** ~382 pixels × 0.09 ha ≈ 34.4 ha (coarser than Hansen due to a different reprojection grid; treat as area-share indicator, not parcel-accurate hectarage).
- **Hansen 2000 cross-check:** Mapbiomas native-forest at 2000 = 80.1% vs Hansen treecover2000 mean = 82.1%. (Categorical vs continuous; agreement within ~15 pp is expected.)

## Top 10 polygon transitions 1985 → 2023

| From | → To | Pixels | ha |
| --- | --- | ---: | ---: |
| 3 Forest Formation | → (same) 3 Forest Formation | 297 | 26.73 |
| 12 Grassland | → (same) 12 Grassland | 54 | 4.86 |
| 12 Grassland | → 6 Flooded Forest | 16 | 1.44 |
| 3 Forest Formation | → 6 Flooded Forest | 8 | 0.72 |
| 12 Grassland | → 15 Pasture | 4 | 0.36 |
| 3 Forest Formation | → 15 Pasture | 3 | 0.27 |

## Files

```
docs/site_data/mapbiomas_paraguay/
├── mapbiomas_<YEAR>_aoi_50km.tif    × 39 years
├── mapbiomas_<YEAR>_polygon.tif     × 39 years
├── mapbiomas_decadal_quicklook.png  ← 1985/1995/2005/2015/2023
├── class_timeseries.csv             ← long-format AOI + polygon counts
├── change_trajectory_polygon.csv    ← 1985 × 2023 transition matrix
└── summary.md                       ← this file
```

## Caveats

- Mapbiomas Paraguay is a categorical 30 m LULC product — each pixel
  gets a single class label per year. Use Hansen GFC (§12.10) for
  continuous canopy %, and NICFI for sub-canopy degradation.
- Collection 2 publishes 1985–2023; 2024 (and the Collection 1 →
  Collection 2 deltas) are not yet released. Refresh when MapBiomas
  PY announces Collection 3.
- The `polygon` clips are reprojection-aligned to Mapbiomas' EPSG:4326
  grid, so they differ from Hansen's at the per-pixel level. Compare
  area shares, not pixel-by-pixel overlays.
- Per-year class %s sum across all classes present in the polygon,
  including the legitimate non-forest classes (pasture, agriculture,
  grassland). The deck cares about the native-forest delta, not the
  full LULC breakdown.
- Network-fetched via `/vsicurl/` — re-runs reuse the on-disk AOI
  clips and skip the network. Delete `mapbiomas_<YEAR>_aoi_50km.tif`
  to force a re-fetch.
