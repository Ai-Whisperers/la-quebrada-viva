---
name: property_map_v2_brief
description: Property map v2 indexed data spine (13 batches A-K‴, 86-species candidate pool, 437-species biodiversity envelope, MS Open Buildings 737 polys reach, triple-confirmed zero open water, 41-yr NDVI history, 6-mo S1 SAR, MapBiomas + Hansen forest tracking, SoilGrids profile, 50 km comparables ring) over the 30.9 ha Mbopicua polygon — successor to the v1 composite, canonical for the deck data tables and the digital-twin pull.
metadata:
  type: project
---

# Property map v2 brief — La Quebrada Viva (Phase-0 §12 v2, indexed data spine)

> Successor to the v1 composite. v1 stays canonical for the 300 dpi
> polygon-clip PNG; **v2 is the indexed data spine the deck and the
> digital twin pull from**. 13 batches (A-K‴) integrate Cop30
> hydrography, OSM, 50 km comparables, 86-species Atlantic Forest pool,
> 437-species biodiversity envelope, MS Open Buildings ML pass,
> SoilGrids profile, 5-yr S2 timeseries, 6-mo S1 RTC SAR, 41-yr Landsat
> NDVI, Hansen GFC v1.12, Mapbiomas Paraguay Coll 2, JRC GSW v1.4.

## Headline

- **v1 → v2 delta is *evidence depth*, not *evidence direction*** — every v1 claim survives v2 cross-checks. The novel additions are temporal (1984-2025 surface water, 1985-2023 native forest, 1985-2025 NDVI), areal (50 km comparables ring + 25 km biodiversity envelope), and resolutional (MS Open Buildings ML + SoilGrids 250 m).
- **Triple-confirmed 0 % open water** across (i) S-2 AWEIsh −0.677 / NDWI −0.706 / MNDWI −0.581, (ii) S-1 SAR VV −8.33 dB > −15 dB threshold, (iii) JRC GSW v1.4 zero polygon cells across 1984-2021 in all 4 layers. The polygon has been dry land for the entire Landsat era.
- **Hansen GFC v1.12** 82.1 % treecover2000, 0.63 ha cumulative stand-replacement loss 2001-2024, 0 gain pixels. **Mapbiomas Paraguay Coll 2** native forest **80.6 % (1985) → 84.0 % (2023)**, Δ +3.4 pp. The polygon is forest-positive on a 4.94 %-loss landscape (≈3× below AOI deforestation rate).
- **41-year Landsat NDVI** mean +0.696, peak +0.782 in 2024, drought floor +0.564 in 2003. **5-yr Sentinel-2 NDVI** mean +0.773 across 12 scenes 2020-H1 → 2025-H2. The 1985 → 2025 trajectory is monotonically greening with one 2003 drought scar.
- **Mbopicua scope-lock 30.9 ha** (Wesley KML) holds across every batch. The buildable cluster is the canonical AOI; the broader 62 ha boleto purchase, the 50 km comparables ring, and the 25 km biodiversity envelope are framing-only.
- **86 candidate tree species** in the Atlantic Forest 25 km pool (most-cited *Trichilia catigua* 61 occ; lapacho present at 1 occ). **437 GBIF species + 727 iNat observations** in the 25 km biodiversity envelope; **0 IUCN-threatened** at the 25 km scale (corrected from earlier 1 false-positive).
- **MS Open Buildings** 737 polygons / 59 947 m² in the AOI ±1 km ring; nearest neighbour 196 m S, 17 m² shed-scale. Extends OSM's 9-polygon S-boundary cluster downward to ML-resolution shed-scale; **still 0 polygons inside the polygon**.
- **JRC GSW v1.4 ↔ Mapbiomas disagreement on "wetland"** is informative not contradictory: JRC measures open-water occurrence only (zero); Mapbiomas Flooded Forest class registers seasonally-flooded forest (small but nonzero). Polygon is dry land + flood-prone gallery forest along the Quebrada axis.
- **Photo-verification register** (14-row cross-ref, sibling [[property_map_brief]] §photo_verification) is the promotion path — v2 layers stay 🛰️ until Wesley's 2026-07-27 → 2026-08-27 intake closes. R35 (drone LiDAR / sub-1 m imagery) is the only unlock for per-stem species ID.

## Pull parameters

| Field | Value |
| --- | --- |
| v1 baseline | [[property_map_brief]] (300 dpi composite, 2026-06-28) |
| Polygon | Wesley KML, 30.9 ha Mbopicua cluster, EPSG:4326 |
| Indexed-spine vintage | 2026-06-28 (T+1) post-escritura |
| Raster compute CRS | EPSG:32721 (UTM 21S) |
| Vector storage CRS | EPSG:4326 |
| Batch count | 13 (A, B, C, D, E, F, G, H, I, J, K, K′, K″, K‴) |
| Compute drivers | `scripts/build_property_map.py` (composite), `scripts/analyze_stream.py` (D8), 12 ad-hoc batch pullers in `scripts/phase0_*.py` |

## Batch index — what each letter pulled

| Batch | Source | Resolution | Vintage | Polygon-clip output | Brief |
| --- | --- | --- | --- | --- | --- |
| A | Sentinel-2 (Element84 STAC) | 10 m | 2026-05-12 single date | 4-bin NDVI + NDWI + composite | [[property_map_brief]] |
| B | Copernicus GLO-30 DEM (OpenTopography) | 30 m | 2025 mosaic | D8 flow-routing 15 LineStrings, threshold ≥30 cells | [[hydrogeology_brief]] |
| C | OSM Overpass | vector | 2026-06-28 | 9 buildings (all S), 1 road, 2 farmland | [[property_map_brief]] |
| D | OSM + WDPA + 50 km comparables ring | mixed | 2026-06-28 | 401 WDPA-locked + 5 OSM protected-areas | [[comparables_brief]] |
| E | Atlantic Forest tree DB (GBIF subset, 25 km) | point | 1850-2025 | 86 candidate species; *Trichilia catigua* 61 occ | [[atlantic_forest_trees_brief]] |
| F | GBIF + iNat biodiversity, 25 km envelope | point | 1850-2025 | 437 spp + 727 obs; 0 IUCN-threatened | [[biodiversity_25km_brief]] |
| G | MS Open Buildings v3 | ML polygon | 2023 vintage | 737 polys / 59 947 m² in AOI ±1 km; 196 m nearest | [[infrastructure_brief]] |
| H | ISRIC SoilGrids v2.0 | 250 m | 2020 vintage | pH 5.3, clay-increasing argillic horizon | [[soilgrids_brief]] |
| I | Sentinel-2 timeseries | 10 m | 2020-H1 → 2025-H2 (12 scenes) | NDVI mean +0.773, floor 0.728 | [[sentinel2_brief]] |
| J | Sentinel-1 RTC γ⁰ | 10 m | 6-mo (Apr-Oct 2026, 14 scenes) | VV −8.33 dB, VH −14.09 dB, VV−VH +5.76 dB | [[sentinel1_brief]] |
| K | Landsat 4/5/7/8/9 annual | 30 m | 1985-2025 (41 yr) | NDVI mean +0.696, 2024 peak +0.782, 2003 floor +0.564 | [[landsat_brief]] |
| K′ | Hansen GFC v1.12 | 30 m | 2000 baseline + 2001-2024 loss | 82.1 % treecover2000, 0.63 ha loss, 0 gain | [[hansen_gfc_brief]] |
| K″ | Mapbiomas Paraguay Coll 2 | 30 m | 1985-2023 (39 yr) | Native forest 80.6 → 84.0 % Δ +3.4 pp | [[mapbiomas_paraguay_brief]] |
| K‴ | JRC GSW v1.4 | 30 m | 1984-2021 | Polygon-zero across 4 layers, AOI landscape-wetlandisation ≈26× | [[jrc_gsw_brief]] |

## v1 → v2 delta — what's new

| Theme | v1 (single date) | v2 (multi-source / multi-decade) | Direction |
| --- | --- | --- | --- |
| Canopy NDVI | 4-bin S-2 2026-05-12 | 12-scene S-2 timeseries 2020-2025 + 41-yr Landsat 1985-2025 | Confirms greening, +0.696 → +0.782 |
| Forest cover | NDVI proxy | Hansen 82.1 % + Mapbiomas 80.6 → 84.0 % | Multi-decade absolute baseline |
| Forest loss | Not measured | Hansen 0.63 ha 2001-2024 + Mapbiomas Δ +3.4 pp | Forest-positive trajectory |
| Surface water | NDWI 2026-05-12 single date | NDWI + AWEIsh + MNDWI + S-1 SAR + JRC GSW 1984-2021 | Triple-zero confirmed |
| Stream network | 15 D8 LineStrings | Same + S-1 SAR moisture cross-check + JRC zero | DEM streams remain canonical |
| Buildings | 9 OSM polys S of polygon | + 737 MS Open Buildings ML in AOI ±1 km | 0 on-property holds at ML resolution |
| Roads | 1 OSM road `Camino a Escobar` | Same + MS Open Buildings non-road | OSM remains canonical |
| Soil | Not pulled | SoilGrids 250 m (pH 5.3, argillic horizon, clay-increasing) | Phase-1 unlock for foundation + drainage |
| Tree species | None | 86 Atlantic Forest candidates (25 km pool) | Per-stem ID still gated on R35 |
| Threatened flora | None | 0 IUCN-threatened at 25 km (corrected) | Conservation framing clarified |
| Fauna | None | 437 GBIF spp + 727 iNat obs (25 km) + 50 dense-canopy Aves (5 km) | Habitat envelope quantified |
| Protected areas | None | 401 WDPA-locked + 5 OSM in 50 km ring | Comparables framing |
| Radar | None | S-1 RTC γ⁰ 14 scenes | Closed-canopy confirmation |
| Burn history | None | Mapbiomas Fire (gated, deferred) + Landsat NDVI dip 2003 | Single 2003 drought scar |

## Cross-check with other briefs

| Source | Claim | property_map_v2 agrees? |
| --- | --- | --- |
| [[sentinel2_brief]] | NDVI floor 0.728, mean 0.773 across 2020-2025 | Yes — Batch I direct source |
| [[sentinel1_brief]] | VV −8.33 dB closed-canopy, no flooded patches | Yes — Batch J direct source; supports triple-zero water |
| [[landsat_brief]] | 41-yr NDVI mean +0.696, peak +0.782 in 2024 | Yes — Batch K direct source |
| [[hansen_gfc_brief]] | 82.1 % treecover2000, 0.63 ha loss, 0 gain | Yes — Batch K′ direct source |
| [[mapbiomas_paraguay_brief]] | Native forest 80.6 → 84.0 %, Δ +3.4 pp | Yes — Batch K″ direct source |
| [[jrc_gsw_brief]] | Zero polygon cells, AOI landscape-wetlandisation ≈26× | Yes — Batch K‴ direct source; the JRC ↔ Mapbiomas Flooded Forest tension is *informative*, not a contradiction |
| [[canopy_height_brief]] | Meta CHM 1 m mean 10.9 m | Yes — corroborates Hansen 82 % treecover2000 + Mapbiomas dense bins |
| [[soilgrids_brief]] | pH 5.3, argillic horizon | Yes — Batch H direct source |
| [[infrastructure_brief]] | MS Open Buildings 737 polys, nearest 196 m S | Yes — Batch G direct source; extends OSM v1 |
| [[atlantic_forest_trees_brief]] | 86 candidate species, *Trichilia catigua* 61 occ | Yes — Batch E direct source |
| [[biodiversity_25km_brief]] | 437 GBIF + 727 iNat, 0 IUCN-threatened | Yes — Batch F direct source |
| [[comparables_brief]] | 401 WDPA-locked + 5 OSM in 50 km ring | Yes — Batch D direct source |
| [[hydrogeology_brief]] | 15 D8 LineStrings, threshold ≥30 cells | Yes — Batch B direct source |
| [[property_map_brief]] | v1 composite at 300 dpi, polygon-clip canonical | v2 is downstream-of; v1 stays canonical for the PNG |
| [[client_photos_brief]] | 14-row register at `client_photos/2026-06_post_escritura/index.md` | Yes — v2 promotion gated on intake window 2026-07-27 → 2026-08-27 |

## Engineering implications

- **v2 is the canonical data spine for the deck and the digital twin** — every chart, every claim, every site-knowledge sentence draws from these 13 batches. v1 stays canonical for the composite PNG specifically because the v1 driver (`build_property_map.py`) produces the byte-identical 300 dpi page used in the frozen escritura bundle. Re-rendering v1 risks invalidating the bundle hash; keep them separate.
- **Triple-zero water is now defensible against any review** — single-date NDWI is the weakest of the three; the 1984-2021 JRC GSW historical record at 30 m is the strongest. For Wesley-side claims, lead with JRC ("no surface water in any of the 38 Landsat years"). For engineering claims (Phase-1 designed water feature), lead with S-1 VV (−8.33 dB > −15 dB = closed canopy, no waterlogged understory). NDWI single-date is the weakest leg; never cite alone.
- **The forest-positive trajectory is the marketable conservation claim** — 3× below AOI deforestation + +3.4 pp Mapbiomas gain + 0 gain pixels in Hansen (Hansen gain is 2000-2012 only, so gain absence is methodological not biophysical — disclose this). Combined narrative: *"the parcel held its 1985 forest cover through 39 years of regional deforestation."*
- **The 86-species pool is candidate-only at v2 resolution** — none of the 13 batches resolves per-stem species ID. R35 (drone LiDAR or sub-1 m NICFI + DeepForest crown detection) is the unlock; until then, the deck claims "diverse Atlantic Forest community within 25 km" not "X species on-site." See [[research_gaps]] R35.
- **The 437-species biodiversity envelope at 25 km is framing-only** — the polygon-scale fauna inference is the 50 dense-canopy Aves community in [[gbif_brief]] (5 km buffer). The 25 km envelope is "regional pool" framing; do not say "437 species on the property."
- **MS Open Buildings ML extends OSM but does not refute it** — 737 polys in ±1 km AOI is the regional density; 0 on-property is the v1 OSM finding extended at ML resolution. For Phase-1 site layout this is the strongest "vacant land" evidence available pre-photo.
- **SoilGrids 250 m profile is the Phase-1 foundation + drainage input** — pH 5.3 (acid, gallery-forest typical), clay-increasing argillic horizon. Limits siting decisions for septic + foundation; the 250 m resolution is too coarse for per-cabin micro-siting (drone LiDAR / on-site borings unlock that).
- **The deck must show v2 batch index** — readers ask "how do you know X?"; the per-batch index table answers in 13 rows. Keep the index table on a single deck page.
- **JRC ↔ Mapbiomas disagreement is the only "tension" in v2** — handle by re-framing: JRC measures *open water*, Mapbiomas Flooded Forest measures *closed-canopy seasonally-flooded forest*. Both can be true (and are). Do not let a reader think the two products contradict.

## Sub-render typology

- `lqv/subscene/property_v2_batch_index.py` — 13-row batch index table over polygon outline; deck-page anchor showing every source and its resolution.
- `lqv/subscene/property_v2_canopy_history.py` — 41-yr Landsat NDVI line + 39-yr Mapbiomas native-forest area line + Hansen 24-yr treecover2000 bar; load-bearing "forest-positive trajectory" infographic.
- `lqv/subscene/property_v2_water_triple_zero.py` — 3-panel page: NDWI median heatmap + S-1 VV histogram + JRC GSW 1984-2021 occurrence raster; load-bearing triple-zero confirmation.
- `lqv/subscene/property_v2_buildings_reach.py` — polygon outline + 9 OSM polys + 737 MS Open Buildings polys with 1 km buffer; load-bearing "vacant land at ML resolution" page.
- `lqv/subscene/property_v2_biodiversity_envelope.py` — 25 km buffer polygon + GBIF point density + iNat observation count + 0 IUCN-threatened annotation; framing-only deck page.
- `lqv/subscene/property_v2_comparables_ring.py` — 50 km ring + 401 WDPA-locked polygons + 5 OSM protected areas; comparables-context deck page.
- `lqv/subscene/property_v2_soil_profile.py` — SoilGrids 250 m cross-section through polygon centroid; Phase-1 foundation + drainage anchor.
- `lqv/subscene/property_v2_species_pool.py` — Atlantic Forest 25 km pool with 86 candidates; top-10 species by occurrence count; *Trichilia catigua* / lapacho callouts.

## Provenance

- **Sentinel-2 (Batch A, I):** Element84 Earth Search STAC, no auth, B02-B08 bands. Single-date 2026-05-12 scene (v1) + 12-scene timeseries 2020-H1 → 2025-H2.
- **Copernicus DEM (Batch B):** OpenTopography REST `globaldem`, `OPENTOPOGRAPHY_API_KEY` in `.env.local`.
- **OSM Overpass (Batch C):** 2026-06-28 mirror state, polygon bbox + 2 km buffer.
- **Comparables (Batch D):** WDPA v2024-Q2 (gated by token; 401 polys cached) + OSM `boundary=protected_area`.
- **Atlantic Forest pool (Batch E):** GBIF occurrence subset filtered to 25 km radius from polygon centroid, Atlantic Forest classification per Oliveira-Filho 2017 tree DB.
- **Biodiversity (Batch F):** GBIF + iNat 25 km radius; 0 IUCN-threatened (corrected from earlier 1 false-positive after taxonomy verification).
- **MS Open Buildings (Batch G):** v3 (2023 vintage) polygon set, AOI ±1 km clip.
- **SoilGrids (Batch H):** ISRIC SoilGrids v2.0, 250 m, 2020 vintage.
- **Sentinel-1 RTC γ⁰ (Batch J):** Microsoft Planetary Computer RTC product, 14 scenes Apr-Oct 2026.
- **Landsat (Batch K):** L4/5/7/8/9 annual NDVI composites 1985-2025 via Earth Engine partner GCS bucket.
- **Hansen GFC v1.12 (Batch K′):** `earthenginepartners-hansen` GCS bucket, tile `20S_060W`.
- **Mapbiomas Paraguay Coll 2 (Batch K″):** mapbiomas.org Paraguay portal Coll 2, 1985-2023.
- **JRC GSW v1.4 (Batch K‴):** EC JRC Global Surface Water portal, all 4 layers 1984-2021.
- **License:** All batches CC-BY-4.0 or public domain; consolidated citation in [[license_obligations]].

## Carry-forward gaps

- **Per-stem species ID** (R35) — drone LiDAR or sub-1 m NICFI + DeepForest gates the 86-candidate → on-site-stem promotion.
- **Mapbiomas Fire annual product** — Phase-0 §12 future-batch K⁗; pull to confirm/refute the 2003 NDVI dip as drought-vs-fire.
- **NICFI Planet 4.77 m monthly mosaics** — user-side signup gated (in [[deferred_data]]); the sub-1 m sweet spot between Landsat 30 m and drone 5 cm.
- **Mapillary streetside** — along `Camino a Escobar` for boundary-eye-level imagery; token gated on user-side signup.
- **WDPA token rotation** — 401 polys cached; full re-pull needs token rotation. Phase-1 task.
- **GEE auth** — would replace several batches with direct Earth Engine pulls; gated on user-side signup.
- **CMIP6 NEX-GDDP** (Task #39 background) — climate-envelope batch; on completion writes [[cmip6_brief]].
- **MOD11 LST** — yearly Day + Night mean TIFs + summary.json + per-granule/monthly/annual CSVs pulled 2026-06-29; [[mod11_brief]] write-up pending.
- **ALOS PALSAR L-band 2007-2010 + 2015-2020** — Task #30 deferred (MPC SAS HTTP 000 timeout, ~30 min periodic retry).
- **Drone SfM at 5-10 cm GSD** — replaces Cop30 DEM hydrography + OSM road on-property; aligns with the user's LOD directive.
- **Photo intake window 2026-07-27 → 2026-08-27** — promotion of 14-row register at sibling [[property_map_brief]] §photo_verification.

## Cross-references

- [[property_map_brief]] — v1 baseline 300 dpi composite (canonical PNG).
- [[sentinel2_brief]] / [[sentinel1_brief]] / [[landsat_brief]] — Batches A/I, J, K.
- [[hansen_gfc_brief]] / [[mapbiomas_paraguay_brief]] / [[jrc_gsw_brief]] — Batches K′, K″, K‴.
- [[canopy_height_brief]] — Meta CHM 1 m corroboration.
- [[soilgrids_brief]] — Batch H.
- [[hydrogeology_brief]] — Batch B.
- [[infrastructure_brief]] — Batch G.
- [[atlantic_forest_trees_brief]] — Batch E.
- [[biodiversity_25km_brief]] — Batch F.
- [[comparables_brief]] — Batch D.
- [[gbif_brief]] / [[fauna_brief]] / [[flora_brief]] — 5 km biodiversity inside the 25 km envelope.
- [[client_photos_brief]] — 14-row promotion register.
- [[post_escritura_site_knowledge]] §3 — T+1 knowledge-pack narrative.
- [[decisions_log]] 2026-06-28 — polygon scope-lock decision.
- [[research_gaps]] R01 (stream permanence), R35 (individual trees).
- [[deferred_data]] — NICFI / Mapillary / GEE / WDPA-rotation / CMIP6 / MOD11 / ALOS PALSAR pending unlocks.
- [[license_obligations]] — consolidated CC-BY-4.0 citation.
- [[feedback_subscene_clip_end]] — sub-render `cam.data.clip_end` must bypass 100 m default at parcel scale.

Generated 2026-06-29 (T+2 post-escritura).
