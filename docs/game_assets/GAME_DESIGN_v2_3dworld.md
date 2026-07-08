# La Quebrada Viva — 3D World Builder (v2)

**Version:** 0.2 (2026-07-08) — **scope pivoted**: from "buyer videogame" to "collaborative planning tool"
**Author:** Erebus / Ai-Whisperers
**Engine:** Unreal Engine 5.7 + Three.js browser fallback
**Target users:** Ivan + Wesley van de Camp (collaborative site planning)
**Target platform:** Desktop (UE5.7 + Nanite/Lumen) + Browser (Three.js, no GPU required)

---

## 1. Why this pivot

The original GAME_DESIGN.md (v0.1) framed LQV as a "buyer walkthrough videogame." After
auditing the actual user behavior — Ivan + Wesley sit together with maps and 3D renders,
debating *where to place the cob house*, *which slope is buildable*, *how far the quebrada
is from the planned house site* — the real deliverable is a **3D world with the topology,
property boundary, quebrada, monte, waterfall, OSM roads, and buildability zones already
loaded**, that both people can navigate together and use as the canvas for placement
decisions.

**Zero game mechanics.** No quests, no NPCs, no scoring, no day/night cycle, no
inventory, no audio cues. The "game" is the world itself; the "play" is collaborative
spatial planning with the client.

The original v0.1 GAME_DESIGN.md is preserved at `GAME_DESIGN_v1_archived.md` for
historical context.

## 2. What ships in v0.2 (this version)

**The world** (the only thing that matters):
- 62-ha LQV parcel + ~1,100-ha AOI context
- Real DEM (Copernicus GLO-30, 30 m) → low-poly stepped terrain mesh
- All 13 cerros/peaks (auto-detected from closed contour rings) marked in 3D
- Quebrada (year-round stream) as blue ribbon mesh
- Waterfall candidate locations as Niagara/Skia-fall particles
- Monte/escarpment highlighted with darker shading + low-poly rocks
- Esri HD satellite texture draping the terrain (Zelda-tinted, not photoreal)
- 60-80 low-poly trees scattered per Hansen/NDVI density (lapacho, palmera, pine)
- OSM roads + pathways as low-poly trails
- Cob house in **low-poly Zelda style** (thatched roof, stone chimney, arched door)
- 4-5 house-typology placeholders (cob, bamboo wigwam, tatakua, worker housing, glamping tent)

**The tools** (planning-specific):
- **WASD + mouse-look camera** (free walk, first-person at human eye-height)
- **Orbit camera** (mouse-drag, "see the whole property from above")
- **Click-to-measure** (place 2 markers → distance + elevation diff + avg slope)
- **Click-to-inspect** (any terrain pixel → elevation + slope + aspect + NDVI in HUD)
- **Click-to-place** (pick typology from radial menu, click terrain → place house)
- **Buildability overlay** (red = slope >15°, green = buildable, yellow = caution)
- **Solar PV overlay** (cyan = good roof orientation, with monthly shading estimate)
- **Quebrada + 50m buffer** (no-build zone highlighted)
- **Save/load layout** (JSON of placed houses → shareable with Wesley)
- **Screenshot** (capture current camera view → share with stakeholder)

## 3. Three navigation modes

### 3.1 Free walk (default for client meetings)
- First-person at 1.7 m eye-height
- WASD + mouse-look, Shift to sprint
- Esc = release mouse for menu access
- Click = inspect/measure/place (context-sensitive)

### 3.2 Orbit (default for solo planning)
- Mouse-drag = orbit around target point (default: parcel centroid)
- Mouse-wheel = zoom
- Right-drag = pan target
- Click-on-terrain = move target to that point

### 3.3 Cinematic (no input, just view)
- Auto-orbit at 30-second cycle
- Useful when projector-ing to a wall during a client call
- Pause with Space

## 4. Site analysis data already wired

| Layer | Source | Visualization | Use |
|---|---|---|---|
| Buildability | `geodata/lqv_buildability_zones.geojson` (1.1 MB, 4 classes) | Color-coded overlay: green (≤5°), yellow (5-15°), orange (15-30°), red (>30°) | Where can a house go? |
| Solar PV | `geodata/lqv_solar_pv_zones.geojson` (382 KB) | Cyan overlay on north/NE/NW-facing slopes <30° | Where to put solar panels? |
| Quebrada + 50m buffer | `geodata/lqv_quebrada_polygon.geojson` (288 KB) | Blue ribbon + red hatched buffer | Where NOT to build (flood zone) |
| Cerros/peaks | `data/peaks_10km.geojson` (new from this session) | Cone markers at each summit with elevation popup | Visualize surrounding topography |
| Slope heatmap | `data/slope_10km.jpg` (new from this session) | Green→red raster | Quick visual scan for buildable areas |
| Aspect map | `data/aspect_10km.jpg` (new from this session) | HSV color-wheel | Sun orientation for any slope |
| NDVI canopy | `data/ndvi_canopy_10km.geojson` (637 KB) | Green overlay, denser = healthier forest | Where to thin trees vs. preserve |
| Hansen forest loss | `data/hansen_loss_10km.geojson` (1.9 MB) | Red patches where forest was cleared | Historical disturbance context |
| OSM roads | `geodata/lqv_osm_roads.geojson` (636 KB) | Yellow lines | Access routes to/from site |
| OSM waterways | `geodata/lqv_osm_waterways.geojson` (273 KB) | Light blue lines | Confirms quebrada on official map |
| Waterfall candidates | `geodata/lqv_waterfall_candidates.geojson` | Animated particle + audio proximity | Find the 274m cascade |

## 5. Asset pipeline (low-poly retro style)

### 5.1 Style reference

Color palette (Zelda: Breath of the Wild inspired, Paraguay-tuned):
- Grass: `#7a9b4e` (Atlantic Forest green, slightly desaturated)
- Foliage dark: `#3d5a2a`
- Foliage bright: `#a8c668` (lapacho yellow-pink tree variant)
- Earth: `#8a6a3a` (reddish-brown clay, matches the quebrada sediment)
- Rock: `#6e6258` (weathered sandstone)
- Water: `#5b9dd9` (Atlantic-clear turquoise)
- Sky: `#e8d8b0` (warm hazy, not photoreal blue)
- House cob walls: `#d4a154` (warm sun-baked earth)
- House thatch: `#a8895a` (golden straw)
- Stone chimney: `#4a4540`
- Door: `#3a2e22` (dark wood)

Lighting model: cel-shaded (3-tone: bright / mid / shadow), soft ambient occlusion
between meshes, no specular highlights on grass/foliage (matte). Hard rim light on
buildings to read silhouettes against the sky. NO bloom, NO motion blur, NO depth of
field (clean, readable, "this is a planning document" aesthetic).

### 5.2 Mesh budget per asset

| Asset | Poly target | UV channels | Texture |
|---|---|---|---|
| Terrain (62 ha @ 1m resolution) | ~50k tris | 1 (satellite drape) | 1024×1024 Zelda-tinted Esri |
| Tree (per-instance, 6 variants) | 80-200 tris | 0 (vertex color) | — |
| Rock cluster | 30-60 tris per rock | 0 (vertex color) | — |
| Waterfall mesh | 60 tris | 0 (animated UV) | 256×256 water normal |
| Cob house | 800-1500 tris | 2 (atlas for door/thatch/wall) | 512×512 atlas |
| Tatakua standalone | 400 tris | 1 | 256×256 |
| Worker housing (T04) | 600 tris | 2 | 512×512 |
| Bamboo wigwam | 300 tris | 1 | 256×256 |
| Glamping tent | 200 tris | 1 | 256×256 |

Total scene budget (Wes + 5 visitors + trees + rocks + waterfall): ~150k tris. Fits
in 6-draw-call batches, runs at 60 fps on any 2018+ GPU, no LOD needed for the
62-ha scale.

### 5.3 Generation pipeline

```
Phase A — Terrain & geographic features (Blender headless):
  tools/build_lowpoly_terrain.py   → lowpoly_terrain.glb (50k tris, vertex-colored cliffs)
  tools/build_lowpoly_archetypes.py → 8 archetypes: tree_lapacho.glb, tree_palmera.glb,
                                          tree_pino.glb, rock_cluster.glb,
                                          waterfall.glb, monte_highlight.glb,
                                          gate.glb, walking_trail.glb
  tools/build_lowpoly_house.py   → lqv_house_cob_lowpoly.glb (Zelda style, 1k tris)
  tools/build_lowpoly_typo_set.py → 5 typology variants: cob, tatakua, worker, wigwam, glamping

Phase B — Asset placement (deterministic from real data):
  tools/place_lowpoly_world.py    → reads geo-data + Hansen + NDVI, generates
                                    placed_lowpoly_world.json with:
                                    - terrain transform
                                    - tree positions + species per Hansen/NDVI pixel
                                    - rock positions on cliffs (slope >30°)
                                    - waterfall + stream segments
                                    - house typology catalog (for click-to-place)
  Generates placed_lowpoly_world.json consumable by both Three.js and UE5.

Phase C — Deploy:
  tools/build_threejs_preview.py → exports placed_lowpoly_world.json +
                                    all GLBs as a static HTML bundle
                                    deployable to lqv-walkthrough.pages.dev/play
  tools/build_ue5_3dworld.py      → UE5.7 editor Python: spawns terrain Static
                                    Mesh, places each archetype, wires
                                    click-to-place + measurement tools
```

## 6. Three.js browser preview (deployed free)

This is the **immediate value deliverable**. Runs in any browser, no GPU, no UE5,
no installation. Deploys to `lqv-walkthrough.pages.dev/play.html` (or `/play`).

```html
<canvas id="world"></canvas>
<script type="importmap">
{
  "imports": {
    "three": "https://unpkg.com/three@0.169.0/build/three.module.js",
    "three/addons/": "https://unpkg.com/three@0.169.0/examples/jsm/"
  }
</script>
<script type="module">
  // Load placed_lowpoly_world.json + GLBs
  // Wire OrbitControls + first-person toggle
  // Wire raycast click-to-place + click-to-measure
  // Wire site-analysis overlay toggles
</script>
```

**Try it:** https://lqv-walkthrough.pages.dev/play.html (live after this session)

## 7. UE5.7 build (the production target)

When the operator wants to open UE5.7 (requires GPU host + UE install — see
`docs/_archive/2026-07-08_ue5_zombie/tools/install_ue5_on_gpu.sh` and
`provision_hetzner_gpu.sh`):

1. `bootstrap_lqv_3dworld_on_laptop.sh` creates a fresh `.uproject` with all
   required plugins enabled (World Partition, Nanite, Lumen, Cesium NOT NEEDED
   for this version, Niagara for waterfall, EnhancedInput, PythonScriptPlugin).
2. `build_lqv_3dworld_level.py` runs inside UE editor:
   - Imports `lowpoly_terrain.glb` as Nanite Static Mesh
   - Spawns InstancedStaticMesh for each tree species (60-80 trees total)
   - Spawns waterfall Niagara system at the GPS-confirmed cascade location
   - Sets Cesium-free scene lighting (3-tone cel-shading via Material parameter)
   - Wires click-to-place logic in Blueprint or C++
   - Saves `/Game/LQV_3DWorld.umap`
3. `deploy_lqv_pixstream_3dworld.sh` pushes to Hetzner GPU server with Pixel
   Streaming for browser-based access from any device.

## 8. Site analysis HUD (the planning tool's killer feature)

When the user clicks anywhere on the terrain, the HUD shows:

```
┌────────────────────────────────────────────────┐
│ 📍 Pin: -25.6082°, -57.0304° (3.2 km N of gate) │
│ ↗ Elevation: 287 m   ↘ Slope: 18.4° (orange)     │
│ ☀ Aspect: 142° (SE-facing)   🌳 NDVI: 0.72      │
│ ⚡ Solar: 4.2 kWh/m²/day (good)                   │
│ 💧 Nearest quebrada: 142 m (NO-BUILD BUFFER)     │
│ 🏠 Buildability: CAUTION (slope 15-30°)         │
└────────────────────────────────────────────────┘
```

All values are computed from the data already in the repo. The HUD answers
Wes's most common question during planning: **"can I put a house here?"**

## 9. Click-to-place typology picker

Press `Tab` → radial menu with the 5 typologies + "remove house" + "save layout":

```
              [Cob house]
                ↑
[Glamping]  ←       →  [Worker housing]
   ↓                 ↓
[Tatakua]    [Wigwam]
                ↓
           [Remove last]
           [Save layout]
```

Each typology card shows: thumbnail render + name + footprint area + estimated
cost (from MASTER_BRIEF reconciled). Click to select → cursor becomes ghost
outline → click terrain to place. Right-click to cancel. Undo: Ctrl+Z.

## 10. Save / share

- **Save layout**: serializes placed houses + camera state to JSON,
  downloads as `lqv_layout_YYYY-MM-DD.json`
- **Share URL**: encodes layout in URL hash, copy-paste link for Wesley
- **Screenshot**: PNG of current view, downloads as `lqv_view_YYYY-MM-DD_HH-MM.png`
- **Export to UE5**: writes a `LQV_3DWorld_Placement.json` in the format the UE5
  build script reads, so what Wes designs in the browser can be opened directly
  in UE5 with all houses pre-placed

## 11. Open design questions for the operator

1. **Default camera height on first load?** Bird's-eye (200m) or ground (1.7m)?
2. **Which typology should be default in the picker?** (Cob = flagship)
3. **Cost estimates in the picker — do you want them?** (links to MASTER_BRIEF)
4. **Auto-snap to nearest buildable zone?** Or allow free placement?
5. **Quebrada buffer distance?** (default 50m — close enough for views, far enough for safety)
6. **Save layout format?** (JSON vs. CSV vs. KMZ for Google Earth import)

## 12. Critical references

- `docs/game_assets/heightmaps/lqv_terrain_height_16bit.png` — terrain mesh source
- `docs/game_assets/textures/lqv_esri_z17_2km.png` — satellite drape source
- `geodata/lqv_property_polygon.geojson` — 62-ha boundary (decoration)
- `geodata/lqv_buildability_zones.geojson` — 4-class slope overlay
- `geodata/lqv_solar_pv_zones.geojson` — solar suitability overlay
- `geodata/lqv_quebrada_polygon.geojson` — stream + buffer
- `data/peaks_10km.geojson` — 13 cerros (new)
- `tools/build_lowpoly_*.py` — Blender headless asset pipeline (this PR)
- `tools/build_threejs_preview.py` — browser deploy (this PR)
- `tools/build_ue5_3dworld_level.py` — UE5 editor Python (when GPU available)
- `tools/bootstrap_lqv_3dworld_on_laptop.sh` — fresh UE5 project bootstrap
- `GAME_DESIGN_v1_archived.md` — original videogame vision (preserved for context)
