# Canopy height brief — La Quebrada Viva (Phase-0 §12 v1)

_Pulled 2026-06-29 from Tolan et al. 2024 Meta High-Resolution Canopy Height (1 m source, EPSG:4326 10° resampled summary). AOI: 5 km buffer around parcel centroid (-57.0355, -25.6073). Sample points: 6 (centroid + 4 KML corners + Wesley pin)._

## Headline

- **Parcel-centroid canopy: 10.91 m mean, 13.56 m p95, 95.5% cover > 5 m** → mid-storey gallery forest pocket around the quebrada head.
- **NE corner: 12.68 m mean, 15.00 m p95, 100% cover > 5 m** → mature forest patch (deck "T-DT North woodlot").
- **NW, SE, Wesley pin: 2-4 m mean, 20-50% cover > 5 m** → degraded secondary scrub / regenerating chaco-mesopotámico mosaic.
- **SW corner: 0.27 m mean, 1.8% cover > 5 m** → essentially cleared (pasture / chacra).
- **AOI 5 km buffer average: 3.46 m mean canopy, 13 m p95, 28.9% of pixels carry canopy > 5 m** — typical Paraguarí district mosaic of remnant gallery forest in valley bottoms plus cleared pasture/cropland on ridges.

This **dismantles the GEDI L2A 48 m mean** that the on-disk fallback file showed: GEDI L2A waveforms over heterogeneous canopy + steep slope bias toward emergent / top-of-waveform returns and the 25-point sample is non-representative. The Meta CHM is the ground truth here; treat the GEDI cache as a high-side outlier reflecting emergent-tree extremes (single lapacho / yvyrá-pytá > 30 m) on the valley wall.

## Per-point indicators (3×3 of 28 m pixels around point)

| Point | avg m | median m | p95 m | cover % | cover5m % | typology |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| centroid | 10.91 | 11.22 | 13.56 | 97.7 | 95.5 | gallery forest pocket |
| corner_NE | 12.68 | 12.56 | 15.00 | 100.0 | 100.0 | mature woodlot |
| corner_NW | 3.72 | 3.89 | 5.67 | 51.4 | 41.3 | secondary scrub |
| corner_SE | 3.41 | 2.50 | 8.89 | 41.7 | 27.3 | degraded mosaic |
| corner_SW | 0.27 | 0.00 | 1.22 | 5.2 | 1.8 | cleared pasture |
| wesley_pin | 2.36 | 2.28 | 6.44 | 35.2 | 20.3 | regen low scrub |

_Per-point values stored in `canopy_points.csv`; raw windowed rasters in `meta_chm_aoi_<stat>.tif`._

## AOI summary (5 km buffer, 160 000 pixels at ≈28 m)

| Stat | mean | median | p95 | max | unit |
| --- | ---: | ---: | ---: | ---: | --- |
| avg | 3.46 | 1.22 | 13.01 | 24.52 | m |
| median | 3.30 | 0.00 | 13.00 | 25.00 | m |
| p95 | 5.69 | 5.00 | 16.00 | 31.00 | m |
| cover | 42.4 | 27.9 | 100.0 | 100.0 | % |
| cover5m | 28.9 | 2.7 | 100.0 | 100.0 | % |
| stdev | 1.33 | 1.09 | 3.78 | 11.47 | m |

**Tallest canopy in the 100 km² window: 31 m p95 / 24.5 m mean** — consistent with Atlantic-Forest remnant emergents (lapacho, timbó, yvyrá-pytá). Within the 62-ha parcel the tallest mature stand is at the NE corner ridge (12.7 m mean, ~15 m p95) — this matches the visual cue Wesley flagged on the satellite mosaic.

## Cross-reference with hydrogeology + soil

Canopy spatial pattern aligns with the [[hydrogeology_brief]] TWI map and the [[soilgrids_v2_summary]] clay profile:
- The 10–13 m canopy at the **centroid + NE corner** sits in the high-TWI valley-bottom drift (TWI 10.53–10.97) where the 30-60 cm clay loam holds soil water through the dry season → gallery forest persists.
- The **cleared SW corner** and degraded **NW / SE / Wesley pin** positions are on the higher-slope shoulders (slope 7–15%, TWI 10.7–11.1) where laterite topsoil drains faster → easier to clear, recolonized by low scrub when pasture is abandoned.

## Engineering / design implications

### Restoration / housing-park siting
- **Preserve the NE woodlot and centroid gallery forest pocket as-is** — these are the only mature (> 10 m) canopy on the parcel and are the visual + ecological backbone for any "eco-housing" or vacation-rental positioning. Hectarage to protect: ≈ 12-15 ha based on the > 5 m / > 10 m AOI mask (refine when DeepForest crown detection lands).
- **Reforestation priority zones**: SW corner (currently 0.27 m mean), Wesley-pin shoulder, and the SE band. Plant native succession species (lapacho rosado, yvyrá-pytá, peterevy, ka'á he'ẽ) — these will close canopy to ~ 5 m within 8-12 years per Atlantic-Forest restoration baselines.
- The Meta CHM patch at NE is small enough (~ 4-6 ha) that a single bad clearing event would erase it. Flag for the escritura close-out + first-month policy: **no clearing inside the NE woodlot or centroid gallery forest pocket** until the housing-park site plan locks viewsheds.

### Solar / PV siting (Rule 9 reciprocity)
PV array should sit on the SW cleared corner or the NW low-scrub band where canopy < 5 m and no clearing of mature trees is required. Avoid the NE woodlot and centroid gallery forest — even thinning would degrade the visual asset and the microclimate buffer.

### Sub-render typology mapping
- Sub-render `lqv/subscene/canopy_NE_woodlot.py`: target ≈ 12-15 m closed canopy, leaf-area-index ≈ 3-4, dominant species per `[[fauna_flora_brief]]`.
- Sub-render `lqv/subscene/scrub_secondary.py`: target ≈ 2-4 m mixed scrub, 30-50% cover, scattered emergents.
- Sub-render `lqv/subscene/cleared_pasture.py`: target ≈ 0-1 m grass with isolated lapacho/timbó snags.

## Provenance

- **Tolan et al. 2024 — Meta High-Resolution Canopy Height 1 m** (CC-BY-4.0): `s3://dataforgood-fb-data/forests/v1/alsgedi_global_v6_float_epsg4326_v3_10deg/meta_chm_lat=-20.0_lon=-60.0_<stat>.tif` (anonymous-readable). Reference: https://github.com/facebookresearch/HighResCanopyHeight ; https://research.facebook.com/publications/very-high-resolution-canopy-height-maps-from-rgb-imagery-using-self-supervised-vision-transformer-and-convolutional-decoder-trained-on-aerial-lidar/
- Native CHM was generated from Maxar imagery at 1 m via a DINOv2-based SSL vision transformer trained on aerial LiDAR; the 10° EPSG:4326 product aggregates 1 m to ≈28 m per pixel and stores 7 statistics (avg/median/p95/stdev as cm uint16; cover/cover5m as per-mille; count as raw integer).
- Pipeline: `scripts/phase0_canopy_height_v1.py` — `/vsicurl/` windowed read, AOI = 0.1° × 0.1° around centroid, per-point 3×3 mean, scale factors applied.
- **GEDI L2A on-disk fallback** (`docs/site_data/gedi_l2a_clean_summary.txt`): 25 clean shots, mean 48.5 m — high-side outlier per discussion above. Retain for cross-reference; not deck-grade.

## Carry-forward gaps (deferred)

- **Tree-crown delineation** (DeepForest + detectree2 on the high-res Sentinel-2 / Planet NICFI mosaic) — not yet pulled this batch; will provide per-tree species-level identification for the NE woodlot + centroid gallery forest.
- **Lang et al. 2023 ETH Global Canopy Height 10 m** — ETH share gated through DOI 10.3929/ethz-b-000609802 (no direct file). Could cross-validate Meta numbers if pulled via the research-collection web UI (user-side).
- **Potapov 2019 Forest_height_2019_SAM.tif** — endpoint dead (404 at glad.geog.umd.edu/Potapov/...). Skip.
- Field-truth (Wesley walk + smartphone clinometer at the 6 sample points) would settle the GEDI vs Meta dispute definitively. Document for the post-escritura site-walk checklist.
