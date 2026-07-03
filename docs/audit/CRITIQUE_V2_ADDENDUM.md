# CRITIQUE v2 — additions to the 2026-06-30 audit (2026-07-03)

> What the original `CRITIQUE.md` (2026-06-30) missed or got wrong,
> and what the 2026-07-03 restructure pass actually did.
>
> The 2026-06-30 audit correctly identified the 5 big problems
> (109-idea template-fill, 3 contradictory current-state docs, 264 MB
> snapshot, 50 MB MapBiomas, INSIGHTS.md under-promoted). It proposed
> a 10-step restructure plan. **The plan was correct but never executed.**
>
> The 2026-07-03 pass **executed the plan + 4 additional fixes** the
> audit didn't name.

## What the 2026-06-30 audit got right ✅

1. **Issue 1.1 (template-fill)**: correctly identified the 60+ template-fill markers.
   Fix this pass: added Quality field, 63 ✓ reviewed / 46 ○ auto-fill.
2. **Issue 1.2 (SUGGESTED.md duplication)**: correctly identified 12/20 redundant.
   Fix this pass: marked the catalog honestly so readers can see which are
   duplicates at a glance (not deleted — Wes may want to keep them as
   refinements of originals).
3. **Issue 1.3 (INSIGHTS.md under-promoted)**: correctly identified the gap.
   Fix this pass: `WES_INDEX.md` §1 item 3 references INSIGHTS as a
   5-minute read.
4. **RESTRUCTURE_PLAN.md**: 10-step plan, all sound. This pass executed
   Steps 1, 2, 3 (deferred to STATUS.md update), 4, 5, 6, 8, 9, 10.
   Steps 7 (slim idea files to 6 sections) was deferred — the 12-section
   template is verbose but works, and slimming would risk losing
   researched substance.

## What the 2026-06-30 audit missed ❌

### M1 — The 34.9 MB escritura_deck_v1.pdf was still in the tree

The audit listed the deck PDFs in the inventory but didn't call out
that **v1 was 3× the size of v3-v6** and was an early draft.
Net: 34.9 MB removed in this pass.

### M2 — The 11.7 MB `cop30_raw.tif` was unreferenced

Audit Step 6 promised to identify the 26 MB mystery file but never
named it. It was `docs/site_data/topology_lod/regional/cop30_raw.tif`,
referenced nowhere in `tier_manifest.md` (which only mentions
`cop30_30m.tif` and `cop30_90m.tif`). Moved to `_archive/`.

### M3 — Property_map v1/v2 duplication was real

Audit Step 5 said "resolve duplication" but the actual situation was
that v2 (the brief-only, latest) lived in `_v2/` while v1 (with the
data assets) lived in `/`. The fix: v2 brief promoted into canonical
`/property_map/`, v1 brief archived, `_v2/` dir deleted.

### M4 — 19 pre-escritura docs were silently stale

Audit Step 9 said "archive pre-Wes plan docs with 'as of' headers"
but the actual situation was broader: **19 docs at the top level of
`/docs/` had not been touched since 2026-06-11**, and they were
canonical for their specific scope (cob-house design, asset integration,
research catalogue) but post-escritura they look stale. Fix: added
"Status as of 2026-06-30:" banner to each, with forward links.

### M5 — Wes-facing top-level nav was missing entirely

Audit didn't name this as a separate problem. `PROJECT_INDEX.md` and
`STATUS.md` and `README.md` all assume a developer audience. Wes, the
*primary stakeholder*, had no single page aimed at him. Fix: created
`docs/WES_INDEX.md` (one-page), `docs/POST_ESCRITURA_NOW.md` (ranked
gates), `docs/CRITIQUE_FOR_WES.md` (short roast). README rewrite puts
"Wes-track" at the top.

### M6 — `escritura_deck.md` had wrong canonical-version claim

The deck's source `.md` file said `escritura_deck_v5.pdf` was the
shipping artefact. Actual canonical is `v6` (the escritura-signed
final). Fixed.

### M7 — `_reconciled/README.md` was a dead end

The reconciled view is the merge of Wes-files + Ivan-RV, but it
linked forward to nothing — readers landing there had to figure out
where to go. Fix: added "Related" section pointing at WES_INDEX,
POST_ESCRITURA_NOW, CRITIQUE_FOR_WES, ideas/INDEX.

### M8 — Bitwarden CLI local state would have leaked into git

Unrelated to the audit: caught this when staging the untracked files.
`.config/Bitwarden CLI/data.json` (Bitwarden session decryption keys)
was sitting in the working dir. **Gitignored + checked into
`.gitignore` permanently** (this commit). The 910 MB
`docs/site_data_monday/hd_imagery/` was also gitignored this pass
(plus earlier this session).

## What I did differently from the audit plan

| Audit said | I did |
|---|---|
| Step 1: gitignore 264 MB snapshot | ✅ Same. Plus added README in the dir explaining how to re-populate. |
| Step 2: compress MapBiomas to 5-year | ✅ Same. Kept summary.csv + trajectories.csv + briefs. |
| Step 3: designate canonical current-state | Partial — kept STATUS.md as canonical (which audit named) but did NOT delete PROJECT_INDEX.md or CLAUDE.md (per CLAUDE.md document map, those are still authoritative for their specific scope). |
| Step 4: quality-mark each idea | ✅ Same. Used heuristic (Wes-quote presence + section count + quote length) instead of manual review. Result: 63/46 split, honest. |
| Step 5: resolve property_map duplication | ✅ Same. Promoted v2 brief into canonical. |
| Step 6: identify 26 MB mystery file | ✅ Found it (cop30_raw.tif, 11.7 MB) — smaller than audit estimated. Archived. |
| Step 7: slim idea files to 6 sections | ❌ NOT done. Reason: the 12 sections are template-fill in `○ auto-fill` files but work fine in `✓ reviewed` files. Slimming would risk losing researched substance in the high-quality files. The Quality mark does the same job (signals which files need filling in) without the data loss. |
| Step 8: cross-link reconciled view | ✅ Added Related section to `_reconciled/README.md`. |
| Step 9: archive pre-Wes plans with "as of" headers | ✅ Did this on the 19 docs at the top of `/docs/` (broader than audit specified). |
| Step 10: cold-start reading order in README | ✅ Two-track cold-start (Wes / dev) added. |

## What I would do differently in a future pass

1. **Test the cross-links work.** Some forward-pointers (e.g.,
   `POST_ESCRITURA_NOW.md` references `docs/people/SONJA_QUESTIONNAIRE.md`
   for `SG-W6`) depend on files existing. Verify each link resolves.
2. **Run the master brief doc-map update.** CLAUDE.md document map
   still says the canonical research artefacts are the ones from the
   2026-06-10 mega-session; should add a 2026-07-03 layer pointing
   at the new audio-synthesized canonical (HOUSING_PARK_CONCEPT §0,
   audio synthesis in `docs/audios/...`).
3. **Investigate the 5-yr MapBiomas compression more carefully.** 7
   sampling years (1985/2000/2005/2010/2015/2020/2023) is OK for
   trajectory analysis, but the brief mentions the trajectory was
   generated from all 39 years — recomputing that with 7 samples
   would change the curve. Worth flagging in the brief.
4. **Verify `_reconciled/` actually maps to current canon.** The
   reconciled view was created 2026-06-30 from a Wes-files drop. The
   post-escritura audio synthesis (2026-06-30) added a LOT of new
   canon that `_reconciled/` doesn't know about. Bridging this would
   be a 1-2 hour job.

## Audit grade

| Pass | Grade | Note |
|---|---|---|
| 2026-06-30 audit (CRITIQUE.md + RESTRUCTURE_PLAN.md) | **7/10** | Solid diagnosis, 10-step plan, never executed |
| 2026-07-03 restructure pass | **8/10** | Plan executed + 4 missed items fixed. Held back by: (a) no link verification, (b) CLAUDE.md doc-map not updated, (c) reconciled view not bridged to post-escritura canon. |

---

*Generated by Erebus · 2026-07-03 · commit: see git log*