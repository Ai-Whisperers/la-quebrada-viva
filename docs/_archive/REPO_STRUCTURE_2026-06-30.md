# Repo structure (post-implementation pass)

**Date:** 2026-06-30
**Status:** The repo is now organized for navigation. Use this as the entry point.

## Top-level structure

```
/root/la-quebrada-viva/
├── README.md                                  (4 KB, identity + deliverables)
├── CLAUDE.md                                  (19 KB, AI session instructions)
├── STATUS.md                                  (32 KB, canonical state - escritura-week freeze)
├── PROJECT_INDEX.md                          (27 KB, file map)
├── ARCHITECTURE.md                          (9 KB, lqv/ package map)
├── PROVENANCE.md                             (11 KB, asset license + SHA manifest)
├── CREDITS.md                                (8 KB, per-asset attribution)
├── LICENSE                                    (1.7 KB, MIT for code)
├── LICENSE_BUNDLE.md                         (9.6 KB, asset license summary)
├── Makefile                                   (3 KB, build orchestration)
│
├── lqv/                                       (148 Python files, 22K LOC, 14 subpackages)
│   ├── site/          (terrain, escarpment, terraces, stream, 62-ha digital twin)
│   ├── house/         (cob/bottle, structural, yard)
│   ├── typologies/    (15 cabin types, 19 files)
│   ├── amenities/     (eco pool, floating dining, labrisa lounge, modern oasis)
│   ├── flora/         (15 species modules)
│   ├── subscene/      (53 sub-render drivers, the asset layer)
│   ├── materials/     (9 material modules)
│   ├── restaurant/    (4 kitchen modules)
│   ├── util/          (4 utility modules - 10 rules check, sun check, audit)
│   ├── animation/     (turntable)
│   ├── output/        (equirectangular)
│   └── finance/       (BoQ writer)
│
├── renders/                                  (21 PNGs - 18 final A/B/C × 6 cameras + 3 sub)
├── tools/                                    (check_licenses.py + site_data submodule)
├── LICENSES/                                 (393 verbatim legal text files)
│
└── docs/                                     (411 .md files - the documentation layer)
    ├── WES_TODO.md                  (running TODO, 16 items)
    ├── WES_TODO_UPDATE.md           (status log)
    ├── WES_5_THIS_WEEK.md          (1.5-hour action plan)
    ├── PRIORITIES_NEXT.md           (tomorrow morning's action list)
    ├── STATUS_REPORT.md             (final implementation summary)
    ├── IMPLEMENTATION_PROGRESS.md  (running log)
    ├── IMPLEMENTATION_COMPLETE.md  (final summary)
    ├── CRITICAL_PATH.md            (visual dep graph)
    ├── TIMELINE.md                  (3-year build schedule)
    ├── 4ENTITY_BV_CASCADE.md      (BV structure visual)
    │
    ├── MASTER_BRIEF.md              (reconciled project overview, 18 KB)
    ├── AUDIT/                       (3 audit docs)
    │   ├── INVENTORY.md
    │   ├── CRITIQUE.md
    │   └── RESTRUCTURE_PLAN.md
    │   └── PATCHES_AND_GAPS_FOUND.md
    │
    ├── WRITTEN_BRIEFS_FOR_HUMAN_ACTIONS/   (5 briefings, in `people/`)
    │   ├── SONJA_QUESTIONNAIRE.md    (16 Q's)
    │   ├── ATTORNEY_BRIEF.md         (12 Q's)
    │   ├── SITE_VISIT_BRIEF.md       (7-day plan)
    │   ├── WES_ACTIONS.md            (5 things)
    │   └── CONTACTS.md               (human network)
    │
    ├── _reconciled/                 (merged view, 10 files)
    │   ├── MASTER_BRIEF.md           (single-page)
    │   ├── FINANCIAL_MODEL.md        (€5.5M Phase 1)
    │   ├── CABIN_CATALOG.md          (30 cabins, 10 types)
    │   ├── INFRASTRUCTURE_8_PHASES.md
    │   ├── EQUIPMENT_STRATEGY.md
    │   ├── MATERIALS_PRICE_TEMPLATE.md
    │   ├── ACTIVITIES_25_PLUS.md
    │   ├── BUSINESS_STRUCTURE.md
    │   ├── OPEN_DECISIONS.md
    │   ├── DECISIONS_LOG.md
    │   ├── LAND_PARCEL.md
    │
    ├── people/                      (human-side, 5 files + README)
    │
    ├── research/                    (research tooling + 64 result files)
    │   ├── EXECUTION.md            (research tracker)
    │   ├── SPRINT1_AI_BATCH_PLAN.md (30-item plan)
    │   ├── 5_ONDERWERPEN_MATERIALS.md
    │   └── RESULTS/                  (64 answer files)
    │       ├── M04_cement_rebar_pricing.md
    │       ├── M05_aluminum_glass.md
    │       ├── M08_septic_reed_bed.md
    │       ├── M09_fasteners.md
    │       ├── M10_flooring.md
    │       ├── M11_paint.md
    │       ├── M21_pool_equipment.md
    │       ├── M22_kitchen_equipment_import.md
    │       ├── M22_M43_restaurant_suppliers_corrected.md
    │       ├── M23_ac_units.md
    │       ├── M24_customs_brokers.md
    │       ├── M_marketing_tracker.md
    │       ├── F03_ande_3phase.md
    │       ├── F09_solar_pv.md
    │       ├── F10_lifepo4_battery.md
    │       ├── F11_cell_coverage.md
    │       ├── F12_starlink.md
    │       ├── F15_cistern_sizing.md
    │       ├── F19_generator_sizing.md
    │       ├── F20_tundra_vs_presio.md
    │       ├── F_series_tracker.md
    │       ├── L05_NL_BV_threshold_70k.md
    │       ├── L06_PY_entity_types.md
    │       ├── L08_RUC_setup.md
    │       ├── L14_bancard_pagopar.md
    │       ├── L15_L16_L17_banking_bundle.md
    │       ├── L17_fx_transfer.md
    │       ├── L18_currency_hedging.md
    │       ├── L19_tax_treaty.md
    │       ├── L20_MERCOSUR_residency.md
    │       ├── L21_SENATUR_classification.md
    │       ├── L22_insurance_minimums.md
    │       ├── L23_L_series_index.md
    │       ├── BR01_name_pick.md
    │       ├── BR02_domain_check.md
    │       ├── BR03_spanish_domains.md
    │       ├── AH01_hilux_pricing.md
    │       ├── AH02_tundra_parts.md
    │       ├── AH03_used_vs_new_REVISED.md
    │       ├── PA03_san_ber_hotels.md
    │       ├── MK06_senatur_statistics.md
    │       ├── MK08_air_access.md
    │       ├── V04_european_dutch_market.md
    │       ├── V08_multi_season_tour.md
    │       ├── W01_W08_sonja_salary_preliminary.md
    │       ├── W03_project_name_check.md
    │       ├── W04_anexo_I_status.md
    │       ├── W05_drone_lidar_pilots.md
    │       ├── W11_W12_aguinaldo_vacaciones.md
    │       ├── FT10_chef_partnership.md
    │       ├── FT11_eu_restaurants_PY.md
    │       ├── FT14_py_products.md
    │       ├── FT15_restaurant_tech.md
    │       ├── EN02_native_plants.md
    │       ├── EN05_volunteer_tourism.md
    │       ├── D6_wellness_pool.md
    │       ├── D14_brand_positioning.md
    │       ├── X01_X04_event_infrastructure.md
    │       ├── R01_fire_safety_plan.md
    │       ├── insurance_fire_bundle.md
    │       ├── F14_inaa_water_permit.md
    │       └── (more to come)
    │
    ├── patches/                     (2 patch files for HOUSING_PARK_CONCEPT + RESEARCH_GAPS)
    │
    ├── ideas/                       (109 idea files, 12-section format)
    │   ├── INDEX.md
    │   ├── INSIGHTS.md
    │   ├── SUGGESTED.md
    │   ├── WES_TODO.md
    │   ├── vision/                  (5 ideas)
    │   ├── buyer_experience/        (8)
    │   ├── amenities/               (10)
    │   ├── construction/            (18)
    │   ├── house_typologies/        (7)
    │   ├── operations/              (24)
    │   ├── finance_legal/           (16)
    │   ├── site_specifics/          (8)
    │   ├── marketing/                (10)
    │   └── risk_mitigation/         (7)
    │
    ├── audios/                      (5 audio recordings + 6 final docs)
    │
    ├── site_data/                   (Paraguayan site analysis, see INVENTORY.md)
    ├── render_catalogue/           (926 renders across 53 assets)
    ├── escritura_deck/             (legal-frozen, 7 files, escritura week)
    ├── boq/                         (BoQ, frozen at escritura, 3 files)
    ├── finance/                     (FX rates, frozen)
    ├── comms/                       (Wes + Thijs communications, frozen)
    ├── email_drafts/                (Wes + Peña + Burgos emails, frozen)
    │
    ├── HOUSING_PARK_CONCEPT.md      (8 concept menu, 29 KB)
    ├── EUROPEAN_TOURISM_SPEC.md     (target market research, 33 KB)
    ├── MASTER_TODO.md               (project phases P0-P4, 31 KB)
    ├── RESEARCH_GAPS.md             (R01-R50 research tracker, 24 KB)
    ├── MASTER_BRIEF.md              (1-page project brief, frozen)
    ├── DECISIONS.md                 (project decisions, frozen)
    ├── GAPS_ANALYSIS.md             (gap analysis, frozen)
    ├── ARCHIVE_RUNBOOK.md           (archive procedures)
    ├── CHANGELOG.md                 (change log)
    ├── CLIENT.md, REPO_UPDATES.md, REPO_RESEARCH_100.md, etc. (frozen context)
    │
    ├── INDEX.md                     (docs/ navigation index)
    ├── _archive/                    (2026-06-1X, sealed)
    ├── 2026-06-13_snapshot/         (site_data snapshot, gitignored)
    │
    ├── MASTER_TODO.md, etc.         (master trackers)
    ├── RESULTS_GUIDE.md
    ├── satellite/                   (GEE/NICFI quickstart)
    └── references/                  (Wes 2026-06-11 reference)
```

## Where to start (5 entry points)

1. **`docs/WES_5_THIS_WEEK.md`** — Wes's immediate action list (5 things, 1.5-2 hr)
2. **`docs/_reconciled/MASTER_BRIEF.md`** — single-page project overview
3. **`docs/_reconciled/OPEN_DECISIONS.md`** — 15 pending decisions
4. **`docs/research/EXECUTION.md`** — research tracker (65/128 items answered)
5. **`docs/PRIORITIES_NEXT.md`** — tomorrow morning's action list (Wes's 5 things)

## How to navigate the canonical doc tree

**For strategic questions** (what is the project? what's the plan?):
- `_reconciled/MASTER_BRIEF.md` (1 page, the answer)
- `_reconciled/FINANCIAL_MODEL.md` (€5.5M Phase 1 detail)
- `_reconciled/BUSINESS_STRUCTURE.md` (4-BV cascade)
- `_reconciled/CABIN_CATALOG.md` (30 cabins, 10 types)

**For research questions** (what do we know? what do we still need?):
- `research/EXECUTION.md` (tracker)
- `research/SPRINT1_AI_BATCH_PLAN.md` (30-item plan)
- `research/RESULTS/*.md` (65+ answer files)
- `audios/2026-06-30-wes-post-escritura/final/IDEAS_LOG.md` (95 ideas from audios)
- `RESEARCH_GAPS.md` (R01-R50)
- `IDEAS_CATALOG_PATCH_PLAN.md` (how to update the 109)

**For decision questions** (what's open?):
- `_reconciled/OPEN_DECISIONS.md` (15 open)
- `_reconciled/DECISIONS_LOG.md` (closed)
- `PRIORITIES_NEXT.md` (tomorrow's action list)
- `CRITICAL_PATH.md` (visual dep graph)
- `TIMELINE.md` (3-year build schedule)

**For human action** (what do I do?):
- `WES_5_THIS_WEEK.md` (Wes's 5 actions)
- `people/SONJA_QUESTIONNAIRE.md` (16 Q's for Sonja)
- `people/ATTORNEY_BRIEF.md` (12 Q's for attorney)
- `people/SITE_VISIT_BRIEF.md` (W1.2 7-day plan)
- `people/WES_ACTIONS.md` (5 things this week)
- `people/CONTACTS.md` (human network)

**For the audio synthesis work** (the 5 Wes recordings):
- `audios/2026-06-30-wes-post-escritura/SYNTHESIS.md` (overview)
- `audios/2026-06-30-wes-post-escritura/final/SYNTHESIS.md`
- `audios/2026-06-30-wes-post-escritura/final/DREAMLIST_NL.md` (15 wish categories)
- `audios/2026-06-30-wes-post-escritura/final/IDEAS_LOG.md` (95 ideas)
- `audios/2026-06-30-wes-post-escritura/final/RESEARCH_CATALOGUE.md` (131 items)
- `audios/2026-06-30-wes-post-escritura/final/ACTIONLIST_ES_EN.md` (P0-P4 plan)

**For the canonical historical context** (frozen at escritura):
- `STATUS.md` (canonical state)
- `HOUSING_PARK_CONCEPT.md` (8 concept menu)
- `EUROPEAN_TOURISM_SPEC.md` (target market)
- `MASTER_TODO.md` (P0-P4 phase plan)
- `BOQ/` (escritura-frozen BoQ)
- `escritura_deck/` (frozen legal docs)
- `_archive/2026-06-1X/` (sealed archive)

**For audit/critique** (how good is the current state?):
- `audit/INVENTORY.md` (file inventory)
- `audit/CRITIQUE.md` (honest roast)
- `audit/RESTRUCTURE_PLAN.md` (proposed actions)
- `audit/PATCHES_AND_GAPS_FOUND.md` (gap analysis)

**For the canonical code** (the LQV renderer pipeline):
- `lqv/` (148 Python files, 22K LOC, 14 subpackages)
- `ARCHITECTURE.md` (lqv/ package map)
- `CLAUDE.md` (AI session instructions)

**For frozen artefacts** (escritura-week, don't modify):
- `escritura_deck/` (7 files, 77 MB)
- `boq/` (BoQ, $268,685.45 USD frozen)
- `comms/`, `email_drafts/` (legal communications)
- `LICENSE_BUNDLE.md`, `LICENSES/` (legal text)
- `dist/print_pack_2026-06-27/` (gitignored, USB contents)

## Net result

- **65+ research items answered** (51% of catalog + 30+ additional = ~60% of full research universe)
- **6 human-side briefings ready** for Wes to execute
- **15 open decisions tracked** in `_reconciled/OPEN_DECISIONS.md`
- **4-BV cascade documented** for attorney validation
- **1 transcription error fixed** (Sonia's 16th → 60th birthday)
- **1 hallucination corrected** (GastroHaus → real PY suppliers)
- **1 NPV revised** (Tundra vs Hilux with import tax impact)

**Status: implementation complete. Foundation built. Execution is waiting on the human side.**

Wes's 5 actions this week = 1.5-2 hours = unblocks 30+ items + Phase 1 break-ground conditions.
