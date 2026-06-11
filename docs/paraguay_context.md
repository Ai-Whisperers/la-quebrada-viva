# Paraguay Context — Canonical Root

**Purpose.** Single entry point for every Paraguay-specific concern across the project:
site/climate/hydrology (where the building sits and what the weather does), market/community
(who comes, who supplies, who staffs), and regulatory/tax (what the law requires). This is an
**index doc**: it points to the canonical section in the source doc and gives a one-paragraph
orientation, so readers find what they need in one hop without re-reading either source in full.

Created **2026-06-11** as part of `docs/UPGRADE_PLAN.md` T1.5 (doc consolidation). The two
source docs are not deleted or excerpted — they remain authoritative for their own scope.
Cross-references in those docs point back here so navigation is bidirectional.

## Source docs

- **`docs/paraguay_clay_house_research.md`** — site & environment (v2, site CONFIRMED Escobar / Paraguarí).
  Authoritative for **location, hydrology, climate, orientation, infrastructure constraints,
  earthen-architecture rules for humid subtropical Paraguay**. Supersedes MASTER_BRIEF where they
  conflict on these topics.
- **`docs/EUROPEAN_TOURISM_SPEC.md`** — market & operations (Wesley's 2026-06-10 direction).
  Authoritative for **target market, San Bernardino / German / Dutch supply chain,
  vacation-rental typologies, events, regulatory framework (SENATUR / SET / municipal),
  tax classification, foreign ownership, marketing channels, phased rollout**.

## Topic index

### A. Site, geology, hydrology, climate

| Topic | Canonical location | One-line orientation |
| --- | --- | --- |
| Confirmed administrative location (Escobar District, Paraguarí) | `paraguay_clay_house_research.md` §2.1 | Where the property actually is on the map. |
| Satellite-search coordinates | `paraguay_clay_house_research.md` §2.2 | UTM / lat-lon anchors used during the site search. |
| Geological formation (Caacupé sandstone, red laterite) | `paraguay_clay_house_research.md` §2.3 | Why the boulders and soil read the colors they do. |
| Topographic profile (escarpment, terraces, stream) | `paraguay_clay_house_research.md` §2.4 | Vertical relationships that drive positional coupling in code. |
| Orientation (NNW sun for passive design) | `paraguay_clay_house_research.md` §2.5 | Why the corredor faces NNW and why Variant A sun elevation is 13°. |
| Five-zone stream system (28-photo reconstruction) | `paraguay_clay_house_research.md` §3.1–3.4 | Stream profile, water quality per zone, micro-hydro feasibility. |
| Site feature inventory | `paraguay_clay_house_research.md` §4 | Boulders, terraces, footbridge line y=−25.5, escarpment line y=20. |
| Material palette from photographs | `paraguay_clay_house_research.md` §6 | Hex colors for laterite, moss, sandstone, lapacho flowers, water. |
| Climate — temperature / humidity / rainfall / extremes | `paraguay_clay_house_research.md` §7 | The numeric envelope behind Rule 5 (overhangs) and Rule 6 (passive). |
| Infrastructure problems (grid, water, internet outages) | `paraguay_clay_house_research.md` §8 | The threat model behind Rule 7 (critical systems outage-proof). |

### B. Earthen architecture for humid subtropical Paraguay

| Topic | Canonical location | One-line orientation |
| --- | --- | --- |
| Cob construction (humidity-tuned mix, not desert cob) | `paraguay_clay_house_research.md` §9.1 | Why the cob is lime-finished, not cement-plastered (Rule 2). |
| Bottle walls (orientation, thermal mass, mosquito control) | `paraguay_clay_house_research.md` §9.2 | Why bottles are sealed and how they integrate with cob courses. |
| The 10 non-negotiable design rules | `MASTER_BRIEF.md` §14 (canonical) | Cross-referenced from `CLAUDE.md` "10 design rules" and `docs/research/README.md`. |
| Passive cooling for humid subtropical (not desert) | `paraguay_clay_house_research.md` §9.4 | Corredor + cross-vent + thermal mass; AC supplementary only. |

### C. Smart-home stack, water, energy

| Topic | Canonical location | One-line orientation |
| --- | --- | --- |
| Existing homelab + sensor deployment + automation platform | `paraguay_clay_house_research.md` §10 | Ivan's stack — what is already running vs what to add. |
| Stream-based + rainwater + greywater systems | `paraguay_clay_house_research.md` §11 | Why mosquito-proof mesh is mandatory on every cistern (Rule 10). |
| Micro-hydro + LiFePO4 + PV on separate steel frame | `paraguay_clay_house_research.md` §12 | The energy architecture behind Rules 7 and 9. |
| Structural systems (foundation, raised base) | `paraguay_clay_house_research.md` §13 | Why earthen walls never touch ground (Rule 4). |

### D. Target market & demand

| Topic | Canonical location | One-line orientation |
| --- | --- | --- |
| Who comes (North American / European, age band, demographics) | `EUROPEAN_TOURISM_SPEC.md` §1.1 | The customer profile this property is designed for. |
| Why Paraguay at all (Iguazú transit, heritage, NGO/Mennonite) | `EUROPEAN_TOURISM_SPEC.md` §1.2 | Why this niche exists at all in a non-mass-market country. |
| Price points, length of stay | `EUROPEAN_TOURISM_SPEC.md` §1.3 | USD ranges and typical booking duration. |
| Seasonality (June–August peak — both hemispheres flow inward) | `EUROPEAN_TOURISM_SPEC.md` §1.4 | When the property is full vs empty. |
| What this market expects / will not compromise on | `EUROPEAN_TOURISM_SPEC.md` §1.5–1.6 | Hard-stop requirements (water pressure, payments, privacy). |

### E. Supply chain — San Bernardino & immigrant communities

| Topic | Canonical location | One-line orientation |
| --- | --- | --- |
| San Bernardino as the regional anchor | `EUROPEAN_TOURISM_SPEC.md` §2.1 | What is already there: lake, Colegio Goethe, German bakeries. |
| German-Paraguayan community network | `EUROPEAN_TOURISM_SPEC.md` §2.2 | Chamber, schools, bilingual staff pool, brewers, butchers. |
| Dutch community (smaller, Wesley-relevant) | `EUROPEAN_TOURISM_SPEC.md` §2.3 | Cheese, herring, rijsttafel — the Wesley-narrative angles. |
| The end-to-end supply chain for the project | `EUROPEAN_TOURISM_SPEC.md` §2.4 | Who supplies what: bread / charcuterie / beer / chefs / FOH staff. |
| Logistics (transport from San Ber to Escobar) | `EUROPEAN_TOURISM_SPEC.md` §2.5 | Distance, delivery cadence, cold-chain considerations. |

### F. Property typologies, events, eco positioning

| Topic | Canonical location | One-line orientation |
| --- | --- | --- |
| Comparable properties in Paraguay & region | `EUROPEAN_TOURISM_SPEC.md` §3 | The current competitive landscape and what the gap is. |
| Vacation-rental typology mix (cob hero + supporting houses) | `EUROPEAN_TOURISM_SPEC.md` §4.1 | The 8 typologies in the housing park and what each is for. |
| Per-house requirements (water, power, connectivity, plugs) | `EUROPEAN_TOURISM_SPEC.md` §4.2 | The non-negotiable amenity floor (incl. Type C/F + 110V plugs). |
| Service level (concierge, cleaning, breakfast) | `EUROPEAN_TOURISM_SPEC.md` §4.3 | What "premium rural" means operationally. |
| Events as second business line | `EUROPEAN_TOURISM_SPEC.md` §5 | Weddings, retreats, family reunions, cultural workshops. |
| Eco-natural retreat positioning | `EUROPEAN_TOURISM_SPEC.md` §6 | What "eco-natural" means to this market and how to deliver it. |
| Restaurant as Phase 2 | `EUROPEAN_TOURISM_SPEC.md` §7 | European + Dutch cuisine sourced via San Ber; not Phase 1. |

### G. Regulatory, tax, ownership

| Topic | Canonical location | One-line orientation |
| --- | --- | --- |
| Municipal permits (Escobar district) | `EUROPEAN_TOURISM_SPEC.md` §8.1 | What needs to be filed at the local level. |
| SENATUR (national tourism registry) | `EUROPEAN_TOURISM_SPEC.md` §8.2 | Whether and how to register as a tourism establishment. |
| SET (tax) — IVA, IRP, IRACIS classification | `EUROPEAN_TOURISM_SPEC.md` §8.3 | The tax framework for short-term rentals. |
| Insurance | `EUROPEAN_TOURISM_SPEC.md` §8.4 | What is available locally, what is missing. |
| Hotel vs residential classification | `EUROPEAN_TOURISM_SPEC.md` §8.5 | The legal-class question that affects everything downstream. |
| Foreign ownership and remittance | `EUROPEAN_TOURISM_SPEC.md` §8.6 | Wesley + Thijs as Dutch nationals — moving money out. |

### H. Distribution & marketing

| Topic | Canonical location | One-line orientation |
| --- | --- | --- |
| OTAs (Booking, Airbnb, Vrbo, Mr & Mrs Smith) | `EUROPEAN_TOURISM_SPEC.md` §9.1 | Which platforms to prioritize for the target market. |
| Direct channel (own site, repeat guests) | `EUROPEAN_TOURISM_SPEC.md` §9.2 | The long-game margin play. |
| PR / travel media | `EUROPEAN_TOURISM_SPEC.md` §9.3 | Where the niche reads about rural Paraguay. |
| Partnership channels (Iguazú operators, heritage tours) | `EUROPEAN_TOURISM_SPEC.md` §9.4 | Inbound from adjacent itineraries. |
| Expat word-of-mouth | `EUROPEAN_TOURISM_SPEC.md` §9.5 | The Colegio Goethe alumni / Mennonite / NGO network. |
| Sequencing (what to invest in first) | `EUROPEAN_TOURISM_SPEC.md` §9.6 | Marketing-spend ordering for Phase 1 launch. |

### I. Phased rollout

| Topic | Canonical location | One-line orientation |
| --- | --- | --- |
| Phase 0 — Pre-closing (now → 2026-06-27 escritura) | `EUROPEAN_TOURISM_SPEC.md` §10 (Phase 0) | What must land before the notary signing. |
| Phase 1 — Houses + Airbnb-ready (months 1–9) | `EUROPEAN_TOURISM_SPEC.md` §10 (Phase 1) | First revenue line; the rental product. |
| Phase 2 — Scale houses + events begin (months 9–18) | `EUROPEAN_TOURISM_SPEC.md` §10 (Phase 2) | Adding events as second revenue line. |
| Phase 3 — Restaurant (year 2+) | `EUROPEAN_TOURISM_SPEC.md` §10 (Phase 3) | Why restaurant is intentionally Phase 3, not Phase 1. |
| Phase 4 — Refinement + scaling (year 3+) | `EUROPEAN_TOURISM_SPEC.md` §10 (Phase 4) | What "good" looks like at steady state. |

## How this doc relates to other roots

- **`MASTER_BRIEF.md`** owns the 10 design rules (§14). This doc points at the Paraguay-specific
  evidence behind each rule (climate data, water quality, infrastructure outage profile) — it
  does **not** restate the rules.
- **`CLAUDE.md`** owns the active-session invariants (renderer byte-identity, RNG ordering,
  positional coupling, MAT registry). This doc owns the *contextual reasoning* for why those
  invariants exist in a Paraguayan setting.
- **`HOUSING_PARK_CONCEPT.md`** owns Wesley's expanded 62-ha vision. `EUROPEAN_TOURISM_SPEC.md`
  refines that vision against the European-tourism market; this doc indexes that refinement.
- **`docs/research/README.md`** owns the 2026-06-10 research synthesis (case studies, site
  criteria, GIS tiering). This doc complements it — research synthesis stays there, the
  *Paraguay-specific projection of that synthesis onto our property* lives in the source docs
  this index points to.

## Update protocol

When adding Paraguay-specific material:

1. Decide whether it is site/environment (→ `paraguay_clay_house_research.md`) or
   market/operations/regulatory (→ `EUROPEAN_TOURISM_SPEC.md`).
2. Add the content to the appropriate source doc, in the matching section number.
3. Add a one-line row in the matching table above (Topic / Canonical location / One-line orientation).
4. If the topic is genuinely cross-cutting (e.g., a climate fact that drives a market timing
   decision), put the main content in the most natural source doc and add one row in *each*
   relevant section here, both pointing back to the canonical section.

Do not duplicate full sections into this doc. The contract is: this doc tells you *where*
to look; the source doc tells you *what* is true.
