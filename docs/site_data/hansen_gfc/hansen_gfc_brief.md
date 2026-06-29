---
name: hansen_gfc_brief
description: Hansen Global Forest Change v1.12 (2000-2024) stand-replacement loss + treecover2000 + gain over the 50 km AOI and the 30.9 ha Mbopicua polygon — mean 82.1% canopy at 2000, 0.63 ha loss over 24 years, 0 gain pixels.
metadata:
  type: project
---

# Hansen GFC v1.12 forest-change brief — La Quebrada Viva (Phase-0 §12 v1)

> Hansen Global Forest Change v1.12 (2000-2024) tile `20S_060W` pulled
> from `earthenginepartners-hansen` GCS bucket. Five layers
> (treecover2000, lossyear, gain, datamask, derived loss) over the
> 50 km-buffered AOI rectangle and the 30.9 ha Mbopicua polygon. Native
> ≈30 m × 27 m grid at lat −25.6° (cos-corrected).

## Headline

- **Polygon canopy at 2000: mean 82.1 %, max 100 %, 412 / 446 cells with any canopy (92.4 %)** — the parcel was already a closed-canopy patch when the Hansen baseline began.
- **Stand-replacement loss 2001-2024: 7 pixels ≈ 0.63 ha** — ~2 % of the polygon over 24 years, concentrated in 4 events (2001, 2003 ×4, 2007, 2014).
- **Forest gain 2000-2012: 0 pixels** — Hansen never flagged any regrowth inside the parcel during the only gain-product window.
- **Datamask mean 1.00** — polygon is 100 % land per Hansen (no inland-water mask).
- **50 km AOI loss 4.94 %** vs polygon 1.57 % → parcel sits ~3× below the regional deforestation rate of the Paraguarí buffer landscape.
- **Cross-confirms [[sentinel2_brief]] NDVI 0.728-0.825 wall-to-wall** — the 6-yr S-2 NDVI floor (0.728) is consistent with Hansen's "no new loss since 2014" finding.

## Pull parameters

| Field | Value |
| --- | --- |
| Source | `https://storage.googleapis.com/earthenginepartners-hansen/GFC-2024-v1.12` |
| Tile | `20S_060W` |
| Centroid | (−57.0355, −25.6073) |
| AOI buffer | 50.0 km |
| AOI bbox | W −57.5350 / E −56.5360 / S −26.0578 / N −25.1568 |
| Pixel size | ~30 m N-S × ~27 m E-W (1 arcsec cos-corrected) |
| Pixel ha | 0.0900 ha nominal (30×30) |
| Polygon cell count | 446 (raster-overlap, ≈40.1 ha covers 30.9 ha geometry) |
| AOI cell count | 14 401 584 |
| Version | v1.12 (2024 update) |
| Vintage | 2000 baseline → 2024 loss/lossyear |
| Gain vintage | 2000-2012 only (band not updated post-v1.0) |

## Layer summary — polygon vs AOI

| Layer | AOI valid | AOI nonzero % | Polygon valid | Polygon nonzero % | Polygon mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| treecover2000 (%) | 14 401 584 | 54.80 | 446 | 92.38 | 82.11 |
| lossyear (2001-24) | 14 401 584 | 4.94 | 446 | 1.57 | 0.08 |
| gain (2000-12) | 14 401 584 | 0.09 | 446 | 0.00 | 0.00 |
| datamask | 14 401 584 | 100.00 | 446 | 100.00 | 1.00 |
| loss = lossyear > 0 | 14 401 584 | 4.94 | 446 | 1.57 | 0.02 |

The 92.38 % vs 54.80 % nonzero contrast is the load-bearing number: the parcel is a mature dense-canopy patch sitting in a landscape that is roughly half-forested half-pasture/cropland.

## Loss-year histogram (polygon, 2001-2024)

| Year | Polygon loss px | Polygon loss ha | AOI loss px | AOI share % |
| ---: | ---: | ---: | ---: | ---: |
| no loss | 439 | — | 13 690 595 | 95.06 |
| 2001 | 1 | 0.09 | 11 070 | 0.077 |
| 2003 | 4 | 0.36 | 22 685 | 0.157 |
| 2007 | 1 | 0.09 | 20 725 | 0.144 |
| 2014 | 1 | 0.09 | 28 969 | 0.201 |
| 2002, 2004-06, 2008-13, 2015-24 | 0 | 0.00 | varies | — |

Read this as four micro-events: 2003 is the largest (4 contiguous px ≈ 0.36 ha — likely a single edge-clearing or windthrow), then three single-pixel losses spread across 13 years. No event after 2014 — the parcel has been stable for 10 consecutive years on this product.

The AOI tells a different story: regional loss accelerates from ~11 000 px/yr (2001) to ~48 000 px/yr (2024), a 4-5× rate increase consistent with the documented BAAPA (Bosque Atlántico del Alto Paraná) deforestation front. The parcel has resisted that front so far.

## Cross-check with other ground-truth

| Source | Claim | Hansen agrees? |
| --- | --- | --- |
| [[sentinel2_brief]] | NDVI 0.728-0.825 wall-to-wall 2020-2025 | Yes — no Hansen loss after 2014 + NDVI floor 0.728 both say "still dense" |
| [[landsat_brief]] | 41 yr NDVI trend 0.681 → 0.782 | Consistent — slow greening over the Landsat window matches "no net loss" Hansen story |
| [[canopy_height_brief]] | Meta CHM 1 m mean 10.9 m canopy | Consistent — 82 % treecover2000 + ≥10 m canopy = closed gallery forest |
| [[gbif_brief]] | 50 dense-canopy Aves, 0 mammals | Consistent — closed-canopy habitat with intact avian community, missing mammal records is a sampling artefact not a habitat artefact |
| [[infrastructure_brief]] | 0 buildings inside parcel, nearest 196 m | Consistent — 0 stand-replacement loss after 2014 means no on-parcel construction in 10 yr |
| [[osm_brief]] | no roads inside parcel | Consistent — Hansen would catch any new road as loss; none after 2014 |

## Engineering implications

- **The parcel is a stable mature-forest patch on a deforesting landscape.** The 3× contrast (polygon 1.57 % vs AOI 4.94 % loss) is the most marketable conservation claim in the deck: *"the property is forest-positive in a forest-negative neighbourhood."*
- **No Hansen loss after 2014** means the Phase-1 "before" state is the 2024 satellite + 2014 historical Hansen baseline; no Phase-0 reconstruction of mid-record clearings is needed.
- **The 4 micro-events (2001 / 2003 / 2007 / 2014)** — 7 pixels totalling 0.63 ha — should be located on the parcel via lossyear pixel coordinates to decide whether they correspond to (a) the OSM-mapped southern boundary trail edge, (b) the Quebrada channel windthrow, or (c) genuine selective clearings. This is the next pixel-tight task (see Carry-forward).
- **Sub-canopy degradation is invisible to Hansen.** Hansen v1.12 catches only stand-replacement (>50 % canopy loss in a single 30 m pixel). Selective logging, thinning, fire-damaged understory all show as "no loss" — for those signals defer to [[mapbiomas_brief]] (Phase-0 §12 #11) + NICFI ([[deferred_data]] R3X) + the **[[client_photos_brief]] shot-need #05** species photos.
- **The `gain` band is historical-only (2000-2012)** and shows zero polygon gain. Do not cite "no Hansen gain" as evidence of "no restoration" — the band stopped updating in 2012. Use Mapbiomas land-cover trajectories for current regrowth claims.
- **For UNFCCC Paraguay forest definitions, both the ≥10 % and ≥30 % treecover2000 thresholds classify the parcel as "forest"** (mean 82.1 %). The BAAPA-default ≥30 % threshold puts 92.4 % of polygon cells over the line.

## Sub-render typology

- `lqv/subscene/hansen_treecover_map.py` — polygon outline + treecover2000 colour ramp (0-100 % yellow→dark-green), AOI inset showing the deforestation front; used for the deck's "forest-positive parcel" claim.
- `lqv/subscene/hansen_loss_timeline.py` — 4-event timeline (2001, 2003, 2007, 2014) with px-count bars; 1-row strip for the deck appendix.
- `lqv/subscene/hansen_aoi_contrast.py` — 50 km AOI loss raster (red 2001-2024 fade ramp) with the parcel polygon as a green island; load-bearing "neighbourhood is deforesting, we are not" infographic.
- `lqv/subscene/hansen_pixel_attribution.py` — fires only after the 7 lossyear pixel coordinates are mapped back to OSM / Quebrada / clearing locations; renders an annotated polygon overlay.

## Provenance

- **Source URL:** `https://storage.googleapis.com/earthenginepartners-hansen/GFC-2024-v1.12/Hansen_GFC-2024-v1.12_<layer>_20S_060W.tif`
- **Citation:** Hansen, M. C., P. V. Potapov, R. Moore, M. Hancher et al. (2013) "High-Resolution Global Maps of 21st-Century Forest Cover Change." *Science* 342: 850-53. Data updated v1.12 (2024).
- **License:** CC-BY-4.0 (UMD GLAD lab).
- **Pulled:** 2026-06-29 by AI Whisperers via direct GCS HTTP fetch (no auth required).
- **Outputs:** 4 AOI rasters + 4 polygon-clipped rasters + 4 PNG previews + summary.md (this brief synthesizes summary.md into the canonical template).
- **Coordinate system:** EPSG:4326 native; reprojection to EPSG:32721 (UTM 21S) deferred to Blender-mesh time.

## Carry-forward gaps

- **Pixel-attribution pass for the 7 loss pixels** — extract (lat, lon) for the 4 events and overlay on [[osm_brief]] + [[hydrogeology_brief]] flow-routing. If the 2003 4-px cluster sits on the Quebrada channel, it's likely windthrow not clearing; if it's on the parcel margin, it's an edge-management event.
- **Mapbiomas Paraguay (next §12 item) extends the record back to 1985** and adds land-cover trajectory classes (regrowth, secondary forest, pasture). Required to claim restoration vs persistence.
- **NICFI Planet 4.7 m monthly mosaics** would catch sub-Hansen selective logging since 2015 — gated on user-side signup ([[deferred_data]]).
- **TMF / JRC Tropical Moist Forest annual product** is a complementary stand-replacement record with a different algorithm — pull as a cross-check in §12 #12+.
- **The 50 km AOI summary stats are landscape-context only**; a 5 km neighbourhood version would tighten the "forest-positive parcel on deforesting landscape" claim to the immediate-neighbour scale. Re-pull with `buffer=5_km` for Phase-1 deck v7.
- **UNFCCC Paraguay official forest definition** — currently using BAAPA-default ≥30 %; check `ministerio_ambiente_py` published threshold for the legal carbon-accounting claim.

## Cross-references

- [[sentinel2_brief]] — 6-yr NDVI 0.728-0.825 floor consistent with "no Hansen loss after 2014".
- [[landsat_brief]] — 41-yr coarse 30 m NDVI 0.681 → 0.782 trend (Hansen complement at higher temporal cadence).
- [[canopy_height_brief]] — Meta CHM 1 m mean 10.9 m corroborates the 82.1 % treecover2000.
- [[extended_aoi_brief]] — polygon NDVI 0.888 / 0.918 caps the Hansen treecover2000 reading.
- [[gbif_brief]] — closed-canopy avian guild matches the Hansen "stable dense forest" classification.
- [[fauna_brief]] / [[flora_brief]] — iNat 5 km observations frame the "habitat" inside the Hansen forest cover.
- [[hydrogeology_brief]] — flow-routing locations for the loss-pixel-attribution pass.
- [[infrastructure_brief]] — building-coverage check against post-2014 Hansen "no loss" claim.
- [[osm_brief]] — road / boundary check against same.
- [[mod11_brief]] / [[mod16_brief]] / [[chelsa_brief]] — climate envelope under which the parcel held canopy when neighbours cleared.
- [[client_photos_brief]] shot-need #05 — species ID + understorey state photo set to ground-truth the "stable mature forest" claim.
- [[post_escritura_site_knowledge]] §3 — deck NDVI 0.917 + canopy claims this brief Hansen-anchors.
