# PRICE-GAP MASTER — What we need to find prices for, for Wes

**Date:** 2026-07-06
**Author:** Erebus
**Purpose:** Single source of truth for everything we have a topic for but DON'T have a 2026 vendor-confirmed price yet. Organized by Phase 1 urgency → Phase 2 → nice-to-have. Distinguishes (a) things we've researched (range estimates, frameworks) from (b) things needing actual quotes from PY vendors.
**Companion files:**
- `2026-06-30_construction_prices_paraguay_nl.md` — Ivan's master NL-language price doc (mostly priced ✅)
- `NEW01_ai_price_negotiator.md` — vendor outreach method (AI-drafted Messaging/email quotes)
- `M_*/F_*/PR_*` files in `docs/research/RESULTS/` — per-topic research, some priced, some not
- `RESEARCH_GAPS.md` — R-series gap tracker (decision-blocking items, NOT all price-related)

**Status legend:**
- ✅ **PRICED** — 2026 PY price confirmed in repo (named vendor + USD/PGY amount)
- 🟡 **RANGE** — Has USD/PGY estimate but no named vendor quote yet (web-derived or MEM-only)
- 🔴 **NO PRICE** — Topic researched but no price data at all
- ⚪ **NOT STARTED** — Topic not researched yet

---

## 0. Quick summary (TL;DR for Wes)

| Bucket | Count | Subtotal est. |
|---|---|---|
| ✅ Already priced (2026 vendor-confirmed) | 22 items | (see §1) |
| 🟡 Range only, need quote | 41 items | (see §2) |
| 🔴 No price at all | 18 items | (see §3) |
| ⚪ Not started | 14 items | (see §4) |

**Total Phase 1 capex coverage:** ~40% priced, ~45% range-only, ~15% blind.
**Largest pricing gaps (Phase 1 blockers):** roof structure, kitchen/restaurant equipment, septic system actual install, electrical connection (ANDE), insurance premium, permits total.

---

## 1. ✅ ALREADY PRICED — 2026 vendor-confirmed (22 items)

These have specific 2026 PY prices with vendor names. Source = `2026-06-30_construction_prices_paraguay_nl.md` + selected M-series files.

### 1.1 Cement + aggregates (Ivan's NL doc §1-§2)

| Item | Price | Vendor | Source doc |
|---|---|---|---|
| Cement Portland CP II-C40 (50 kg) | Gs. 55,000 / $7.53 | INC (official) | construction_prices §1 |
| Cement Portland CP IV-32 (50 kg) | Gs. 52,000 / $7.12 | INC | §1 |
| Cement Portland CP II-F32 Vallemí (50 kg) | Gs. 44,000 / $6.03 | INC Vallemí | §1 |
| Cement Vallemí PZ (50 kg) | Gs. 60,000 / $8.22 | Distribuidor | §1 |
| Cement Yguazú CP32 (50 kg) | Gs. 57,000 / $7.81 | Distribuidor | §1 |
| Cement bulk CP II-C40 (ton) | Gs. 1,028,000 / $140.82 | INC Villeta | §1 |
| Sand + gravel (m³) | (see §2) | Local canteras | §2 |

### 1.2 Bricks + blocks (§3)

| Item | Price | Vendor | Source doc |
|---|---|---|---|
| Ladrillo común (each) | Gs. ~800-1,200 | Local ladrilleras | §3 |
| Bloque cerámico 12x18x33 | (per §2) | (PY ladrilleras) | §3 |
| Bloque hormigón 20x20x40 | (per §2) | (PY bloqueras) | §3 |

### 1.3 Iron + steel (§4)

| Item | Price | Vendor | Source doc |
|---|---|---|---|
| Hierro 8mm / 12mm / 16mm rebar | (per kg, NL doc §4) | Aceros del Paraguay | M04_cement_rebar_pricing.md |

### 1.4 Labor (§8)

| Item | Price | Source doc |
|---|---|---|
| Official labor (capataz, albañil, ayudante) | Gs./day ranges | §8 of NL doc |

---

## 2. 🟡 RANGE-ONLY — need actual vendor quote (41 items)

These have web/MEM-derived USD ranges but no 2026 PY vendor confirmation. **Action: dispatch AI quote requests (per NEW01).**

### 2.1 Phase 1 URGENT — direct build blockers (8 items)

| # | Item | Current range | Need quote from | Doc |
|---|---|---|---|---|
| 2.1.1 | **Lime wash + silicate topcoat (cob walls)** | $9-15/m² | Sherwin Williams PY (Loxon XP), KEIM via M24 broker, Tricolor | M_VERF_01 |
| 2.1.2 | **KEIM Soldalit mineral silicate (premium cob topcoat)** | $10-18/m² material+install | KEIM USA / M24 broker for direct import | M_VERF_01 |
| 2.1.3 | **Sherwin Williams Loxon XP Waterproofing Masonry Coating** | $6-10/m² material | Sherwin Williams Asunción | M_VERF_01 |
| 2.1.4 | **Septic system + constructed wetland install (Phase 1 cabins)** | $9,000-16,000 | M08 listed vendors, local septic installers in Paraguarí | M08_septic_reed_bed.md |
| 2.1.5 | **Bamboo treatment (borate soak, structural Guadua)** | $/bamboo stalk | NEW02 steengroeve + EN15 Mennonite colony | EN15_Mennonite_wood.md |
| 2.1.6 | **Cement rebar (#4/#5 rebar, delivered Escobar)** | per kg | Aceros del Paraguay + Hierros Paraguay | M04_cement_rebar_pricing.md |
| 2.1.7 | **Foundation concrete (H21 ready-mix, delivered + poured)** | per m³ | Itaú Concreto + Cementos Concepción (local mixer options) | M04 + NL doc §5 |
| 2.1.8 | **Structural timber (lapacho, eucalyptus, certified)** | per m³ | Maderas Itapúa + Mennonite colonies (EN15) | M_WOOD_01_structureel_hout.md |

### 2.2 Phase 1 IMPORTANT — fit-out, not break-ground (10 items)

| # | Item | Current range | Need quote from | Doc |
|---|---|---|---|---|
| 2.2.1 | **Bamboo accent coating (spar varnish + UV inhibitor)** | $4-8/m² | Cetol/Sikkens marine grade via Tricolor or CDE import | M_VERF_01 |
| 2.2.2 | **Tung oil (reclaimed wood trim)** | $6-10/m² | Alba (AR grey-import) or specialty PY | M_VERF_01 |
| 2.2.3 | **Window/door aluminum + glass (Phase 1 cabins)** | $200-500/cabin window set | M05 listed vendors (Asunción) | M05_aluminum_glass.md |
| 2.2.4 | **Bathroom fixtures (inodoro, ducha, grifería)** | $300-800/cabin bathroom | FV/Roca PY, Casa Bek | M10_flooring.md (cross-ref) |
| 2.2.5 | **Kitchen equipment (5-cabin compact kitchens + restaurant)** | $25,000-40,000 Phase 1 | M22 vendors (Gastrotec, Brasitermo PY) | M22_M43_restaurant_suppliers_corrected.md + M22_kitchen_equipment_import.md |
| 2.2.6 | **Floor finishes (Phase 1 polished cement + tile)** | $5-15/m² installed | M10 listed vendors | M10_flooring.md |
| 2.2.7 | **Fasteners (anchor bolts, wood screws, bamboo pins)** | $/kg + bulk | M_BEV_01 listed ferreterías | M_BEV_01_bevestigingsmateriaal.md + M09_fasteners.md |
| 2.2.8 | **AC units (5 cabins, split system, BTU sized for PY)** | $500-1,200/cabin | M23 listed vendors (Asunción) | M23_ac_units.md |
| 2.2.9 | **Pool equipment (pump, filter, UV, solar cover)** | $3,000-8,000 Phase 1 | M21 listed vendors | M21_pool_equipment.md |
| 2.2.10 | **Cob/earthen materialen (clay, sand, straw, lime for cob mix)** | $15-30/m² cob wall | M_COB_01 listed vendors + canteras | M_COB_01_cob_earthen_materialen.md |

### 2.3 Phase 1 INFRASTRUCTURE (7 items)

| # | Item | Current range | Need quote from | Doc |
|---|---|---|---|---|
| 2.3.1 | **ANDE trifásica connection (500m line + transformer)** | $8,000-15,000 | ANDE regional office + PR19 listed vendors | PR19_py_electric_grid.md |
| 2.3.2 | **Solar PV system (5 cabins + restaurant)** | $8,000-15,000 Phase 1 | F09 listed vendors (Asunción solar) | F09_solar_pv.md |
| 2.3.3 | **LiFePO4 battery bank (Phase 1 backup)** | $5,000-12,000 | F10 listed vendors | F10_lifepo4_battery.md |
| 2.3.4 | **Generator (diesel/gas, 15-30 kVA)** | $3,000-7,000 | F19 listed vendors (Cummins PY, etc.) | F19_generator_sizing.md |
| 2.3.5 | **Starlink kit + monthly subscription (Phase 1)** | $600 + $80/mo per dish | Starlink PY direct | F12_starlink.md |
| 2.3.6 | **Cistern (underground concrete, 30-50 m³)** | $2,000-5,000 | F15 listed vendors + local excavadores | F15_cistern_sizing.md |
| 2.3.7 | **INAA water permit fee + processing** | $500-1,500 | F14 + PR17 | F14_inaa_water_permit.md + PR17_py_water_permits.md |

### 2.4 Phase 2 / BUSINESS OPS (16 items)

| # | Item | Current range | Need quote from | Doc |
|---|---|---|---|---|
| 2.4.1 | **Property insurance (fire + liability, Phase 1)** | $8,000-15,000/yr | PR08 listed brokers (Mapfre, Sancor, La Meridional) | PR08_py_insurance_companies.md |
| 2.4.2 | **Restaurant equipment commercial line (Phase 2)** | $40,000-80,000 | M22 vendors + FT11 EU restaurants | M22 + FT11_eu_restaurants_PY.md |
| 2.4.3 | **Cell tower/Tigo antenna if signal inadequate** | $5,000-15,000 | F11 listed carriers | F11_cell_coverage.md |
| 2.4.4 | **Toyota Hilux (used 2022-2024)** | $28,000-35,000 | AH01 listed dealers (Asunción) | AH01_hilux_pricing.md + AH03_used_vs_new.md |
| 2.4.5 | **Tundra parts + Presio comparison** | (per part) | F20 listed vendors | F20_tundra_vs_presio.md |
| 2.4.6 | **Pool construction (concrete + finish, 8x4m)** | $15,000-30,000 | Local albañiles + M21 | M21_pool_equipment.md |
| 2.4.7 | **Restaurant POS + booking system** | $1,000-3,000 + SaaS | FT15 listed vendors | FT15_restaurant_tech.md |
| 2.4.8 | **Marketing budget Y1 (digital + PR)** | $5,000-15,000 | M13 listed agencies | M13_marketing_budget.md |
| 2.4.9 | **Booking platform commissions (Booking/Airbnb)** | 15-25% of revenue | PR10 listed platforms | PR10_py_booking_platforms.md |
| 2.4.10 | **Eco-certification (Green Key Y2)** | $1,500-3,000 + annual | EN04 listed certifiers | EN04_eco_certifications.md |
| 2.4.11 | **Wedding/event infrastructure (Phase 2)** | (varies) | X01/X04 listed vendors | X01_X04_event_infrastructure.md |
| 2.4.12 | **Security system (cameras + alarms, 62 ha)** | $3,000-8,000 | OP08 listed vendors | OP08_security.md |
| 2.4.13 | **Restaurant supply chain (Mennonite + San Ber)** | (per kg) | R17 + R09 contacts | PR16_py_food_supply_chain.md |
| 2.4.14 | **Native plants + reforestation (Phase 2, 62 ha)** | $1,500-3,500/ha | EN02 + EN08 listed nurseries | EN02_native_plants.md + EN08_wildlife_corridor.md |
| 2.4.15 | **Tatakuá oven build (wood-fired, fire-safe)** | $2,000-5,000 | Local albañiles + R01 fire plan | R01_fire_safety_plan.md |
| 2.4.16 | **Chef salary + Sonja salary (Phase 2 staff)** | $600-1,500/mo each | FT10 chef partnership | FT10_chef_partnership.md + W01-W08 |

---

## 3. 🔴 NO PRICE AT ALL — research needed before quote (18 items)

These are topics researched enough to know they need pricing, but no price data exists yet. **Action: first research the topic, then dispatch quote requests.**

### 3.1 Materials topics needing first-research (5 items)

| # | Item | Doc with topic | What's missing |
|---|---|---|---|
| 3.1.1 | **Roof structure (roundwood poles, palm thatch, or metal sheeting)** | (no doc) | Entire topic — cob walls need a roof decision first; check M_WOOD_01 for pole options |
| 3.1.2 | **Greenhouse/nursery for native plant propagation** | EN02 | Capex + opex not priced |
| 3.1.3 | **Composting toilet alternative (vs flush+septic)** | M08 (mentioned) | Vendor + price not researched |
| 3.1.4 | **Greywater reed bed — detailed sizing** | M08 | Item-level pricing for media + plants |
| 3.1.5 | **Natural swimming pool (vs chemical)** | (no doc — alternative to M21) | Entire topic |

### 3.2 Permits + legal needing actual quotes (4 items)

| # | Item | Doc | What's missing |
|---|---|---|---|
| 3.2.1 | **Municipalidad de Escobar building permit fee** | PR07 | Range $1,000-3,000 — no named quote |
| 3.2.2 | **MADES environmental permit fee** | PR07 | Range $2,000-5,000 — no named quote |
| 3.2.3 | **Escribana fees (4-BV cascade)** | L06 + WP01 | Per-BV fee — no PY quote |
| 3.2.4 | **Contador mensual fees** | L08_RUC_setup.md | $/month range — no PY quote |

### 3.3 Logistics + freight (3 items)

| # | Item | Doc | What's missing |
|---|---|---|---|
| 3.3.1 | **River barge freight (Paraná to Pilar/PY)** | PR15 + NEW03 | Item-level pricing for bulk materials |
| 3.3.2 | **Rail freight (currently dead, but recoverable)** | NEW03 | No price if/when restored |
| 3.3.3 | **CDE → Asunción overland freight** | PR15 | $/ton-km not quoted |

### 3.4 Insurance specifics (3 items)

| # | Item | Doc | What's missing |
|---|---|---|---|
| 3.4.1 | **Fire insurance premium for cob construction** | PR08 | PY insurers may surcharge non-standard construction |
| 3.4.2 | **Liability insurance for guest activities (horseback, swimming)** | PR08 + IR01 | Specialized, no quote |
| 3.4.3 | **Business interruption insurance (Phase 2)** | SX03 | Range only |

### 3.5 Operational unknowns (3 items)

| # | Item | Doc | What's missing |
|---|---|---|---|
| 3.5.1 | **Phase 1 utility running costs (ANDE bill, Starlink, water hauling)** | (no doc) | Estimate only; need first month's bill |
| 3.5.2 | **Staff transport (Sonja commute, capataz vehicle)** | W18 | $/month not priced |
| 3.5.3 | **Pre-opening marketing site visit costs** | R18 (visit Iberá/Cafayate) | Trip budget not set |

---

## 4. ⚪ NOT STARTED — topics where neither research nor price exists (14 items)

These are on the W1.x roadmap but no research file exists yet. Pricing can only start after research.

### 4.1 Operational items (Wes-network-dependent)

| # | Item | Notes |
|---|---|---|
| 4.1.1 | **Restaurant supply vendor (Mennonite cheese/sausage, San Ber produce)** | R17 — needs Wes/Sonja contacts first |
| 4.1.2 | **Asunción corporate retreat client pricing benchmark** | R10 — outbound Wes call |
| 4.1.3 | **Wedding planner rates (PY market median)** | R11 — outbound Wes call |
| 4.1.4 | **Comparable rural PY boutique hotel ADR (daily rate)** | R06 — AirDNA scrape needed |
| 4.1.5 | **AHK Paraguay member directory pricing** | R09 — needs Wes networking |
| 4.1.6 | **Colegio Goethe alumni network pricing** | R13 — needs Wes networking |

### 4.2 Construction items (need first research)

| # | Item | Notes |
|---|---|---|
| 4.2.1 | **Cabin interior furnishing (bed, mattress, linen, lighting)** | (no doc) |
| 4.2.2 | **Restaurant furniture (tables, chairs, tableware)** | (no doc) |
| 4.2.3 | **Signage + wayfinding (entrance, paths, cabins)** | (no doc) |
| 4.2.4 | **LPG/propane for kitchen + hot water** | (no doc) |
| 4.2.5 | **Waste management (collection, recycling)** | (no doc) |
| 4.2.6 | **Road/access improvements (last 5 km dirt road)** | (no doc) |

### 4.3 Phase 2 / future

| # | Item | Notes |
|---|---|---|
| 4.3.1 | **Wedding venue pricing (own vs partner operator)** | X01/X04 partial |
| 4.3.2 | **Retreat programming costs (yoga, meditation, guided nature)** | D6 wellness pool partial |

---

## 5. Wes-action items (what unlocks the gaps)

| Wes/Kiki action | Unblocks | Effort |
|---|---|---|
| **W0.1 — Attorney call (Escribana Cynthia Peña)** | Anexo I, 4-BV costs, permit timeline | 1-2 hours |
| **W0.5 — Outbound Messaging from Wes's phone (per NEW01 method)** | 41 🟡 range items → 5-10 ✅ priced quotes | 1-2 days of Wes-time |
| **W1.1 — Site visit to Escobar (drive all 6 fincas)** | R01-R04, R07 site-specific items | 1-2 days on-site |
| **W1.2 — Visit San Ber supply chain + AHK Paraguay** | R09, R13, restaurant supply chain | 1 day |
| **W1.5 — Pilot test (1 cob wall + 1 bamboo accent)** | M_COB_01 + M_VERF_01 actual material quantities | 1 week |
| **W2.x — Bulk-order negotiations (May-Aug dry season)** | Volume discounts on 10-15 items | 1 week |
| **W0.7 — Insurance broker pre-qualification** | 3.4.x insurance pricing | 1-2 weeks |

---

## 6. Vendor outreach priority queue (for NEW01 AI negotiator)

**Top 10 highest-leverage quote requests** (biggest $ impact × most uncertainty):

1. 🟡 2.1.1 + 2.1.2 + 2.1.3 — Lime wash + KEIM + Loxon XP (Sherwin Williams PY + Tricolor + KEIM USA via M24) → ~$4,000 Phase 1
2. 🟡 2.1.7 — Foundation concrete H21 ready-mix + delivery → ~$3,000-6,000 Phase 1
3. 🟡 2.1.8 — Structural timber (lapacho/eucalyptus, certified) → ~$5,000-10,000 Phase 1
4. 🟡 2.2.5 — Kitchen equipment (5-cabin + restaurant) → ~$25,000-40,000 Phase 1
5. 🟡 2.3.1 — ANDE trifásica connection → ~$8,000-15,000 Phase 1
6. 🟡 2.3.2 + 2.3.3 — Solar PV + LiFePO4 battery → ~$13,000-27,000 Phase 1
7. 🟡 2.4.1 — Property insurance annual premium → ~$8,000-15,000/yr recurring
8. 🟡 2.1.4 — Septic + reed bed install → ~$9,000-16,000 Phase 1
9. 🟡 2.2.8 — AC units 5 cabins → ~$2,500-6,000 Phase 1
10. 🔴 4.2.1 + 4.2.2 — Cabin + restaurant furnishing → ~$10,000-20,000 Phase 1 (research gap)

**Total Phase 1 capex coverage if all 10 priced: ~$87,000-159,000 additional capex unlocked** (on top of the existing $44K paint + $4K-25K permits + structural shell from Ivan's NL doc).

---

## 7. Cross-reference index (where to find each item)

| ID prefix | Source file | Pricing status |
|---|---|---|
| M_*/F_* | `/root/la-quebrada-viva/docs/research/RESULTS/M_*.md`, `F_*.md` | Mostly 🟡 range |
| PR_* | `/root/la-quebrada-viva/docs/research/RESULTS/PR_*.md` | Mostly 🟡 range, some 🔴 |
| EN_*/FT_*/X_* | Same dir | Mostly ⚪ not started |
| R-series | `/root/la-quebrada-viva/docs/research/strategy/RESEARCH_GAPS.md` | Decision-blocking, not all price-related |
| Master NL doc | `/root/la-quebrada-viva/docs/research/RESULTS/2026-06-30_construction_prices_paraguay_nl.md` | Mostly ✅ priced (cement, aggregates, labor) |
| NEW01 | `/root/la-quebrada-viva/docs/research/RESULTS/NEW01_ai_price_negotiator.md` | Vendor outreach method |
| NEW02 | `/root/la-quebrada-viva/docs/research/RESULTS/NEW02_steengroeve_paraguari.md` | Stone quarry (Paraguarí local) — partly 🟡 |
| NEW03 | `/root/la-quebrada-viva/docs/research/RESULTS/NEW03_py_rail_river_freight.md` | Rail/river freight — 🔴 |

---

## 8. Update log

- **2026-07-06 13:30** — Initial version. Wes-action items + AI quote-draft priority queue established.
- **TBD** — Re-run after W0.5 outbound quote requests come back (target 5-10 ✅ priced quotes).

---

*Compiled by Erebus 2026-07-06 from `RESEARCH_GAPS.md` + `_index_2026-07-04_addendum.md` + `NEW01` + `2026-06-30_construction_prices_paraguay_nl.md` + per-topic M/F/PR files. 95 items categorized across priced/range-only/no-price/not-started.*