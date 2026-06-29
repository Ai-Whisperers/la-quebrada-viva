---
name: jrc_gsw_brief
description: JRC Global Surface Water v1.4 (1984-2021) 30 m surface-water occurrence / seasonality / recurrence / transitions over the 50 km AOI and the 30.9 ha Mbopicua polygon — zero water cells inside the parcel across all four layers, AOI ~2% water with ~96 000 new-seasonal cells indicating active regional flood-pulse dynamics.
metadata:
  type: project
---

# JRC GSW v1.4 surface-water brief — La Quebrada Viva (Phase-0 §12 v1)

> JRC Global Surface Water v1.4 (1984-2021) tile `60W_20S` pulled from
> `https://storage.googleapis.com/global-surface-water/downloads2021`.
> Four layers (occurrence, seasonality, recurrence, transitions) over
> the 50 km-buffered AOI rectangle and the 30.9 ha Mbopicua polygon.
> 30 m grid, 38 yr Landsat-derived water-occurrence record.

## Headline

- **Polygon surface-water cells: 0 / 446 across all four layers, every year, every season.** Zero permanent water, zero seasonal water, zero historical occurrence above the 30 m threshold over the full 1984-2021 window.
- **Polygon seasonality max 0 mo/yr, recurrence max 0 %, occurrence max 0 %.** No sub-pixel disambiguation — every JRC cell inside the parcel reads "no water observed since Landsat-5 went live."
- **50 km AOI water footprint 1.74-2.11 % depending on layer** — landscape contains real water bodies (Lago Ypacaraí to the north-east, Tebicuary headwaters, Paraguarí oxbows) but none of them touch the parcel.
- **AOI transitions: 96 296 cells became *new seasonal* water 1984-2021** vs only 5 191 *new permanent* and 3 752 *lost seasonal* — landscape is gaining flood-pulse extent ~26× faster than it is losing it, consistent with the BAAPA-margin agricultural-pond proliferation in the Paraguarí buffer.
- **136 469 cells of permanent water across the AOI** (~12 282 ha) — Lago Ypacaraí and the larger inland reservoirs dominate this signal.
- **Cross-confirms [[sentinel2_brief]] NDWI absence** + **[[hydrogeology_brief]] dry-channel finding** + **[[hansen_gfc_brief]] datamask mean 1.00** — four independent products all agree: the parcel has no surface water at ≥30 m resolution.

## Pull parameters

| Field | Value |
| --- | --- |
| Source | `https://storage.googleapis.com/global-surface-water/downloads2021` |
| Tile | `60W_20S` |
| Centroid | (−57.0355, −25.6073) |
| AOI buffer | 50.0 km |
| AOI bbox | W −57.5350 / E −56.5360 / S −26.0578 / N −25.1568 |
| Pixel size | 30 m × 30 m (1 arcsec native, cos-corrected) |
| Pixel ha | 0.0900 ha nominal |
| Polygon cell count | 446 (same grid as Hansen, covers 30.9 ha geometry) |
| AOI cell count | 14 401 584 |
| Version | v1.4 |
| Vintage | 1984 baseline → 2021 (end-of-Landsat-5/7/8 era) |

## Layer summary — polygon vs AOI

| Layer | AOI valid | AOI nonzero % | Polygon valid | Polygon nonzero % | Polygon max |
| --- | ---: | ---: | ---: | ---: | ---: |
| occurrence (% of valid obs water) | 14 401 584 | 1.74 | 446 | 0.00 | 0 |
| seasonality (months/yr water) | 14 401 584 | 1.70 | 446 | 0.00 | 0 |
| recurrence (% of years with water) | 14 401 584 | 2.11 | 446 | 0.00 | 0 |
| transitions (1984→2021 class) | 14 401 584 | 2.11 | 446 | 0.00 | 0 |

The polygon-zero result is symmetric across all four layers — there is no plausible JRC class that lights up. The parcel is hydrologically "dry" at this resolution.

## AOI transitions histogram (1984-2021)

| Class | Description | AOI cells | AOI ha | Polygon cells |
| ---: | --- | ---: | ---: | ---: |
| 0 | No change / no data (land) | 14 097 894 | 1 268 810 | 446 |
| 1 | Permanent water both periods | 136 469 | 12 282 | 0 |
| 2 | New permanent (became permanent) | 5 191 | 467 | 0 |
| 3 | Lost permanent (was, then gone) | 3 154 | 284 | 0 |
| 4 | Seasonal water both periods | 2 056 | 185 | 0 |
| 5 | New seasonal (became seasonal) | 96 296 | 8 667 | 0 |
| 6 | Lost seasonal (was, then gone) | 3 752 | 338 | 0 |
| 7 | Seasonal → Permanent | 1 149 | 103 | 0 |
| 8 | Permanent → Seasonal | 3 178 | 286 | 0 |
| 9 | Ephemeral permanent | 948 | 85 | 0 |
| 10 | Ephemeral seasonal | 51 497 | 4 635 | 0 |

Read the AOI result as: the wider landscape has 12 282 ha of stable permanent water (large lakes / reservoirs), and is *adding* seasonal water-pulse area at ~8 667 ha gross (+5 of 51 497 ephemeral pulses fired in the window) — landscape-level wetlandisation, not desiccation. None of it touches the parcel.

## Cross-check with other ground-truth

| Source | Claim | JRC GSW agrees? |
| --- | --- | --- |
| [[sentinel2_brief]] | NDWI < 0 wall-to-wall, no open-water cells | Yes — independent confirmation, polygon-zero across both products |
| [[hydrogeology_brief]] | Quebrada channel < 30 m wide, no perennial pool | Yes — sub-30 m channel falls below JRC resolution, correctly absent |
| [[hansen_gfc_brief]] | datamask mean 1.00 (100% land) | Yes — Hansen mask and JRC water layer mutually consistent |
| [[mapbiomas_paraguay_brief]] | Flooded Forest class 0 → 24 px (2015-2023) | Partial — MapBiomas detects sub-30 m flood-pulse gallery that JRC does not; the two products disagree on the *gallery riparian zone* (JRC blind, MapBiomas catches it) |
| [[landsat_brief]] | 41-yr NDVI green floor 0.681 | Yes — sustained vegetation cover incompatible with periodic standing water |
| [[mod16_brief]] | ET 824-1162 mm/yr | Consistent — high ET regime + zero ponded water = water leaves as transpiration not via open-water evaporation |
| [[property_map_brief]] | NDWI raster shows no water cells | Yes — same Sentinel-2 NDWI sub-pixel result, polygon-zero |
| [[client_photos_brief]] shot-need #07 | Wesley site visit to photograph Quebrada channel state | Open — required to validate sub-pixel hydrology that JRC cannot see |

## Engineering implications

- **No perennial pond, lake, or reservoir on parcel.** Any deck claim about "water feature" must be read as either (a) the sub-30 m Quebrada channel (not a JRC water body, gallery riparian only), or (b) a *proposed* designed water feature (pool, reflection pond, retention basin). Do not imply the parcel has standing water at deck time.
- **The 96 296-cell AOI "new seasonal" surge is a regional context datum, not a parcel claim.** It reflects the rural-pond construction boom across BAAPA buffer agriculture (cattle troughs, irrigation reservoirs) and the Lago Ypacaraí periodic flooding. Cite it only as landscape-context for "we are a dry-canopy patch in a flood-pulse-active matrix."
- **JRC blind to the Quebrada gallery.** The 30 m JRC pixel is wider than the channel itself; even when the Quebrada flows after rain, the water column is sub-pixel and surrounded by closed canopy, both of which kill the Landsat water signal. This is a known instrument limitation — the absence of JRC water here is *not* evidence of no flow. Defer to DEM flow-routing ([[hydrogeology_brief]]) + [[mapbiomas_paraguay_brief]] Flooded Forest class (which fires 2015-2023) + shot-need #07 photos for the actual hydrology.
- **MapBiomas Flooded Forest disagreement is informative, not contradictory.** MapBiomas reclassifies dense forest with seasonal sub-canopy water as Flooded Forest (class 6) using a different Landsat-derived signature than JRC. The 24 px MapBiomas signal (post-2015) inside the parcel suggests a gallery-riparian flood pulse that JRC's open-water-only definition misses. The deck-safe phrasing is: "no open standing water at 30 m; sub-canopy seasonal hydrology indicated by MapBiomas." Avoid claiming "no water at all" — claim "no open water visible from space."
- **Designed-water-feature siting** (Phase-1 pool/pond locations) is free of any "remove existing water body" complication. A reflection pond or retention basin is a green-field design, not a restoration of historic water.
- **For groundwater claims** (Wesley's standing data-completeness directive: "better water presence under ground water") JRC GSW is silent. Defer entirely to [[hydrogeology_brief]] for the Guaraní Aquifer / Patiño Aquifer / local water-table depth claims. JRC is a *surface* product only.

## Sub-render typology

- `lqv/subscene/jrc_gsw_aoi_water.py` — 50 km AOI occurrence raster (white→blue ramp, 0-100 %) with parcel polygon outline; load-bearing "we are a dry island in a wetting landscape" infographic. Lago Ypacaraí to the NE will dominate visually — crop or annotate so it does not eat the frame.
- `lqv/subscene/jrc_gsw_transitions_map.py` — AOI transitions raster (11-class categorical palette: stable-permanent dark-blue, new-permanent royal-blue, lost-permanent grey-blue, new-seasonal cyan, lost-seasonal pale-cyan, etc.); 1-row strip for the deck appendix showing the landscape-level flood-pulse dynamics.
- `lqv/subscene/jrc_gsw_polygon_inset.py` — polygon-only crop showing all 446 cells black-on-white (zero-water highlight); used as the literal "0 water pixels" assertion in the deck and the boleto/escritura data appendix.
- `lqv/subscene/jrc_mapbiomas_disagreement.py` — overlay of the 24-px MapBiomas Flooded Forest cells (post-2015) on top of the JRC zero-water polygon raster; shows the gallery-riparian-only signal that requires sub-pixel ground-truth. Implementation gated on [[mapbiomas_paraguay_brief]] per-pixel transition raster.
- `lqv/subscene/jrc_gsw_pond_proposal.py` — *deferred* until Phase-1 architectural design picks a pond/pool location; renders the proposed feature on top of the JRC-zero polygon as the "no existing water to remove" siting argument.

## Provenance

- **Source URL:** `https://storage.googleapis.com/global-surface-water/downloads2021/<layer>/<layer>_60W_20S_v1_4_2021.tif`
- **Citation:** Pekel, J.-F., Cottam, A., Gorelick, N., Belward, A. S. (2016) "High-resolution mapping of global surface water and its long-term changes." *Nature* 540: 418-422. Data version v1.4 (2021 update).
- **License:** CC-BY-4.0 (European Commission Joint Research Centre).
- **Pulled:** 2026-06-29 by AI Whisperers via direct GCS HTTP fetch (no auth required).
- **Outputs:** 4 AOI rasters + 4 polygon-clipped rasters + 4 PNG previews + summary.md (this brief synthesizes summary.md into the canonical template).
- **Coordinate system:** EPSG:4326 native; reprojection to EPSG:32721 (UTM 21S) deferred to Blender-mesh time.

## Carry-forward gaps

- **JRC Monthly History 2022-2025** — v1.4 ends 2021. Pull `JRC/GSW1_4/MonthlyHistory` via GEE for the post-vintage years to capture any new BAAPA-margin pond construction near the parcel. Gated on [[deferred_data]] GEE-auth.
- **JRC Monthly Recurrence 2015-2023 polygon-clip** — the existing brief uses yearly aggregates; a monthly-resolution clip would reveal *when* the Quebrada pulses (matching the MapBiomas Flooded Forest 2015 emergence) and could be cross-walked against [[chirps_brief]] rainfall.
- **Sub-30 m hydrography** — Quebrada channel + minor arroyos are JRC-invisible. Resolve via drone SfM + 0.5 m NDWI ([[property_map_v2]] §3 plan) and DEM flow-routing ([[hydrogeology_brief]]).
- **Groundwater table depth** — JRC silent. Drill a piezometer (Phase-1 hydrology budget line) or pull the SNC water-table contour map for Paraguarí ([[deferred_data]] R6). Required for foundation-design groundwater claims.
- **Water-feature catchment area** — once Phase-1 sites a pond/pool, derive the upstream catchment from the Cop30 DEM and compute its rainfall-driven yield ([[chirps_brief]] × [[mod16_brief]] water balance).
- **Lago Ypacaraí trophic-state cross-reference** — the AOI's dominant permanent-water signal is Ypacaraí, a known eutrophic lake. If the deck cites the lake as a regional amenity / day-trip context, attach a water-quality caveat (Itaipu Binacional + MADES public data).

## Cross-references

- [[sentinel2_brief]] — NDWI sub-pixel water search; agrees on polygon-zero water.
- [[landsat_brief]] — 41-yr NDVI floor 0.681; sustained canopy incompatible with periodic open water.
- [[hansen_gfc_brief]] — datamask mean 1.00 cross-confirms polygon-as-land.
- [[mapbiomas_paraguay_brief]] — Flooded Forest 24 px post-2015; the gallery-riparian sub-canopy hydrology JRC misses.
- [[canopy_height_brief]] — 10.9 m canopy mean; closed canopy is the reason JRC cannot see the Quebrada from above.
- [[hydrogeology_brief]] — DEM flow-routing + Guaraní/Patiño Aquifer context; load-bearing for any groundwater claim.
- [[extended_aoi_brief]] — AOI rectangle hydrology context.
- [[infrastructure_brief]] — no on-parcel water infrastructure (no irrigation pond, no pump house).
- [[osm_brief]] — no OSM `natural=water` features inside parcel; cross-confirms.
- [[mod16_brief]] — high ET regime; water leaves as transpiration, not standing-water evaporation.
- [[chirps_brief]] — rainfall driver for any sub-pixel flood-pulse; required for JRC-MapBiomas reconciliation.
- [[property_map_brief]] — NDWI raster cross-check, same polygon-zero result.
- [[client_photos_brief]] shot-need #07 — Quebrada channel ground-truth photo set; required to validate sub-30 m hydrology JRC cannot see.
- [[post_escritura_site_knowledge]] — deck-level "we are a dry-canopy patch" framing this brief JRC-anchors.
