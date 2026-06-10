# STATUS — La Quebrada Viva render pipeline

> Read at session start. Update the manifest + task list at session end. Last updated: 2026-06-10.

## Render manifest (deliverable: 12 finals — A/B × 6 cameras)

Hero-camera finals at 512 samples / 2560×1440; all others at 256 samples / 1920×1080.

| Render | File | Status |
|---|---|---|
| A hero | `renders/A_hero.png` | ☑ 2026-06-10 (512 samples, 2560×1440, verified) |
| A stream_up | `renders/A_stream_up.png` | ☑ 2026-06-10 (256 samples, 1920×1080) |
| A terrace | `renders/A_terrace.png` | ☑ 2026-06-10 (256 samples, 1920×1080) |
| A cliff | `renders/A_cliff.png` | ☑ 2026-06-10 (256 samples, 1920×1080) |
| A dusk | `renders/A_dusk.png` | ☑ 2026-06-10 (256 samples, 1920×1080, verified) |
| A petal_macro | `renders/A_petal_macro.png` | ☑ 2026-06-10 (256 samples, 1920×1080, verified) |
| B hero | `renders/B_hero.png` | ☑ 2026-06-10 (512 samples, 2560×1440, verified valley mist reads) |
| B stream_up | `renders/B_stream_up.png` | ☑ 2026-06-10 (256 samples, 1920×1080) |
| B terrace | `renders/B_terrace.png` | ☑ 2026-06-10 (256 samples, 1920×1080, verified mist) |
| B cliff | `renders/B_cliff.png` | ☑ 2026-06-10 (256 samples, 1920×1080, verified mist) |
| B dusk | `renders/B_dusk.png` | ☑ 2026-06-10 (256 samples, 1920×1080) |
| B petal_macro | `renders/B_petal_macro.png` | ☑ 2026-06-10 (256 samples, 1920×1080) |

12/12 finals delivered. Spot-verified A_hero, B_hero, A_petal_macro, A_dusk, B_terrace, B_cliff against the 10 design rules + Phase 6 additions (grass tufts, valley mist, anthurium, pindo bark, bridge abutments). All pass.

## Open tasks (ranked; pick from the top unless told otherwise)

### Top priority — asset plan
0. **Execute `docs/asset_plan.md` phases 1–8.** Authoritative roadmap for the remaining work: HDRI swap → ground PBR → lapacho generation → Sketchfab flora batch → Rule 7/9/10 props → detail flora → atmosphere polish → render 12 finals. Also documents the 7 blockers and the CC-BY attribution flow (`CREDITS.md`). The numbered tasks below are still valid but are now subsumed by the asset plan's phasing.

### Scene completeness
1. ~~Wire `scatter_grass_tufts`~~ DONE 2026-06-10 (Phase 6): `flora.scatter_grass_tufts(n=80)` appended in `build_scene.py` **after** `scatter_lapacho_petals` so the petal RNG draw stays byte-identical to baseline. Grass consumes RNG state that was otherwise unused.
2. ~~Variant B valley mist~~ DONE 2026-06-10 (Phase 6): `lighting.build_valley_mist(variant, skip)` added — B-only Volume Scatter cube at (11,-10,0.3) scale (8,30,2), density 0.04, anisotropy 0.3. Sits in z=-0.7…+1.3 (below canopy volume z=4…14 → no double-scatter overlap). Skipped on previews like canopy volume — judge on finals.
3. **Lapacho trunk material** — uses `MAT['mango_trunk']`; give lapacho its own bark material (flagged in `lqv/flora/lapacho.py` docstring). _Note 2026-06-10: stale relative to Phase 3 — task 9/12 (Hyper3D lapacho) would obsolete this entirely. Defer; revisit only if Hyper3D path is abandoned._
4. ~~Stream zones — weir~~ DONE 2026-06-10: weir (3 sandstone blocks at y=-11.0, x∈{-1.2,0,+1.2}+11, centre block notched lower for spillway) + penstock + pelton housing + tailrace in `lqv/site/stream.py`. Channel + pool + cascades + weir + bridge now read as 4 of the 5 brief zones; gorge headwall + bamboo belt are the remaining gaps.
5. ~~Anthurium epiphytes~~ DONE 2026-06-10 (Phase 6): new module `lqv/flora/anthurium.py` with `scatter_anthuriums()` + `_add_rosette()` helper. Hardcoded 4 trunks (-3,-10), (8,-14), (-18,0), (22,-22) at mid-trunk z=3.0–4.0, 5–7 strappy leaves per rosette tilted 28–58°. New material `MAT['anthurium_leaf']` (#2E4A1E principled, SSS 0.08). Appended after `scatter_grass_tufts` in `build_scene.py`.
6. ~~Rule-7/9/10 props for detail shots~~ DONE 2026-06-10 (Phase 5): micro-hydro at weir (penstock + pelton housing + tailrace), solar PV on separate anodized-steel frame in east yard (4 posts x∈{+7.5,+9.5} y∈{-2,+2}, south posts 3.2m / north 1.6m → 21.8° tilt, panel→`MAT['pv_glass']`), cob cistern with 0.5mm steel-mesh cap + anodized rim + downspout at (-9,+5), LiFePO4 battery cabinet at (-11.4,+5), tatakuá enhanced with chimney + lip + ash door + firewood pile. All builders deterministic — no `random.*` — RNG-draw order preserved.
7. ~~Pindo trunk texture~~ DONE 2026-06-10 (Phase 6): second DISPLACE modifier on each pindo trunk in `lqv/flora/pindo.py` — fine-scale CLOUDS (noise_scale=0.55) at strength 0.035, layered atop the existing add_subdiv_displace. Reads as Syagrus retained leaf-base scarring. Deterministic — no `random.*`.

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
- 2026-06-10 (Phase 5): rule-7/9/10 props slotted **after** `build_stream()` and **before** `flora.populate()` in `build_scene.py`. All three new builders (`build_services`, weir/pelton additions in `build_stream`, tatakuá enhancements) are hardcoded — they make zero `random.*` calls — so the RNG draw order for `flora.populate` + `scatter_lapacho_petals` is byte-identical to pre-Phase-5. New materials: `steel_anodized`, `pv_glass`, `steel_mesh` in `lqv/materials.py`. Solar tilt computed from south/north post heights (`atan2(1.6, 4.0) ≈ 21.8°`) — close to Paraguarí ≈25°S optimum. Cistern NW utilities corner pairs with east-side weir/pelton: outage-proof power stack reads as paired on hero + terrace cams.
- 2026-06-10 (Phase 6): scene completeness sweep — items 1, 2, 5, 7 landed. Order in `build_scene.py` is now: `…populate → scatter_lapacho_petals (A only) → scatter_grass_tufts → scatter_anthuriums → setup_world_and_sun → build_canopy_volume → build_valley_mist`. **RNG-order strategy:** new random consumers (grass + anthurium) sit AFTER the petal draw, not inside `flora.populate`, so the petal scatter and all upstream flora positions stay byte-identical to pre-Phase-6. `build_valley_mist` skipped on previews (same policy as `build_canopy_volume`), so the new mist is only visible in finals. Pindo retained-leaf-base scars: a SECOND DISPLACE modifier on the existing trunk mesh density — no extra subdiv pass, keeps poly count flat. Item 3 (lapacho trunk material) deliberately deferred — Hyper3D phase will replace the procedural lapacho wholesale and that'd throw away any bark material work done now.

## Environment

- Blender 4.2.3 LTS on PATH; Cycles GPU autodetect exists in `lqv/engine.py` but **this machine renders on CPU** — AMD RX 6400 (Navi 24) + Vega iGPU present, no ROCm/HIP runtime installed (verified 2026-06-09: `device=CPU backend=None`). Budget render times accordingly. Optional speedup: install AMD's HIP runtime (system-level, sudo — Ivan's call).
- blender-mcp available for interactive work; Poly Haven via MCP.
