---
title: "Flora brief — La Quebrada Viva"
phase: Phase-0
section: "§12 #4 extension"
centroid: "-57.0355, -25.6073"
parcel_radius_km: 5.0
regional_radius_km: 25.0
data_sources: ["expected_species_ranked.csv (3906 rows)", "GBIF Magnoliopsida/Liliopsida (25 km)", "iNaturalist research-grade (25 km + 5 km tight)"]
status: "v1 — synthesis on top of biodiversity_25km/ + new 5 km Plantae pull"
parcel_inat_plantae_obs: 8
---

# Flora brief — La Quebrada Viva

Parcel centroid `-57.0355, -25.6073` (-25.6073°S, -57.0355°W), ~350 m elevation, Atlantic Forest / Cerrado ecotone, Paraguarí. Expected-species ranking is the curated 3,906-row checklist crossed against Atlantic-Forest (BF.2020), Argentine, and Paraguayan threatened-species lists.

## TL;DR

- **Expected-species pool:** 3,906 spp ranked. 234 timber, 68 medicinal, 64 food/edible, 1 endemics already documented within 25 km, 71 palms.
- **Threatened in regional pool:** 127 species (81 PY *en peligro* + the rest *amenazada* / AR Endangered). 0 have been photographed within 5 km.
- **Parcel-tight (5 km iNat Plantae, research-grade):** 8 GPS-actual plant observations. Top-30 regional trees → 1 confirmed in 5 km; top-20 shrubs → 0 confirmed.
- **5 km plant iconic-mix:** Plantae 8.

## Critical flag — *Araucaria angustifolia*
Pino-paraná (*Araucaria angustifolia*) — PY **en peligro**, AR **Endangered**, IUCN Critically Endangered globally. AF status: confirmed. Atlantic-Forest records: 519. **Status on site: not yet seen in 5 km iNat — confirm before any clearing.** Any specimen on the parcel is a deck-grade conservation story and a hard no-cut constraint.

## Top 10 likely trees (by 25 km occurrence)

| Scientific | Vernacular | Family | n (25 km) | 5 km? | PY threat | Uses |
|---|---|---|---:|:---:|---|---|
| *Sebastiania brasiliensis* | Blanquillo | Euphorbiaceae | 113 | · | — | — |
| *Trichilia catigua* | Catiguá | Meliaceae | 61 | · | — | medicinal |
| *Piper amalago* | Anisillo | Piperaceae | 57 | · | — | — |
| *Trichilia pallida* | Chanchuwi | Meliaceae | 55 | · | — | — |
| *Chrysophyllum marginatum* | Vasuriña | Sapotaceae | 51 | · | — | — |
| *Trichilia elegans* | Catigua blanca | Meliaceae | 43 | · | — | — |
| *Psychotria carthagenensis* | Jazmín de la costa | Rubiaceae | 42 | · | — | — |
| *Annona emarginata* | Araticú | Annonaceae | 40 | · | — | — |
| *Copaifera langsdorffii* | Brazilian diesel tree | Fabaceae | 39 | · | — | fuel · medicinal · poison · resins_gums  |
| *Myrcia laruotteana* | — | Myrtaceae | 39 | · | — | — |

## Top 10 likely shrubs (by 25 km occurrence)

| Scientific | Vernacular | Family | n (25 km) | 5 km? | Uses |
|---|---|---|---:|:---:|---|
| *Capsicum baccatum* | ají | Solanaceae | 35 | · | — |
| *Acalypha communis* | akalyfa bežná | Euphorbiaceae | 25 | · | — |
| *Aloysia gratissima* | Cedrón de monte | Verbenaceae | 19 | · | — |
| *Eugenia punicifolia* | Murta | Myrtaceae | 18 | · | — |
| *Baccharis linearifolia* | — | Asteraceae | 18 | · | — |
| *Pombalia bigibbosa* | — | Violaceae | 18 | · | — |
| *Praecereus euchlorus* | — | Cactaceae | 5 | · | — |
| *Solanum viarum* | tropical soda-apple | Solanaceae | 5 | · | — |
| *Buddleja stachyoides* | Argentine butterfly bush | Scrophulariaceae | 2 | · | ornamental |
| *Cereus stenogonus* | — | Cactaceae | 2 | · | — |

## Threatened species (top 15 by 25 km occurrence)

Full list (87 entries) in `threatened.csv`. **PY *en peligro*: 81** + PY *amenazada*: 40 + AR Endangered/CR: ~13 (overlap). These drive the no-cut overlay on the master plan.

| Scientific | Vernacular | PY | AR | n (25 km) | 5 km? |
|---|---|---|---|---:|:---:|
| *Maytenus ilicifolia* | — | en_peligro | — | 3 | · |
| *Balfourodendron riedelianum* | marfim | en_peligro | — | 1 | · |
| *Cordia trichotoma* | — | en_peligro | Indeterminada (may | 1 | · |
| *Parodia nigrispina* | — | en_peligro | — | 1 | · |
| *Ateleia glazioveana* | — | en_peligro | — |  | · |
| *Araucaria angustifolia* | — | en_peligro | Endangered |  | · |
| *Amburana cearensis* | — | en_peligro | — |  | · |
| *Cedrela angustifolia* | — | en_peligro | Indeterminada |  | · |
| *Cedrela fissilis* | — | en_peligro | — |  | · |
| *Euterpe edulis* | — | en_peligro | Endangered |  | · |
| *Myroxylon peruiferum* | — | en_peligro | Vulnerable |  | · |
| *Simira sampaioana* | — | en_peligro | — |  | · |
| *Zeyheria tuberculosa* | — | en_peligro | — |  | · |
| *Aspidosperma polyneuron* | — | en_peligro | Endangered |  | · |
| *Calophyllum brasiliense* | — | en_peligro | — |  | · |

## Timber + ethnobotanical cross-cuts

- **Timber species (regional pool):** 234. Top by 25 km occurrence in `timber.csv`. Most overlap with the *en peligro* list — selective harvest only via SNC management plan, never on natural-forest polygons.
- **Medicinal:** 68 species with documented medicinal use (folk-pharmacopoeia, *farmacopea criolla* and Mbyá-Guaraní use). Source list in `medicinal.csv`.
- **Food / edible:** 64 species. See `food.csv`. Top families: Myrtaceae (guavas / *arazá* / *pitanga*), Annonaceae (*araticú*), Sapotaceae (*aguaí*).

## Palms (Arecaceae)

- *Syagrus romanzoffiana* — Queen palm; 25 km n=2; 5 km ·; uses: fodder | food | ornamental
- *Euterpe edulis* — —; 25 km n=; 5 km ·; uses: food
- *Attalea funifera* — —; 25 km n=; 5 km ·; uses: fibres
- *Butia catarinensis* — —; 25 km n=; 5 km ·; uses: fibres | food
- *Butia eriospatha* — —; 25 km n=; 5 km ·; uses: food
- *Geonoma gamiova* — —; 25 km n=; 5 km ·; uses: fibres
- *Syagrus botryophora* — —; 25 km n=; 5 km ·; uses: ornamental
- *Allagoptera caudescens* — —; 25 km n=; 5 km ·; uses: —

## Endemics documented in 25 km

1 species classified pure or near endemic to the Atlantic Forest **and** already documented within 25 km of the parcel (GBIF or iNat). Top 10:

| Scientific | Vernacular | Family | Endemism | n (25 km) | 5 km? |
|---|---|---|---|---:|:---:|
| *Psychotria leiocarpa* | — | Rubiaceae | near_endemic | 1 | · |

## GBIF cross-reference (top 25 km records)

**Dicots (Magnoliopsida):**
- *Sebastiania brasiliensis Spreng.* — Euphorbiaceae — n=113
- *Arachis glabrata Benth.* — Fabaceae — n=66
- *Forsteronia pubescens A.DC.* — Apocynaceae — n=64
- *Trichilia catigua A.Juss.* — Meliaceae — n=61
- *Solanum chacoense Bitter* — Solanaceae — n=57
- *Piper amalago L.* — Piperaceae — n=57
- *Trichilia pallida Sw.* — Meliaceae — n=53
- *Chrysophyllum marginatum (Hook. & Arn.) Radlk.* — Sapotaceae — n=50
- *Alicia anisopetala (A.Juss.) W.R.Anderson* — Malpighiaceae — n=46
- *Heteropterys argyrophaea A.Juss.* — Malpighiaceae — n=45

**Monocots (Liliopsida):**
- *Zea mays L.* — Poaceae — n=20
- *Lasiacis maculata (Aubl.) Urb.* — Poaceae — n=19
- *Pharus lappulaceus Aubl.* — Poaceae — n=19
- *Olyra ciliatifolia Raddi* — Poaceae — n=19
- *Panicum millegrana Poir.* — Poaceae — n=18
- *Cyperus incomtus Kunth* — Cyperaceae — n=17
- *Dioscorea multiflora Mart. ex Griseb.* — Dioscoreaceae — n=15
- *Bulbostylis sphaerocephala (Boeckeler) Lindm.* — Cyperaceae — n=14
- *Maranta sobolifera L.Andersson* — Marantaceae — n=13
- *Paspalum guenoarum Arechav.* — Poaceae — n=13

## Top families in the regional pool

- Fabaceae: 707 spp
- Myrtaceae: 707 spp
- Rubiaceae: 338 spp
- Lauraceae: 226 spp
- Melastomataceae: 169 spp
- Annonaceae: 121 spp
- Sapotaceae: 94 spp
- Solanaceae: 89 spp
- Moraceae: 81 spp
- Euphorbiaceae: 79 spp
- Arecaceae: 71 spp
- Bignoniaceae: 62 spp
- Asteraceae: 59 spp
- Malvaceae: 56 spp
- Rutaceae: 55 spp

## Most-observed species in 5 km iNat

- *Pityrogramma calomelanos* — 1 obs
- *Ruellia angustiflora* — 1 obs
- *Luehea divaricata* — 1 obs
- *Allophylus edulis* — 1 obs
- *Lithraea molleoides* — 1 obs
- *Trichocentrum pumilum* — 1 obs
- *Zygostates alleniana* — 1 obs
- *Thaumatophyllum bipinnatifidum* — 1 obs

## Caveats

- iNat coverage is biased toward areas with iNaturalist users; absence in 5 km ≠ absence on parcel.
- The expected-species list was built from Atlantic-Forest BF.2020 checklists + PY/AR threat lists; a species marked *new to AF* is in the regional pool but not yet on the AF checklist (likely Cerrado / Chaco edge species).
- *En peligro* status is national PY. IUCN global category often more lenient (e.g. *Cordia trichotoma* maybe LC globally, en peligro in PY).
- Family + vernacular may have UTF-8 / Spanish-accent issues in raw CSV.

## v2 backlog

- SNC (Secretaría Nacional de Cultura) tree-cutting permit lookup.
- iNat field guide for the parcel area (geo-bounded checklist export).
- TRY Plant Trait Database lookup for top-30 trees (LMA, wood density, shade tolerance) to inform the species mix for restoration plantings.
- Phenology synthesis (flowering / fruiting calendar) from iNat photos.
- Cross-check with the new T-DT canopy raster (NDVI / EVI 2024-2026).
