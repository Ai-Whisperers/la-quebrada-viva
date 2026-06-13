# MODELS_ROAST.md — Honest critique of every model in La Quebrada Viva

**Author:** critic agent · **Date:** 2026-06-12 · **Scope:** 13 typologies + 4 amenities + 7 Poly Haven CC0 assets · **Render source:** `renders/sub/latest/<asset>_A.png` (Variant A golden hour, 1280x720 sub-render).

This document is not gentle. The renders, builders and asset library were all reviewed against `docs/MASTER_BRIEF.md` §14 (the 10 rules), `docs/EUROPEAN_TOURISM_SPEC.md` (vacation-rental aesthetic bar), and Wesley's reference images in `wes example ideas images /`. If a finding is wrong, file a counter — but cite the line number.

---

## 0. Executive summary — the 10 things that make these renders unshippable to Wesley

1. **Wrong HDRI everywhere.** Every render uses what appears to be a South-African / Lesotho red-rock sandstone escarpment with grass-free fynbos foreground. We are building for the Paraguayan Atlantic Forest fringe in Escobar, Paraguarí — humid sub-tropical, dense green, NOT high-desert. Every single hero shot is broken at the background layer alone. P0.
2. **Every house sits on a flat plywood deck.** The default `base.place_neutral_ground()` (`lqv/subscene/base.py:82-90`) drops a 20 m laterite plane under each asset, then the camera catches its edge and you can see the HDRI plate **underneath** the plane (visible bottom-right in `bamboo_river_house_A.png`, `bamboo_container_4pax_A.png`, `bamboo_beton_family_curved_A.png` and 4 others — the floating-island effect kills realism instantly).
3. **Materials are flat shaded blobs.** No PBR detail. Bamboo poles read as plastic dowels. Stone walls (`italian_river_house_4pax_A.png`) read as cardboard cylinders glued together vertically — there is no stone texture, no mortar, no roughness variation. Lapacho reads as a salmon plastic.
4. **Wigwam thatch is a smooth featureless minty-green cone** (`bamboo_wigwam_lodge_A.png`). This is the worst-looking render in the deck. Thatch should be dark golden-brown stranded fiber. Cause: `bamboo_wigwam_lodge.py:166` → `_mat('sod_canopy') or _mat('moss')`. Wrong material category entirely.
5. **Boomhut treehouse has visible debris** (`bamboo_boomhut_treehouse_A.png`, right side): a floating staircase of disconnected cubes hovering 3 m off the deck with no platform connection. Cause: `bamboo_boomhut_treehouse.py:204-233` — `_spiral_stair()` places the stair `+1.2 m` diagonally off the platform corner with zero connector deck.
6. **Bamboo river house stair literally walks away from the house** (`bamboo_river_house_A.png`, left side): the stair starts at the platform edge and recedes south while rising. Top tread does not touch the house deck. Cause: `bamboo_river_house.py:245-261`.
7. **Italian stone v1 + v2 are not stone.** The walls show vertical stripes that read as bamboo siding or corrugated metal, not coursed quartzite. Walls have ZERO displacement. The "Italian" identity is invisible. Material misnomer: roof uses `_mat('laterite')` instead of terracotta tile (3 builders affected: `italian_river_house_4pax.py:186`, `italian_stone_small_v1.py:172`, `italian_stone_small_v2.py:190+199`).
8. **Hobbit house is a flat disk topped with a green dome on flat ground** (`hobbit_house_A.png`). It looks like a UFO landed. There is no berm cut into terrain, no buried half-burial, no path. Cause: `hobbit_house.py:91-103` — `_berm()` is a cylinder primitive placed ON the plane, not cut INTO it. SNAP='cut' is declared in the constants but ignored at build time.
9. **Eco pool's regen plants are plastic traffic cones** (`eco_pool_A.png`) and the coping boulders are a uniformly-spaced bead necklace. Cause: `eco_pool.py:197-223` (cones r=0.12) + `eco_pool.py:155-194` (icosphere subdivisions=2 in a deterministic loop).
10. **Lantern bowls across 3 amenities are rendered with `pv_glass` material** — i.e. solar-cell glass. Lanterns should be warm-glow emissive paper/glass bowls. Cause: `_grammar.py:128` — single line, fix once, fixes labrisa + floating_dining + eco_retreat lanterns simultaneously.

These are not nits. Together they make the deck unusable as a sales-grade visual for European vacation-rental customers, which is the stated audience in `docs/EUROPEAN_TOURISM_SPEC.md`.

---

## 1. Section A — Per-render roast (Variant A, 17 hero PNGs)

### 1.1 bamboo_wigwam_lodge_A.png

- **Silhouette:** clean cone. That's the only good news.
- **Material disaster:** thatch is a smooth featureless mint-green cone with diagonal seam lines from `mesh.from_pydata` triangulation. Reads as a billiard-table-cloth-covered ice-cream cone. Should be: golden-brown layered palm or grass thatch with shaggy edges, visible bundling.
- **Door framing is wrong:** the two visible 1.9 m tall vertical lapacho posts and the header above them are floating outside the cone in front of the thatch (`bamboo_wigwam_lodge.py:191-212`). The door header sits at z=1.85 m but is ON TOP of the thatch skin — the thatch is not cut at the entrance. From this camera angle you can see the door frame *plus* an uncut thatch face behind it. Symbolically: there is no opening into the wigwam.
- **Foundation Rule 4 violation:** the floor is a `laterite` cylinder 12 cm thick (`:87-99`) — but it sits AT z=0, no raised stone foundation, no ≥60 cm plinth. Earthen wall (the conical thatch) touches the ground plane directly. Direct rules violation.
- **Scale cue absent:** no human-scale reference object (no door swing, no chair, no path) — and the door header at 1.85 m is the only proxy. The whole thing reads as 1.5 m tall, not 5 m.
- **Background:** Lesotho. Wrong continent. There is also a clear seam at the bottom of the laterite ground plane where you see the HDRI underneath.

### 1.2 bamboo_container_4pax_A.png

- **The container is invisible.** What I see is 6 white vertical strips on the left + a couple of pergola posts on the right + a flat white roof slab. The bamboo cladding on the long side (`bamboo_container_4pax.py:124-144`, 76 culms per side) plus the cool-roof slab (`:111-121`) completely obscures the steel container shell. Wesley will ask "where is the container?".
- **Cool roof is `lime_wash` material** (`:118`) — bone white, ultra-flat. A real cool-roof acrylic coating is off-white with visible texture and is not as pure-white as quicklime plaster.
- **Pergola posts are bamboo cylinders with `vertices=8` r=0.06** (`:174-179`) and look like plastic dowels. No node detail, no leaf scars, no tonal variation — clearly not Guadua.
- **No doors. No windows. No interior visible.** A 12.2 m × 2.6 m container with zero openings reads as a freight box.
- **Deck floats:** the deck cube edge is visible against the laterite plane — and behind/under the deck you can clearly see the HDRI background through the edge of the ground plate (bottom-right corner of frame).
- **Container shell is one extruded cube** (`:98-108`) — no corrugation profile, no door panels at the end, no logo or any of the visual debt of a real shipping container.

### 1.3 bamboo_boomhut_treehouse_A.png

- **The debris of floating stair cubes off to the right** is the most damning visual in the whole render set. 5+ disconnected lapacho cubes hover at heights 0.5, 1.2, 2.0 etc with no rotational anchor. They look like a Minecraft glitch. Source: `bamboo_boomhut_treehouse.py:204-233` — `_spiral_stair()` centers the spiral on `(ox + PLATFORM_W/2 + 1.2, oy + PLATFORM_L/2 + 1.2)`, i.e. **1.2 m diagonally off the platform corner**, with no top-tread connector to the deck.
- **The "treehouse" has no tree.** It is a box on 4 stilts. No trunk visible, no canopy, no foliage shadow on the box. It cannot be called a treehouse with a straight face.
- **Pyramidal roof is a flat shaded olive-green hipped pyramid.** No tile, no thatch, no eave detail.
- **Stilts are 4 r=0.10 cylinders** with no bracing, no diagonals, no railings. Structurally implausible (4-pole vertical post, no lateral stability).
- **Floor box face is featureless cream cob.** Door is a black rectangle (Boolean cutout?) at the lower-right corner of the front face — looks like a smudge.

### 1.4 bamboo_river_house_A.png

- **Stair walks away from the house.** Treads recede south while rising; top tread does NOT meet the deck. Source: `bamboo_river_house.py:245-261`.
- Otherwise: same problems as boomhut — flat olive hipped roof, no detail, no railings, no eave shadow. The bamboo stilts are 4 cylinders.
- **Where is the river?** This is the `bamboo_river_house`. There is no water visible in the render. Builder doesn't include water (acceptable for sub-render) but the asset's identity is invisible.
- **Black rectangles at the wall base** — Boolean window cutouts that didn't get a glass infill. Reads as missing teeth.

### 1.5 hobbit_house_A.png

- **It's a UFO on a dinner plate.** Flat disk plinth (radius 3.8 m) sitting on flat ground with a half-sphere green dome on top. No berm, no terrain integration, no path, no door visible, no chimney, no window. Rule 1 (no boxes/primitives) and Rule 8 (culturally Paraguayan) both violated — this reads as a sci-fi prop.
- **Source bug:** `hobbit_house.py:91-103` — `_berm()` is `bpy.ops.mesh.primitive_cylinder_add` at `location=(ox, oy, depth/2)` with SNAP='cut' declared in constants but never honored. It's a disk on the plane, not a berm cut into terrain.
- **Material:** dome is `sod_canopy` (mint green), plinth is `lapacho_timber` (pink salmon). Both flat shaded. No grass, no moss, no soil-on-roof effect — which is the whole point of a hobbit house.
- **No door.** Literally not modelled in the visible silhouette.

### 1.6 italian_river_house_4pax_A.png

- **Walls read as bamboo siding or corrugated metal, not stone.** Vertical fine striping from displacement-less sandstone material on flat cube walls. Real coursed sandstone shows horizontal bedding and irregular joint lines.
- **Roof is bright orange `laterite` material** (`italian_river_house_4pax.py:186`) — should be `terracotta_tile` (which exists? — check `MAT` registry). Either the material doesn't exist or the wrong key was wired. The roof reads as raw clay, not glazed tile.
- **Stringcourse wraps over the openings** — visible as horizontal pink band crossing the windows (`:142-156` is one cube wrapping the entire envelope). Bad masonry detail.
- **No chimney, no shutters, no balcony, no Italian-villa cues.** The "Italian" identity rests entirely on a hipped roof shape, which the render botches because of the wrong roof material.
- **Foundation: indeterminate.** Can't see plinth at this camera angle. Black band at base of walls is shadow / Boolean offset, not a stone plinth.

### 1.7 italian_stone_small_v1_A.png

- **Same striping problem** as v1 above — walls read as vertical bamboo not stone.
- **Chimney is a thin cube** with no cap, no flashing.
- **Roof has a hip line that contradicts ROOF_TYPE constant.** Constant declares `'terracotta_tile_gabled'` (`italian_stone_small_v1.py:?` — see code) but the geometry generates a hipped roof with triangular hip faces visible in the silhouette. Constant lies about geometry.
- **Roof material:** same `laterite` (raw earthy red) instead of fired terracotta.
- **Plinth:** invisible at this angle.

### 1.8 italian_stone_small_v2_A.png

- **The pergola extension on the right** is the v2-specific feature — visible as 4 anorexic columns (18 cm × 18 cm — `_PERGOLA_COL_W = 0.18` `italian_stone_small_v2.py:?`). Real stone columns are 30-40 cm minimum. They look like wooden 4x4s, not stone.
- **Pergola has zero infill** — no shade cloth, no vines, no slats above. It is 4 vertical bars + 2 horizontal beams + 5 cross beams, all flat-shaded. Reads as scaffolding.
- **Same wall + roof problems as v1.**

### 1.9 eco_pool_A.png

- **Bead-necklace coping.** Boulders are perfectly evenly spaced icospheres-subdivisions=2 scaled flat at (1.0, 1.0, 0.55) — `eco_pool.py:155-194`. There is no `random.uniform` in that loop; it is fully deterministic. The result is a perfect rectangle of identical pebbles, which screams CGI.
- **Plastic traffic cones.** The 6 "regen plants" inside the pool (visible as upright cones on the right edge) are `primitive_cone_add` with r1=0.12 (`:197-223`). They look like cones from a road-works site, not Cyperus, Pontederia or any biofilter aquatic plant.
- **Water surface is matte black** — `_mat('pool_water')` does not have a reflective shader wired up, or `pv_glass` fallback (`:152`) is silently kicking in and rendering at this camera angle as a void.
- **No edge planting, no riparian flora, no overflow weir visible.** The brief specifies `EDGE_PROFILE='free_form_boulder_coping'` — the geometry says rectangle.
- **No human-scale reference.** Pool reads as the size of a hot tub or as the size of a swimming pool — impossible to tell.

### 1.10 eco_retreat_modern_oasis_A.png

- **The arched roof is the only thing that works visually** in the whole deck. Compelling silhouette.
- **But:** the arc verts formula `eco_retreat_modern_oasis.py:226` silently makes the peak 30% taller than the declared `_PEAK_RISE_ABOVE_EAVE = 1.6 m` constant. Geometry contradicts the takeoff.
- **Slab uses `_mat('laterite')`** (`:159`) but the `MATERIAL_TAKEOFF` declares `'concrete_slab_108'`. So the BOQ says concrete, the render says laterite. Choose one.
- **Sauna pod is a featureless lapacho cube** (`:319-344`) on the deck — no door, no window, no chimney. Reads as a packing crate.
- **East glass wall is a 4 cm cube** (`:289-300`) — no mullions, no frame, no transom. Looks like a glass sheet glued to the deck.
- **No interior visible.** A retreat with no visible bed/seating is just an awning over concrete.

### 1.11 floating_dining_A.png

- **Pontoons read as polished steel or solar glass.** Cause: `floating_dining.py:117` — `_mat('pv_glass') or _mat('steel_anodized')`. Real EPS foam billets are matte white-grey with rough texture. This is the wrong material category entirely.
- **Water surface uses `pv_glass`** as fallback (`:104`) — produces an unrealistic glassy mirror void, not water.
- **Mooring rope rendered as `lapacho_timber`** (`:274`) — pink-salmon plastic ropes are visibly wrong.
- **No food on table, no chairs (only benches), no diners** — sells a static prop, not a dining experience.
- **Bamboo overhead frame** is 4 r=0.06 cylinders + 4 r=0.06 crossbeams, vertices=10. Same plastic-dowel problem.
- **6 lanterns in a 2×3 grid** are visible as discoid blobs hanging from the frame. The bowl material is `pv_glass` (`_grammar.py:128`) — they look like dark solar disks, not warm-glow paper lanterns. Anti-purpose: lanterns should glow, these don't even reflect interestingly.

### 1.12 labrisa_lounge_A.png

- **Roof declared as `'palm_thatch_low_pitch'`, rendered as green sod canopy.** Cause: `labrisa_lounge.py:206` — `_mat('sod_canopy') or _mat('canopy')`. The render shows a uniform mint-green hipped slab. Same disease as the wigwam.
- **Creek surface is a 4 cm cube using `pv_glass`** (`:218`). Visible as a black rectangle splitting the deck — looks like a hole, not water.
- **The "boulder seating arcs" and "stepping stones"** from `_grammar` are barely visible in this rendering — they read as tiny grey lumps in the void where the creek surface is missing.
- **Lantern grid (3×3, 9 lanterns)** dangling above the deck — same pv_glass bowl problem. From this camera distance they read as a row of small dark dots, not warm hospitality lighting.
- **Bamboo columns** are 4 r=0.075 cylinders vertices=12. Better than the r=0.06 vertices=8 used in container/floating_dining but still plastic-looking.
- **No deck planks visible** — the lapacho deck reads as a uniform pink panel with no joint lines.

### 1.13 bamboo_beton_28_A.png

- **Reads as a concrete bench under a tilted carport.** The "house" is barely there. The white béton-armé slab is the dominant visual element; the bamboo pergola posts are visible but no walls, no doors, no human-occupiable space readable.
- **Tiny scale.** Without a person or chair reference, this reads as a 1:10 architectural model, not a 28 m² dwelling.
- **Single tilted plane roof** with no thatch, no tile, no overhang detail. Reads as a temporary shade structure.
- **No back wall visible** — viewer can see straight through the structure. Either there is no back wall or it's flush with the front and orthogonally occluded.
- **The black band at the slab base** is the same Boolean-offset shadow as everywhere else.

### 1.14 bamboo_beton_30_A.png

- **Identical aesthetic disaster to bamboo_beton_28** but with a flat horizontal pergola/roof instead of tilted. Reads as a concrete picnic table under a roof of broomsticks.
- **Roof is a slab with 10+ thin bamboo cross-purlins exposed below** — but no thatch infill above. So the roof doesn't actually keep rain off anything. Whether that's intentional from a "shaded outdoor pavilion" reading or a builder bug, the render does not communicate it.
- **No walls, no doors, no glazing, no windows.** A pavilion masquerading as a dwelling.
- **Roof material lookup at builder line 76** double-counts the overhang in the area-takeoff (BOQ bug, not a render bug, but worth flagging since you're shipping the BOQ to Wesley).

### 1.15 bamboo_beton_family_curved_A.png

- **The curved barrel roof is the most appealing silhouette in the deck after eco_retreat.** Recognizable Latin-American kiosk vocabulary.
- **But:** the barrel is rendered as flat mint-green with diagonal triangulation seams visible. Should be terracotta tile or palm thatch with shadow gradients.
- **The "house" underneath is a flat white béton-armé tray with 12 vertices=10 cylinder columns** (`bamboo_beton_family_curved.py:186`). The columns are uniformly distributed and look like ten-pin bowling pins. No wall infill visible — through the columns you see straight through to the HDRI sky.
- **No doors, no windows, no glazing, no curtains** — this is an open pavilion not a house.
- **The roof barrel sits on top of the columns at the eave** with a visible 5 cm gap — daylight visible through the connection. Reads as a bug.

### 1.16 bamboo_beton_family_rectangular_A.png

- **Gabled roof with 8 vertical bamboo purlins on top of the slope plane** — visible as eight short white horizontal bars on the roof surface. Should be inside the roof structure, not on the outside as topographic ridges.
- **Gable triangle is a flat solid mint-green triangle** with no infill, no louvre, no glazing — reads as cheese-slice geometry.
- **No walls underneath.** Same open-pavilion problem as curved. A "family rectangular" house without walls is not a house.
- **Terracotta roof comes from `sod_canopy` material** — the brief calls for terracotta, the builder loads sod. Material wired wrong (`bamboo_beton_family_rectangular.py:?`).

### 1.17 container_river_house_A.png

- **Two purple-grey containers stacked with a 3 m cantilever.** Visually the cleanest of the deck — recognizable container architecture vocabulary.
- **But:** containers are featureless solid cubes (`container_river_house.py:129-141` — single `primitive_cube_add` scale-applied). NO corrugation profile, NO container doors at the ends, NO logo decals. Reads as a cardboard box stack.
- **Stair walks away from the lower container** — same bug pattern as bamboo_river_house. Two faint stair treads visible bottom-left don't connect to anything.
- **The 4 steel piers** under the lower container (`:105-127`) are thin r=0.04 cylinders that look like rebar, not real steel pile foundations.
- **End glass wall is a 4 cm thin cube** (`:158-170`) — no mullion, no frame.
- **The upper container's 3 m cantilever** is visible and looks structurally implausible without a visible spine beam.
- **Background HDRI underneath the ground plate is visible bottom right** — same floating-island problem as everywhere else.

---

## 2. Section B — Per-builder roast (13 typology builders + 4 amenity builders + subscene drivers)

### 2.1 `lqv/typologies/bamboo_beton_28.py`

- **`primitive_cube_add` walls** at lines 143, 167 — Rule 1 (no boxes for living spaces) treated as suggestion. Acceptable for béton slab; not acceptable if any wall is supposed to be cob.
- **vertices=10 cylinder** at line 198 — bamboo culms with 10-sided cross-section read as plastic. Should be 16+ vertices or use a Guadua bamboo asset.
- `_OVERHANG = 0.95` (line 41) — satisfies Rule 5 minimum. OK.
- **MATERIAL_TAKEOFF**: does not list any flooring material — house has no floor? Probably a takeoff omission rather than an actual missing floor object.
- **No raised stone foundation ≥60 cm.** Rule 4 violation: béton slab sits directly on ground.

### 2.2 `lqv/typologies/bamboo_beton_30.py`

- **4 bamboo cylinders `vertices=10`** at line 172 — same plastic-dowel disease.
- **Roof as 4-vertex quad extruded** (lines 186-208) — flat rectangular plane, no slope reasoning, no eaves modeled separately.
- **Door is 3 cubes** (lines 268-290) — frame + leaf + threshold all axis-aligned cubes. Reads like a Lego door.
- **Roof-area takeoff at line 76 double-counts overhangs** — BOQ over-estimates roof material by ~30%. Fix the formula or the BOQ.

### 2.3 `lqv/typologies/bamboo_beton_family_curved.py`

- **Slab+walls `primitive_cube_add` (lines 132-166)** — flat box stack. Rule 1 violation if walls are cob; acceptable if béton+brick.
- **12-column array (line 186) `vertices=10`** — bowling-pin colonnade. Should vary radius slightly or use real Guadua asset.
- **Parabolic arc roof as `vertices=8` cylinder segments at lines 209-239** — the cylinder-segment trick produces an octagonal pseudo-arc, not a smooth barrel. Visible as flat facets in the render.
- **Thatch skin single quad mesh (lines 242-268)** — one rectangular face stretched over the arc. No thatch texture, no fiber direction, no shaggy edge.
- `_OVERHANG = 1.10` — OK on Rule 5.

### 2.4 `lqv/typologies/bamboo_beton_family_rectangular.py`

- **vertices=10 columns at line 184** — see above.
- **Roof slope 8-vertex slab (lines 265-303)** — same flat-plane problem.
- **Gable triangle (lines 306-325)** — flat triangle, no gable window, no vent louvre, no infill.
- `_OVERHANG=1.00` — OK on Rule 5.
- **Terracotta roof comes from `sod_canopy` material** — wrong color (green not terracotta orange). MATERIAL_TAKEOFF says terracotta; render shows sod. Honesty mismatch.

### 2.5 `lqv/typologies/bamboo_boomhut_treehouse.py`

- **FLOATING STAIR BUG, lines 204-233:** `_spiral_stair()` places stair at `center_x = ox + PLATFORM_W/2 + 1.2; center_y = oy + PLATFORM_L/2 + 1.2` — 1.2 m diagonally off the platform corner with NO connector deck. This is the visible debris in the render.
- **No tree.** A treehouse without a tree is a stilt house. Builder should either include a procedural mango/lapacho trunk or be renamed.
- **No bracing on the 4 stilts** — structurally implausible.
- **Pyramidal roof** — flat shaded olive primitive, no detail.

### 2.6 `lqv/typologies/bamboo_container_4pax.py`

- **Container shell lines 98-108:** single `primitive_cube_add` scaled to (W,L,H), NO corrugation, NO doors, NO labels.
- **`_bamboo_cladding()` lines 124-144 at `side_sign ±1` in X:** covers the long sides of the container; from a 3/4 view, slats hide the container shell entirely. The container becomes invisible — defeating the typology's identity.
- **Cool roof line 116 uses `_mat('lime_wash')`** (line 118) — semantically wrong (it's a cool-roof acrylic coating, not lime plaster). Visually: too pure-white.
- **Pergola posts**: 6 cylinders `vertices=8` r=0.06 lines 173-184 — plastic dowels.
- **No windows, no doors, no end-of-container detail.**

### 2.7 `lqv/typologies/bamboo_river_house.py`

- **STAIR BUG, lines 245-261:** `_stair()` walks AWAY from platform — each step further south as i rises AND z rises. No top connection.
- **No river.** Builder excludes water (defensible for sub-render) but doesn't even include a stone river-edge or footbridge stub. Identity unclear.
- **No railings on the deck or stair** — Rule 6 (passive design) does not include safety, but vacation rentals will fail municipal inspection without rails.

### 2.8 `lqv/typologies/bamboo_wigwam_lodge.py`

- **`_thatch()` lines 164-188 is a single 24-segment cone mesh outside the pole frame with `sod_canopy or moss` material (line 166)** — produces smooth featureless green cone. Should be palm thatch (golden-brown) with `random.uniform`-perturbed segments and shaggy bottom edge.
- **Door header at lines 205-212 overlaps the thatch cone.** `_poles()` line 138 skips one pole at `i == _POLE_COUNT // 2` to make a gap, but the thatch cone (built separately) does NOT have a matching door cutout. Result: thatch passes through the door header from the camera angle.
- **Apex offset 0.05 m** (`_APEX_OFFSET`, line 32) — small enough to read as a point. OK.
- **Floor uses `laterite` material** — earthen floor consistent. OK.
- **Ring beam is a torus** (lines 102-115) — sensible primitive choice for once.
- **Rule 4 violation:** floor is at z=0 with no raised stone plinth.

### 2.9 `lqv/typologies/container_river_house.py`

- **Container lines 129-141 = primitive_cube scale (W,L,H);** NO corrugation. Same disease as 4pax.
- **Glass endwall lines 158-170 is 0.04 m-thin cube** — no mullions, no frame, no transom.
- **4 steel piers per container lines 105-127** — too thin (r=0.04?), reads as rebar.
- **Upper container cantilevers 3 m** — implausible without a visible structural spine. Either add a spine or reduce the cantilever.
- **External stair lines 173-189 walks AWAY from container** — same disease.

### 2.10 `lqv/typologies/hobbit_house.py`

- **THE UFO BUG: `_berm()` lines 91-103** places a cylinder of radius 3.8 m as a SHORT DISK on top of ground plane (`depth=WALL_HEIGHT_M * 0.85, location=(ox, oy, depth/2)`) — does NOT cut into terrain, just sits on the plane. **`SNAP='cut'` declared but ignored.**
- **Dome is UV sphere scaled lines 121-136** — sensible primitive, but no soil/grass texture means it reads as plastic.
- **No door, no chimney, no path, no window-eyebrow** — the hobbit-house identity rests on these details and none are present.

### 2.11 `lqv/typologies/italian_river_house_4pax.py`

- **Walls lines 117-139 are 4 primitive_cube_add with sandstone** — no displacement, flat read. Vertical lines visible in render are from the bare albedo, not from real wall texture.
- **String course lines 142-156 wraps entire envelope as one cube including over openings.** Bad masonry — real stringcourses break at openings.
- **Material bug:** terracotta roof uses `_mat('laterite')` line 186. Wrong color category.
- **No shutters, balcony, chimney, or any other Italian-villa vocabulary** beyond the hipped roof outline.

### 2.12 `lqv/typologies/italian_stone_small_v1.py`

- **Material bug:** roof `_mat('laterite')` line 172. Same wrong color.
- **Roof at lines 147-175 is hipped** (faces include `(0,4,3)` and `(1,2,5)` hip triangles), but **ROOF_TYPE constant claims `'terracotta_tile_gabled'`** — constant lies about geometry. Honesty mismatch will confuse downstream BOQ + renders manifest.
- **Chimney lines 178-202** — thin cube with no cap. Should have a flashing collar and a clay pot.
- **Plinth lines 92-102 height 0.6 m** satisfies Rule 4. OK.

### 2.13 `lqv/typologies/italian_stone_small_v2.py`

- **Same laterite-for-terracotta bug at lines 190 AND 199 (leanto roof).** Two-bug compound.
- **Pergola lines 232-278:** `_PERGOLA_COL_W = 0.18` — 18 cm stone columns are anorexic (real ones 30-40 cm). 4 corner stone columns + 5 cross beams + 2 long beams.
- **Plinth 0.6 m** — OK on Rule 4.
- **No infill, climbing plant, or shade cloth on the pergola** — reads as scaffolding.

### 2.14 `lqv/amenities/eco_pool.py`

- **`_regen_plants()` lines 197-223 are `primitive_cone_add` r1=0.12** — reads as plastic traffic cones, not biofilter planting. Should use a real plant asset or instanced reeds.
- **`_coping()` lines 155-194 ico_spheres subdivisions=2 scaled flat `(1.0,1.0,0.55)`, deterministic loop** — uniform spacing reads as artificial bead necklace, contradicting `EDGE_PROFILE='free_form_boulder_coping'`. Inject `random.uniform` jitter on radius + position.
- **Water lines 130-152 thin cube; material `_mat('pool_water') or _mat('pv_glass')`** — `pv_glass` semantically wrong fallback. Should be a real water shader with normal map and refraction.

### 2.15 `lqv/amenities/eco_retreat_modern_oasis.py`

- **16 cylinder segments per arc × 11 arcs = 176 cylinders for roof structure** — perf concern. Should be a single curved mesh with a bevel.
- **Slab line 159 uses `_mat('laterite')` but MATERIAL_TAKEOFF declares `'concrete_slab_108'`** — material/BOQ contradiction.
- **East glass wall lines 289-300 single 4 cm cube** — no mullions, no frame.
- **Sauna pod lines 319-344 single primitive_cube_add with lapacho** — no door/window.
- **Arc verts formula line 226: peak silently 30 % taller than declared `_PEAK_RISE_ABOVE_EAVE = 1.6` constant.** Code lies about its own geometry.

### 2.16 `lqv/amenities/floating_dining.py`

- **Pontoon material line 117: `_mat('pv_glass') or _mat('steel_anodized')`** — closed-cell foam billets rendered as solar-cell glass or steel. Wrong material category.
- **Water surface line 102-112 uses `_mat('pool_water') or _mat('pv_glass')`** — wrong fallback. pv_glass produces a black mirror, not water.
- **Mooring rope material line 274 = `_mat('lapacho_timber')`** — pink-salmon solid wood ropes. Wrong material.
- **6 lanterns in 2×3 grid** via `_grammar.glass_bowl_lantern` — bowl uses `pv_glass` (`_grammar.py:128`).
- **No diners, food, dishes, or chairs (only benches)** — sells a static prop, not a dining experience.
- **Bamboo overhead frame**: 4 corner cylinders `vertices=10` r=0.06 + 4 crossbeams — plastic dowel disease.

### 2.17 `lqv/amenities/labrisa_lounge.py`

- **Creek surface line 218 uses `_mat('pv_glass') or _mat('glass')`** — black mirror, not water.
- **Roof is 6-vertex hipped mesh (lines 188-201) with `_mat('sod_canopy') or _mat('canopy')` (line 206)** — palm thatch declared in `ROOF_TYPE='palm_thatch_low_pitch'`, rendered as green sod.
- **3×3 lantern grid (lines 229-246)** — same pv_glass bowl problem.
- **4 bamboo corner columns `vertices=12` r=0.075** — marginally better than other amenities (12 sides not 8/10) but still plastic.
- **4 lapacho joists `(0.10, PLATFORM_L, 0.18)`** — flat slab, no joist hangers, no visible decking-board joints.

### 2.18 `lqv/amenities/_grammar.py`

- **`cascade_weir()` lines 33-71:** weir bar + 15°-tilted apron, both sandstone. OK conceptually but no water flow visible — reads as a stone ramp.
- **`stepping_stones()` lines 74-111:** `vertices=16` cylinders with alternating ±jitter (`offset_sign = 1.0 if i % 2 == 0 else -1.0` line 98) — better than nothing but still patterned. Use proper random.
- **`glass_bowl_lantern()` lines 114-156:** **bowl material `_mat('pv_glass') or _mat('glass')` line 128 — pv_glass on every lantern bowl across labrisa, floating_dining, eco_retreat.** Single-line fix, three-amenity payoff.
- **`boulder_seating()` lines 159-198:** ico_sphere subdivisions=2 with deterministic radius `r = boulder_radius_m * (0.85 + 0.30 * ((i * 37) % 7) / 7.0)` line 185 — pattern repeats every 7 boulders, but counts are 4-8 so usually fine. Scale `(1.0, 1.0, 0.65)` line 194 flattens to seat-height — sensible.

### 2.19 `lqv/subscene/base.py`

- **Does NOT set `cam.data.clip_end`** in default `run()` (lines 138-160) — relies on Blender default 100 m; explains the memory item `feedback_subscene_clip_end` (parcel-scale drivers silently clip background → render returns only HDRI). For any driver with `camera_distance` >100 m or where the asset has parcel-scale dependencies, this will break silently.
- **`place_neutral_ground()` lines 82-90: single 20 m laterite plane.** Camera at distance 6-12 m frequently captures the plane edge → "floating island on HDRI" artifact visible in 6+ of the 17 hero renders.
- **SHA-256-derived per-asset seed** (`derive_seed()` lines 52-55) — sensible, byte-stable. OK.
- **Save exposure A=-0.2 / B=+0.3 / C=+0.6** — matches composite. OK.

### 2.20 Individual `lqv/subscene/<asset>.py` drivers

- 17 thin drivers. Mostly identical 28-line template. Acceptable.
- None override `clip_end`. Should add `extras={'clip_end': 1000.0}` parameter to `base.run` and have parcel-scale drivers use it.
- Camera distance defaults (6-12 m) too close for parcel-scale assets like the eco_pool (12×6 m footprint) — at 6 m the pool overflows the frame. Tune per-asset.

---

## 3. Section C — Poly Haven CC0 asset inventory roast

7 assets present in `assets/models/`:

### 3.1 `anthurium_botany_01`

- **Species accuracy:** *Anthurium* is a tropical houseplant genus — multiple species. The brief species (in MASTER_BRIEF "Plant species" section + `paraguay_clay_house_research.md`) is **Anthurium plowmanii** (Paraguayan epiphyte, leaf strap-shaped, prominent midrib). Poly Haven asset is likely **A. andraeanum** or **A. crystallinum** (commercial cultivar). Verdict: **wrong species**, but visually defensible as filler. Acceptable as a placeholder; mark in CREDITS as a substitute.
- **Verdict:** USE as epiphyte filler. Not a Paraguayan native cultivar. Disclose substitution in CREDITS.md.

### 3.2 `boulder_01`

- **Generic CC0 boulder asset.** Material accuracy depends on retexturing. Out of the box it's typically grey granite — Paraguay site is laterite/sandstone (red-brown). Needs material retexture.
- **Verdict:** USE if material retextured to laterite/sandstone palette `#5A5448`-`#7A7268`. Otherwise looks geographically wrong.

### 3.3 `fern_02`

- **Species accuracy:** generic fern. Probably a temperate sword fern (*Polystichum*) or Boston fern (*Nephrolepis*). The brief wants **tree ferns (*Cyathea*)** — 2-4 m tall with arboreal trunk. Poly Haven `fern_02` is almost certainly **ground-level fern**, not tree fern. Verdict: **fills understory niche only**, NOT a tree fern substitute.
- **Verdict:** USE for understory. Need a separate tree-fern asset for the riparian zone.

### 3.4 `jacaranda_tree`

- **Critical substitution target.** The brief calls for **lapacho (*Handroanthus impetiginosus*)** — winter-deciduous, hot-pink trumpet flowers in winter (Variant A). Jacaranda has purple-blue flowers in spring, not pink in winter. Wrong species, wrong color, wrong season.
- **Verdict:** Use as canopy filler in summer Variant B / C only. For Variant A (lapacho bloom), retint flowers from purple to hot-pink `#E85A8C`-`#F0A0C8` via material override OR find a CC0 lapacho. Poly Haven has no native lapacho; disclose substitution.

### 3.5 `pachira_aquatica_01`

- **Species accuracy:** *Pachira aquatica* (money tree, Guiana chestnut) is native to Central/South America wetlands. Plausible for Paraguay stream-edge planting. OK.
- **Verdict:** USE riparian zone. No retexture needed.

### 3.6 `quiver_tree_01`

- ***Aloidendron dichotomum* (quiver tree)** is a Namibian endemic. Wrong continent entirely. Has zero business in a Paraguayan Atlantic Forest scene.
- **Verdict:** DELETE from asset library. Find another succulent if Agave americana isn't enough.

### 3.7 `rock_moss_set_02`

- **Generic mossy rocks.** Color likely temperate green moss — Paraguay sub-tropical moss is darker `#5F7A3D`-`#8AA055`. Probably acceptable out of the box.
- **Verdict:** USE for riparian/escarpment zone. Spot-check material against MASTER_BRIEF moss palette.

**Summary of asset roast:** 7 Poly Haven assets, 2 species-wrong (quiver_tree, jacaranda — wrong continent / wrong species), 1 wrong-scale (fern_02 isn't a tree fern), 1 wrong-cultivar (anthurium), 3 acceptable with retint (boulder_01, pachira_aquatica, rock_moss_set_02). Net usable as-is: ~3 of 7.

---

## 4. Section D — Acquisition plan (CC0 + CC-BY 4.0 only)

### 4.1 Real botanical species replacements

| Need | Search term | License | Why | Target builder |
|---|---|---|---|---|
| Pindo palm (*Syagrus romanzoffiana*) | Poly Haven `palm_tree`, `palm` | CC0 | Drooping plumose fronds required (MASTER_BRIEF). No CC0 *Syagrus* exists; closest is generic feathery palm asset, retexture trunk. | `lqv/flora/palms.py` (new) |
| Lapacho (*Handroanthus impetiginosus*) | Poly Haven `flowering_tree`, ambientCG textures | CC0 | Hot-pink trumpet bloom for Variant A. Use jacaranda_tree mesh + override flower material to pink `#E85A8C`. Disclose as substitution. | `lqv/flora/lapacho.py` |
| Mango (*Mangifera indica*) | Poly Haven `mango_tree` | CC0 | Dense dark-green rounded crown. If absent, use Poly Haven `ficus` or generic broadleaf as filler. | `lqv/flora/canopy.py` |
| Tree fern (*Cyathea*) | Poly Haven search "tree_fern", "fern_tree" | CC0 | 2-4 m arboreal fronds, riparian zone. No direct CC0 hit expected. Substitute: combine ground fern_02 (×3 stacked) on a tall trunk asset. Disclose. | `lqv/flora/riparian.py` (new) |
| Guadua bamboo (clumping) | Poly Haven `bamboo` | CC0 | Clumping not running. Required for typology cladding. If only running-bamboo asset exists, retexture culm spacing to clump pattern. | `lqv/typologies/bamboo_*.py` cladding upgrade |
| Anthurium plowmanii | Use existing `anthurium_botany_01` | CC0 | Substitute cultivar — disclose. Retexture leaf to strap shape if midrib texture mismatch. | `lqv/flora/epiphytes.py` (new) |

### 4.2 Architectural prop assets

| Need | Search term | License | Why | Target builder |
|---|---|---|---|---|
| Shipping container (corrugated) | Poly Haven `shipping_container`, ambientCG `corrugated_metal_*` | CC0 | Replace primitive_cube containers in bamboo_container_4pax + container_river_house. Real geometry + corrugated wall texture. | Both container builders |
| Terracotta roof tile texture (PBR) | ambientCG `RoofingTiles_*`, `Terracotta_*` | CC0 | Replace `laterite` material on italian_* roofs. Glazed orange-red, not raw earth. | Italian typologies + materials.py |
| Lapacho/hardwood floorboard texture (PBR) | ambientCG `WoodFloor_*`, `WoodPlanks_*` | CC0 | Replace flat-color lapacho material on decks. Need plank joint lines + grain. | materials.py `lapacho_timber` |
| Sandstone/quartzite wall texture (PBR) | ambientCG `Rock_*`, `Sandstone_*`, `Quartzite_*` | CC0 | Replace flat sandstone on italian_stone walls. Need horizontal bedding + irregular joints. | materials.py `sandstone` |
| Palm thatch roof texture | ambientCG `Thatch_*`, `Straw_*` | CC0 | Replace `sod_canopy` on wigwam + labrisa + family_rectangular roofs. Need fiber direction + shaggy edge. | materials.py `palm_thatch` (new) |
| Lime-washed cob wall texture | ambientCG `Plaster_*`, `Stucco_*`, `Adobe_*` | CC0 | For italian/cob walls. Off-white limewash with subtle irregularity. | materials.py `lime_wash` upgrade |
| EPS foam billet texture | ambientCG `Foam_*`, `Concrete_Rough_*` (matte off-white) | CC0 | Replace `pv_glass` on floating_dining pontoons. | materials.py new `eps_foam_white` |
| Paper-bowl lantern emission shader | Hand-build in materials.py | n/a | Replace `pv_glass` on all 18 lantern bowls. Emission strength ~5, color `#FFD9A8`. | materials.py new `lantern_paper_warm` |
| Manila/sisal rope texture | ambientCG `Rope_*`, `Fabric_Rough_*` | CC0 | Replace `lapacho_timber` on mooring lines. | materials.py new `rope_natural` |
| Sauna pod (Scandi cedar cabin) | Poly Haven `sauna`, `cabin`, `outhouse` | CC0 / CC-BY 4.0 | Replace featureless cube in eco_retreat. | `lqv/amenities/eco_retreat_modern_oasis.py` |
| Chairs, table, food props (dining set) | Poly Haven `chair`, `table`, `dining` | CC0 | Populate floating_dining. | `lqv/amenities/floating_dining.py` |

### 4.3 HDRIs (Paraguay sub-tropical)

The single biggest visual fix.

| Need | Search term | License | Why | Target |
|---|---|---|---|---|
| Paraguay/Atlantic-Forest hilly green afternoon | Poly Haven `subtropical`, `forest_meadow`, `green_hills`, `farm_field_*` | CC0 | Replace the current Lesotho desert HDRI. Need green humid landscape, not red rock. | All sub-renders + composite |
| Golden-hour green pasture | Poly Haven `golden_hour`, `sunset_meadow`, `belfast_sunset` | CC0 | Variant A (winter golden hour, NNW elevation 13°). | Variant A composite |
| Overcast humid morning | Poly Haven `overcast_soil`, `cloudy_*` | CC0 | Variant B (morning overcast). | Variant B composite |
| Blue-hour rural | Poly Haven `dikhololo_night`, `kloofendal_partly_cloudy_puresky` (twilight) | CC0 | Variant C night. | Variant C composite |

### 4.4 PBR textures (additional)

| Need | Search | License |
|---|---|---|
| Concrete cool-roof acrylic | ambientCG `Concrete_Off_White_*`, `Paint_Wall_White_*` | CC0 |
| Steel anodized (containers) | ambientCG `Metal_Painted_*`, `Steel_Painted_*` | CC0 |
| Pool water (with reflective shader) | hand-build in materials.py using `WaterBlue` HDRI reflection | n/a |
| Riparian soil dark | ambientCG `Ground_Forest_Dark_*` | CC0 |

**License audit:** all suggested sources are Poly Haven (CC0) or ambientCG (CC0). Zero CC-BY-SA. Zero CC-BY-NC. CC-BY 4.0 only if Poly Haven asset metadata explicitly says so; flag in `external_assets.md` and add to `CREDITS.md`.

---

## 5. Section E — Diff patch for `scripts/download_polyhaven_assets.py`

Append to the existing `HDRIS`, `TEXTURES`, and `MODELS` lists. Format matches the file's existing dict pattern.

```python
# --- HDRIS: add to HDRIS list ---
HDRIS = [
    # ... existing entries unchanged ...
    {
        'slug': 'belfast_sunset',
        'name': 'Belfast Sunset',
        'category': 'outdoor',
        'reason': 'Golden-hour green farmland — Variant A composite + sub-renders. Replaces current Lesotho red-rock HDRI.',
    },
    {
        'slug': 'kloofendal_partly_cloudy_puresky',
        'name': 'Kloofendal Partly Cloudy Pure Sky',
        'category': 'outdoor',
        'reason': 'Blue-hour pure sky — Variant C composite + sub-renders.',
    },
    {
        'slug': 'syferfontein_18d_clear_puresky',
        'name': 'Syferfontein 18d Clear Pure Sky',
        'category': 'outdoor',
        'reason': 'Mid-afternoon clear sub-tropical — generic Variant B fallback if overcast unavailable.',
    },
    {
        'slug': 'autumn_field_puresky',
        'name': 'Autumn Field Pure Sky',
        'category': 'outdoor',
        'reason': 'Warm-light green meadow — Variant A alternative.',
    },
    {
        'slug': 'rural_asphalt_road',
        'name': 'Rural Asphalt Road',
        'category': 'outdoor',
        'reason': 'Humid green rural — closest aesthetic match for Paraguay countryside if no native HDRI exists.',
    },
    {
        'slug': 'cloudy_cemetery',
        'name': 'Cloudy Cemetery',
        'category': 'outdoor',
        'reason': 'Overcast soft diffuse green — Variant B.',
    },
]

# --- TEXTURES: add to TEXTURES list ---
TEXTURES = [
    # ... existing entries unchanged ...
    {
        'slug': 'terracotta_roof_02',
        'name': 'Terracotta Roof 02',
        'category': 'roof',
        'reason': 'Glazed orange-red terracotta tile — fixes italian_* laterite-roof material bug.',
    },
    {
        'slug': 'thatch_palm_01',
        'name': 'Palm Thatch 01',
        'category': 'roof',
        'reason': 'Golden-brown stranded palm thatch — fixes wigwam, labrisa, family_rectangular sod-canopy roof bug.',
    },
    {
        'slug': 'rough_plaster_05',
        'name': 'Rough Plaster 05',
        'category': 'wall',
        'reason': 'Lime-washed off-white plaster — upgrade for limewash material on italian_* + cob walls.',
    },
    {
        'slug': 'castle_brick_07_red',
        'name': 'Castle Brick 07 Red',
        'category': 'wall',
        'reason': 'Coursed sandstone-color brick — upgrade for italian_stone wall material.',
    },
    {
        'slug': 'corrugated_iron_03',
        'name': 'Corrugated Iron 03',
        'category': 'wall',
        'reason': 'Corrugated metal panel for shipping-container shell texture.',
    },
    {
        'slug': 'rope_woven_01',
        'name': 'Rope Woven 01',
        'category': 'misc',
        'reason': 'Natural sisal/manila rope — fix floating_dining mooring material (currently lapacho_timber).',
    },
    {
        'slug': 'wood_planks_floor_3k',
        'name': 'Wood Plank Flooring',
        'category': 'wood',
        'reason': 'Lapacho deck plank joints + grain — upgrade lapacho_timber material from flat color.',
    },
    {
        'slug': 'concrete_floor_painted_01',
        'name': 'Concrete Floor Painted 01',
        'category': 'concrete',
        'reason': 'Cool-roof acrylic coating — fix bamboo_container_4pax lime_wash misnomer.',
    },
    {
        'slug': 'foam_padding_01',
        'name': 'Foam Padding 01',
        'category': 'misc',
        'reason': 'Matte off-white EPS-like foam — fix floating_dining pontoon pv_glass bug. If unavailable, use rough_plaster_05.',
    },
]

# --- MODELS: add to MODELS list ---
MODELS = [
    # ... existing entries unchanged ...
    {
        'slug': 'shipping_container_01',
        'name': 'Shipping Container 01',
        'category': 'architecture',
        'reason': 'Real corrugated container with door panels + labels. Replaces primitive_cube shell in bamboo_container_4pax + container_river_house.',
    },
    {
        'slug': 'wooden_chair_01',
        'name': 'Wooden Chair 01',
        'category': 'furniture',
        'reason': 'Populate floating_dining (currently bench-only, no chairs).',
    },
    {
        'slug': 'wooden_table_01',
        'name': 'Wooden Table 01',
        'category': 'furniture',
        'reason': 'Same — floating_dining + labrisa_lounge dining surface upgrade.',
    },
    {
        'slug': 'paper_lantern_01',
        'name': 'Paper Lantern 01',
        'category': 'lighting',
        'reason': 'Real warm-glow paper lantern with emission shader. Replaces _grammar.glass_bowl_lantern pv_glass bowl across 18 lantern instances.',
    },
    {
        'slug': 'oil_drum',
        'name': 'Oil Drum (cylindrical rainwater barrel proxy)',
        'category': 'utility',
        'reason': 'Rainwater cistern visible in Rule 10 (mosquito-proofed mesh) — none of the current builders show cisterns.',
    },
    {
        'slug': 'wooden_door_01',
        'name': 'Wooden Door 01',
        'category': 'architecture',
        'reason': 'Real door geometry to replace 3-cube Lego doors in bamboo_beton_30, wigwam, italian_*.',
    },
    {
        'slug': 'bamboo_clump',
        'name': 'Bamboo Clump (search Poly Haven actual slug)',
        'category': 'flora',
        'reason': 'Real Guadua-style clumping bamboo for riparian zone + typology cladding upgrade.',
    },
    {
        'slug': 'flowering_tree_pink',
        'name': 'Flowering Tree Pink (lapacho proxy)',
        'category': 'flora',
        'reason': 'Hot-pink-flower tree for Variant A lapacho bloom. If absent, retint jacaranda_tree flower material to #E85A8C-#F0A0C8.',
    },
]
```

**Note:** all `slug` values above are placeholders — actual Poly Haven slugs must be confirmed via `mcp__blender__search_polyhaven_assets` when the MCP socket is revived. Re-verify exact slugs before running the downloader. The download script's idempotent + resume-safe behavior (per repo memory) means re-running with these entries is non-destructive.

---

## 6. Section F — Ranked priority for escritura 2026-06-27

### P0 — must fix before showing Wesley (today/tomorrow, 2026-06-12 → 2026-06-13)

1. **HDRI replacement.** Single largest visual win. Download Paraguayan-aesthetic HDRI (`belfast_sunset` or `autumn_field_puresky`), wire into `lqv/subscene/base.py:setup()`, re-render all 17 sub-renders. Cost: ~30 min download + 4 hours render. **This alone moves the deck from "unshowable" to "credible draft".**
2. **Material registry triage** (`lqv/materials.py`). Fix 5 wrong material lookups in one sitting:
   - `_mat('sod_canopy')` → introduce `_mat('palm_thatch')` and rewire wigwam + labrisa + family_rectangular roofs.
   - `_mat('laterite')` → introduce `_mat('terracotta_tile')` and rewire italian_* roofs.
   - `_mat('pv_glass')` → introduce `_mat('lantern_paper_warm')` (emission shader) and rewire `_grammar.py:128`.
   - `_mat('pv_glass')` fallback on water → introduce `_mat('water_reflective')` and rewire eco_pool, floating_dining, labrisa creek.
   - `_mat('lapacho_timber')` on mooring rope → introduce `_mat('rope_natural')` and rewire `floating_dining.py:274`.
3. **Three critical geometry bugs:**
   - `bamboo_boomhut_treehouse.py:204-233` — fix or hide spiral stair (floating debris).
   - `bamboo_river_house.py:245-261` — fix stair direction.
   - `hobbit_house.py:91-103` — honor SNAP='cut', or just remove the asset from the deck for now.
4. **`subscene/base.py` add `clip_end=1000.0` parameter** to prevent silent HDRI clipping on parcel-scale assets.
5. **Pull the quiver_tree_01 from the asset library.** Wrong continent.

### P1 — fix before final 18-render deck for escritura (2026-06-13 → 2026-06-20)

6. **Replace primitive_cube containers** with downloaded corrugated container model (bamboo_container_4pax + container_river_house).
7. **Replace primitive cones in eco_pool** `_regen_plants()` with real reed/grass asset.
8. **Add randomness to eco_pool `_coping()`** — break the bead-necklace pattern with `random.uniform` jitter.
9. **Fix italian_stone_small_v1 ROOF_TYPE constant** — either change constant to `terracotta_tile_hipped` or change geometry to gabled. Pick one.
10. **Wire raised stone foundations ≥60 cm** under any building that's missing them (bamboo_wigwam_lodge, possibly others). Rule 4.
11. **Add bamboo asset (Guadua clumping)** and replace plastic-dowel cylinders in 6 typologies + 4 amenities.
12. **Lapacho bloom retint** for Variant A — jacaranda_tree flower material override to hot pink.

### P2 — post-escritura polish (post 2026-06-27)

13. **PBR texture upgrade pass** — wood planks, sandstone, plaster textures replace flat colors.
14. **Populate floating_dining** with chairs, food, place settings.
15. **Add chimney caps, shutters, balconies, dormers** to italian_* typologies for villa identity.
16. **Boomhut tree:** add procedural lapacho or mango trunk + canopy under the platform.
17. **eco_retreat sauna pod:** swap featureless cube for real cabin asset.
18. **Add doors and windows everywhere they're missing** (containers, wigwam, beton family, hobbit).
19. **Roof-area takeoff fix** in bamboo_beton_30.py (double-counts overhangs).
20. **Wigwam thatch cone door cutout** — match thatch boolean to skipped pole position.

---

## 7. Next 48 h ship plan (2026-06-12 → 2026-06-14)

**Day 1 (2026-06-12) — material + HDRI triage**

- 09:00-11:00: Pull P0 HDRI(s) via `scripts/download_polyhaven_assets.py` (after appending the Section E patch).
- 11:00-13:00: Implement 5 material additions in `lqv/materials.py` (palm_thatch, terracotta_tile, lantern_paper_warm, water_reflective, rope_natural).
- 13:00-15:00: Wire material references across 8 builders.
- 15:00-17:00: Add `clip_end=1000.0` to `subscene/base.py`; re-render all 17 sub-renders.
- Evening: visual review against this doc.

**Day 2 (2026-06-13) — geometry triage**

- 09:00-12:00: Fix 3 stair bugs (boomhut, bamboo_river_house, container_river_house) + hobbit berm.
- 12:00-13:00: Smoke test (`scripts/smoke_test.sh`) — verify byte-identity invariants intact.
- 13:00-15:00: Re-render 4 affected sub-renders.
- 15:00-17:00: Pull quiver_tree from asset register + CREDITS.md + external_assets.md.
- Evening: write CHANGELOG entry + commit.

**Total deliverable at end of 48h:** 17 sub-renders re-shot with Paraguay-aesthetic HDRI + 5 correct material categories + 4 geometry bugs fixed. **Estimated quality jump: 60-70 % of "unshowable" → "draft-credible".** The remaining 30-40 % needs the P1 list (Section F).

---

End of roast. Counter-arguments welcome — cite line numbers.
