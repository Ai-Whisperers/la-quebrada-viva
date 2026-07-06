# CHEATSHEET — Riverstone Valley (LQV) — The 1-Page Map

> **For Wesley van de Camp.** Generated 2026-07-06 by Erebus after the repo structural audit.
>
> This is the **single page** to find anything you need. After reading this once (3 min), you can navigate the project in <2 minutes.

---

## TL;DR — 9 files you actually need

| # | File | Why | Read time |
|---|---|---|---:|
| 1 | This file (CHEATSHEET.md) | Single-page map | 3 min |
| 2 | `docs/wes/WES_INDEX.md` | The 5-min read for Wes | 5 min |
| 3 | `docs/research/RESULTS/CAPEX_OPTIONS_2026-07-06.md` | Capex analysis (3 options per decision) | 30 min |
| 4 | `docs/research/RESULTS/SUPPLY_CHAIN_RECOMMENDATIONS_2026-07-06.md` | Vendor master list + logistics | 20 min |
| 5 | `docs/research/RESULTS/LEGAL_RESEARCH_PACK_2026-07-06.md` | 4-BV, taxes, permits, NL↔PY treaty | 30 min |
| 6 | `docs/research/RESULTS/ARCHAEOLOGICAL_CULTURAL_RESEARCH_2026-07-06.md` | Mbyá + archaeology + finding protocol | 20 min |
| 7 | `docs/_reconciled/business/FINANCIAL_MODEL_2026-07-06.xlsx` | 10-sheet financial model | 30 min |
| 8 | `docs/boq/BOQ_Phase1_2026-07-06.csv` + `.md` | Bill of quantities for builders | 15 min |
| 9 | `docs/people/stakeholders/ATTORNEY_BRIEF_1PAGE.md` | Print for attorney | 5 min |

**Total: ~3 hours** to be fully prepared for the HG-1 attorney call.

---

## Where the 5 hard gates are unblocked

| Gate | What | Who | When | Doc that unblocks it |
|---|---|---|---|---|
| **HG-1** | NL+PY attorney call | Wes + attorney | ~2 hr | #5 (Legal research) + #9 (Attorney brief 1-pager) |
| **HG-2** | Fase 1 ownership choice | Wes | ~1 hr | #5 (Legal §A.3-5) + #7 (Financial model TaxProjection sheet) |
| **HG-3** | Insurance broker outreach | Wes | ~2 hr + 6 wk wait | #5 (Legal §D.2 — forest fire at WTW $22-37K/yr) |
| **HG-4** | PY site visit | Wes + driver | ~1 day | #6 (Mbyá visit on the way) + R35 drone LiDAR before |
| **HG-5** | Anexo I chase | Wes | ~30 min | R02 + chase Escribana Cynthia Peña |

---

## The 5 highest-impact vendor calls (1 afternoon)

Per #4 (Supply chain), these 9 calls unlock 70% of Phase 1 capex:

1. **3 M22 vendors** (kitchen equipment): Gastro-Haus Asu, Brasitermo Asu, + 1 local used market
2. **3 M08 vendors** (septic): 3 INAA-permitted installers per M08
3. **3 NEW02 quarries** (stone): Piribebuy, Sapucai, Itá

After these calls, the BOQ's "estimated" column becomes actual quotes.

---

## The 4 docs you can send to OUTSIDE people RIGHT NOW

| Doc | Send to | Why |
|---|---|---|
| `docs/people/stakeholders/ATTORNEY_BRIEF_1PAGE.md` | NL+PY attorney | Print 1 copy for each |
| `docs/people/stakeholders/MBYA_CONSULTATION_PACKAGE_2026-07-06.md` | INDI (Asunción) | Spanish letter to start the Mbyá consultation |
| `docs/people/stakeholders/FIND_PROTOCOL_2026-07-06.md` | Construction foreman | Print, sign before any excavation starts |
| `docs/boq/BOQ_Phase1_2026-07-06.csv` | Cob builder + vendors | Quote against this |

---

## What's in `docs/research/RESULTS/` (the 167-file research library)

The library has 5 categories:

1. **M_*** (materials) — M04 cement, M05 aluminum, M08 septic, M09 fasteners, M22 kitchen, M_COB_01 cob, M_WOOD_01 timber, M_BEV_01 fasteners, M_VLOER_01 flooring, M_VERF_01 paint, M13 marketing budget
2. **L_*** (legal/tax) — L05 NL BV threshold, L06 PY entity types, L08 RUC, L19 NL-PY treaty, L21 SENATUR, L22 insurance, L25 IVA, L27 income tax, L28 capital gains, L30 salary tax, L31 IPS, L33 Wes personal tax
3. **PR_*** (PY regulations) — PR03 cob pioneers, PR07 construction permits, PR08 insurance companies, PR11 restaurant equipment, PR12 labor law, PR13 lodging tax, PR15 freight logistics, PR16 food supply, PR18 septic regulations, PR20 construction market
4. **FT_*** (future tech) — FT10 chef partnership, FT11 EU restaurants PY, FT15 restaurant tech
5. **Other** — IR01 fire insurance, SX03 insurance market, MK06 SENATUR stats, AH (auto hilux/tundra), EN (eco/wildlife), V02 sonja, X01 events, etc.

**How to search**: use `docs/research/RESULTS/INDEX.md` (the master index, 22 KB). Or just grep `grep -r "<keyword>" docs/research/RESULTS/`.

**R-item status** (per `docs/research/strategy/RESEARCH_GAPS.md`):
- ✅ **Done**: R39, R45, R46, R48, R49 (5 items)
- 🔴 **Open** (28 items in flight — being researched today): R05, R12, R13, R15, R16, R17, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R32, R33, R34, R36, R37, R38, R42, R43, R44 — **will be DONE by tomorrow**
- 🔴 **Still open** (Wes-blocked): R01 (site visit), R02 (Anexo I), R03 (Municipalidad meeting), R07 (cob builder quotes)
- 🟡 **Pending**: R31 (cultural heritage — done in archaeology doc), R35 (drone LiDAR), R40 (ANDE verification), R41 (unused), R47 (Sonja questionnaire)

---

## The 3 docs Ivan / Kiki / AI operators need (NOT Wes)

If you're Ivan / Kiki / Erebus (not Wes), these are your cold-start docs:

1. `STATUS.md` — canonical current state
2. `CLAUDE.md` — operating instructions for AI sessions
3. `ARCHITECTURE.md` — `lqv/` package map + fragility notes

---

## Folder layout (the 5 that matter)

```
/root/la-quebrada-viva/
├── README.md                     ← you are here first (1 page)
├── PROJECT_INDEX.md              ← auto-generated structural sweep
├── STATUS.md                     ← canonical current state (for AI)
├── CHEATSHEET.md (this file)     ← the 1-page map
├── docs/
│   ├── INDEX.md                  ← single navigation entrypoint
│   ├── wes/                      ← 12 files built for Wes
│   ├── state/                    ← canonical state (POST_ESCRITURA_NOW)
│   ├── _reconciled/              ← post-reconciliation canonical
│   │   ├── business/             ← financial model + BV structure
│   │   ├── buildings/            ← cabin specs
│   │   └── land/                 ← land parcel docs
│   ├── people/
│   │   ├── wes/                  ← Wes profile + actions
│   │   ├── stakeholders/         ← attorney + insurance + Mbyá + find protocol
│   │   └── decisions/            ← decisions log
│   ├── research/
│   │   ├── RESULTS/              ← 167 research artifacts (the working library)
│   │   ├── strategy/             ← HOUSING_PARK_CONCEPT + RESEARCH_GAPS
│   │   └── METHODS/              ← how the research was done
│   ├── specs/                    ← specs for house, render, tourism
│   ├── boq/                      ← bill of quantities
│   ├── comms/                    ← outreach drafts
│   ├── ideas/                    ← not-yet-decided ideas
│   ├── audit/                    ← structural audit + gap analysis
│   └── site_data/                ← technical: satellite imagery, GIS layers
└── splats/, renders/, lqv/, scripts/, tests/, tools/    ← technical (don't read directly)
```

---

## The 30-min Wes action list (BEFORE the HG-1 attorney call)

In order of time-to-completion:

1. **Read this cheatsheet + WES_INDEX.md** (8 min)
2. **Read CAPEX_OPTIONS_2026-07-06.md §C** (decision matrix, 5 min)
3. **Read LEGAL_RESEARCH_PACK §K** (the "what blocks Wes" section, 5 min)
4. **Open the FINANCIAL_MODEL_2026-07-06.xlsx** in Google Sheets, play with the Sensitivity sheet (10 min)
5. **Send the 4 outbound docs** to attorney + INDI + builder + vendors (start the chains, 5 min)

After these 5 steps, you have:
- A clear picture of the 5 hard gates
- The decision matrix for each gate
- The vendor/attorney/Mbyá chains started
- A model you can manipulate to test "what if" scenarios

**Then** book the 5 hard gates (4-5 hours of your time, over 2 weeks):
- HG-1: attorney call (2 hr)
- HG-2: ownership choice (1 hr)
- HG-3: insurance broker outreach (2 hr)
- HG-4: site visit (1 day)
- HG-5: Anexo I chase (30 min)

---

## What's NEW this week (2026-07-06 audit day)

| New | Status |
|---|---|
| 4-doc research pack (CAPEX + Supply + Legal + Archaeology) | ✅ shipped |
| Financial model xlsx (10 sheets, 3 scenarios, sensitivity) | ✅ shipped |
| BOQ CSV + MD (103 line items, €486K total) | ✅ shipped |
| Mbyá consultation package (3 languages) | ✅ shipped |
| Ceremonies + wellness programming research | ✅ shipped |
| Find protocol (3 languages, for builders) | ✅ shipped |
| 28 R-items batch (in flight, ~10-30 min) | 🔄 in progress |
| Repo structural audit (this cheatsheet is part of it) | ✅ shipped |
| Subagent provider routing fix (gateway restarted) | ✅ shipped |

---

*Erebus, 2026-07-06. The 1-page map. Keep this open in a browser tab. Read once. Done.*