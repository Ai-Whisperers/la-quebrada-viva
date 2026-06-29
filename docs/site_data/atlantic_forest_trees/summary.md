# Atlantic Forest Tree DB × LQV — Phase-0 §12 #3
**Citation.** Lima RAF, Oliveira AA, Pitta GR, et al. (2024) Comprehensive conservation assessments reveal high extinction risks across Atlantic Forest trees. Science 383(6680):219-225. DOI 10.1126/science.abq5099
**Source.** [https://github.com/LimaRAF/THREAT](https://github.com/LimaRAF/THREAT) — repo license GPL-3 for code, data tables redistributed with attribution.
## Counts
| Metric | Value |
| --- | ---: |
| Species in merged master (AF + PY threat + AR threat/endemic) | 5789 |
| Species with AF endemism record (Appendix F) | 5033 |
| AF endemic (pure + near-endemic, Lima et al. 2024) | 2381 |
| PY-threatened (MAG/SEAM list) | 121 |
| AR-threatened | 111 |
| AR-endemic (BAAPA cross-border) | 271 |
| Commercial timber species | 234 |
| Species with documented uses | 348 |
| Also documented within 25 km of LQV (Batch A: GBIF + iNat) | 86 |

## Top 15 families in merged checklist
| Family | Species |
| --- | ---: |
| Fabaceae | 707 |
| Myrtaceae | 707 |
| Rubiaceae | 338 |
| Melastomataceae | 298 |
| Lauraceae | 226 |
| Asteraceae | 185 |
| Euphorbiaceae | 184 |
| Solanaceae | 165 |
| Malvaceae | 121 |
| Annonaceae | 121 |
| Rutaceae | 99 |
| Sapotaceae | 94 |
| Sapindaceae | 87 |
| Erythroxylaceae | 83 |
| Moraceae | 81 |

## Top 25 LQV-area overlap species (already documented within 25 km)
| # | Binomial | Family | Vernacular (PY) | AF status | PY threat | Endemism | LQV occ. | Score |
| ---: | --- | --- | --- | --- | --- | --- | ---: | ---: |
| 1 | *Balfourodendron riedelianum* | Rutaceae | marfim | confirmed | en_peligro | widespread | 1 | 7 |
| 2 | *Cordia trichotoma* | Boraginaceae | — | confirmed | en_peligro | widespread | 1 | 7 |
| 3 | *Copaifera langsdorffii* | Fabaceae | Brazilian diesel tree | confirmed | — | widespread | 39 | 6 |
| 4 | *Parapiptadenia rigida* | Fabaceae | Anchico | confirmed | — | widespread | 34 | 6 |
| 5 | *Nectandra megapotamica* | Lauraceae | canela | confirmed | — | widespread | 28 | 6 |
| 6 | *Peltophorum dubium* | Fabaceae | caña fístola | new to AF | — | widespread | 26 | 6 |
| 7 | *Myrcianthes pungens* | Myrtaceae | guaviyú | confirmed | — | widespread | 20 | 6 |
| 8 | *Ocotea puberula* | Lauraceae | Laurel Guaica | confirmed | — | widespread | 18 | 6 |
| 9 | *Anadenanthera colubrina* | Fabaceae | Red Angico | confirmed | — | widespread | 2 | 6 |
| 10 | *Pterogyne nitens* | Fabaceae | — | confirmed | — | widespread | 2 | 6 |
| 11 | *Handroanthus impetiginosus* | Bignoniaceae | pink ipê | confirmed | — | widespread | 1 | 6 |
| 12 | *Psychotria leiocarpa* | Rubiaceae | — | confirmed | — | near_endemic | 1 | 6 |
| 13 | *Trichilia catigua* | Meliaceae | Catiguá | confirmed | — | widespread | 61 | 5 |
| 14 | *Luehea divaricata* | Malvaceae | Azota caballos | confirmed | — | widespread | 31 | 5 |
| 15 | *Eugenia uniflora* | Myrtaceae | cerezo de Cayena | confirmed | — | widespread | 28 | 5 |
| 16 | *Protium heptaphyllum* | Burseraceae | Caraño | confirmed | — | widespread | 28 | 5 |
| 17 | *Casearia gossypiosperma* | Salicaceae | Cambroé | confirmed | — | widespread | 27 | 5 |
| 18 | *Cordia americana* | Boraginaceae | guayaibí | confirmed | — | widespread | 27 | 5 |
| 19 | *Psidium guineense* | Myrtaceae | Allpa guayaba | confirmed | — | widespread | 24 | 5 |
| 20 | *Eugenia pyriformis* | Myrtaceae | perita costeña | confirmed | — | widespread | 23 | 5 |
| 21 | *Alchornea triplinervia* | Euphorbiaceae | Gakamenewe | confirmed | — | widespread | 21 | 5 |
| 22 | *Maytenus ilicifolia* | — | — | in PY threat list but not in AF checklist | en_peligro | — | 3 | 5 |
| 23 | *Syagrus romanzoffiana* | Arecaceae | Queen palm | confirmed | — | widespread | 2 | 5 |
| 24 | *Baccharis trimera* | — | — | in PY threat list but not in AF checklist | amenazada | — | 1 | 5 |
| 25 | *Ceiba speciosa* | Malvaceae | Silk floss tree | confirmed | — | widespread | 1 | 5 |

## Files
```
docs/site_data/atlantic_forest_trees/
├── atlantic_forest_checklist_master.csv  ← full join (binomial × AF/PY/AR/uses/LQV)
├── threatened_species_paraguay.csv       ← PY threat slice
└── summary.md                            ← this file
docs/site_data/flora/
└── expected_species_ranked.csv          ← candidate list, scored
```

## Caveats
- The 25 km biodiversity pull (Batch A) is taxonomically broad (Aves +
  Mammalia + Reptilia + Amphibia + Insecta + Liliopsida + Magnoliopsida).
  Only the two plant classes can intersect the AF tree checklist.
- The PY-threatened list bundled in the THREAT repo is a snapshot, not
  the live MADES/SEAM resolution. Treat as guidance, not legal status.
- `endemism_level_pct` is a continuous score (Lima et al. 2024 method);
  the categorical `endemism_group` (pure_endemic / near_endemic / occasional /
  widespread) is what the BAAPA conservation lit uses operationally.
- Authority strings are dropped on join (`Tabebuia heptaphylla (Vell.) Toledo`
  → `Tabebuia heptaphylla`); 1.3% of names collide with later taxonomic
  revisions (e.g. *Tabebuia* → *Handroanthus*). Validate before deck use.
- Cross-tab is for ecology-grounding the deck/digital twin, not for
  regulatory inventory — the SNC padron + a botanist transect remain
  the source of truth for any management plan.
