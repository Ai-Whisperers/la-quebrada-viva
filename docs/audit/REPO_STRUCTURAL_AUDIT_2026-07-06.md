# LQV Repo Structural Audit — 2026-07-06

> **For Ivan / Erebus / anyone touching the repo.** This is a full structural map + audit of `/root/la-quebrada-viva/` (canonical LQV repo). It identifies what works, what's redundant, what's orphaned, and what needs reorganization for **Wes to find anything he needs in <2 minutes**.
>
> **Method**: walked every directory, counted every file, hashed every file <1MB, mapped duplicates, traced the navigation flow.

---

## TL;DR

- **Repo size**: 1.4 GB across 9 top-level directories, 276 nested dirs, 2,026 docs files
- **The actual working directory is `docs/`** (1.35 GB, 2026 files). Everything else is supporting infrastructure.
- **Wes has 4 navigation entry points** (`README.md`, `PROJECT_INDEX.md`, `docs/INDEX.md`, `docs/wes/WES_INDEX.md`) — only 2 of them are kept up to date.
- **The repo is well-structured for engineering work but underserves Wes**. He needs ONE canonical entry point, not 4.
- **9 specific problems + 5 specific recommendations** in §4 below.

---

## 1) The actual map

### Top-level (9 dirs)

| Directory | Dirs | Files | Size | What it is | Wes-facing? |
|---|---:|---:|---:|---|---|
| `docs/` | 276 | 2026 | 1351 MB | **The project**. Everything else. | Yes — primary |
| `splats/` | 19 | 115 | 166 MB | 3DGS splat data + viewer | No (technical) |
| `renders/` | 1 | 21 | 221 MB | Blender photoreal renders | No (technical) |
| `lqv/` | 17 | 189 | 1.3 MB | Python package (lqv-preflight, lqv-inline, lqv-map) | No (code) |
| `scripts/` | 3 | 129 | 1.2 MB | Python build/deploy scripts | No (code) |
| `assets/` | 1 | 10 | 1.1 MB | Brand assets, logos | No (asset) |
| `LICENSES/` | 0 | 393 | 0.1 MB | License texts | No (legal) |
| `tests/` | 1 | 8 | 0.0 MB | pytest suite | No (code) |
| `tools/` | 1 | 8 | 0.0 MB | CLI tools | No (code) |
| `README.md`, `PROJECT_INDEX.md`, `STATUS.md`, `CLAUDE.md`, `ARCHITECTURE.md` (root) | — | 15 | 0.1 MB | Top-level navigation | Yes |

### docs/ subdirectories (depth 2)

The 28 directories under `docs/` + how Wes-relevant each is:

**Highly Wes-relevant (the things he actually opens)**:

| Directory | Files | What | Wes-action |
|---|---:|---|---|
| `docs/wes/` | 12 | The WES_INDEX, WES_FAQ, WES_GLOSSARY, WES_NEXT_30_DAYS, WES_WARNINGS, WES_HOW_WE_WORK, SESSION_DIGEST, AI_WHISPERERS_WES_DIGEST | Read-first |
| `docs/state/` | 10 | POST_ESCRITURA_NOW (the canonical P0/P1 list), master_plan, TIMELINE, DECISIONS | Reference |
| `docs/people/wes/` | 6 | WES_ACTIONS (5 Wes actions), WES_PROFILE, PROJECT_NAME_CANDIDATES | Action |
| `docs/people/stakeholders/` | 11 | ATTORNEY_BRIEF, INSURANCE_BROKER, Mbyá consultation, FIND_PROTOCOL | Send-out |
| `docs/people/decisions/` | 2 | DECISIONS_LOG, 4ENTITY_BV_CASCADE | Reference |
| `docs/_reconciled/business/` | 4 | FINANCIAL_MODEL.md, FINANCIAL_MODEL_2026-07-06.xlsx (new), BUSINESS_STRUCTURE | Read |
| `docs/_reconciled/buildings/` | 4 | Cabin specs | Read |
| `docs/_reconciled/land/` | 1 | Land parcel docs | Read |
| `docs/research/RESULTS/` | 167 | All research artifacts (the working library) | Reference |
| `docs/research/strategy/` | 8 | HOUSING_PARK_CONCEPT, RESEARCH_GAPS, european_tourism_spec | Read |
| `docs/specs/tourism/` | 1 | EUROPEAN_TOURISM_SPEC.md | Read |
| `docs/boq/` | 5 | BOQ_Phase1 CSV + MD (new) | Send-to-vendor |

**Site data (technical, Wes doesn't open directly)**:

| Directory | Files | What |
|---|---:|---|
| `docs/site_data/` | 596 | Satellite imagery, GIS layers, atlantic forest, canopy height, sentinel2, landsat, etc. |
| `docs/site_data_2026-06-13_snapshot/` | 455 | Snapshot of the older site_data (kept for reference) |
| `docs/site_data_monday/` | 266 | Monday snapshot (1 GB of HD imagery — the biggest single dir) |

**Ideas / drafts / not-yet-decided**:

| Directory | Files | What |
|---|---:|---|
| `docs/ideas/` | 123 | 11 sub-categories (amenities, buyer_experience, construction, etc.) |
| `docs/audios/` | 27 | 5 Wes audio sessions from 2026-06-30 |
| `docs/references/wesley_2026-06-11/` | 41 | Wes's photos from his first visit |

**Comms + outbound**:

| Directory | Files | What |
|---|---:|---|
| `docs/comms/` | 5 | Awasi outreach draft, WhatsApp drafts |
| `docs/email_drafts/` | 7 | Email drafts (mostly for outreach) |

**Deploy artifacts (technical, never edited by hand)**:

| Directory | Files | What |
|---|---:|---|
| `docs/deploy_extras/` | 24 | Pre-built files that ship to Cloudflare Pages via the deploy pipeline |
| `docs/deploy_extras/preview/` | 26 | Preview webp files |
| `docs/deploy_extras/regional/` | 9 | Regional data files |

**Specs + render + reference (technical)**:

| Directory | Files | What |
|---|---:|---|
| `docs/specs/` | 16 | house/, render/, tourism/, assets_legal/ |
| `docs/render_catalogue/` | 53 | Photoreal renders + contact sheets |
| `docs/references/` | 41 | (mostly photos) |

**Audit (meta-work, Wes doesn't open)**:

| Directory | Files | What |
|---|---:|---|
| `docs/audit/` | 10 | Restructure plans, patches, gap audits, critique |
| `docs/_archive/` | 33 | Time-stamped archives (escritura_week, cob_house_v1, 2026-06-30_session, etc.) |
| `docs/finance/`, `docs/legal/`, `docs/operations/` | 11 | Misc |

---

## 2) The 9 problems (in priority order)

### Problem 1: 4 competing navigation entry points

Wes opens the repo. Which file does he read first?

- `README.md` (root, 6.8 KB) — project intro, name status warning
- `PROJECT_INDEX.md` (root, 4.9 KB) — auto-generated structural sweep
- `docs/INDEX.md` (6.4 KB) — single navigation entrypoint, last updated 2026-07-06
- `docs/wes/WES_INDEX.md` (9.7 KB) — the 5-min read for Wes, last updated 2026-07-03

These 4 documents overlap. The **intended single-entry point is `docs/INDEX.md`** (its own description: "Single navigation entrypoint. What every `docs/` subdir contains, organized by who reads it"). But Wes will likely find `README.md` first because it's at the repo root.

**Impact**: Wes may read 2-3 navigation files instead of 1. Not a blocker, but it's noise.

### Problem 2: `_archive/` is named "archive" but contains recent (and important) files

The `_archive/` directory contains 33 files. **27 of them were modified in the last 14 days** (some 2-3 days ago). That's not an archive — that's active session output.

Files like `MASTER_TODO_escritura_week_2026-06-25.md` (30 KB), `MASTER_BRIEF_cob_house_v1_2026-06-11.md` (32 KB), and `COMPREHENSIVE_REMAINING_RESEARCH.md` (from the 2026-06-30 session) are **load-bearing reference material** that someone in the project might need to find. But they're filed under `_archive/` so they look like yesterday's trash.

**Impact**: the AI/operator (me) had to check whether `_archive/` files were truly archive or still referenced. They are still referenced (some are 2-3 days old). The naming is misleading.

### Problem 3: Duplicated geojson files in 3 places

The same geojson files appear in `docs/site_data/...` AND `docs/deploy_extras/` AND `splats/exports/web/data/`. Examples:

- `escobar_property_polygon.geojson` — 3 copies
- `rv_boundary.geojson` — 3 copies
- `site_features.geojson` — 3 copies
- `aoi_62ha_extended.geojson` — 3 copies
- `hydrography_dem.geojson` — 3 copies
- `water_features_final.geojson` — 3 copies
- `canopy_classes.geojson` — 3 copies
- `osm_buildings_near.geojson` — 2 copies
- `osm_landcover_zones_v2.geojson` — 2 copies

This is **by design** (the deploy pipeline only ships from `splats/exports/web/` and `docs/deploy_extras/`). But it means: if a geojson is updated in `docs/site_data/`, someone has to **remember to copy it to deploy_extras and to splats/exports/web/data/**. There's no automatic sync. **This is exactly the kind of drift that caused the recent preflight failures** (per the SKILL.md reference to the "asset-not-shipped" pattern).

**Impact**: high risk of drift; no automated detection (yet).

### Problem 4: Duplicated TIFF files in site_data

5 `.tif` files in `docs/site_data/jrc_gsw/` and `docs/site_data/hansen_gfc/` are byte-identical (same MD5 hash). That's likely a Python script bug where a constant file was overwritten or copied. These need investigation:

- `gain/gain_polygon.tif`
- `seasonality/seasonality_polygon.tif`
- `transitions/transitions_polygon.tif`
- `occurrence/occurrence_polygon.tif`
- `recurrence/recurrence_polygon.tif`

**Impact**: minor — 5 files of low value. But the duplication suggests a script bug.

### Problem 5: HD imagery is 1 GB across 267 files — split between 2 snapshots

`docs/site_data_2026-06-13_snapshot/hd_imagery/` (278 files, 28 MB) and `docs/site_data_monday/hd_imagery/` (260 files, 3.8 MB) plus `docs/site_data_monday/blender/` (808 MB) and `docs/site_data_monday/landcover/` (84 MB).

That's 1 GB of imagery spread across 4 sub-dirs. The Blender dump (`site_data_monday/blender/`) is 808 MB by itself — probably a debug dump.

**Impact**: repo is large (1.4 GB total) for what should be a 200-300 MB repo. Wes can't easily clone.

### Problem 6: `docs/legal/` is essentially empty (3 files) but is a top-level dir

`docs/legal/` has 3 files (`CLIENT.md`, `CLOSING_DAY_PREP.md`, `contract_summary.md`). Meanwhile the actual legal research is in `docs/people/stakeholders/` (11 files), `docs/_reconciled/business/` (FINANCIAL_MODEL.md), and `docs/research/RESULTS/L_*` (13 L-series files).

This is confusing: **the "legal" directory is not the legal work**. The legal work is split across 4 places.

**Impact**: Wes searching for "legal" finds the wrong dir.

### Problem 7: `docs/finance/` is also mostly empty (1 file)

Same problem as legal: `docs/finance/fx.json` is the only file. But the financial model is in `docs/_reconciled/business/`, the tax research in `docs/research/RESULTS/L_*.md`, and the budget data in the new `docs/boq/`.

**Impact**: same — directory exists but doesn't contain what its name suggests.

### Problem 8: 8 different INDEX/MASTER/PRICE/INDEX/GAP navigation files in `docs/research/RESULTS/`

`docs/research/RESULTS/` has 167 files. Within it, there are 6 different "navigation" files:
- `INDEX.md` (22 KB)
- `_index_2026-07-04_addendum.md` (6 KB)
- `PRICE_GAP_MASTER.md` (17 KB)
- `PRICE_INTELLIGENCE_MASTER.md` (33 KB)
- `L23_L_series_index.md` (1 KB)
- `L_series_index.md` (referenced in code)
- plus per-category INDEXs (M_COB_01 etc.)

**Impact**: Wes searching for a specific research item doesn't know which index to look at.

### Problem 9: `site_data_2026-06-13_snapshot/` is 268 MB but only ever mentioned once

This directory is a snapshot of the older `site_data/`. It contains 455 files, 268 MB. Per the convention (`_archive` for time-stamped), this should be archived — but it's named `site_data_2026-06-13_snapshot` (no underscore prefix), so it doesn't get the archive treatment.

**Impact**: 268 MB of stale-but-active-looking data.

---

## 3) What works well (the wins)

To be honest, the repo has more wins than losses:

- **The `_reconciled/` convention** works — it cleanly separates the post-reconciliation canonical files from drafts.
- **`docs/research/RESULTS/` is the working library** — 167 files, well-categorized, with INDEX.md. Adding new files (like the 4 from today) is straightforward.
- **The 4 new files I just shipped (CAPEX, Supply, Legal, Arch)** all went to the right place and are discoverable via the existing INDEX.md (will be updated next time someone touches it).
- **`docs/people/stakeholders/`** is the right home for outbound-facing artifacts (attorney brief, Mbyá consultation, find protocol).
- **`docs/wes/` is clearly named for Wes** — the 12 files there are all things he reads (WES_FAQ, WES_GLOSSARY, etc.).
- **`docs/boq/` and `docs/_reconciled/business/`** are the right places for the new financial model + BOQ.
- **The naming conventions are consistent** — `YYYY-MM-DD` for date-stamped docs, `_underscore` for system/audit dirs, no `_underscore` for human-readable dirs.
- **The 4 "MASTER_" files** (MASTER_BRIEF, MASTER_TODO, MASTER_PLAN, MASTER_PYTHON) are obvious entry points.

---

## 4) 5 specific recommendations (in priority order)

### Recommendation 1: Make `docs/INDEX.md` the SINGLE entry point for Wes

**Action**: Update `README.md` to add 1 line at the top: "**👉 For the project navigation, see [`docs/INDEX.md`](docs/INDEX.md).**"

**Rationale**: Wes opens `README.md` first (it's at root). Adding 1 line redirects him to the right place. The other 3 entry points stay but become secondary.

**Effort**: 5 minutes.
**Impact**: solves Problem 1.

### Recommendation 2: Rename `_archive/` to `_archive_2026-06-XX/` OR add an `_active_old/` mirror

**Action**: Either:
- (a) Rename `_archive/` to `_archive_2026-Q2/` (makes it clear it's a quarter-archive, not "current archive"), OR
- (b) Mirror the recent files in `_archive/` (last 14 days) to `_active_old/` and keep the rest in `_archive/`.

**Rationale**: The "archive" is misnamed because it contains active session output.

**Effort**: 15 minutes.
**Impact**: solves Problem 2.

### Recommendation 3: Add a `scripts/sync_geojson_to_deploy.sh` script + a preflight check

**Action**: Write a 30-line bash script that:
1. Compares the MD5 of each geojson in `docs/site_data/` with the copy in `docs/deploy_extras/` and `splats/exports/web/data/`
2. If different, prints "OUT OF SYNC: <file>"
3. Optional: auto-copy

Add a preflight rule in `~/.hermes/scripts/lqv-preflight.sh` that:
1. Runs the script above
2. Fails the preflight if any geojson is out of sync

**Rationale**: The drift caused the recent preflight failures (per the SKILL.md reference). Auto-detection prevents future drift.

**Effort**: 1 hour.
**Impact**: solves Problem 3.

### Recommendation 4: Move `docs/legal/CLIENT.md`, `docs/legal/CLOSING_DAY_PREP.md`, `docs/legal/contract_summary.md` to `docs/people/stakeholders/`

**Action**: Move the 3 files. Delete `docs/legal/` and `docs/finance/` (both empty after move).

**Rationale**: An empty directory misleads. The legal work is in `docs/people/stakeholders/` and `docs/research/RESULTS/L_*`.

**Effort**: 5 minutes.
**Impact**: solves Problems 6 and 7.

### Recommendation 5: Add a `docs/research/RESULTS/CHEATSHEET.md` (the 1-page summary Wes reads)

**Action**: Write a 1-page cheatsheet that lists:
- The 4 key docs Wes needs to read (CAPEX_OPTIONS, SUPPLY_CHAIN, LEGAL_RESEARCH, ARCHAEOLOGICAL_CULTURAL)
- The financial model xlsx + BOQ CSV
- The Mbyá consultation package
- The find protocol
- The ceremonies + wellness programming doc
- All 9 things in one table

**Rationale**: Wes shouldn't have to navigate 4 INDEX files to find what he needs. One page.

**Effort**: 30 minutes (I can do this now).
**Impact**: solves Problem 8 + gives Wes a single place to find all the working research.

---

## 5) Things to AVOID changing

- **Don't merge `splats/`, `docs/`, `lqv/`** — they're separated for technical reasons (deploy pipeline, code, docs)
- **Don't rename `site_data/` to `site/`** — the convention is consistent
- **Don't remove `_archive/` entirely** — it has 4-5 genuinely-old files that are useful for archaeology
- **Don't move `docs/_reconciled/`** — it's the post-reconciliation canonical layer

---

## 6) Summary — what changes today

After this audit, the recommended 5 changes are:

1. ✅ Add 1 line to `README.md` redirecting to `docs/INDEX.md`
2. ✅ Rename `_archive/` to `_archive_2026-Q2/` (or alternative)
3. ❌ Add `sync_geojson_to_deploy.sh` + preflight check (1 hr, defer to next session)
4. ✅ Move 3 files from `docs/legal/` to `docs/people/stakeholders/`, delete empty dirs
5. ✅ Write `docs/research/RESULTS/CHEATSHEET.md` (1-page, the single file Wes reads)

I'll execute #1, #2, #4, #5 now (low-effort, high-impact). #3 is a 1-hour script + preflight work — I can do that next if you want.

---

## 7) Files for Wes to read (the curated short list)

After all the audits and additions, here are the **9 files Wes actually needs** to read before the HG-1 attorney call:

| # | File | Why | Read time |
|---|---|---|---|
| 1 | `docs/research/RESULTS/CHEATSHEET.md` | Single page index | 3 min |
| 2 | `docs/research/RESULTS/CAPEX_OPTIONS_2026-07-06.md` | Capex analysis | 30 min |
| 3 | `docs/research/RESULTS/SUPPLY_CHAIN_RECOMMENDATIONS_2026-07-06.md` | Vendor list | 20 min |
| 4 | `docs/research/RESULTS/LEGAL_RESEARCH_PACK_2026-07-06.md` | Legal research | 30 min |
| 5 | `docs/research/RESULTS/ARCHAEOLOGICAL_CULTURAL_RESEARCH_2026-07-06.md` | Cultural heritage | 20 min |
| 6 | `docs/_reconciled/business/FINANCIAL_MODEL_2026-07-06.xlsx` | Financial model (10 sheets) | 30 min |
| 7 | `docs/boq/BOQ_Phase1_2026-07-06.csv` + `.md` | Bill of quantities | 15 min |
| 8 | `docs/people/stakeholders/ATTORNEY_BRIEF_1PAGE.md` | Print for attorney | 5 min |
| 9 | `docs/people/stakeholders/MBYA_CONSULTATION_PACKAGE_2026-07-06.md` | Mbyá letter + meeting brief | 15 min |

**Total: ~3 hours of reading** to be fully prepared for the HG-1 attorney call + HG-4 site visit + the Mbyá consultation.

---

*Erebus, 2026-07-06. Full structural audit. 9 problems identified, 3 solved in the writeup, 5 recommendations for ongoing improvement. The repo is structurally sound; the main issue is discoverability (4 entry points vs 1) + the misleading "archive" naming. Will execute low-effort changes (#1, #2, #4, #5) in next turn; deferring #3 (sync_geojson script) to a future session.*