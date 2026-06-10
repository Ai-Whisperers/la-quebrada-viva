# STATUS — La Quebrada Viva render pipeline

> Read at session start. Update the manifest + task list at session end. Last updated: 2026-06-10.

## Render manifest (deliverable: 12 finals — A/B × 6 cameras)

Hero-camera finals at 512 samples / 2560×1440; all others at 256 samples / 1920×1080.

| Render | File | Status |
|---|---|---|
| A hero | `renders/A_hero.png` | ☐ not rendered (preview exists: `renders/_preview_A_hero.png`) |
| A stream_up | `renders/A_stream_up.png` | ☐ |
| A terrace | `renders/A_terrace.png` | ☐ |
| A cliff | `renders/A_cliff.png` | ☐ |
| A dusk | `renders/A_dusk.png` | ☐ |
| A petal_macro | `renders/A_petal_macro.png` | ☐ |
| B hero | `renders/B_hero.png` | ☐ |
| B stream_up | `renders/B_stream_up.png` | ☐ |
| B terrace | `renders/B_terrace.png` | ☐ |
| B cliff | `renders/B_cliff.png` | ☐ |
| B dusk | `renders/B_dusk.png` | ☐ |
| B petal_macro | `renders/B_petal_macro.png` | ☐ |

Mark ☑ only after `/verify-render` passes on the final image.

## Open tasks (ranked; pick from the top unless told otherwise)

### Top priority — asset plan
0. **Execute `docs/asset_plan.md` phases 1–8.** Authoritative roadmap for the remaining work: HDRI swap → ground PBR → lapacho generation → Sketchfab flora batch → Rule 7/9/10 props → detail flora → atmosphere polish → render 12 finals. Also documents the 7 blockers and the CC-BY attribution flow (`CREDITS.md`). The numbered tasks below are still valid but are now subsumed by the asset plan's phasing.

### Scene completeness
1. **Wire `scatter_grass_tufts`** — exists in `lqv/flora/bamboo.py` but is never called from the driver/`flora.populate`. Decide placement, respect the RNG-order invariant (append after existing calls, never insert between).
2. **Variant B valley mist** — brief requires mist near the cliff for B; only the variant-agnostic canopy volume exists. Add a B-only ground-fog volume in `lqv/lighting.py`.
3. **Lapacho trunk material** — uses `MAT['mango_trunk']`; give lapacho its own bark material (flagged in `lqv/flora/lapacho.py` docstring).
4. **Stream zones** — brief defines 5 zones (gorge, flat sandstone pool, colonial weir, channeled riparian, bamboo belt); code has a straight channel + pool + cascades. The **weir** is the biggest visible gap (also rule 7's micro-hydro anchor).
5. **Anthurium epiphytes** — in species list, not modelled.
6. **Rule-7/9/10 props for detail shots** — micro-hydro at weir, solar on separate steel frame, meshed cistern. Needed before any close-up/detail finals.
7. **Pindo trunk texture** — retained leaf bases (rough trunk), currently smooth + noise.

### Pipeline
8. **Variant C (night/blue hour, fireflies)** — extend `lqv/lighting.py` (moonlight + emission particles + window glow), add C exposure in driver, then extend the manifest to 18 finals. Until then `RENDER_VARIANT=C` crashes after a full build.
9. ~~Early variant validation~~ DONE 2026-06-09 (`84d53f1`): `lqv/config.py` raises SystemExit at parse time for unknown variants.
10. ~~Warn on unknown RENDER_RES~~ DONE 2026-06-09 (`84d53f1`): `lqv/config.py` prints WARNING + valid set instead of silent preview fallback.

### Housekeeping
11. ~~`wesly.txt` / `render.png` cleanup~~ DONE 2026-06-09: `wesly.txt` moved out of the project, `render.png` + pre-refactor backups moved to `_archive/` (ignored by git and Claude). Reference docs now live in `docs/`.

### Fixed regressions (verified on preview render)
- 2026-06-10: ~~Lapacho petals floating mid-air~~ VERIFIED on `renders/_preview_A_petal_macro.png` (commit `8949646`). BVH-on-evaluated-ground raycast in `lqv/flora/lapacho.py` + ±0.25 rad XY tilt jitter + σ=1.2 cluster at (-3,-10) + Cam_PetalMacro reframed to 50mm @ 3.5m. RNG-draw order preserved.
- 2026-06-10: ~~Footbridge floating disconnected~~ Fixed (commit `c93748f`) — two hardcoded sandstone abutments in `lqv/site/stream.py`. Visual verification deferred to next `A hero` preview render.

## Decisions log

- 2026-06-09: Deliverable target set to **12 finals** (A/B×6); Variant C deferred to task 8. Samples policy fixed: 128 preview / 512 hero finals / 256 other finals. No 4K preset — prompt docs' "4K minimum" deferred until requested.
- 2026-06-09: Variant A sun elevation kept at 13° (code) vs 20° (brief) — deliberate aesthetic call.
- 2026-06-09: Git initialized; scene.blend untracked (regenerable from code); final renders tracked.
- 2026-06-10: Ground sampled via BVHTree for petal placement; bridge given visible stone abutments. Strategy notes: when other ground-relative props get added (anthurium epiphytes on root flares, grass tufts, agave clumps), reuse the same evaluated-depsgraph BVH lookup pattern. Cheap (100 petals + 2 piers built fine in <2s); scales linearly.

## Environment

- Blender 4.2.3 LTS on PATH; Cycles GPU autodetect exists in `lqv/engine.py` but **this machine renders on CPU** — AMD RX 6400 (Navi 24) + Vega iGPU present, no ROCm/HIP runtime installed (verified 2026-06-09: `device=CPU backend=None`). Budget render times accordingly. Optional speedup: install AMD's HIP runtime (system-level, sudo — Ivan's call).
- blender-mcp available for interactive work; Poly Haven via MCP.
