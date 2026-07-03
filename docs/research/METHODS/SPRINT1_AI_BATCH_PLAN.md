# Sprint 1 AI batch — 30 items, ready to dispatch

**Purpose:** Document the next AI batch to run, with method routing and acceptance criteria per item. This is what gets dispatched in W1.1 (Sprint 1, weeks 2-4).

**Date:** 2026-06-30

---

## Batch composition: 30 items, 4 sub-batches by domain

### Sub-batch 1: Materials validation (6 items, 1 week)

| ID | Topic | Method | Acceptance | Result file (when done) |
|---|---|---|---|---|
| M09 | Bevestigingsmateriaal (fasteners) — bulk import vs local ferretería | MEM + URL fetch | 3 ferreteria quotes (Asunción, CDE, Encarnación) | `M09_fasteners.md` |
| M10 | Vloeren — tegels vs gepolijst cement vs hergebruikt hout | MEM + URL fetch | 3 quotes per material type | `M10_flooring.md` |
| M11 | Verf — exterior weatherbestendig, anti-hongos | MEM + URL fetch | 3 brands × price per L | `M11_paint.md` |
| M21 | Pool equipment (filter, pump) — import vs local | MEM + URL fetch | Equipment list for D6 wellness pool | `M21_pool_equipment.md` |
| M23 | AC units — sizing for PY climate, import lead time | MEM + URL fetch | 3 brands × 9K-24K BTU | `M23_ac_units.md` |
| M24 | Customs broker recommendations | MEM + URL fetch | 3 broker contacts in Asunción + CDE | `M24_customs_brokers.md` |

### Sub-batch 2: Infrastructure & F-series (4 items, 1 week)

| ID | Topic | Method | Acceptance | Result file |
|---|---|---|---|---|
| F10 | LiFePO4 battery sizing for backup | MEM | Sizing for 10-30 kWh + 3 brands | `F10_battery.md` |
| F15 | Cistern sizing for rainwater + backup | MEM | Sizing for 5K-50K L + materials | `F15_cistern.md` |
| F19 | Generator sizing for restaurant backup | MEM | Sizing 15-50 kVA + diesel cost | `F19_generator.md` |
| F20 | Toyota Tundra vs Presio PY dirt roads | MEM + existing research | 3 dealer quotes for 2026 | `F20_tundra.md` |

### Sub-batch 3: Finance, banking, FX (6 items, 1 week)

| ID | Topic | Method | Acceptance | Result file |
|---|---|---|---|---|
| L14 | Bancard / Pagopar — card payment onboarding | URL fetch | 3 onboarding options + fees | `L14_bancard.md` |
| L15 | Banco Itaú / Ueno / Familiar — B2B banking, dual PYG/USD | URL fetch | 3 banks' B2B options | `L15_banks.md` |
| L16 | Billeteras móviles — staff payments + tips | URL fetch | 3 wallet options (Tigo Money, Personal Pay, Zimple) | `L16_wallets.md` |
| L17 | FX transfer costs NL → PY (Wes + Thijs remitting) | URL fetch | Wise/Revolut/N26 fees comparison | `L17_fx.md` |
| L06 | PY holding company (S.A. vs S.R.L. vs E.A.S.) | MEM + attorney cross-ref | Recommend one type, justify | `L06_holding.md` |
| L08 | RUC applying for each BV (4× RUC) | MEM | Process + cost + time | `L08_ruc.md` |

### Sub-batch 4: Auto, market, partnerships, branding (8 items, 1 week)

| ID | Topic | Method | Acceptance | Result file |
|---|---|---|---|---|
| AH01 | Toyota Tundra vs Presio current pricing (dealer + import) | URL fetch + dealer outreach | 3 quotes for each model 2026 | `AH01_tundra_pricing.md` |
| AH02 | Tundra parts availability in PY | URL fetch | 3 dealer locations + parts lead times | `AH02_tundra_parts.md` |
| AH03 | Used vs new for bouwfase (cost-benefit) | MEM | NPV calc: used vs new over 5 years | `AH03_used_vs_new.md` |
| BR01 | Project name pick (Riverstone Valley vs Spanish alts) | MEM | Top 3 ranked + domain check | `BR01_name.md` |
| BR02 | Domain availability for RiverstoneValley.com + .com.py | Direct whois | Domain available status | `BR02_domain.md` |
| BR03 | Domain for Spanish alts (Villa del Cielo, etc.) | Direct whois | All 4 candidates checked | `BR03_spanish_domains.md` |
| PA03 | San Bernardino hotel list — cross-promotion targets | URL fetch + Sonja | 5 hotels with contact + rates | `PA03_san_ber_hotels.md` |
| MK08 | Air access for European visitors (Copa/Lufthansa/KLM/Iberia/Air Europa) | URL fetch | Route + frequency + price table | `MK08_air_access.md` |

### Sub-batch 5: Water, environment, food (6 items, 1 week)

| ID | Topic | Method | Acceptance | Result file |
|---|---|---|---|---|
| F14 | Stream water permit (INAA) | MEM | Permit process + time + cost | `F14_inaa.md` |
| EN02 | Native plant species list for Escobar | URL fetch + Kuikopee forester | Species list for Fase 1 | `EN02_native_plants.md` |
| FT10 | Chef partnership — German-trained chefs in PY | URL fetch + Sonja | 3 chef profiles + availability | `FT10_chef.md` |
| FT11 | Existing European restaurants in PY | URL fetch | 5 restaurants with cuisine + price | `FT11_existing_eu_rest.md` |
| FT14 | PY wine, cheese, chocolate, coffee (domestic products) | URL fetch | Supplier list for restaurant | `FT14_py_products.md` |
| FT15 | Restaurant tech stack — POS, reservations, online ordering | URL fetch | 3 options comparison | `FT15_restaurant_tech.md` |

---

## Routing summary

- **MEM-only items (no web needed):** 8 (M09, M10, M11, F10, F15, F19, L08, AH03, FT14)
- **URL fetch (direct):** 14 (M21, M23, M24, F20, L14, L15, L16, L17, AH02, BR02, BR03, PA03, MK08, FT11, FT15)
- **URL fetch + outreach (need a real vendor contact):** 4 (L06, AH01, BR01, FT10)
- **URL fetch + Sonja contact:** 2 (F14, EN02)
- **MEM only, no fetch:** 2 (L06, AH03)

---

## Dispatch order (priority by Sprint 1 weeks 2-4)

**Week 2 (parallel):**
- Sub-batch 1 (Materials) — 6 items
- Sub-batch 2 (Infrastructure) — 4 items
- Sub-batch 3 (Finance/banking) — 6 items

**Week 3 (parallel):**
- Sub-batch 4 (Auto/market/branding) — 8 items
- Sub-batch 5 (Water/food) — 6 items

**Week 4 (synthesis):**
- Compile "Sprint 1 final report" with cross-references
- Update WES_TODO and RESEARCH_CATALOGUE status

---

## Total time + cost

- **30 items × ~1 day each = 30 working days** (if sequential)
- **30 items / 5 parallel sub-batches = 6 calendar days** (if parallel agents)
- **Realistic:** 1-2 weeks with Erebus orchestrating + 2-3 subagents in parallel
- **Cost:** Brave API quota (already paid for); 0 incremental spend

---

## What this batch enables

After Sprint 1 + Sprint 0 combined:
- **All P1-blockers answered** (28 of 28)
- **Materials + insurance + infrastructure validated** for Fase 1 break-ground
- **Banking + FX + customs pipeline** for the operational setup
- **Auto + market + partnerships** for the Fase 2 buildout

**Wes can then book the attorney + Sonja calls in parallel**, having concrete numbers to discuss instead of abstractions.

---

## What is NOT in this batch (intentionally deferred)

- **All Fase 2+ items:** P3-P4 (Sprint 2-3) — back of queue
- **V05,V06,V08,V09 (VR event simulation):** F03 — Fase 2 marketing, not now
- **C04 (schooling for Wes's family):** P3 — lifestyle, not project-critical
- **R32, R33 (tech stack choice):** P3 — booking system not needed for 1-2 years
- **All S-series site decisions** (S01-S07):** depend on site visit (W1.2) for data
- **EN05, EN08, EN10 (forest + climate):** long-term, not Sprint 1

These are in the backlog. They'll move up as Phase 1 stabilizes.
