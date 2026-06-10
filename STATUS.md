# STATUS — La Quebrada Viva render pipeline

> Read at session start. Update the manifest + task list at session end. Last updated: 2026-06-09.

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
9. **Early variant validation** — `lqv/config.py` should reject unknown variants at parse time instead of crashing post-build in lighting.py.
10. **Warn on unknown RENDER_RES** instead of silent preview fallback (`lqv/config.py`).

### Housekeeping
11. `wesly.txt` (unrelated call transcript) and `_archive`-worthy `render.png` (stale toy EEVEE render) are still at project root — ignored via `.claudeignore`/`.gitignore`; Ivan to confirm moving them out.

## Decisions log

- 2026-06-09: Deliverable target set to **12 finals** (A/B×6); Variant C deferred to task 8. Samples policy fixed: 128 preview / 512 hero finals / 256 other finals. No 4K preset — prompt docs' "4K minimum" deferred until requested.
- 2026-06-09: Variant A sun elevation kept at 13° (code) vs 20° (brief) — deliberate aesthetic call.
- 2026-06-09: Git initialized; scene.blend untracked (regenerable from code); final renders tracked.

## Environment

- Blender 4.2.3 LTS on PATH; Cycles GPU autodetect (HIP/ROCm on this machine), CPU fallback.
- blender-mcp available for interactive work; Poly Haven via MCP.
