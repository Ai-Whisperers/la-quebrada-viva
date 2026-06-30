# Reconciled Project — Master Brief

**Date:** 2026-06-30
**Status:** Reconciled view (read-only — does not modify either source)
**Sources:**
- **Wes's working files** (the Excel/DOCX set Ivan pasted in) — **CANONICAL** for financial, cabin, infra, equipment, activities, F&B, materials, business structure
- **Ivan's LQV repo + working dir** (`Ai-Whisperers/la-quebrada-viva` + `/root/.hermes/lqv-splat/`) — **SUPPLEMENTARY** for escritura milestone, land details, 3DGS pipeline, Sonja's 2030 deadline, partnership structure, render-pipeline typology concept art

**How to read this document set:** This is the **merged view**. It does not modify or replace either source. Both stay intact (Wes's files locally, LQV repo on GitHub). This set is the single page Wes + Ivan + Kiki + Erebus read to understand the project as it stands now.

---

## 1. Project Identity (merged)

| Field | Value | Source |
|---|---|---|
| Project name | **Eco Jungle Resort Paraguay** (Wes's working name) | Wes's files |
| Working alias | La Quebrada Viva (LQV) | LQV repo |
| Location | Paraguay, riverfront jungle (exact location TBD) | Wes's files |
| **Confirmed land** | 62 ha in **Escobar, Paraguarí** (~120 km SE of Asunción) | LQV repo (Ivan's earlier work) |
| Currency (canonical) | **EUR** (primary, per Wes's models) | Wes's files |
| Currency (PY local) | PYG (₲) | Wes's files |
| Currency (cross-ref) | USD (Ivan's NL price doc) | LQV repo |
| **Escritura** | **Signed 2026-06-27** at commit `0081129` (escritura-2026-06-27 tag) | LQV repo |
| Phase 1 scope | 30 cabins (10 types), full infra + amenities, 3-year build | Wes's files |
| Phase 1 build budget | **€5,503,736** (excl. land) | Wes's financial model |
| Phase 1 occupancy scenarios | 20% / 25% / 35% | Wes's financial model |
| Hard milestone | **Sonja's 60th in 2030** = operational by Sept 2029 | LQV repo (Wes's verbal commitment) |
| Partnership | **Wesley + Thijs 75/25** (legal owners, escritura-frozen) | LQV repo |
| Investment vehicle | TBD: founder-controlled + 3-5 passive (per Wes) **OR** 4-entity BV cascade (per Ivan) | Conflict — see §10 |

---

## 2. The 4-Entity BV Cascade (Ivan's draft, NOT YET LOCKED)

Wes's working files mention a "founder-controlled structure with 3-5 passive investors getting capital + co-ownership." Ivan's LQV repo independently drafted a 4-entity BV cascade as a candidate structure. **Both are drafts, neither is locked.** The decision is owed by Wes + Thijs + (eventual) accountant.

**Ivan's 4-entity draft (from prior session):**
1. **Land BV (PY)** — owns 62 ha parcel. Stays with Wes + Thijs personally. Ground income stays in their pocket.
2. **Finance BV (NL)** — interface to Dutch investors. PY finance is easy locally; NL investors need a Dutch-facing entity to wire money into.
3. **Phase 1 BV** — build + rent Phase 1 (first 3-6 typologies). Self-liquidating.
4. **Phase 2 BV + Phase 3 BV** — later phases. Equipment cascade: when Phase 1 is done, sell machines to Phase 2 BV at cost-plus.

**Why this is interesting:** the equipment cascade means investors recover their machine money first in any phase. Lower risk than a single PY entity that mixes land + ops + equipment.

**Why it may not be right:** Wes's working files emphasize a "founder-controlled structure" that prevents removal/takeover. The 4-entity BV cascade with separate phase BVs is structurally similar (each phase BV is independent) but adds Dutch-incorporation complexity that the simple founder model avoids.

**Status:** **OPEN DECISION.** Booked as Idea F01 in the LQV catalog. See `docs/ideas/finance_legal/f01_4-entity_bv_cascade_(land_py_+_finance_nl_+_phase_.md`.

---

## 3. Cabin Plan — 30 cabins, 10 types (CANONICAL from Wes's files)

| Type | Qty | m² | Build €/m² | Total build € | Night price € | Avg guests |
|---|---|---|---|---|---|---|
| 2p Basic | 3 | 40 | 875 | €105,000 | €75 | 2 |
| 2p Boomhut (Treehouse) | 3 | 42 | 1,276 | €160,800 | €135 | 2 |
| 2p Beekhuisje (Creek) | 2 | 60 | 1,133 | €136,000 | €145 | 2 |
| 2p Luxe Spa | 7 | 90 | 1,517 | €955,500 | €220 | 2 |
| 4p Basic | 2 | 90 | 856 | €154,000 | €130 | 4 |
| 4p Boomhut | 2 | 95 | 1,176 | €223,500 | €190 | 4 |
| 4p Beekhuisje | 2 | 105 | 1,124 | €236,000 | €210 | 4 |
| 4p Luxe Spa | 3 | 115 | 1,484 | €513,750 | €290 | 4 |
| Family Basic Creek | 3 | 145 | 998 | €433,500 | €240 | 5.5 |
| Family Luxe Spa | 3 | 160 | 1,481 | €711,000 | €420 | 5.5 |
| **TOTAL** | **30** | | | **€3,629,050** | | |

**Build cost range:** €856-€1,517/m² (heavily influenced by luxury level: Basic vs Spa)
**Nightly rate range:** €75-€420
**Total Phase 1 cabin build:** €3.629M (66% of total Phase 1 capex)

**Note on Ivan's LQV 13 typologies:** Ivan's prior render pipeline (`lqv/typologies/`) contains 13 typology build files (cob, bottle, clay_terracotta, italian_stone, hobbit, boomhut, container, etc.) which were built as **concept art** during the 18-final-render sprint. These are NOT a commitment to 13 specific built structures. They serve as visual reference for Wes to choose from. Some (cob, boomhut) overlap with the 10-type plan. Some (hobbit, container, clay_terracotta) are not in the current 10-type plan. Decision needed: keep them as concept art only, or retire.

**See:** [`CABIN_CATALOG.md`](CABIN_CATALOG.md) for full per-type detail with build cost calculations, materials, and design notes.

---

## 4. Financial Model — €5,503,736 Phase 1 (CANONICAL from Wes's files)

### Capex Summary

| Item | Cost € | Notes |
|---|---|---|
| 30 cabins | 3,629,050 | All 10 types |
| Restaurant + lounge | 260,000 | Full service |
| Reception/office/laundry | 70,000 | Basic building |
| Natural pool/pond | 90,000 | Self-executed |
| Wellness basic | 65,000 | Sauna/cold plunge/massage |
| Roads/parking/earthworks | 80,000 | Own machines |
| Water/septic/sewer | 60,000 | Self-executed |
| Electric/internet/camera | 75,000 | |
| Landscaping/jungle/paths | 90,000 | Self-grown plants |
| Activities basic | 45,000 | Mini golf/archery |
| **Bali craftsmen** | **155,000** | 3 men × 18 months |
| **Paraguay build team** | **180,000** | 5-8 men × 36 months |
| Design/engineering/permits | 60,000 | |
| Transport/import/tools | 55,000 | |
| **Subtotal** | **4,914,050** | |
| Contingency 12% | 589,686 | |
| **TOTAL PHASE 1** | **5,503,736** | Excl. land |

### Build Phasing (3-year plan)

| Year | Scope | % of capex | Capex € |
|---|---|---|---|
| Year 1 | Basic infra + 5 cabins + reception | 35% | ~1,926,308 |
| Year 2 | Restaurant + pool + 10 cabins | 35% | ~1,926,308 |
| Year 3 | Final 15 cabins + wellness | 30% | ~1,651,120 |

### Revenue Model (3 scenarios)

| Scenario | Occupancy | Days/cabin | Cabin revenue € | Staff costs € | Fixed costs € | Total investment € |
|---|---|---|---|---|---|---|
| Negative | 20% (73 days) | 73 | 465,010 | 203,280 | 235,075 | 5,503,736 |
| Average | 25% (91.25 days) | 91 | 581,263 | 231,000 | 302,593 | 5,503,736 |
| Good | 35% (128 days) | 128 | 813,768 | 258,720 | 388,112 | 5,503,736 |

### Additional Revenue Streams (cabin revenue is only part)

- Breakfast: 65% guests × €7
- Lunch: 20% guests × €7
- Dinner: 45% guests × €15
- Cocktails: 25% guests × 2 × €6
- Bottle service rooms: €7,665-€13,414
- Honeymoon packages: €13,140-€22,995
- Wellness/spa revenue

### Staff Plan (27 base staff, +25% social costs)

| Role | Count | Monthly salary € |
|---|---|---|
| Resort manager | 1 | 1,500 |
| Reception | 2 | 650 |
| Housekeeping | 8 | 450 |
| Garden/maintenance | 4 | 500 |
| Chef/kitchen | 3 | 700 |
| Service/bar | 4 | 550 |
| Wellness | 2 | 500 |
| Security | 2 | 500 |
| Marketing/admin | 1 | 700 |

**Total personnel:** €203,280 (low scenario) → €231,000 (avg) → €258,720 (good)

**Note:** these roles are 4-5x more staff than the LQV catalog estimated (~7 workers for Phase 1). The full Phase 1 buildout is operationally heavier than the cob-house-only concept.

**See:** [`FINANCIAL_MODEL.md`](FINANCIAL_MODEL.md) for the full breakdown.

---

## 5. Build Approach

**Construction team:**
- 3 Bali craftsmen × 18 months = €155,000 (training + specialist bamboo/concrete work)
- 5-8 Paraguayan build team × 36 months = €180,000 (concrete + general construction)

**Approach:** Start with concrete + bamboo. Use Paraguayan construction workers first. Build in batches of 5 with 6 different styles so guests can return for new experiences.

**Build sequence:**
1. Year 1: Basic infrastructure (water, electric, roads, parking) + 5 first cabins + reception
2. Year 2: Restaurant + natural pool + 10 more cabins (Year-2 batch)
3. Year 3: Final 15 cabins + wellness + activities

**Important:**
- Build only in **dry season** (May-Oct) for cob/earthen work that needs dry cure
- 14 GB host constraint applies to any digital design (LQV render pipeline) but not to physical construction
- 3-5 month build window per cabin batch (typical)

---

## 6. Equipment Strategy

**Decision tree:**
- **Heavy equipment (excavators, cranes, loaders) → import 2nd hand from Netherlands**
  - 50-70% cost savings vs new
  - Example: 3-ton mini excavator = €18,000 (2nd hand NL import) vs €55,000 (new NL) vs ~€70,000 (new PY)
  - 8-ton crawler crane = €35,000 vs €135,000
  - 20-ton crawler crane = €60,000 vs €260,000
- **Standard agricultural / light equipment → buy new in Paraguay**
  - Tractors, dump trucks, flatbed trailers: PY market is competitive
- **Power tools** → mix (LQV render pipeline needs high-spec; build site can use mid-range)

**See:** [`EQUIPMENT_STRATEGY.md`](EQUIPMENT_STRATEGY.md) for the full 10-category equipment comparison tool.

---

## 7. Infrastructure Plan — 8 Phases

1. **Terrain survey & base** — georeferencing, elevation maps, 3D terrain model, water features, groundwater, soil, rock layers, road/utility locations
2. **Raw materials** — tierra roja, fill sand, topsoil, river sand, crushed stone grades, cement, concrete, rebar
3. **Water supply** — well drilling (50/100/150m), pumps, filters (sand/carbon/UV), water storage (5K-100K liters), HDPE pipes
4. **Sewer & water treatment** — PVC/beton pipes, inspection pits, pumping stations, biodigester, biological treatment, wetland/reed field, water reuse for irrigation
5. **Electricity** — ANDE grid connection, transformers (100-400kVA), generator (100-250kVA), cables, distribution boards
6. **Internet** — Starlink, fiber optic, local providers (Tigo/Claro/Personal)
7. **Roads & paving** — asphalt, poured concrete, concrete bricks, grass concrete tiles, gravel mats, curbs, drainage, culverts, wadis, rainwater basins
8. **Irrigation** — source, buffer basin, HDPE pipes, drip lines, sprinklers (pop-up/rotor/micro), pumps, automation computer, sensors, treated water reuse

**Status:** All 8 phases planned, prices NOT YET FILLED. Template exists in `Paraguay_Infra_Masterplan_Uitgebreid_NL.xlsx`.

**Ivan's 3DGS pipeline is relevant here** — the 3D terrain model in phase 1 can be built from Wes's 5 phone videos + ALOS DEM + Sentinel-2. This is the **"inmeten terrein"** work that Ivan already partially completed (per `docs/ideas/site_specifics/`).

**See:** [`INFRASTRUCTURE_8_PHASES.md`](INFRASTRUCTURE_8_PHASES.md) for the full per-phase scope.

---

## 8. Materials & Pricing — 17-Category Master List

**Priority codes:**
- 🔴 = Biggest impact on total build cost (resolve first)
- 🟠 = Important for local vs import comparison
- 🟡 = Important for resort appearance & rental value
- 🟢 = Needed later in project
- ⚙️ = Machines & tools
- 🚛 = Transport & logistics
- 📋 = Visit by appointment (require on-site supplier meetings)

**Categories:**
1. Raw construction (cement, concrete, blocks, bricks, rebar, sand, gravel) 🔴
2. Roofs & structures 🔴
3. Facades & exterior (plaster, stone, bamboo, cladding, lighting) 🟠
4. Frames, doors & glass (aluminum, sliding, double glazing) 🔴🟠
5. Interior finishing (tiles, PVC floors, paint, interior doors) 🟠
6. Sanitary & bathrooms 🟠
7. Kitchens 🟠
8. Furniture & interior 🟠🟡
9. Electrical & lighting 🔴
10. Water & sewer
11. Infrastructure (roads, parking, drainage)
12. Landscaping & nature
13. Wellness, eco pool & recreation
14. Large machines ⚙️
15. Small machines
16. Hand tools
17. Transport, import & logistics 🚛

**Ivan's NL prices doc has pricing for 13 of these categories** (cement, sand, gravel, bricks, iron, etc.) — see `docs/research/2026-06-30_construction_prices_paraguay_nl.md`. This can be **merged into the master template** to start filling in real numbers.

**See:** [`MATERIALS_PRICE_TEMPLATE.md`](MATERIALS_PRICE_TEMPLATE.md) for the full 14-sheet master with Ivan's existing prices filled in where available.

---

## 9. Activities — 25+ Catalogued

**Budget activities:** mini golf, axe throwing, nail hammering, zip line, scavenger hunt, night jungle trek, stargazing platform/dome tents, survival course (rope bridges/climbing/obstacles), catapult shooting, football panna field, petanque court

**Premium activities:** buggy & quad rental

**Health/wellness:** yoga, outdoor gym, breathing sessions, ice baths, bootcamp, kickboxing

**Entertainment:** campfire evenings with live music, live music at lounge, lounge parties, live football screening, jungle cinema, romantic private dinner by creek, floating breakfast, hammock zones, yoga platforms

**See:** [`ACTIVITIES_25_PLUS.md`](ACTIVITIES_25_PLUS.md) for the full per-activity detail with cost estimate + revenue model.

---

## 10. OPEN DECISIONS — Where the two sources disagree

These decisions are owed by Wes + (where applicable) Ivan, Kiki, accountant, lawyer. None are committed.

### 10.1 Business structure (4-entity BV vs founder-controlled + 3-5 passive)

| Aspect | Ivan's LQV draft (F01) | Wes's working files |
|---|---|---|
| Entity 1 | Land BV (PY, owned by Wes + Thijs) | Implied: founder-controlled structure |
| Entity 2 | Finance BV (NL, for Dutch investors) | Not mentioned |
| Entity 3-5 | Phase 1/2/3 BVs with equipment cascade | 3-5 passive investors in single structure |
| Control | Land BV stays with Wes+Thijs, phase BVs independent | Founder retains absolute control, no removal/takeover |
| NL hook | Finance BV makes NL investment easy | Not mentioned |

**Decision needed:** Which model? Both serve similar ends (founder control + investor capital). The 4-entity BV adds Dutch-incorporation tax optimization. The founder model is simpler. **Erebus recommendation: book a 1-hour call with a NL+PY dual-tax accountant to compare.**

**Tracked in:** `docs/ideas/finance_legal/f01_4-entity_bv_cascade_(land_py_+_finance_nl_+_phase_.md`

### 10.2 Currency canonical

| Source | Currency |
|---|---|
| Wes's financial model | EUR |
| Ivan's NL prices doc | USD + PYG |
| LQV render pipeline budget | USD |
| LQV BoQ | USD |

**Decision needed:** Pick one canonical base. **Erebus recommendation:** EUR for investor-facing (matches Wes's audience), USD for international comparisons, PYG for PY local costs. Three layers, explicit conversion dates, no hidden math.

**Tracked in:** Same F01 file.

### 10.3 Cabin typology: 10-type plan (Wes) vs 13 render-files (Ivan)

Wes's files show 10 specific types (2p/4p/family × basic/boomhut/beek/luxe spa). Ivan's render pipeline has 13 build files. **The 13 are concept art, not a build commitment.** The 10 are the build plan.

**Decision needed:** Retire Ivan's excess typology build files (hobbit, container, clay_terracotta, italian_stone_v1/v2, candle_path) or keep as concept art only?

**Tracked in:** `docs/ideas/finance_legal/f01_4-entity_bv_cascade_(land_py_+_finance_nl_+_phase_.md` (cross-reference to `docs/ideas/house_typologies/`)

### 10.4 LQV 3DGS pipeline integration

Ivan has built a 3DGS self-host pipeline (Vast.ai + COLMAP + gsplat) + Three.js viewer at `lqv-walkthrough.pages.dev`. This is relevant to:
- B07 phone capture pipeline (Wes needs to share 5 phone videos)
- Infrastructure phase 1 (3D terrain model)
- Buyer/investor experience (VR walkthrough before building)

**Status:** Pipeline ready, blocked on Wes's captures.

---

## 11. Sources of Truth — where to look for what

| Question | Look here |
|---|---|
| What does the project look like as a whole? | `MASTER_BRIEF.md` (this file) |
| What's the financial model? | `FINANCIAL_MODEL.md` |
| What are the 30 cabins? | `CABIN_CATALOG.md` |
| What's the 8-phase infra plan? | `INFRASTRUCTURE_8_PHASES.md` |
| What's the equipment buy/import strategy? | `EQUIPMENT_STRATEGY.md` |
| What activities are planned? | `ACTIVITIES_25_PLUS.md` |
| What's the materials pricing template? | `MATERIALS_PRICE_TEMPLATE.md` |
| What's the business structure? | `BUSINESS_STRUCTURE.md` |
| What land + escritura details are known? | `LAND_PARCEL.md` |
| What are the open decisions? | `OPEN_DECISIONS.md` |
| What does each idea in the catalog look like? | `docs/ideas/INDEX.md` (109 ideas, 12-section format) |
| What are the 20 patterns from reading the catalog? | `docs/ideas/INSIGHTS.md` |
| What 20 ideas did Erebus push into the catalog? | `docs/ideas/SUGGESTED.md` |
| What are the construction prices in NL/Gs/USD? | `docs/research/2026-06-30_construction_prices_paraguay_nl.md` |
| What did Wes say in his brainstorms? | `briefs/wes_recording_2026-06-30_{raw,dreamlist,actionlist}.md` |

---

## 12. Next steps (the bridge)

The reconciled view surfaces decisions, not makes them. The bridge from reconciled view to action:

1. **Wes reviews this reconciled view** + flags any data that's wrong
2. **Wes + Ivan** resolve the 4 open decisions in §10
3. **Erebus drafts the missing pieces** — most critical:
   - The 4-entity BV memo (Ivan's draft) for the accountant call
   - The buyer-pitch deck (Wes's financial model as foundation)
   - The price-collection sprint (Wes's 17-category list with Ivan's NL prices where available)
   - The Sonja-weekend brief (operational by 2030) for Phase 1 spec
4. **After 4-entity decision is made**, build a 1-page financial summary that both EUR (Wes's model) and PYG (PY local cost) reference

**One critical guard:** the escritura-frozen BoQ at `docs/boq/boq_rollup.md` (SHA `2e4c265c…01137`) is **not** in this reconciled view. It was the legal scope frozen at signing. It remains the legal baseline. The €5.5M Phase 1 buildout is the **next phase** — what happens after escritura closes.

---

**Maintained by:** Erebus (AI Whisperers) · **For:** Wesley van de Camp + Ivan + Kiki
**Last updated:** 2026-06-30
**Status:** First-pass reconciliation. Both sources preserved. This is a bridge, not a replacement.
