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
