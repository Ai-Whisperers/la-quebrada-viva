# Landsat C2-L2 annual median 1985–2025 — Phase-0 §12 #8

**Source.** Microsoft Planetary Computer STAC, collection `landsat-c2-l2` (USGS Landsat Collection 2 Level-2 Surface Reflectance, 30 m, Landsat 4-TM / 5-TM / 7-ETM+ / 8-OLI / 9-OLI-2).
**License.** USGS-PD (USGS data are in the public domain).
**AOI bbox (EPSG:4326).** W-57.0450 S-25.6450 E-57.0150 N-25.6150
**Target grid (EPSG:32721, 30 m).** W495480 S7163610 E498510 N7166970  (101×112 px)
**Window.** 1985–2025  (41 years).
**Scene budget.** ≤ 8 cleanest scenes per year (filter: `eo:cloud_cover < 30.0%`).
**Years with data.** 41 / 41.

## Per-year polygon-mean indices

| Year | n | Platforms | NDVI | NBR | NDMI |
| ---: | ---: | --- | ---: | ---: | ---: |
| 1985 | 8 | landsat-5 | +0.681 | +0.517 | +0.217 |
| 1986 | 8 | landsat-5 | +0.664 | +0.467 | +0.175 |
| 1987 | 8 | landsat-5 | +0.631 | +0.422 | +0.147 |
| 1988 | 8 | landsat-4|landsat-5 | +0.690 | +0.516 | +0.208 |
| 1989 | 8 | landsat-5 | +0.699 | +0.519 | +0.214 |
| 1990 | 5 | landsat-5 | +0.680 | +0.480 | +0.200 |
| 1991 | 8 | landsat-5 | +0.689 | +0.507 | +0.211 |
| 1992 | 8 | landsat-5 | +0.665 | +0.506 | +0.217 |
| 1993 | 8 | landsat-5 | +0.661 | +0.471 | +0.176 |
| 1994 | 8 | landsat-5 | +0.710 | +0.531 | +0.224 |
| 1995 | 8 | landsat-5 | +0.696 | +0.541 | +0.224 |
| 1996 | 8 | landsat-5 | +0.644 | +0.462 | +0.167 |
| 1997 | 8 | landsat-5 | +0.699 | +0.517 | +0.205 |
| 1998 | 8 | landsat-5 | +0.722 | +0.559 | +0.242 |
| 1999 | 8 | landsat-5|landsat-7 | +0.600 | +0.370 | +0.099 |
| 2000 | 8 | landsat-5|landsat-7 | +0.648 | +0.410 | +0.127 |
| 2001 | 8 | landsat-5|landsat-7 | +0.669 | +0.439 | +0.148 |
| 2002 | 8 | landsat-5|landsat-7 | +0.732 | +0.522 | +0.228 |
| 2003 | 8 | landsat-5|landsat-7 | +0.564 | +0.331 | +0.057 |
| 2004 | 8 | landsat-5|landsat-7 | +0.690 | +0.455 | +0.182 |
| 2005 | 8 | landsat-5|landsat-7 | +0.649 | +0.399 | +0.130 |
| 2006 | 8 | landsat-5|landsat-7 | +0.633 | +0.408 | +0.125 |
| 2007 | 8 | landsat-5|landsat-7 | +0.727 | +0.528 | +0.223 |
| 2008 | 8 | landsat-5|landsat-7 | +0.681 | +0.466 | +0.179 |
| 2009 | 8 | landsat-5|landsat-7 | +0.707 | +0.515 | +0.214 |
| 2010 | 8 | landsat-5|landsat-7 | +0.671 | +0.455 | +0.161 |
| 2011 | 8 | landsat-5|landsat-7 | +0.726 | +0.523 | +0.235 |
| 2012 | 8 | landsat-7 | +0.733 | +0.529 | +0.225 |
| 2013 | 8 | landsat-7|landsat-8 | +0.737 | +0.498 | +0.221 |
| 2014 | 8 | landsat-7|landsat-8 | +0.726 | +0.475 | +0.198 |
| 2015 | 8 | landsat-7|landsat-8 | +0.756 | +0.567 | +0.254 |
| 2016 | 8 | landsat-7|landsat-8 | +0.704 | +0.456 | +0.176 |
| 2017 | 8 | landsat-7|landsat-8 | +0.694 | +0.465 | +0.176 |
| 2018 | 8 | landsat-7|landsat-8 | +0.770 | +0.574 | +0.260 |
| 2019 | 8 | landsat-7|landsat-8 | +0.700 | +0.468 | +0.175 |
| 2020 | 8 | landsat-7|landsat-8 | +0.738 | +0.539 | +0.247 |
| 2021 | 8 | landsat-7|landsat-8 | +0.722 | +0.517 | +0.226 |
| 2022 | 8 | landsat-7|landsat-8|landsat-9 | +0.747 | +0.546 | +0.251 |
| 2023 | 8 | landsat-7|landsat-8|landsat-9 | +0.743 | +0.519 | +0.228 |
| 2024 | 8 | landsat-8|landsat-9 | +0.782 | +0.556 | +0.272 |
| 2025 | 8 | landsat-8|landsat-9 | +0.771 | +0.547 | +0.265 |

## Summary statistics (across per-year polygon means)

| Index | Min | Max | Mean |
| --- | ---: | ---: | ---: |
| NDVI | +0.564 | +0.782 | +0.696 |
| NBR  | +0.331  | +0.574  | +0.490  |
| NDMI | +0.057 | +0.272 | +0.198 |

## Index definitions

- **NDVI** = (NIR − Red) / (NIR + Red). Greenness / live biomass. Native forest is typically 0.7–0.9; bare soil ≤ 0.2.
- **NBR** = (NIR − SWIR2) / (NIR + SWIR2). Normalized Burn Ratio. Healthy canopy ≈ +0.6 to +0.9; recent burn drops to ≤ +0.1. The year-over-year **dNBR** signature is the standard fire-scar metric (Key & Benson 2006).
- **NDMI** = (NIR − SWIR1) / (NIR + SWIR1). Normalized Difference Moisture Index. Tracks canopy water content; closed humid forest ≈ +0.3 to +0.5; drought-stressed canopy ≤ +0.1.

## QA_PIXEL mask

Per-scene Collection 2 Level-2 QA_PIXEL band drops pixels where any of these bits are set: 1 (dilated cloud), 2 (cirrus), 3 (cloud), 4 (cloud shadow). Bit 5 (snow) is kept — no snow expected at −25.6° S / 350 m elevation. Fill pixels (QA == 0) are also dropped. Masked pixels become NaN in each per-scene index and are excluded from the per-year `np.nanmedian` composite.

## Surface-reflectance scaling

C2-L2 reflectance bands are 16-bit DN. Scaled to physical reflectance via `SR = DN · 0.0000275 − 0.2` (USGS), then any value outside [0, 1] is treated as NaN (post-mask artifacts on cloud edges, deep shadow, sensor saturation).

## Sensor coverage by era

- **1985–1992**: Landsat 5 TM is the workhorse; Landsat 4 TM adds a handful of scenes 1985-1993.
- **1993–1998**: gap-prone — Landsat 4 retired 1993, Landsat 5 alone, less reliable cloud-free coverage. Some years may carry n=0.
- **1999–2003**: Landsat 7 ETM+ joins; full 16-day combined revisit.
- **2003–2012**: ETM+ SLC-off (post 2003-05-31) striping; medians fill the stripes from Landsat 5 scenes where both fly.
- **2013–2021**: Landsat 8 OLI takes over; consistent ≤ 30 % cloud scenes year-round.
- **2021–2025**: Landsat 9 OLI-2 doubles cadence with L8.

## Cross-references

- Phase-0 §12 #6 (Sentinel-2 L2A 2020–2025 timeseries, `docs/site_data/sentinel2/timeseries_2020_2025/`) is on the same AOI corners at **10 m**. Per-pixel NDVI comparison requires a 3:1 block-mean downsample on the S2 side (or 3:1 nearest upsample on the Landsat side, with care taken to flag the fake resolution).
- Phase-0 §12 #7 (Sentinel-1 RTC, `docs/site_data/sentinel1/rtc_6mo_median/`) sits on the same corners at 10 m too — its VH dB median is the post-2014 radar counterpart to the Landsat NBR/NDMI moisture record.
- Phase-0 §12 #10 (Hansen GFC v1.12, `docs/site_data/hansen_gfc/`) gives **annual treecover loss-year** 2001–present at 30 m. Cross-check: Landsat NBR drop year should match Hansen `lossyear` for any pixel that lost canopy.
- Phase-0 §12 #11 (Mapbiomas Paraguay, `docs/site_data/mapbiomas_paraguay/`) categorical LULC 1985–2023 at 30 m. Same temporal span as this dataset; per-pixel join in EPSG:32721 reveals which Mapbiomas class transitions actually show in the NDVI / NBR / NDMI time series.

## Files

```
docs/site_data/landsat/annual_median_1985_2025/
├── <YEAR>/                          × N years with data
│   ├── ndvi.tif        (30 m, float32, median composite)
│   ├── nbr.tif
│   ├── ndmi.tif
│   └── *.tif.meta.json (per-file STAC/license sidecar incl. scene_ids)
├── annual_quicklook.png   ← grid of per-year NDVI panels
├── decadal_quicklook.png  ← 3-row × 5-decade NDVI/NBR/NDMI panel
├── polygon_indices.csv    ← per-year polygon means
└── summary.md             ← this file
```

## Caveats

- ≤ 8 cleanest scenes per year is enough to stabilize the median against speckle and per-scene haze, but is **not** a phenology-aware composite. Wet/dry season scenes are co-stacked — NDVI ≈ 0.78 plateau reflects evergreen canopy, not seasonal flush.
- C2-L2 QA_PIXEL is conservative: thin cirrus and cloud-edge shadow are aggressively masked, sometimes over-masked. A year with no scenes meeting the cloud-cover filter is simply missing in the output.
- L7 ETM+ SLC-off striping (post 2003-05-31) creates ~22 % data gaps in single scenes. Per-year medians fill these from L5/L8 co-coverage where available; years 2003–2012 still carry some residual stripe artifacts near the AOI edges.
- Native Landsat is **30 m**. This driver does NOT resample to the 10 m S2/S1 grid — that would fabricate resolution. The EPSG:32721 corners match Batches I/J so downstream joins are a clean 3:1 block-mean (or per-pixel 30 m read with S2 pre-aggregated to 30 m).
- Per-year `.tif` files are kept on disk for re-runs but are **git-ignored** (see `.gitignore`: `docs/site_data/landsat/**/*.tif`). The PNG / CSV / MD outputs and the per-file `.meta.json` sidecars are tracked.
- Surface-reflectance pixels outside [0, 1] after scaling are treated as NaN. This is a common post-mask cleanup (cloud-edge halos, deep shadow, sensor saturation can produce out-of-range values) and discards roughly 0.1–0.5 % of unmasked pixels in this AOI.
- MPC's SAS tokens expire after ~50 minutes. This driver fetches a fresh token at startup; if a run lasts longer than that across many years, `read_band` may 403 mid-run — restart and the per-year TIF cache will skip already-completed years.
