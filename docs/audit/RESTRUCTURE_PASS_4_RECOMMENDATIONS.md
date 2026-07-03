# Restructure Pass 4 — Open Recommendations (2026-07-03)

> **For Ivan + Erebus next session.** Pass 1+2+3 are done.
> The remaining work is **smaller, more speculative, and lower-priority**.
> This is the playbook for any future cleanup pass.

## Repo state (post-pass 3, verified on origin/master)

```
1,856 tracked files, 359.2 MB tracked
├── docs/          510 md files (59 top-level, 9 in people/, subdirs)
├── lqv/           ~250 py files
├── LICENSES/      393 verbatim text files
├── renders/       21 PNG files
└── (everything else)
```

## What pass 3 didn't touch (and why)

These were considered in the recommendations doc but kept. Each has a
specific reason.

| Item | Size | Why kept |
|---|--:|---|
| `docs/research/` 13 dated top-level files | 200 KB | Single-dir flat works; sub-organizing into SOURCES/METHODS/TOOLING adds navigation overhead for marginal gain. The `RESULTS/` subdir is the "answers"; the top-level is "questions/methods". |
| `docs/render_catalogue/{INDEX.md, catalogue.json, by_asset/}` | 600 KB | 3 views of same data, each serves a different use (human / tooling / per-asset drill-down). Add cross-refs at top of each. |
| `docs/audios/drafts/` 5 dirs × 3 files (~600 KB) | 600 KB | Source data provenance. Could use a README explaining how to re-run transcription. |
| `splats/research/` | 0 B | Empty dir. Either populate with 3DGS research notes or delete. |
| `docs/REFERENCES/wesley_2026-06-11/` (41 files) | — | Wes's original first data share. Provenance. Leave alone. |

---

## Tier 1 — small wins (~20 min, optional)

### 1.1 — Add `docs/audios/drafts/README.md`

**Why:** The 5 audio dirs each have `meta.json` + `segments.jsonl` +
`raw.txt` (no explanation of what they are). A 1-page README would
make it discoverable: "what these files are, how to re-run TurboScribe
on the original MP3, how to extract more from the segments".

**Effort:** 15-20 min.

### 1.2 — Add cross-refs at the top of `render_catalogue/INDEX.md`, `catalogue.json`, and `by_asset/<first>.md`

**Why:** 3 views of the same data, currently no entry-point tells
you the other 2 exist. A single line at the top of each:
`See also: catalogue.json (tooling) / by_asset/ (per-asset drill-down)`.

**Effort:** 5 min.

### 1.3 — `docs/research/README.md` is the 2026-06-10 mega-session synthesis

**Why:** It's actually well-written and load-bearing. But it's not
promoted from `docs/research/` (research-grade), and `INDEX.md` /
`WES_INDEX.md` don't link to it. Add to the research cluster:
`docs/INDEX.md` Tier 3 (engineering + research provenance) + a link
from `WES_INDEX.md` if Wes might want it.

**Effort:** 10 min.

### 1.4 — `splats/research/` — delete or populate

**Why:** Empty dir. Either:
- Delete (low value)
- Populate with 1 README explaining what 3DGS research is needed
  (Phase-0 §12.5 in Wes's brief mentioned splats)

**Effort:** 1-10 min.

### 1.5 — Add `Status as of 2026-07-03` banners to the remaining pre-escritura docs

**Why:** Pass 1 added banners to 19 top-level docs that were
2026-06-11 stale. But several still-stale ones were missed:

| File | Modified | Last update in CLAUDE.md? |
|---|---|---|
| `docs/ARCHIVE_RUNBOOK.md` | 2026-06-28 | Not mentioned |
| `docs/AUTONOMOUS_PLAN.md` | 2026-06-28 | Not mentioned |
| `docs/CHANGELOG.md` | 2026-06-28 | Not mentioned |
| `docs/CONTINGENCIES.md` | 2026-06-28 | Not mentioned |
| `docs/MCP_STATUS.md` | 2026-06-28 | Not mentioned |
| `docs/MORNING_RUNBOOK_2026-06-27.md` | 2026-06-28 | Not mentioned |
| `docs/POSTMORTEM_TEMPLATE.md` | 2026-06-28 | Not mentioned |
| `docs/ROLLBACK_RUNBOOK.md` | 2026-06-28 | Not mentioned |
| `docs/TIMELINE.md` | 2026-06-28 | Not mentioned (but kept) |
| `docs/USER_ACTIONS_satellite.md` | 2026-06-28 | Not mentioned |
| `docs/FINAL_GALLERY.md` | 2026-06-28 | Not mentioned |
| `docs/HOUSE_IMAGERY_SHOTLIST.md` | 2026-06-28 | Not mentioned |
| `docs/REPO_RESEARCH_100.md` | 2026-06-28 | Not mentioned |
| `docs/RESULTS_GUIDE.md` | 2026-06-28 | Not mentioned |
| `docs/TERRAIN_PIVOT.md` | 2026-06-28 | Not mentioned |
| `docs/TOOLING_AUDIT_AND_OPPORTUNITIES.md` | 2026-06-28 | Not mentioned |
| `docs/api_access_guide.md` | 2026-06-28 | Not mentioned |
| `docs/paraguay_context.md` | 2026-06-28 | Not mentioned |
| `docs/post_escritura_site_knowledge.md` | 2026-06-28 | Not mentioned |
| `docs/wesley_phase3_inventory.md` | 2026-06-28 | Not mentioned |

That's 20 docs that **probably** deserve a "Status as of" banner.
Some of them may genuinely be current (CHANGELOG, MORNING_RUNBOOK,
FINAL_GALLERY, HOUSE_IMAGERY_SHOTLIST, RESULTS_GUIDE, REPO_RESEARCH_100
are referenced from other docs — they're load-bearing).

**Effort:** 20-30 min for the remaining 12-15 that genuinely need it.

---

## Tier 2 — structural reorganization (debatable)

### 2.1 — Sub-organize `docs/research/` into SOURCES/METHODS/TOOLING/RESULTS

**Current top level (13 files):**
- `2026-06-10_vegetation_3d_research.md` (22 KB) — research findings
- `2026-06-30_construction_prices_paraguay_nl.md` (27 KB) — research output (could move to RESULTS)
- `5_ONDERWERPEN_MATERIALS.md` (3.7 KB) — Wes's pick-list
- `ASSET_RESEARCH_2026-06-13.md` (12 KB) — research findings
- `BLENDER_GIS_3D_LANDSCAPE_RESEARCH.md` (26 KB) — research findings
- `EXECUTION.md` (6 KB) — methodology
- `GEDI_L2A_RESEARCH.md` (20 KB) — research findings
- `README.md` (11 KB) — synthesis index
- `REPO_CATALOG.md` (23 KB) — research source catalog
- `SPRINT1_AI_BATCH_PLAN.md` (6.9 KB) — methodology
- `property_map_v2_data_sources.md` (38 KB) — research sources
- `property_map_v2_tooling.md` (37 KB) — research tooling
- `r38_san_bernardino_targets.md` (9 KB) — research findings

**Proposed reorg:**
```
docs/research/
├── README.md                       (synthesis index)
├── METHODS/
│   ├── EXECUTION.md
│   └── SPRINT1_AI_BATCH_PLAN.md
├── SOURCES/
│   ├── REPO_CATALOG.md
│   ├── property_map_v2_data_sources.md
│   └── r38_san_bernardino_targets.md
├── TOOLING/
│   ├── BLENDER_GIS_3D_LANDSCAPE_RESEARCH.md
│   ├── property_map_v2_tooling.md
│   ├── ASSET_RESEARCH_2026-06-13.md
│   └── 5_ONDERWERPEN_MATERIALS.md
└── RESULTS/                        (existing 107 files + the 27 KB construction prices NL)
    └── 2026-06-30_construction_prices_paraguay_nl.md
```

**Net:** Better mental model. Cost: 4 sub-dirs to navigate vs 1.

**Effort:** 30 min (mostly mechanical moves).

### 2.2 — Sub-organize `docs/site_data/` (23 subdirs)

**Current:** 23 subdirs each with 1-3 brief files.

**Proposed:** Group by purpose:
```
docs/site_data/
├── TERRAIN/             (dem, topology_lod, soilgrids, chelsa, climate_era5, chirps, mod11, mod16)
├── LAND_COVER/          (mapbiomas_paraguay, hansen_gfc, landsat, jrc_gsw, atlantic_forest_trees)
├── BIODIVERSITY/        (flora, fauna, gbif, biodiversity_25km, canopy_height)
├── SATELLITE_OBS/       (sentinel1, sentinel2, alos_palsar, osm, nasa_power, infrastructure)
└── PROPERTY/            (property_map, property_map_v2, extended_aoi, comparables, client_photos, hydrogeology, analysis)
```

**Effort:** 1 hour (23 subdir moves + brief README per group).

---

## Tier 3 — content quality (out of scope for restructure, future content work)

### 3.1 — Refresh 2026-06-10 master research to 2026-07-03

`docs/research/README.md` says "Compiled 2026-06-10" but a lot has changed
in the project since. Could be re-synthesized with:
- The post-escritura audio synthesis findings
- The Sprint 0 research results (F09, F11, F12, L05, M04, M05, M08, M22)
- The 5-yr MapBiomas sample (after pass 1)
- The 9 new datasets (CHELSA, ERA5, MOD16, MOD11, etc.)

**Effort:** 2-4 hours. Not blocking; just stale.

### 3.2 — Resolve the 30 open decisions in `_reconciled/OPEN_DECISIONS.md`

This is content work, not structure work. The 30 decisions block Phase 1.
Wes needs to weigh in (W0.1 attorney call, W0.2 Sonja call, etc. per
`people/WES_ACTIONS.md`).

**Effort:** Variable; depends on Wes's time.

---

## Tier 4 — what I would NOT touch

Same as pass 3:
- ❌ **The 510 doc-layer files** (mostly load-bearing after pass 3)
- ❌ **`lqv/` Python package** (4+ hour audit, Wes doesn't read)
- ❌ **`docs/audios/final/`** (canonical per Wes's audios)
- ❌ **`LICENSES/` 393 files**
- ❌ **18 final PNGs**

---

## What's the ROI at this point?

After pass 1+2+3 (8 commits, 1,856 files, 359 MB tracked, top-level
docs 80 → 59, idea catalog split, every "what to do" resolves to ONE
canonical doc), the repo is honestly well-organized. The remaining
work is **incremental polish, not structural reorganization**.

**Estimated value of remaining Tier 1 work:** 30-45 min for slightly
better discoverability (audios README, render_catalogue cross-refs,
research README promotion, ~15 status banners).

**Estimated value of Tier 2 work:** 1-2 hours for a research/ dir
reorg that may or may not improve navigation. Risk: creates new
"where do I look?" questions.

**Recommendation:** Do Tier 1.5 (status banners) — it's mechanical
and prevents future Wes-confusion. Skip Tier 2 unless the
reorg has a clear use case. Defer Tier 3 (content quality) until
Wes's next interaction.

---

*Generated by Erebus · 2026-07-03 · after pass 3 (commit f4dccd2).*
*See RESTRUCTURE_PASS_3_RECOMMENDATIONS.md for what pass 3 did.*
*See RESTRUCTURE_PASS_2_RECOMMENDATIONS.md for what pass 2 did.*