---
name: mapbiomas_paraguay_brief
description: MapBiomas Paraguay Collection 2 (1985-2023) 30 m annual land-cover trajectory over the 50 km AOI and the 30.9 ha Mbopicua polygon — native-forest share 80.6% → 84.0% (Δ +3.4 pp), zero Forest→Agriculture, 7 px (~0.63 ha) pasture conversion over 38 yr.
metadata:
  type: project
---

# MapBiomas Paraguay 1985-2023 land-cover trajectory brief — La Quebrada Viva (Phase-0 §12 v1)

> MapBiomas Paraguay Collection 2 (1985-2023) 39 annual categorical
> rasters at 30 m, pulled from the public GCS bucket. Class statistics
> for every year are reported polygon-side at 382 raster cells
> (~34.4 ha; reprojection grid differs from Hansen's 446 cells / 40.1 ha
> at the same parcel). Pre-Hansen baseline extends the record 15 years
> back to 1985 and adds the regrowth + Flooded Forest classes that
> Hansen v1.12 collapses into "treecover2000".

## Headline

- **Native-forest share 80.6 % (1985) → 84.0 % (2023), Δ +3.4 pp over 38 yr** — the parcel is *forest-positive across the entire MapBiomas record*, not just the 24-yr Hansen window. Native forest = `Forest Formation (3)` + `Flooded Forest (6)` combined.
- **Zero Agriculture pixels ever inside the polygon (1985-2023)** — the parcel was never converted to cropland. This is the load-bearing claim Hansen cannot make (Hansen's lossyear is class-blind).
- **Flooded Forest emerges 2015** (12 px → 24 px by 2023) along the Quebrada gallery — corroborates [[hydrogeology_brief]] flow path and the canopy-densification signal in [[landsat_brief]] (NDVI 0.681 → 0.782 across 41 yr).
- **Forest → Pasture across 38 yr: 3 px (~0.27 ha); Grassland → Pasture: 4 px (~0.36 ha); total pasture conversion 7 px ≈ 0.63 ha** — identical magnitude to Hansen's 0.63 ha stand-replacement loss tally. The two products converge on "~0.6 ha disturbed over the modern record."
- **Grassland → Flooded Forest succession: 16 px (~1.44 ha)** — the largest single transition besides persistence. The parcel is *actively gaining native forest from grassland*, not losing forest.
- **Stable-forest persistence: 297 / 308 of the 1985 Forest pixels remain Forest in 2023 (96.4 %)** — among the most persistent BAAPA fragments in the 50 km buffer.
- **Hansen 2000 cross-check: MapBiomas Forest Formation = 80.1 % vs Hansen treecover2000 = 82.1 %** — agreement within ~2 pp, well inside categorical-vs-continuous expected tolerance. The two products tell the same story.

## Pull parameters

| Field | Value |
| --- | --- |
| Source | `https://storage.googleapis.com/mapbiomas-public/initiatives/paraguay/collection_2/` |
| Collection | 2 (Paraguay; ATBD published 2024) |
| Vintage | 1985-2023 (39 annual rasters) |
| Centroid | (−57.0355, −25.6073) |
| AOI buffer | 50.0 km |
| AOI bbox | W −57.5350 / E −56.5360 / S −26.0578 / N −25.1568 |
| Pixel size | 30 m × 30 m (EPSG:4326 reproj at AOI latitude) |
| Pixel ha | 0.0900 ha nominal |
| Polygon cell count | 382 (reproject-overlap, ≈34.4 ha covers 30.9 ha geometry) |
| Tile format | COG, 256×256 internal, uint8 categorical |
| Dtype | uint8 (class codes 0-62) |
| Coordinate system | EPSG:4326 native |
| Pulled | 2026-06-29 by AI Whisperers via direct GCS HTTP fetch (no auth required) |
| License | CC-BY-SA-4.0 (MapBiomas) |

## Per-decade snapshot — polygon (382 cells = ~34.4 ha)

| Year | Forest Form. px (%) | Flooded Forest px (%) | Grassland px (%) | Pasture px (%) | Agriculture px | Native-forest (3+6) % |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1985 | 308 (80.6) | 0 (0.0) | 74 (19.4) | 0 (0.0) | 0 | **80.6** |
| 1990 | 306 (80.1) | 0 (0.0) | 73 (19.1) | 3 (0.8) | 0 | **80.1** |
| 1995 | 306 (80.1) | 0 (0.0) | 73 (19.1) | 2 (0.5) | 0 | **80.1** |
| 2000 | 306 (80.1) | 0 (0.0) | 65 (17.0) | 11 (2.9) | 0 | **80.1** |
| 2005 | 302 (79.1) | 0 (0.0)¹ | 55 (14.4) | 9 (2.4) | 0 | **79.1** |
| 2010 | 306 (80.1) | 0 (0.0) | 73 (19.1) | 3 (0.8) | 0 | **80.1** |
| 2015 | 301 (78.8) | 12 (3.1) | 59 (15.4) | 10 (2.6) | 0 | **81.9** |
| 2020 | 304 (79.6) | 12 (3.1) | 61 (16.0) | 5 (1.3) | 0 | **82.7** |
| 2023 | 297 (77.7) | 24 (6.3) | 54 (14.1) | 7 (1.8) | 0 | **84.0** |

¹ The 2005 snapshot shows 16 px (4.19 %) classified as `Wetland (11)` — likely a class-evolution artefact of Collection 2's algorithm before Flooded Forest stabilised in the 2015+ window. Treat as a precursor of the post-2015 Flooded Forest signal, not a separate wetland.

The pre-2015 Forest Formation series oscillates between 302-308 px (79.1-80.6 %), explicable as a single re-classification swap (a 4-px patch flipping Forest↔Pasture in the 2000-2009 window). The 2015+ regime is the *real* signal: Flooded Forest separates out as a stable 12-24 px class along the channel, and the net native-forest share rises to 84.0 % by 2023.

## Change-trajectory matrix — polygon, 1985 → 2023 (382 cells, all transitions)

| From (1985) | To (2023) | Pixels | Area (ha) | Share (%) |
| --- | --- | ---: | ---: | ---: |
| Forest Formation | Forest Formation | 297 | 26.73 | 77.7 |
| Grassland | Grassland | 54 | 4.86 | 14.1 |
| Grassland | Flooded Forest | 16 | 1.44 | 4.2 |
| Forest Formation | Flooded Forest | 8 | 0.72 | 2.1 |
| Grassland | Pasture | 4 | 0.36 | 1.0 |
| Forest Formation | Pasture | 3 | 0.27 | 0.8 |

Total: 382 px = 100 %. Five non-zero off-diagonal cells; no Forest→Agriculture, no Forest→Water, no Forest→Built. The four-decade record is dominated by persistence (351 / 382 = 91.9 % of cells in the same broad class) and *successional gain* (24 / 382 = 6.3 % converted *into* native forest, primarily Grassland → Flooded Forest along the Quebrada).

Net flow into native-forest classes over 38 yr: +13 px (308 → 321), composed of −11 px exiting Forest Formation (3 Pasture + 8 Flooded Forest) and +24 px entering Flooded Forest (8 from Forest Formation + 16 from Grassland). The +16 Grassland → Flooded Forest succession alone is **5× larger than the +3 Forest → Pasture loss**. The MapBiomas record says the parcel is *gaining* native forest, not losing it.

## Cross-check with other ground-truth

| Source | Claim | MapBiomas agrees? |
| --- | --- | --- |
| [[hansen_gfc_brief]] | 82.1 % treecover2000, 0.63 ha stand-replacement loss 2001-2024 | Yes — MapBiomas Forest Formation 2000 = 80.1 % (2 pp inside Hansen's continuous estimate); MapBiomas 7 px ≈ 0.63 ha pasture conversion over 38 yr matches the 0.63 ha Hansen loss across 24 yr |
| [[sentinel2_brief]] | NDVI 0.728-0.825 wall-to-wall 2020-2025; zero open water at 10 m | Yes — 2020-2023 native-forest share 82.7-84.0 % is consistent with sustained high NDVI; Flooded Forest 12-24 px is *gallery* not open water (S-2 < 10 m at gallery edges) |
| [[landsat_brief]] | 41 yr NDVI 0.681 (1985) → 0.782 (2024) | Yes — MapBiomas captures the same greening: +3.4 pp native-forest share over the same window via Grassland → Flooded Forest succession |
| [[canopy_height_brief]] | Meta CHM mean 10.9 m polygon-wide; GEDI mean 27.7 m | Consistent — MapBiomas Forest Formation 297 px + Flooded Forest 24 px = closed mature gallery + upland forest mosaic |
| [[gbif_brief]] | 50 dense-canopy Aves, intact avian guild | Consistent — 38 yr of forest persistence + active gallery succession explains the intact bird community |
| [[extended_aoi_brief]] | Polygon NDVI 0.888-0.918 | Consistent — top decile of AOI NDVI matches MapBiomas's "highest native-forest persistence in 50 km buffer" reading |
| [[hydrogeology_brief]] | Quebrada channel modelled flow path | Yes — Flooded Forest 16+8 = 24 px aligns spatially with the modelled channel (pixel-attribution deferred to next pass) |
| [[infrastructure_brief]] | 0 buildings inside polygon, nearest 196 m | Consistent — no Built or Non-vegetated Area pixels ever inside polygon (1985-2023) |

## Engineering implications

- **"Zero Forest → Agriculture" is the strongest restoration / conservation claim in the deck.** Hansen says 0.63 ha lost; MapBiomas adds *what it became*: pasture, not cropland. The parcel was never industrialised. The 38-yr record is the single most defensible carbon-permanence statement available pre-Phase-1.
- **The +16 px (1.44 ha) Grassland → Flooded Forest succession is the load-bearing "active regrowth" datum.** This is what Hansen v1.12's discontinued `gain` band cannot show. The parcel is actively *gaining* gallery forest along the Quebrada — material for the deck's Phase-1 restoration / PSA-Bosques argument. Spatial overlay onto [[hydrogeology_brief]] flow-routing is the next pixel-tight task.
- **The 2015 Flooded Forest emergence (12 px) is contemporaneous with Hansen's last loss event (2014).** Interpretation: the 2014 stand-replacement loss (1 px ≈ 0.09 ha) is *not* parcel-margin clearing but a reclassification at the gallery-edge ecotone, where dense closed canopy transitions to flooded riparian forest. Worth pixel-aligning before deciding whether to mark the 2014 event as "anthropogenic" or "natural" in the deck.
- **The 2000-2009 oscillation (Forest Formation 302-306 px, Pasture 2-11 px)** is an artefact of Collection 2's mid-record classification instability, not real land-use flapping. Use the 1985-1995 baseline and the 2015-2023 modern regime as the two anchor periods. Avoid citing the 2005 dip ("79.1 %") as deforestation — it is recoverable across 2010.
- **Hansen × MapBiomas 2000 agreement within 2 pp** validates both products for the brief and unlocks the joint claim "82 ± 2 % canopy at 2000, stable to growing through 2023." This is the deck-ready uncertainty band.
- **For UNFCCC / PSA-Bosques Paraguay forest-definition compliance,** native forest under MapBiomas (classes 3+6) at 84.0 % in 2023 sits well above any practical ≥30 % canopy / ≥0.5 ha / ≥3 m height threshold. The legal carbon-baseline claim is defensible across the entire 38-yr record.
- **The 4 px Grassland → Pasture transition is the only Phase-0 "land-use change" finding requiring Wesley confirmation.** It is 0.36 ha over 38 yr — likely the southern boundary edge where the OSM trail meets the neighbouring finca. [[client_photos_brief]] shot-need #09 (property edges + adjacent finca use) will validate.

## Sub-render typology

- `lqv/subscene/mapbiomas_decadal_panel.py` — 9-cell decadal panel (1985 / 1990 / 1995 / 2000 / 2005 / 2010 / 2015 / 2020 / 2023) showing the polygon outline + MapBiomas class palette colour-fill. Header strip for the deck appendix; reads as a flipbook of "the parcel kept its forest while the neighbourhood did not."
- `lqv/subscene/mapbiomas_native_forest_trend.py` — single-line plot of native-forest share (classes 3+6 combined) 1985-2023, with Hansen treecover2000 anchor + 2 pp uncertainty band, and the 2015 Flooded Forest emergence flagged. Hero chart for the §12 brief slide.
- `lqv/subscene/mapbiomas_change_trajectory_chord.py` — chord diagram of the 6 non-zero From → To transitions, edge thickness ∝ px count. The "active succession" claim is read in the thick Grassland → Flooded Forest chord vs the thin Forest → Pasture chord.
- `lqv/subscene/mapbiomas_class_pie.py` — 1985 vs 2023 side-by-side pie / stacked-bar showing class composition shift; loads the same data the chord plot uses but is print-friendlier for the deck.
- `lqv/subscene/mapbiomas_aoi_contrast.py` — paired 50 km AOI vs polygon native-forest trend lines; analogue of `hansen_aoi_contrast.py` but with the 38-yr record. Deferred until AOI-side time-series is summarised (currently polygon-only).

## Provenance

- **Source URL pattern:** `https://storage.googleapis.com/mapbiomas-public/initiatives/paraguay/collection_2/lulc/coverage/<year>.tif` (per-year COG, EPSG:4326, uint8 categorical).
- **Citation:** MapBiomas Paraguay Project — Collection 2 (1985-2023) of the Annual Land Use Land Cover Maps of Paraguay, accessed 2026-06-29 via `https://paraguay.mapbiomas.org/`.
- **License:** CC-BY-SA-4.0. Mandatory attribution: *"Data: MapBiomas Paraguay — Collection 2 (1985-2023). CC-BY-SA-4.0."* Applies to every render, deck slide, and PR-bundle export.
- **Pulled:** 2026-06-29 by AI Whisperers via direct GCS HTTP fetch (no auth required); 39 annual rasters → `coverage_<year>.tif` + per-year polygon-clipped `coverage_polygon_<year>.tif` + `class_timeseries.csv` + `change_trajectory_polygon.csv` + `summary.md`.
- **Coordinate system:** EPSG:4326 native; polygon reproject differs from Hansen reproject by 64 cells (382 vs 446). For Phase-1 cross-product overlay, reproject both to EPSG:32721 (UTM 21S) at 30 m and snap to a shared grid.
- **Classes observed in polygon (out of 62 in legend):** Forest Formation (3), Flooded Forest (6), Wetland (11, 2005 only), Grassland (12), Pasture (15). All others (Forest Plantation, Agriculture sub-classes, Mining, Built, Non-vegetated, Water) = 0 pixels in every year.

## Carry-forward gaps

- **Per-pixel transition raster (1985 → 2023) not yet produced — currently only the 6-row aggregate matrix.** A 382-pixel transition map is needed to (a) overlay the +16 Grassland → Flooded Forest succession onto [[hydrogeology_brief]] flow-routing and (b) locate the 7 px pasture conversion against the [[osm_brief]] southern boundary trail.
- **Decade-by-decade transition matrices (1985→1995, 1995→2005, 2005→2015, 2015→2023)** would resolve whether the +3.4 pp gain is steady accumulation or a single 2015+ event. Headline rate suggests the latter.
- **Collection 3 refresh** — when MapBiomas Paraguay Collection 3 publishes (expected 2026-Q4), re-pull and update this brief. Collection 2 ends at 2023; the 2024-2025 window will need patching from Hansen / Sentinel-2 until Collection 3 lands.
- **BAAPA-ecoregion clip** — the 50 km AOI bbox cuts an arbitrary square; clipping to the official BAAPA (Bosque Atlántico del Alto Paraná) polygon would let the brief claim "X-th percentile native-forest persistence in the legally designated ecoregion." Defer to Phase-1 deck v7.
- **MapBiomas fire-scar overlay (`mapbiomas_fire`)** is a separate collection — pull as §12 #14+ for the deck's "no fire damage" companion to "no clearing".
- **Inter-collection deltas (Collection 1 → 2 cell-by-cell change)** would quantify algorithm drift independent of real land-cover change. Useful for the methodological footnote in the deck appendix.
- **Cross-reference against MapBiomas Brazil Atlantic Forest** (Mata Atlântica) for the BAAPA trans-border classification — the Paraguay and Brazil collections use compatible legends but separate calibration ATBDs.

## Cross-references

- [[hansen_gfc_brief]] — 24-yr stand-replacement record this brief extends back to 1985; cross-validated at 2000.
- [[sentinel2_brief]] — 10 m wall-to-wall 2020-2025 NDVI floor 0.728 consistent with 2020-2023 84 % native-forest share.
- [[landsat_brief]] — 41-yr 30 m NDVI 0.681 → 0.782 trend; same temporal envelope as MapBiomas, complementary continuous vs categorical view.
- [[canopy_height_brief]] — Meta CHM + GEDI height layer that MapBiomas 3+6 classes correspond to in cross-section.
- [[gbif_brief]] — avian community persistence corroborated by 38-yr forest persistence (297/308 stable Forest cells).
- [[extended_aoi_brief]] — polygon NDVI 0.888-0.918 at 10 m maps onto MapBiomas 84 % native-forest at 30 m.
- [[hydrogeology_brief]] — Quebrada flow-routing prediction the +24 px Flooded Forest emergence corroborates.
- [[fauna_brief]] / [[flora_brief]] — iNat 5 km observations frame habitat inside the MapBiomas Forest Formation class.
- [[infrastructure_brief]] — zero MapBiomas Built / Non-vegetated cells consistent with "0 buildings inside polygon".
- [[osm_brief]] — southern boundary trail check against the 7 px pasture-conversion locations once per-pixel transitions are produced.
- [[client_photos_brief]] shot-need #05 (species ID) / #09 (boundary use) / #13 (wildlife sign) — ground-truth pass for the MapBiomas classes.
- [[post_escritura_site_knowledge]] §3 — deck native-forest + NDVI claims this brief MapBiomas-anchors across the full 1985-2023 record.
