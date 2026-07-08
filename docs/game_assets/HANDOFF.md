# La Quebrada Viva → Unreal Engine 5.7 — Handoff

**Phase 1 complete (commit `eeafde9`).** All assets exported. Ready for
UE5.7 + Cesium for Unreal assembly.

## What shipped (36 MB total under `docs/game_assets/`)

```
docs/game_assets/
├── MANIFEST.json                          (master inventory, consumed by UE build script)
├── heightmaps/
│   ├── lqv_terrain_height_16bit.png       (UE Landscape import — 108×180 16-bit PNG)
│   ├── lqv_terrain_height_meters.csv      (debug — full 19,440 cell elevation grid)
│   ├── lqv_flow_accumulation.png          (quebrada visualisation, grayscale)
│   └── lqv_terrain_metadata.json          (UE import settings)
├── geodata/
│   ├── lqv_property_polygon.geojson       (62-ha escritura polygon — Cesium anchor)
│   ├── lqv_aoi_bbox.geojson               (1100-ha acquisition bbox)
│   ├── lqv_aoi_extended.geojson
│   ├── lqv_buildability_zones.geojson     (4 classes, 1358 polygons — in-game overlay)
│   ├── lqv_quebrada_polygon.geojson       (pysheds flow-accumulation, 716 polygons)
│   ├── lqv_waterfall_candidates.geojson   (top-5 DEM step-detection, point features)
│   ├── lqv_osm_roads.geojson              (10km box roads + tracks)
│   ├── lqv_osm_waterways.geojson          (10km box OSM water)
│   └── lqv_solar_pv_zones.geojson         (north-facing + slope<30%, 770 polygons)
├── textures/
│   ├── lqv_esri_z17_2km.png               (1792×1792 @ 1.07 m/pixel, ~1.9×2.1 km coverage)
│   └── README.md                          (Esri attribution + Cesium usage notes)
└── glb/
    ├── riverstone_cob_house.glb           (14 MB, 99 objects — house + ground)
    └── riverstone_house_only.glb          (14 MB, 65 objects — house w/o ground)
```

## Tools (under `tools/`)

| Script | Purpose |
|---|---|
| `tools/lqv_to_ue.py` | Idempotent one-pass export of every asset above. Re-run anytime. |
| `tools/lqv_fetch_esri_hd.py` | Esri HD tile fetch (49 tiles → 1 PNG). |
| `tools/export_lqv_glb.sh` | Blender headless driver: builds Cob/Bottle/Tatakua via existing `lqv/house/*.py`, exports GLB. |
| `tools/export_lqv_house_minimal.py` | Bypasses Cycles/GPU requirement so GLB export works on CPU-only machines. |

## Next session — Phase 2: UE5.7 + Cesium assembly

### Hardware prerequisites

The current VPS (`/dev/sda1`, 387 GB disk, 31 GB RAM, **no GPU**) is fine for
asset pipeline + headless export. **UE5 editor + Pixel Streaming require a
GPU host.** Two viable options:

1. **Local dev box** (recommended for interactive work)
   - Linux/Windows/Mac with RTX 3060+ (8 GB VRAM minimum)
   - Epic Games Launcher download (UE 5.7 = ~30 GB)
   - Build the game locally, then deploy to cloud for Pixel Streaming

2. **Cloud GPU rental** (for build/CI without local hardware)
   - Hetzner GPU server (€120-300/month, RTX 4000 Ada)
   - Vast.ai spot instances ($0.50-1.50/hour, RTX 4090)
   - Runway / AWS g5 instances ($1-3/hour)

### Step-by-step (local box assumed)

```bash
# 1. Install UE 5.7
#    Epic Games Launcher → Unreal Engine → Install 5.7.x → ~30 GB

# 2. Install Cesium for Unreal
#    Open UE → Edit → Plugins → search "Cesium for Unreal" → install (free, MIT core)
#    Get a Cesium ion token at https://cesium.com/ion/tokens (free tier OK)
#    In UE: Cesium → Cesium ion Token → paste token

# 3. Create new project
#    File → New Project → Games → Open World template
#    Project name: LQV_Walk, location: pick somewhere outside the LQV repo
#    (UE generates tons of cache files; keep it separate)

# 4. Enable World Partition + Nanite + Lumen
#    World Settings → World Partition → Enable (default on)
#    Project Settings → Rendering → Hardware Ray Tracing → enable
#    Project Settings → Rendering → Lumen → enable Global Illumination + Reflections
#    Project Settings → Rendering → Nanite → enable (required for Landscape)

# 5. Drop in the Cesium World Terrain + Bing Aerial
#    Place Actors → Cesium → Cesium3DTileset
#    Tileset URL: https://assets.cesium.com/1 (requires ion token)
#    Or for offline: use our local Esri PNG as a drape texture on a plane

# 6. Import our heightmap as a Landscape
#    In Content Browser → Import → lqv_terrain_height_16bit.png
#    When prompted "Create Landscape" → Yes
#    Section size: 255 (from lqv_terrain_metadata.json)
#    Z scale: 100 (we have 142m relief, UE exaggerates)
#    XY scale: 100 (1 UE unit = 1 m)
#    Total components: 16 (from metadata)

# 7. Anchor to LQV centroid
#    In Cesium World Terrain, set the camera/anchor to:
#       Lon: -57.030, Lat: -25.630, Height: 200m
#    This snaps the world to Paraguay and our heightmap aligns to ground truth.

# 8. Import the GLB
#    Import → riverstone_cob_house.glb
#    Drag onto level. Move to flat zone (127-169 m elevation per analysis JSON)
#    Scale: 100x (cm to m) or set import scale to 0.01

# 9. Place buildability overlay
#    Import lqv_buildability_zones.geojson as a CSV → use CesiumPolygon or
#    build a procedural mesh from the polygons for the 4 buildability classes

# 10. Waterfall
#    Use lqv_waterfall_candidates.geojson rank-1 (-57.019, -25.625, 287m, 28m drop)
#    Niagara → Waterfall template, attach to mesh

# 11. Quebrada
#    Import lqv_quebrada_polygon.geojson as polygons → use Cesium's
#    PolygonRasterOverlay or UE5 Water System to render the stream

# 12. Foliage
#    Procedural Foliage Tool → scatter using lqv_flow_accumulation.png
#    as a density mask (forest = high acc areas, low areas = cleared)
#    Use Meta CHM stats (mean 3.5m, p95 13m) for tree height distribution
```

### Optional: Pixel Streaming deploy

```bash
# On the cloud GPU server (Hetzner/Vast.ai):
# 1. Install UE 5.7 (Linux build, ~25 GB)
# 2. Package the project: Package Project → Windows/Linux → builds ~10 GB
# 3. Run with -PixelStreaming flags + a TURN/STUN server
# 4. Front with Cloudflare Calls or LiveKit Cloud for global WebRTC
# 5. Embed in iframe at lqv-walkthrough.pages.dev/play
```

## Critical numbers to remember

| What | Value | Source |
|---|---|---|
| Centroid | -57.030, -25.630 | `aoi_62ha.geojson` metadata |
| Elevation range | 116 – 395 m AMSL | `alos_aw3d30_dem.tif` (raw, full bbox) |
| Parcel relief | 142 m (121–263 m at parcel) | `01_buildable_terrain.json` |
| Buildable flat (slope <5%) | 81 ha (29.4% of parcel) | `01_buildable_terrain.json` |
| Buildable flat + moderate (slope <15%) | 220 ha (79.7%) | `01_buildable_terrain.json` |
| Aspect distribution dominant | E 22.9%, SE 18.4%, NE 14.5% | `01_buildable_terrain.json` |
| Solar PV suitable | 20.5 ha (7.4%) → 20.5 MW theoretical | `04_solar_pv.json` |
| Canopy mean / p95 | 3.46 m / 13.01 m | `05_canopy_height.json` |
| Quebrada threshold | 50 cells (4.5 ha upstream) | `tools/lqv_to_ue.py` |
| Best waterfall candidate | -57.019, -25.625, 287 m, 28 m drop | `06_drainage_basin.json` |
| Property polygon (62 ha) | **Pending Anexo I from escritura** | `property_polygon/` |
| Coordinate system | WGS84 (EPSG:4326), UTM 21J for analysis | repo convention |
| Engine convention | +Y north (south hemisphere), +X east | per `build_scene.py` header |

## Open questions for the operator

1. **GPU box?** Local dev machine, or rent Hetzner/Vast.ai?
2. **Pixel Streaming vs downloadable build?** Pixel Streaming = server-rendered (costs scale 1:1 with users). Downloadable = free, but each user needs a decent GPU.
3. **Cesium ion token?** Free tier = 50k tile requests/month. Paid = ~$50/month for unlimited. The LQV viewer is low-volume so free tier is fine for v1.
4. **Game mode?** First-person walk, third-person walk, top-down planning, or all three?
5. **Anexo I?** When the 62-ha polygon arrives, replace `lqv_property_polygon.geojson` and re-run `tools/lqv_to_ue.py`.