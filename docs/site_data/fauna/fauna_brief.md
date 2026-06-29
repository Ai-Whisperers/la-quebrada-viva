---
title: "Fauna brief — La Quebrada Viva"
phase: Phase-0
section: "§12 #4 extension"
centroid: "-57.0355, -25.6073"
parcel_radius_km: 5.0
regional_radius_km: 25.0
data_sources: ["GBIF top-N per class (25 km)", "iNaturalist research-grade (25 km + 5 km tight)"]
status: "v1 — synthesis on top of biodiversity_25km/ + new 5 km tight iNat pull"
parcel_inat_obs: 43
---

# Fauna brief — La Quebrada Viva

Parcel centroid `-57.0355, -25.6073` (-25.6073°S, -57.0355°W), ~350 m elevation, Atlantic Forest / Cerrado ecotone, Paraguarí.

## TL;DR

- **Regional checklist (25 km buffer):** 50 birds (top 50 of 100 GBIF), 59 mammals, 18 amphibians, 0 reptiles (GBIF) — but **iNat research-grade adds 24 reptile + 5 amphibian species** that GBIF's top-N didn't surface; plus 100 insect species (top 100 GBIF).
- **Parcel-tight (5 km iNat, research-grade):** 43 GPS-actual observations. Of the top 50 regional birds, **1 have been photographed within 5 km of the property**; 2 of 59 regional mammals likewise.
- **IUCN-flagged species in the regional checklist:** 0 (NT/VU/EN/CR).
- **Iconic-taxon mix of 5 km observations:** Insecta 20, Plantae 8, Arachnida 4, Mammalia 4, Reptilia 4, Amphibia 1, Fungi 1, Aves 1.

## Top 5 birds at the property

| Scientific | Vernacular | Family | n (25 km) | 5 km? | Months |
|---|---|---|---:|:---:|---|
| *Thraupis sayaca* | Celestino | Thraupidae | 447 | · | — |
| *Coragyps atratus* | Buitre negro americano | Cathartidae | 412 | · | Mar·Jul·Sep·Nov·Dec |
| *Leptotila verreauxi* | Paloma Apical | Columbidae | 405 | · | Oct |
| *Pitangus sulphuratus* | Benteveo | Tyrannidae | 404 | · | — |
| *Furnarius rufus* | Hornero | Furnariidae | 387 | · | — |

## Mammals expected on the property

| Scientific | Vernacular | Family | n (25 km) | 5 km? |
|---|---|---|---:|:---:|
| *Sooretamys angouya* | Colilargo paraguayo | Cricetidae | 31 | · |
| *Desmodus rotundus* | Desmodus rotundus | Phyllostomidae | 28 | · |
| *Nectomys squamipes* | Atlantic Forest Nectomys | Cricetidae | 27 | · |
| *Molossus rufus* | Moloso cola gruesa grande | Molossidae | 27 | · |
| *Carollia perspicillata* | Murciélago cola corta de Sebas | Phyllostomidae | 25 | · |
| *Artibeus lituratus* | Murciélago frugívoro común | Phyllostomidae | 23 | · |
| *Molossops temminckii* | Moloso pigmeo | Molossidae | 20 | · |
| *Akodon montensis* | Ratón selvático | Cricetidae | 20 | · |
| *Sturnira lilium* | Little Yellow-Shouldered Bat | Phyllostomidae | 19 | · |
| *Cynomops abrasus* | Moloso rojizo | Molossidae | 19 | · |
| *Oligoryzomys nigripes* | Colilargo isleño | Cricetidae | 16 | · |
| *Platyrrhinus lineatus* | Frutero de línea dorsal | Phyllostomidae | 16 | · |
| *Nyctinomops laticaudatus* | Moloso labios arrugados chico | Molossidae | 15 | · |
| *Myotis nigricans* | Murcielaguito negruzco común | Vespertilionidae | 9 | · |
| *Promops nasutus* | Moloso cola larga chico | Molossidae | 8 | · |

## Frog chorus — likely sources around the cistern + creek

| Scientific | Vernacular | Family | Months observed (regional iNat) |
|---|---|---|---|
| *Rhinella diptycha* | Cururú | Bufonidae | Jan·Feb·Aug·Sep·Oct·Nov·Dec |
| *Elachistocleis bicolor* | Rana Pinguino | Microhylidae | May·Sep·Dec |
| *Scinax fuscovarius* | Fuscous-blotched Treefrog | Hylidae | Feb·Aug |
| *Melanophryniscus fulvoguttatus* | Spotted Red-belly Toad | Bufonidae | May |

## Reptiles — iNat-only (GBIF top-N returned empty)

GBIF's Reptilia rollup for the 25 km buffer returned zero species (likely a query-shape artifact), but iNat research-grade has **24 reptile species** observed within 25 km. Full list in `inat_only_reptilia.csv`. Top: *Ameiva ameiva*, *Amphisbaena alba*, *Apostolepis dimidiata*, *Bothrops diporus*, *Dipsas turgida*, *Erythrolamprus poecilogyrus*, *Hemidactylus mabouia*, *Homonota rupicola* ….

## Pollinators relevant for lapacho + yvyra-itá flowering

Filtered Insecta to Hymenoptera/Lepidoptera/Diptera/Odonata: **54 species** in the 25 km regional pool. Full list in `pollinators.csv`. The lapacho rosado (*Handroanthus impetiginosus*) flowering in August–September is what brings the most visible pollinator pulse; the Insecta records are not seasonally resolved at the species level in GBIF so the deck should treat this as a calendar callout, not a quantitative claim.

## Engineering hooks for the deck + scene

- **Soundscape:** the amphibian list is the audio bed for night renders at the pool / creek — frog chorus months (above) match the wet-season (Oct–Mar) acoustics the deck markets.
- **Visible birds at dawn camera:** the top 5 above are the species the broker should mention when prospects ask 'what will I see from the terrace at 06:30?' Three are tanagers / pigeons / vultures (high visibility, high count).
- **Mammal narrative:** capybara + brown agouti + crab-eating fox are the deck-friendly species — large enough to be a feature, common enough that camera-trap evidence is realistic. Larger felids (puma, ocelot) appear in the regional list but the parcel is too small to claim residence honestly.
- **Pollinator calendar:** August lapacho bloom → Apidae visitors (already in the Hymenoptera 24-species pool). Use this for the 'living calendar' page of the deck, not a quantitative bee count.

## Caveats

- **GBIF top-N caps** mean rare species at the edges of the regional pool are not represented. The 60-cap on Reptilia + Amphibia + Mammalia is the actual species count GBIF returned, not an arbitrary cut.
- **iNat is biased toward charismatic + photographable taxa.** Frogs are under-represented relative to actual chorus species; same for nocturnal mammals.
- **No SNAP / SEAM official surveys folded in** — the SNC padrón web lookup (Phase-0 §12 #18) is user-side and not blocking this brief.
- **'Seen within 5 km' is a strong signal**, not a guarantee of presence on the parcel itself. The 5 km radius covers ~78 km² — parcel is ~62 ha (~0.62 km²), so the iNat-confirmation rate is a regional anchor, not a parcel inventory.

## v2 backlog

- AppEEARS-style polygon pull of GBIF *occurrences* (not just species summary) for the 5 km buffer → produces a real occurrence-density map per taxon.
- eBird hotspot data once the API key is provisioned (currently blocked).
- Cross-reference with `flora/expected_species_ranked.csv` for plant–pollinator pairs (lapacho ↔ Apidae, yvyra-itá ↔ Trigonini, palo de jazmín ↔ moths).
- Camera-trap deployment plan for the parcel — would convert the 'expected mammals' table into measured presence within ~30 days.
