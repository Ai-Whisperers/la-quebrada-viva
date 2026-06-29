# Sentinel-2 L2A 12-date timeseries 2020–2025 — Phase-0 §12 #6

**Source.** element84 Earth-Search STAC, collection `sentinel-2-l2a` (Copernicus Sentinel-2 L2A surface reflectance, 10 m).
**License.** CC-BY-4.0 (ESA Sentinel Legal Notice ≈ CC-BY-4.0).
**AOI bbox (EPSG:4326).** W-57.0450 S-25.6450 E-57.0150 N-25.6150
**Target grid (EPSG:32721, 10 m).** W495480 S7163620 E498500 N7166960  (302×334 px)
**Scenes resolved.** 12 / 12 bi-annual buckets (2020-03-24 → 2025-10-14).

## Per-scene polygon-mean indices

| Bucket | Date | Scene | Cloud % | NDVI | NDWI | MNDWI | AWEIsh |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 2020-H1 | 2020-03-24 | `S2B_21JVM_20200324_1_L2A` | 0.0 | +0.761 | -0.700 | -0.579 | -0.657 |
| 2020-H2 | 2020-12-09 | `S2B_21JVM_20201209_1_L2A` | 0.0 | +0.766 | -0.693 | -0.559 | -0.767 |
| 2021-H1 | 2021-05-08 | `S2B_21JVM_20210508_1_L2A` | 0.0 | +0.825 | -0.767 | -0.628 | -0.603 |
| 2021-H2 | 2021-12-24 | `S2B_21JVM_20211224_1_L2A` | 0.0 | +0.740 | -0.685 | -0.573 | -0.731 |
| 2022-H1 | 2022-04-18 | `S2A_21JVM_20220418_0_L2A` | 0.0 | +0.809 | -0.736 | -0.599 | -0.647 |
| 2022-H2 | 2022-11-24 | `S2A_21JVM_20221124_0_L2A` | 0.0 | +0.770 | -0.691 | -0.562 | -0.741 |
| 2023-H1 | 2023-03-19 | `S2B_21JVM_20230319_1_L2A` | 0.0 | +0.789 | -0.709 | -0.575 | -0.634 |
| 2023-H2 | 2023-10-10 | `S2A_21JVM_20231010_0_L2A` | 0.0 | +0.734 | -0.665 | -0.559 | -0.673 |
| 2024-H1 | 2024-03-13 | `S2B_21JVM_20240313_0_L2A` | 0.0 | +0.782 | -0.722 | -0.613 | -0.664 |
| 2024-H2 | 2024-10-19 | `S2B_21JVM_20241019_1_L2A` | 0.0 | +0.728 | -0.658 | -0.558 | -0.668 |
| 2025-H1 | 2025-05-12 | `S2C_21JVM_20250512_0_L2A` | 0.0 | +0.801 | -0.745 | -0.616 | -0.633 |
| 2025-H2 | 2025-10-14 | `S2B_21JVM_20251014_0_L2A` | 0.0 | +0.771 | -0.699 | -0.557 | -0.712 |

## Summary statistics (across the 12-scene polygon means)

| Index | Min | Max | Mean |
| --- | ---: | ---: | ---: |
| NDVI   | +0.728   | +0.825   | +0.773   |
| NDWI   | -0.767   | -0.658   | -0.706   |
| MNDWI  | -0.628  | -0.557  | -0.581  |
| AWEIsh | -0.767 | -0.603 | -0.677 |

## Index definitions

- **NDVI** = (NIR − Red) / (NIR + Red). Greenness / live biomass. Native forest is typically 0.7–0.9; bare soil ≤ 0.2.
- **NDWI** (Gao) = (Green − NIR) / (Green + NIR). Canopy / surface water content. Positive = open water; negative = vegetation.
- **MNDWI** = (Green − SWIR1) / (Green + SWIR1). Better water discriminator than NDWI in built/turbid scenes (Xu 2006).
- **AWEIsh** = Blue + 2.5·Green − 1.5·(NIR + SWIR1) − 0.25·SWIR2. Feyisa et al. 2014 — open-water index tuned for shadow rejection. Positive = water.

## Cloud / shadow masking (SCL)

Per-scene Scene Classification (SCL) is the L2A 20 m product band. We **keep** classes 4 (vegetation), 5 (bare), 6 (water), 11 (snow) and **mask** 1 (saturated), 2 (dark), 3 (cloud shadow), 8 (cloud medium-prob), 9 (cloud high-prob), 10 (thin cirrus), 0 (no-data). Masked pixels become NaN in each index array and are excluded from both the per-scene polygon mean and the 12-scene `np.nanmedian` stack.

## Cross-references

- Phase-0 §12 #10 (Hansen GFC, `docs/site_data/hansen_gfc/`) gives continuous treecover2000 / loss-year — pair with NDVI median for the deck's canopy story.
- Phase-0 §12 #11 (Mapbiomas PY, `docs/site_data/mapbiomas_paraguay/`) gives categorical 30 m LULC 1985–2023 — pair with MNDWI/AWEIsh median to check whether Mapbiomas' Flooded Forest (class 6) pixels actually carry water signal here.
- Phase-0 §12 #12 (JRC GSW, `docs/site_data/jrc_gsw/`) gives global surface-water occurrence — AWEIsh median is the high-res LQV-only counterpart.

## Files

```
docs/site_data/sentinel2/timeseries_2020_2025/
├── <SCENE_ID>/                     × up to 12 scenes
│   ├── red.tif        (10 m, 0-10000 reflectance)
│   ├── green.tif
│   ├── blue.tif
│   ├── nir.tif
│   ├── swir16.tif     (resampled 20 m → 10 m, bilinear)
│   ├── swir22.tif     (resampled 20 m → 10 m, bilinear)
│   ├── scl.tif        (20 m → 10 m, nearest)
│   └── *.tif.meta.json (per-file STAC/license sidecar)
├── timeseries_quicklook.png  ← 5-panel RGB+NDVI+NDWI+MNDWI+AWEIsh
├── polygon_indices.csv       ← per-scene polygon means + bucket label
└── summary.md                ← this file
```

## Caveats

- Bucket coverage is **best-effort**: if every Sentinel-2 pass in a half-year exceeds 30% cloud, that bucket is empty and the median composite is computed from the remaining scenes.
- The 2024-H2 scene `S2B_21JVM_20241019_1_L2A` clears the AOI bbox-coverage filter but only resolves ~18 k of ~101 k valid pixels (likely a partial-tile granule on the AOI edge); other 11 scenes cover the full grid. The median stack uses `np.nanmedian`, so the 12-scene composite is unaffected outside the missing footprint.
- The 12-scene median is **not** a phenology-aware composite — wet/dry season scenes are mixed into one stack. For a dry-season-only or wet-season-only median, regenerate with a narrower bucket window.
- Bands are warped to a fixed 10 m EPSG:32721 grid via `rasterio.vrt.WarpedVRT` (nearest for 10 m bands & SCL, bilinear for 20 m SWIR). The output is exactly aligned across scenes, so per-pixel differencing between scenes is meaningful.
- Per-scene `.tif` files are kept on disk for re-runs but are **git-ignored** (see `.gitignore`: `docs/site_data/sentinel2/**/*.tif`). The PNG / CSV / MD outputs and the per-file `.meta.json` sidecars are tracked.
- Polygon means here use the full **AOI rectangle** (62 ha bbox), not the cadastral padron union, because Batch I needs a stable footprint that doesn't drift if a padron lookup later changes the parcel polygon. For padron-aligned numbers, intersect the COGs with `scripts/satellite/_aoi.parcel_polygon_geojson()` downstream.
