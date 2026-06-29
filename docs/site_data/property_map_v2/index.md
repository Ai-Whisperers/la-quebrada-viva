# Property map v2 — La Quebrada Viva (T+2, 2026-06-29)

> Phase-0 §12 #20 synthesis. Cross-references every site-data batch (A–K) landed since the
> 2026-06-28 v1 baseline at `docs/site_data/property_map/`. Adds 41-year Landsat history,
> 6-month Sentinel-1 SAR, multi-decade Mapbiomas + Hansen forest tracking, triple-confirmed
> surface-water absence, full SoilGrids profile, 86 LQV-area Atlantic Forest tree species,
> 25 km biodiversity envelope, MS Open Buildings reach, and a 50 km comparables ring.
>
> v1 stays canonical for the polygon-clip composite PNG; v2 is the indexed data spine the
> deck and the digital twin pull from.

## TL;DR — v1 → v2 delta

| Question | v1 (2026-06-28) | v2 (2026-06-29) |
|---|---|---|
| Canopy density | S2 NDVI single date 2026-05-12, 4 bins @ 10 m | + S2 timeseries 2020-H1→2025-H2 (12 scenes, NDVI mean **+0.773**); + Landsat **41-year** NDVI 1985-2025 (mean **+0.696**, peak +0.782 in 2024, drought floor +0.564 in 2003) |
| Forest cover | implied dense from NDVI | Hansen GFC v1.12 **82.1 %** treecover2000; Mapbiomas Paraguay native forest **80.6 % (1985) → 84.0 % (2023)**, Δ +3.4 pp |
| Forest loss (1985-2024) | unknown | **~0.63 ha** (7×30 m pixels) on Hansen, concentrated 2001/2003/2007/2014 — none after 2015 |
| Surface water inside polygon | NDWI single-date = 0 % | **Triple-confirmed 0 %** across (i) S2 AWEIsh −0.677 / NDWI −0.706 / MNDWI −0.581, (ii) S1 SAR VV −8.33 dB > −15 dB threshold, (iii) JRC GSW v1.4 1984-2021 — **zero polygon cells with any historical water occurrence** across all 4 layers (occurrence, seasonality, recurrence, transitions) |
| Streams | Cop30 D8 flow-accum, 15 LineStrings | unchanged at v2 — JRC GSW confirms none are permanent water bodies; S1 ratio + Cop30 morphology jointly classify as seasonal/ephemeral |
| Buildings | OSM Overpass: 9 polygons south of polygon, 0 on-property | + MS Open Buildings quadkey z=9 `210301312`: **737 polygons** in AOI ±1 km, Σ 59 947 m². Nearest building **196 m** from polygon centroid (17 m² shed-scale). Still 0 on-property structures |
| Roads | OSM: `Camino a Escobar` | unchanged |
| Soil profile | unknown | SoilGrids 250 m, 25 pts in AOI: **pH ~5.3 acidic at all depths**; clay 207 → 321 g/kg with depth (argillic B-horizon); sand 567 → 480 g/kg; SOC **429 → 75** (highly organic A-horizon); CEC 194 → 175 cmol/kg; coarse fragments 50 → 86 (residual soil over saprolite) |
| Tree species (candidate list) | flora research only | **86 species** within 25 km cross-ref'd to Atlantic Forest THREAT master (5 789 spp). Top hits: *Trichilia catigua* (61 occ), *Copaifera langsdorffii* (39), *Parapiptadenia rigida* "Anchico" (34), *Luehea divaricata* (31), *Nectandra megapotamica* (28), *Eugenia uniflora* (28), *Protium heptaphyllum* (28), *Cordia americana* "guayaibí" (27), *Peltophorum dubium* "caña fístola" (26), *Myrcianthes pungens* "guaviyú" (20), *Anadenanthera colubrina* "Red Angico" (2), *Handroanthus impetiginosus* "pink ipê / **lapacho**" (1) |
| Threatened flora (PRY) | unknown | 3 en_peligro spp in the 86-species LQV pool: *Balfourodendron riedelianum* "marfim", *Cordia trichotoma*, *Maytenus ilicifolia* + 1 amenazada *Baccharis trimera*, 1 near_endemic *Psychotria leiocarpa* |
| Fauna context (25 km) | open question | GBIF: **437 species** (Aves 100, Magnoliopsida 100, Insecta 100, Liliopsida 60, Mammalia **59**, Amphibia 18); iNaturalist: **727 research-grade obs**; IUCN-threatened in this pull: **0** |
| Protected areas (50 km) | unknown | WDPA REST 401-locked (token gap); OSM Overpass returns **5 records**: Distrito de Escobar 4.0 km, Bosques Embrujados reserve 3.7 km, Monumento Natural Cerro Koi 48.1 km, Cerro Chororî 49.3 km |
| Radar history | none | S1 RTC γ⁰ Dec 2025 → Jun 2026, 14 scenes desc relorbit 68 IW VV+VH: polygon VV mean **−8.33 dB**, VH **−14.09 dB**, VV−VH **+5.76 dB** (closed canopy signature; no flooded patches) |
| Burn history | unknown | Landsat NBR per-year (1985-2025): mean +0.490, min +0.331 in 2003 (drought), peak +0.574 in 2018 — no year-over-year dNBR drop > 0.20 inside polygon ⇒ no detectable burn scar at 30 m for the full Landsat era |

## Per-batch cross-reference index

| Code | Batch | Path | Resolution | Window | Anchor finding |
|---|---|---|---|---|---|
| A | v1 property map composite | `docs/site_data/property_map/index.md` | 10 m / 30 m | 2026-05-12 single date | 4-class NDVI surface + Cop30 hydrography + 9 OSM neighbour buildings |
| B | Cop30 DEM hydrography | `docs/site_data/property_map/vector/hydrography_dem.geojson` | 30 m | static | 15 LineStrings entering N/NE, exiting SW low corner |
| C | OSM Overpass | `docs/site_data/property_map/vector/{buildings,roads,natural}_osm.geojson` | vector | live | sparse — 9 buildings (all S of polygon), 1 road, 2 farmland |
| D | Comparables / protected | `docs/site_data/comparables/summary.md` | vector | 50 km buffer | 5 hits — WDPA 401-locked; Bosques Embrujados 3.7 km is nearest |
| E | Atlantic Forest tree DB | `docs/site_data/atlantic_forest_trees/summary.md` | regional | 5 789-spp master | **86 LQV-area candidates**, 3 PY en_peligro |
| F | Biodiversity 25 km | `docs/site_data/biodiversity_25km/summary.md` | 25 km radius | live API | GBIF 437 spp · iNat 727 obs · IUCN-threatened 0 |
| G | MS Open Buildings | `docs/site_data/infrastructure/buildings/summary.md` | 1 m vector | 2024 ML pass | 737 polygons / 59 947 m² in AOI ±1 km; nearest 196 m |
| H | SoilGrids profile | `docs/site_data/soilgrids/cube/summary.md` | 250 m, 25 pts | static | pH 5.3 acidic; clay-increasing argillic profile; SOC 429→75 |
| I | Sentinel-2 timeseries | `docs/site_data/sentinel2/timeseries_2020_2025/summary.md` | 10 m | 12 scenes 2020-03 → 2025-10 | NDVI **+0.773**, NDWI −0.706, MNDWI −0.581, AWEIsh −0.677 |
| J | Sentinel-1 RTC SAR | `docs/site_data/sentinel1/rtc_6mo_median/summary.md` | 10 m | 14 scenes 2025-12 → 2026-06 | VV −8.33 dB, VH −14.09 dB, ratio +5.76 dB (no flood patches) |
| K | Landsat annual median | `docs/site_data/landsat/annual_median_1985_2025/summary.md` | 30 m | 41/41 years | NDVI +0.696 (drought +0.564 in 2003, peak +0.782 in 2024) |
| K′ | Hansen GFC v1.12 | `docs/site_data/hansen_gfc/summary.md` | 30 m | 2000-2024 | 82.1 % treecover2000; ~0.63 ha loss 2001-2024; 0 gain |
| K″ | Mapbiomas Paraguay Coll 2 | `docs/site_data/mapbiomas_paraguay/summary.md` | 30 m | 1985-2023 (39 rasters) | Native forest 80.6 % → 84.0 % (Δ +3.4 pp); 297 px stable forest |
| K‴ | JRC GSW v1.4 | `docs/site_data/jrc_gsw/summary.md` | 30 m | 1984-2021 | **0 polygon cells** with any water occurrence — confirms I+J |

## Layer provenance

| Layer | Sensor / dataset | Native res. | Re-projected to | Auth needed | Re-fetch script |
|---|---|---|---:|---|---|
| Canopy classes | Sentinel-2 L2A (Element84) | 10 m | EPSG:32721 | none | `scripts/fetch_sentinel2.py` |
| S2 timeseries indices | Sentinel-2 L2A | 10 m | EPSG:32721 | none | `scripts/phase0_sentinel2_timeseries_batch.py` |
| S1 RTC γ⁰ VV/VH | Sentinel-1 GRD via MPC | 10 m | EPSG:32721 | MPC SAS (50-min) | `scripts/phase0_sentinel1_sar_batch.py` |
| Landsat annual indices | Landsat C2-L2 via MPC | 30 m | EPSG:32721 | MPC SAS | `scripts/phase0_landsat_annual_batch.py` |
| ALOS PALSAR-2 γ⁰ | ALOS-2 25 m via MPC | 25 m | EPSG:32721 | MPC SAS — **outage** | `scripts/phase0_alos_palsar_batch.py` |
| Hansen GFC | UMD Hansen v1.12 | 30 m | EPSG:32721 | GCS public | `scripts/phase0_hansen_gfc_batch.py` |
| Mapbiomas PY | Coll 2 via Google Cloud | 30 m | EPSG:32721 | public | `scripts/phase0_mapbiomas_paraguay_batch.py` |
| JRC GSW | JRC EU v1.4 | 30 m | EPSG:32721 | public | `scripts/phase0_jrc_gsw_batch.py` |
| Hydrography (D8) | Copernicus 30 m DEM | 30 m | EPSG:4326 | OpenTopography API (in `.env.local`) | `scripts/analyze_stream.py` |
| Buildings (ML) | Microsoft Global Buildings | vector | EPSG:4326 | none | `scripts/phase0_buildings_batch.py` |
| Buildings (community) | OSM Overpass | vector | EPSG:4326 | none | `scripts/build_property_map.py` |
| SoilGrids cube | ISRIC v2.0 REST | 250 m | sampled at 25 pts | none | `scripts/phase0_soilgrids_batch.py` |
| Atlantic Forest tree DB | Lima et al. THREAT 2024 | tabular | n/a | none | `scripts/phase0_atlantic_tree_db_batch.py` |
| Biodiversity (occurrence) | GBIF + iNaturalist + eBird | vector | EPSG:4326 | optional (rate-limit) | `scripts/phase0_biodiversity_25km_batch.py` |
| WDPA + comparables | Protected Planet REST + OSM | vector | EPSG:4326 | **WDPA token gap** | `scripts/phase0_comparables_batch.py` |

## Honesty caveats — inherited from v1, extended

1. **Individual tree positions are still not shipped.** The 86-species Atlantic Forest DB pool is a *candidate list* — it tells us what's regionally plausible (with occurrence counts within 25 km), not what's actually standing on the 30.9 ha. Needs sub-1 m imagery (NICFI 4.77 m unlocks NICFI-DeepForest crown detection) or a crewed field walk to convert candidates → stems. R35 (drone LiDAR) remains on hold pending photos.
2. **No GEE pull yet (Phase-0 §12 #1).** Service-account auth uninstalled. All raster batches use MPC + Element84 + GCS substitutes. Mapbiomas + Hansen ship via GCS public buckets, not the GEE asset path.
3. **NICFI 4.77 m Planet basemap unrequested (Phase-0 §12 #2).** Signup is user-side. NICFI mosaics would let us run DeepForest crown detection and convert the candidate list into per-stem polygons; until then, canopy is a surface, not a count.
4. **Single-pass Sentinel-1 only.** 6-month window 2025-12 → 2026-06 is wet-season-heavy. Dry-season radar (Jul-Oct 2026) will show whether VH-band drops in the SW stream corridor — a flood-pulse signature that confirms the seasonal-only classification.
5. **Soil pH 5.3 is a 250 m grid average across 25 sample points.** Spot variation under the SW stream corridor (likely more acidic, organic-fed) and the open ridge (likely less acidic, more mineral) is not captured. A 5-pit auger sweep at T+30 would resolve.
6. **Water-table depth is unknown.** SoilGrids depth-to-bedrock is regional-scale; the actual static water table at any drill site inside the polygon is not derivable from satellite. SAG (Guaraní Aquifer System) regional context says shallow water-bearing horizons exist but doesn't fix a depth. Bore a test well to know.
7. **Mapbiomas Coll 2 is 30 m and uint8.** Native-forest class boundary can mis-classify pixels on the canopy edge of the SW corridor. The +3.4 pp gain (1985→2023) is a real signal but the per-pixel transitions matrix (e.g. Grassland→Flooded Forest, 16 px) is noisier than the per-class totals.
8. **WDPA REST is 401-locked.** All 5 comparables come from OSM Overpass gap-fill. The "Bosques Embrujados" 3.7 km hit is a haunted-forest-themed nighttime adventure park, NOT a conservation reserve — the OSM name is the operational name, designation/IUCN are blank. A WDPA shapefile download would re-classify.
9. **MS Open Buildings is ML, not surveyed.** The 737 polygons / 59 947 m² in the AOI ±1 km ring are model outputs trained on Maxar imagery; some sheds and roofs may be hallucinated. Ground-truth via OSM (already done — 9 polygons) is the cross-check; the **delta** (737 ML − 9 OSM) is mostly real-but-untagged structures S/SE of the polygon, not on-property.
10. **Atlantic Forest THREAT DB is taxonomic, not on-the-ground.** 86 species *can* occur within 25 km — occurrence counts (e.g. *Trichilia catigua* 61) reflect documented herbarium/iNat records within the 25 km ring, not within the 30.9 ha. Many of these 86 are forest-interior species; what's actually on the polygon depends on which ecotone bands the canopy mosaic covers.

## What this v2 spine can / cannot answer

**Can answer (now):**

- *"Has the polygon been deforested in the satellite era?"* → No. Hansen 2001-2024 shows ~0.63 ha cumulative loss across 24 years (last event in 2014). Mapbiomas 1985-2023 shows native forest actually **gained** 3.4 pp.
- *"Has there been a fire in the polygon?"* → No detectable burn scar at 30 m for 1985-2025. Landsat NBR multi-decade floor is the 2003 drought (+0.331), not a burn signature.
- *"Is there any standing water inside the polygon, ever?"* → No, triple-confirmed (S2 indices, S1 SAR backscatter, JRC GSW 1984-2021).
- *"What's the multi-decade canopy trend?"* → Slight greening; 1985 NDVI mean +0.681, 2025 NDVI mean +0.771. Brief drought trough in 2003 (NDVI +0.564, NBR +0.331, NDMI +0.057).
- *"What tree species are regionally plausible on the polygon?"* → 86 candidates from the Atlantic Forest DB within 25 km, top genera in *Trichilia*, *Copaifera*, *Parapiptadenia*, *Luehea*, *Nectandra*, *Eugenia*, *Protium*, *Cordia*, *Peltophorum*, *Myrcianthes* — including lapacho (*Handroanthus impetiginosus*) already encoded in the render.
- *"What soil are we sitting on?"* → Acidic (pH 5.3), sandy-loam topsoil → clay-rich argillic B-horizon, residual soil over saprolite, high organic A-horizon. Standard humid-subtropical lateritic profile.
- *"How far is the nearest non-OSM-mapped structure?"* → ~196 m S from polygon centroid, ML-detected, 17 m² — likely a shed.
- *"What other protected areas / comparables sit inside a day-trip?"* → 4 (Distrito de Escobar 4 km, Bosques Embrujados 3.7 km, Monumento Natural Cerro Koi 48 km, Cerro Chororî 49 km).

**Cannot answer yet (needs incoming data or Tier-1 unlocks):**

- Individual stem positions, species ID per stem, age structure, DBH distribution → NICFI + DeepForest (Phase-0 §12 #15) or drone LiDAR (R35).
- Are the DEM-traced streams permanent vs. seasonal vs. ephemeral? → walk + EXIF-GPS photos in dry season + S1 radar dry-season pull (Phase-0 §12 #7 extension).
- On-property built features: cabins, sheds, gates, fences, paths, salto pool — invisible to MS Open Buildings and OSM. Photos only.
- Subsurface: water-table depth, depth-to-bedrock spot-confirmed, aquifer transmissivity → drill a test well, MOPC Recursos Hídricos consult.
- Cultural features: graves, shrines, boundary markers, historic land-use phases → ground-walk + neighbour interviews.
- ALOS PALSAR-2 L-band biomass / canopy structure (Phase-0 §12 #9) — **Batch L blocked by MPC SAS outage**. Re-attempt after server recovery.
- Mapillary streetside imagery along Camino a Escobar (§12 #19) — not yet pulled.
- Per-stem fauna sightings — eBird per-hotspot list and iNaturalist EXIF-mapped obs at <500 m exist in F but were aggregated to 25 km here; a polygon-clip pull would extract them.

## Pending-photo gap matrix (extends v1)

| Question | Layer that would answer it | Photo needed | Shot-list ref |
|---|---|---|---|
| Are the SW streams permanent? | dry-season S1 SAR + EXIF-GPS field photo | wet vs dry season comparison at salto / footbridge axis | `client_photos/2026-06_post_escritura/index.md` rows 3, 7 |
| Where is the salto / natural pool? | photo + EXIF GPS | overhead + tier shots | rows 5, 6 |
| Are there on-property cabins/sheds? | photo | walk-by every structure | rows 8–12 |
| Internal access tracks? | photo + GPX | full traverse | row 13 |
| Soil pH spot-confirm? | physical sample → handheld pH meter | top-3 land-use bands | new request: T+30 sweep |
| Lapacho stand count? | NICFI + DeepForest | n/a — software, not photos | Phase-0 §12 #15 |

## Index of v3+ unknowables

These are the things v2 explicitly leaves on the table for future-Tier data lifts:

1. **Per-stem position + species ID** → NICFI 4.77 m + DeepForest (Tier-1 free) → ALS LiDAR (Tier-3 paid, ~$4-9 k).
2. **Sub-canopy soil moisture + flooded-forest extent** → ALOS PALSAR-2 L-band when MPC SAS recovers (Tier-0 free).
3. **Per-segment stream permanence** → S1 dry-season pull + field photos (Tier-0 free).
4. **Water-table depth + aquifer character** → test-well bore + MOPC consult (Tier-2 paid, ~$800-2 500).
5. **In-polygon fauna sightings (not 25 km envelope)** → camera-trap deployment for 60 d (Tier-3, ~$300-600/trap).
6. **Cultural/historic land-use** → neighbour + cadastral office interviews (Tier-0 time only).
7. **Per-pixel land-use 2025+** → Mapbiomas Coll 3 once released; until then, S2 timeseries serves.
8. **Climate cube spot-check vs WorldClim** → WorldClim 2.1 host (geodata.ucdavis.edu) currently down; CHIRPS + ERA5-Land + NASA POWER on disk are now synthesized in `docs/site_data/climate_cube.md` as the v1 cube. WorldClim spot-check + MOD16A2 ET pending v2.

## Related

- Climate cube synthesis: `docs/site_data/climate_cube.md` (Phase-0 §12 #17 v1, three-source cross-validated)
- v1 baseline: `docs/site_data/property_map/index.md` (canonical composite PNG @ 300 dpi)
- v2 master spec: `docs/research/property_map_v2_data_sources.md` (§4-§16 source manifest)
- v2 tooling plan: `docs/research/property_map_v2_tooling.md` (5-phase upgrade plan, Tier 0 = $0)
- DECISIONS log: `docs/DECISIONS.md` 2026-06-28 (polygon scope-lock)
- Pending-photo intake: `docs/site_data/client_photos/2026-06_post_escritura/index.md` (14-row shot list)
- Research gaps: `docs/RESEARCH_GAPS.md` R01, R35
- Knowledge pack: `docs/post_escritura_site_knowledge.md` (T+1 narrative)

Generated 2026-06-29 (T+2 post-escritura).
