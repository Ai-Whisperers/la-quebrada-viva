# AUTONOMOUS_PLAN — La Quebrada Viva ultrawork (2026-06-13 → 2026-06-27)

Source-of-truth plan at `/home/ai-whisperers/.claude/plans/glimmering-tumbling-fiddle.md`
(Phases A–H **complete** at `85e86aa`). This file tracks the post-A→H asset-pivot +
project-roast/improvement-plan ultrawork wave.

## Goal

1. Push downloaded asset count past **200** (currently 132 unique IDs on disk).
2. Analyze every asset, integrate the top picks into LQV builders via sub-render-first
   workflow.
3. Honest roast of the entire project (critic), translate findings into a numbered
   improvement plan, implement the plan.

Escritura T-14 days. Phase H polish (4-elevation renders + deck rebuild) is the only
hard blocker for the escritura PDF; everything else here is "make-the-deck-better"
infra.

## Items (TaskList IDs, ordered)

### Wave 1 — dispatch parallel (cap-4)

- **W1a — critic / #79** — Roast review of repo + lqv/ + scripts/ + docs/. Output
  `docs/CRITIQUE_2026-06-13.md` (file_path:line_number specificity). Then synthesize
  ranked plan to `docs/IMPROVEMENT_PLAN_2026-06-13.md` (P0/P1/P2).
- **W1b — autonomous-worker / #72** — Extend `scripts/download_polyhaven_assets.py`
  with ≥80 new verified-CC0 Poly Haven slugs. Build sibling
  `scripts/download_ambientcg_assets.py` for ≥40 ambientCG IDs. Run both. Write
  per-asset stubs to `LICENSES/<id>.txt`. Persist research notes to
  `docs/research/ASSET_RESEARCH_2026-06-13.md`. Target ≥200 unique IDs on disk.
- **W1c — autonomous-worker / #75** — Sub-render-first flora photoreal drivers:
  `lqv/subscene/flora_jacaranda.py`, `flora_anthurium.py`, `flora_pachira.py`
  following `lqv/subscene/hobbit_house.py` pattern (clip_end=20000, A/B/C variants,
  base.setup→place_neutral_ground→cameras.subscene_camera→base.save_subrender).
- **W1d — autonomous-worker / #76 + #77 + #78 bundle** —
  - boulder cluster `lqv/subscene/boulder_cluster.py` (boulder_01 +
    namaqualand_boulder_02/03/04) → integrate into `lqv/amenities/labrisa_lounge.py`
    seating
  - dusk HDRI compare `lqv/subscene/hdri_dusk_compare.py` (qwantani_dusk_2 vs
    bambanani_sunset vs qwantani_sunset_puresky)
  - brick/clay material registration in `lqv/materials/` (red_brick_03 +
    castle_brick_02_red + clay_block_wall + clay_plaster) + wall-panel compare

### Wave 2 — after Wave 1 (dispatch fresh cap-4)

- **W2a — autonomous-worker / #80** — Implement P0+P1 items from
  `docs/IMPROVEMENT_PLAN_2026-06-13.md`. Defer P2 unless on critical path.
- **W2b — autonomous-worker / #68** — Phase H polish: 4-elevation Dutch renders for
  13 typologies + rebuild `scripts/build_escritura_deck.py`.
- **W2c — autonomous-worker** — Re-run `scripts/analyze_assets.py` to refresh
  `docs/ASSETS_INVENTORY.csv` + `docs/ASSETS_INTEGRATION_PLAN.md`.
- **W2d — critic** — Final pass: "is the deck shippable for 2026-06-27?"

## Acceptance

- ≥200 unique CC0 / CC-BY 4.0 IDs on disk under `assets/{hdris,textures,models}/`.
- Every new asset has matching `LICENSES/<id>.txt` stub.
- Per-asset sub-renders exist at `renders/sub/latest/<asset>_A.png` for each Phase
  D-1/D-2 pick.
- `docs/CRITIQUE_2026-06-13.md` exists with ≥30 specific findings (file:line).
- `docs/IMPROVEMENT_PLAN_2026-06-13.md` exists with P0/P1/P2 ranking.
- All P0 + P1 implemented (or explicitly deferred with reason).
- `scripts/smoke_test.sh` exits 0.
- `scripts/build_boq.py` produces non-zero CSV/MD.
- `scripts/build_escritura_deck.py` produces non-zero PDF.

## Stop conditions

- All acceptance criteria met → final report.
- Same error repeats 3× → document blocker, move on, surface in final report.
- Resource exhaustion (disk >90%, API hard rate-limited) → pause + surface.
- Destructive op needed (delete branches, rotate creds, force-push, drop tables) →
  pause + ask.
- Escritura deadline 2026-06-27 reached with MVP floor met → stop + report.

## Hard constraints (carried, non-negotiable)

- License CC0 + CC-BY 4.0 ONLY (no CC-BY-SA, no CC-BY-NC).
- Sub-render-first workflow for every new asset/typology/amenity.
- Renderer byte-identity at `85e86aa` preserved — zero edits to `build_scene.py`.
- Never `git add -A` / `git add .` — explicit staging only.
- Never stage `scripts/mcp_daemon.py`, `docs/site_data/sentinel2/*.tif`,
  `docs/*_boleto_*.pdf`, `docs/*_escritura_*.pdf`, `docs/2026-*_*.pdf`.
- Never commit unless user explicitly asks. Conventional Commits +
  `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`.
- Don't touch `lqv/scatter_lapacho_petals*` or hidden `WindowCut_*` cutters.
- Subscene clip_end = 20000.0 for parcel-scale.
- Sub-render output: `renders/sub/runs/<RENDER_RUN_ID>_<asset>[_<tag>]/<variant>.png`
  mirrored to `renders/sub/latest/`.
- MCP socket dead — no `mcp__blender__*` calls; direct URL downloads only.
- RNG: `random.seed()` AFTER `materials.build_materials()` BEFORE first `build_*`.
- Currency USD primary, PYG @ 7300/USD secondary.
- cap-4 ceiling on parallel autonomous-workers.

## Delegation pattern

- `autonomous-worker` × cap-4 (Wave 1: 3 + Wave 2: ≤4)
- `critic` × 2 (Wave 1 entrance roast + Wave 2 final pass)
- `asset-researcher` × on-demand inside Wave 1 worker if it stalls
