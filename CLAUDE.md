# house-field — project instructions

This project supports **Wesley van de Camp** in visualizing a real 62-ha property in **Escobar District, Paraguarí, Paraguay**, on which Wesley plans a **housing park + restaurant + amenities**. The current 3D work renders **La Quebrada Viva**, a cob/bottle earthen house that's the first example building typology on the site. Renders are concept art; the site model is the durable deliverable. See `docs/HOUSING_PARK_CONCEPT.md` for the full vision and `docs/CLIENT.md` for who Wesley is.

## Document map — which file is authoritative for what

- `docs/CLIENT.md` — **Wesley van de Camp = client & 75% owner** (Thijs = 25% co-buyer, not the design client); AI Whisperers (Ivan) = digital support lead. Sellers, notary, intermediary, **escritura deadline 2026-06-27**. Read first for "who is this for".
- `docs/HOUSING_PARK_CONCEPT.md` — **Wesley's expanded vision (2026-06-10)**: 62 ha as a housing park + restaurant + amenities in Escobar, Paraguarí. 8 concept models, restaurant deep-dive, Paraguay-specific legal/tax/cultural/climate considerations, phasing, **25 open questions for Wesley**, suggested next steps. The current cob/bottle design is one example house on the larger site, not the whole vision.
- `docs/wesley_brief_onepager.md` — **DRAFT one-pager for the 27 Jun escritura signing** (short version of HOUSING_PARK_CONCEPT). Will be polished once Wesley answers the 5 priority questions.
- `docs/EUROPEAN_TOURISM_SPEC.md` — **Refined direction (2026-06-10, latest)**: houses-first vacation rentals for European / 1st-world travelers, restaurant later (European + Dutch, sourced via San Bernardino + German community). Style blend: resort + events + eco-natural retreat. Deep Paraguay research: target market, San Bernardino / German / Dutch community supply chain, comparable properties, vacation-rental typology, events, eco positioning, restaurant plan, regulatory (SENATUR / SET / municipal), marketing channels, refined phasing, 26 open questions.
- `docs/RESEARCH_GAPS.md` — **Living tracker of what we still need to find out**. 34 items across 5 tiers, with status (🔴 open / 🟡 in-progress / 🟢 done / ⚫ blocked), owner (W / I / A / H / L), source, effort. Tier 1 (8 items) targets the 27 Jun closing. Findings log at the bottom. This is the action list.
- `docs/SESSION_LOG.md` — **Narrative log of the 2026-06-10 session** (the one that produced all the planning docs). What was created, decisions made, what's at risk, what's next. Read after a break to re-orient.
- `docs/research/README.md` — **Research synthesis 2026-06-10** (5 sub-reports, ~80 repos catalogued). Includes 10 design rules, 5 site-selection criteria, 5 case studies (Chaa Creek / Awasi / Inkaterra / San Bernardino / Mennonite colonies), Tier-1/2/3 GIS layers, GEDI tooling, Blender GIS, Earthdata auth + cloud-pool EULA diagnosis. The "what to adopt / not adopt" punchlist is at the bottom.
- `docs/site_data/DATA_INVENTORY.md` — **Clear-language reference of all the data we got from NASA + OpenTopography** (4 DEMs, GEDI L2A, derived analyses). For Wesley read-through — explains each dataset, what it shows, key findings, cross-validation, what's still missing, scripts to re-fetch.
- `docs/research/REPO_CATALOG.md` — **141 GitHub repos across 6 domains** (Blender GIS, geospatial Python, NASA Earthdata, real estate, Paraguay/Atlantic Forest, vegetation 3D), each with verdict (adopt / reference / skip / dead). The 51/97 user-supplied URLs that were 404 are flagged honestly. Top 10 to drop in: pysheds, pyflwdir, whitebox-python, earthaccess, nasa/GEDI-Data-Resources, simonbesnard1/gedidb, joewdavies/geoblender, johnbalvin/pyairbnb, ics-py, melizeche/dolarPy.
- `docs/AI_WHISPERERS_STYLE.md` — **Ivan's communication & execution rules** (self-improvement, learned 2026-06-10). Read first by every AI Whisperers session working on this project. No preambles, no narration, one complete deliverable per message.
- `docs/AI_WHISPERERS_STYLE.md` — **Ivan's communication & execution rules** (self-improvement, learned 2026-06-10). Read first by every AI Whisperers session working on this project. No preambles, no narration, one complete deliverable per message.
- `docs/MASTER_BRIEF.md` §16-19 — Vacation-rental synthesis added: 5 site-selection criteria, 5 case studies, 10 eco-retreat design rules, Tier-1/2/3 GIS layers. §1-15 unchanged (the cob design rules + render spec).
- `docs/contract_summary.md` — quick-reference for the 2026-04-28 boleto privado. Greppable parcel/price/penalty table. Full text: `docs/2026-04-28_boleto_compraventa_torrasca-vandecamp.pdf`.
- `docs/CLOSING_DAY_PREP.md` — printable actionable T-7 / T-5 / T-2 / signing-day / T+30 checklist for the 27 Jun escritura signing, with risk register. Companion to `contract_summary.md`.
- `docs/paraguay_clay_house_research.md` — **v2 research, site CONFIRMED (Escobar, Paraguarí)**. Authoritative for location, stream/hydrology, orientation. Supersedes MASTER_BRIEF where they conflict.
- `docs/MASTER_BRIEF.md` — design brief: zones, climate constraints, smart-home stack, flora inventory, Blender tech specs (§12), variants/cameras (§13), the 10 rules (§14). **Owner line (Ivan) is the architect/visualizer — not the legal landowner.** Land is Thijs + Wesley's per `CLIENT.md`.
- `docs/prompt_house_render.md` / `docs/prompt_location_scene.md` — shot-level art direction. They describe a **Variant C (night/blue hour with fireflies) that is NOT implemented in code** — see Variants below.
- `ARCHITECTURE.md` — map of the `lqv/` package + fragility notes. **Read before editing any code.**
- `STATUS.md` — canonical current state (render manifest, vision summary, doc inventory, open tasks, decisions log, critical dates, next session priorities). **Read at session start, update at session end.**
- `docs/claude_code_blender_best_practices.md` — generic tooling reference; read on demand only.

### Supplementary docs (Tier 2 — planning + research artefacts, 2026-06-10 mega-session)

These supplement the primary Document map above; named here so future sessions can discover them without grep. Authority remains with the primary-map docs when they conflict.

- `docs/master_plan.md` — original asset-import + phase plan that drove the 2026-06-10 work (Phases 1-8). Forward source-of-truth for the import ordering; downstream consumers are `asset_plan.md` §G and `external_assets.md`.
- `docs/asset_plan.md` — per-phase asset shortlist with §§A/B/C breakdowns and §C.4 Hyper3D prompt archive. §G is the phase plan.
- `docs/external_assets.md` — per-asset download register; `[USED]` vs `[PLANNED]` ledger. Cross-references `LICENSES/README.md` (legal-text backing-store) and `CREDITS.md` (attribution lines).
- `docs/research_index.md` — index of the ~80 catalogued repos from `docs/research/`; ASCII-tree navigation.
- `docs/photographic_references.md` — separate license framework for reference photography in `assets/references/` (parallel to `LICENSES/README.md`, but for reference photos not assets).
- `docs/cultural_notes.md` — Paraguayan cultural specifics underlying Rule 8 (corredor / tatakuá / tereré / mate / lapacho timber semantics). Reciprocal of CLAUDE.md "Plant species" + "Material color references" sections.
- `docs/build_sequence.md` — physical construction phasing for the cob/bottle house (foundation → cob courses → bottle wall → roof → finishes). Pairs with `docs/bom.md`.
- `docs/floor_plan.md` / `docs/section_view.md` — 2D drawings (plan + section) backing the procedural geometry in `lqv/house/`.
- `docs/site_data_spike.md` — site survey constants (UTM coordinates, elevation, stream profile, escarpment line y=20, footbridge y=−25.5). Reciprocal to `ARCHITECTURE.md` "Positional coupling" invariant.
- `docs/bom.md` — bill of materials for the cob house (rough quantities). Pairs with `build_sequence.md`.
- `docs/energy_budget.md` — Rule 7 + Rule 9 energy stack (micro-hydro + LiFePO4 + PV) sizing notes.
- `docs/license_obligations.md` — narrative of how each license obligation (CC0 traceability, CC-BY 4.0 attribution, CC-BY-SA exclusion) is satisfied at distribution time. Reciprocal of `LICENSE_BUNDLE.md` §§1-6 and `LICENSES/README.md`.
- `docs/housing_park_phasing.md` — 5-year phase plan for the broader 62-ha housing park (downstream of `HOUSING_PARK_CONCEPT.md`). Independent of the cob-house render delivery.
- `docs/wesley_deliverable_bundle.md` — Tier 1 / Tier 2 / Tier 3 packaging spec for the Wesley deliverable. Tier 2 USB bundle includes `CREDITS.md`, `LICENSE_BUNDLE.md`, `LICENSES/` directory.
- `docs/research/README.md` is the synthesis; `docs/research/*.md` are the sub-reports (already linked via that README).
- `CREDITS.md` (repo root) — per-asset attribution lines (CC-BY 4.0 required, CC0 traceability).
- `LICENSE_BUNDLE.md` (repo root) — per-license summary + bundle-readiness checklist. Cross-references CLAUDE.md "Things to refuse / push back on" for the CC-BY-SA exclusion rationale.
- `LICENSES/README.md` — verbatim CC0-1.0 + CC-BY-4.0 legal-code mirror (offline-complete legal corpus for the redistribution bundle). The triple `CREDITS.md` + `LICENSE_BUNDLE.md` + `LICENSES/README.md` together satisfies CC-BY 4.0 attribution at distribution time (this is *why* the bundle-readiness gates in LICENSE_BUNDLE.md §6 are written the way they are).
- `LICENSE` (repo root) — MIT license for `lqv/`, `build_scene.py`, `scripts/`, `docs/` code. Does NOT cover `assets/` or `renders/`.

## Current state of the code — do not "fix" what already works

- The renderer is **already Cycles** (`lqv/engine.py:15`) with GPU autodetect, OptiX/OIDN denoise, AgX "Punchy", caustics on. There is no EEVEE anywhere. If a doc says otherwise it is stale.
- `build_scene.py` is a thin driver over the `lqv/` package. The pre-refactor monolith lives at `_archive/build_scene.py.pre-refactor.bak` — **reference only, never edit or import it**. `_archive/` holds stale artifacts; ignore it.

## How to run (use the scripts — they back up scene.blend first)

```bash
scripts/smoke_test.sh                  # build only, no render (RENDER_SKIP=1) — run after any code edit
scripts/render_preview.sh A hero       # 1280x720 preview -> renders/_preview_A_hero.png
scripts/render_final.sh A hero         # full-res final  -> renders/A_hero.png
scripts/render_all_finals.sh           # all 18 finals (A/B/C x 6 cams)
```

**Every headless run overwrites `scene.blend`** (the script rebuilds the scene from code and saves). The scripts copy `scene.blend` to `scene.blend.session-backup` before running. Never run `blender --background --python build_scene.py` bare without that backup.

Env vars (full reference in `build_scene.py` docstring):
`RENDER_VARIANT=A|B|C` · `RENDER_CAM=hero|stream_up|terrace|cliff|dusk|petal_macro` · `RENDER_SAMPLES=<int>` · `RENDER_RES=preview|final|hero` · `RENDER_SKIP=1`

**Trap:** an unknown `RENDER_RES` value silently falls back to 1280×720 preview. Only `preview|720`, `final|1080`, `hero|1440` exist. There is no 4K preset; the prompt docs' "4K minimum" is aspirational, current deliverable spec is hero 2560×1440, others 1920×1080.

**Samples policy:** previews 128, hero-camera finals 512, all other finals 256. The scripts set these; don't improvise per session.

## Variants — what exists vs what's planned

- **Variant A — winter golden hour** (hero): lapacho bare + pink bloom, petal carpet, sun NNW (elevation deliberately 13° in code vs brief's 20° — keep), exposure −0.2. IMPLEMENTED.
- **Variant B — morning overcast**: fully leafed, soft diffuse, exposure +0.3. IMPLEMENTED (valley mist still missing — see STATUS.md).
- **Variant C — night/blue hour with fireflies**: IMPLEMENTED 2026-06-10. Cool moonlight + low blue sky strength (`lqv/lighting.py`), warm window-glow emission planes inside the cob cutouts (`lqv/house/cob.py:build_window_emission`), ~80 firefly emission spheres scattered over corredor + lower terrace (`lqv/flora/fireflies.py`). Variant C exposure +0.6 in `build_scene.py`. Deliverable target is now **18 finals** (A/B/C × 6 cams).

## The 10 design rules (MASTER_BRIEF §14) — never violate

1. **No right angles in cob walls** — organic sculpted forms only (bmesh + subdiv + displacement, never box modeling).
2. **No cement plaster on cob** — always lime; must read as lime-washed earth.
3. **No standing water anywhere** — dengue protocol. No puddles, no open cisterns. (The flat-rock stream pool is a mandated landscape feature, not a violation.)
4. **Earthen walls never touch ground** — raised stone foundation, 60cm minimum.
5. **Wide overhangs (90cm+) on all sides.**
6. **Passive design ≤ 35°C** — corredor + cross-ventilation + thermal mass; AC hidden.
7. **Critical systems outage-proof** — micro-hydro + LiFePO4 visible in detail shots.
8. **Culturally Paraguayan first** — corredor, tatakuá, courtyard, low-pitched roof, lapacho timber. Not Tuscan, not Bali, not Earthship-generic.
9. **Solar on separate steel frame** — never on the living sod roof.
10. **All cisterns mosquito-proofed** — 0.5mm stainless mesh visible on any tank.

## Material color references (from photographs — do not improvise)

- Red laterite soil: `#8B3A1F` to `#A85832`
- Moss on sandstone terraces: `#5F7A3D` to `#8AA055`
- Sandstone/quartzite boulders: `#5A5448` to `#7A7268`
- Atlantic Forest canopy: `#2F4A1E` to `#4A6B2A`
- Stream water over bedrock: dark `#3A4538`, over laterite `#A85832` shallows
- Lapacho flowers (winter variant): hot pink `#E85A8C` to `#F0A0C8`

## Plant species — critical accuracy notes

- **Pindo palm** (*Syagrus romanzoffiana*): plumose **drooping** fronds. NOT coconut, NOT stiff date palm. Trunk has retained leaf bases.
- **Lapacho** (*Handroanthus impetiginosus*): deciduous; bare-branched + hot-pink trumpet flowers in winter. Variant A must show this; Variant B must not.
- **Mango**: dominant canopy, dense dark-green rounded crown.
- **Tree ferns** (*Cyathea*): riparian shade, 2–4m, fronds 1.5m+.
- **Bamboo** (*Guadua*/*Chusquea*): clumping along stream, NOT running bamboo.
- **Agave** (*Agave americana*): colonizing lower terraces, not a designed succulent garden.
- **Anthurium plowmanii**: epiphytes on trunks near stream (not yet modelled — STATUS.md).

## Code invariants — break these and renders silently change

1. **RNG seed ordering**: `random.seed()` in `build_scene.py` must stay AFTER `materials.build_materials()` and BEFORE the first `build_*` call. Never reorder the build calls, never add `random.*` upstream of the seed.
2. **`MAT` registry** (`lqv/materials.py`): string-keyed global; builders do `MAT['key']` at call time. `build_materials()` must run first; a typo'd key is a runtime KeyError.
3. **Positional coupling**: hero camera aim ↔ pool position ↔ footbridge y=−25.5 ↔ escarpment y=20 are mutually tuned. Don't move one without checking the others (see ARCHITECTURE.md).
4. **Hidden `WindowCut_*` objects** are live Boolean cutters — never unhide, rename, or delete them.
5. Previews skip the canopy volume, so preview atmosphere ≠ final atmosphere. Eyeball geometry/materials on previews; judge volumetrics only on finals.

## Tool scope

- **Interactive scene work**: blender-mcp (`mcp__blender__execute_blender_code`, `get_viewport_screenshot`, `get_scene_info`). Interactive edits are throwaway — the headless build regenerates the scene from code, so anything worth keeping must land in `lqv/`.
- **Finals**: headless via the `scripts/` wrappers only.
- **Assets**: Poly Haven via `mcp__blender__search_polyhaven_assets` / `download_polyhaven_asset`.

## Verification before claiming a render is done

Use the `/verify-render` skill. Short version: preview first → check the 10 rules + species accuracy on the image itself → only then render final → save to `renders/<variant>_<cam>.png` → update STATUS.md manifest.

## Git

This is a git repo. Commit after every working change (`git add -A && git commit`). `scene.blend`, previews, and backups are gitignored; final renders are tracked. Before risky code edits, commit first so `git checkout -- lqv/` can recover.

## Things to refuse / push back on

- EEVEE for final renders (preview viewport only).
- Modeling the house as boxes/cubes (rule 1).
- Solar panels on the living roof (rule 9).
- "Tuscan villa", "Bali resort", "Earthship" framing (rule 8).

## When you don't know

Check `STATUS.md`, then `ARCHITECTURE.md`, then the doc map above. If the docs are silent, pick a default consistent with rules 1, 2, and 8, note it in the commit message, continue. Don't ask the user to make Blender/engineering decisions.

## Critique-derived standing rules (additive 2026-06-10)

Synthesised from `docs/CRITIQUE_2026-06-10.md` + `docs/UPGRADE_PLAN.md` + `docs/sub_render_strategy.md`. These are additive; they supersede any conflicting older guidance above without removing it (per the additions-only directive).

1. **Sub-render-first is the default workflow** for any new asset / typology / amenity. The monolithic `build_scene.py` is only for the final composite. See `docs/sub_render_strategy.md` — `lqv/subscene/<asset>.py` drivers + per-asset RNG derivation + `renders/sub/<asset>_<variant>.png` outputs. 31-target queue covers 5 house + 5 landscape + 7 flora + 8 typology + 6 amenity.
2. **Push to GitHub remote** before further doc work — escritura is 2026-06-27 (single-disk SPOF risk on a 17-day window). UPGRADE_PLAN.md T0.1. The repo currently has no remote; this is the highest-priority infra task.
3. **RNG invariant must be tested** (UPGRADE_PLAN T1.2 — `tests/test_rng_invariants.py`) before any `build_scene.py` reorder or touch. The composite seed ordering is load-bearing for byte-identity across the 18 finals at `85e86aa`.
4. **Doc consolidation > doc extension** — before adding a back-pointer or new research doc, check if an existing doc can absorb it. The mesh has reached 15-node bidirectional closure; further extensions risk over-indexing.

**Standing reminders (additive)**:
- Escritura date: **2026-06-27**. Tier 0 of `docs/UPGRADE_PLAN.md` is everything that must land before that date.
- Line 133's `git add -A && git commit` is **superseded** by the explicit-staging-only policy (NEVER `git add -A` or `git add .`). Stage files by name; `scripts/mcp_daemon.py` always excluded; `docs/site_data/sentinel2/*.tif` gitignored as regenerable; `docs/*_boleto_*.pdf` / `docs/*_escritura_*.pdf` / `docs/2026-*_*.pdf` always excluded.
- The duplicate `docs/AI_WHISPERERS_STYLE.md` entry at lines 16/17 is known and deferred per the additions-only directive — flagged here for future cleanup, not removed now.
- Renderer byte-identity invariant: do not touch `lqv/scatter_lapacho_petals` without explicit user authorization. Task #1 (floating petals on `_petal_macro` finals) is deferred for the same reason — fixing it would supersede `85e86aa`.
- MCP socket is dead this session — `mcp__blender__*` calls will fail. Tasks #10 + #12 remain blocked until the socket is revived.
