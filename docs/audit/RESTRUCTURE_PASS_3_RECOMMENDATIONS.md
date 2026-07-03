# Restructure Pass 3 — Open Recommendations (2026-07-03)

> **For Ivan + Erebus next session.** After pass 1 (−337 MB, 109 idea
> files quality-marked) and pass 2 (12 moves, 80 → 63 top-level docs),
> here's what's still on the table. Lower-priority than pass 1+2 but
> still worth doing if Ivan wants the repo fully polished.

## Repo state (post-pass 2, verified on origin/master)

```
1,854 tracked files, 359.2 MB tracked
├── docs/          510 md files (after pass 2: 63 top-level + 9 in people/ + subdirs)
├── lqv/           ~250 py files
├── LICENSES/      393 verbatim text files
├── renders/       21 PNG files (18 finals + 3 demo)
└── (everything else: configs, scripts, tests, data, .claude)
```

---

## Tier 1 — clear wins (do these next session)

### 1.1 — Archive `docs/patches/` (already applied)

**Problem:** `docs/patches/HOUSING_PARK_CONCEPT_audio_deltas.md` (7.8 KB)
and `docs/patches/RESEARCH_GAPS_R39-R50_audio_deltas.md` (5.2 KB) were
**patch files describing edits that have already been applied** (commits
3ceca61 / 3806b5c). They have no current value — they're instruction
documents that have been completed.

**Recommended action:** Move both to `docs/_archive/2026-06-30_session/patches/`
+ a 1-line `MANIFEST.md` explaining they were applied.

**Net effect:** -13 KB from canonical docs/. One less source of
"is this applied or not?" confusion.

### 1.2 — `docs/REPO_STRUCTURE.md` (14 KB) is a structural doc nobody indexes to

**Problem:** `REPO_STRUCTURE.md` was authored 2026-06-30 to describe
the repo's post-implementation-pass layout. Now that pass 2 has
moved 12 files around, this doc is **factually stale** (it still
talks about `docs/WES_TODO.md`, `docs/WES_5_THIS_WEEK.md`, etc.
being at the top of `docs/`).

**Recommended action:**
- Either: refresh `REPO_STRUCTURE.md` to reflect current layout
- Or: archive it (move to `_archive/2026-06-30_session/`) since
  `docs/INDEX.md` + `WES_INDEX.md` + `STATUS.md` already serve
  the navigation role

**Recommendation:** Archive. Three navigation docs (INDEX + WES_INDEX
+ STATUS) is enough; a fourth creates more confusion than it solves.
Add a 1-line note to `docs/INDEX.md` Tier -1 explaining the move.

### 1.3 — `docs/MASTER_TODO.md` (31 KB) is the old 2026-06-25 master plan

**Problem:** `MASTER_TODO.md` is a 4-tier P0a/P0b/P1-P4 + cross-cutting
tracker from 2026-06-25 (T-2 to escritura). It's the **most-detailed
TODO ever written for this project** (31 KB, every item tagged with
owner + gate + ETA), but it predates:
- The 2026-06-27 escritura signing (P0a is closed)
- The 2026-06-30 audio synthesis (5 new domains, 95 new ideas)
- The 2026-07-03 restructure (12 file moves)

**Recommended action:**
- Move to `_archive/2026-06-30_session/MASTER_TODO_escritura_week_2026-06-25.md`
- Top-level `MASTER_TODO.md`: rewrite as 1-line stub pointing at
  `POST_ESCRITURA_NOW.md` (canonical current TODO)

**Net effect:** -31 KB from canonical docs/. The "what to do" is now
POST_ESCRITURA_NOW (5 hard gates) + WES_INDEX (Wes-track 5 actions).

### 1.4 — `docs/T_PLUS_1_DEBRIEF.md` (4.7 KB) is a one-off session note

**Problem:** Single-session retrospective from 2026-06-28. Not
referenced anywhere, not a current artefact.

**Recommended action:** Move to `_archive/2026-06-30_session/`.

### 1.5 — `docs/PR_BACK_TO_BASE.md` (4.6 KB) — git/PR workflow note

**Problem:** PR-back-to-base workflow doc. Not relevant to the
project; only relevant to repo maintenance.

**Recommended action:** Move to `_archive/` (one-time maintenance note).

### 1.6 — `docs/OCTAVA_VENDOR_TRACKER.md` (4.6 KB) — single-vendor tracker

**Problem:** Tracks a single vendor relationship. Could stay
(canonical vendor docs are useful) or be archived.

**Recommended action:** Keep, but add header banner pointing to
`docs/research/RESULTS/F18_AI_operations.md` for the broader
AI-ops-vendor context.

---

## Tier 2 — bigger restructures (debatable)

### 2.1 — Archive the 46 `○ auto-fill` idea files

**Problem:** 46 of the 109 idea files are marked `○ auto-fill`
(template structure, no Wes substance). They're honest placeholders
but they bloat `ls docs/ideas/` and confuse readers who don't
read the Quality field.

**Recommended action:** Move the 46 `○ auto-fill` files to
`docs/ideas/_archive/2026-06-30_autofill/` + a manifest.

**Tradeoff:** Reduces ideas/ from 109 → 63 files (matching the
63 ✓ reviewed). Easier to navigate. But the auto-fill files
might still be useful as "what we considered" even if not
fully fleshed out.

**Net effect:** ~140 KB moved. 46 fewer files in the canonical
ideas/ tree. `INDEX.md` updated to point at archive.

### 2.2 — `docs/research/` top level has 13 dated files that may overlap with `RESULTS/`

**Files in `docs/research/` (top level):**
- `2026-06-10_vegetation_3d_research.md` (22 KB) — pre-implementation research
- `2026-06-30_construction_prices_paraguay_nl.md` (27 KB) — single 27 KB ref doc
- `5_ONDERWERPEN_MATERIALS.md` (3.7 KB) — Wes's 15-materials picker
- `ASSET_RESEARCH_2026-06-13.md` (12 KB) — asset-pipeline research
- `BLENDER_GIS_3D_LANDSCAPE_RESEARCH.md` (26 KB) — Blender+GIS tooling
- `EXECUTION.md` (6 KB) — execution tracker
- `GEDI_L2A_RESEARCH.md` (20 KB) — GEDI data research
- `README.md` (11 KB) — research synthesis index
- `REPO_CATALOG.md` (23 KB) — 141 GitHub repos catalog
- `SPRINT1_AI_BATCH_PLAN.md` (6.9 KB) — research sprint plan
- `property_map_v2_data_sources.md` (38 KB) — property map v2 sources
- `property_map_v2_tooling.md` (37 KB) — property map v2 tooling
- `r38_san_bernardino_targets.md` (9 KB) — San Ber supply chain

**Plus `docs/research/RESULTS/` (107 files, 652 KB).**

**Problem:** Some of these are catalogues of what to research, others
are the research results, others are tooling. Mixed into the same dir.

**Recommended action:** Sub-organize `docs/research/` into:
- `docs/research/SOURCES/` (the 141-repo catalog, vegetation research,
  construction prices NL — what to research)
- `docs/research/METHODS/` (EXECUTION.md, SPRINT1_AI_BATCH_PLAN.md,
  GEDI_L2A_RESEARCH.md — how to research)
- `docs/research/RESULTS/` (unchanged — 107 files of answered research)
- `docs/research/TOOLING/` (BLENDER_GIS, property_map_v2_*, ASSET_RESEARCH)

**Tradeoff:** Better mental model. But 4 sub-dirs to navigate vs 1.
The current single-dir layout is fine if RESULTS/ is treated as the
"answer" and the top-level as "questions/methods". Could also just
keep flat + better cross-linking.

### 2.3 — `docs/_reconciled/IDEAS_CATALOG_PATCH_PLAN.md` is itself a patch plan

**Problem:** This 5 KB doc from 2026-06-30 says "this is the patch
plan for the ideas catalog — do it later." The Quality-marking pass
already addressed half of what it suggested. The remaining 4 items
(AH auto category, cross-link to research-catalogue, V01 update, V02
update) are 4-6 hours of Erebus work that the doc itself recommends
deferring until W0.1-W0.7 actions resolve.

**Recommended action:** Move to `_archive/2026-06-30_session/`
+ add a pointer in `docs/ideas/INDEX.md` noting the patch plan was
addressed (Quality mark) and the remaining items are deferred.

---

## Tier 3 — quality cleanup (low ROI, high polish)

### 3.1 — `docs/render_catalogue/by_asset/` (53 files, 230 KB)

**Problem:** Each render asset has its own 4-7 KB markdown file in
`by_asset/`. The metadata is also in `INDEX.md` (22 KB) and
`catalogue.json` (343 KB). Three views of the same data.

**Recommended action:** Keep all three (they serve different uses:
`INDEX.md` for humans, `catalogue.json` for tooling, `by_asset/` for
per-asset drill-down). Add cross-reference at the top of each.

### 3.2 — `docs/audios/drafts/` (5 audio dirs, ~600 KB raw transcripts)

**Problem:** Raw audio drafts (segments.jsonl + raw.txt + meta.json)
for each of the 5 audios. These are the source data; `final/` has
the cleaned synthesis. The drafts are valuable provenance but are
600 KB of mostly-timestamped JSONL.

**Recommended action:** Add `docs/audios/drafts/README.md` explaining
what's here, what was extracted, and how to re-run transcription.
Keep as-is.

### 3.3 — Empty `splats/research/` dir

**Problem:** Empty dir at `splats/research/`. Doesn't serve a purpose
without content.

**Recommended action:** Either populate with research notes about
3DGS (Gaussian Splatting) pipeline, or delete.

### 3.4 — `docs/TERRAIN_PIVOT.md` (37 KB) and `docs/REPO_RESEARCH_100.md` (31 KB)

**Problem:** Two large top-level docs. `TERRAIN_PIVOT.md` is about
the design decision to render terrain (not just house); `REPO_RESEARCH_100.md`
is about 100 repos evaluated. Both are useful but bulky.

**Recommended action:** Verify they're referenced from `docs/research/README.md`
or `docs/INDEX.md`. If not, add forward-refs.

### 3.5 — `docs/_archive/2026-06-1X/` has 8 files that could merge

Already noted in RESTRUCTURE_PASS_2_RECOMMENDATIONS.md §3.1.
Three CRITIQUE variants (180 KB total) could collapse to one
`CRITIQUES_HISTORY.md`.

### 3.6 — `docs/GAPS_ANALYSIS.md` (35 KB) vs `docs/RESEARCH_GAPS.md` (23 KB)

**Problem:** Two gap-analysis docs. `GAPS_ANALYSIS.md` is from
2026-06-04 (pre-Wes-share, escritura-week scope); `RESEARCH_GAPS.md`
is the post-Wes-share, post-audio-synthesis tracker (R39-R50 added).

**Recommended action:** Either:
- Archive `GAPS_ANALYSIS.md` (pre-Wes, superseded by RESEARCH_GAPS)
- Or: merge into `RESEARCH_GAPS.md` if there's content not yet captured

**Likely verdict:** Archive. `RESEARCH_GAPS.md` is the canonical
tracker per `CLAUDE.md` document map.

---

## Tier 4 — what I would NOT touch

- ❌ **510 doc-layer files** (mostly load-bearing after pass 2)
- ❌ **`lqv/` Python package** (4+ hour audit, Wes doesn't read)
- ❌ **`docs/audios/final/`** (canonical per Wes's audios, do not modify)
- ❌ **`LICENSES/` 393 files** (verbatim legal mirror)
- ❌ **18 final PNGs** (byte-frozen at `85e86aa`)
- ❌ **`docs/_reconciled/`** (only added cross-link section; content stays)

---

## Recommended next session order

If Ivan wants to do Tier 1 in one pass (15-20 min):

1. Tier 1.1: Move 2 `docs/patches/` files to `_archive/2026-06-30_session/patches/`
2. Tier 1.2: Move `REPO_STRUCTURE.md` to `_archive/`
3. Tier 1.3: Move `MASTER_TODO.md` to `_archive/`, replace with 1-line stub
4. Tier 1.4: Move `T_PLUS_1_DEBRIEF.md` to `_archive/`
5. Tier 1.5: Move `PR_BACK_TO_BASE.md` to `_archive/`

**Estimated time:** 15-20 min (mostly `git mv` + 1-line stubs + 1 commit).

**Estimated outcome:**
- Top-level docs: 63 → ~58 (down to canonical only)
- Total "_archive" docs: 21 → 25
- MASTER_TODO + REPO_STRUCTURE + the 3 patches/one-offs no longer
  compete with POST_ESCRITURA_NOW + WES_INDEX as the canonical
  "what to do" / "where to navigate"
- All Tier 1 moves preserve history (git mv)

If Ivan also wants Tier 2 in the same session (45 min total):
- Tier 2.1: Archive 46 auto-fill idea files (10 min, mostly mechanical)
- Tier 2.3: Archive IDEAS_CATALOG_PATCH_PLAN.md (1 min)
- Tier 3.6: Archive GAPS_ANALYSIS.md (1 min)

**Net if Tier 1+2+selected Tier 3 done:**
- Top-level docs: 63 → ~58
- Ideas/: 109 → 63 files (matches the 63 ✓ reviewed)
- Dated/orphan docs: 5 fewer in canonical paths
- Cognitive load of "which is current?" reduced by ~30%

---

*Generated by Erebus · 2026-07-03 · after pass 2 (commits dd7b6fa).*
*See RESTRUCTURE_PASS_2_RECOMMENDATIONS.md for what was done in pass 2.*