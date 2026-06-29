# Sentinel-2 L2A vegetation + water indices brief — La Quebrada Viva (Phase-0 §12 v1)

> Sentinel-2 L2A surface reflectance over the 62 ha AOI rectangle covering
> the 30.9 ha Mbopicua polygon. Includes a 6-band single-scene snapshot
> (S2B 2026-05-12) and a 12-scene bi-annual timeseries 2020-H1 → 2025-H2.
> Indices: NDVI / NDWI / MNDWI / AWEIsh. Native 10 m grid in EPSG:32721.

## Headline

- **Single scene S2B_21JVM_20260512_0_L2A** (2026-05-12) clears at 0.004 % cloud, sun elev 38.9°.
- **Scene-level land cover (S2 classifier):** 89.88 % vegetation, 8.03 % bare, 2.07 % water — the parcel's NDVI 0.918 sits in the top quartile of the vegetation share.
- **12-scene timeseries (2020-2025)** NDVI 0.728 → 0.825 (mean 0.773) — wall-to-wall canopy stable through the 2022 drought.
- **All scenes 0.0 % cloud** under SCL masking; only 2024-H2 is partial-tile (18 524 px vs ~100 860 elsewhere).
- **MNDWI / AWEIsh both negative** in every scene → zero open water at S-2 resolution across the full record; the Quebrada is sub-pixel.
- **Polygon NDVI 0.888 mean / 0.918 median** ([[extended_aoi_brief]]) — caps the 41 yr Landsat trend 0.681 → 0.782 ([[landsat_brief]]) at the canopy ceiling.

## Snapshot scene — S2B_21JVM_20260512_0_L2A

| Field | Value |
| --- | --- |
| STAC ID | `S2B_21JVM_20260512_0_L2A` |
| Date | 2026-05-12 |
| Platform | Sentinel-2B |
| Collection | element84 Earth-Search `sentinel-2-l2a` |
| Tile | 21JVM (MGRS) |
| EPSG | 32721 |
| Pitch | 10 m (B/G/R/NIR), 20 m → 10 m (SWIR) |
| Cloud cover (scene) | 0.0041 % |
| Sun elev | 38.92° |
| s2:vegetation | 89.88 % |
| s2:not_vegetated | 8.03 % |
| s2:water | 2.07 % |
| Bands held | red, green, blue, nir, swir16, scl |
| Bbox of scene | W −58.00 / E −56.90 / S −26.31 / N −25.31 (footprint) |

Bands are gitignored (each ~200 MB). The 1.5 MB `preview_rgb.png` quicklook + 32 KB metadata JSON are tracked.

## Sentinel-2 12-date polygon-mean timeseries

| Bucket | Date | Scene | Cloud | Valid px | NDVI | NDWI | MNDWI | AWEIsh |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2020-H1 | 2020-03-24 | `S2B_21JVM_20200324_1_L2A` | 0.0 % | 100 860 | +0.761 | −0.700 | −0.579 | −0.657 |
| 2020-H2 | 2020-12-09 | `S2B_21JVM_20201209_1_L2A` | 0.0 % | 100 844 | +0.766 | −0.693 | −0.559 | −0.767 |
| 2021-H1 | 2021-05-08 | `S2B_21JVM_20210508_1_L2A` | 0.0 % | 100 816 | +0.825 | −0.767 | −0.628 | −0.603 |
| 2021-H2 | 2021-12-24 | `S2B_21JVM_20211224_1_L2A` | 0.0 % | 100 860 | +0.740 | −0.685 | −0.573 | −0.731 |
| 2022-H1 | 2022-04-18 | `S2A_21JVM_20220418_0_L2A` | 0.0 % | 100 868 | +0.809 | −0.736 | −0.599 | −0.647 |
| 2022-H2 | 2022-11-24 | `S2A_21JVM_20221124_0_L2A` | 0.0 % | 100 860 | +0.770 | −0.691 | −0.562 | −0.741 |
| 2023-H1 | 2023-03-19 | `S2B_21JVM_20230319_1_L2A` | 0.0 % | 100 860 | +0.789 | −0.709 | −0.575 | −0.634 |
| 2023-H2 | 2023-10-10 | `S2A_21JVM_20231010_0_L2A` | 0.0 % | 100 860 | +0.734 | −0.665 | −0.559 | −0.673 |
| 2024-H1 | 2024-03-13 | `S2B_21JVM_20240313_0_L2A` | 0.0 % | 100 860 | +0.782 | −0.722 | −0.613 | −0.664 |
| 2024-H2* | 2024-10-19 | `S2B_21JVM_20241019_1_L2A` | 0.0 % | 18 524 | +0.728 | −0.658 | −0.558 | −0.668 |
| 2025-H1 | 2025-05-12 | `S2C_21JVM_20250512_0_L2A` | 0.0 % | 100 864 | +0.801 | −0.745 | −0.616 | −0.633 |
| 2025-H2 | 2025-10-14 | `S2B_21JVM_20251014_0_L2A` | 0.0 % | 100 856 | +0.771 | −0.699 | −0.557 | −0.712 |

\* 2024-H2 is a partial-tile granule (18 524 valid px); other 11 scenes carry the full ~100 860 px.

## 12-scene summary statistics

| Index | Min | Max | Mean | Range |
| --- | ---: | ---: | ---: | ---: |
| NDVI | +0.728 | +0.825 | +0.773 | 0.097 |
| NDWI (Gao) | −0.767 | −0.658 | −0.706 | 0.109 |
| MNDWI | −0.628 | −0.557 | −0.581 | 0.071 |
| AWEIsh | −0.767 | −0.603 | −0.677 | 0.164 |

Six-year NDVI floor 0.728 (2024-H2) > the 0.6 dense-canopy threshold → canopy never thinned out below "dense forest" across the record.

Wet/dry split (H1 = autumn / late wet, H2 = late spring / dry-end):

- **H1 scenes (Mar-May)** NDVI mean +0.794 (5 scenes) — peak canopy after the wet season.
- **H2 scenes (Oct-Dec)** NDVI mean +0.752 (5 scenes ignoring 2024-H2) — late dry-season dip, but still well above the 0.6 floor.

The ~0.04 NDVI seasonal swing is much smaller than the inter-annual variability of the surrounding Cerrado, reinforcing the gallery-forest classification (cf. [[landsat_brief]]).

## Index definitions

- **NDVI** = (NIR − Red) / (NIR + Red). Greenness / live biomass.
- **NDWI (Gao)** = (Green − NIR) / (Green + NIR). Canopy / surface water content. Positive = open water.
- **MNDWI** = (Green − SWIR1) / (Green + SWIR1). Built-area water discriminator (Xu 2006).
- **AWEIsh** = Blue + 2.5·Green − 1.5·(NIR + SWIR1) − 0.25·SWIR2. Shadow-rejecting open-water index (Feyisa et al. 2014).

## SCL masking

Per-scene Scene Classification (SCL) 20 m product band drives masking. Keep classes 4 (vegetation), 5 (bare), 6 (water), 11 (snow); mask 0 (no-data), 1 (saturated), 2 (dark), 3 (cloud shadow), 8 (cloud med-prob), 9 (cloud high-prob), 10 (thin cirrus). Masked pixels → NaN in each index array and excluded from both polygon means and the 12-scene `np.nanmedian` stack.

## Engineering implications

- **Canopy NDVI is structurally locked** at 0.728–0.825 across 6 years — the Blender scatter density (lapacho / piquillín / tajy) can use a single canopy-density value without seasonal modulation.
- **Zero open water** at S-2 10 m means any blue-water render of the Quebrada has to come from gallery-forest pixel logic (NDWI between −0.55 and −0.65 = "wet vegetation under canopy", not "river") + the 1 m parcel-tight DEM flow-routing ([[hydrogeology_brief]]).
- **2.07 % scene-level water** in the 2026-05-12 snapshot is from larger surface waters NW + S of the AOI (e.g. Mbopicuá creek confluence), not the parcel itself.
- **8.03 % scene-level bare** captures roads + pastures + soybean fallow surrounding the forest patch — the parcel polygon itself sits in the 89.88 % vegetation class.
- **SCL pre-mask** lets us re-derive any pixel-tight statistic on demand; the per-scene `.tif` files are gitignored but stay on disk for reruns.

## Sub-render typology

- `lqv/subscene/sentinel2_rgb_quicklook.py` — `preview_rgb.png` overlay at the parcel polygon for a deck spread.
- `lqv/subscene/ndvi_canopy_density.py` — 10 m NDVI 0.6→0.95 colour ramp, parcel polygon outline, used as a scatter density driver.
- `lqv/subscene/timeseries_strip.py` — 12-scene strip (1 row × 12 cols) NDVI quicklook for the briefing deck.
- `lqv/subscene/water_indices_panel.py` — 3-panel NDWI / MNDWI / AWEIsh for the "zero open water" deck claim.

## Provenance

- **STAC catalogue:** element84 Earth-Search, collection `sentinel-2-l2a`.
- **License:** CC-BY-4.0 (ESA Sentinel Legal Notice ≈ CC-BY-4.0).
- **Target grid:** EPSG:32721 (UTM 21S), W495480 / S7163620 / E498500 / N7166960, 302 × 334 px @ 10 m.
- **Resampling:** rasterio `WarpedVRT` — nearest for 10 m bands + SCL, bilinear for 20 m SWIR.
- **Reflectance transform:** scale-only DN→reflectance (offset=−0.1 deliberately not applied; see [[extended_aoi_brief]] §Reflectance-transform footnote).

## Carry-forward gaps

- **Wet-season-only median + dry-season-only median** — re-bucket the 12 scenes by hemisphere (DJF + MAM = wet, JJA + SON = dry) for separate composites; current median is phenology-naive.
- **Per-pixel multi-temporal stack** — currently only polygon means are saved in CSV; per-pixel 12-scene stack would let us flag any pixel that drops below NDVI 0.5 in any scene (likely the access lane).
- **Co-registration with Cop30 / ALOS** — bands warped to EPSG:32721, DEMs in EPSG:4326. Need a single canonical CRS for any Blender mesh + texture pair; the snapshot script in `lqv/snapshot.py` currently does this transform lazily.
- **Sentinel-1 SAR backscatter** — separate `docs/site_data/sentinel1/` ingest, not part of this brief.

## Cross-references

- [[extended_aoi_brief]] — polygon NDVI 0.888 mean / 0.918 median, reflectance-transform convention.
- [[landsat_brief]] — 41 yr coarse 30 m NDVI trend (0.681 → 0.782) under-caps this 10 m record.
- [[post_escritura_site_knowledge]] §3 — the deck NDVI 0.917 figure this brief reproduces.
- [[hydrogeology_brief]] — gallery-forest "wet vegetation under canopy" pixel logic.
- [[canopy_chm_brief]] — Meta CHM 1 m mean canopy height 10.9 m the NDVI 0.918 corroborates.
- [[mod16_brief]] — actual ET 1091 mm/yr the dense-canopy NDVI is transpiring.
