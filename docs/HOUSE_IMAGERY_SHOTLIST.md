# House imagery shotlist — multi-view + x-ray + interior coverage

**Authored 2026-06-25.** Post-escritura sprint plan. Scope: convert each buildable typology from its current 3-image footprint (lighting variants A/B/C from one south-east hero angle) into a 12-shot portrait covering cardinal elevations, plan, section, x-ray cutaway, interior, and detail close-ups.

Renderer is byte-frozen at `85e86aa` through 2026-06-27. **All work below lands after the escritura signs**, against the sub-render-first workflow (`lqv/subscene/<asset>.py`). Composite `build_scene.py` is untouched.

---

## 1. Current state — what we ship today

Each of the 16 buildable assets currently renders as **3 PNGs at one camera angle**:

| Variants | Camera | Distance | Lens |
|---|---|---|---|
| A — golden hour | `Cam_Subscene` 3/4 SE | 6–14 m (asset-tuned) | 28–35 mm |
| B — overcast | same | same | same |
| C — blue hour + fireflies | same | same | same |

Where each driver is `lqv/subscene/<asset>.py`, calling `cameras.subscene_camera(target, distance, height, lens)` once. See `lqv/cameras.py:55`. Output flat path `renders/sub/<asset>_<variant>.png` is back-compat invariant; per-run paths land under `renders/sub/runs/<RENDER_RUN_ID>_<asset>[_<tag>]/<variant>.png`.

**Coverage assets** (16):

- *Typologies (13):* hobbit_house, italian_stone_small_v1, italian_stone_small_v2, italian_river_house_4pax, container_river_house, bamboo_river_house, bamboo_container_4pax, bamboo_wigwam_lodge, bamboo_boomhut_treehouse, bamboo_beton_30, bamboo_beton_28, bamboo_beton_family_curved, bamboo_beton_family_rectangular, bamboo_curved_roof_villa, clay_terracotta_estate
- *Reference (1):* cob_bottle_lqv (built from `build_scene.py`; subscene driver mirrors it for parity)

`bamboo_portal`, `bamboo_outdoor_shower`, `candle_path` are typology-amenities and ship their own 3-shot footprint already; they get a reduced shotlist (§4.E).

## 2. What's missing — the gap analysis

| Missing dimension | Why it matters | Cost to add |
|---|---|---|
| **Cardinal elevations** (N/E/S/W orthographic) | Architects, contractors, and Wesley's permit packet expect orthographic facades. Hero 3/4 alone is sales material, not buildable documentation. | 4 cameras per asset, no geometry change. |
| **Top-down plan** | Footprint legibility. Reads roof geometry. Disambiguates curved vs rectangular family villas. | 1 orthographic camera, +Z 50 m. |
| **Long-axis + cross sections** | Shows interior volumes, ceiling height, mezzanine relationships. Required for energy / passive-design verification (Rule 6: ≤35 °C). | 1 clipping-plane per axis. Two cameras. |
| **X-ray cutaway** (transparent shell, see structure + services) | Demonstrates Rule 4 (stone plinth), Rule 5 (overhangs), Rule 7 (micro-hydro + LiFePO4 visible), Rule 10 (mosquito mesh on cisterns). Currently invisible. | 1 camera + material override. |
| **Interior eye-level** | Vacation-rental marketing requires it. European tourist buyers (per `EUROPEAN_TOURISM_SPEC.md`) decide on interior photos. | 1–2 cameras, requires furniture stubs in typologies (currently absent). |
| **Detail close-ups** | Joinery (lapacho-bamboo joins), tatakuá oven, roof underside (rule 5 overhang), services panel. Wesley uses these to verify Rule 8 (culturally Paraguayan). | 1–3 cameras, 50 mm macro. |
| **Per-house improvements not yet shipped** | See `docs/DEFERRED_BUGS.md` Bug 1 (black water), Bug 2 (plastic lapacho), Bug 3 (`.003` flora LOD collision). Bug 2 is the highest-leverage fix; lapacho timber reads as plastic across 17 assets. Multi-angle shots will amplify the failures, not hide them — **bugs 1–2 must land before mass re-render**. | Per DEFERRED_BUGS estimate: 1.5 dev-days. |

## 3. The 12-shot canonical matrix

For each house, render 12 shot types × 3 lighting variants = **36 PNGs per house** at final resolution. Total: 16 houses × 36 = **576 finals**.

| # | Shot tag | Camera class | Purpose | Lens | Variants |
|---|---|---|---|---|---|
| 1 | `hero_se` | 3/4 perspective | Existing hero (back-compat) | 28–35 mm | A,B,C |
| 2 | `elev_n` | Orthographic N→S | Cardinal elevation, structural | ortho | A,B |
| 3 | `elev_e` | Orthographic E→W | Cardinal elevation, structural | ortho | A,B |
| 4 | `elev_s` | Orthographic S→N | Cardinal elevation, structural | ortho | A,B |
| 5 | `elev_w` | Orthographic W→E | Cardinal elevation, structural | ortho | A,B |
| 6 | `plan` | Orthographic top-down | Roof + footprint | ortho | B |
| 7 | `section_long` | Perspective, clip-plane on long axis | Interior volume, ceiling height | 28 mm | A,B,C |
| 8 | `section_cross` | Perspective, clip-plane on short axis | Cross-ventilation path (Rule 6) | 28 mm | A,B,C |
| 9 | `xray` | Hero angle, transparent BSDF override | Structure + services visible through shell | 28 mm | B |
| 10 | `interior_main` | Eye-level, inside main room | Hospitality marketing | 24 mm | A,C |
| 11 | `interior_sleep` | Eye-level, inside sleep area (where applicable) | Hospitality marketing | 24 mm | C |
| 12 | `detail` | 50 mm close, joinery / services panel / overhang | Rule verification (4, 5, 7, 8, 10) | 50 mm | A,B |

**Variant count rationale:** orthographic elevations don't benefit from blue-hour, so we save ~30% render budget by skipping variant C on shots 2–6 and 12. The `plan` shot only needs B (neutral, overcast) since A/C add sun-glare on a top-down. Interior shots invert: A is warm daylight, C is the "lit windows at dusk" hero for rental marketing.

Per-house total: 1×3 + 4×2 + 1×1 + 2×3 + 1×1 + 1×2 + 1×1 + 1×2 = **24 PNGs** (not 36 — the variant pruning above brings it down).

Full corpus: 16 × 24 = **384 finals** + 16 × 24 previews at 720p = **768 PNGs total**.

## 4. Per-asset specializations

### A. Houses on water (loggia / river plane visible)

`italian_river_house_4pax`, `container_river_house`, `bamboo_river_house`

- Section `cross` must cut through the river plane. Show pile/stilt structure under floor.
- `xray` must reveal the stilts and flood-clearance gap. This is Rule 4 evidence the house "doesn't touch the ground."
- Add a `detail_pile` shot at 50 mm of the stilt-to-foundation joint.
- **Blocked on `DEFERRED_BUGS` Bug 1** — current water shader renders as black slab; multi-angle would multiply the visibility of the bug.

### B. Earth-integrated houses

`hobbit_house`, `cob_bottle_lqv`

- Add `section_long` cut on east face to show sod-roof depth (250–400 mm) — passive-design evidence.
- `xray` of `cob_bottle_lqv` must show the bottle wall in cross-section (the bottle bottoms reading as colored disks through translucent cob). This is the *signature* shot for La Quebrada Viva.
- `detail_bottle_wall` at 50 mm: bottle bases protruding through interior cob, light passing through.
- `detail_tatakua` at 50 mm: clay oven (`lqv/subscene/tatakua.py` exists) integrated to corredor.

### C. Bamboo-shell houses

`bamboo_river_house`, `bamboo_container_4pax`, `bamboo_wigwam_lodge`, `bamboo_boomhut_treehouse`, `bamboo_curved_roof_villa`

- Add a `detail_culm_join` shot at 50 mm: bamboo-to-bamboo lashing or steel-collar joint. Demonstrates structural credibility.
- `xray` should reveal interior bamboo structural frame distinct from woven exterior skin — these are visually distinct in the typologies and reading them apart matters for procurement.
- `bamboo_boomhut_treehouse`: add `view_up_from_below` shot, 24 mm wide, showing the treehouse from ground level looking up through the canopy.

### D. Hybrid bamboo-concrete + signature villas

`bamboo_beton_28`, `bamboo_beton_30`, `bamboo_beton_family_curved`, `bamboo_beton_family_rectangular`, `bamboo_curved_roof_villa`, `clay_terracotta_estate`

- These are the largest typologies (28–70 m², 1–2 storey). Add a `hero_aerial` shot at 45° elevation, 18–22 m distance — between hero_se and plan.
- `bamboo_beton_family_curved` and `bamboo_curved_roof_villa`: the curved roof is the value prop. Add `detail_roof_ribs` at 50 mm showing the lapacho rib geometry.
- `clay_terracotta_estate`: 2-storey, so `interior_sleep` is the upstairs bedroom. Section cuts must show stair geometry.

### E. Typology amenities (reduced shotlist)

`bamboo_portal`, `bamboo_outdoor_shower`, `candle_path`

These are sub-house-scale. Keep current 3-variant hero + add only:
- `elev_front` (single ortho elevation, not all four)
- `detail` (joinery / lantern / shower-head)
- `xray` for `bamboo_outdoor_shower` only (shows plumbing — rule 6 / rule 10 cistern context)

Total per amenity: 3 + 2 = **5 PNGs**. Three amenities × 5 = 15 PNGs.

## 5. Implementation strategy — driver changes

### 5.1 New env var: `RENDER_VIEW`

Don't overload the `RENDER_VARIANT` alphabet (A/B/C are lighting and pytest enforces it via `tests/test_typology_contract.py` and `tests/test_render_catalogue.py`). Introduce a parallel axis:

```bash
RENDER_VIEW=hero|elev_n|elev_e|elev_s|elev_w|plan|section_long|section_cross|xray|interior_main|interior_sleep|detail
```

Default `RENDER_VIEW=hero` preserves existing behavior byte-for-byte. Adding new branches inside each `lqv/subscene/<asset>.py` is additive; no composite path changes.

### 5.2 Output paths

```
renders/sub/runs/<RENDER_RUN_ID>_<asset>_<view>/<variant>.png
renders/sub/latest/<asset>_<variant>_<view>.png
renders/sub/<asset>_<variant>_<view>.png            # flat back-compat; hero stays unsuffixed
```

Hero shot (default view) keeps the existing flat path `renders/sub/<asset>_<variant>.png` to preserve the back-compat invariant. New views land at `<asset>_<variant>_<view>.png`. Pre-existing tooling reads only the hero path; no breakage.

### 5.3 Camera helpers — additions to `lqv/cameras.py`

Add four new helpers (none break existing signatures):

```python
def subscene_ortho_elevation(target, cardinal: str, bbox_size: float, height: float = 2.4)
def subscene_ortho_plan(target, bbox_size: float, height: float = 50.0)
def subscene_section_camera(target, axis: str, clip_offset: float, distance: float, lens: float = 28.0)
def subscene_interior_camera(target_inside, eye_height: float = 1.6, lens: float = 24.0)
```

`bbox_size` is asset-tuned per driver. The clip-plane offset uses Blender's camera `clip_start` shifted into the geometry rather than a true geometry boolean — cheaper, deterministic, no mesh edits.

### 5.4 X-ray override

Implement as a material-override pass in `lqv/subscene/base.py`:

```python
def apply_xray_override(scene, asset_collection, except_materials: set[str]):
    """Swap exterior-wall materials for a Transparent BSDF (alpha=0.15) on render-time only.
    Preserves Boolean cutters and lighting. Excludes furniture, services, and structural
    materials in `except_materials` so the structure + services stay opaque."""
```

`except_materials` for each house lists what stays solid: bamboo/lapacho structural members, micro-hydro turbine, LiFePO4 rack, cistern shell, mosquito mesh, plumbing, fireplace stack. Everything else (cob walls, sod roof, terracotta tile, beton infill, plaster) goes 85% transparent.

### 5.5 Section clipping

Cycles supports per-camera `clip_start` but a true cut-plane needs either:
1. A Boolean modifier on the building parent (expensive, mesh edit on hot path), or
2. A camera-aligned `clip_start` shifted past the front wall, leaving a hard cut edge (cheap, no mesh change).

**Use option 2.** Drawback: cut edge has no shaded interior face. Mitigation: place a low-intensity area light just behind the camera so the cut interior reads as a dark-but-visible volume rather than pure black.

### 5.6 Interior shots — geometry prerequisites

**Stub status:** interior shots require furniture stubs in `lqv/typologies/<asset>.py`. Audit per typology before scheduling the interior batch — most typologies model the shell + roof but no bed/table/services. Stub furniture as box-modeled primitives with the canonical materials:

- Bed: 2.0 m × 1.4 m × 0.5 m, `linen_white` mattress, `lapacho_timber` frame
- Table: 1.2 m × 0.8 m × 0.75 m, `lapacho_timber`
- Bench: 1.0 m × 0.4 m × 0.45 m, `lapacho_timber`
- Stove: 0.6 m × 0.6 m × 0.9 m, `metal_black`
- Cistern (visible): 0.8 m ⌀, `concrete_grey` + mosquito-mesh emission top (Rule 10)

This is a single PR's worth of work (~6 hours) across the 16 typologies. Land it as a stub pass; refine geometry in a later sprint.

## 6. Render budget — host constraints

Per `feedback_render_parallelism.md`: 14 GB host MUST serialize sub-renders. Per `feedback_subscene_clip_end.md`: each driver MUST set `cam.data.clip_end >> 100 m`.

| Stage | Count | Samples | Time/shot | Wall time |
|---|---|---|---|---|
| Preview pass (review) | 768 | 64 | ~25 s | ~5.3 h |
| Final pass (deliverable) | 384 | 256–512 | ~100 s | ~10.7 h |

Run the preview pass overnight first (single batch, `RENDER_RUN_ID=multiview_preview_2026-06-30` after escritura). Review the contact sheet, fix per-asset framings, then queue finals.

## 7. Improvements analysis — what gets better with multi-view

| Improvement category | Currently | After multi-view |
|---|---|---|
| Documentation rigor | 3 PNGs per house, single angle | 24 PNGs per house, orthographic + plan + section — usable by a builder |
| Rule verification (the 10) | Hero hides Rule 4 (plinth), Rule 5 (overhang depth), Rule 7 (hidden services), Rule 10 (cistern mesh) | `xray` + `detail` shots make every rule auditable from a single contact sheet |
| Rental marketing | Zero interior shots | `interior_main` (warm A) + `interior_sleep` (dusk C with window glow) per house — the Airbnb-shaped image pack |
| Permit packet | Hero not acceptable to municipal review | Cardinal elevations + plan + section = permit-ready set |
| Material truth | Black water + plastic lapacho bugs hidden by camera angle | Multi-angle exposure forces material fixes (DEFERRED_BUGS Bug 1+2) — net positive |
| Pre-build verification | Wesley/contractors cannot see structural intent | `xray` makes stilts, beam runs, services all visible — pre-construction verification possible |

## 8. Sequencing — what to do, in what order

Post-escritura sprint, weeks 1–3:

**Week 1 (post-2026-06-27):**
1. Fix DEFERRED_BUGS Bug 1 (black water shader) — 1 day.
2. Fix DEFERRED_BUGS Bug 2 (lapacho plastic) — 1 day.
3. Land furniture stubs across 16 typologies — 1 day.
4. Add `RENDER_VIEW` env handling + new camera helpers in `lqv/cameras.py` — 1 day.

**Week 2:**
5. Implement `apply_xray_override` in `lqv/subscene/base.py` — 0.5 day.
6. Wire up new views in each of 16 subscene drivers — 2 days (one PR per material family: italian, bamboo, beton+villa, hobbit+cob, container).
7. First preview batch (768 shots, overnight) + contact-sheet review — 1 day.

**Week 3:**
8. Per-asset framing fixes from contact-sheet review — 1 day.
9. Final batch (384 shots, two overnights).
10. New `docs/render_catalogue/INDEX.md` section + bundle the multi-view pack into the next Wesley deliverable.

Total: **~10 dev-days + 3 overnight render windows.**

## 9. Out of scope here

- Animation / fly-through. Treated separately if Wesley wants a video pack.
- VR / 360° panoramas. Same — separate sprint.
- Photogrammetry-based texture refresh. Tracked under the asset-researcher pass.
- Composite (`build_scene.py`) recamera. The 6-camera composite (hero/stream_up/terrace/cliff/dusk/petal_macro) stays byte-frozen at `85e86aa`; this work is all sub-render side.

## 10. References

- `docs/sub_render_strategy.md` — sub-render-first workflow doctrine
- `docs/DEFERRED_BUGS.md` — Bug 1 (water), Bug 2 (lapacho), Bug 3 (flora LOD)
- `docs/MASTER_BRIEF.md` §14 — the 10 design rules the `xray` + `detail` shots prove
- `docs/EUROPEAN_TOURISM_SPEC.md` — buyer profile that drives `interior_*` need
- `lqv/cameras.py:55` — `subscene_camera()` baseline being extended
- `lqv/subscene/base.py:79` — `VARIANT_PROFILES` (lighting) which stays untouched
- `memory/feedback_subscene_clip_end.md` — clip_end gotcha that bit us at `4409dba`
- `memory/feedback_render_run_folders.md` — `RENDER_RUN_ID` path convention
- `memory/feedback_render_parallelism.md` — serial-execution hard ceiling
