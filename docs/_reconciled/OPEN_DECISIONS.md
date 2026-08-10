# Open Decisions — Where the Two Sources Disagree

**Date:** 2026-06-30
**Status:** Active list of decisions owed. Updated as Wes + Ivan + Kiki make calls.

---

## How this document is organized

Each open decision has:
- **What it is** (1 sentence)
- **The 2-3 options** being weighed
- **Who needs to decide** (Wes, Ivan, Kiki, accountant, etc.)
- **When it blocks** (which downstream work is held)
- **Recommendation** (Erebus's take, not binding)
- **Status** (open, in_progress, decided)

---

## Decision 1 — Business structure (4-entity BV vs founder-controlled vs hybrid)

**What it is:** What legal structure sits on top of the escritura ownership for Phase 1 operations + investor capital?

**Options:**
- (a) Wes's founder-controlled (1 PY entity, 3-5 passive investors)
- (b) Ivan's 4-entity BV cascade (land PY + finance NL + Phase 1 PY + Phase 2 PY)
- (c) Hybrid: Land BV + Operational S.A. + NL holding

**Who decides:** Wes + Thijs, with accountant recommendation

**Blocks:** Investor pitch deck, capital raise timing, Phase 1 capex deployment

**Recommendation:** Hybrid (option c). Best of both — land equity protected + NL hook + simpler than 4-entity

**Status:** OPEN — needs NL+PY dual-tax accountant consultation

**See:** `BUSINESS_STRUCTURE.md` for full analysis

**Tracked in:** RV catalog `F01_4-entity_bv_cascade...md`

---

## Decision 2 — Currency canonical

**What it is:** Which currency is the canonical base for the financial model?

**Options:**
- (a) EUR (Wes's current model)
- (b) USD (international investor + banker standard)
- (c) Three-layer: EUR (investor-facing) + USD (international) + PYG (PY local) with explicit conversion

**Who decides:** Wes (it's his money)

**Blocks:** Cross-referencing between the financial model and any cost research

**Recommendation:** Option (c) three-layer. EUR for investor pitch, USD for international, PYG for PY local. All with explicit FX date.

**Status:** OPEN

**Tracked in:** Same F01

---

## Decision 3 — Cabin typology scope: 10-type plan vs 13 render-files

**What it is:** Ivan's render pipeline has 13 typology build files. Wes's 10-type plan has 10. How to reconcile?

**Options:**
- (a) Retire Ivan's 3 extra (hobbit, container, clay_terracotta) + italian_stone_v1/v2
- (b) Keep all 13 as concept art, separate from build plan
- (c) Build only 6-7 of Ivan's that match Wes's types (cob, bottle, boomhut, bamboo river, etc.)

**Who decides:** Wes (he chooses what to build)

**Blocks:** Render pipeline maintenance, future type additions

**Recommendation:** Option (b) — keep all 13 as concept art, separate from build commitment. Cheapest, preserves options.

**Status:** OPEN

**See:** `CABIN_CATALOG.md` for the cross-reference table

**Tracked in:** RV catalog `house_typologies/` (4 ideas including T04 worker housing)

---

## Decision 4 — RV 3DGS pipeline integration

**What it is:** Ivan has a 3DGS self-host pipeline (Vast.ai + COLMAP + gsplat) + Three.js viewer. Where does it fit in Phase 1?

**Options:**
- (a) Phase 1 infra: 3D terrain model from 5 phone videos (kills 2 birds: validates pipeline + produces engineering base map)
- (b) Phase 2 marketing: VR walkthrough for investors after first 5 cabins built
- (c) Both: (a) for infra + (b) for marketing, sequenced

**Who decides:** Wes + Ivan (technical)

**Blocks:** Wes's phone capture pipeline (B07), buyer experience stack (B01-B05)

**Recommendation:** Option (c) — but (a) is the immediate priority. Even 2 short videos = enough to start training.

**Status:** BLOCKED on Wes's captures (B07)

**See:** `LAND_PARCEL.md` §4 + RV catalog `B07_phone_capture_pipeline...md`

---

## Decision 5 — Materials pricing collection sprint

**What it is:** Wes has 17-category priority list + 14-sheet master template. Ivan has partial NL prices doc. Need full data to fill the templates.

**Options:**
- (a) Wes travels to PY, visits 30+ suppliers in 2-week sprint (Q3 2026)
- (b) Erebus researches online + drafts quotes from 17 categories (faster but less accurate)
- (c) Hybrid: Erebus does online research, Wes validates top 10 categories in person

**Who decides:** Wes (operational) + Erebus (research)

**Blocks:** Cabin build cost accuracy, financial model confidence, investor pitch credibility

**Recommendation:** Option (c). Get to 70% accuracy in 2 weeks, then refine.

**Status:** OPEN

**See:** `MATERIALS_PRICE_TEMPLATE.md`

**Tracked in:** RV catalog `docs/ideas/construction/` (15 ideas)

---

## Decision 6 — Insurance pre-qualification BEFORE breaking ground

**What it is:** Per Insight #3, insurance availability + cost is the gate before any structure goes up.

**Options:**
- (a) Get 3 international broker quotes (Marsh, Aon, WTW) before any construction
- (b) Build first, insure second (risk: uninsurable structure)
- (c) Skip insurance (highest risk)

**Who decides:** Wes + insurance broker

**Blocks:** ANY structure going up

**Recommendation:** Option (a). Hard gate. Even 1 quote is enough to validate the path.

**Status:** OPEN — URGENT

**See:** RV catalog `I10_insurance_broker_pre-qualification...md` + `F05_insurance_stack...md` + `R01_fire_safety_plan...md`

**Tracked in:** RV catalog `risk_mitigation/`

---

## Decision 7 — Build order within Phase 1 (Year 1: 5 cabins)

**What it is:** Which 5 cabin types are first? Where on the property?

**Options:**
- (a) 1 of each type (5 cabins, 1 of each): testing the full mix early
- (b) All 2p Basic (cheapest, fastest): validate operations before going premium
- (c) 2p Luxe Spa + 2p Boomhut (highest margin, Instagram-driven): premium-first strategy

**Who decides:** Wes + Ivan

**Blocks:** Year 1 capex deployment, Year 1 revenue ramp

**Recommendation:** Option (b) for Year 1, then (a) in Year 2. Reasoning: validate the operational stack (cleaning, F&B, booking) on the simplest cabins first, then scale premium. Avoids the "premium cabin + broken service" failure mode.

**Status:** OPEN

**Tracked in:** RV catalog `house_typologies/` + `operations/`

---

## Decision 8 — Marketing channel strategy

**What it is:** Where do the first guests come from? Direct Messaging? Booking.com? Airbnb? Tour operators?

**Options:**
- (a) Direct Messaging + website form only (save 15% Booking.com commission, Phase 1 only)
- (b) Booking.com + Airbnb (reach, but commission)
- (c) Tour operators (NL/DE San Bernardino network) (lower volume, higher touch)

**Who decides:** Wes (with Erebus research)

**Blocks:** First guest bookings, Year-1 revenue ramp

**Recommendation:** Phase 1 = (a) + (c) (direct + tour operators). Phase 2 = add (b) when inventory justifies the platform fees. Per Insight #7, the 15% Booking.com commission kills margin for low ADR Phase 1.

**Status:** OPEN

**Tracked in:** RV catalog `M01_booking.com_+_airbnb...md` + `I05_referral_program...md`

---

## Decision 9 — 4-entity BV vs hybrid (Erebus's third option)

**What it is:** Within the business structure decision, is the 4-entity BV worth the complexity, or does the hybrid (Land BV + Op S.A. + NL Holding) achieve the same goals with less admin?

**Options:**
- (a) 4-entity BV (Ivan's draft)
- (b) Hybrid: Land BV + Operational S.A. + NL Holding (Erebus's recommendation)
- (c) Single entity (Wes's draft)

**Who decides:** Wes + Thijs, with accountant

**Blocks:** Phase 1 capex deployment, investor capital raise

**Recommendation:** Option (b) hybrid. See `BUSINESS_STRUCTURE.md` for full analysis.

**Status:** OPEN — depends on Decision 1

---

## Decision 10 — Personal success metric (Wes)

**What it is:** Per Insight #20, Wes hasn't defined his personal success metric. Without it, every idea is "good" but none is "the right one."

**Options:**
- (a) Financial: €X passive income by 2030
- (b) Lifestyle: X weeks/year in PY, X weeks in NL
- (c) Impact: X hectares regenerated, X locals employed
- (d) Family: X kids raised partly on site
- (e) All of the above + weights

**Who decides:** Wes (personal)

**Blocks:** Project re-prioritization. Once known, ~30% of catalog items will get re-prioritized.

**Recommendation:** All of the above + weights. Even rough numbers help.

**Status:** OPEN

---

## Decision 11 — Sonja's 60th deadline: hard or soft?

**What it is:** Is the 2030 Sonja-60th goal a contractual/booked event, or aspirational?

**Options:**
- (a) Hard: build the calendar to it
- (b) Soft: nice-to-have
- (c) Hard but flexible: aim for it, but don't over-build for it

**Who decides:** Wes + Sonja

**Blocks:** Build cadence math, Sonja-weekend brief

**Recommendation:** Option (c). The brief itself is the most useful artefact (forces you to specify the experience).

**Status:** OPEN

**Tracked in:** RV catalog `V02_2030_operational_milestone...md`

---

## Decision 12 — Hire the previous owner's caretaker?

**What it is:** There's a man on the property getting "oppas geld" (sitting money) for watching the land. Wes wants to convert this to a worker contract.

**Options:**
- (a) Hire him (new contract, higher wage, real work)
- (b) Don't hire (he's not the right fit)
- (c) Hire someone else (different person, fresh contract)

**Who decides:** Wes + Thijs

**Blocks:** Operations start, on-site security

**Recommendation:** Option (a) per Wes's brief — "die moeten we de juiste manier met de mensen leren." But follow Sonja's cultural advice on wage calibration.

**Status:** OPEN — needs Sonja conversation

**Tracked in:** RV catalog `O02_hire_previous_owner's_caretaker...md` + `O10_cultural_adaptation...md`

---


## Decision 13 — Anexo I status (NEW from W0.4 chase)

**What it is:** Cl. OCTAVA (ii) of the boleto required sellers to deliver Anexo I (technical descriptions of all 6 fincas: linderos, rumbos, medidas) ~5 May 2026. Status as of 2026-06-30: overdue 2 months.

**Why it matters:** Anexo I is required for legal completeness (L07), for IMAGRO tax calculations, for insurance underwriting, and for accurate property boundary mapping for cabin siting. Without it, 1+ fincas may have unclear boundaries.

**Who decides:** Wes → Escribana Peña (1 phone call)

**Blocks:** L07, accurate Phase 1 cabin siting, insurance, IMAGRO

**Recommendation:** Chase this WEEK. A 2-month overdue Anexo I is a flag that something is wrong. Best case: paperwork delay at Peña's office. Worst case: a seller doesn't have clear title.

**Status:** OPEN. See `[GHOST] docs/research/RESULTS/W04_anexo_I_status.md` (renamed/removed in 2026-07-03 restructure) for full context.

**Tracked in:** WES_TODO W0.4

---

## Decision 14 — "Riverstone Valley" as canonical project name? (NEW from W0.3)

**What it is:** Wes's 2026-06-30 brainstorm surfaced 5 name candidates: Riverstone Valley, Villa del Cielo, Cielo Azul, Lluvia Dorada, Lluvia de Oro. Plus existing names: Riverstone Valley (Ivan's), Eco Jungle Resort Paraguay (Wes's working files). WES_TODO W0.3 asks Wes to pick one.

**Options:**
- (a) Riverstone Valley — Anglo, matches Eskenbach/suburbanization theme
- (b) Villa del Cielo — Spanish, "mooi"
- (c) Cielo Azul / Lluvia Dorada / Lluvia de Oro — other Spanish candidates
- (d) Keep current (Riverstone Valley or Eco Jungle Resort)

**Who decides:** Wes (5 minutes)

**Blocks:** All of D14 (Cross-cutting brand/naming), website, social media handles, marketing copy

**Recommendation:** Pick one, check domain (Erebus does the whois via local command), defensively register .com + .com.py + .io variants

**Status:** OPEN. Domain check procedure in `../../docs/research/RESULTS/BR01_name_pick.md`.

**Tracked in:** WES_TODO W0.3

---

## Decision 15 — Insurance pre-qualification as hard gate? (NEW from insurance_fire_bundle.md)

**What it is:** Insurance broker pre-qualification (3 quotes) is technically in WES_TODO W3.1 (month). But the hard-gate logic (no build until insured) is a separate decision. Three quotes from Marsh Brazil + Aon Argentina + Mapfre PY would take 4-6 weeks to arrive.

**Options:**
- (a) Hard gate: no break-ground until 3 quotes received and coverage confirmed at <10% of project value
- (b) Soft gate: get quotes in parallel with Fase 1 prep; only enforce if coverage available
- (c) Off-grid risk: build cob instead of wood/bamboo to reduce insurance requirement

**Who decides:** Wes + insurance broker (after quotes arrive)

**Blocks:** L07 (escritura legal completeness), Phase 1 break-ground

**Recommendation:** Hard gate. Per Insight #3, building uninsured wooden structures in forested PY is gambling, not investing. €25-80K/year for proper insurance is <0.2% of the €5.5M build cost.

**Status:** OPEN. Awaiting W3.1 insurance broker outreach.

**Tracked in:** WES_TODO W3.1 + insurance_fire_bundle.md

---

## Summary


**12 open decisions, none blocked by Ivan's work — all waiting on Wes** (or in 2 cases, Wes + Sonja or Wes + Thijs).

**Priority for Wes's next 7 days:**
1. **D6 Insurance pre-qualification** (URGENT — hard gate before any structure)
2. **D10 Personal success metric** (cheap, 30 min conversation with self)
3. **D1 + D9 Business structure** (book the accountant call)
4. **D5 Materials pricing collection** (plan the 2-week supplier trip)

**Erebus can support:**
- D1, D9: draft the 1-page summary Wes brings to the accountant
- D5: online research for the 17 categories (60% coverage achievable in 1 week)
- D8: marketing research (channels + comparables)

**Tracked in:** RV catalog `OPEN_DECISIONS.md` (mirror of this file in the catalog directory)
