# Asset plan — La Quebrada Viva

Single execution doc synthesising: (1) scene-completeness gap audit, (2) HDRI + PBR texture shortlist, (3) flora + prop 3D model shortlist, (4) integration roadmap, (5) prioritised execution order. Treat this as the source of truth for what we still need to render Variants A+B at brief quality.

Authoritative inputs:
- `docs/MASTER_BRIEF.md` (zones, flora list, 10 rules, render matrix §13)
- `docs/paraguay_clay_house_research.md` v2 (Escobar, Paraguarí — site CONFIRMED)
- `CLAUDE.md` (code invariants, material palette, species notes)
- `STATUS.md` (open backlog; petal/bridge regressions verified 2026-06-10)

---

## A. Scene audit — what's missing vs the brief

Gap audit identified 23 items; 7 are blockers for shipping the 12 final renders. Buckets:

**Blockers (must land before any "final" tick on STATUS.md manifest):**
1. **Lapacho flowering tree** — current model is icosphere puffballs assigned to `MAT['mango_trunk']`. Reads as cartoon at hero distance. Needed for Variant A bare+pink AND Variant B leafed silhouette.
2. **Ground PBR** — laterite is a flat color shader. At hero/cliff cameras the lack of microdetail kills realism.
3. **HDRI environment** — current lighting is purely procedural (sun + sky shader). Variant A golden hour and Variant B overcast both need real-world skydome captures for believable ambient bounce.
4. **Stream weir** (Rule 7 anchor) — brief defines 5 zones; weir is missing. Also gates micro-hydro prop.
5. **Solar PV on separate steel frame** (Rule 9) — present as bare geometry placeholder; needs visible panel + frame for any detail/establishing shot.
6. **Cistern with 0.5mm stainless mesh** (Rule 10) — currently a smooth cylinder; rule violation on close inspection.
7. **Pindo palm** — drooping plumose fronds, not coconut. Current model is icosphere + stiff radial leaves.

**High-leverage (lifts every render once landed):**
- Lapacho trunk bark material (currently `MAT['mango_trunk']` shared)
- Mango canopy realism (icospheres + displacement; could use real model)
- Cob wall surface texture (raw clay block + lime plaster overlay)
- Footbridge timber detail
- Tatakuá oven (small structure on terrace; brief calls it out as cultural marker)
- Bottle wall section (rule-8 cultural authenticity — recycled glass set in cob)

**Detail-shot polish:**
- Anthurium plowmanii epiphytes (STATUS.md task 5)
- Tree fern understory (riparian shade)
- Bamboo clumps along stream (clumping, not running)
- Agave on lower terraces (colonising, not designed)
- Grass tufts (`scatter_grass_tufts` exists, not wired — STATUS.md task 1)
- Pelton wheel + housing for micro-hydro

**Atmosphere / lighting:**
- Variant B valley mist (STATUS.md task 2)
- Dusk variant sky (currently A/B lighting borrowed for `dusk` cam)

**Deferred (do not work on until 12 finals ship):**
- Variant C night/blue hour + fireflies (STATUS.md task 8)
- 4K render preset (brief aspirational, not deliverable spec)

---

## B. Research gaps — things we cannot just download

These came back negative from the asset research pass; each has a workaround.

| Gap | Why no off-the-shelf | Workaround |
|---|---|---|
| **Lapacho (Handroanthus impetiginosus) — bare branches + pink trumpets** | Sketchfab free tier has zero usable models; only paid CGAxis sapling + paid Evermotion chrysantha exist. Polyhaven has no flowering trees. | **Generate via Hyper3D / Hunyuan3D** for Variant A (bare + pink bloom) and Variant B (fully leafed). Prompts in §C below. Fall back to polyhaven `jacaranda_tree` as a mid-distance silhouette stand-in (wrong color — only acceptable at >40m from camera). |
| **Lapacho (leafed)** | Same as above. | Hyper3D prompt for leafed variant. |
| **Thatch / sapé roof texture** | Poly Haven has no thatch PBR; Sketchfab thin and mostly low-poly props. | Generate procedurally OR Hyper3D-generate a tileable thatch texture from a text prompt + reference photo. The brief currently shows tile roof, not thatch — defer unless we change roof material. |
| **Anthurium plowmanii** species accuracy | Available Sketchfab model (Lassi Kaukonen, CC-BY) is labelled "anthurium" generically; species-true _plowmanii_ has bird-nest rosette leaves, not heart-leaf shape. | Use the available CC-BY model AND verify visually against reference photos; if wrong species, Hyper3D-generate. |
| **Mango (CC-BY-NC found, REJECTED)** | Highest-quality free mango pack on Sketchfab is CC-BY-NC. We're not commercial but we want a clean licence story. | Use Jagobo `tropical-mango-trees-free-6997814540f14929bf13cf3828b5dc90` (CC-BY, 755k tris, 5 tree variants). Safe. |
| **Bottle wall section** (recycled glass in cob — Rule 8 cultural marker) | No off-the-shelf model fits the cob/bottle aesthetic. | Build procedurally in `lqv/` — instance FrodoUndead `glass-bottles-334377879cb4475d9a4720a2f7c4cf55` (CC-BY) inside a small cob panel mesh; use existing `clay_block_wall` PBR as mortar. |
| **Pelton wheel housing** | Available Filipe.Canto pelton wheel asset gives the runner, not the casing. | Build housing procedurally in `lqv/`; use the model for the wheel itself. |
| **Steel frame for solar PV** | 3DJeff panel asset is bare panel only. | Build steel frame procedurally (square tube extrusions in `lqv/`); panel asset instanced on top. Rule 9: frame must read as separate from sod roof. |

---

## C. Reusable assets — ranked shortlist

All Poly Haven assets are CC0 (no attribution required, but `CREDITS.md` lists them for traceability). All Sketchfab picks below are **CC-BY** unless flagged otherwise; `CREDITS.md` MUST list each before any render ships.

### C.1 HDRI environments (Poly Haven — CC0)

| Slot | Primary | Alternates | Notes |
|---|---|---|---|
| Variant A — winter golden hour, sun NNW, elevation 13° | `kiara_1_dawn` (16K available; 4K for previews) | `bambanani_sunset`, `belfast_sunset_puresky` | Match brief §12 lighting; replace pure procedural sky shader in `lqv/lighting.py` for Variant A path. |
| Variant B — morning overcast | `misty_pines` (16K) | `cannon`, `forest_slope` | Soft diffuse, exposure +0.3 per brief. |
| `dusk` camera | `qwantani_dusk_2` (24K) | `the_sky_is_on_fire` | Currently both variants borrow A/B sky for dusk; this gives proper blue-hour ambient. |

Download command pattern:
```python
mcp__blender__download_polyhaven_asset(asset_id="kiara_1_dawn", asset_type="hdris", resolution="4k")
```
Use `4k` for previews + non-hero finals; bump to `8k` for hero finals only (memory budget).

### C.2 PBR textures (Poly Haven — CC0)

| Surface | Primary | Tiling notes |
|---|---|---|
| Laterite ground (`MAT['laterite']`) | `aerial_mud_1` (8K, 8m×8m tile) | Pair with the brief's `#8B3A1F`–`#A85832` color targets via shader-mix to keep the photographed mud the right Paraguayan red. |
| Laterite alt / wet patches | `brown_mud_03`, `clay_floor_001` | For under-canopy shaded mud. |
| Moss/sandstone (terraces, stream rocks) | `aerial_grass_rock` (8K, 15m×15m) | Best blend of `#5F7A3D` moss + `#5A5448` rock per palette. |
| Rock detail | `dry_riverbed_rock`, `coast_sand_rocks_02`, `forest_ground_04` | For close-up boulders + weir face. |
| Cob walls (raw clay block) | `clay_block_wall` | Base layer under lime wash. |
| Cob walls (lime plaster overlay) | `clay_plaster` | Mix on top via mask; Rule 2 says always lime, never cement. |
| Cob walls (worn detail) | `rough_plaster_brick`, `damaged_plaster` (use as mask) | For corners + weather streaks. |
| Milled lapacho timber (corredor posts, doors) | `dark_wood` | Hardwood reddish-brown. |
| Footbridge deck timber | `wood_floor_deck` | Weathered planks. |
| Other timber detail | `weathered_brown_planks`, `rough_wood` | Use sparingly. |
| Lapacho bark | `tree_bark_03` | Use for trunk material (replaces shared `MAT['mango_trunk']` — STATUS.md task 3). |
| Pindo bark (retained leaf bases) | `palm_tree_bark` | For STATUS.md task 7. |
| Mango bark | `bark_platanus` | Closest match. |

### C.3 Flora + prop models (Sketchfab — CC-BY unless flagged)

| Asset | UID | Licence | Tris | Edit roadmap |
|---|---|---|---|---|
| **Pindo palm** | `palm-tree-1fba8da266bc428ebfe8fe8a4f4df987` | CC-BY (blendfile site) | 55k | Bend fronds downward (Edit-mode proportional edit) for drooping silhouette; replace material with `palm_tree_bark` for trunk. Brief species note: NOT coconut. |
| **Mango pack** | `tropical-mango-trees-free-6997814540f14929bf13cf3828b5dc90` | CC-BY (Jagobo) | 755k (5 trees) | Decimate to ~150k each if memory becomes an issue. Use multiple variants for the canopy backdrop. |
| **Tree fern** | `tree-fern-1-c6bc31d122c043a19346c90f5cbde40e` | CC-BY (b_nealie) | 130k | Use directly; scatter 8–15 along stream. |
| **Fern (understory)** | polyhaven `fern_02` | CC0 | n/a | For ground-cover fill under trees. |
| **Bamboo (Guadua)** | `3c13dc82ffb54d079a71fb8160d0cf90` | CC-BY (local.yany) | **1.5M — must decimate to ~50k** | Decimate aggressively before instancing; clumping placement per brief. |
| **Bamboo (backup)** | Maskable backup UID — research note | CC-BY | n/a | If local.yany asset doesn't decimate cleanly. |
| **Agave americana** | `efe126efa459471c81cfc3132357b1b6` | CC-BY (LucaDubs) | **1M — must decimate to ~50k** | Lower-terrace placement; instance with rotation jitter. |
| **Anthurium plowmanii** | `e6a92c1ddb8941e9b8aa92dc1f0f3c18` | CC-BY (Lassi Kaukonen) | 95k | **Verify species visually before commit** (see §B). If wrong, Hyper3D-generate. Place as epiphyte on lapacho/mango trunks near stream. |
| **Solar panel** | `71f959c15448419e98be183871b7ed19` | CC-BY (3DJeff) | n/a | Procedural steel frame in `lqv/` — Rule 9 (NOT on sod roof). |
| **Pelton wheel runner** | `de3a9ddc430740eaac82fd43b06b7394` | CC-BY (Filipe.Canto) | n/a | Procedural housing in `lqv/`; visible at weir for Rule 7. |
| **Water tank (5000L)** | `7cd2b87c332a4cce8f881e3b0b4faa40` | CC-BY (Maggadog) | n/a | Scale 0.6×. **Must add 0.5mm stainless mesh procedurally over inlets** — Rule 10. |
| **Tatakuá oven** | `d98456e4673943feb277dab8b45e5db6` | CC-BY (knockcg) | 2.3k | Clean upgrade over any procedural placeholder. Terrace placement per brief. |
| **Glass bottles** (bottle wall) | `glass-bottles-334377879cb4475d9a4720a2f7c4cf55` | CC-BY (FrodoUndead) | n/a | Instance inside cob panel for Rule-8 cultural marker. |

### C.4 Hyper3D / Hunyuan3D generation prompts (gaps with no free asset)

Run via `mcp__blender__generate_hyper3d_model_via_text` then `mcp__blender__import_generated_asset`.

**Lapacho — Variant A (winter, bare + pink bloom):**
> "Handroanthus impetiginosus (lapacho rosado) tree, ~10m tall, completely bare branches in winter dormancy, covered in clusters of hot-pink trumpet-shaped flowers at every twig tip. Asymmetric branching, three to five main limbs spreading from the trunk. Trunk diameter ~40cm, deeply furrowed grey-brown bark. No leaves. Pink trumpet flowers in dense terminal clusters, color range hex #E85A8C to #F0A0C8. Botanically accurate."

**Lapacho — Variant B (summer, fully leafed):**
> "Handroanthus impetiginosus (lapacho rosado) tree, ~10m tall, fully leafed with dark-green palmately compound leaves, five leaflets per leaf, leaflet edges finely serrated. Asymmetric branching, three to five main limbs. Trunk diameter ~40cm, deeply furrowed grey-brown bark. No flowers. Dense rounded canopy. Botanically accurate."

**Thatch tileable texture (deferred unless roof material changes):**
> "Sapé thatch roof, dried golden-brown palm thatch fibers, tileable seamless 2m square, top-down view, slightly weathered, natural strand variation."

### Procedural-recipe entries (no Hyper3D call — recorded here for reproducibility)

Variant C's emission-heavy elements are fully procedural; no external mesh is downloaded or generated. They are catalogued here alongside the Hyper3D prompts so the entire generated/procedural surface area of the scene is reproducible from this one section.

**Fireflies (Variant C — `lqv/flora/fireflies.py`):**
> 80 UV-spheres scattered with a 1:2 ratio between the corredor and the lower terrace. Each sphere uses `MAT['firefly']` with `emission_strength=80`. **Ordering invariant:** the scatter call must run AFTER `scatter_anthuriums` so RNG draw order — and therefore positional byte-identity vs the in-flight C render — stays stable. Re-running the build with a different ordering shifts every downstream `random.*` consumer.

**Cob window emission planes (Variant C — `lqv/house/cob.py:build_window_emission`):**
> Warm window-glow emission planes inserted inside each cob cutout, sized to fit just behind the hidden `WindowCut_*` Boolean cutters (see CLAUDE.md "Code invariants" #4). Material is `MAT['window_glow']` tuned to read as a candle/oil-lamp interior at dusk, not a modern LED. Strength is set on the material in `lqv/materials.py`; the builder only places geometry.

**Bottle-wall procedural panel (Rule 8 cultural marker — `lqv/house/cob.py`):**
> Instanced glass bottles (Sketchfab UID `334377879cb4475d9a4720a2f7c4cf55`, FrodoUndead, CC-BY 4.0) packed into procedural cutouts in a cob panel. Bottle material is a honey-coloured + clear-glass mix to read as recovered Quilmes/Brahma bottles. The cob panel geometry is procedurally generated; only the bottle mesh is external. Listed here (not §C.3) because the *panel as a whole* is a procedural assembly, not a downloadable asset.

---

## D. Integration plan

### D.1 Repo conventions

Create `assets/` at project root with subdirectories:
```
assets/
  hdris/         # downloaded .exr/.hdr — gitignored (regenerable via download script)
  textures/      # Poly Haven PBR sets — gitignored
  models/        # Sketchfab + Hyper3D imports — tracked (binary blendfiles small)
  references/    # photo references for visual verification
CREDITS.md       # CC-BY attribution — tracked
scripts/download_assets.sh  # idempotent re-download script — tracked
```

`assets/hdris/` and `assets/textures/` go in `.gitignore` because the Poly Haven MCP can re-fetch them deterministically by ID. `assets/models/` is tracked so the build is reproducible without depending on Sketchfab uptime.

### D.2 Per-asset edit roadmap

For each model that lands in `assets/models/`:
1. **License sanity**: add an entry to `CREDITS.md` with author, UID, licence URL.
2. **Decimate** if > 200k tris (use Blender's Decimate modifier set to ~0.2 ratio, then apply).
3. **Re-origin**: set origin to bottom-center so ground anchoring works with the BVH lookup pattern.
4. **Material override**: where the asset's built-in material conflicts with our palette, override via `assign(obj, MAT['<key>'])` after import.
5. **Wire into `lqv/`**: each asset gets a `place_<asset>(x, y, scale, ...)` helper in the relevant `lqv/flora/*.py` or `lqv/site/*.py`. Use the existing BVH ground sampling pattern (see `lqv/flora/lapacho.py:90-105`) for ground anchoring.

### D.3 RNG invariant preservation

`CLAUDE.md` rule: `random.seed()` runs after `materials.build_materials()` and before the first `build_*` call. **All asset-placement helpers that use `random.*` must be called in the existing order; new helpers append to the end of `build_scene.py`, never insert between existing calls.** Otherwise every prior render becomes irreproducible.

When using `bpy.ops.object.transform_apply` or `bpy.context.view_layer.update()` mid-scatter, do it consistently across runs (the petal scatter already does this — model it).

### D.4 HDRI integration in `lqv/lighting.py`

Replace the procedural sky shader for Variants A/B with a `ShaderNodeTexEnvironment` driven by the downloaded HDRI:
- Variant A → `kiara_1_dawn` rotated so the bright spot lands NNW (matches brief §12 sun position; deliberately 13° elevation per CLAUDE.md not 20°).
- Variant B → `misty_pines` with `Background.Strength = 1.2`.
- Keep the existing sun lamp for direct shadows — HDRI provides ambient bounce only.
- Previews skip canopy volume (CLAUDE.md invariant 5); HDRI itself is preview-safe.

### D.5 CREDITS.md schema

```markdown
## CC-BY assets

- **<asset name>** — <author> — Sketchfab UID `<uid>` — CC-BY-4.0 — used as <where in scene>
```

Pre-populated with all Sketchfab picks above; mark each `[USED]` once it lands in `assets/models/`. Removing an asset from the scene = remove the entry.

### D.6 MCP socket prerequisite

Poly Haven downloads run through `mcp__blender__download_polyhaven_asset`. The asset-researcher pass hit "Could not connect to Blender" on its MCP attempts — the BlenderMCP addon needs to be live on `localhost:9876` before the download script runs. Verify with `mcp__blender__get_polyhaven_status` before the first download; if dead, start interactive Blender + enable the addon, then run the batch.

---

## E. Prioritised execution order

Ordered by **cost × visual impact**. Each phase is independently shippable: if we run out of time, we still have a more polished scene than before.

### Phase 1 — HDRI environment swap (highest leverage / lowest cost)

Replaces procedural sky → real skydome. Lifts every render that has visible sky. ~30 min if MCP socket cooperates.

1. `mcp__blender__get_polyhaven_status` — confirm socket.
2. Download `kiara_1_dawn` @ 4K, `misty_pines` @ 4K, `qwantani_dusk_2` @ 4K.
3. Edit `lqv/lighting.py` to add HDRI path for each variant. Keep procedural sky as fallback.
4. `scripts/render_preview.sh A hero` — verify golden-hour ambient looks right.
5. Commit: `feat(lighting): real-world HDRI environments for Variants A/B/dusk`.

### Phase 2 — Ground PBR (laterite + sandstone)

Replaces flat color → photographed texture. Lifts every render with visible ground.

1. Download `aerial_mud_1`, `aerial_grass_rock`, `dry_riverbed_rock` @ 4K.
2. Edit `lqv/materials.py` — add ShaderNodeTexImage chains to `MAT['laterite']`, `MAT['sandstone']`, `MAT['moss']`. Use UV scale 1/8 for laterite (8m tile), 1/15 for sandstone-moss.
3. Color-mix against brief palette hex values to keep Paraguayan red, not generic mud.
4. `scripts/render_preview.sh A hero` then `A cliff`. Verify color match.
5. Commit: `feat(materials): photographed PBR for ground surfaces`.

### Phase 3 — Lapacho replacement (Hyper3D generation)

Single biggest fidelity gain. Variant A's whole identity hinges on the pink-bloomed lapacho carpeted with petals.

1. `mcp__blender__get_hyper3d_status` — confirm credits.
2. Generate Variant A model (prompt §C.4). Import via `mcp__blender__import_generated_asset`. Inspect.
3. Generate Variant B model (prompt §C.4). Same.
4. Save the two generated models to `assets/models/lapacho_A.blend` and `lapacho_B.blend`.
5. Edit `lqv/flora/lapacho.py` to **append** (RNG-order!) a `place_lapacho_imported(x, y, flowering)` function that links from the saved blend. Keep the existing `add_lapacho` for fallback.
6. Switch the foreground lapacho at (-3, -10) — the one Cam_PetalMacro frames — to use the imported model.
7. `scripts/render_preview.sh A petal_macro` — verify hero-pose lapacho.
8. Commit: `feat(flora): Hyper3D-generated lapacho for Variants A/B`.

### Phase 4 — Pindo palm + mango pack + tree fern + bamboo (Sketchfab batch)

Knocks out four species in one batch download.

1. `mcp__blender__download_sketchfab_model` × 4 with the UIDs above.
2. For each: decimate if >200k tris, re-origin, save to `assets/models/`.
3. Add `place_*` helpers in `lqv/flora/palm.py`, `lqv/flora/mango.py`, `lqv/flora/fern.py`, `lqv/flora/bamboo.py`. Use the existing BVH ground-anchor pattern.
4. Update `CREDITS.md`.
5. `scripts/render_preview.sh A cliff` (pindo foreground) + `A hero` (mango backdrop) + `A stream_up` (tree fern + bamboo).
6. Commit: `feat(flora): Sketchfab imports — pindo, mango, tree fern, bamboo`.

### Phase 5 — Rule 7/9/10 props

Required for any close-up that includes a "outage-proof systems" beat. Without these, detail finals violate brief rules.

1. Download water tank, pelton wheel, solar panel, tatakuá from Sketchfab.
2. Build procedural housings: pelton casing, solar steel frame.
3. Add 0.5mm stainless mesh to tank inlets — Rule 10.
4. Build stream weir geometry in `lqv/site/stream.py` (also closes STATUS.md task 4).
5. Place all props; update CREDITS.md.
6. Render-test each in a preview that frames it.
7. Commit individually per prop with `feat(props): <name>`.

### Phase 6 — Detail flora (agave, anthurium, grass tufts)

After the visual identity is locked, fill in understory richness.

1. Download agave + anthurium.
2. Wire `scatter_grass_tufts` from `lqv/flora/bamboo.py` (STATUS.md task 1).
3. Verify anthurium species; Hyper3D fallback if wrong.
4. Commit per asset.

### Phase 7 — Atmosphere polish

1. Variant B valley mist (STATUS.md task 2).
2. Lapacho trunk material (STATUS.md task 3) — uses `tree_bark_03` texture now that we've got it.
3. Pindo trunk texture (STATUS.md task 7) — uses `palm_tree_bark`.

### Phase 8 — Render all 12 finals

`scripts/render_all_finals.sh` from a clean state. Run `/verify-render` per output. Update STATUS.md manifest.

### Deferred (do not touch until phase 8 ships)

- Variant C night/blue hour + fireflies (STATUS.md task 8). 12 → 18 finals.
- 4K render preset.
- Bottle wall procedural section (Rule 8) — nice-to-have if any shot frames it.
- Cob walls PBR overlay — current shader is acceptable at hero distance; can wait.

---

## F. What this plan does NOT cover

- It does not touch positional coupling (hero ↔ pool ↔ bridge ↔ escarpment). Imported models must be **dropped at the existing positions**, not moved.
- It does not redesign cob walls. The procedural displacement is already on-brief.
- It does not address windows, doors, smart-home interior tech. Those are interior-shot concerns — out of scope for the 12 establishing finals.
- It does not change the samples policy (128 / 512 / 256) or seed (20260609).

---

## G. Cross-references (additive 2026-06-10 — closes orphan gap to license/deliverable satellites)

This plan was previously a closed loop ending at §F. The satellite docs added over the 2026-06-10 session reference *this* doc as the source of truth for asset selection, but the reverse pointers were missing. Listed here so future readers can traverse the asset graph in either direction:

- `docs/external_assets.md` — live download/status mirror of §C above plus Variant C procedural-recipe traceability block; the "is it actually on disk yet" companion to this plan's "what we want and why".
- `docs/license_obligations.md` — what we owe whom (CC0 vs CC-BY 4.0) for every asset in §C; includes a Variant C procedural-recipe carve-out confirming Variant C imagery adds no new attribution obligation beyond the A/B CC0 chain.
- `LICENSES/README.md` (repo root) — verbatim CC0 + CC-BY 4.0 legal-code mirror; the legal-text companion to the per-asset attribution rows planned in §D.5 (`CREDITS.md` schema).
- `docs/wesley_deliverable_bundle.md` — Tier-1/2/3 shipping manifest for the 2026-06-27 escritura package; the assets in §C feed the Tier-2 USB/cloud bundle and back the Tier-1 prints.
- `CREDITS.md` (repo root, populated as assets land) — per-asset attribution rows in the schema sketched in §D.5.
- `LICENSE_BUNDLE.md` (repo root) — full license texts shipped alongside any redistribution.
- `STATUS.md` (repo root) — source of truth for "which `place_*` helper is wired right now" vs "asset still on Phase 4 backlog"; reconciles this plan's phased order against in-flight render state.
- `docs/SESSION_LOG.md` — narrative log of asset-plan execution including the per-cam render-loop architecture decision that ratified Phase 8.
- `ARCHITECTURE.md` (repo root) — `lqv/` package code map; the `place_*` integration points named in §D.2 live in the modules listed there.
- `CLAUDE.md` (repo root) — code invariants (RNG seed ordering, MAT registry, hidden `WindowCut_*` Boolean cutters) that §D.3 must preserve when wiring new assets.

### Extended back-pointers (additive 2026-06-10, second pass)

The original §G above closed the legal/deliverable axis. This second-pass extension closes the remaining axes (upstream-plan, research, cultural-backing, physical-construction, reference-photography) so the asset plan is reachable from every adjacent doc. Listed below with *why* each back-link matters:

- `docs/master_plan.md` §Phase 1-8 — master_plan is the forward Phase 1-8 source-of-truth; this asset_plan is downstream of master_plan §Phase 7/8 (asset procurement + final renders). When master_plan phases shift, §E "Prioritised execution order" above shifts with them. Master_plan is upstream; this is the import-line plan that executes its phasing.
- `docs/research_index.md` (root note + per-repo entries) — research_index catalogues the ~80 repositories surveyed during Phase 7.5 to identify candidate Sketchfab/PolyHaven/Hyper3D-adjacent assets and reusable code patterns. The §C.3 Sketchfab shortlist + §C.4 Hyper3D prompt archive draw from that survey. research_index is upstream; §C is the curated downstream shortlist.
- `docs/cultural_notes.md` §Plants + §Materials — Rule 8 ("culturally Paraguayan first") backing. Every flora pick in §C.3/§C.4 (lapacho, pindo palm, mango, tatakuá, cob-panel) traces back to a cultural_notes entry. cultural_notes is the *why* behind species choices; §C is the *what we download* derived from those choices.
- `docs/floor_plan.md` + `docs/section_view.md` — 2D drawings of the cob house. Asset placement helpers (`lqv/house/cob.py`, `lqv/site/site_plan.py`) reference these drawings as positional source-of-truth; §D.2 per-asset edit roadmap aligns each `place_*` helper to a drawing landmark. Drawings are upstream of `place_*`; `place_*` is upstream of §C asset rows.
- `docs/bom.md` — bill of materials for the physical build. Every §C asset row that represents a material (cob panels, sandstone, laterite, lapacho) maps to a BOM line item. bom.md is the construction-side companion to this digital-asset plan; together they answer "what to build" vs "what to render".
- `docs/site_data_spike.md` — site survey constants (62-ha boundary, contour topology, water-line position). §C.1 HDRI selection (Nishita sky strength + sun angle) and §C.2 ground PBR selection (laterite/sandstone vs other terrain) are constrained by site_data_spike findings. site_data_spike is the empirical input; §C is the asset-side response.
- `docs/photographic_references.md` — parallel framework for reference photography (NOT embedded in renders, but used by humans as visual ground truth during §C.4 Hyper3D prompt iteration). When a Hyper3D prompt produces a candidate, reference photos validate cultural authenticity. photographic_references.md is the parallel reference-library; this plan is the asset-procurement plan.
- `docs/build_sequence.md` — physical construction phasing (foundation → cob walls → bottle-windows → roof → finishings). §C.2 ground PBR + §C.4 cob-panel Hyper3D recipe map to specific phases in build_sequence. build_sequence is the physical timeline; this plan is the visual asset timeline for the renders that *show* that physical timeline.
- `docs/energy_budget.md` — Rule 7+9 energy stack (solar + biogas + grey-water). §C.4 Hyper3D recipes for solar panels + biogas digester + grey-water tanks trace back to energy_budget sizing. energy_budget is the engineering target; §C is the visual artefact derived from it.
- `docs/wesley_brief_onepager.md` — the one-pager Wesley brings to the escritura; key visual claims ("Paraguayan first", "low-impact", "62 ha") are backed by the assets selected here. wesley_brief_onepager is the message; §C feeds the imagery that supports the message.
- `docs/contract_summary.md` — parcel + ownership facts; §C.1 HDRI sun-angle calibration uses the contract_summary parcel coordinates to set the latitude-correct sun path. contract_summary is the geographic ground-truth; §C.1 HDRI orientation is downstream.
