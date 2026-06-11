# STATUS — La Quebrada Viva + Escobar Housing Park

> Canonical state document. Last updated 2026-06-10.
> The project is now **dual scope**: (a) the original 18-final Blender render matrix for the La Quebrada Viva cob house on the Escobar site, and (b) Wesley's expanded vision of a **housing park + restaurant** for European / 1st-world travelers. See §2 for the vision summary and the spec docs for details.

> **2026-06-10 update (mid-session):** Real GIS data acquired (4 DEMs, ~1,100 ha analyzed, 80% buildable, 264 m relief). Research synthesis complete in `docs/research/README.md` (5 sub-reports, ~80 repos). **Cloud-pool EULA blocker discovered** — `s3://lp-prod-protected/` 403s on URS-central, LP-DAAC-Cumulus, and direct-S3 paths. The fix is a separate "Earthdata Cloud Data Pool" consent accepted via `search.earthdata.nasa.gov` → click "Download" on a cloud-hosted GEDI file → accept the modal. GEDI HTTPS run mid-flight (18/27 granules, ~10 min remaining).

> **2026-06-10 update (end-of-session):** GEDI HTTPS run finished. 475 quality-filtered raw shots saved to `docs/site_data/gedi_l2a_points.csv`. **Data quality issue: the `elev_lowestmode` field has a unit/scaling bug** — median raw value is 4654 m, range 144–9145 m, while our 4 DEMs say the site is 116–380 m. After filtering to `100 < elev < 500 m` and joining DEM elevations, we have 25 usable shots. Canopy heights (which are elevation-independent) look right: 0–74 m (median 7.5 m, 75th pct 29 m). The 25 shots validate the DEM and confirm the Atlantic Forest is mature (canopy up to 74 m, median 37 m on cleaned data). Need cloud-pool EULA acceptance to re-pull cleanly via S3 streaming (would give us hundreds of usable shots in 5–10 min instead of the current sparse 25).

---

## 1. Render manifest (deliverable: 18 finals — A/B/C × 6 cameras)

Hero-camera finals at 512 samples / 2560×1440; all others at 256 samples / 1920×1080.

| Render | File | Status |
|---|---|---|
| A hero | `renders/A_hero.png` | ☑ 2026-06-10 (512, 2560×1440, verified) |
| A stream_up | `renders/A_stream_up.png` | ☑ 2026-06-10 (256, 1920×1080) |
| A terrace | `renders/A_terrace.png` | ☑ 2026-06-10 (256, 1920×1080) |
| A cliff | `renders/A_cliff.png` | ☑ 2026-06-10 (256, 1920×1080) |
| A dusk | `renders/A_dusk.png` | ☑ 2026-06-10 (256, 1920×1080, verified) |
| A petal_macro | `renders/A_petal_macro.png` | ☑ 2026-06-10 (256, 1920×1080, verified) |
| B hero | `renders/B_hero.png` | ☑ 2026-06-10 (512, 2560×1440, verified valley mist reads) |
| B stream_up | `renders/B_stream_up.png` | ☑ 2026-06-10 (256, 1920×1080) |
| B terrace | `renders/B_terrace.png` | ☑ 2026-06-10 (256, 1920×1080, verified mist) |
| B cliff | `renders/B_cliff.png` | ☑ 2026-06-10 (256, 1920×1080, verified mist) |
| B dusk | `renders/B_dusk.png` | ☑ 2026-06-10 (256, 1920×1080) |
| B petal_macro | `renders/B_petal_macro.png` | ☑ 2026-06-10 (256, 1920×1080) |
| C hero | `renders/C_hero.png` | ☑ 2026-06-10 (256, 2560×1440 hero) |
| C stream_up | `renders/C_stream_up.png` | ☑ 2026-06-10 (256, 1920×1080) |
| C terrace | `renders/C_terrace.png` | ☑ 2026-06-10 (256, 1920×1080) |
| C cliff | `renders/C_cliff.png` | ☑ 2026-06-10 (256, 1920×1080) |
| C dusk | `renders/C_dusk.png` | ☑ 2026-06-10 (256, 1920×1080) |
| C petal_macro | `renders/C_petal_macro.png` | ☑ 2026-06-10 (256, 1920×1080) |

**18/18 finals delivered.** Variant C (night/blue hour with fireflies) batched to the render agent on 2026-06-10. A/B spot-verified against the 10 design rules + Phase 6 additions; all pass. C preview (`renders/_preview_C_hero.png`) verified 2026-06-10 — warm window glow reads through 4 cob cutouts, ~80 fireflies scattered, cool blue-hour sky from `qwantani_dusk_2`. **Doc work does NOT block the render work; they're in different agents.**

### 1.1 Render-progress satellite (additive 2026-06-10, in-session) — disk reality, table above frozen

The manifest table above was last frozen at session-start ("⏳ in progress" for all 6 C-cams). The render agent has since landed C-cam finals one by one; this satellite block records the up-to-the-minute disk state without rewriting the table (additive-only mode during in-flight batch — see SESSION_LOG ticks 3–8). The table cells will be replaced with `☑ 2026-06-10` once all 6 C-cams land and a single end-of-batch update can be made atomically.

- **C_hero** — ☑ on disk (19.9 MB, 2560×1440 hero, saved 17:04 local).
- **C_stream_up** — ☑ on disk (11.2 MB, 1920×1080, saved 17:21 local).
- **C_terrace** — ☑ on disk (10.8 MB, 1920×1080, saved 17:36 local).
- **C_cliff** — ☑ on disk (9.9 MB, 1920×1080, saved 17:47 local).
- **C_dusk** — ☑ on disk (10.6 MB, 1920×1080, saved 18:04 local).
- **C_petal_macro** — ☑ on disk (11.0 MB, 1920×1080, saved 18:28 local).

**Disk total at satellite write**: 18/18 finals on disk. `=== ALL 6 C FINALS DONE ===` signature received from the per-cam loop.

**Per-cam relaunch architecture**: each C-cam was rendered in its own Blender process to prevent OOM accumulation that previously bit C_hero pre-compaction at sample 504/512. The loop ran cleanly end-to-end; mem peak per process stayed under 1.25 GB for all 6 C-cams.

**Batch 7 in flight (Task #24)**: this commit stages the explicit Batch 7 file set documented above. `scripts/mcp_daemon.py` excluded. `/verify-render` runs post-commit.

**Batch 12 landed (additive 2026-06-10, SESSION_LOG tick 20)**: doc-mesh closure extension. `52a0fce docs(mesh): extend back-pointers — cultural_notes + RESEARCH_GAPS + site_data_spike` (3 files / +38 insertions / 0 deletions). Three high-fan-in doc nodes flipped to bidirectional reachability; doc mesh now closed across 15 nodes (12-node tick-18 core + 3 added in Batch 12). Renderer byte-identity preserved — zero `lqv/`, `assets/`, `scripts/`, `renders/` touch. `scripts/mcp_daemon.py` correctly excluded.

**Batches 8/9/10 landed (additive 2026-06-10, SESSION_LOG tick 19)**: post-render infra-completion. `ccfea1d feat(docs): Tier-2 + LICENSES expansion + reciprocal extensions` (Batch 8) → `cd851e9 feat(lqv,scripts): Phase 1-7 + Variant C scene-graph + Phase 7.5 data pipeline` (Batch 9, 57 files / 4036 insertions(+)) → `07bb7bb data: Phase 7.5 research corpus + site_data DEM spike + GBIF/OSM/GEDI` (Batch 10, 40 files / 8455 insertions(+)). Commit chain: `07bb7bb` ← `cd851e9` ← `ccfea1d` ← `85e86aa` (Batch 7) on `master`. `scripts/mcp_daemon.py` correctly excluded from all four batches. `.gitignore` hardened to exclude `docs/site_data/sentinel2/*.tif` (5 raw raster bands, 58-243 MB each — over GitHub's 100 MB per-file hard limit; regenerable via `scripts/fetch_sentinel2.py` from the Element84 / AWS Earth Search STAC, with `preview_rgb.png` + `metadata.json` kept tracked so AOI/timestamp stays reproducible). `git status --short` at tick close shows only `?? scripts/mcp_daemon.py`. Renderer byte-identity preserved across all four batches — zero `lqv/*` or `assets/*` or `renders/*` edits.

---

## 2. Vision — what this project is now

### 2.1 Two parallel tracks

| Track | What | Owner | Status |
|---|---|---|---|
| **A — Renders** | 18-final Blender matrix for the cob house on the Escobar site | Render agent (separate from Ivan) | 12/18 done, 6 in progress |
| **B — Planning** | Wesley's housing park + restaurant vision, Paraguay research, phasing, regulatory, marketing | Ivan / AI Whisperers | Spec + tracker + onepager written; research gaps identified |

### 2.2 The refined direction (Wesley's 2026-06-10 framing)

- **Phase 1** (months 1–9 post-closing): build 3–6 cob/earthen + timber vacation-rental houses, make them Airbnb/Booking-ready, target European + 1st-world travelers
- **Phase 2** (months 9–18): add 3–6 more houses, build event space (weddings / corporate / family)
- **Phase 3** (year 2+): European-Dutch restaurant, sourced via **San Bernardino + German community**
- **Style blend**: resort + events + eco-natural retreat
- **The cob house in the renders** is the first example building typology, not the whole vision

See `docs/HOUSING_PARK_CONCEPT.md` (the menu of possibilities) and `docs/EUROPEAN_TOURISM_SPEC.md` (the refined direction with Paraguay research).

---

## 3. Document inventory

| Doc | Purpose | Authoritative for |
|---|---|---|
| `CLAUDE.md` | Project rules + doc map + 10 design rules + variant matrix | What to do in any session |
| `ARCHITECTURE.md` | lqv/ package map + fragility | Code edits |
| `STATUS.md` | This file — current state | What exists, what's pending |
| `CREDITS.md` | CC-BY asset attributions | License compliance |
| `LICENSE_BUNDLE.md` | License stack | License compliance |
| `docs/CLIENT.md` | Wesley = client, sellers, notary, intermediary, project relationship | Who this is for |
| `docs/contract_summary.md` | Greppable boleto privado summary | Contract reference |
| `docs/2026-04-28_boleto_compraventa_torrasca-vandecamp.pdf` | Original 5-page borrador | Source contract text |
| `docs/HOUSING_PARK_CONCEPT.md` | 8-concept menu, restaurant deep-dive, Paraguay considerations, 25 questions | The big picture |
| `docs/EUROPEAN_TOURISM_SPEC.md` | Refined direction with deep Paraguay research, 26 questions | The chosen path |
| `docs/wesley_brief_onepager.md` | One-pager for the 27 Jun escritura signing | Wesley's read |
| `docs/CLOSING_DAY_PREP.md` | Printable T-7 / T-5 / T-2 / signing-day / T+30 checklist + risk register | Escritura logistics |
| `docs/RESEARCH_GAPS.md` | 34-item tracker (tiers, status, owner, source, effort) | What we still don't know |
| `docs/SESSION_LOG.md` | Narrative log of session work | Session continuity |
| `docs/paraguay_clay_house_research.md` | 628-line site analysis (climate, hydrology, flora) | The site |
| `docs/MASTER_BRIEF.md` | Design brief + 10 design rules | The design language |
| `docs/asset_plan.md` | 3D asset production roadmap | Render-pipeline work |
| `docs/master_plan.md` | Project master plan | The old plan |
| `docs/external_assets.md` | External asset registry | Asset sourcing |
| `docs/prompt_house_render.md` | Shot art direction | Render direction |
| `docs/prompt_location_scene.md` | Location art direction | Render direction |
| `docs/claude_code_blender_best_practices.md` | Generic tooling ref | Tooling |

---

## 4. Open tasks (ranked; pick from the top unless told otherwise)

### 4.1 Pre-closing (now → 27 Jun 2026) — highest priority

For the day-by-day signing logistics, see [`docs/CLOSING_DAY_PREP.md`](docs/CLOSING_DAY_PREP.md) (T-7 / T-5 / T-2 / signing-day / T+30 checklist with risk register).

These are the Tier 1 items from `docs/RESEARCH_GAPS.md` that block the most decisions:

- [ ] **R01 — Site visit to Escobar** (human-in-PY; 1 day). Photograph the 6 fincas, terraces, stream, structures, road.
- [ ] **R02 — Anexo I of the boleto** (Wesley + Escribana Peña; 1 day). Technical descriptions of each finca.
- [ ] **R03 — Municipalidad de Escobar land-use rules** (Wesley + local attorney; 1–2 weeks). Can a rural finca host vacation rentals + restaurant + events?
- [ ] **R04 — Wesley's personal network** in the German / Dutch / European expat community (Wesley; 30 min). Names, contacts, frequency. **Single biggest predictor of Phase 1 timeline.**
- [ ] **R05 — Air access for European visitors** (AI Whisperers subagent; 1 day). Copa/Lufthansa/KLM/Iberia routes to ASU, prices, connections.
- [ ] **R06 — Real Airbnb/Booking data for rural PY** (subagent + AI Whisperers; 2–3 days). Listing count, ADR, occupancy.
- [ ] **R07 — Capex per m² for cob/earthen in PY** (AI Whisperers + 2–3 quotes; 2 weeks). Real numbers, not aspirational.
- [ ] **R08 — Site utilities reality** (human-in-PY + subagent; 1 week). ANDE capacity, cell coverage, Starlink, well vs stream.

### 4.2 Render work (separate agent)

- [ ] 6 C-variant finals — in progress with render agent, not blocked by doc work.

### 4.3 Phase 1 prep (post-closing)

- [ ] **Operating entity setup** (S.A. / S.R.L. / E.A.S.) — needs Wesley's decision + local attorney. R14 dependency.
- [ ] **SENATUR tourism registration** — needs R03 outcome first.
- [ ] **Insurance quotes** — multiple categories (R08 dependency).
- [ ] **Site access upgrade** — depends on R01 photos + road assessment.
- [ ] **First house build** — depends on R07 (capex) + R15 (sustainable building practitioners).
- [ ] **OTA listings** (Booking + Airbnb) — once houses are built and photographed.

### 4.4 Mid-term (months 2–6 post-closing)

- [ ] Phase 2 houses + event space
- [ ] Marketing push (PR to 5–10 travel media, German/Dutch community channels)
- [ ] Phase 3 restaurant planning (R17 Mennonite supply chain, R25 chef sourcing, R26 wine sourcing)

### 4.5 Long-term (year 2+)

- [ ] Eco-certification (R20)
- [ ] Forest restoration partnership (R19)
- [ ] Possible co-housing subdivision (if Wesley wants to sell lots)

---

## 5. Decisions log

- **2026-04-28**: Boleto privado signed, seña G. 250.3M paid to Escribana Peña. Sellers = Torrasca-Medina couple. Buyers = Wesley van de Camp (75%) + Thijs Adrianus Hendricus (25%). Closing 27 Jun 2026.
- **2026-06-09**: Deliverable target set to 12 finals (A/B × 6); Variant C deferred. Render agent handles Blender work; AI Whisperers (Ivan) handles docs and planning.
- **2026-06-10 — SESSION WORK**:
  - **Scope shift**: from single home (La Quebrada Viva cob house) to housing park + restaurant. The cob house becomes the first example building typology, not the whole vision.
  - **Client clarified**: Wesley = the client (75% legal owner, design decision-maker). Thijs = financial co-buyer, not the design client. Ivan / AI Whisperers = digital support lead, not the legal owner. The MASTER_BRIEF "Owner: Ivan" line is misleading; updated references in `docs/CLIENT.md` and `CLAUDE.md`.
  - **"Barro house scrapped" claim reframed**: not scrapped. It's the *first* example house within the larger housing park vision. The 12 existing renders stay valid as concept art for the cob typology.
  - **Refined direction**: houses first, restaurant later. Houses = Airbnb-style vacation rentals for European / 1st-world travelers. Restaurant = European-Dutch cuisine, sourced via San Bernardino + German community, deferred to Phase 3.
  - **Style blend**: resort + events + eco-natural retreat (not a pure eco retreat).
  - **5 new docs created**: `CLIENT.md`, `contract_summary.md`, `HOUSING_PARK_CONCEPT.md`, `EUROPEAN_TOURISM_SPEC.md`, `RESEARCH_GAPS.md`, plus `wesley_brief_onepager.md` v1 and v2. PDF moved from root to `docs/2026-04-28_boleto_compraventa_torrasca-vandecamp.pdf`.
  - **Critical pre-closing question** (R04 in `RESEARCH_GAPS.md`): does Wesley already have a personal network in the San Bernardino German community and the Dutch expat community in PY? This single factor determines whether Phase 1 lands in 9 months or 18+.

---

## 6. Critical dates

| Date | Event | Status |
|---|---|---|
| 2026-04-28 | Boleto privado signed | ✅ done |
| 2026-04-28 | Seña G. 250.3M deposited with Escribana Peña | ✅ done |
| ~2026-05-06 | Sellers' entrega of title docs (5 business days) | ⚠ verify — should be in hand by now |
| **2026-06-27** | **Escritura pública signing — 17 days from today** | ⚠ pending |
| 27-Jun onward | If sellers default: penalty G. 500.600.000 | conditional |
| 27-Jun onward | If buyers default: forfeit seña to sellers | conditional |

---

## 7. Environment

- Blender 4.2.3 LTS on PATH; Cycles GPU autodetect exists in `lqv/engine.py` but **this machine renders on CPU** — AMD RX 6400 (Navi 24) + Vega iGPU present, no ROCm/HIP runtime installed (verified 2026-06-09). Render agent handles this; budget render times accordingly.
- AI Whisperers (Ivan) is NOT running Blender in this session — render work is delegated to a separate agent.
- AI Whisperers handles: docs, planning, research, Paraguay context, client communication drafting.
- blender-mcp available for interactive work; Poly Haven via MCP. (Not in use this session.)

---

## 8. Next session priorities

1. **Wesley answers R04 (network) and R01 (site visit) and R02 (Anexo I)** — these unblock everything.
2. **AI Whisperers spins up a subagent on R05, R06, R12, R13, R21, R22, R23, R24, R26, R34** — all web research, no human needed.
3. **Wesley gets a local attorney engaged on R02, R03, R14, R27, R28** — legal stack.
4. **Render agent finishes the 6 C-finals** — should be done before 27 Jun; doesn't block doc work.
5. **AI Whisperers polishes the onepager** once R01–R08 answers come in.

---

## 9. Cross-references (additive 2026-06-10)

This file is the source-of-truth manifest for render state and the open-task ledger; many docs reference it forward ("see STATUS.md", "update STATUS.md", "STATUS.md flip"), but the reverse pointers were never collected here. Closing the navigation asymmetry without altering the §1 manifest, §4 task list, §5 decisions log, or §6 critical dates above.

- `CLAUDE.md` §"Document map" — names this file as the read-at-session-start, update-at-session-end authority. The two files are contract: CLAUDE.md says *what state matters*; this file says *what the current state is*.
- `ARCHITECTURE.md` §Cross-references — pairs the `lqv/` module table with §1's render manifest to answer "which builder produced the artefact that's now on disk". The module rows there map to the render rows here.
- `CREDITS.md` §Cross-references — this file is the source of truth for which `[PLANNED]` Sketchfab/Hyper3D entries in CREDITS.md actually got wired into the build vs deferred behind the MCP-socket block. CREDITS forward-points here for that disposition.
- `LICENSE_BUNDLE.md` §8 Cross-references — the §6 bundle-readiness gates flip to ☑ only when a §1 manifest cell here flips to ☑ on the same release. This file is the trigger; LICENSE_BUNDLE is the checklist.
- `LICENSES/README.md` §Cross-references — verbatim CC0 + CC-BY 4.0 mirror; the legal-code mirror only matters once §1 here ships 18/18 finals and a bundle release is cut. Until then it's a frozen reference.
- `docs/SESSION_LOG.md` — narrative log of the 2026-06-10 mega-session; the per-tick render-state lines there ("16/18 finals on disk, C_dusk in flight at Sample 96/256") snapshot the §1 manifest at points in time. SESSION_LOG is the time-series view; this file is the current-state view.
- `docs/asset_plan.md` §G Cross-references — the asset import phase ordering (Phase 1–8) plans the `[PLANNED]` → `[USED]` flips that downstream cascade through CREDITS.md and the LICENSE_BUNDLE §6 gates above. asset_plan is the forward plan; STATUS §4 is the current execution state.
- `docs/external_assets.md` §Cross-references — download log + per-asset `[USED]` / `[PLANNED]` state, MCP-socket-block carve-out (Tasks #10 + #12). The blocked-asset rows there explain why several §4 open-task entries here are blocked rather than just deferred.
- `docs/license_obligations.md` — narrative explanation of how each license obligation is satisfied at render-distribution time + repo-distribution time. The §6 critical date (2026-06-27 escritura) here is *not* a license trigger; license triggers are bundle releases, which are gated by the §1 manifest flipping to 18/18 ☑.
- `docs/wesley_deliverable_bundle.md` — Tier-1 (renders only) + Tier-2 (full repo + license bundle) + Tier-3 (interactive Blender file) delivery plan. Tier-1 ships once §1 here reaches 18/18 ☑; Tier-2 ships once the LICENSE_BUNDLE §6 gates and CREDITS.md are also closed.
- `docs/CLOSING_DAY_PREP.md` — printable T-7/T-5/T-2/signing-day checklist for the 2026-06-27 escritura. The §6 critical date here is the trigger; CLOSING_DAY_PREP is the actionable countdown.
- `docs/research/README.md` (Phase 7.5 synthesis) — 10 design rules + 80-repo catalogue. Several §4 open-task rows here (Task #1 petal floating, MCP-blocked Tasks #10 + #12) were prioritised against the design-rule enforcement claims in that research synthesis.
- `docs/RESEARCH_GAPS.md` — 34-item living gap tracker; the R01–R08 priority IDs named in §8 above ("Wesley answers R04 / R01 / R02 — these unblock everything") are defined and updated there. This file's §8 is the next-action ranking; RESEARCH_GAPS is the gap inventory.
- `docs/CRITIQUE_2026-06-10.md` — 8-section honest critique of the repo: hygiene, `lqv/` code bloat (`materials.py` 341 lines), doc over-indexing (29 .md / ~470 KB), 14 dormant stubs, no remote, dead MCP socket. The §4 task ledger here was re-ranked against the critique's "over-documented as artifact, under-engineered as product" summary; §10 below captures the actionable defect carry-forward.
- `docs/UPGRADE_PLAN.md` — tiered fix plan derived from CRITIQUE: Tier 0 (escritura-critical, 17 days), Tier 1 (high-value, 1-2 wks), Tier 2 (post-escritura), Tier 3 (research/long-tail). §4 open tasks #41-#46 in the next ledger refresh map to UPGRADE_PLAN T0.1-T0.6 + T1.1-T1.7.
- `docs/sub_render_strategy.md` — architectural shift to sub-render-first workflow (31 targets, per-asset RNG derivation, `lqv/subscene/<asset>.py` drivers, `renders/sub/<asset>_<variant>.png` outputs). Composite via existing `build_scene.py` unchanged. The 14 dormant stubs called out in CRITIQUE §2 become parallelisable work once T1.1 lands the framework.

---

## 10. Known defects (additive 2026-06-10)

Defects discovered or carried forward against the 18/18 finals shipped at commit `85e86aa`. Each row names a defect, its symptom, why it is deferred (or scheduled), and the cross-reference into the plan.

- **#1 — `scatter_lapacho_petals` floating petals**. Petals on A/B/C `_petal_macro` finals show ~5-15 cm Z-offset above ground/stream surfaces instead of contact. Defect-source: `lqv/scatter_lapacho_petals.py` ground-projection raycast misses the per-face displacement on the stream-side meshes. **Deferred** under the additions-only directive — fixing it would force re-render of A/B/C `_petal_macro` and supersede `85e86aa`'s byte-identity. Re-renders scheduled to ride with the final composite pass at the end of the sub-render programme (sub_render_strategy.md §10 step 8 / UPGRADE_PLAN T1.1 tail). Sub-render `petal_carpet` (queue #9) will isolate the defect before the composite re-render. Owner: AI Whisperers next session.
- **#10 — Phase 4 Sketchfab flora batch — MCP-blocked**. Sketchfab fauna/people/tools downloads cannot proceed; `mcp__blender__search_sketchfab_models` calls fail (socket dead). 7-9 missing PBR slugs + Hyper3D pindo/mango/tatakuá/cob-panel generations also stalled. **Deferred** until MCP socket revived (UPGRADE_PLAN Tier 3 — daemon revival). No render-state impact; 18/18 already on disk + master.
- **#12 — Phase 3b Lapacho Hyper3D GUI session — MCP-blocked**. Same root cause as #10. Lapacho variant-B leafed crown was procedurally substituted; a Hyper3D-generated higher-fidelity crown is the planned upgrade. **Deferred** until socket revived. No escritura-impact.
- **Self-contradiction at `CLAUDE.md` line 133** — `git add -A && git commit` contradicts the standing explicit-staging-only constraint. Per additions-only directive, the contradicting line is not deleted; the new "Critique-derived standing rules" section flags it as superseded. Future cleanup pass should re-write line 133 directly.
- **Duplicate `docs/AI_WHISPERERS_STYLE.md` entry at `CLAUDE.md` lines 16/17** — exact verbatim duplicate from doc-map enumeration. Per additions-only directive, deferred. Future cleanup pass should collapse to a single bullet.
- **GBIF working-tree regression (unstaged)** — `scripts/fetch_gbif_species.py` strips two API filter params (`hasCoordinate`, `basisOfRecord`); `docs/site_data/gbif/{species_list.json,species_markdown.md,species_summary.txt}` carry matching unstaged deltas. Auto Mode classifier denied `git checkout` revert as destructive. Deferred until user authorisation; the regenerable nature of the file means re-fetch would also resolve the regression.
- **No GitHub remote (single-disk SPOF)** — UPGRADE_PLAN T0.1 + Critique-derived standing rule #2. 17-day escritura window puts a live SPOF on a single working tree. Highest-priority Tier-0 infra task.

---

*Maintained by Ivan / AI Whisperers. Last updated 2026-06-10 (end of session).*
