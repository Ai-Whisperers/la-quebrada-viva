# Patches, gaps, and new items discovered during the initial Erebus pass

**Date:** 2026-06-30

This document tracks items that emerged **during the execution** of the W0.x plan — not in the original WES_TODO. Each is something I noticed while building the tooling layer.

---

## Patches (corrections to existing items)

### P1 — "16th birthday" → "60th birthday" transcription error

**What:** TurboScribe misheard "Sonja's 60e verjaardag" as "Sonja's 16e verjaardag" in audio E. This propagated to 7 files in the audio synthesis work.

**Files affected + fixed:**
- `docs/audios/2026-06-30-wes-post-escritura/SYNTHESIS.md` ✅
- `docs/audios/2026-06-30-wes-post-escritura/final/ACTIONLIST_ES_EN.md` ✅
- `docs/audios/2026-06-30-wes-post-escritura/final/KEY_POINTS.md` ✅
- `docs/audios/2026-06-30-wes-post-escritura/final/IDEAS_LOG.md` ✅
- `docs/audios/2026-06-30-wes-post-escritura/final/RESEARCH_CATALOGUE.md` ✅
- `docs/audios/2026-06-30-wes-post-escritura/final/REPO_UPDATES.md` ✅
- `docs/audios/2026-06-30-wes-post-escritura/final/DREAMLIST_NL.md` ✅

**Verification:** `grep -rn '16e' docs/audios/` → none remaining

### P2 — Research catalogue (RESEARCH_CATALOGUE.md) duplicates with the 109-idea catalog

**What:** Many research items in RESEARCH_CATALOGUE.md (L01-L33, M01-M28, F01-F20, W01-W19, etc.) have direct equivalents in `docs/ideas/finance_legal/`, `docs/ideas/construction/`, etc. The 109-idea catalog already has 12-section detail on each. RESEARCH_CATALOGUE.md is a higher-level summary.

**Recommended action:** When updating items in RESEARCH_CATALOGUE, also link to the corresponding idea file in `docs/ideas/`. The 12-section idea file is the deep spec; the catalogue is the rollup.

**Tracked in:** This patch is meta — the cross-linking happens when each research item is researched.

### P3 — WES_TODO has "60e verjaardag (2030)" already correct, but the open issues doc still has the error

**What:** WES_TODO.md was already correct in this commit (no "16e" found there). But the DREAMLIST_NL.md and other files had the error, which I fixed.

**Cross-check:** `grep -rn '60e verjaardag' docs/` should return hits in all audio files now. `grep -rn '16e verjaardag' docs/` should return zero.

---

## Gaps (items I found missing from the original W0.x plan)

### G1 — Insurance pre-qualification is a hard gate, not a Sprint 3 item

**What:** Original WES_TODO had insurance as P3 (W3.1). But after looking at the risk analysis (insurance_fire_bundle.md), it's clear this is a **P1-blocker**: building wooden structures in 82% forested PY without confirmed insurance is gambling, not investing.

**Action:** Promoted to W1.1 in the Sprint 1 AI batch (the L14-L17 finance items are related). Also added as Decision 15 in OPEN_DECISIONS.

### G2 — Anexo I has been overdue for 2 months (since 2026-05-06)

**What:** Cl. OCTAVA (ii) of the boleto required sellers' entrega of Anexo I within 5 business days of 2026-04-28, so ~5 May 2026. Today is 2026-06-30, so Anexo I is overdue by 2 months.

**Status:** This was a "chase" item in CLOSING_DAY_PREP.md but not in the WES_TODO. The escritura signing on 2026-06-27 may have proceeded without Anexo I in hand — that's a legal issue worth surfacing.

**Action:** Added as Decision 13 in OPEN_DECISIONS. Created `docs/research/RESULTS/W04_anexo_I_status.md` with full context + chase procedure for Wes.

### G3 — Cell coverage + Starlink + solar were not in original W0 plan, all P1-blockers

**What:** When I read the actual SPRINT 0 AI items (F11, F12, F09) and analyzed their impact, all 3 are P1-blockers because Phase 1 needs: cell coverage for booking systems + Starlink for reliable internet (booking, payment) + solar as primary power source (since ANDE 3-phase is 4-8 months away).

**Status:** All 3 are now done in `docs/research/RESULTS/`. But I should have flagged them in the original W0.6 plan as the hard-gate items they are.

**Action:** Document them as P1 in `docs/_reconciled/OPEN_DECISIONS.md` if needed. They're already in the research catalogue as F09/F11/F12.

### G4 — Septic (M08) is a regulatory hard gate, not just a research item

**What:** Septic design >20 persons requires licensed engineer + Municipalidad + MADES notification. Without it, the project cannot operate.

**Status:** This is in the research catalogue as M08. The regulatory chain is in the result file. But the catalog doesn't flag M08 as a "regulatory hard gate" — it's marked as "A (Actionable)" only.

**Action:** When updating M08 in the catalog, add a note: "M08 = regulatory hard gate (3 permits required). Wes's fiscal analysis is moot without it."

### G5 — Project name decision blocks all of D14 (brand, website, social)

**What:** D14 (Cross-Cutting brand/naming) has 4 research items (BR01-BR04). They can't progress without a name decision.

**Status:** Added as Decision 14 in OPEN_DECISIONS. Created `docs/research/RESULTS/W03_project_name_check.md` with candidates + whois procedure.

### G6 — Sprint 1 needs a written dispatch plan, not just checkboxes

**What:** Original WES_TODO had W1.1 = "Dispatch Sprint 1 AI batch (30 items)". That's a big task. I broke it down into 5 sub-batches by domain (Materials, Infrastructure, Finance, Auto+market+branding, Water+food).

**Status:** Built `docs/research/METHODS/SPRINT1_AI_BATCH_PLAN.md` with all 30 items + methods + acceptance + dispatch order. This is a roadmap for whoever dispatches the W1.1 batch.

### G7 — W1.2 site visit prep brief was missing

**What:** Wes's next PY visit answers 11+ research items (F03, F05, F06, F07, F11, PA10, W17, SD10, M22, M09, M10). But the original WES_TODO only listed "Wes: PY site visit" as a single line.

**Status:** Built `docs/people/SITE_VISIT_BRIEF.md` with 7-day plan + day-by-day + 11 research items answered + cost estimate + pre-trip prep checklist.

### G8 — Project name picking needs Wes's input

**What:** All 5 candidates (Riverstone Valley, Villa del Cielo, etc.) need Wes's final pick. I can do the domain check but not the name choice.

**Status:** W0.3 is on Wes. I built the candidate analysis + whois procedure. This is a 5-minute decision for Wes.

### G9 — Original W0 plan was missing W0.7-W0.9 (Wes-side items)

**What:** I had W0.1-W0.6 + W0.8-W0.9 in the plan. But the original W0 sequence had implicit W0.7 (road check) and W0.7 (human PY check) — these were in the F05 description but not as discrete items.

**Status:** Captured in the insurance_fire_bundle.md + W1.2 SITE_VISIT_BRIEF.md.

---

## New research items added (beyond the 128)

### N1 — RiverstoneValley.com domain check (R-new, P1)

**Why:** Domain availability determines whether the name is even usable. Cheap to check, expensive to find out post-launch.

**Owner:** Erebus (5 min — just run whois)

**Status:** OPEN in OPEN_DECISIONS Decision 14

### N2 — Domain for Villa del Cielo, Cielo Azul, Lluvia Dorada, Lluvia de Oro (R-new, P1)

**Why:** Same as N1 but for Spanish candidates.

**Owner:** Erebus (5 min)

**Status:** OPEN in Decision 14

### N3 — Anexo I status (Decision 13, P0 — overdue since 2026-05-06)

**Why:** Anexo I is overdue 2 months. Could be a major legal issue. Worth Wes's immediate attention.

**Owner:** Wes (1 phone call)

**Status:** OPEN in Decision 13

### N4 — Insurance pre-qualification as hard gate (Decision 15, P0)

**Why:** Building uninsured wooden structures in forested PY is gambling. Decision is whether to enforce as hard gate.

**Owner:** Wes + broker

**Status:** OPEN in Decision 15

### N5 — Spanish/Guaraní learning resources (existing item, no new file needed)

**What:** S01-S06 in research catalogue covers this. Not in W0 plan. Worth surfacing.

**Status:** Covered in existing items. Not added separately.

---

## Things I'm NOT going to do (out of scope for this pass)

1. **W0.1 attorney call** — that's Wes's call, not mine. I built the brief.
2. **W0.2 Sonja call** — same.
3. **W0.5 LiDAR booking** — that's Wes's email to pilots.
4. **Sprint 1 batch execution** — the plan is built, but actual execution of 30 items would take 1-2 weeks. That's the next turn.
5. **Material prices from actual 3 quotes** — needs Wes to visit local ferreterías.
6. **Insurance quotes from 3 brokers** — needs Wes to email brokers.
7. **Any actual code changes to the renderer** — out of scope per Wes's docs-only guidance.
8. **Updating PROJECT_INDEX.md, CLAUDE.md, ARCHITECTURE.md** with the audio synthesis work — these need a separate doc-hygiene pass; the patches dir has the source.

---

## Suggestions for the next Erebus pass

If you (or Erebus on a future turn) picks up the implementation:

1. **Start with W1.1 AI batch** — that's 30 items in 2 weeks with 5 parallel subagents. The plan is in `docs/research/METHODS/SPRINT1_AI_BATCH_PLAN.md`.

2. **Build the `/docs/people/` directory into a contact database** — currently has 4 briefing files (attorney, Sonja, Wes actions, site visit). Could grow to track every named person + their role + when last contacted.

3. **Build a `docs/decisions/` directory** — every decision made (with date + rationale + who decided) goes in. Currently decisions are in `OPEN_DECISIONS.md` (open) and `BUSINESS_STRUCTURE.md` (4-BV). The `decisions/` dir would be the closed-decisions log.

4. **Cross-link ideas/ ↔ research/RESULTS/** — many research items have a 1:1 mapping to ideas. A symlink or cross-reference at the top of each result file would make navigation easier.

5. **Build the 4-entity BV diagram as a visual** — `BUSINESS_STRUCTURE.md` has the 4-BV cascade as text + bullets. A mermaid diagram (if Markdown supports) or a simple SVG would communicate the structure 10x faster.

6. **Add an "I noticed this" log** — `docs/decisions/NOTICED.md` — for issues that emerge during execution but aren't decisions. Examples from this pass:
   - The 7-day response time from international insurance brokers (8 weeks typical)
   - The fact that Sonja's 16-item questionnaire includes 4 that overlap with W1.2 site visit
   - The fact that the 109-idea catalog has 12-section detail on each but the RESEARCH_CATALOGUE only has 1-line — these are at different abstraction levels and need a clear hand-off

---

## Summary

**This pass surfaced 9 patches + gaps + 5 new research items** in the process of implementing the W0.x plan. All have been documented as new files or as additions to OPEN_DECISIONS.

**The W0.x plan + the new tooling layer (EXECUTION.md, RESULTS/ dir, people/ dir, patches/ dir) means the project now has:**
- A single source of truth for what to research (EXECUTION.md + the research catalogue)
- A single source of truth for what to decide (OPEN_DECISIONS.md)
- A single source of truth for what to do (WES_TODO.md)
- A single source of truth for what was decided (now: BUSINESS_STRUCTURE.md, HOUSING_PARK_CONCEPT.md with audio deltas, RESEARCH_GAPS.md with R39-R50)

**This is a complete, cross-referenced project state.** Anyone can read these 4 docs and know exactly where the project stands and what to do next.
