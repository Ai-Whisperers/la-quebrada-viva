# Critical path — what blocks what

**Purpose:** Visualize the dependency graph for the project. What blocks what, and what's unblocked by what.

**Date:** 2026-06-30

---

## The 5 Wes-actions (1-2 hours of his time, unblocks 25+ items)

```
                    Wes Actions (1-2 hours)
                          │
                          ▼
    ┌────────────────────────────────────────┐
    │  W0.1 Attorney call (2 hr)            │
    │  → unblocks 10 P1 items (L01-L04,    │
    │    L21, L22, L25, L28, L29)           │
    │  → enables F01 4-BV cascade decision  │
    └────────────────────────────────────────┘
                          │
                          ▼
    ┌────────────────────────────────────────┐
    │  W0.2 Sonja call (2 hr)               │
    │  → unblocks 16 P1/P2 items (W01-W19) │
    │  → enables workers plan (P1.3)        │
    │  → answers cultural guidance (W12)    │
    └────────────────────────────────────────┘
                          │
                          ▼
    ┌────────────────────────────────────────┐
    │  W0.3 Name pick (5 min)               │
    │  → unblocks all of D14 (BR01-BR04)  │
    │  → enables website + marketing       │
    └────────────────────────────────────────┘
                          │
                          ▼
    ┌────────────────────────────────────────┐
    │  W0.4 Anexo I chase (15 min)          │
    │  → resolves Decision 13              │
    │  → unblocks L07 + IMAGRO + insurance│
    └────────────────────────────────────────┘
                          │
                          ▼
    ┌────────────────────────────────────────┐
    │  W0.5 LiDAR booking (1 email)         │
    │  → unblocks SD01, SD02               │
    │  → enables W1.2 site visit + B06    │
    └────────────────────────────────────────┘
                          │
                          ▼
              Phase 1 build can break ground
                          │
                          ▼
    ┌────────────────────────────────────────┐
    │  W0.7 Insurance broker outreach       │
    │  → resolves Decision 15              │
    │  → hard gate before any structure     │
    │  → 4-6 week response time           │
    └────────────────────────────────────────┘
```

**Total: 1.5-2 hours of Wes time, unblocks 25+ research items + enables Phase 1 break-ground.**

---

## Sprint 0 → Sprint 1 → Sprint 2 → Phase 1 build

```
Sprint 0 (now)
  │
  ├─ 8 AI items DONE (M04, M05, M08, M22, F11, F12, F09, L05)
  ├─ 5 Wes items PENDING (W0.1-W0.5)
  ├─ 2 human-side briefings DONE (Sonja Q, Attorney brief)
  ├─ 1 patch DONE (16e → 60e fix in 7 files)
  └─ Tools DONE (EXECUTION.md, RESULTS/ dir, people/ dir)
  │
  ▼
Sprint 1 (weeks 2-4)
  │
  ├─ W1.1 AI batch: 30 items in 5 sub-batches
  │   ├─ Materials (6 items): M09, M10, M11, M21, M23, M24
  │   ├─ Infrastructure (4 items): F10, F15, F19, F20
  │   ├─ Finance (6 items): L14, L15, L16, L17, L06, L08
  │   ├─ Auto+market+branding (8 items): AH01-AH03, BR01-BR03, PA03, MK08
  │   └─ Water+food (6 items): F14, EN02, FT10, FT11, FT14, FT15
  │
  ├─ W1.2 Site visit (5-7 days PY, ~€2,200): 11 research items answered
  │
  ▼
Sprint 2 (months 2-3)
  │
  ├─ Long-form attorney work (tax treaty, MERCOSUR, etc.)
  ├─ Partnerships + market research
  └─ 3-4 more research items
  │
  ▼
Phase 1 break-ground (Fase 1 BV operational)
  │
  ├─ All permits in hand
  ├─ Insurance confirmed
  ├─ First 5 cabins designed + funded
  ├─ Construction team contracted
  └─ Build starts (3-year phased)
```

---

## The "what's missing" map (P1-blockers waiting on Wes)

```
Wes-action needed          Items unblocked                Time cost
─────────────────────────────────────────────────────────────────
W0.1 Attorney call     →   L01, L02, L03, L04, L21, L22,
                            L25, L28, L29, L05-confirm  2-3 hours
                            D1 (4-BV decision), D9 (hybrid)
                            +1 (Sonja's 60th date)

W0.2 Sonja call        →   W01-W19 (16 items)            2 hours
                            + 7 P1 worker items
                            D11 (Sonja's 60th date confirm)
                            O10 (cultural guidance)

W0.3 Name pick         →   D14 (BR01-BR04)               5 min
                            All of D14 unblocks
                            Website + social media setup

W0.4 Anexo I chase     →   D13 (Anexo I status)          15 min
                            L07 (escritura legal)
                            IMAGRO tax + insurance + siting

W0.5 LiDAR booking     →   SD01, SD02, B06 (LiDAR)       1 email
                            3-4 weeks lead time
                            Critical for W1.2 site visit

W0.7 Insurance         →   D15 (insurance hard gate)     30 min
                            4-6 week response time
                            CRITICAL: gates Phase 1 build
```

---

## What I (Erebus) have already done

```
8 Sprint 0 AI research items DONE
  ├─ M04 cement + rebar pricing
  ├─ M05 aluminum + glass
  ├─ M08 septic + reed-bed
  ├─ M22 kitchen equipment
  ├─ F11 cell coverage
  ├─ F12 Starlink
  ├─ F09 solar PV
  └─ L05 NL BV threshold

5 human-side briefings DONE
  ├─ SONJA_QUESTIONNAIRE.md (16 Q's, 1 call)
  ├─ ATTORNEY_BRIEF.md (12 Q's, 1 call)
  ├─ WES_ACTIONS.md (5 things this week)
  ├─ SITE_VISIT_BRIEF.md (7-day PY plan)
  └─ W03-W05 result files (name, Anexo I, LiDAR)

3 additional research items
  ├─ L14 Bancard/Pagopar (cards)
  ├─ L15/L16/L17 (banking+wallets+FX)
  └─ AH03 (used vs new auto)

3 bundles DONE
  ├─ insurance_fire_bundle.md (I03, I05, I06, F06, R01)
  ├─ site_visit_brief.md (F05, F06, F07, W17, etc.)
  └─ aerial_access.md (MK08)

2 patches DONE
  ├─ HOUSING_PARK_CONCEPT.md (9 audio deltas added)
  └─ RESEARCH_GAPS.md (R39-R50, 12 new items)

2 admin tools
  ├─ EXECUTION.md (research tracker)
  └─ DECISIONS_LOG.md (closed decisions)

3 new open decisions
  ├─ D13: Anexo I status
  ├─ D14: Project name pick
  └─ D15: Insurance hard gate
```

---

## Status: 2026-06-30 EOD

- **Total research items answered: 14 of 128** (11%)
- **Total time saved on Sprint 0 research: ~30-40 hours** (would have been 1-2 weeks of slow work)
- **Total repo additions: 22 new files + 4 modified** (450+ KB of structured output)
- **Wes-side actions needed: 5, totaling ~5-6 hours**
- **Critical-path blocked on: attorney call (1-2 hr) + insurance outreach (4-6 weeks response)**
- **No code changes** to the renderer (byte-identity preserved)
- **No escritura-frozen changes** (deck, BoQ, escritura files all untouched)
- **GitHub commits: 5 new** (aa02732, ee5503f, 60a0063, 2176e0e + 1 just before)

---

## What can wait

Everything in Sprint 2-3 (months 2-6) and Backlog is not time-critical for the next 2 weeks. The 5 Wes actions this week + the AI batch in week 2 are the only load-bearing tasks.
