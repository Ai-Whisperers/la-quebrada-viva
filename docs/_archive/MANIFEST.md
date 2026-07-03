# Archive manifest

Documents moved out of the live tree during the T-2 pre-escritura sweep
(2026-06-25). All are preserved verbatim under their dated subdirectory; no
content was edited as part of the move. Use this index to find the previous
location and the reason each was retired.

Live consumers were rewritten to either drop the reference or point at the new
path under `docs/_archive/<batch>/<file>`. Historical references (SESSION_LOG,
on-master commit history, the `STATUS.md` history blocks) were intentionally
left untouched — those documents describe what was true at the time of writing
and rewriting them would be revisionism.

## 2026-06-1X batch (sealed 2026-06-25, T-2 to escritura signing)

Moved during the pre-escritura critique-and-organize sweep. Each was either a
historical snapshot (critique / roast frozen at the date in the filename) or a
tiered fix-plan whose actionable items have either landed or been re-tracked
under the live TaskList. The active operating playbook now lives in `CLAUDE.md`
+ `STATUS.md` + `MASTER_BRIEF.md`; these older planning docs are kept here for
provenance only.

| Filename | Previous path | Why archived |
|---|---|---|
| `CRITIQUE_2026-06-10.md` | `docs/CRITIQUE_2026-06-10.md` | First honest-roast critique snapshot. All Tier-0 items now closed; the §1–§8 findings are folded into `CLAUDE.md` standing rules + `STATUS.md` §10 known defects. |
| `CRITIQUE_2026-06-13.md` | `docs/CRITIQUE_2026-06-13.md` | Mid-session critique iteration — superseded by the 2026-06-23 roast captured directly against the live TaskList. |
| `CRITIQUE_BUILDERS_v2.md` | `docs/CRITIQUE_BUILDERS_v2.md` | Builder-module roast at the typology level. Actionable items either landed (cob/bamboo/clay families) or are tracked as POST-ESCRITURA TaskList items #43–#47. |
| `HOUSES_REVIEW_2026-06-14.md` | `docs/HOUSES_REVIEW_2026-06-14.md` | Per-house critique pass against the 17-typology matrix. Meta-patterns 9/10/11 became `DEFERRED_BUGS.md` D1/D2/D3 — those are the live carry-forward. |
| `IMPROVEMENT_PLAN_2026-06-13.md` | `docs/IMPROVEMENT_PLAN_2026-06-13.md` | Tier-by-tier improvement plan iteration. Superseded by `TOOLING_AUDIT_AND_OPPORTUNITIES.md` for the tooling axis and by the live TaskList for the project-management axis. |
| `MODELS_ROAST.md` | `docs/MODELS_ROAST.md` | 640-line per-model critique. Actionable items folded into `DEFERRED_BUGS.md` D1/D2/D3 + `CRITIQUE_BUILDERS_v2.md` (also archived). |
| `UPGRADE_PLAN.md` | `docs/UPGRADE_PLAN.md` | Tier-0/1/2/3 fix-plan derived from the first critique. Tier-0 fully landed; Tier-1 mostly landed (sub-render framework, ruff, Makefile, RNG tests); Tier-2/3 carry forward via TaskList #34–#50. |
| `AUTONOMOUS_PLAN.md` | `AUTONOMOUS_PLAN.md` (repo root) | Standalone long-running autonomy roadmap. Operating instructions now live in `CLAUDE.md`; the per-session plan lives in the in-conversation TaskList. |

## What stayed live

Documents adjacent to these in the critique/plan family that were **kept** in
the live tree because they still drive day-to-day decisions:

- `STATUS.md` — canonical state document (refreshed alongside this archive
  batch to T-2 figures).
- `CLAUDE.md` — operating playbook + critique-derived standing rules.
- `MASTER_BRIEF.md` — 10 design rules + house-typology contracts.
- `DEFERRED_BUGS.md` — D1/D2/D3 post-escritura bug ledger.
- `docs/TOOLING_AUDIT_AND_OPPORTUNITIES.md` — superseding tooling-axis
  improvement plan.
- `docs/sub_render_strategy.md` — sub-render-first architectural design doc.
- `PROJECT_INDEX.md` — repo map (links to archived docs were rewritten to
  point at this batch).


## Pass 2 (2026-07-03) — Tier 1+2 consolidation

Moved as part of `docs/audit/RESTRUCTURE_PASS_2_RECOMMENDATIONS.md`. The canonical "what to do" answers are now `docs/POST_ESCRITURA_NOW.md` + `docs/WES_INDEX.md` + `docs/people/WES_ACTIONS.md`.

| Filename | Previous path | Why archived |
|---|---|---|
| `MASTER_BRIEF_cob_house_v1_2026-06-11.md` | `docs/MASTER_BRIEF.md` | Pre-Wes-share cob-house-only master brief (33 KB). Superseded by `docs/_reconciled/MASTER_BRIEF.md` (18 KB, post-Wes-share housing-park scope). The top-level `docs/MASTER_BRIEF.md` is now a 1-line pointer stub. |
| `DECISIONS_LOG_escritura_week_2026-06.md` | `docs/DECISIONS.md` | Escritura-week append-only decision log. Superseded by `docs/_reconciled/OPEN_DECISIONS.md` (housing-park open decisions) + `docs/people/DECISIONS_LOG.md` (housing-park closed). Top-level `docs/DECISIONS.md` is now a 1-line pointer stub. |
| `2026-06-30_session/` (10 files + MANIFEST) | `docs/{WES_TODO,WES_TODO_UPDATE,WES_5_THIS_WEEK,PRIORITIES_NEXT,CRITICAL_PATH,STATUS_REPORT,IMPLEMENTATION_COMPLETE,IMPLEMENTATION_PROGRESS,FINAL_SUMMARY,COMPREHENSIVE_REMAINING_RESEARCH}.md` | 10 closed-session docs from 2026-06-30 implementation pass. All superseded by `POST_ESCRITURA_NOW.md` + `WES_INDEX.md`. New `MANIFEST.md` in the dir explains the mapping. |
| `topology_lod_unreferenced/cop30_raw.tif` | `docs/site_data/topology_lod/regional/cop30_raw.tif` | 11.7 MB unreferenced raster (not in `tier_manifest.md`). |
| `property_map_v1_brief.md` | `docs/site_data/property_map/property_map_brief.md` (renamed) | Superseded by v2 brief, now promoted to canonical `docs/site_data/property_map/property_map_brief.md`. |

## Pass 3 (2026-07-03) — Tier 1 + 2.1 + 3.6

Moved as part of `docs/audit/RESTRUCTURE_PASS_3_RECOMMENDATIONS.md`. Smaller stale docs that don't compete with POST_ESCRITURA_NOW but bloat the canonical tree.

| Filename | Previous path | Why archived |
|---|---|---|
| `2026-06-30_session/patches/` (2 files) | `docs/patches/` | Patch instruction files that were already applied in commits 3ceca61 / 3806b5c. No current value. |
| `REPO_STRUCTURE_2026-06-30.md` | `docs/REPO_STRUCTURE.md` | 14 KB structural doc, now factually stale (references WES_TODO.md at top level — moved in pass 2). Three nav docs (INDEX + WES_INDEX + STATUS) serve the role. |
| `MASTER_TODO_escritura_week_2026-06-25.md` | `docs/MASTER_TODO.md` | 31 KB / 768-line master plan from escritura week (T-2 to signing). Predates signing + audio synthesis + pass 2. Top-level `docs/MASTER_TODO.md` is now a 1-line pointer stub. |
| `T_PLUS_1_DEBRIEF_2026-06-28.md` | `docs/T_PLUS_1_DEBRIEF.md` | Single 2026-06-28 session retrospective, unreferenced. |
| `PR_BACK_TO_BASE_workflow_note.md` | `docs/PR_BACK_TO_BASE.md` | One-time git/PR workflow note, not project-relevant. |
| `GAPS_ANALYSIS_2026-06-04.md` | `docs/GAPS_ANALYSIS.md` | 35 KB pre-Wes-share gap analysis, superseded by `docs/RESEARCH_GAPS.md` (canonical per CLAUDE.md document map). |
| `IDEAS_CATALOG_PATCH_PLAN_2026-06-30.md` | `docs/_reconciled/IDEAS_CATALOG_PATCH_PLAN.md` | 5 KB patch plan, doc itself recommends deferring 4-6 hours of work. Quality-marking (pass 1) addressed half; remaining items still deferred per the doc. |

The 109-idea catalog is now split:
- `docs/ideas/` — 63 ✓ reviewed files
- `docs/ideas/_archive/2026-06-30_autofill/` — 46 ○ auto-fill files (with MANIFEST explaining the split)

## Live pointer stubs (1-liners at top-level)

These exist at their historical paths but are no longer full documents:

| File | Points to |
|---|---|
| `docs/MASTER_BRIEF.md` | `docs/_reconciled/MASTER_BRIEF.md` |
| `docs/MASTER_TODO.md` | `docs/POST_ESCRITURA_NOW.md` |
| `docs/DECISIONS.md` | `docs/_reconciled/OPEN_DECISIONS.md` + `docs/people/DECISIONS_LOG.md` + this archive |
