# 109-idea catalog — patch + cross-link (Erebus follow-up)

**Purpose:** Many of the 109 idea files in `docs/ideas/` are template-fill. The audio synthesis work surfaced deltas that should be reflected. This file tracks the patch work needed.

**Date:** 2026-06-30
**Status:** Diagnostic. The actual patching is a separate (larger) effort.

## What's known (from the audio synthesis work)

The 5 audios from 2026-06-30 surfaced 95 ideas (numbered + bucketed) + 5 new domains + 12 R39-R50 items + multiple corrections. These are the deltas that should be reflected in the existing 109-idea catalog.

## Deltas identified

### New items to add (or already added to RESEARCH_GAPS)

- R39: Hovenier deep-research (Wes's first AI delegation)
- R40: Ipoh-Karai railroad
- R41: Toyota Tundra vs Presio
- R42: LiDAR pilots
- R43: Restaurant equipment suppliers
- R44: Car insurance
- R45: Starlink PY
- R46: Stone quarries
- R47: Sonja wages (covered by W01_W08 file)
- R48: Cement time-series (covered by M04 file)
- R49: Local stone
- R50: AI price negotiation

**Status:** R39-R50 are in RESEARCH_GAPS.md, not in `docs/ideas/`. Should be cross-linked.

### New domain (per DREAMLIST_NL §D1-D15)

The DREAMLIST has 15 domains (D1-D15). The current 109-idea catalog has 10 categories:
- vision (V)
- buyer_experience (B)
- amenities (A)
- construction (C)
- house_typologies (T)
- operations (O)
- finance_legal (F)
- site_specifics (S)
- marketing (M)
- risk_mitigation (R)

**Missing from the 10 categories:**
- D4 insurance (covered partially by F-series)
- D5 site experience (covered partially by A-series)
- D6 VR (covered by B-series)
- D7 infrastructure (covered by F-series)
- D8 auto (not present, need to add AH items)
- D9 market (covered by M-series)
- D10 food/restaurant (covered partially by A-series)
- D11 forest (not present)
- D12 site data (not present)
- D13 partnerships (not present)
- D14 cross-cutting (partially covered)

**Verdict:** The 10 categories cover most of it. AH-series (auto) and some M/FT/R items are missing from the 109-idea catalog but exist in the RESEARCH_CATALOGUE. Cross-link is needed.

## What's in the 109-idea catalog that needs updating

### 12-section pattern (per Wes's 2026-06-30 work)

All 109 files were rewritten to a 12-section template. The pattern is good but many sections are template-fill:
- "What Wes wants" — has quotes where available, generic otherwise
- "Risks & failure modes" — generic "no specific risks" for ~30% of items
- "Done = shipped" — generic "should be measurable artefact" for ~20%

**Quality marker suggestion:** add a `Quality: ✓ reviewed / ○ auto-generated / ✗ flagged` field to each file.

### Cross-link with RESEARCH_CATALOGUE

Every item in `docs/ideas/` should link to its corresponding item in `docs/research/RESULTS/` (if answered) or `docs/audios/2026-06-30-wes-post-escritura/final/RESEARCH_CATALOGUE.md` (if not yet answered).

This makes the 109-idea catalog a "view" of the larger research state, not a parallel universe.

## What's deferred (per OUT_DECISIONS, open decisions, etc.)

| Decision | Effect on idea catalog |
|---|---|
| D1 4-BV structure | Affects F-series ideas (depends on entity type) |
| D2 Currency canonical | Affects M-series, financial figures |
| D3 10-type plan vs 13 render-files | Affects T-series (3 vs 13) |
| D4 name pick | Affects all marketing-facing files |
| D5 marketing channels | Affects M-series |
| D6 4-BV vs hybrid | Affects F-series |
| D7 5e holding | Affects F-series |
| D8 build order | Affects T-series, C-series, O-series |
| D9 4-entity vs hybrid | Affects F-series |
| D10 personal success metric | Affects prioritization of all 109 items |
| D11 Sonja's 60th hard or soft | Affects timeline |
| D12 hire caretaker | Affects O-series |
| D13 Anexo I | Affects S-series (property boundaries) |
| D14 name | Affects M-series |
| D15 insurance gate | Affects C-series, R-series |

**Each open decision affects 5-20 idea files.** Updating the catalog should wait for these decisions to resolve.

## What's recommended for the next pass

1. **Add a 13th category for AH (Auto)** — the auto/Tundra items need a home
2. **Cross-link each 109-idea file** to the corresponding research-catalogue item
3. **Quality-tag each 109-idea file** with a `Quality: ✓/○/✗` field
4. **Update V01 (Vision)** with the audio deltas (4-BV structure, machinepark, wellness pool spec, family model)
5. **Update V02 (2030)** with the corrected 60th birthday milestone

**Time estimate:** 4-6 hours of Erebus work. Not done in this pass because:
- W0.1 attorney call (this week) may change the 4-BV structure
- W0.3 name pick (this week) may change brand references
- These are higher-priority than catalog updates

**Recommendation:** defer the 109-idea catalog patch to a future pass, AFTER Wes's 5 actions this week resolve. Then the patch is informed by the latest decisions.

## Status

⚠️ Identified but not executed. Defer until W0.1-W0.7 actions are complete.
