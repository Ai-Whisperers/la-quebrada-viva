# La Quebrada Viva — Master Plan

> Single source of truth for what the scene should ultimately contain, what is already shipped, what is missing, and how the remaining work is sequenced. Supersedes the scattered roadmap notes in `STATUS.md` and `docs/asset_plan.md` for high-level planning; those remain authoritative for fine-grained task tracking.

Last updated: 2026-06-10.

---

## 1. Current state — what is already in the scene

12/12 finals delivered for Variants A (winter golden hour, lapacho bloom) and B (morning overcast, full leaf) across all six cameras (`hero`, `stream_up`, `terrace`, `cliff`, `dusk`, `petal_macro`). Hero finals at 512 samples / 2560×1440; others at 256 / 1920×1080.

Scene contents — verified by spot-check against the 10 design rules:

- **Earthworks**: sculpted laterite ground (`build_ground`), terraced sandstone retaining walls (`build_terraces`), 20m escarpment headwall at y=+20 (`build_escarpment`).
- **Stream system**: channel + flat-rock pool at (11,-22), cascades, micro-hydro weir at y=-11 with notched centre stone, penstock + Pelton housing + tailrace, sandstone footbridge with abutments at y=-25.5.
- **House**: cob U-plan walls (organic, no right angles) on a 60cm raised foundation; lime-washed; four window cut-outs with lapacho sills (south corredor pair + east/west external pair); low-pitch sod roof with 0.9m+ overhangs and lapacho rafters; corredor on five posts.
- **Bottle wall** (`build_bottle_wall`): cobalt/amber/green/brown glass bottles cast into a cob section.
- **Tatakuá** (`build_tatakua`): clay oven + chimney + lip + ash door + firewood pile.
- **Rule 7/9/10 props** (`build_services`): anodized-steel solar PV frame (~21.8° tilt), cob cistern with 0.5mm stainless mesh cap + anodized rim + downspout, LiFePO4 battery cabinet.
- **Flora** (`flora.populate` + scatterers): 5 pindo palms with retained leaf-base scars, 3 lapachos (bare + pink bloom in A), 4 mango canopies, 4 tree ferns, 5 bamboo clumps, 5 agave clumps, 80 grass tufts, 4 anthurium epiphyte rosettes on trunks, 100 lapacho petals on the ground in A.
- **Lighting/atmosphere**: A uses `kiara_1_dawn_4k.exr` HDRI + warm sun NNW @ 13° elevation; B uses `misty_pines_4k.exr` HDRI + soft diffuse sun. Bounded canopy Volume Scatter cube (god rays) + B-only ground-hugging valley mist cube. World is never volumed (would black out).
- **Cameras**: 6 named cameras built from `lqv/cameras.py` for the six fixed shots.

Code invariants documented in `CLAUDE.md` (RNG-seed ordering, MAT registry, positional coupling, `WindowCut_*` Boolean cutters, preview-skipped volumes). Pipeline runs Cycles CPU (AMD RX 6400 + Vega iGPU, no ROCm).

---

## 2. Gap analysis — what is missing

### Hard gaps (blocking the spec)

1. **Variant C — night/blue hour with fireflies.** Spec'd in `docs/prompt_house_render.md`. Currently crashes after the full scene build at `lqv/lighting.py:61` because the variant guard rejects C. Required: blue-hour HDRI (we have `qwantani_dusk_2_4k.exr` on disk), cool low-angle moonlight sun, warm window emission planes, scattered firefly emission spheres over corredor + lower terrace. Extends the deliverable from 12 to 18 finals.
2. **`CREDITS.md`** — Poly Haven HDRIs/PBR textures are CC0 (no obligation) but any downstream Sketchfab CC-BY models we incorporate will need attribution. File doesn't exist yet.

### Soft gaps (would raise polish bar but not in spec)

3. **Lapacho bark material** — currently borrows `mango_trunk`. Deferred per STATUS.md: only worth doing if the Hyper3D path for lapacho is abandoned.
4. **Mango canopy silhouette** — procedural placeholder reads correctly at hero distance but flat in macro. A real mango model (e.g. Sketchfab CC0) would lift `petal_macro` and `stream_up` cams.
5. **Gorge headwall + bamboo belt** — two of the five stream-brief zones still absent (per STATUS task 4 closing note).
6. **Paraguayan detail props** — hammock on corredor posts, mate/tereré table, laundry line, wood pile, ember/fire emission in the tatakuá, cántaro on porch, manioc rows, chicken coop. None are spec-blocking but they sell Rule 8 (culturally Paraguayan first) at macro distance.

### Hard blockers (external)

7. **MCP socket dead** — the `blender-mcp` addon socket is not responding. This blocks any Phase 4 work that needs Sketchfab/Poly Haven downloads or Hyper3D/Hunyuan3D generation through the in-process bridge. Workaround: HDRIs that are already on disk (we have three) can be wired without touching MCP. All asset-import work is blocked until the addon comes back.

---

## 3. Reusable models — base assets worth pulling in

Compiled from the asset-research subagents (Poly Haven + Sketchfab) plus the existing `docs/asset_plan.md` shortlist. These are NOT yet downloaded; MCP blocker applies to anything except HDRIs already on disk.

### Already on disk (no MCP needed)

| Asset | File | License | Variant use |
|---|---|---|---|
| `kiara_1_dawn_4k.exr` | `assets/hdris/` | CC0 (Poly Haven) | A — winter golden hour |
| `misty_pines_4k.exr` | `assets/hdris/` | CC0 (Poly Haven) | B — overcast morning |
| `qwantani_dusk_2_4k.exr` | `assets/hdris/` | CC0 (Poly Haven) | **C — blue hour (Phase 7)** |

### Poly Haven targets (CC0, no attribution required)

| Asset | ID | Use |
|---|---|---|
| HDRI `moonless_golf` | `moonless_golf` | Variant C fallback if `qwantani_dusk_2` reads too warm |
| Texture `aerial_mud_1` | `aerial_mud_1` | Already wired (laterite ground PBR) |
| Texture `dry_riverbed_rock` | `dry_riverbed_rock` | Already wired (sandstone + stream bed) |
| Texture `aerial_grass_rock` | `aerial_grass_rock` | Already wired (moss material) |
| Texture `tree_bark_03` | `tree_bark_03` | Already wired (lapacho bark) |
| Model `WoodenTable_03` | poly haven props | Mate/tereré table on corredor |
| Model `painted_wooden_bench` | poly haven props | Corredor seating |

### Sketchfab targets (CC-BY mostly — needs CREDITS.md)

| Asset | UID | License | Use |
|---|---|---|---|
| Mango tree CC0 | `62e297e1f36f448a8618192185e818fe` | CC0 | Replace procedural mango canopy in `flora.populate` |
| Agave americana CC-BY | `efe126efa459471c81cfc3132357b1b6` | CC-BY | Replace procedural agave at lower-terrace spots |
| Capybara CC-BY | `f9201e6cca66434dbb5f759bd9884d75` | CC-BY | Optional Rule 8 wildlife sell on `stream_up` |
| Hammock (paraguayan) | `b5b2e42309144dafaf2efe9b71a491c8` | **CC-BY-SA** | Corredor hammock — share-alike propagates on redistribution; flag before bundling |

### Hyper3D / Hunyuan3D generation targets (when MCP back online)

| Target | Why generate instead of search |
|---|---|
| Lapacho tree (bare + pink trumpet flowers, winter form) | Specific Paraguayan species not on Sketchfab |
| Pindo palm with retained leaf-base scarring | Procedural reads correct but model would lift hero macro |
| Cántaro (Paraguayan earthenware water jug) | Cultural prop, no public CC asset found |
| Tatakuá clay oven detail (foreground macro) | Procedural enhancement landed Phase 5 but a generated model would lift `terrace` cam |

---

## 4. Roadmap — phases 7 through 11

### Phase 7 — Variant C (night/blue hour + fireflies) — **STARTING NOW**

No MCP dependency; everything procedural. Code touches:

- `lqv/config.py:46-49` — lift variant guard from `('A','B')` to `('A','B','C')`.
- `lqv/lighting.py:_HDRI_BY_VARIANT` — add `'C': ('qwantani_dusk_2_4k.exr', 0.5)`.
- `lqv/lighting.py:setup_world_and_sun` — add C branch: cool blue moonlight (energy 0.15, color (0.6,0.75,1.0), 5° soft angle, near-horizon rotation), sky strength fallback 0.05.
- `lqv/materials.py` — add `MAT['window_glow']` (warm white emission 12.0) and `MAT['firefly']` (yellow-green emission 80.0).
- `lqv/house/cob.py` — hoist `window_specs` to a module-level `WINDOW_SPECS` constant; add `build_window_emission(variant)` that places emission planes inside each window at z=2.1, recessed 0.10m inside the wall normal, scaled 0.85× of the cutout. C-only guard.
- `lqv/flora/fireflies.py` (new) — `scatter_fireflies(n=80, variant)` bounded over corredor (x∈[-6,6], y∈[-4,-2]) + lower terrace (x∈[-8,8], y∈[-8,-4]) at z∈[1.0,2.5], small UV-sphere emission. C-only guard.
- `build_scene.py:92` — extend exposure ternary into if/elif/else: A=-0.2, B=+0.3, C=+0.6.
- `build_scene.py` — call `build_window_emission(cfg.variant)` after `build_cob_house()`; call `flora.scatter_fireflies(variant=cfg.variant)` after `scatter_anthuriums`.
- `scripts/render_all_finals.sh` — `for variant in A B C`; echo "ALL 18 FINALS DONE".
- `STATUS.md` — manifest target 18 finals; six new C rows.

Verification: smoke test → preview C/hero → 6 finals.

### Phase 8 — Paraguayan detail props (no MCP dependency)

Procedural-only props that reinforce Rule 8 at macro distance. Each is hardcoded (no `random.*`) so RNG order stays byte-identical:

- Hammock between two corredor posts (curve + cloth-shape, lapacho-rope material).
- Mate/tereré set (`mate` cup + `bombilla` + `termo` thermos) on a small lapacho table on the corredor.
- Laundry line between the corredor and a tree.
- Wood pile beside the tatakuá.
- Ember/fire emission inside the tatakuá (deferred from Phase 5 — pairs naturally with Variant C window glow).
- Cántaro on the corredor floor (earthenware water jug).
- Manioc + maize rows in the east yard.
- Wire-mesh chicken coop near the cistern.

### Phase 9 — Procedural flora silhouette upgrades (no MCP dependency)

Polish on existing placeholders, targeted at the macro cams:

- Pindo plumose drooping fronds — replace the current flat frond plane with a multi-leaflet curve sweep so silhouette reads `Syagrus` not `Cocos`.
- Bamboo culm refinement — segmented nodes via array modifier, slight taper.
- Lapacho distinctive bark material (item 3) — only if Phase 10 Hyper3D path is abandoned.
- Anthurium leaf shape — current strap planes work at hero distance; macro cam would benefit from a slight curl + glossier specular.

### Phase 10 — External asset integration (BLOCKED on MCP socket)

When the MCP addon comes back:

1. Pull Poly Haven `moonless_golf` HDRI as a Variant C fallback (`qwantani_dusk_2` is warmer than pure blue hour).
2. Pull Poly Haven `WoodenTable_03` + `painted_wooden_bench` for the corredor.
3. Pull Sketchfab mango CC0 `62e297e1f36f448a8618192185e818fe` — replace procedural mango at four spots in `flora.populate`.
4. Pull Sketchfab agave CC-BY `efe126efa459471c81cfc3132357b1b6` — replace procedural agave at five spots.
5. **Decision required from user before pulling** the CC-BY-SA hammock — share-alike propagates if we redistribute the bundle. If user opts out, fall back to procedural hammock in Phase 8.
6. Hyper3D-generate the lapacho tree + cántaro from text prompts; import via `import_generated_asset`.
7. After every external asset lands: append a line to `CREDITS.md` with asset name + UID + license + author.

### Phase 11 — Render bundle + delivery

- Re-run `scripts/render_all_finals.sh` to regenerate all 18 finals against the upgraded scene.
- Verify against the 10 rules + species accuracy on each image.
- Write `CREDITS.md` (CC-BY attribution) and `LICENSE_BUNDLE.md` (which assets propagate share-alike).
- Update STATUS.md to "all 18 delivered" and tag the commit.

---

## 5. License/credits handling

- **Poly Haven assets** are CC0 — no attribution required, no `CREDITS.md` entry needed. We can include them silently.
- **Sketchfab CC-BY assets** require an attribution line per asset (author + title + UID + license URL). Maintain `CREDITS.md` at repo root with one line per CC-BY asset.
- **Sketchfab CC-BY-SA assets** (currently only the hammock under consideration) propagate share-alike. If we redistribute the asset bundle (e.g. publish `assets/sketchfab/` with the scene), every derivative incorporating that asset must also be CC-BY-SA. Recommendation: keep CC-BY-SA assets out of the bundle by default; pull them only if user explicitly opts in.
- **Hyper3D / Hunyuan3D outputs**: license terms differ; check at generation time and record in `CREDITS.md` regardless.

---

## 6. Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| MCP socket stays dead | High (current state) | Blocks Phase 10 entirely | Phase 7-9 are fully procedural; Phase 10 is the only blocked work |
| Variant C night render comes out muddy on CPU | Medium | Phase 7 slips | Smoke test before commit; iterate exposure (currently +0.6) and HDRI strength (currently 0.5) before committing to 6 finals |
| CC-BY-SA hammock accidentally bundled | Low | License contamination | Mark hammock as `# CC-BY-SA — needs opt-in` in `CREDITS.md` and skip by default |
| RNG order broken by Phase 8 prop scatter | Medium | A/B finals drift | All Phase 8 props are hardcoded (no `random.*`); fireflies guarded C-only |
| Variant C 6 finals push delivery from 12 to 18, ~50% more render hours | Certain | Schedule slip | Accept; deliver A/B finals first as baseline, then C as a follow-up batch |

---

## 7. Definition of done

The scene is "complete" when:

- 18 finals delivered (A/B/C × 6 cams), each verified against the 10 rules + species accuracy.
- All four blockers from the original asset plan resolved (HDRI swap landed for A/B/C, ground PBR landed, Sketchfab batch landed, MCP socket either restored or worked around).
- `CREDITS.md` lists every CC-BY asset with author + UID + license.
- `STATUS.md` manifest shows 18/18 ☑.
- `scripts/render_all_finals.sh` produces a clean run from `scene.blend` not present.
- Git tag `v1.0-bundle` on the final commit.
