# Restructure Pass 2 — Open Recommendations (2026-07-03)

> **For Ivan + Erebus next session.** After the 2026-07-03 restructure
> pass (4 commits, −337 MB tracked), here's what's still on the table.
> Each item has a size estimate + a clear "should we?" call.
>
> Created by Erebus after inventorying the post-restructure repo.

## Repo inventory (post-restructure)

```
1,850 tracked files, 359.2 MB tracked
├── docs/          510 md files (the doc layer)
├── lqv/           ~250 py files (the 3D rendering code)
├── LICENSES/      393 verbatim text files
├── renders/       21 PNG files (18 finals + 3 demo)
└── (everything else: configs, scripts, tests, data, .claude)
```

The doc layer is now ~510 .md files. Several clusters of duplication
remain. Below is the prioritized cleanup list.

---

## Tier 1 — clear consolidation wins (do these)

### 1.1 — Consolidate 12 "what to do this week" / status / plan docs → 3

**Problem:** The post-escritura + audio-synthesis work spawned ~12
overlapping "what to do next" / "current state" / "implementation
status" docs. None of them reference each other. All compete for
the same mental slot.

| File | Lines | Real role |
|---|--:|---|
| `docs/WES_TODO.md` | 468 | Running research+decisions+actions TODO |
| `docs/WES_5_THIS_WEEK.md` | 126 | "5 things this week" consolidated |
| `docs/WES_TODO_UPDATE.md` | 204 | Status log of WES_TODO |
| `docs/POST_ESCRITURA_NOW.md` | 105 | **2026-07-03 — canonical** |
| `docs/PRIORITIES_NEXT.md` | 114 | Critical items (superseded by POST_ESCRITURA_NOW) |
| `docs/WES_INDEX.md` | 151 | **2026-07-03 — canonical** (links to people/WES_ACTIONS.md) |
| `docs/CRITICAL_PATH.md` | 204 | Visual dep graph |
| `docs/TIMELINE.md` | 151 | 3-year build schedule |
| `docs/STATUS_REPORT.md` | 217 | Pre-2026-06-30 implementation summary |
| `docs/IMPLEMENTATION_COMPLETE.md` | 196 | Pre-2026-06-30 final summary |
| `docs/IMPLEMENTATION_PROGRESS.md` | 268 | Pre-2026-06-30 running log |
| `docs/FINAL_SUMMARY.md` | 181 | Pre-2026-06-30 final summary |

**Recommended action:**
- **Move to `docs/_archive/2026-06-30_session/`:**
  - WES_TODO.md, WES_5_THIS_WEEK.md, WES_TODO_UPDATE.md (superseded by WES_INDEX + WES_ACTIONS)
  - STATUS_REPORT.md, IMPLEMENTATION_COMPLETE.md, IMPLEMENTATION_PROGRESS.md, FINAL_SUMMARY.md (closed-session snapshots)
  - CRITICAL_PATH.md (visual, may want to keep if diagrams are useful)
  - TIMELINE.md (still useful as reference; keep but add header pointing at POST_ESCRITURA_NOW)
- **Keep at top level:** WES_INDEX.md, POST_ESCRITURA_NOW.md, CRITIQUE_FOR_WES.md, STATUS.md
- **Move to `docs/people/`:** 4ENTITY_BV_CASCADE.md (Wes-relevant, belongs with WES_ACTIONS.md)

**Net effect:** 8 files moved to `_archive/`, 2 moved to `people/`,
top-level doc count drops from 80 → ~70. The confusion of "which is
the current TODO?" goes away because there's only one: POST_ESCRITURA_NOW +
WES_INDEX + WES_ACTIONS.

**Size:** ~150 KB moved. No file deletions (history preserved in `_archive/`).

### 1.2 — Add forward-references from `docs/INDEX.md` to the new Wes-track nav

**Problem:** `docs/INDEX.md` (5.9 KB, Tier 0-6 cold-start nav for devs)
was last updated 2026-06-25 (escritura week) and doesn't know about
the new Wes-facing docs (`WES_INDEX.md`, `POST_ESCRITURA_NOW.md`,
`CRITIQUE_FOR_WES.md`).

**Recommended action:** Add a top section to `docs/INDEX.md`:

```markdown
## Tier 0 (2026-07-03) — post-restructure pointers

> If you (or your stakeholder) is **Wes**, open `WES_INDEX.md` instead.
> If you're looking for **what blocks Phase 1 right now**, open
> `POST_ESCRITURA_NOW.md`.
> If you want to know **what's wrong with this repo**, read
> `CRITIQUE_FOR_WES.md` (Wes-facing) or `docs/audit/CRITIQUE_V2_ADDENDUM.md`
> (dev-facing).

---

[existing Tier 0-6 content]
```

**Net effect:** Wes-track docs are reachable from the existing
dev-track index. No file deletions. ~10 lines added.

### 1.3 — Move `4ENTITY_BV_CASCADE.md` to `docs/people/`

**Problem:** This 173-line doc is Wes-facing (visualizes the BV
structure that Wes needs to discuss with his attorney) but lives
at top level of `docs/`, mixed with engineering + research + status docs.

**Recommended action:** Move to `docs/people/4ENTITY_BV_CASCADE.md`
alongside `WES_ACTIONS.md` and `ATTORNEY_BRIEF.md` (same audience:
Wes + his NL+PY dual-tax attorney).

**Net effect:** Top-level docs drops 1, `people/` group becomes
the natural "stuff for the human/attorney/sonja" bucket.

### 1.4 — Move `post_escritura_one_pager.md` + `wesley_brief_onepager.md`

**Problem:** Two one-pagers for Wes at top level. `wesley_brief_onepager.md`
was the escritura-week brief; `post_escritura_one_pager.md` is the
post-signing version. They're both single-page stakeholder briefs.

**Recommended action:** Move both to `docs/people/` (rename
`post_escritura_one_pager.md` → `wesley_post_escritura_one_pager.md`
to disambiguate). Add a one-line forward-ref in `WES_INDEX.md`.

---

## Tier 2 — debatable consolidations (probably worth doing)

### 2.1 — `docs/MASTER_BRIEF.md` (33 KB) vs `docs/_reconciled/MASTER_BRIEF.md` (18 KB)

**Problem:** Two "MASTER BRIEF" docs at different locations. The
top-level one is from 2026-06-11 (pre-Wes-share, cob-house-focused);
the `_reconciled/` one is from 2026-06-30 (post-Wes-share, housing-park-focused).

**Recommended action:**
- Keep `_reconciled/MASTER_BRIEF.md` as canonical (post-Wes, has the
  housing-park scope). Add header banner pointing to it.
- Top-level `MASTER_BRIEF.md`: move to `_archive/2026-06-11_pre-Wes-share/`
  or keep but rename `MASTER_BRIEF_cob_house_v1.md` for clarity.

**Net effect:** One "MASTER BRIEF" again. Saves 33 KB if archived
+ 18 KB retained = 51 KB total in repo either way, but the cognitive
load of "which is current?" goes away.

### 2.2 — `docs/CLAUDE.md` document map is stale

**Problem:** `CLAUDE.md` (19 KB) has a "Document map — which file is
authoritative for what" section that hasn't been updated since the
restructure pass. It doesn't mention `WES_INDEX.md`,
`POST_ESCRITURA_NOW.md`, `CRITIQUE_FOR_WES.md`,
`docs/audit/CRITIQUE_V2_ADDENDUM.md`, or the new
`docs/people/` contents.

**Recommended action:** Add the new docs to the document map.

**Net effect:** Cold-start for AI sessions (Erebus next session) is
self-documenting. ~10 lines added.

### 2.3 — `docs/_reconciled/OPEN_DECISIONS.md` (13 KB) vs `docs/_reconciled/DECISIONS_LOG.md` (9 KB)

**Problem:** Two decision-tracking docs in `_reconciled/`:
- `OPEN_DECISIONS.md` — 30 open decisions owed by Wes
- `DECISIONS_LOG.md` — closed decisions (mostly "pending" still)

`docs/DECISIONS.md` (top-level, 8.9 KB) is a third decisions doc
(escritura-week, project-level). Three decision docs is too many.

**Recommended action:**
- Keep `_reconciled/OPEN_DECISIONS.md` (canonical for housing-park decisions)
- Move `_reconciled/DECISIONS_LOG.md` → `docs/people/` (Wes-facing
  decision receipts)
- Move top-level `docs/DECISIONS.md` → `_archive/2026-06-04_session/` (escritura-week decisions, frozen)

**Net effect:** Two decision docs → one. ~25 KB consolidated.

---

## Tier 3 — quality cleanups (low ROI but high polish)

### 3.1 — `docs/_archive/2026-06-1X/` has 8 files that could be merged

Files: AUTONOMOUS_PLAN.md, CRITIQUE_2026-06-10.md, CRITIQUE_2026-06-13.md,
CRITIQUE_BUILDERS_v2.md, HOUSES_REVIEW_2026-06-14.md,
IMPROVEMENT_PLAN_2026-06-13.md, MODELS_ROAST.md, UPGRADE_PLAN.md.
Combined: ~180 KB, ~3000 lines.

**Recommended action:** Leave as-is. They're intentional session
snapshots (per the audit doc's recommendations, archive session
docs are kept). If consolidation is desired, merge
CRITIQUE_2026-06-10.md + CRITIQUE_2026-06-13.md + CRITIQUE_BUILDERS_v2.md
into a single `CRITIQUES_HISTORY.md`.

### 3.2 — `lqv/finance/boq.py` no longer exists; `lqv/finance/__init__.py` is the FX rate module

**Problem:** Earlier audit (`docs/audit/INVENTORY.md`) flagged
"`lqv/finance/boq.py` (91 lines) duplicates `scripts/build_boq.py`."
When I checked, `lqv/finance/boq.py` doesn't exist anymore — only
`lqv/finance/__init__.py` (3 KB, the USD→PYG exchange rate module).

**Recommended action:** Update `docs/audit/INVENTORY.md` to reflect
current state. No file moves needed.

### 3.3 — `lqv/subscene/` has 28 sub-50-line driver stubs

**Problem:** Out of 53 files in `lqv/subscene/`, 28 are <50 lines
(mostly 27-line templates for single assets: agave, mango, pindo_palm,
tatakua, terraces, etc.). These are placeholder sub-render drivers
that haven't been filled in.

**Recommended action:** Leave as-is. They're part of the sub-render
pipeline design (`sub_render_strategy.md`); the empty ones are
intentional placeholders that get filled in when their asset renders
are needed.

### 3.4 — `lqv/restaurant/` (4 files, 3.3 KB) and `lqv/animation/` (2 files, 1.2 KB)

**Problem:** Both are stub modules. `restaurant/` has dining_hall,
garden_deck, kitchen — all <1 KB. `animation/` has only turntable.py.

**Recommended action:** Leave as-is. Both are intentionally
scaffolded for future Fase 1 work (restaurant design + walkthrough
animations). The audit doc already flagged these as "stub/scaffolding
left in — decision: keep, archive, or delete?" — keeping is fine
since they cost <5 KB.

### 3.5 — Empty `docs/finance/`, `docs/references/`, `docs/site_data_monday/` dirs

**Problem:** Three empty (or near-empty) directories.

**Recommended action:**
- `docs/finance/fx.json` exists — keep the dir
- `docs/references/wesley_2026-06-11/` — check if empty
- `docs/site_data_monday/` — gitignored bulk imagery, .gitkeep should exist

**Net effect:** Cosmetic. Either delete or add `.gitkeep`.

---

## Tier 4 — what I would NOT touch

- ❌ **The 510 doc-layer files**. They look like a lot but most are
  load-bearing (boq, sat data briefs, audio synth, etc.). Triage is
  only worth it if Wes reports he's confused.
- ❌ **The `lqv/` Python package**. Code structure audit would take
  4+ hours per the 2026-06-30 audit, and Wes doesn't read it.
- ❌ **`docs/ideas/` 109-idea catalog**. Quality-marked (63 ✓ / 46 ○)
  this pass. The `○ auto-fill` files are honest placeholders, not bugs.
- ❌ **`docs/site_data/`** (45 brief files). Each is a data-source
  brief that Wes may or may not read; cheap to keep, expensive to curate.
- ❌ **`LICENSES/` 393 files**. By design, legal-text mirror.
- ❌ **The 18 final PNGs**. Byte-frozen at `85e86aa`.

---

## Recommended next session order

If Ivan wants to do Tier 1 + Tier 2 in one pass, here's the order:

1. Tier 1.1: Move 8 closed-session docs to `_archive/2026-06-30_session/`
2. Tier 1.2: Add forward-references from `docs/INDEX.md` to new docs
3. Tier 1.3: Move `4ENTITY_BV_CASCADE.md` to `docs/people/`
4. Tier 1.4: Move both one-pagers to `docs/people/`
5. Tier 2.1: Consolidate MASTER_BRIEF
6. Tier 2.2: Update `CLAUDE.md` document map
7. Tier 2.3: Consolidate 3 decision docs → 1

**Estimated time:** 30-45 min (mostly `git mv` + header edits + commits).

**Estimated outcome:**
- Top-level docs: 80 → ~70 (cleaner cold-start)
- `people/` becomes the natural "human/stakeholder" bucket (8 files)
- All "what to do next" / "current state" docs reduce from 12 to 3
  (POST_ESCRITURA_NOW + WES_INDEX + STATUS)
- Decision docs reduce from 3 to 1
- Cross-link from `docs/INDEX.md` to Wes-track nav
- Self-documenting `CLAUDE.md` for next AI session

---

*Generated by Erebus · 2026-07-03 · after restructure pass 51e3ea8 / 4a95e21 / 3806b5c / 5f9da20*