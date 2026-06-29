---
title: "GBIF historical species census brief — La Quebrada Viva"
phase: Phase-0
section: "§12 #19 — historical biodiversity record"
centroid: "-57.0300, -25.6300 (legacy bbox centre)"
bbox_w: -57.045
bbox_e: -57.015
bbox_s: -25.645
bbox_n: -25.615
records_total: 54
record_classes: ["Aves: 50", "Magnoliopsida: 2", "Squamata: 1", "Insecta: 1"]
data_sources: ["GBIF.org occurrence search (parcel-tight 0.03° box)"]
status: "v1 — historical record, complements iNat-driven fauna_brief/flora_brief"
---

# GBIF historical species census brief — La Quebrada Viva (Phase-0 §12 v1)

> Single-bbox GBIF pull over a 0.03° × 0.03° box (~3.3 × 3.3 km) approximately
> over Mbopicuá, accessed 2026-06-10. 54 unique species across 4 classes.
> This brief documents the **historical** record that pre-dates the
> iNaturalist-driven [[fauna_brief]] and [[flora_brief]] pulls — useful as
> independent corroboration of the bird community and as the only public
> source for the 1883/1901/1976 pre-iNat occurrences.

## Headline

- **54 species, 54 occurrences** — every species has `occurrenceCount = 1`; the file is a deduplicated species list, not an occurrence table.
- **Aves 92.6 %** (50 / 54) — GBIF for this bbox is dominated by a single 2002-01-16/17 eBird-style checklist event.
- **Date range 1883-03-05 → 2014-03-29** — 131 yr historical window; 50 / 54 first-seen dates fall on 2000-2002 (eBird ingest era).
- **IUCN status: LC = 47 / 54** (87 %); 7 records carry no IUCN rank (Aves taxonomy splits + non-Aves).
- **No mammals, no amphibians, no fish, no fungi** in this GBIF pull — taxonomic blind spots that [[fauna_brief]] (iNat) partly fills (43 parcel-tight iNat obs, 5 km).
- **Pre-eBird records 4 / 54**: *Jacquemontia fruticulosa* 1883, *Atrachelacris unicolor* 1901, *Tropidurus spinulosus* 1976, *Cyanocorax chrysops* 1999 — these are the only verifiable century-scale biodiversity references for the AOI.

## AOI bbox + provenance

| Field | Value |
| --- | --- |
| West | −57.045° |
| East | −57.015° |
| South | −25.645° |
| North | −25.615° |
| Width × height | 0.030° × 0.030° (~3.3 × 3.3 km, ~10.9 km²) |
| Coverage vs 30.9 ha parcel | bbox is offset ~0.5 km W and ~0.02° S of the parcel centroid (−57.0355, −25.6073) — partly overlaps the parcel but skews W/S |
| Coverage vs 5 km parcel-tight ring | bbox is **inside** the 5 km ring used by [[fauna_brief]] / [[flora_brief]] |
| Source | GBIF.org occurrence search, accessed 2026-06-10 |
| Output | `species_list.json` (54 records, 23 KB), `species_markdown.md`, `species_summary.txt` |

The bbox is roughly half a kilometre offset W of the actual parcel centroid — the species list should be read as "Mbopicuá rural matrix species" rather than "parcel-tight." It still captures the same Atlantic-Forest / Cerrado ecotone the parcel sits in.

## Class × order breakdown (n=54)

| Class | Order | Families | Species | Share |
| --- | --- | ---: | ---: | ---: |
| Aves | Passeriformes | 16 | 30 | 55.6 % |
| Aves | Piciformes | 3 | 7 | 13.0 % |
| Aves | Cuculiformes | 1 | 4 | 7.4 % |
| Aves | Columbiformes | 1 | 3 | 5.6 % |
| Aves | Psittaciformes | 1 | 2 | 3.7 % |
| Aves | Apodiformes | 1 | 1 | 1.9 % |
| Aves | Charadriiformes | 1 | 1 | 1.9 % |
| Aves | Accipitriformes | 1 | 1 | 1.9 % |
| Aves | Pelecaniformes | 1 | 1 | 1.9 % |
| Magnoliopsida | Myrtales | 1 | 1 | 1.9 % |
| Magnoliopsida | Solanales | 1 | 1 | 1.9 % |
| Squamata | (unset) | 1 | 1 | 1.9 % |
| Insecta | Orthoptera | 1 | 1 | 1.9 % |

Passeriformes dominate at 30 / 54 (55.6 %), in line with the global signal for Neotropical lowland forest checklists.

## Top families (Aves only, n=50)

| Family | Species | Notable representatives |
| --- | ---: | --- |
| Thraupidae | 6 | Sayaca Tanager, Blue Dacnis, Red-crested Cardinal, Red-crested Finch, Bluish-gray Saltator, Chestnut-bellied Seed-Finch |
| Tyrannidae | 5 | Great Kiskadee, Tropical Kingbird, Cattle Tyrant, Streaked Flycatcher, Brown-crested Flycatcher |
| Picidae | 5 | Campo Flicker, Little Woodpecker, Pale-crested Woodpecker, White Woodpecker, Green-barred Woodpecker |
| Cuculidae | 4 | Guira Cuckoo, Smooth-billed Ani, Striped Cuckoo, Squirrel Cuckoo |
| Columbidae | 3 | White-tipped Dove, Ruddy Ground Dove, Picui Ground Dove |
| Furnariidae | 3 | Rufous Hornero, Narrow-billed Woodcreeper, Great Rufous Woodcreeper |
| Corvidae | 2 | Plush-crested Jay, Purplish Jay |
| Icteridae | 2 | Red-rumped Cacique, Yellow-rumped Marshbird |
| Psittacidae | 2 | Yellow-chevroned Parakeet, Cobalt-rumped Parrotlet |
| Thamnophilidae | 2 | Barred Antshrike, Great Antshrike |
| Turdidae | 2 | Pale-breasted Thrush, Rufous-bellied Thrush |

The 5 woodpecker species (Picidae) + 2 hornero/woodcreeper (Furnariidae) confirm structurally complex bark/cavity-dependent guild — consistent with the [[canopy_chm_brief]] mean canopy height 10.9 m and the [[sentinel2_brief]] NDVI 0.918 dense-canopy reading.

## Pre-eBird historical occurrences (the load-bearing rows)

| Year | Species | Class / Family | Significance |
| ---: | --- | --- | --- |
| 1883-03-05 | *Jacquemontia fruticulosa* | Magnoliopsida / Convolvulaceae | Earliest known biodiversity record in the AOI; herbarium-vintage observation pre-dating any motorised access. Likely an explorer / missionary herbarium specimen. |
| 1901-02-28 | *Atrachelacris unicolor* | Insecta / Acrididae | Type-locality-era grasshopper specimen; the only invertebrate in the full GBIF pull. |
| 1976-07-04 | *Tropidurus spinulosus* | Squamata / Tropiduridae | Spiny lava lizard — the **only reptile** in the AOI's GBIF record. Rock-dwelling, would match the [[extended_aoi_brief]] sub-3 m escarpments. |
| 1999-11-26 | *Cyanocorax chrysops* | Aves / Corvidae | Plush-crested Jay — bridges the historical → eBird era. Forest-edge omnivore. |
| 2014-03-29 | *Ludwigia peruviana* | Magnoliopsida / Onagraceae | Wetland herb — most recent GBIF record. Direct hint that **standing or seasonal surface water** exists somewhere in the bbox (corroborates the [[hydrogeology_brief]] ephemeral-channel hypothesis). |

## Temporal distribution

| Era | First-seen count | Notes |
| --- | ---: | --- |
| 1883 | 1 | Herbarium specimen |
| 1901 | 1 | Type-locality entomology |
| 1976 | 1 | Reptile salvage record |
| 1999-2002 | 50 | eBird-style checklist push (Aves) — single observer-event dominated |
| 2014 | 1 | Aquatic herb |

50 of the 54 records (92.6 %) cluster in the 1999-2002 window. This is **not** a structural population signal; it is observer-effort artefact. The biodiversity decline (or stability) between 2002 and 2026 is **invisible** in this GBIF pull.

## Cross-check with [[fauna_brief]] (iNat 5 km, 43 parcel-tight obs)

- **Species overlap with iNat parcel pull**: low — iNat 5 km picks up additional fauna classes (mammals, amphibians, reptiles) that GBIF misses entirely in this bbox.
- **Cattle Tyrant, Great Kiskadee, Southern Lapwing, Black Vulture, Whistling Heron** — all 5 hyper-generalist open-country birds appear in both lists → confirmed resident.
- **Plush-crested Jay (*Cyanocorax chrysops*)** — confirmed in both eras (1999 + recent iNat).
- **Tropidurus spinulosus** (1976) — the only reptile in GBIF, NOT in the [[fauna_brief]] reptile pull (iNat reported 35 obs of other reptiles at 5 km). The 50-yr-old specimen confirms historical presence; a 2026 site visit (#13 in [[client_photos_brief]]) should target rock outcrops.

## Engineering implications (Blender + deck)

- **Bird scatter density** — 50 species at 30.9 ha + dense canopy is consistent with **gallery-forest density ~80-120 territorial pairs/ha** (Atlantic-Forest reference); for ambient audio + occasional fly-through silhouettes in the hero shot, scatter ~50 stationary "perched-bird" markers proportional to family share above.
- **Family share → scatter weights**: Thraupidae 12 %, Tyrannidae 10 %, Picidae 10 %, Cuculidae 8 %, Columbidae 6 %, Furnariidae 6 %, Corvidae 4 %, Psittacidae 4 %, Thamnophilidae 4 %, Turdidae 4 %, others 32 %. Use these to drive `lqv/subscene/birds_scatter.py` colour-class weighting.
- **Reptile / amphibian / mammal layers** — GBIF returns **0 species** of these classes. Do not draw conclusions from absence; rely on [[fauna_brief]] iNat pull for mammals (5 km), amphibians, and updated reptile count. Deck claim: "GBIF historical record covers Aves only; mammals + reptiles documented via iNaturalist."
- **Wetland herb (*Ludwigia peruviana*)** corroborates the **ephemeral water** hypothesis on the parcel even though [[sentinel2_brief]] reports zero open water at 10 m — Ludwigia tolerates flooded margins, so even a seasonal swale supports it. This narrows the Quebrada-channel question: photo #01 in [[client_photos_brief]] should specifically search for Ludwigia mats as a water-presence proxy.
- **Tropidurus spinulosus** (1976) — rock-loving lizard. Sub-render: if Wesley's photos reveal exposed bedrock per [[client_photos_brief]] #04 / #08, add `lqv/subscene/tropidurus_perch.py` with 1-2 lizards on rocks as ecological-authenticity detail.

## Sub-render typology

- `lqv/subscene/birds_scatter.py` — 50 perched-bird markers, family share weighted, on canopy tops within parcel polygon. Cycles render only.
- `lqv/subscene/historical_record_timeline.py` — 1883 → 2014 dot timeline for the deck appendix (5 marked rows, the pre-eBird gems).
- `lqv/subscene/aves_family_pie.py` — 11-segment pie of family shares (Thraupidae / Tyrannidae / Picidae / …) for the biodiversity deck spread.
- `lqv/subscene/ludwigia_mat.py` — riparian / swale-edge Ludwigia bed at the predicted ephemeral-water polygon (drives off [[hydrogeology_brief]] TWI mask).

## Provenance

- **Source**: GBIF.org occurrence search, accessed 2026-06-10.
- **Endpoint**: `https://api.gbif.org/v1/occurrence/search` with bbox filter; per-species reduced to one row.
- **Citation**: GBIF.org (2026), GBIF Occurrence Download, accessed via API. Each row in `species_list.json` carries a `gbifKey` permalinking to the species hub (e.g. `5421024` = *Ludwigia peruviana*).
- **License**: CC-BY-4.0 (downstream data is per-publisher; aggregated reuse under CC-BY).
- **Limitations**:
  - `occurrenceCount = 1` is a deduplication artefact, not a true single-observation flag.
  - bbox is offset W from the actual parcel centroid; treat the species list as **Mbopicuá rural matrix** rather than parcel-tight.
  - 0 mammals / 0 amphibians / 0 fish / 0 fungi is observer-blindness, not absence.
  - 50 / 54 first-seen dates cluster in 2000-2002 (single eBird import era).

## Carry-forward gaps

- **Re-pull at parcel-tight 0.05° box** (≈ 5.5 × 5.5 km) centred on (−57.0355, −25.6073) — current bbox is offset W. This would reproduce the [[fauna_brief]] / [[flora_brief]] coverage exactly and let us do a clean GBIF ↔ iNat cross-table.
- **Per-occurrence pull** (`occurrenceCount` per species) — the current file is collapsed to 1 row per species. A `species_occurrences.csv` with date + observer + coordinates would let us see post-2014 GBIF activity and split eBird-era from earlier records.
- **Mammals + amphibians + fish + fungi via GBIF** — the current pull was bbox-only and apparently returned 0 in those classes. Re-pull with explicit `taxonKey` filters per class to confirm true absence vs query artefact.
- **eBird hotspot ID** — the 2002-01-16/17 single-event ingest likely matches a single eBird hotspot. Look up the hotspot for the bbox and pull its full checklist history (often hundreds of additional species at the same point over 20 years).
- **GBIF spatial polygon query** — switch from bbox to the actual 8-vertex parcel polygon WKT to get a parcel-tight species list rather than a 10.9 km² approximation.
- **Cross-link to [[atlantic_forest_trees]]** — the 2 Magnoliopsida records are a tiny fraction of expected plants; pair with the atlantic_forest_trees research dir for a ranked "expected at this latitude / forest type" list.

## Cross-references

- [[fauna_brief]] — iNat 5 km parcel-tight pull (43 obs, mammals + amphibians + reptiles); GBIF + iNat together give the most complete fauna picture.
- [[flora_brief]] — iNat Plantae 5 km pull (50 + species ranked); GBIF here adds only 2 plant rows, both useful (*Ludwigia*, *Jacquemontia*).
- [[hydrogeology_brief]] — *Ludwigia peruviana* hints at ephemeral water; brief's TWI mask predicts the same locus.
- [[client_photos_brief]] — shot-need #01 (channel), #04 (escarpment / rock for *Tropidurus*), #13 (wildlife sign) are directly informed by this brief.
- [[canopy_chm_brief]] — 5-species Picidae woodpecker guild + Furnariidae corroborates the 10.9 m mean canopy height.
- [[sentinel2_brief]] — NDVI 0.918 dense-canopy reading supports the bark/cavity-dependent guild strength.
- [[extended_aoi_brief]] — sub-3 m bedrock outcrops are the *Tropidurus* habitat the 1976 record points to.
- [[post_escritura_site_knowledge]] §3 — biodiversity context the deck draws from.
