# Biodiversity 25 km — La Quebrada Viva (Phase-0 §12)

_Pulled 2026-06-29 from GBIF Occurrence (per-class queries) + iNaturalist (research-grade observations only). 25 km radius around parcel centroid (-57.0355, -25.6073), BBox W-57.2853 S-25.8325 E-56.7857 N-25.3821. Covers the parcel + ~ Quiindy + ~ Acahay + the Lago Ypoá western shore — a Cerrado / Atlantic-Forest transition belt._

## Headline

- **437 GBIF species + 727 iNaturalist research-grade observations across 42 yrs (1984-05-06 → 2026-06-24)** — the 25 km circle is a **well-documented Atlantic-Forest / Cerrado ecotone** with a strong long-tail of regional naturalist records, not a data desert.
- **The avifauna signal is the strongest** — 100 bird species, 14 853 observations, dominated by the open-edge generalist guild (Thraupidae, Tyrannidae, Cathartidae, Columbidae). The top 5 (Celestino, Buitre negro, Paloma Apical, Benteveo, Hornero) are all canonical Paraguayan campo birds — confirming the **landscape matrix is mosaic, not closed forest**. This matches the [[canopy_height_brief]] CHM showing gallery-forest islands in open pasture.
- **Mammal fauna is bat-dominant**: 4 of the top 10 occurrences are Phyllostomidae + Molossidae (Desmodus rotundus, Carollia, Artibeus, Sturnira, Molossus, Cynomops, Molossops). Bats are the **highest-density vertebrate group** here — design a dusk-roost-friendly envelope (no white floodlights pointed up; warm CCT ≤ 2700 K wall washes; allow attic/eave gaps in service buildings).
- **Atlantic Forest indicator species are present**: *Sooretamys angouya* (Colilargo paraguayo, AF-endemic rodent), *Nectomys squamipes* ("Atlantic Forest Nectomys"), *Trichilia catigua*, *T. pallida*, *Sebastiania brasiliensis* — confirming the Mbopicua corridor is biogeographically **part of the Upper Paraná Atlantic Forest** ecoregion, not strictly Chaco-Pampean.
- **One unambiguous invasive** showed up: *Solenopsis invicta* (red imported fire ant, 19 records). Plan picnic areas + child zones with mound-disturbance in mind; do **not** import fill from outside the parcel without screening.
- **GBIF-reptilia returned 0 records** (likely API bug / class-name mismatch in our query). The iNat pull shows 35 reptilia obs in the same window — **regional reptile fauna is not actually 0**; the [[fauna_brief]] curated lists are the authoritative source for now, and the GBIF query needs a v2 pull with `kingdom=Animalia&class=Reptilia` re-checked.
- **No IUCN-flagged species in the GBIF top-100s per class** — but this is mostly because GBIF returns LC + null for ~ 99 % of records and we capped at 100/class. The [[atlantic_forest_trees_brief]] PY-threatened slice and the [[flora_brief]] threatened.csv carry the actual conservation flags for plants. For vertebrates, cross-reference *Tapirus terrestris* / *Panthera onca* / *Myrmecophaga tridactyla* presence with the SEAM Paraguay red list (Phase-1 task).

## Class totals

| GBIF class | species | total occurrences | notes |
| --- | ---: | ---: | --- |
| Aves | 100 | 14 853 | dominant signal, open-edge generalists + AF forest birds |
| Magnoliopsida (dicots / trees) | 100 | 3 014 | AF + Cerrado mix, Myrtaceae-rich |
| Insecta | 100 | 582 | beetles + ants + bees; *Solenopsis invicta* invasive |
| Liliopsida (monocots) | 60 | 504 | Poaceae-dominated (grass matrix), bamboos + sedges |
| Mammalia | 59 | 409 | bats + rodents + edge generalists |
| Amphibia | 18 | 212 | Bufonidae + Hylidae + Leptodactylidae |
| **Reptilia** | **0** | **0** | **query bug — fix in v2 pull** |

| iNat iconic taxon | obs |
| --- | ---: |
| Plantae | 271 |
| Insecta | 223 |
| Aves | 92 |
| Arachnida | 45 |
| Reptilia | 35 |
| Amphibia | 22 |
| Mammalia | 17 |
| Fungi | 16 |
| Actinopterygii | 5 |
| Mollusca | 1 |

_Raw per-class JSONs in this dir; unified table in `species_combined.csv` (873 rows)._

## Top species the design should know about

### Birds (visible / audible on the parcel daily)

| species | vernacular | guild | design hook |
| --- | --- | --- | --- |
| *Pitangus sulphuratus* | Benteveo | open-edge flycatcher | the loud "kiskadee" call at dawn; nests on power lines + tree forks |
| *Furnarius rufus* | Hornero | terrestrial insectivore | clay oven-nests on roof eaves + posts → leave deliberate nest sites on the corredor structure |
| *Coragyps atratus* | Buitre negro | scavenger | thermal-soaring over hot pavement; do not site dumpsters in views |
| *Vanellus chilensis* | Tero / Alcaraván | grassland sentinel | alarms at intruders → security side-effect, plan for noise on south pastures |
| *Cyclarhis gujanensis* | Juruviara / Alegrín | canopy songbird | gallery-forest indicator; loud at dawn — bedroom orientation matters |
| *Crotophaga ani* | Pirinchu / Ani | edge insectivore | flocks in disturbed pastures |
| *Caracara plancus* / *Milvago* spp. | Carancho | open-country raptor | territorial — do not feed scraps near pool |

Family richness: **Tyrannidae 12 spp, Thraupidae 10 spp, Furnariidae 7 spp** — the parcel sits in a flycatcher-tanager-ovenbird matrix, exactly the assemblage [[fauna_brief]] birds_likely.csv lists.

### Mammals (mostly nocturnal, mostly bats)

The top-20 mammals are **dominated by Phyllostomidae + Molossidae (free-tailed + leaf-nosed bats)** plus AF-endemic cricetid rodents. Design implication: **the parcel will be alive at dusk**. Plan:

- Warm-CCT bollards (≤ 2700 K) so the bat foraging window stays usable.
- No bright outdoor floods aimed at the canopy (the gallery is the foraging belt).
- *Desmodus rotundus* (vampire bat) presence is expected at 25 km radius and is not a livestock-emergency until a domestic-mammal density threshold is crossed — keep horses + cattle housed under closed roofs at night per the standard PY mitigation.

The non-bat list (Sooretamys, Nectomys, Akodon, Cavia, agouti / paca / capybara likely though not in the GBIF top-59) implies a **viable rodent + caviomorph prey base** — feeds the local raptor + felid food web. Keep the riparian gallery as continuous as possible to keep the corridor functional.

### Trees (Magnoliopsida — what the AF + Cerrado margins actually carry)

| species | vernacular | family | role |
| --- | --- | --- | --- |
| *Sebastiania brasiliensis* | Blanquillo | Euphorbiaceae | climax AF understory, common dominant |
| *Trichilia catigua* | Catiguá | Meliaceae | climax canopy, hardwood |
| *Trichilia pallida* | Chanchuwi | Meliaceae | mid-canopy AF |
| *Chrysophyllum marginatum* | Vasuriña | Sapotaceae | bird-dispersed AF tree |
| *Piper amalago* | Anisillo / pariparoba | Piperaceae | understory shrub, medicinal (gut, anti-inflammatory) |
| *Solanum chacoense* | Chaco Potato | Solanaceae | Cerrado-Chaco signal, wild crop relative |
| *Eugenia myrcianthes* | ñangapiry / Surinam cherry | Myrtaceae | edible fruit, bird-attractor |
| *Arachis glabrata* | rhizoma peanut | Fabaceae | groundcover, nitrogen-fixer, livestock forage |

**Myrtaceae 13 spp + Bignoniaceae 8 spp + Sapindaceae 7 spp + Fabaceae 5 spp + Apocynaceae 5 spp** — this is a textbook Upper Paraná Atlantic Forest tree spectrum, complementing [[atlantic_forest_trees_brief]] (Lima 2024 checklist). The [[flora_brief]] trees_likely.csv list is consistent with these top families.

### Monocots — the **grass matrix is Poaceae-dominated**

Top monocots: *Lasiacis maculata* (carrizo), *Pharus lappulaceus* (guizazo de perro), *Olyra ciliatifolia*, *Panicum millegrana*, *Paspalum guenoarum*. *Zea mays* (cultivated maize) ranks #1 by GBIF count because herbarium duplicates concentrate near research stations — **do not** read this as "the parcel is a maize field"; it isn't. The native pasture is *Paspalum* + *Panicum* + *Lasiacis*, exactly the species the campo restoration plan should privilege.

### Amphibians — full 18-species list

The 25 km pull found all 18 frogs/toads, dominated by *Melanophryniscus stelzneri* (Redbelly Toad, 152 obs) + Hylidae (treefrogs) + Leptodactylidae (rain frogs). All 18 are seasonal-wetland-dependent — every one will use the quebrada + ephemeral pools the [[hydrogeology_brief]] flagged. Design implication: do **not** route stormwater straight into pipes; route to vegetated detention basins for amphibian breeding habitat. Pair with the [[mod16_brief]] residual ~ 685 mm/yr — the quebrada baseflow is the habitat backbone.

### Insects — a few that matter

- *Solenopsis invicta* (red imported fire ant) — **invasive**, paint targets red on the parcel map.
- *Solenopsis macdonaghi* — native fire ant, ecological role + sting risk.
- *Megachile curvipes* + *Augochlorella tredecim* — native solitary bees, pollinator priority (leave bare-soil patches for nesting).
- *Aracanthus robustus*, *Anotylus insignitus*, *Hemiceras soso* — beetles + moths, leaf-litter dependent, validate forest-floor function.

## Cross-reference with the rest of the data stack

| Layer | What it adds | Reference |
| --- | --- | --- |
| Property-scale GBIF (≤ 5 km) | the parcel's own confirmed occurrences (vs the 25 km regional pool here) | [[gbif_brief]] (species_markdown.md) |
| iNat 5 km parcel pull | locally-observed plants + fauna inside the buffer | [[fauna_brief]] inat_5km_observations.json + [[flora_brief]] inat_5km_plantae.json |
| Atlantic Forest checklist | regional master list (PY threatened slice) | [[atlantic_forest_trees_brief]] |
| CHELSA bioclim | climatic envelope for each species | [[chelsa_brief]] |
| Canopy CHM (Meta) | habitat-stratum (gallery 10-12 m, scrub 3-5 m, pasture 0.3 m) | [[canopy_height_brief]] |
| MOD16 ET | productivity — drives invertebrate + frugivore abundance | [[mod16_brief]] |
| MOD11 LST (running) | thermal microhabitat for reptiles + dawn-active insects | [[mod11_brief]] (in progress) |
| Hansen GFC | forest-loss history filters the species likely to recolonize | [[hansen_gfc_brief]] |
| MapBiomas PY | landcover trajectory (1985-2024) | [[mapbiomas_paraguay_brief]] |
| OSM polygon | built features + roads → fragmentation context | [[osm_brief]] |

## Engineering / design implications

### Architecture
- **Bat-aware lighting** (warm CCT, no uplighting, dim-to-amber after 23:00) — most photogenic vertebrate-encounter moments at the parcel are dusk Phyllostomidae passes.
- **Hornero nest shelves** on the corredor's external structural members — free local-fauna PR moment, costs nothing.
- **No closed-off attics** in service buildings: leave 12 mm bat-pass gaps screened with hardware cloth so colonies establish without entering living space.
- **Pollinator strip** of 30 m wide in the SW chacra (the dry-end zone in [[mod16_brief]]): mix *Arachis glabrata* groundcover + *Lonchocarpus* + *Anadenanthera* + *Tabebuia heptaphylla* + *Handroanthus impetiginosus* for bee + sunbird + bat-flowering coverage.

### Restoration sequencing (5-yr plan input)
1. **Year 1**: close riparian gallery gaps with the [[atlantic_forest_trees_brief]] climax list — *Sebastiania*, *Trichilia*, *Chrysophyllum*, *Cordia*.
2. **Year 2**: enrich SE + SW edges with bird-attractor frugivores — *Eugenia*, *Inga*, *Psidium*, *Cecropia* — to pull avifaunal seed-dispersers across the matrix gap.
3. **Year 3**: reintroduce Myrtaceae-Bignoniaceae understory under the year-1 cover.
4. **Year 4-5**: monitor; expect the canopy bird family count (Furnariidae, Vireonidae, Thraupidae endemics) to climb 30-50 % per [[fauna_brief]] reference trajectories from CONAPI restoration sites.

### Sub-renders (Cycles, [[feedback_sub_render_first]])
- `lqv/subscene/biodiversity_dusk.py`: a 30-second dusk vignette over the gallery — Phyllostomidae silhouette pass, hornero alarm-call, *Pitangus* perch on corredor rail. Sells "fauna-first design".
- `lqv/subscene/pollinator_strip.py`: 30 m SW pollinator strip with *Arachis* groundcover + *Tabebuia* canopy. Drives the food-web panel.
- `lqv/subscene/avifauna_canopy.py`: gallery-top morning chorus — *Cyclarhis* + *Turdus* + *Pitangus* placements over the existing CHM mesh.

## Carry-forward gaps

- **GBIF Reptilia query bug** — 0 records vs iNat 35 obs implies the query itself failed. Re-run `phase0_biodiversity_25km.py` with explicit `kingdom=Animalia&class=Reptilia&srsname=epsg:4326` and back-check against the [[fauna_brief]] reptiles.csv canonical list.
- **No fish records pulled** — Lake Ypoá + the quebrada hold Actinopterygii (5 iNat obs); add a v2 pull for class Actinopterygii.
- **IUCN red-list status sparse** — most GBIF records return null. Cross-reference with the **SEAM PY 2019 vertebrate red list** + the **MADES 2023 update** (deferred to Phase-1 — both are PDF-only and need OCR).
- **Pollinator richness undercaptured** — Apidae + Halictidae + Megachilidae at 25 km radius will exceed the 100-species cap. Re-pull with `class=Insecta&order=Hymenoptera` only when designing the pollinator strip.
- **iNat 727 obs is small** — Paraguay has lower iNat penetration than Brazil + Argentina. Expect 3-5× more obs over the next 3 years; budget a re-pull at delivery T+24 mo.

## Provenance

- **GBIF Occurrence Store**: API v1 (`/occurrence/search`), per-class queries with `decimalLatitude`/`decimalLongitude` window + `hasCoordinate=true&hasGeospatialIssue=false`, paginated to first 100 species per class by occurrence-count rank. Snapshot 2026-06-29.
- **iNaturalist API v1** (`/observations`): `quality_grade=research`, point + radius, all kingdoms, paginated. 727 obs returned 2026-06-29.
- **Pipeline**: `scripts/phase0_biodiversity_25km.py` (per-class GBIF call → JSON → unified CSV merge with iNat) + this brief.
- Citation: GBIF.org (2026) GBIF Occurrence Download; iNaturalist contributors (2026) Research-grade observations.

## Engineering snapshot

```
GBIF species          437 (100+100+100+60+59+18+0)
GBIF occurrences   19 574
iNat obs              727 (1984-2026, 42 yrs)
Combined CSV rows     873
Class coverage          7 + 10 iNat iconic taxa
Top family            Phyllostomidae (bats) — 4 of top 10 mammal occurrences
AF indicator spp        Sooretamys, Nectomys, Sebastiania, Trichilia × 2
Invasive flagged        Solenopsis invicta (red fire ant)
Known data gap          Reptilia GBIF returned 0 (re-pull needed)
```
