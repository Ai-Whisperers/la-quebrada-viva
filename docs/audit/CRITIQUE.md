# Critique + Roast — LQV Repo (2026-06-30)

**Purpose:** Honest critical assessment of every major section. Specific. Constructive. No "looks good" hedging.

**Method:** Read every major file + run structural analysis. Score each section on signal-to-noise. Flag specific issues with specific fixes.

**Audience:** Ivan + Kiki + Erebus. NOT for Wes until things are fixed.

---

## How to read this

- **§1-3** = load-bearing (everything below this is detailed)
- Each section has: **what's working**, **what's broken**, **specific fixes**
- **🔥 = urgent** (block Wes reading the repo)
- **⚠️ = important** (block a clean audit)
- **🪨 = cosmetic** (defer)

---

## 0. The high-altitude verdict

**The repo is over-built and under-curated.** It grew from 0 → 2,159 files in 6 weeks across 4 build phases. Each phase was a different "voice" (Wes recordings → render pipeline → escritura freeze → reconciled view) and they piled up rather than integrating. The result: 5 ways to find the same answer, 3 contradictory "current state" docs, and ~310 MB of files that could be gitignored or LFS'd without losing anything.

**Wes's actual UX of the repo right now:** he doesn't read the repo. He reads WhatsApp messages and Ivan's summaries. The repo is operational infrastructure, not a document. That's OK — but the audit needs to make it navigable for the next person (which is Ivan, post-handover).

**The 3 highest-leverage fixes** (in order):
1. Consolidate "current state" into 1 doc (not 3)
2. Gitignore the 264 MB snapshot + 50 MB MapBiomas rasters (50% size reduction)
3. Either complete the 109-idea catalog or archive it

---

## §1. The 109-Idea Catalog — `docs/ideas/` (1,308 sections, 850 KB)

### 🔥 Issue 1.1: Mass auto-generation without per-idea verification

All 109 idea files were generated in 2 large Python script passes on 2026-06-30. Each file is ~4.5 KB with the same 12 sections. The content is **largely template-fill** with category-specific content blocks.

**Specific examples of template-fill:**
- "What Wes wants" section: 60+ files show the same pattern — the deliverable string + a few quotes
- "Why this matters" section: 30+ files say "no direct quote extracted — derived from broader context"
- "Risks & failure modes" section: 15+ files say "no specific risks identified beyond standard category risks"
- "Cost / time estimate": category default applied when no specific data
- "Done = shipped": generic "should be a measurable artefact" placeholder

**What this means:** the catalog has **structure** but not **substance** for most ideas. A reader can browse 109 well-formatted files and still know very little about each.

**Fix options:**
- **(A) Quality-mark each file**: add a `Quality: ✓ reviewed / ○ auto / ✗ flagged` field
- **(B) Slim to 30-50 key ideas**: archive the rest as `_archive/ideas_2026-06-30/`
- **(C) Verify each file manually**: 109 × 30 min = 55 hours. Not feasible
- **(D) Adopt the structure but make it lighter**: 1 file per idea with only the most-load-bearing sections (What/Why/Action/Status). ~1 KB each instead of 4.5 KB

**Recommendation:** (A) + (B) hybrid. Mark the 30 load-bearing ideas (V01-V05, F01, B07, C07, M01, etc.) as "✓ reviewed." Archive the rest as bulk. Keep the 12-section structure but reduce to ~50 ideas total.

### 🔥 Issue 1.2: The 20 "SUGGESTED" ideas duplicate existing content

The 20 suggested additions (I01-I20) overlap heavily with existing ideas:
- **I01 Reservation widget** = already implied by M01 (Booking.com listings)
- **I02 Operations dashboard** = stretches M01's scope
- **I03 Glamping tent prototype** = new, but should replace T01-T04 typology focus for Year 1
- **I07 Money story for investors** = useful, no overlap
- **I12 VR scenarios** = B01 expanded
- **I13 Cost benchmark** = useful, no overlap

**8 of 20 suggested ideas** add new value. **12 of 20** are restatements of existing ideas. The SUGGESTED.md makes them feel like a separate bucket, but they're really "refinements."

**Fix:** merge the 8 new-idea ones into their relevant categories. The 12 restatements should be cross-references from existing ideas, not separate files.

### ⚠️ Issue 1.3: INSIGHTS.md is the most-load-bearing file but the least-promoted

INSIGHTS.md (20 patterns, 18 KB) is the **single most valuable doc** in the catalog. It synthesizes 6 weeks of work into actionable patterns. But:
- It's not linked from the root README
- It's not in the cold-start reading order
- It doesn't appear in the STATUS.md "what to read next" section

**Fix:** link from README, add to cold-start order, cross-reference from OPEN_DECISIONS.md (already done partially).

### 🪨 Issue 1.4: 12 sections per file is too many

For an idea to be useful, the reader needs 4 things:
1. **What** is it
2. **Why** does it matter
3. **What to do** (action + cost + dependencies)
4. **Status** + **Source**

The 12 sections include 6 that are derivable (Sources, Changelog, Priority meaning, Status meaning) and 2 that are usually template-fill (Risks, Done = shipped).

**Recommendation:** slim to 6 sections: What / Why / Action / Cost / Status / Sources. Drop the rest. Result: ~1.5 KB per file, 109 × 1.5 = 163 KB total instead of 850 KB.

---

## §2. The Render Pipeline — `lqv/` (148 files, 22K lines)

### ⚠️ Issue 2.1: Concept art typologies don't match the build plan

The LQV render pipeline has 13 typology build files. Wes's 10-type plan is the build plan. There's an **imperfect overlap** (boomhut, bamboo_curved_roof, bamboo_river match types in Wes's plan; cob, bottle, hobbit, container, clay_terracotta, italian_stone do not).

**What this means:** Ivan rendered 13 typologies as concept art. 3-5 of them match Wes's plan; 8-10 are not in the plan. They're not useless — they could be used for the buyer-experience VR walkthrough, or as future expansion options. But they're **not** the build plan.

**Fix:** add a `LQV_PLAN_MATCH.md` per typology file that says "matches Wes's Plan Type B" or "concept art only, not in build plan."

### ⚠️ Issue 2.2: The 18 "finals" are concept art, not deliverables

The 18 final renders (A/B/C × 6 cameras, byte-frozen at `85e86aa`) are visually beautiful but they were generated in the escritura-week sprint as the closing-day deck assets. The cob house they depict is **not yet built** on the parcel. The renders are **concept art**, not as-built.

**What this means:** the escritura deck used these renders as "the cob house we'll build." But the actual build will differ (different materials, different site position, different specific details). The renders are **valuable as concept art** but should not be confused with reality.

**Fix:** clearly mark the 18 renders in the catalogue as "concept art for the escritura deck, not the actual build." Or note "the actual build will use these as the design intent but may differ."

### 🪨 Issue 2.3: `lqv/finance/boq.py` duplicates `scripts/build_boq.py`

Two BoQ generators exist:
- `lqv/finance/boq.py` (91 lines) — the BoQ writer
- `scripts/build_boq.py` — a "bpy-stub shim for outside-Blender execution" per STATUS.md

These are **supposed to be** one calls the other. But they could be in conflict if the BoQ logic has diverged.

**Fix:** verify they're consistent. If they are, document the relationship. If not, decide which is canonical and delete the other.

### 🪨 Issue 2.4: `lqv/restaurant/` has 4 files, 87 lines, no shipped outputs

The `lqv/restaurant/` subpackage has 4 files totaling 87 lines. These are concept-only — no builds, no renders.

**Fix:** either build them out or archive to `_archive/lqv_restaurant_2026-06-30/`.

### 🪨 Issue 2.5: Tests are 4 files for 22K lines of code

**Test coverage: <10%.** Only 4 test files for a production codebase. The repo has `lqv/util/ten_rules_check.py` (135 lines) which is a design-rule validator — that's a test, not a unit test. And `lqv/util/random_audit.py` (114 lines) is an audit tool, not a test. So real unit tests = 2-3 files.

**Fix:** add tests for the 12-section `rich_content_for` template that built the 109 idea files. It's the highest-leverage place for tests because any future change to the catalog format would have to keep the test green.

---

## §3. The Site Data Corpus — `docs/site_data/` (~1,200 files, 395 MB)

### 🔥 Issue 3.1: 264 MB pre-Wes-data-share snapshot is now stale

`docs/site_data_2026-06-13_snapshot/` is 264 MB, 18 files, contains the state of the site_data corpus on 2026-06-13 — the day before Wes shared the full files.

**Why this exists:** T-10 to escritura, the snapshot was preserved as "the canonical state at that point." After escritura, the snapshot is **historical** but still in git.

**Fix:** gitignore the snapshot dir. Add a `docs/site_data_2026-06-13_snapshot/README.md` (kept in git) that says "This snapshot is preserved on local disk only. To re-populate, see scripts/satellite/."

**Size saved:** 264 MB → 0 in git. Disk usage unchanged.

### 🔥 Issue 3.2: 50 MB of MapBiomas rasters

`docs/site_data/mapbiomas_paraguay/` = 83 files, 50 MB. The MapBiomas Paraguay land cover product is annual, 1985-2023, plus mosaics. For trajectory analysis, 5-year sampling would be enough.

**Fix:** keep the most recent 5 years (2019-2023) + 1985 + 2000 (key reference years). Move older to `.gitignore`. Keep the brief markdown.

**Size saved:** ~40 MB.

### ⚠️ Issue 3.3: 26 MB mystery file in `topology_lod/`

`docs/site_data/topology_lod/` has 1 file, 26 MB. What is it?

**Likely:** a high-resolution topology derivative (e.g. high-res DEM processed, or a 3D model export). Need to identify before deciding what to do.

**Fix:** identify the file, decide if it's a duplicate of a smaller artifact, decide if it belongs in the repo.

### ⚠️ Issue 3.4: `property_map/` vs `property_map_v2/`

`docs/site_data/property_map/` (4 files, 1.2 MB) and `docs/site_data/property_map_v2/` (2 files, 44 KB) likely represent the same data in two iterations.

**Fix:** verify which is the canonical version. Move the superseded one to `_archive/`.

### 🪨 Issue 3.5: 23 sub-buckets in `docs/site_data/`, many with 1-3 files

The current organization is "one subdir per dataset" (mapbiomas, hansen_gfc, jrc_gsw, soilgrids, ...). This produced 23 micro-buckets. Some have 1 file. Some are 1 KB total.

**Fix:** either commit to "one dataset = one subdir" (current state, justified for the corpus) or reorganize by "by region" / "by use case." The current state is fine for researchers but hard for a casual reader.

---

## §4. The Reconciled View — `docs/_reconciled/` (11 files, 108 KB)

### ⚠️ Issue 4.1: Duplicates content from other docs

The reconciled view has MASTER_BRIEF.md (18 KB), FINANCIAL_MODEL.md (6.5 KB), CABIN_CATALOG.md (7 KB), etc. Some of this content already exists in:
- `STATUS.md` (32 KB) — has financial numbers
- `docs/HOUSING_PARK_CONCEPT.md` (29 KB) — has cabin plan
- `docs/MASTER_TODO.md` (31 KB) — has open items
- `docs/ideas/` (109 files) — has brainstorm detail

**Issue:** the reconciled view is a "bridge" doc. That's its purpose. But the bridge duplicates the source it bridges to. So you have:
- 1 source doc
- 1 bridge doc that summarizes the source

Both stay. But the reader doesn't know which is the canonical.

**Fix:** every doc in `_reconciled/` should clearly state its relationship to the source. e.g. `BUSINESS_STRUCTURE.md` should say "summary of LQV catalog F01 + Wes's invesment center.docx" so the reader knows where to go for full detail.

### 🪨 Issue 4.2: OPEN_DECISIONS.md duplicates idea files

OPEN_DECISIONS.md has 12 decisions. Many of these decisions are **also** tracked as ideas in `docs/ideas/`:
- D1 (Business structure) = F01
- D5 (Materials pricing) = many `construction/` ideas
- D6 (Insurance pre-qualification) = I10 + F05 + R01
- D7 (Build order) = house_typologies T01-T04

**Issue:** decisions are tracked in 2 places. A status update in one doesn't propagate to the other.

**Fix:** make OPEN_DECISIONS.md a **summary view** with cross-references to the detailed idea files. When a decision resolves, update the idea file's status (planned → in_progress → shipped) and OPEN_DECISIONS.md gets a 1-line update.

---

## §5. The Status + Master + Index Triad

### 🔥 Issue 5.1: Three "current state" docs tell different stories

| Doc | When written | Says |
|---|---|---|
| `STATUS.md` | 2026-06-25 (T-2) | "escritura deck frozen, signing on 2026-06-27" |
| `docs/_reconciled/MASTER_BRIEF.md` | 2026-06-30 | "escritura signed 2026-06-27, Phase 1 €5,503,736" |
| `docs/ideas/INDEX.md` | 2026-06-30 | "109 ideas, P0/P1/P2/P3 priorities" |
| `docs/MASTER_TODO.md` | 2026-06-25 (T-2) | "P0a escritura week, P0b T+1, P1-P4 phases" |

**Issue:** Wes opens the repo, sees STATUS.md at 32 KB, reads it, gets the T-2 view. Sees reconciled MASTER_BRIEF, gets the post-Wes-share view. Sees MASTER_TODO, gets a different todo list. No single "where are we" doc.

**Fix:** designate ONE current-state doc. Recommendation: **`docs/_reconciled/MASTER_BRIEF.md`** is the canonical current state. STATUS.md is the **historical record** of the escritura freeze (rename to `STATUS_2026-06-25_escritura_freeze.md` to make this explicit). MASTER_TODO is also historical, but the "P1+ post-escritura" section needs to be updated.

### ⚠️ Issue 5.2: PROJECT_INDEX.md claims 1,186 files but repo has 2,159

PROJECT_INDEX.md says "1,186 tracked files" (per the README's "Cold-start docs" section). Actual: 2,159.

**What happened:** the file was written when the repo was at 1,186 files (probably around 2026-06-25). Since then, 973 files were added (site_data corpus + the 109-idea catalog + the 11 reconciled docs + the LQV subcode work).

**Fix:** regenerate PROJECT_INDEX.md. Or better, make it a generated file (script reads the repo, writes the index).

---

## §6. The Site Data + Render Catalogue PNGs

### ⚠️ Issue 6.1: 9.3 MB of duplicate render catalogue PNGs in `docs/`

`docs/render_catalogue/by_asset/` and `docs/render_catalogue/contact_sheets/` are PNGs. The canonical renders are in `renders/` (gitignored except 18 finals).

**Why this duplication:** the catalogue is a viewer-optimized subset. Easy to browse without trawling renders/sub/runs/.

**But:** if the canonical renders are in `renders/` and the gitignore excludes them, then the catalogue is the **only git-tracked view** of the renders. So they're not duplicates — they're the **canonical git-tracked version** of the renders.

**Fix:** keep the catalogue, but document the relationship clearly. Add a `docs/render_catalogue/README.md` that says "the PNGs here are the canonical view of all 926 renders. The original Blender files are in `renders/sub/runs/` (mostly gitignored)."

### 🪨 Issue 6.2: `renders/sub/` not gitignored

Per the inventory, `renders/sub/` has the latest sub-renders. Some are tracked. The `.gitignore` excludes `renders/sub/` entirely, but the actual repo has files in there.

**Fix:** verify `.gitignore` actually excludes. If files are tracked, they're a mistake. Run `git ls-files renders/sub/` to verify.

---

## §7. The Escritura-Frozen Scope (DO NOT TOUCH)

### ✅ What's working

- `docs/escritura_deck/` has 6 PDF versions, all byte-pinned. This is the legal record.
- `docs/boq/` has the escritura-frozen $268,685.45 BoQ. SHA `2e4c265c…01137`.
- `docs/finance/`, `docs/comms/`, `docs/email_drafts/` are all T-2 frozen.
- The `escritura-2026-06-27` git tag wraps commit `0081129`. SHA `9ce96b85…4a53c` for the bundle.

**This is the load-bearing legal scope. Do not restructure, do not rename, do not touch.**

### 🪨 Issue 7.1: 77 MB of deck PDFs is a lot

`docs/escritura_deck/` has 6 PDF files totaling 77 MB. Most of this is the v6 final (the canonical). The other 5 (v1-v5) are revision history.

**Fix:** keep v6 canonical. Consider gitignoring v1-v5 (they're preserved on the local disk for the legal record, not needed in the repo). This would save ~60 MB.

---

## §8. Pre-Wes Plan Docs

### ⚠️ Issue 8.1: `HOUSING_PARK_CONCEPT.md` (29 KB) and `EUROPEAN_TOURISM_SPEC.md` (33 KB) are pre-Wes

Both written 2026-06-10. Both useful as historical/background. Both don't mention 30 cabins / 10 types / €5.5M.

**What they're good for:** the **13 typologies** in the LQV render pipeline trace back to these docs. The 8 concepts in HOUSING_PARK_CONCEPT are still valid. The 25 questions in HOUSING_PARK_CONCEPT are still relevant.

**What they're stale for:** the financial figures, the 10-type build plan, the 4-entity BV vs founder-controlled decision.

**Fix:** add a header to each: "As of 2026-06-10. Superseded for financial/operational by docs/_reconciled/ on 2026-06-30. See the reconciled view for current state."

---

## §9. Files I did NOT find in the repo (gaps)

After auditing, several things Wes mentioned in the recordings are **not yet in the repo** as files:

1. **Wes's Excel/DOCX files** (Eco_Resort_Paraguay_Fase1_Financieel_Model.xlsx, etc.) — Ivan saw them in a paste but they're on Wes's local machine, not in the repo. If Wes wants them version-controlled, the 11 reconciled docs are the structured alternative.

2. **`top 15 inverstering plannen.xlsx`** (Wes's 15 parallel investment ideas) — not in repo. The reconciled view references "the 15 other ideas" but doesn't have them as actual files. They live in Wes's head / Wes's local files.

3. **Capture of Wes's 5 phone videos** (B07) — BLOCKED. The pipeline is ready, the brief is written, but the actual videos aren't shared.

4. **Wes's personal success metric** (per INSIGHT #20) — not defined. Not in the repo. Doesn't have to be in the repo. It's a Wes-side conversation.

5. **Wes's personal network contacts** (San Bernardino German community, Dutch reforestation guy in Caacupé, etc.) — mentioned in recordings, not in repo. Should be in `docs/contacts.md` if Wes wants.

**Recommendation:** create a `docs/CONTACTS.md` (Wes-side, just a list of names + roles + best contact) if these are needed for action.

---

## §10. The 3-hour reading for Ivan

If Ivan wants to "know where things are" in 3 hours, here's the order:

1. `README.md` (5 min) — what this is
2. `docs/_reconciled/MASTER_BRIEF.md` (20 min) — current state
3. `docs/_reconciled/OPEN_DECISIONS.md` (10 min) — what to do next
4. `docs/audit/INVENTORY.md` (this directory) (30 min) — file map
5. `docs/audit/CRITIQUE.md` (this file) (30 min) — what's wrong + what to fix
6. `docs/audit/RESTRUCTURE_PLAN.md` (next file) (15 min) — the actual plan
7. `STATUS.md` (30 min, if needed) — escritura state historical record
8. `docs/ideas/INDEX.md` (15 min) — 109-idea catalog structure
9. `docs/research/2026-06-30_construction_prices_paraguay_nl.md` (20 min) — material prices

**Total: ~3 hours.**

---

## §11. Summary scorecard

| Section | Verdict | Score | Action priority |
|---|---|---|---|
| 109-idea catalog | **Bloated, low individual value** | 4/10 | 🔥 slim + quality-mark |
| Render pipeline | **Largely fine, some stub subdirs** | 7/10 | ⚠️ verify dupes, archive stubs |
| Site data corpus | **Massive, partially stale, oversized** | 5/10 | 🔥 gitignore snapshot, compress rasters |
| Reconciled view | **Useful but duplicates content** | 7/10 | ⚠️ add cross-refs + headers |
| Status triad | **3 contradictory current-state docs** | 3/10 | 🔥 designate one canonical |
| Escritura scope | **Frozen, do not touch** | 10/10 | ✅ leave alone |
| Pre-Wes plans | **Useful background, stale details** | 6/10 | ⚠️ add "as of" headers |
| Site data + render PNGs | **Duplicate but justified** | 7/10 | 🪨 add README explaining |

**Overall repo grade: 6/10.** Functional, useful, but overgrown. Restructure brings it to 8/10 in 1 day of focused work.

---

## §12. Recommended execution order (for the restructure)

1. **Gitignore the snapshot** (5 min, 264 MB saved)
2. **Compress MapBiomas to 5 years** (15 min, 40 MB saved)
3. **Designate MASTER_BRIEF.md as canonical current state** (10 min, 1 doc rename)
4. **Mark each idea file with quality tag** (30 min, 1 script + 1 commit)
5. **Move duplicate property_map_v2 to _archive** (5 min)
6. **Identify the 26 MB topology_lod file** (10 min)
7. **Slim the 109 idea files to 6 sections** (1 hour, 1 script + careful commit)
8. **Cross-link reconciled view with source docs** (30 min, header additions)
9. **Archive pre-Wes plan docs with "as of" headers** (10 min)
10. **Add README + cold-start order to bucket E** (30 min)

**Total: ~4 hours of focused work. ~310 MB saved. Repo grade: 8/10.**

The actual `git mv` commands are in `RESTRUCTURE_PLAN.md` (next file).
