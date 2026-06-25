# Houses Review — 2026-06-14

Hand-off review gallery for Wesley's full La Quebrada Viva catalog: 13 typologies + 4 amenities, 3 variants each (A interior-dawn, B neutral mid-day, C hero-golden). 51 sub-renders total.

§-refs trace back to `docs/TERRAIN_PIVOT.md` (§3.x typologies, §4.x amenities). Thumbnail paths point at the `renders/sub/latest/` mirror — the per-run originals live at `renders/sub/runs/review_2026-06-14_<asset>/<variant>.png`.

## Methodology

- Batch: `scripts/render_review_2026_06_14.sh` (cap-4 via `xargs -P4`).
- Env per job: `RENDER_RUN_ID=review_2026-06-14 RENDER_VARIANT={A,B,C} RENDER_FLORA_PHOTOREAL=1 RENDER_RES=preview RENDER_SAMPLES=64 PYTHONPATH=$ROOT`.
- Per-asset logs: `renders/sub/runs/review_2026-06-14_logs/<asset>_<variant>.log`.
- Builder under `lqv/typologies/` or `lqv/amenities/`; subscene driver mirror under `lqv/subscene/<asset>.py`.

Variant profiles (per `lqv/subscene/base.py:VARIANT_PROFILES`):

| Variant | Mood | Sun elev / azim | Strength |
|---|---|---|---|
| A | Interior / dawn | low, east | warm, dim |
| B | Neutral mid-day | high, neutral | flat reference |
| C | Hero / golden | low-west, golden | strong, saturated |

## Catalog

### Typologies (§3.x)

| §-ref | Asset · LOC | A — interior/dawn | B — neutral mid-day | C — hero/golden |
|---|---|---|---|---|
| §3.1 | [hobbit_house](../lqv/typologies/hobbit_house.py) · 444<br>~6 m round cob half-dome embedded in berm, ~3 m crown | <a href="../renders/sub/latest/hobbit_house_A.png"><img src="../renders/sub/latest/hobbit_house_A.png" width="220"></a> | <a href="../renders/sub/latest/hobbit_house_B.png"><img src="../renders/sub/latest/hobbit_house_B.png" width="220"></a> | <a href="../renders/sub/latest/hobbit_house_C.png"><img src="../renders/sub/latest/hobbit_house_C.png" width="220"></a> |
| §3.2 | [italian_stone_small_v1](../lqv/typologies/italian_stone_small_v1.py) · 446<br>Small 2-PAX rural Italian stone cottage, single storey | <a href="../renders/sub/latest/italian_stone_small_v1_A.png"><img src="../renders/sub/latest/italian_stone_small_v1_A.png" width="220"></a> | <a href="../renders/sub/latest/italian_stone_small_v1_B.png"><img src="../renders/sub/latest/italian_stone_small_v1_B.png" width="220"></a> | <a href="../renders/sub/latest/italian_stone_small_v1_C.png"><img src="../renders/sub/latest/italian_stone_small_v1_C.png" width="220"></a> |
| §3.3 | [italian_stone_small_v2](../lqv/typologies/italian_stone_small_v2.py) · 627<br>Sister of v1, identical stone grammar, different massing | <a href="../renders/sub/latest/italian_stone_small_v2_A.png"><img src="../renders/sub/latest/italian_stone_small_v2_A.png" width="220"></a> | <a href="../renders/sub/latest/italian_stone_small_v2_B.png"><img src="../renders/sub/latest/italian_stone_small_v2_B.png" width="220"></a> | <a href="../renders/sub/latest/italian_stone_small_v2_C.png"><img src="../renders/sub/latest/italian_stone_small_v2_C.png" width="220"></a> |
| §3.4 | [italian_river_house_4pax](../lqv/typologies/italian_river_house_4pax.py) · 504<br>Two-storey Italian-stone river-bank house, 4 PAX | <a href="../renders/sub/latest/italian_river_house_4pax_A.png"><img src="../renders/sub/latest/italian_river_house_4pax_A.png" width="220"></a> | <a href="../renders/sub/latest/italian_river_house_4pax_B.png"><img src="../renders/sub/latest/italian_river_house_4pax_B.png" width="220"></a> | <a href="../renders/sub/latest/italian_river_house_4pax_C.png"><img src="../renders/sub/latest/italian_river_house_4pax_C.png" width="220"></a> |
| §3.5 | [container_river_house](../lqv/typologies/container_river_house.py) · 300<br>20-ft shipping container on stilts over creek bend | <a href="../renders/sub/latest/container_river_house_A.png"><img src="../renders/sub/latest/container_river_house_A.png" width="220"></a> | <a href="../renders/sub/latest/container_river_house_B.png"><img src="../renders/sub/latest/container_river_house_B.png" width="220"></a> | <a href="../renders/sub/latest/container_river_house_C.png"><img src="../renders/sub/latest/container_river_house_C.png" width="220"></a> |
| §3.6 | [bamboo_river_house](../lqv/typologies/bamboo_river_house.py) · 609<br>Critical-path creek typology, stilt-mounted bamboo + footbridge | <a href="../renders/sub/latest/bamboo_river_house_A.png"><img src="../renders/sub/latest/bamboo_river_house_A.png" width="220"></a> | <a href="../renders/sub/latest/bamboo_river_house_B.png"><img src="../renders/sub/latest/bamboo_river_house_B.png" width="220"></a> | <a href="../renders/sub/latest/bamboo_river_house_C.png"><img src="../renders/sub/latest/bamboo_river_house_C.png" width="220"></a> |
| §3.7 | [bamboo_container_4pax](../lqv/typologies/bamboo_container_4pax.py) · 776<br>Shipping container + bamboo-frame wraparound veranda, 4 PAX | <a href="../renders/sub/latest/bamboo_container_4pax_A.png"><img src="../renders/sub/latest/bamboo_container_4pax_A.png" width="220"></a> | <a href="../renders/sub/latest/bamboo_container_4pax_B.png"><img src="../renders/sub/latest/bamboo_container_4pax_B.png" width="220"></a> | <a href="../renders/sub/latest/bamboo_container_4pax_C.png"><img src="../renders/sub/latest/bamboo_container_4pax_C.png" width="220"></a> |
| §3.8 | [bamboo_wigwam_lodge](../lqv/typologies/bamboo_wigwam_lodge.py) · 540<br>Small fat-bottomed conical glamping wigwam, bamboo frame | <a href="../renders/sub/latest/bamboo_wigwam_lodge_A.png"><img src="../renders/sub/latest/bamboo_wigwam_lodge_A.png" width="220"></a> | <a href="../renders/sub/latest/bamboo_wigwam_lodge_B.png"><img src="../renders/sub/latest/bamboo_wigwam_lodge_B.png" width="220"></a> | <a href="../renders/sub/latest/bamboo_wigwam_lodge_C.png"><img src="../renders/sub/latest/bamboo_wigwam_lodge_C.png" width="220"></a> |
| §3.9 | [bamboo_boomhut_treehouse](../lqv/typologies/bamboo_boomhut_treehouse.py) · 455<br>Dutch boomhut hexagonal bamboo treehouse, 3 lapacho hosts, 2 PAX | <a href="../renders/sub/latest/bamboo_boomhut_treehouse_A.png"><img src="../renders/sub/latest/bamboo_boomhut_treehouse_A.png" width="220"></a> | <a href="../renders/sub/latest/bamboo_boomhut_treehouse_B.png"><img src="../renders/sub/latest/bamboo_boomhut_treehouse_B.png" width="220"></a> | <a href="../renders/sub/latest/bamboo_boomhut_treehouse_C.png"><img src="../renders/sub/latest/bamboo_boomhut_treehouse_C.png" width="220"></a> |
| §3.10 | [bamboo_beton_30](../lqv/typologies/bamboo_beton_30.py) · 466<br>Hybrid micro-house, 2 PAX, polished-concrete spine + woven bamboo | <a href="../renders/sub/latest/bamboo_beton_30_A.png"><img src="../renders/sub/latest/bamboo_beton_30_A.png" width="220"></a> | <a href="../renders/sub/latest/bamboo_beton_30_B.png"><img src="../renders/sub/latest/bamboo_beton_30_B.png" width="220"></a> | <a href="../renders/sub/latest/bamboo_beton_30_C.png"><img src="../renders/sub/latest/bamboo_beton_30_C.png" width="220"></a> |
| §3.11 | [bamboo_beton_28](../lqv/typologies/bamboo_beton_28.py) · 524<br>Stripped sibling of `bamboo_beton_30`, smaller footprint | <a href="../renders/sub/latest/bamboo_beton_28_A.png"><img src="../renders/sub/latest/bamboo_beton_28_A.png" width="220"></a> | <a href="../renders/sub/latest/bamboo_beton_28_B.png"><img src="../renders/sub/latest/bamboo_beton_28_B.png" width="220"></a> | <a href="../renders/sub/latest/bamboo_beton_28_C.png"><img src="../renders/sub/latest/bamboo_beton_28_C.png" width="220"></a> |
| §3.12 | [bamboo_beton_family_curved](../lqv/typologies/bamboo_beton_family_curved.py) · 680<br>Family-scale crescent / banana plan, convex side bamboo screen | <a href="../renders/sub/latest/bamboo_beton_family_curved_A.png"><img src="../renders/sub/latest/bamboo_beton_family_curved_A.png" width="220"></a> | <a href="../renders/sub/latest/bamboo_beton_family_curved_B.png"><img src="../renders/sub/latest/bamboo_beton_family_curved_B.png" width="220"></a> | <a href="../renders/sub/latest/bamboo_beton_family_curved_C.png"><img src="../renders/sub/latest/bamboo_beton_family_curved_C.png" width="220"></a> |
| §3.13 | [bamboo_beton_family_rectangular](../lqv/typologies/bamboo_beton_family_rectangular.py) · 697<br>Family-scale rectangular sibling, same hybrid grammar | <a href="../renders/sub/latest/bamboo_beton_family_rectangular_A.png"><img src="../renders/sub/latest/bamboo_beton_family_rectangular_A.png" width="220"></a> | <a href="../renders/sub/latest/bamboo_beton_family_rectangular_B.png"><img src="../renders/sub/latest/bamboo_beton_family_rectangular_B.png" width="220"></a> | <a href="../renders/sub/latest/bamboo_beton_family_rectangular_C.png"><img src="../renders/sub/latest/bamboo_beton_family_rectangular_C.png" width="220"></a> |

### Amenities (§4.x)

| §-ref | Asset · LOC | A — interior/dawn | B — neutral mid-day | C — hero/golden |
|---|---|---|---|---|
| §4.1 | [eco_pool](../lqv/amenities/eco_pool.py) · 679<br>Wellness pool with organic shoreline, not a suburban rectangle | <a href="../renders/sub/latest/eco_pool_A.png"><img src="../renders/sub/latest/eco_pool_A.png" width="220"></a> | <a href="../renders/sub/latest/eco_pool_B.png"><img src="../renders/sub/latest/eco_pool_B.png" width="220"></a> | <a href="../renders/sub/latest/eco_pool_C.png"><img src="../renders/sub/latest/eco_pool_C.png" width="220"></a> |
| §4.2 | [floating_dining](../lqv/amenities/floating_dining.py) · 527<br>8 m × 5 m open-air platform appearing to float over the creek | <a href="../renders/sub/latest/floating_dining_A.png"><img src="../renders/sub/latest/floating_dining_A.png" width="220"></a> | <a href="../renders/sub/latest/floating_dining_B.png"><img src="../renders/sub/latest/floating_dining_B.png" width="220"></a> | <a href="../renders/sub/latest/floating_dining_C.png"><img src="../renders/sub/latest/floating_dining_C.png" width="220"></a> |
| §4.3 | [labrisa_lounge](../lqv/amenities/labrisa_lounge.py) · 400<br>Central social space, creek runs through it, glass-bowl pendants | <a href="../renders/sub/latest/labrisa_lounge_A.png"><img src="../renders/sub/latest/labrisa_lounge_A.png" width="220"></a> | <a href="../renders/sub/latest/labrisa_lounge_B.png"><img src="../renders/sub/latest/labrisa_lounge_B.png" width="220"></a> | <a href="../renders/sub/latest/labrisa_lounge_C.png"><img src="../renders/sub/latest/labrisa_lounge_C.png" width="220"></a> |
| §4.4 | [eco_retreat_modern_oasis](../lqv/amenities/eco_retreat_modern_oasis.py) · 746<br>Modern oasis retreat (replaces earlier curved-bamboo design) | <a href="../renders/sub/latest/eco_retreat_modern_oasis_A.png"><img src="../renders/sub/latest/eco_retreat_modern_oasis_A.png" width="220"></a> | <a href="../renders/sub/latest/eco_retreat_modern_oasis_B.png"><img src="../renders/sub/latest/eco_retreat_modern_oasis_B.png" width="220"></a> | <a href="../renders/sub/latest/eco_retreat_modern_oasis_C.png"><img src="../renders/sub/latest/eco_retreat_modern_oasis_C.png" width="220"></a> |

## Phase 2b critical fixes applied (carry-over from prior turn)

- `eco_retreat_modern_oasis`: curtain-wall door-gap surgical edit shipped.
- `subscene/base.py`: universal ground + flora upgrade (Phase 2a) backs every render here.
- No-ops verified for the glass-plane sweep and the material-fallback chain sweep.

## Open issues — per-asset critique

Honest-roast critique by `critic` subagent against all three lighting variants per asset. Reads in the same order as the gallery above.

### Typologies

- §3.1 hobbit_house — dome reads as green sod patch on bare orange disc, flat orange door + porthole window plates with no frame depth; HDRI is Utah red-rock canyon (A) / pine fog (B) / steppe (C), all non-Paraguayan and uncorrelated with site; floating petal/stick sprites mid-air from broken scatter, no laterite foundation, sparse fern is only flora
- §3.2 italian_stone_small_v1 — name says "stone" but walls are vertical wood planks, zero stone visible; flat orange shutters and porch columns read as untextured placeholder; walls touch laterite directly (Rule 4 violation: no 60cm stone plinth); ground is bare furrowed laterite to horizon, no flora at all
- §3.3 italian_stone_small_v2 — identical striped wood-plank walls to v1 with identical flat-orange shutters, typologies are not visually differentiated; skillion roof overhang readable but stone pavers at base are a thin patch, walls still touch ground (Rule 4); same furrowed-laterite void around it
- §3.4 italian_river_house_4pax — vertical cream/grey wall stripes read as prison stripes not lapacho board-and-batten; BLACK CLIPPING VOIDS at wall/roof corner joints (geometry gap); "river" is a flat black mirror plane with no water shader and a coffee table sitting on the surface; no second-story access shown, flat-orange windows
- §3.5 container_river_house — stilts terminate in mid-air over dry furrowed laterite, no water under the "river house"; window is a huge blue gradient panel with no glass/frame material; container reads as flat orange-pink metal box with zero Paraguayan integration (no corredor, no veg, no transition to ground)
- §3.6 bamboo_river_house — quonset/half-cylinder shape with smooth cream plastic roof and NO BAMBOO texture anywhere despite the name; black-mirror pool under stilts has a hard orthogonal edge cutting into laterite; stilts read as orange plastic; no riparian flora, no Paraguayan reference
- §3.7 bamboo_container_4pax — flanking "trees" are broken popcorn/marshmallow blobs on visible stick legs (no trunk geometry, no canopy structure); bamboo perimeter frame is a pole cage, not a buildable wall; solar panels on flat roof clash with rural-Paraguay typology; black void in floor center
- §3.8 bamboo_wigwam_lodge — Rule 8 violation: wigwam/tepee cone is North American Plains Native, not Paraguayan vernacular (no corredor, no lapacho, no aleros); cream uniform skin with zero bamboo texture; door is flat orange rectangle; same popcorn-blob trees on stick legs flank it
- §3.9 bamboo_boomhut_treehouse — "treehouse" with NO TREE: structure stands on 4 thin bare vertical poles, no canopy, no trunk, no foliage; spiral staircase wraps a pole that isn't a tree; access bridge connects to nothing; ground is featureless laterite plane
- §3.10 bamboo_beton_30 — massive flat roof reads as thin floating sheet with no fascia depth (Rule 5 alero structure not articulated); pale bamboo columns read as plastic dowels not poles; translucent wall reveals interior whitebox; black corner clipping void at floor; no foundation plinth
- §3.11 bamboo_beton_28 — same flat-pink hovering roof, same plastic-dowel column rhythm as bamboo_beton_30, typology not differentiated; ladder-shaped flat-orange shutter glued onto white interior wall reads as floating decal; pindo-palm-like sprites on roof in A are bare sticks, no plumose fronds; black void under deck
- §3.12 bamboo_beton_family_curved — curve is read as a fan of straight roof slats fanning out (not a smooth curved roof), looks like a half-built pergola not a finished house; white wall panels are unjoined plates with visible gaps between them, no enclosure; stripe at column base reads as Z-fighting; black void in floor center; no walls means no occupiable house
- §3.13 bamboo_beton_family_rectangular — same dowel-sticks-on-roof artifact as 3.11, mass reads as orange shoebox with white horizontal stripe; clerestory is a bright orange band with no visible glazing; no doors visible on any elevation; interior shows whitebox through the openings; no foundation/plinth, walls touch laterite (Rule 4)

### Amenities

- §4.1 eco_pool — pool water is opaque black slab across A/B/C (`pool_water` shader absorbing, not dielectric+specular; 0.06 m thick cube reads as sunken tar pit not surface — `lqv/amenities/eco_pool.py:265-282`); deck is flat orange-salmon plane with no plank seams or grain (`lapacho_timber` rendering as plastic-laminate placeholder); coping slabs coplanar with deck (`_coping`, 285-343) so jacuzzi NE inset illegible; boulder bench reads as three pebbles on a parking lot (mat_moss fallback at line 597 hits sandstone silently); the two bamboo clumps + two lapacho saplings promised in `_surround_flora` are entirely absent; the dominant acacia/mesquite tree right-of-frame is HDRI bleed, not project flora; no pergola, no thatch, no outdoor shower arm visible; Rule 4 plinth nonexistent (deck floats on bare neutral ground); Rule 8 vernacular zero (reads as Lesotho/Atlas plunge pool not Paraguayan cerrado); shower mast pole clips through `EcoPool_Pergola_Thatch` panel in A/C (no Z-fix); scale legibility broken with `DECK_POST_HEIGHT_M=0.30` providing no human-scale anchor
- §4.2 floating_dining — flora is broken: trees are pale low-poly popcorn-blob foliage on thin pale sticks with no trunk taper (catastrophic in A/C where they dominate frame); "floating" plane is a flat black mirror with hard rectangular edge sitting on dry laterite (not water); two-tier deck has no railings (safety read); string-light bulbs are unshaded white spheres
- §4.3 labrisa_lounge — two split deck plates float at different heights with visible gap and no connecting structure (reads as broken not designed); sauna/hot-tub object on right is a tiny gray cylinder cluster with no scale or material legibility; boulder cluster on left is generic asset pasted onto bare laterite; canopy is a flat cream plate with no fascia thickness, columns are pale dowels; string-light bulbs are unshaded spheres
- §4.4 eco_retreat_modern_oasis — rendered with `RENDER_FLORA_PHOTOREAL=0` (photoreal-flora loader name-collision bug producing orphan `jacaranda_tree_leaves_*_LOD0.003` and `fern_02_*.001` objects "not in collection 'Scene Collection'"; see `renders/sub/runs/review_2026-06-14_logs/eco_retreat_modern_oasis_A.log`). Dome (`_build_geodesic_dome`, line 186) reads acceptably — only win; lapacho saplings are the orange-procedural placeholder (cones-and-spheres flowers on dowel trunks) at 1.5× dome scale, destroys modernist composition; reflection pool is again pure black across A and C (only B shows reflection via overcast diffuse fill — `_build_reflection_pool`, 274-290); sandstone coping (297-315) floats as white concrete curb ~24 cm below deck plane (z-coplanarity bug between `cz + DECK_ELEVATION_M + DECK_THICKNESS_M/2` and `cz + POOL_DEPTH_M + POOL_COPING_T_M/2`), pool reads as sunken trench not flush mirror; U-deck `S` plank at line 356 closes all 4 sides — "U opens south" comment lies, topology is a closed rectangle around a hole; curtain-wall door-gap aperture (`CURTAIN_WALL_DOOR_CENTER_I=15±2`, line 62) reads correctly post-fix BUT culms are pale-green vertical sticks with no node banding, no Guadua taper, lintel beam (438) invisibly thin; yoga shelter (`_build_yoga_shelter`, 474) is flat beige panel on 4 toothpick legs, `YOGA_ROOF_TILT_DEG=8` below visual threshold (reads as perfect slab); 2 boulders + bench (537) reads as 3 dumped rocks because `BENCH_W_M=0.4 × BENCH_L_M=1.8` is dwarfed by `BOULDER_RADIUS_M=0.7` spheres; same neutral white-grey ground plane as eco_pool, no Rule 4 plinth, no Paraguari terrain transition; dome `pv_glass` (199) too transparent for contact shadow on B, sharp black AO ring on A/C; SW Guadua clump (670-698, 7 culms in 0.20 m spiral) invisible every frame — too tight a stack to read, or occluded by toy-lapacho

### Meta-patterns (cross-asset)

1. Every HDRI is non-Paraguayan (Utah red-rock A, pine-fog forest B, dry steppe C) — replace with cerrado / Atlantic-Forest-edge dome to match Escobar Paraguarí.
2. Flat-orange untextured material recurs on doors, shutters, columns, decks across almost every typology — placeholder leaking into production renders.
3. The background-tree asset is broken (popcorn-blob foliage on stick legs, no trunks) and appears in `bamboo_container_4pax`, `bamboo_wigwam_lodge`, `floating_dining`, `labrisa_lounge`.
4. Ground is uniformly bare furrowed laterite with no Paraguayan flora (no pasto, no lapacho, no pindo, no mango) outside the structure footprint.
5. Every "river/water" feature renders as a flat black mirror plane with hard orthogonal edges and no water shader (`italian_river_house_4pax`, `bamboo_river_house`, `floating_dining`, `labrisa_lounge`, partial `container_river_house`).
6. Every `bamboo_*` typology shows no bamboo texture on walls or roof — asset name does not match shipped material.
7. Rule 4 violation (60cm stone foundation) is endemic — walls/decks touch laterite directly across nearly all dwellings.
8. Variant A/B/C differ only in HDRI swap — no lapacho-bare-pink in A, no firefly/blue-hour treatment in C; the seasonal/temporal story is not being told. Tracks back to deferred T1.6 (per-variant lighting differentiation).
9. Every water surface (pool, jacuzzi, reflection pond, river, creek) renders as an opaque pure-black slab across A and C, with only B showing any reflection (overcast diffuse fill is masking the broken shader). The `pool_water` / river shader chain is absorbing instead of dielectric+specular — global fix lands one material registration, gates ~12 assets. Highest-leverage single bug in the doc.
10. The `lapacho_timber` material is rendering as flat orange-salmon plastic-laminate across every deck, plank, and coping surface — no grain, no plank seams, no UV scale. Combined with the orange-placeholder doors/shutters/columns from meta-pattern 2, the entire palette skews to a 1990s polypropylene "garden furniture" read. Material registry rewire needed.
11. Photoreal-flora loader has a name-collision bug producing orphan `*_LOD0.003` and `*.001` objects "not in collection 'Scene Collection'" — currently isolated to `eco_retreat_modern_oasis` (and possibly other dense-jacaranda assets); workaround is `RENDER_FLORA_PHOTOREAL=0` which falls back to procedural cones-and-spheres flora that itself reads as Fisher-Price toys. Upstream fix deferred until renderer byte-identity sprint ends (frozen at `85e86aa`).

> Meta-patterns 9, 10, 11 are tracked for the post-escritura sprint at [`docs/DEFERRED_BUGS.md`](DEFERRED_BUGS.md) with reproducer + fix sketch + acceptance criteria for each.

## How to reproduce / re-run

```bash
# Full 51-job batch (cap-4, ~30 min wall):
bash scripts/render_review_2026_06_14.sh

# Single asset re-render at higher quality:
RENDER_RUN_ID=review_2026-06-14 RENDER_VARIANT=C \
RENDER_FLORA_PHOTOREAL=1 RENDER_RES=hd RENDER_SAMPLES=256 \
PYTHONPATH=. blender -b -P lqv/subscene/<asset>.py
```

Outputs:
- Per-run: `renders/sub/runs/review_2026-06-14_<asset>/<variant>.png`
- Mirror: `renders/sub/latest/<asset>_<variant>.png`
- Legacy flat: `renders/sub/<asset>_<variant>.png`
