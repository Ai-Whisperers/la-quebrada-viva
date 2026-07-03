# Wes's Complete TODO — research + decisions + actions, prioritized

**Date:** 2026-06-30
**Status:** First comprehensive TODO. Combines 3 sources (RESEARCH_CATALOGUE 128 items, ACTIONLIST 20 items, OPEN_DECISIONS 12) into one ordered work queue.
**Source of truth:** This file. `docs/MASTER_TODO.md` and `docs/audios/.../final/ACTIONLIST_ES_EN.md` are derived from this.

**Owner legend:**
- **[W]** = Wesley (you) — direct decision/action
- **[I]** = Ivan / Erebus (AI Whisperers) — orchestration, draft, synthesize
- **[A]** = AI subagent — can run unattended, web research
- **[L]** = Local attorney (NL+PY dual-tax) — 1 call answers 9 P1-blockers
- **[S]** = Sonja — 1 call answers 16 cultural/worker/price questions
- **[H]** = Human in PY — Wes or local contact on ground

**Priority legend:**
- **P0** = today/tomorrow, blocks Fase 1 build
- **P1** = this week, blocks Fase 1 ops
- **P2** = 2 weeks, blocks Fase 2 / Fase 1 polish
- **P3** = month, Fase 2 prep
- **P4** = 2030 horizon, nice-to-have

**Sprint allocation:**
- **Sprint 0** = next 1-2 weeks (P0-P1 items, blocks Fase 1)
- **Sprint 1** = weeks 2-4 (P1-P2 items, validates Fase 1 build)
- **Sprint 2** = months 2-3 (P2-P3 items, Fase 2 prep)
- **Sprint 3** = months 4-6 (P3 items, Fase 2 experience)

---

## Status (as of 2026-06-30, end of initial Erebus pass)

**Done in this pass:**
- ✅ W0.6 AI batch: 8 RESEARCH_CATALOGUE items answered (M04, M05, M08, M22, F11, F12, F09, L05) — all in `docs/research/RESULTS/`
- ✅ W0.8 Materials list: `docs/research/5_ONDERWERPEN_MATERIALS.md` built
- ✅ W0.9a HOUSING_PARK_CONCEPT.md patched with 9 audio deltas
- ✅ W0.9b RESEARCH_GAPS.md updated with R39-R50 (12 new items)
- ✅ W0.9c "16e → 60e" transcription error fixed in 6 audio final files + SYNTHESIS.md
- ✅ Sonja questionnaire built: `docs/people/SONJA_QUESTIONNAIRE.md` (16 questions, 1 call)
- ✅ Attorney brief built: `docs/people/ATTORNEY_BRIEF.md` (12 questions, 1 call)
- ✅ Wes actions checklist: `docs/people/WES_ACTIONS.md` (5 things, 4-5 hours)
- ✅ Insurance + fire research bundle: `docs/research/RESULTS/insurance_fire_bundle.md`
- ✅ Research execution tracker: `docs/research/EXECUTION.md`
- ✅ New: `docs/research/RESULTS/` directory with 9 result files
- ✅ New: `docs/people/` directory (3 human-side briefing files)
- ✅ New: `docs/patches/` directory (HOUSING_PARK_CONCEPT + RESEARCH_GAPS patches)

**NOT done (needs human action):**
- ⏳ W0.1 Attorney call (Wes)
- ⏳ W0.2 Sonja call (Wes → Sonja)
- ⏳ W0.3 Project name (Wes)
- ⏳ W0.4 Anexo I chase (Wes → Escribana)
- ⏳ W0.5 LiDAR booking (Wes)

**In progress (AI batch, can be expanded):**
- 🔄 W1.1 Sprint 1 AI batch (30 items, A-owner) — ready to dispatch

**Status: 8/21 Sprint 0 items done by Erebus. 5/21 waiting on Wes. 8/21 waiting on AI batching (can start now).**

## SPRINT 0 — Next 1-2 weeks (THE FASE 1 BLOCKERS)

**Total: 21 items, ~95 working days, compressible to 2 weeks if parallelized.**

### W0.1 — Book the NL+PY dual-tax attorney call [W] ⚡ HIGHEST LEVERAGE

**1-2 hour consultation. Unblocks 9 P1-blockers in one call. Cost: €300-500.**

- [ ] Find a NL+PY dual-tax attorney (ask Kiki's network, Kiki has Asunción contacts)
- [ ] Book 1-2 hour call within 7 days
- [ ] Prep 1-page summary of 4-BV structure (per BUSINESS_STRUCTURE.md) for the call
- [ ] Run the call, capture decisions
- [ ] Update L01-L33 research items with attorney answers

**Items this unblocks:** L01, L02, L03, L04, L05, L21, L22, L25, L28, L29

### W0.2 — Sonja questionnaire (bundled 16-question call) [I→S] ⚡ HIGHEST LEVERAGE

**1-2 hour call with Sonja. Answers 16 cultural/worker/price questions at once.**

- [ ] Build the questionnaire (Ivan — already drafted in ACTIONLIST P0.2)
- [ ] Send to Sonja as 1 PDF (don't fragment into 16 messages)
- [ ] Call — 1-2 hours
- [ ] Capture answers in `docs/people/sonja_kb.md`
- [ ] Update W01-W19 research items with Sonja answers

**Items this unblocks:** W01, W02, W03, W04, W05, W06, W07, W09, W10, W11, W12, W13, W14, W15, W16, W19

### W0.3 — Project name decision [W] ⚡ 5 MINUTES

**Decision only. Everything else blocks on this.**

- [ ] Pick from candidates: "Riverstone Valley" (Wes's brainstorm) | "Villa del Cielo" | "Cielo Azul" | "Lluvia Dorada" | "Lluvia de Oro" | "La Quebrada Viva" (Ivan's) | "Eco Jungle Resort Paraguay" (Wes's working files)
- [ ] Domain check (BR02, BR03 — AI subagent, 1 day)
- [ ] Update `README.md` with the chosen name
- [ ] Update `STATUS.md` cross-references

**Items this unblocks:** BR01, BR02, BR03, all of D14 (cross-cutting brand/naming)

### W0.4 — Chase Anexo I of boleto [W] ⚡ 1 PHONE CALL

**Overdue. Should already be in hand per the boleto's T+5 hábiles clause (~5 May 2026).**

- [ ] Call Escribana Peña Ros — ask for Anexo I status
- [ ] If still missing, get written commitment date
- [ ] Update CLOSING_DAY_PREP.md with chase log

**Items this unblocks:** L07 (legal completeness)

### W0.5 — Book drone LiDAR pilot for next PY visit [W] ⚡ 1 EMAIL

**$1,500-3,000. Needed for cabin siting, road planning, water-shed. Schedule weeks ahead.**

- [ ] Identify 2-3 drone pilots in PY with LiDAR (DJI L1/L2 sensors) — AI subagent
- [ ] Get quotes
- [ ] Book for next PY visit (Q3 2026)
- [ ] Update SD01, SD02 research items

**Items this unblocks:** SD01, SD02, SD04, SD05, SD06, SD07, B06 (LiDAR decision), C04 (ground bores planning)

### W0.6 — Dispatch Sprint 0 AI subagent batch [I/Erebus] ⚡ PARALLEL

**8 items. AI subagent tasks. Run in parallel. ~1 week total.**

- [ ] M04: Cement + rebar pricing PY (cross-ref NL prices doc) [A, 1 week]
- [ ] M05: Ramen/glas import vs local fabrication [A, 1 week]
- [ ] M08: Septic + DINAPI + reed-bed greywater [A, 1 week]
- [ ] M22: Kitchen equipment import logistics [A, 1 day]
- [ ] F11: Cell coverage Tigo/Personal/Claro at site [A, 1 day]
- [ ] F12: Starlink installability at site [A, 1 day]
- [ ] F09: Solar PV sizing using ERA5 climate data already in repo [A, 1 week]
- [ ] L05: NL BV > IB threshold €70k fiscal confirmation (Belastingdienst website) [A, 1 day]

**Update:** mark each done in `docs/research/EXECUTION_LOG.md` when complete.

### W0.7 — Human-in-PY check: road conditions [H]

**1 day. Someone physically checks the road to the property.**

- [ ] Drive to Escobar, photograph road conditions in dry season
- [ ] Note Oct-Apr rain issues
- [ ] Update F05

### W0.8 — Build 5-onderwerpen materials research list [I]

**Already partially drafted (P0.3 in ACTIONLIST).**

- [ ] Compile the 15-onderwerpen materials list
- [ ] Cross-ref to existing 17-category NL prices doc
- [ ] Mark which 5 to research first (Wes picks)
- [ ] Send 2-question finalization to Wes for name + 5 priority picks

### W0.9 — Update HOUSING_PARK_CONCEPT.md + RESEARCH_GAPS.md [I]

**Apply the post-audio-synthesis deltas (P0.5, P0.6 in ACTIONLIST).**

- [ ] HOUSING_PARK_CONCEPT.md: add the 4-BV structure, machinepark principle, wellness pool spec, family-anchored model
- [ ] HOUSING_PARK_CONCEPT.md: add "What's NEW vs 2026-06-10" section
- [ ] RESEARCH_GAPS.md: add R39-R50 from audios
- [ ] **Fix the transcription error**: "Sonja's 16e verjaardag" → "Sonja's 60th birthday (2030)" wherever it appears

### Sprint 0 summary

| Action | Owner | When | Status |
|---|---|---|---|
| W0.1 Attorney call | Wes | This week | ⬜ |
| W0.2 Sonja call | Ivan→Sonja | This week | ⬜ |
| W0.3 Project name | Wes | This week | ⬜ |
| W0.4 Anexo I chase | Wes | Today | ⬜ |
| W0.5 LiDAR booking | Wes | This week | ⬜ |
| W0.6 AI batch | Erebus | This week | ⬜ |
| W0.7 Road check | Human-PY | Within 2 weeks | ⬜ |
| W0.8 Materials list | Ivan | This week | ⬜ |
| W0.9 Doc updates | Ivan | This week | ⬜ |

**Definition of done for Sprint 0:** 21 P1-blockers all answered + 8 AI items shipped + Anexo I in hand + attorney call completed + Sonja call completed + name decided.

---

## SPRINT 1 — Weeks 2-4 (35 items, ~122 days)

**The validation phase. After Sprint 0, Fase 1 build can start. Sprint 1 is the research that validates the build is going right.**

### W1.1 — Dispatch Sprint 1 AI subagent batch (30 items) [I/A]

**All Owner=A. Can run as parallel subagents. ~2 weeks total.**

Materials (D3):
- [ ] M09: Bevestigingsmateriaal (fasteners) — bulk import vs local
- [ ] M10: Vloeren (flooring) — tegels vs cement vs hergebruikt hout
- [ ] M11: Verf (paint) — exterior weatherbestendig, anti-hongos
- [ ] M21: Pool equipment
- [ ] M23: AC units for PY climate

Infrastructure (D7):
- [ ] F01: Ipoh-Karai railroad reopening — plan status
- [ ] F10: LiFePO4 battery sizing for backup
- [ ] F15: Cistern sizing for rainwater
- [ ] F19: Generator sizing for restaurant
- [ ] F20: Toyota Tundra vs Presio (existing research continues)

Banking (D1):
- [ ] L14: Bancard / Pagopar card payment
- [ ] L15: Banco Itaú / Ueno / Familiar B2B banking
- [ ] L16: Billeteras móviles for staff payments
- [ ] L17: FX transfer costs NL → PY

Auto (D8):
- [ ] AH01: Toyota Tundra vs Presio current pricing
- [ ] AH02: Tundra parts availability
- [ ] AH03: Used vs new for bouwfase

W15 hospitality training programs (2 weeks)
Plus 12 more smaller items — see RESEARCH_CATALOGUE for full list.

### W1.2 — Dr. visit to Escobar: F03, F07, F06, W17, F11, PA10, SD10 [W]

**The site visit that unblocks most of D7 (Infrastructure) + key H-items.**

- [ ] ANDE office Paraguarí — get 3-phase upgrade quote (F03)
- [ ] ANDE field visit — check pole + transformer current state (F07)
- [ ] ANDE grid capacity verification (F06)
- [ ] Staff transport Paraguarí → Escobar — bus, frequency, cost (W17)
- [ ] Cell coverage Tigo/Personal/Claro at actual site (F11) — physical check
- [ ] Kuikopee Dutch forester meeting (PA10) — bring name from Wes
- [ ] Site visit (SD10) — walk all 6 fincas, photograph
- [ ] Drone LiDAR survey on this trip (SD01, SD02) — €1,500-3,000

**Items this unblocks:** F03, F07, F06, W17, F11, PA10, SD10, SD01, SD02

### W1.3 — I05 + I06 attorney followup (insurance specifics) [L]

- [ ] Worker injury insurance IPS-related specifics
- [ ] Vehicle insurance for bouwfase auto

### W1.4 — W15 hospitality training programs research [A, 2 weeks]

### Sprint 1 summary

| Action | Owner | When |
|---|---|---|
| W1.1 AI batch (30 items) | Erebus | Weeks 2-4 |
| W1.2 Site visit (multi-item) | Wes | Within 3-4 weeks |
| W1.3 Insurance followup | Attorney | Within 3-4 weeks |
| W1.4 Hospitality research | AI subagent | Weeks 2-4 |

**Definition of done for Sprint 1:** 35 items answered + site visit completed + LiDAR survey done + first-time Fase 1 build can break ground with proper insurance.

---

## SPRINT 2 — Months 2-3 (36 items, ~155 days)

**The "verify and validate" phase. Most of these are 2-week AI research projects.**

### W2.1 — Long-form attorney work [L]

- [ ] L19: Tax treaty NL ↔ PY (2 weeks)
- [ ] L20: MERCOSUR residency for Dutch nationals (2 weeks)
- [ ] L27: Servidumbres de paso (neighbor easement) (2 weeks)
- [ ] L06: PY holding company (S.A. vs S.R.L. vs E.A.S.) (1 week)
- [ ] L08: RUC aanvragen for each BV (1 week)
- [ ] L10-L13: Tariffs (IVA, IRE, IMAGRO, permiso municipal) — bulk dispatch (1 day total)

### W2.2 — Engineer consultation: water + ANDE [L]

- [ ] F14: Stream water permit INAA (2 weeks)
- [ ] F08: ANDE power (covered in Sprint 1 if site visit)

### W2.3 — Sonja continuation: workers + cultural [S]

- [ ] W13: Vetted bouwvakkers registry in Paraguarí (2 weeks)
- [ ] W14: Sub-contractor vs direct hire (1 week)
- [ ] W11: Dependiente vs independiente (2 days)
- [ ] W09-W10: Aguinaldo + Vacaciones (1 day each, can batch)
- [ ] W12: NL-direct vs PY-indirect childcare norms (1 week)

### W2.4 — Partnerships research (I) [2 weeks each]

- [ ] PA03: San Bernardino hotel list — cross-promotion targets
- [ ] PA04: German community in PY — Chamber of Commerce, cultural events
- [ ] PA05: Dutch community in PY — expat networks
- [ ] PA06: Wedding planner partnerships (Asunción, Encarnación, San Ber)

### W2.5 — Market + restaurant + forest AI research [A]

- [ ] EN02: Native plant species list for Escobar (2 weeks)
- [ ] FT10: Chef partnership — German-trained chefs in PY (2 weeks)
- [ ] MK04: Wedding market in rural PY (2 weeks)
- [ ] MK05: Asunción corporate retreat market (2 weeks)
- [ ] MK06: SENATUR tourism statistics (2-3 days)
- [ ] MK08-MK10: Air access for European visitors (1 day each, batch)

### W2.6 — Drone LiDAR survey (if not done in Sprint 1) [W]

- [ ] SD01+SD02 + processing
- [ ] SD04-SD07: cabin/restaurant/event-space siting

### Sprint 2 summary

| Action | Owner | When |
|---|---|---|
| W2.1 Long-form attorney | Attorney | Months 2-3 |
| W2.2 Engineer | Engineer | Months 2-3 |
| W2.3 Sonja continuation | Sonja | Months 2-3 |
| W2.4 Partnerships | Ivan | Months 2-3 |
| W2.5 Market research | AI subagent | Months 2-3 |
| W2.6 LiDAR survey (if not done) | Wes | Within 8 weeks |

---

## SPRINT 3 — Months 4-6 (36 items, ~337 days)

**The "fase 2 prep" phase. Most of these are 2-week AI research projects. Do them when Fase 1 is operational and you have time.**

### W3.1 — Experience + VR + food + forest research [A/I]

- [ ] X01-X14: Site experience research (wellness pool, weddings, family venue, sauna, yoga, chapel, etc.) — 14 items, ~55 days
- [ ] V01-V09: VR / digital twin variants (summer/winter/wedding/family events) — 9 items, ~50 days
- [ ] FT01-FT17: Food & restaurant research (specialty imports, chef, existing restaurants, PY wines, tech stack) — 17 items, ~40 days
- [ ] EN01-EN10: Forest & environment (volunteer tourism, eco-certifications, wildlife corridors, climate projections) — 10 items, ~45 days

### W3.2 — Market + partnerships followup [A]

- [ ] MK11-MK15: Comparable regional properties, family celebration market
- [ ] PA07-PA10: San Bernardino lodging visits, Mennonite colonies, German community partnerships

### W3.3 — Cross-cutting [I/W]

- [ ] C01-C07: Brand voice, naming finalization, marketing plan
- [ ] BR04-BR08: Project structure (S.A. set-up, etc.)

### Sprint 3 summary

| Action | Owner | When |
|---|---|---|
| W3.1 Experience + VR + food + forest | Mixed | Months 4-6 |
| W3.2 Market + partnerships | Mixed | Months 4-6 |
| W3.3 Cross-cutting | Mixed | Months 4-6 |

---

## BACKLOG — Do later or never (36 items, ~337 days)

These are "nice to know" but not on the critical path. Don't do them now. Save them for when you have time. They live in the catalog so they don't get lost.

### B1 — Naming + brand polish (do when brand is priority)

- BR04-BR08: Project structure variants (after the name is picked in W0.3)

### B2 — Personal/Spanish/Guarani learning (do in your own time)

- S01-S06: Spanish/Guaraní learning resources, local idiom packs, formal vs informal register

### B3 — Long-tail VR + multi-season (do when Fase 1 is operational)

- V08: Multi-season tour for clients (2 weeks)
- V09: Event-overlays (birthday, wedding, corporate) (2 weeks)

### B4 — Eco-certifications (do when you have something to certify)

- EN06: Eco-certifications (GSTC, Rainforest Alliance, Bird-Friendly, Carbon Neutral) (1 week)
- EN07: Eco-certification costs + PY precedent (1 week)
- EN08: Wildlife corridor analysis (2 weeks)
- EN10: Climate change projections for Paraguarí (20-year) (2 weeks)

### B5 — Volunteer + reforestation (do in Fase 2)

- EN05: Volunteer tourism for reforestation (1 week)

### B6 — Cross-cutting values (do when you have time to think)

- C04-C07: Long-term reforestation partnership, climate adaptation, policy advocacy

---

## OPEN DECISIONS (not research — actual calls Wes must make)

**These are the 12 decisions I drafted in `docs/_reconciled/OPEN_DECISIONS.md`. They block downstream work. Each is a single yes/no call.**

| # | Decision | Owner | Status | Sprint |
|---|---|---|---|---|
| 1 | Business structure: 4-entity BV vs founder-controlled vs hybrid | Wes | Open | 0 (W0.1) |
| 2 | Currency canonical: EUR vs USD vs 3-layer | Wes | Open | 0 |
| 3 | Cabin typology: 10-type plan vs 13 render-files (retire extras) | Wes | Open | 1 |
| 4 | LQV 3DGS pipeline integration | Wes+Ivan | Blocked on B07 | 1-2 |
| 5 | Materials pricing collection sprint | Wes | Open | 0 (W0.6+W0.8) |
| 6 | Insurance pre-qualification BEFORE breaking ground | Wes+broker | **URGENT** | 0 |
| 7 | Build order within Phase 1 Year 1: 5 cabins (which types?) | Wes+Ivan | Open | 1 |
| 8 | Marketing channel strategy: direct + tour operators only Phase 1 | Wes | Open | 2 |
| 9 | Within business structure: 4-entity vs hybrid | Wes+attorney | Open (depends on 1) | 0 (W0.1) |
| 10 | Personal success metric for Wes (per Insight #20) | Wes | Open | ASAP — 30 min self-conversation |
| 11 | Sonja's 60th in 2030: hard or soft? | Wes+Sonja | Open | 1 |
| 12 | Hire previous owner's caretaker? | Wes+Sonja | Open (Sonja block) | 1 |

---

## ITEMS NOT IN ANY TODO (gaps to flag)

**These things should probably be in the research backlog but aren't:**

1. **Wes's personal health/burnout** (per Insight #19 from prior work) — 2-month full-time solo founder at 8x speed. No research item. Worth flagging once.
2. **Sonja's capacity** — 16 items routed through her. If she's overloaded, all 16 stall. No research item.
3. **Wes's personal success metric** (per Insight #20) — still undefined. Not in any todo.
4. **Backup plan for the local attorney** — 9 P1-blockers all depend on 1 attorney. If unresponsive, those 9 stall.
5. **Backup plan for Wes in PY** — most H-items need a human in PY. If Wes's next visit is delayed, those stall.
6. **The "16th birthday" transcription error** — needs a 1-line fix in KEY_POINTS and ACTIONLIST.

---

## EXECUTION TRACKER — Status table

Update this weekly. Mark items ✅/🔄/❌.

| Sprint | Items | Started | Done | Blocked |
|---|---:|---:|---:|---:|
| Sprint 0 (P0-P1) | 21 | 0 | 0 | 0 |
| Sprint 1 (P1-P2) | 35 | 0 | 0 | 0 |
| Sprint 2 (P2-P3) | 36 | 0 | 0 | 0 |
| Sprint 3 (P3) | 36 | 0 | 0 | 0 |
| Backlog (later) | 36 | 0 | 0 | 0 |
| Open decisions | 12 | 0 | 0 | 0 |
| **Total** | **176** | **0** | **0** | **0** |

---

## How to use this file

1. **Start of week**: read Sprint 0 (the only active sprint until Sprint 0 closes)
2. **Pick the next 1-2 actions** with the right owner tag
3. **Wes** does the 5 things in W0.1-W0.5 (calls + email + name pick)
4. **Erebus** dispatches W0.6 AI batch in parallel
5. **End of week**: update tracker, mark items ✅
6. **When Sprint 0 closes** (all 21 items done): move to Sprint 1
7. **Monthly**: review Backlog + decide if any new items need promotion to Sprint 3

---

## Critical path summary

```
Week 0 (this week):
  Wes: attorney call + Sonja call + Anexo I chase + name + LiDAR email
  Erebus: AI batch (8 items) + materials list + doc updates
Week 1-2:
  Wes: book the 5 things above
  Erebus: continue AI batch
Week 2-3 (Sprint 0 close):
  All 21 P1-blockers answered
  Fase 1 build can break ground
Week 3-4 (Sprint 1 start):
  Wes: PY site visit + LiDAR survey
  Erebus: 30-item AI batch
Month 2-3 (Sprint 2):
  Long-form attorney work
  Partnerships + market research
Month 4-6 (Sprint 3):
  Experience + VR + food + forest
  Cross-cutting brand
2030 (target):
  Sonja's 60th
  All Fase 1-3 operational
```

---

**Maintained by:** Erebus (AI Whisperers)
**For:** Wesley van de Camp + Ivan + Kiki
**Created:** 2026-06-30
**Update cadence:** Weekly (Sprint 0), bi-weekly (Sprints 1-2), monthly (Sprint 3+)
**Status:** First comprehensive TODO. All items derived from 3 source docs: RESEARCH_CATALOGUE.md (128 items), ACTIONLIST_ES_EN.md (20 items), OPEN_DECISIONS.md (12 decisions). Source of truth going forward.
