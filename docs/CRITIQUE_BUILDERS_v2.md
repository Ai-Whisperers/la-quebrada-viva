# Builder roast v2 — 17 typologies + amenities (2026-06-13)

Honest-roast format. Cited line numbers are from the files at HEAD. Author: `critic` subagent + visual cross-check on `renders/sub/latest/*_A.png`.

## Visual cross-check (from 4 spot-checked PNGs)

| Asset | Visible problem |
|---|---|
| `bamboo_river_house_A.png` | Curved roof reads as a fiberglass tent. Ground is one stripe-textured slab. No river. Stilts terminate mid-air with no shadow. Stairs go to nowhere. |
| `hobbit_house_A.png` | Pink-soil ground cube. Dome sits on top of it like a turtle. One stray fern. No berm cut. Window disc reads as a frog eye. |
| `italian_river_house_4pax_A.png` | Plywood-clad cube. Window planes proud of facade as critic flagged. Black corner pillars don't read as Italian stone. No river. Same stripe-textured ground slab. |
| `labrisa_lounge_A.png` | Four white posts holding a slab roof. Reads as a parking structure for a giant Tic-Tac. No bamboo culms. No creek. No pendants. |

## Universal root cause (one fix, 17 renders helped)

- `lqv/subscene/base.py:place_neutral_ground` paints a huge displacement-textured cube as "ground". It reads as cardboard at every render distance. Replace with a real Plane + photoreal grass/earth shader + radial vignette to dirt at edges. Also: `setup_world` defaults to sunset HDRI tint, washing every material into the orange band. Add a noon variant for A and golden-hour for B (currently all 17 _A.png are golden-hour).

## Shared issues (cross-cutting)

- All 17 builders ignore `variant` beyond name-tagging. Variant differentiation lives only in `lqv.subscene.base` lighting/HDRI. Caller comments like "exposure +0.6 in `build_scene.py`" mean the builder geometry is identical A/B/C — fix: gate at least seed jitter (cushion positions, sapling rotation) on `variant` so A/B/C aren't byte-identical geometry.
- `_mat()` / `_resolve()` chains return `None` silently across `hobbit_house.py`, `italian_river_house_4pax.py`, `container_river_house.py`, `bamboo_river_house.py`, `bamboo_container_4pax.py`, `eco_pool.py:169-175`, `floating_dining.py:167-173`, `eco_retreat_modern_oasis.py:168-173`. A missing MAT key renders untextured grey. `hobbit_house._resolve` is the lone one that raises — and it's the right behavior; the rest are wrong.
- Cross-cutting semantically-wrong fallbacks: `sandstone` for lapacho/plywood, `cob_raw` for polished concrete, `palm_thatch` for window glow & mosquito mesh, `water_reflective` for clear glass, `pv_glass` for water surface (`eco_retreat_modern_oasis.py:275`), `concrete_slab_108` for corten steel.
- Walls/roofs/floors are scaled cubes throughout. Glass/doors are inset or proud slabs, never boolean-cut. Hobbit dome and eco_retreat dome use boolean — inconsistent.
- MATERIAL_TAKEOFF dishonesty pattern: arbitrary fudge factors (35%/30% plinth coverage), fake quantities for non-existent geometry (+1.5 / +1.4 m² louver-frame glass), 22 kg hardcoded lashings (labrisa), 65 m magic strut length (eco_retreat). Container count 1→4 in `bamboo_container_4pax.py` to hit a marketing number.
- Two "river houses" (`italian_river_house_4pax.py`, `bamboo_river_house.py`) declare river constants but never build a river plane. `container_river_house.py` doesn't either.
- "Wesley character" doors ≤ 2 m: never asserted anywhere. Several french-door/spine-door slabs in the beton family are 2.1 m+; eco_retreat curtain wall is 3.0 m tall (`CURTAIN_WALL_HEIGHT_M = 3.0`) with no door cut at all.
- Borax treatment overestimated: 0.18 kg/m (beton family), 0.6 kg/m (beton_28). Typical 0.10-0.15 kg/m.
- `random.uniform` used at module scope in labrisa, eco_pool — relies on caller seeding. Fragile.
- Wide silent `except Exception: pass` in eco_pool, floating_dining, eco_retreat_modern_oasis. Flora silently absent.

## Per-builder roast

### `lqv/typologies/hobbit_house.py`
- `_resolve` raises `KeyError` on miss while every sibling returns `None`. Pick loud everywhere.
- Boolean-cut half-dome OK; but no berm cut into terrain. Reads as a dome on flat ground.
- Window disc is `primitive_cylinder` with `depth=0.05` (no glass behind, no frame).
- `variant` ignored.

### `lqv/typologies/italian_stone_small_v1.py`
- `MATERIAL_TAKEOFF['stone_walls'].volume_m3 = 14.0` hardcoded — derive from `_stone_perimeter_m * wall_h * wall_t`.
- Otherwise solid (factors via `lqv/house/stone_wall`).

### `lqv/typologies/italian_stone_small_v2.py`
- Docstring says "gable triangles" but geometry is monopitch.
- French door 0.04 m proud, no cut.
- `MATERIAL_TAKEOFF` hand-typed.
- `PAD_SIZE_M = 1.6` for 10×7 footprint — pad is ¼ door width. Probably meant `16.0`.

### `lqv/typologies/italian_river_house_4pax.py`
- `_RIVER_WIDTH = 8.0`, `_RIVER_PLANE_LEN = 20.0` declared, never used.
- Roof fallback `terracotta_tile → laterite` — orange tile to brown soil.
- Balcony glass clips wall (proud slab, no cut).
- `variant` ignored.

### `lqv/typologies/container_river_house.py`
- Entire MATERIAL_TAKEOFF hardcoded.
- Glass wall 0.04 m proud, no cut.
- 3 bamboo accents on a container — Rule 8 violation (container ≠ Paraguayan vernacular).
- HVAC vent magic offsets `0.27`, `1.83` no comment.
- `_resolve('corten_steel', 'steel_anodized')` — anodized aluminum is brushed silver, not rust-orange.
- No river plane.

### `lqv/typologies/bamboo_river_house.py`
- 90-cylinder rib bamboo ring — heavyweight. `lqv/house/bamboo_frame.build_bamboo_radial_frame` exists; use it.
- River plane delegated to driver but constants declared here — coupling leak.
- Deck has no plank pattern.
- Main deck has no railing — fall hazard from 1.2 m above water.
- `_mat('lapacho_timber', 'sandstone')` — light wood → grey stone.

### `lqv/typologies/bamboo_wigwam_lodge.py`
- Stone foundation at `z+0.001`, dome at `z-0.05` — 5 cm visible gap.
- Door cut only on outer shell; inner liner solid.
- Otherwise cleanest typology.

### `lqv/typologies/bamboo_container_4pax.py`
- BoQ DISHONESTY: container quantity inflated 1 → 4 with explicit fudge comment. Remove the fudge.
- Thatch area double-counts corner overlap.
- Bizarre fallback chains (palm_thatch for window_glow, etc.).

### `lqv/typologies/bamboo_boomhut_treehouse.py`
- Top stair tread at z=3.95 m, platform at z=4.00 m → 5 cm gap.
- Mosquito mesh fallback chains to `palm_thatch` — Rule 10 violation.
- Vista window uses cobalt-blue glass — blocks the vista.
- No rail-gap where bridge meets platform.
- Rope assumes flat ground; on sloped terrain ropes intersect ground.

### `lqv/typologies/bamboo_beton_30.py`
- "35% plinth coverage" arbitrary fudge.
- `_fasteners_count = 12*8 + 24 + 80 + 50 + 40` — magic.
- 6×2.4 m service wall solid slab — Rule 6 cross-vent violation.
- Roof tilt about origin — works by luck; fragile.
- `cob_raw` fallback for polished concrete (brown earth vs grey panel).

### `lqv/typologies/bamboo_beton_28.py`
- 30% plinth fudge (different from v30's 35% — both arbitrary).
- `+1.4 m² louver-frame glass` — no panels in geometry. Fake quantity.
- Borax `0.6 kg/m` — 3-6× typical.
- Docstring promises `lqv.house.bamboo_frame` reuse; actual code copies v30 inline.

### `lqv/typologies/bamboo_beton_family_curved.py`
- Docstring admits inlines v30-style helpers — sibling factor incomplete.
- Roof Euler `(0.0, slope_rad, am)` depends on Blender's intrinsic XYZ default. Fragile.
- `+1.5 m² pv_glass_clerestory` for "4 BR vent panels" — no panels in build.
- L391/411/429 `_resolve('concrete_slab_108', 'cob_raw', 'sandstone')` — concrete falls back to brown earth.
- L595 curtain cloth `cob_raw` fallback — textile drapes ≠ wet mud.
- Clerestory glass + spine doors proud, no cut.
- Borax 0.18 kg/m (2× typical).

### `lqv/typologies/bamboo_beton_family_rectangular.py`
- L569/585 gable cladding `_resolve('lapacho_timber', 'sandstone')` — light wood → grey stone.
- `_gable_triangles` docstring admits it's a "low-height cap rather than a true triangle".
- Spine doors proud planar slabs.
- East louver proud of gable wall.
- Borax 0.18 kg/m.
- Rebar 95 kg/m³ (top of 80-100 range).
- Cob_raw fallback for concrete (shared with `_curved`).

### `lqv/amenities/labrisa_lounge.py`
- L173-189 `_ring_beam` builds 4 parallel joists along Y, not a perimeter ring. Misnamed.
- L180 joists in central 3.5 m of 8 m platform — outer 2.25 m cantilevers off nothing.
- 4 corner columns for 8×9 m thatch roof — 7 m unsupported span.
- L201-214 normal winding may face inward; force `normals_make_consistent`.
- L219 fallback to `'canopy'` — not a registered MAT key.
- L313 module-level random.uniform — fragile.
- L102-103 lashings hardcoded 22 kg.

### `lqv/amenities/eco_pool.py`
- L196 `_mat('stream_bed', 'sandstone', 'laterite')` — pool floor falls back to red soil.
- Deck 4 overlapping cube strips at corners — Z-fight risk.
- L262 pool water is 0.06 m thick cube — reads as jelly slab.
- L571 shower head fallback chain → lapacho (copper → wood).
- L629 height `4.6 + 0.4 * ((j * 13) % 5) / 5.0` — modular determinism pretending to be jitter.
- L617 bamboo clumps from `bamboo_frame.build_bamboo_culm`, not `lqv.flora.bamboo.add_bamboo_clump`. Two-track flora.

### `lqv/amenities/floating_dining.py`
- L80 docstring claims "no walls, no solid roof" — but lantern ring beam is 0.10 m Ø, invisible at parcel distance.
- L408 `span = 8.0` for 9 lanterns on 8 m deck — pendants overlap corner posts.
- L181 water plane fallback chain ends in `pv_glass` (solar panel).
- L130 lantern unit_cost $130 × 9 + L144 wiring set $420 — wiring should be per-lantern.
- L481/491 silent `except Exception: pass`.
- L455 catwalk post name `int(side)` produces `-1`/`1`. Use `L`/`R`.
- L296 3-leg stool angles aren't offset by stool index — all stools' legs at same θ. Reads gridded.

### `lqv/amenities/eco_retreat_modern_oasis.py`
- L80 `_DOME_STRUT_LENGTH_M = 65.0` magic — derive from edges.
- L79 `_DOME_PANEL_AREA_M2 = 2.0 * math.pi * R * H` — wrong formula (`2πR²` for hemisphere; accidentally works only because R==h).
- L275 water plane fallback ends `pv_glass` (solar).
- L201-265 dome `from_pydata` + boolean — breaks all-cube-slab pattern. Factor into `lqv/subscene/geo_dome.py`.
- L412 `CURTAIN_WALL_HEIGHT_M = 3.0` — 5.4 m × 3.0 m wall east of deck, NO door cut. Guests walk around.
- L386 `post_positions[:DECK_POST_COUNT]` — comment claims 16, code accumulates 12. Silent truncation.
- L658 same modulo-as-jitter pattern as eco_pool.
- L596+ `except Exception` + `traceback.print_exc` — at least it logs.

## Beautification priorities (visible-in-render leverage)

1. **`lqv/subscene/base.py:place_neutral_ground`** — replace cube with Plane + photoreal grass/earth + edge vignette. Helps every render.
2. **Context flora** — each driver scatters 5-20 grass/fern/agave/bamboo clumps within 8 m radius of asset.
3. **River planes** — 3 river_house drivers add water plane.
4. **Hobbit berm** — driver embeds dome in a low hill.
5. **Material fallback chains** — fix the worst (glass→water_reflective, concrete→cob_raw, lapacho→sandstone, pool floor→laterite).
6. **Proud-plane glass** — push flush or boolean-cut.
7. **Container BoQ honesty** — remove 1→4 fudge.
8. **Eco-retreat curtain wall door cut** — 0.9 m gap.
9. **Variant differentiation** — A/B/C respect at driver level (HDRI + sun + jitter seed).
