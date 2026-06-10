# house-field — project instructions

This project renders **La Quebrada Viva**, a cob/bottle earthen smart home on a real stream-side property in **Escobar District, Paraguarí, Paraguay**. Render first; real build eventual.

## Document map — which file is authoritative for what

- `paraguay_clay_house_research.md` — **v2 research, site CONFIRMED (Escobar, Paraguarí)**. Authoritative for location, stream/hydrology, orientation. Supersedes MASTER_BRIEF where they conflict.
- `MASTER_BRIEF.md` — design brief: zones, climate constraints, smart-home stack, flora inventory, Blender tech specs (§12), variants/cameras (§13), the 10 rules (§14).
- `prompt_house_render.md` / `prompt_location_scene.md` — shot-level art direction. They describe a **Variant C (night/blue hour with fireflies) that is NOT implemented in code** — see Variants below.
- `ARCHITECTURE.md` — map of the `lqv/` package + fragility notes. **Read before editing any code.**
- `STATUS.md` — render manifest, open tasks, current state. **Read at session start, update at session end.**
- `claude_code_blender_best_practices.md` — generic tooling reference; read on demand only.

## Current state of the code — do not "fix" what already works

- The renderer is **already Cycles** (`lqv/engine.py:15`) with GPU autodetect, OptiX/OIDN denoise, AgX "Punchy", caustics on. There is no EEVEE anywhere. If a doc says otherwise it is stale.
- `build_scene.py` is a thin driver over the `lqv/` package. The pre-refactor monolith lives at `build_scene.py.pre-refactor.bak` — **reference only, never edit or import it**.

## How to run (use the scripts — they back up scene.blend first)

```bash
scripts/smoke_test.sh                  # build only, no render (RENDER_SKIP=1) — run after any code edit
scripts/render_preview.sh A hero       # 1280x720 preview -> renders/_preview_A_hero.png
scripts/render_final.sh A hero         # full-res final  -> renders/A_hero.png
scripts/render_all_finals.sh           # all 12 finals (A/B x 6 cams)
```

**Every headless run overwrites `scene.blend`** (the script rebuilds the scene from code and saves). The scripts copy `scene.blend` to `scene.blend.session-backup` before running. Never run `blender --background --python build_scene.py` bare without that backup.

Env vars (full reference in `build_scene.py` docstring):
`RENDER_VARIANT=A|B` · `RENDER_CAM=hero|stream_up|terrace|cliff|dusk|petal_macro` · `RENDER_SAMPLES=<int>` · `RENDER_RES=preview|final|hero` · `RENDER_SKIP=1`

**Trap:** an unknown `RENDER_RES` value silently falls back to 1280×720 preview. Only `preview|720`, `final|1080`, `hero|1440` exist. There is no 4K preset; the prompt docs' "4K minimum" is aspirational, current deliverable spec is hero 2560×1440, others 1920×1080.

**Samples policy:** previews 128, hero-camera finals 512, all other finals 256. The scripts set these; don't improvise per session.

## Variants — what exists vs what's planned

- **Variant A — winter golden hour** (hero): lapacho bare + pink bloom, petal carpet, sun NNW (elevation deliberately 13° in code vs brief's 20° — keep), exposure −0.2. IMPLEMENTED.
- **Variant B — morning overcast**: fully leafed, soft diffuse, exposure +0.3. IMPLEMENTED (valley mist still missing — see STATUS.md).
- **Variant C — night/blue hour with fireflies**: in the prompt docs only. **NOT implemented — `RENDER_VARIANT=C` builds the whole scene then crashes in `lqv/lighting.py`.** Do not attempt it; it's a tracked task in STATUS.md. Current deliverable target is **12 finals** (A/B × 6 cams), not 18. The `dusk` camera renders under A/B lighting for now.

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
- `RENDER_VARIANT=C` until lighting.py implements it.

## When you don't know

Check `STATUS.md`, then `ARCHITECTURE.md`, then the doc map above. If the docs are silent, pick a default consistent with rules 1, 2, and 8, note it in the commit message, continue. Don't ask the user to make Blender/engineering decisions.
