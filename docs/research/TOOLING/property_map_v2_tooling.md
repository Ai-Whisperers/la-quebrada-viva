# Property map v2 — tooling research

> Roadmap for evolving `docs/site_data/property_map/` (v1 at `e3d8cce`) from a 4-class NDVI raster + DEM hydrography sketch into a complete, photo-anchored 3D digital twin with **tree-by-tree identification**, accurate hydrography, full structure inventory, and a beautiful presentation surface. Audience: future-Ivan + future-Claude pairing in autonomous-work mode.

**Status of v1 (e3d8cce):** Sentinel-2 10 m / Cop30 30 m / OSM — works as a "what we know from space" snapshot, but cannot count stems, cannot resolve seasonal vs perennial streams, and OSM under-reports rural Paraguarí (0 on-property structures, almost no internal tracks).

**Goal of v2 / v3:** every tree (≥ 5 m height) positioned + classified to genus, every structure mapped, every stream classified perennial / seasonal / ephemeral, and the whole thing renderable as a photoreal 3D scene from any camera.

---

## TL;DR — the recommended stack by phase

| Phase | Spend | Outputs | Bottleneck cleared |
|---|---|---|---|
| **0 — Free uplift now** | $0 | NICFI 4.77 m mosaic + Earth Engine time-series + Sentinel-1 SAR + DeepForest crown polygons | NDVI single-date → year-long phenology; aggregate canopy → individual crowns at ~5 m |
| **1 — Photo intake (T+30→T+60)** | ~$50 | Photo-anchored vectors: on-property structures, internal tracks, salto pool, fence lines | OSM coverage gap closed; satellite claims promoted 🛰️→✅ |
| **2 — Drone RGB + multispec flight** | ~$800–2,500 | 5 cm orthomosaic + 10 cm DSM/DTM + photometric tree crowns + multispec species hints | Sub-1 m resolution → individual trees countable + buildings cm-accurate |
| **3 — Drone LiDAR + botany walk** | ~$4,000–9,000 | Canopy Height Model 50 cm, tree-by-tree stems, species ID by field-botanist + iNaturalist | Genus-level species, under-canopy DTM, terrain accurate to ±10 cm |
| **4 — 3D twin build** | $0–$300/mo (UE5 free; Cesium ion paid tier optional) | Walkable scene in Blender + UE5+Cesium streaming, web viewer | Concept art → walkable digital twin |
| **5 — Delivery surface** | $0–$50/mo | Hero stills (Blender), real-time walkthrough (UE5), web viewer (Cesium ion), print cartography (QGIS/Felt) | Single PNG → multi-modal client surface |

The cheapest meaningful upgrade is **Phase 0** and we should do it this week. Drone flight (Phase 2) is the highest leverage paid step. LiDAR (Phase 3) is the only path to per-stem positions under closed canopy and is what `RESEARCH_GAPS.md` R35 has been waiting for.

---

## 1. Where v1 ends and what blocks "complete"

### What v1 has
- Sentinel-2 NDVI 4-class (10 m, single date 2026-05-12, S2B_21JVM_20260512_0_L2A)
- Sentinel-2 NDWI water mask (single date, same tile)
- Copernicus DEM 30 m → D8 fill-pits → flow-accum ≥ 30 cells → 15 stream lines
- OSM Overpass: 9 buildings (all neighbours), 1 road, 2 farmland, 0 water
- Composite: matplotlib + hillshade, 300 dpi, EPSG:32721

### What blocks completion
1. **Sentinel-2 10 m cannot resolve individual tree crowns.** Crown diameters in Atlantic Forest are typically 4–12 m; one S2 pixel averages 4–6 crowns of mixed species. NDVI tells us *canopy density*, not *count* or *species*.
2. **Cop30 DEM 30 m smooths out small headwater channels and any feature < 1 m vertical.** D8 lines below 30-cell threshold are noise; above, they could equally be perennial creeks or dry erosion scars. Sub-canopy ground topography is mostly invisible.
3. **OSM in rural Paraguarí is sparse.** Wesley's cabins, tool sheds, gates, fences, pump-houses, internal tracks, the rumoured salto — none of those are in OSM, ever. Only photos or drone flight will surface them.
4. **Single-date imagery hides phenology.** A May 2026 NDVI snapshot misses the August dry-season die-back and the November green flush — both relevant for deciduous lapacho mapping, pasture vs. forest separation, and seasonal-stream classification.
5. **No species attribute.** Even with crown segmentation, telling lapacho from yvyra-pytã from jacarandá from mango needs multispectral + a field crew.
6. **No 3D.** v1 is a 2D map. The digital-twin goal needs DSM + DTM + canopy structure + texture, not just classes.

These six blockers structure the rest of the research below.

---

## 2. Imagery sources — beyond Sentinel-2

### Free / no-spend
| Source | Resolution | Cadence | Best for | How |
|---|---|---|---|---|
| **NICFI Planet basemap (tropical)** | 4.77 m RGB+NIR | Monthly | **Crown-scale canopy mapping** — the single biggest free upgrade over S2 for our latitude | Sign up at https://www.planet.com/nicfi/ — free tropical access for non-commercial; tiles via XYZ or GeoTIFF download |
| **Sentinel-2 L2A** (currently) | 10 m | 5 days | Phenology time-series (not single date) | `sentinelhub-py`, `eodag`, `pystac-client` + Earthdata or AWS Open Data |
| **Sentinel-1 SAR** | 5×20 m | 6–12 days | Cloud-penetrating, soil moisture, biomass proxy, perennial vs ephemeral water | `sentinelhub-py`, GEE `COPERNICUS/S1_GRD` |
| **Landsat 8 / 9 thermal (TIRS)** | 100 m thermal, 30 m optical | 8 days | Surface temperature for ET / shade mapping | GEE `LANDSAT/LC08/C02/T1_L2` |
| **MODIS Terra/Aqua** | 250 m–1 km | Daily | Long-term phenology baseline (2000–) | GEE `MODIS/061/MOD13Q1` |
| **ALOS PALSAR L-band SAR** | 25 m | Annual mosaic | **Biomass / canopy structure under cloud** (L-band penetrates canopy) | https://www.eorc.jaxa.jp/ALOS/en/dataset/palsar2_l4_e.htm |
| **TanDEM-X 30 m DEM** (DLR) | 30 m | Static | Independent cross-check vs Cop30 | https://geoservice.dlr.de/web/dataguide/tdm30 |
| **ALOS AW3D30** (currently have) | 30 m | Static | DEM cross-check | OpenTopography |
| **SRTM GL1** (currently have) | 30 m | Static | DEM cross-check | OpenTopography |
| **Esri World Imagery** | 30 cm–1 m where available | Variable | Free visual cross-check via tile slip | https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer (XYZ tiles, attribution required) |
| **Bing Maps Aerial** | 30 cm–1 m | Variable | Free visual cross-check | https://dev.virtualearth.net (Bing Maps Key, free tier) |
| **Google Earth Pro** | varies | varies | Manual KML/KMZ digitization + historical imagery slider (one of the few ways to get sub-meter look-back) | Desktop tool — KMZ tile export legal for non-commercial |
| **Google Earth Engine (GEE)** | — | — | **Cloud platform that hosts most of the above + 600+ other datasets, free for research** | https://earthengine.google.com — sign up with `weissvanderpol.ivan@gmail.com`, then `earthengine authenticate` |

**Concrete action:** sign up for GEE + NICFI today, both free, both transformational.

### Paid (per-image)
| Source | Resolution | Cost | When worth it |
|---|---|---|---|
| **Planet PlanetScope** (Tier 2 / commercial) | 3 m | ~$1–3/km²/month subscription, or ~$0.50/km² per image | Daily 3 m for change-detection (e.g., during construction) |
| **Planet SkySat** | 50 cm | ~$5–25/km² | One-off ultra-high-res ortho for hero map |
| **Maxar WorldView-3** | 31 cm | ~$15–50/km² | Tree-crown level RGB from space, when drones aren't an option |
| **Airbus Pléiades** | 50 cm | ~$10–30/km² | Stereo pairs → DEM |
| **Capella Space (SAR)** | 50 cm SAR | ~$50–200/km² | Niche; we don't need this |

For a 30.9 ha polygon (0.31 km²), even a 50 cm Maxar Pleiades grab is ~$5–15. **One-off purchase for hero cartography is cheap; the real spend is drone flights at higher resolution and full 3D.**

### Recommended additions to v2 (free only)
1. **GEE authentication** → enables S2 time-series median (cloud-masked), NICFI tile fetch, SAR, MODIS phenology.
2. **NICFI 4.77 m monthly mosaic** → swap as the canopy base layer; ~6× linear resolution of S2.
3. **S1 SAR VV/VH median** → adds perennial-water + biomass texture under cloud-cover periods.
4. **Sentinel-2 12-date time-series median** → kills cloud artefacts, captures phenology (dry-season die-back of pasture vs evergreen forest).
5. **PALSAR-2 L-band mosaic** → biomass / canopy structure cross-check.

---

## 3. Drone capture — the single highest-leverage paid step

Drones close every gap at once: sub-1 m imagery, cm-scale DSM/DTM via SfM, optional LiDAR for under-canopy ground, optional multispec for species hints. Paraguay has multiple operators.

### Hardware tiers (purchase or hire)
| Tier | Platform | Sensor | Approx total cost | Use case |
|---|---|---|---|---|
| Entry | DJI Mini 4 Pro | 4/3" RGB 48 MP | ~$1,000 | Visual fly-over, not survey-grade |
| Survey-RGB | DJI Mavic 3E (Enterprise) | 4/3" RGB 20 MP, RTK option | ~$3,500 + ~$650 RTK | Photogrammetry orthomosaic 2–3 cm GSD |
| Survey-RGB+RTK | DJI Phantom 4 RTK | RGB 20 MP, on-board RTK | ~$6,500 (discontinued but plentiful used) | Industry-standard photogrammetry, cm GPS |
| Multispec | DJI Mavic 3 Multispectral | RGB + 4 narrowband (G/R/RE/NIR) | ~$5,000 | **Canopy + crop health + species hints in one flight** |
| LiDAR | DJI Matrice 350 RTK + Zenmuse L2 | RGB + LiDAR (240k pts/s, 5 cm acc) | ~$25,000+ | **Under-canopy DTM + per-stem CHM in one flight** |
| Pro mapping | WingtraOne / Quantum Trinity F90+ | RGB + RTK fixed-wing | ~$35,000+ | 100s of ha per flight; overkill at 30 ha |

**For 30.9 ha at La Quebrada Viva:** a single Mavic 3E flight covers it in ~25 min at 60 m AGL → 2 cm GSD orthomosaic. A Zenmuse L2 LiDAR pass covers it in ~35 min → 200+ pts/m² CHM. Both are *one-flight* jobs.

### Hiring vs buying
**Hire for 1–3 surveys, buy if we'll re-fly quarterly.** Going rates in Paraguay / Argentina border region (2026):

- Photogrammetry RGB orthomosaic, ~30 ha: **~$400–900 all-in** (operator + processing).
- Multispec NDVI/NDRE flight, ~30 ha: **~$700–1,500**.
- LiDAR flight, ~30 ha: **~$2,500–4,500** (operator only); **+$1,500–3,500 processing**.

### Operators in Paraguay (research targets, not endorsed yet)
- **Geoinformática Paraguay** — Asunción-based, offers Pix4D / Metashape processing.
- **GeoSurvey PY** — has flown LiDAR for hidroeléctrica projects.
- **Servicios Aéreos Paraguay (SAP)** — full-service drone ops.
- **Universidad Nacional de Asunción (FCA — Facultad Cs. Agrarias)** — academic flight + Pix4D student lab; cheaper if framed as a research collab.
- **AGROCAD SRL** — agro-focused multispec, would handle the 30 ha well.

R37/R38 outreach posture (DECISIONS.md 2026-06-28) extends to these — **no contact until photos drop and Wesley approves**.

### Regulation (DINAC / SENATUR Paraguay)
- DINAC RAP 100 (Reglamento Aeronáutico Paraguayo) governs sUAS < 25 kg.
- **Registration required** for any UAV ≥ 250 g flown commercially.
- **Pilot license (RPAS)** required for commercial operations.
- VLOS within 500 m horizontal / 120 m AGL altitude default.
- Operating in Escobar district (rural, no Class C airspace, no nearby uncontrolled aerodromes within 5 km after a quick AIP check) is straightforward; expect 1-week paper turnaround for a one-off authorization.
- A **registered operator handles all of this** — another reason hiring beats buying for v2.

### Output of one drone flight (RGB SfM)
1. ~2,000–4,000 raw JPGs with EXIF + RTK
2. Sparse pointcloud (SfM) → dense pointcloud (MVS) — ~50–200 M points
3. **DSM (Digital Surface Model)** — top-of-canopy heights, 5–10 cm grid
4. **DTM (Digital Terrain Model)** — ground heights with canopy stripped (poor under closed canopy without LiDAR — this is the LiDAR win)
5. **Canopy Height Model (CHM = DSM − DTM)** — input to tree detection
6. **Orthomosaic** — true-orthorectified RGB, 2–5 cm GSD
7. **Mesh** — textured 3D mesh, ready for Blender / UE5 import

---

## 4. Photogrammetry / SfM software

### Open-source (we can run today, no spend)
| Tool | What it does | Notes |
|---|---|---|
| **OpenDroneMap (ODM)** + **WebODM** | Full pipeline: SfM → dense cloud → DEM → ortho → mesh | https://opendronemap.org — Docker one-liner; well-supported community. **First choice for self-processing.** |
| **Meshroom (AliceVision)** | SfM + MVS GUI | Free, GPU-accelerated, good for textured meshes. Less aero-specific than ODM. |
| **COLMAP + OpenMVS** | SfM (COLMAP) + dense MVS (OpenMVS) | CLI-only, scriptable, research-grade. |
| **MicMac (IGN France)** | Full photogrammetry suite | Steep learning curve; CNES / IGN-grade accuracy. |
| **NodeODM** | ODM as a network service | For pipeline integration. |

### Commercial (only if free fails on a specific dataset)
| Tool | Cost | Notes |
|---|---|---|
| **Agisoft Metashape Pro** | $3,500 perpetual | Industry standard; excellent dense MVS. |
| **Pix4D Mapper / Matic** | $3,500/yr / $260/mo | Operator favorite; cleanest reports. |
| **RealityCapture** | Free for <€1M revenue (Epic) | Best mesh quality, very GPU-hungry. **Free for us.** |
| **DroneDeploy** | $300/mo | Cloud SaaS; quick. |
| **3DSurvey** | €1,500/yr | Slovenia-made; great DTM extraction. |

**Recommendation:** Stand up WebODM in Docker today as the default; keep RealityCapture as the backup for "I need a beautiful mesh for the hero shot."

```bash
docker pull opendronemap/webodm
docker run -d -p 8000:8000 --name webodm opendronemap/webodm
# UI at http://localhost:8000
```

---

## 5. LiDAR — the only path to per-stem positions under closed canopy

R35 has been on hold for this. The Atlantic Forest at La Quebrada Viva has ~85 % closed canopy on satellite — photogrammetry alone cannot give us ground topo or count understorey stems.

### Capture options
- **Drone LiDAR (Zenmuse L2 + M350 RTK)** — best price/perf at 30 ha, 200 pts/m², ±5 cm accuracy. ~$2,500–4,500 to hire.
- **Airborne LiDAR (Cessna + Riegl)** — flown by SAP / Geosurvey, accurate but expensive (~$8–15k for a single mission to 30 ha — overkill).
- **Mobile / backpack LiDAR (e.g. GeoSLAM ZEB Horizon)** — operator walks the polygon; perfect for fine site detail like the salto + internal tracks. Hire ~$200/day.

### Processing software
| Tool | Cost | Best for |
|---|---|---|
| **lidR (R)** | Free | **Individual Tree Detection (ITD)**, CHM, DTM extraction. Industry-standard R package. |
| **PDAL** | Free | CLI pipeline for filter/classify/reproject. |
| **CloudCompare** | Free | GUI for pointcloud inspection + manual classification. |
| **WhiteboxTools** | Free | Hydrology + DEM from LiDAR; pure-Rust, fast. |
| **Open3D (Python)** | Free | Pythonic pipeline, ML-friendly. |
| **LAStools** | $1,500–3,500 | The classic; commercial. |
| **TerraScan (Terrasolid)** | $5,000+ | Industry-grade classification. |
| **Bentley OpenCities / iTwin** | $$$ | Enterprise BIM; not for us. |

**Recommendation:** lidR + WhiteboxTools + PDAL for the whole stack. All free, all scriptable.

### Individual tree detection (ITD) — algorithm choices
- `lidR::find_trees(las, lmf(ws = 5))` — local maxima on CHM (fast, good for distinct crowns).
- `lidR::segment_trees(las, dalponte2016())` — region-growing on CHM (good for closed canopy).
- `lidR::segment_trees(las, li2012())` — pointcloud-based (slow but accurate for complex canopies).
- `itcSegment` (R) — Dalponte's original ITC implementation.
- `TreeIso` — Python ITD on raw pointcloud.
- `AdQSM` — quantitative structure model per tree.

For the Atlantic Forest closed-canopy structure we should run `dalponte2016` or `li2012` and validate against a ground-truth subset.

---

## 6. Individual tree detection — without LiDAR (DL on imagery)

If LiDAR is months away, **deep-learning crown detection on RGB orthomosaics is the bridge**.

### Models / packages
| Tool | Input | Output | Notes |
|---|---|---|---|
| **DeepForest** (PyPI) | RGB tile | Tree crown bounding boxes | Pre-trained on NEON tropical / temperate; fine-tune on our orthomosaic. https://deepforest.readthedocs.io |
| **detectree2** (Restor.eco) | RGB tile | **Crown polygons (Mask R-CNN)** — better than DeepForest's boxes for densely packed crowns | https://github.com/PatBall1/detectree2 — trained on Atlantic Forest / Borneo / Malaysia |
| **TreeSeg** | RGB + CHM | Crown polygons | Hybrid; needs CHM too. |
| **PlanetScope tree-crown segmentation (DeepForest fine-tune)** | NICFI 4.77 m | Aggregated crown clusters | Lower precision but works on free imagery |
| **Segment Anything (Meta SAM2)** | RGB tile + point/box prompt | Crown polygons (zero-shot) | https://github.com/facebookresearch/sam2 — pair with QGIS plugin |
| **Geo-SAM (QGIS plugin)** | Any raster + click | Vector polygons | https://github.com/coolzhao/Geo-SAM — interactive workflow for buildings + crowns |
| **samgeo** (Python) | Raster | Vector polygons | https://samgeo.gishub.org — programmatic SAM for georasters |

### Recommended Phase-0 pipeline
1. Pull NICFI mosaic for our polygon (Phase 0).
2. Run DeepForest pretrained on the NICFI tile → crown bounding boxes.
3. Cross-check against detectree2 Mask R-CNN for polygon shape.
4. Cluster boxes by NDVI bin → "where dense canopy meets crown count."
5. Output `vector/crowns_v1_nicfi.geojson` — first version of trees-as-features.

This won't be perfect at 4.77 m (small understorey trees will merge), but it's the right shape for the v2 deliverable, with v3 replacing it after drone + LiDAR.

---

## 7. Species identification

Crown polygons answer "where is each tree." Species ID answers "what is each tree."

### Field-walk + ML hybrid (the practical path)
1. **Field botanist + iNaturalist app** — a 1-day walk with a regional botanist (UNA Facultad de Ciencias Agrarias has ~10 forest-botany faculty; ~$200–400/day) producing geotagged identifications for ~100–300 sample trees.
2. **Pl@ntNet API** (https://my.plantnet.org/) — free 500 calls/day, identifies from leaf/flower/fruit photos; pair with EXIF GPS to anchor each ID.
3. **iNaturalist Vision API** — similar coverage, taxonomic-rank ID with confidence.

### ML on multispec / hyperspec
- **DJI Mavic 3 Multispectral** gives us 4 narrowband channels — enough to separate broad classes (lapacho deciduous winter signature vs evergreen mango vs pindo palm) but not enough for genus-level ID inside the Atlantic Forest.
- **Hyperspectral drones** (Headwall, Resonon Pika) — ~$50k+, can do genus-level. Out of budget.
- **Public hyperspectral satellite** — EMIT / PRISMA / EnMAP — 30 m GSD; useful for *biome* analysis, not per-tree.

### Reference databases for Paraguayan species
- **Tropicos (Missouri Botanical Garden)** — https://www.tropicos.org — taxonomic backbone.
- **Flora del Paraguay** — Gentry / Spichiger / Mereles series.
- **Atlantic Forest Tree Database (Lima et al. 2020)** — ~5,000 species.
- **GBIF Paraguay occurrences** — https://www.gbif.org/country/PY/ — geotagged occurrence records.
- **Restor.eco regional biome models** — free ecology baseline.

### Practical species output
Target for v3: a **per-tree GeoJSON with `{stem_id, x, y, height, crown_d, genus, species_confidence, source}`** where `source` ∈ {field_ID, plantnet, inaturalist, ml_inferred}. ~80 % stems left at genus-only is acceptable; the 5–10 % "hero" stems (lapachos, ceibos, large palms) should be species-level.

---

## 8. Hydrography v2 — beyond D8 / 30 m

### Better DEMs feed better hydrology
- **Drone SfM DSM/DTM @ 5–10 cm** (Phase 2) replaces Cop30 30 m → 30,000× pixel-area refinement.
- **LiDAR DTM @ 30–50 cm** (Phase 3) is the only way to see micro-channels under closed canopy.

### Better algorithms
| Tool | Notes |
|---|---|
| **pysheds** (currently use) | Python D8, simple. |
| **pyflwdir** (Eilander/Deltares) | **Successor to pysheds — better fill, D-infinity, sub-grid routing.** https://github.com/Deltares/pyflwdir |
| **WhiteboxTools** | Best free flow-routing; D-inf, Mass Flux, FD8. https://www.whiteboxgeo.com/manual/wbt_book/intro.html |
| **TauDEM** | Reference D-inf implementation; CLI. |
| **GRASS GIS r.watershed** | Battle-tested; A* drainage routing. |
| **HydroSHEDS / MERIT-Hydro** | Pre-computed continental hydrography; coarse but cross-check. |

### Photo-anchored stream classification
- Walk every stream with a GPS-enabled camera (Wesley's phone or RTK Emlid Reach).
- For each crossing, photograph + GPS-tag with one of: `perennial / seasonal / ephemeral / dry`.
- Annotate `vector/hydrography_dem.geojson` segments → `vector/hydrography_v2.geojson` with confirmed type.
- Update `post_escritura_site_knowledge.md` §3.

---

## 9. Structures, tracks, fences — the OSM-gap layer

OSM gives us 9 buildings *outside* the polygon. Everything *inside* needs photo or drone digitization.

### Tools for digitizing from imagery + photos
- **QGIS + Geo-SAM** — click a building → polygon; click a track → centerline. Replaces hand-tracing.
- **samgeo** — programmatic SAM on georasters.
- **Roboflow** — for training a custom building detector on Paraguayan vernacular architecture (cob, brick, sheet-metal roof).
- **PlanetScope time-series change detection** — `pystac-client` + `rio-stac` — anything that wasn't there in 2024 but is there in 2027 is new construction, useful during Phase-1 build.

### Output schema for v2
- `vector/buildings_v2.geojson` — OSM buildings (outside) + photo-anchored on-property structures (inside), with `{kind, material, photo_source, confidence}`.
- `vector/tracks_v2.geojson` — internal access tracks digitized from drone ortho, with `{surface, width_m, length_m}`.
- `vector/fences_v2.geojson` — polygon boundary + internal subdivisions.
- `vector/photo_anchored.geojson` — salto, springs, mature singular trees, cultural features.

---

## 10. The 3D twin — six viable stacks

Goal: a walkable / flyable / renderable 3D scene with **photoreal terrain + correct tree positions + correct buildings + correct hydrography + correct lighting**, that we can either render as hero stills (current Cycles pipeline) or stream to client devices.

### Option A — **Blender** (current stack, already deep)
**What we have:** `lqv/` package, `build_scene.py` driver, Cycles + AgX, 18 finals at `85e86aa`.

**Add-ons to install:**
| Add-on | Purpose | Cost |
|---|---|---|
| **BlenderGIS** | KMZ / SHP / raster / DEM / Google-tile import | Free, GPL |
| **Blosm** (formerly Blender-OSM) | OSM 3D buildings + terrain in one click | Free / paid Premium ($35) |
| **A.N.T. Landscape** | Procedural terrain (already shipped with Blender) | Free, built-in |
| **MTree** | **Better procedural trees than Sapling** | Free |
| **The Grove 3D** | Photoreal tree generator | €128 |
| **Botaniq** (Polygoniq) | 850+ botanical assets (paid) | €179 (or €19/mo) |
| **Geo Scatter** | Heavy-duty scatter, replaces stock particles | €99 |
| **Plant Factory** (e-on) | Procedural plant species; legacy but works | Free for personal use |
| **Sapling Tree Gen** | Built-in, free | Free, built-in |
| **HumGen3D / Botaniq** | Optional ground vegetation | varies |

**Pipeline:**
1. BlenderGIS import: polygon KML → DEM GeoTIFF (drone DTM) → SRTM as fallback → orthomosaic as base texture.
2. Geometry Nodes: instance MTree-generated trees at GeoJSON positions; vary scale/rotation by `crown_d` / `height`.
3. Cycles render at 4K hero res; reuse `lqv/lighting.py` setup.
4. Existing cob house module `lqv/house/cob.py` drops in at chosen Phase-1 cabin position.

**Strength:** we own this pipeline already; renders are byte-stable; integrates with existing 18 finals.
**Weakness:** not interactive; large-area scatter is GPU-RAM-hungry; not webable.

### Option B — **Houdini Indie**
**Cost:** $269/yr (Indie license, gross-revenue < $100k).
**Strength:** Heightfields workflow is the best in the industry for sculpted terrain + erosion + procedural scatter at scale. PDG / TOPs for batch processing tile sets. USD pipeline for handing off to UE5.
**Weakness:** new tool to learn; overkill if we stay 2D-render-only.
**When worth it:** if we scale beyond 30 ha (full 62 ha legal + neighbour analysis) or want erosion simulation.

### Option C — **Unreal Engine 5 + Cesium for Unreal**
**Cost:** UE5 free; Cesium for Unreal free; Cesium ion paid tier optional ($95/mo for asset hosting).
**What it unlocks:**
- **Cesium ion** streams global terrain + imagery (Bing Maps Aerial / Sentinel-2 / our own tilesets) on demand.
- **Megascans** library (free for UE) — photoreal trees, rocks, ground textures.
- **PCG (Procedural Content Generation)** — scatter trees from our crown GeoJSON.
- **Nanite + Lumen** — real-time GI at film quality, walkable.
- **Pixel Streaming** — host the scene as a web URL the client opens in a browser.

**Pipeline:**
1. Import polygon + DTM via Cesium.
2. Drape orthomosaic over terrain.
3. PCG graph: each crown polygon → instance Megascans tree by species class.
4. Drop cob cabin (from Blender FBX export) at Phase-1 site.
5. Bake / render hero shots in UE5 Movie Render Queue, or stream live.

**Strength:** real-time, walkable, web-streamable, free.
**Weakness:** UE5 learning curve; PCG graph authoring; binary size large (15–40 GB project).
**When worth it:** the moment we want Wesley to walk through the property in his browser.

### Option D — **Unity HDRP + Cesium for Unity**
Similar capabilities to UE5 path; HDRP for high-end rendering, MicroSplat for terrain layering. Smaller binaries than UE5 but smaller asset library. **Pick this only if we already had Unity expertise; otherwise UE5 wins.**

### Option E — **Twinmotion**
Real-time arch-viz built on UE5, no scripting needed. Cesium tiles supported since 2024. **Easiest non-coder path** to a walkable scene; weakest customization.
**Cost:** $299/yr (commercial); free education.
**When worth it:** if we want Wesley himself to navigate / take screenshots without our help.

### Option F — Web 3D
| Tool | What | When |
|---|---|---|
| **CesiumJS** | Browser-native 3D globe (the open-source ancestor of Cesium for Unreal) | Web-shareable scene from any device |
| **Three.js** | Generic browser 3D | Custom interactive scene |
| **Mapbox GL JS** + 3D terrain | Map-first 3D | If we want a 2D-with-zoom UX |
| **deck.gl** | WebGL data viz over maps | Best for showing per-tree data layers |
| **kepler.gl** (Uber) | No-code map dashboards | Quick share with Wesley |
| **Felt** | Web maps, collaborative | Replace QGIS print map |

### Option G — Terrain authoring
| Tool | Cost | Use |
|---|---|---|
| **Gaea** (QuadSpinner) | Free / $99 | Procedural terrain authoring; export heightmaps |
| **World Creator** | $199–499 | Real-time terrain; great for hero stills |
| **Terragen 4** | $349 | Photoreal renderer + terrain; legacy but beautiful |
| **WorldMachine** | $189 | Heightmap synthesis; export to Blender/UE5 |

These are useful as a **last polish step** — Gaea takes our drone DTM, adds erosion + flow simulation noise, exports a higher-fidelity heightmap back to Blender / UE5.

### Recommendation
- **Today**: stay on Blender, install BlenderGIS + Blosm + MTree, prototype the 3D twin import in `lqv/world/` (new submodule).
- **Phase 4**: parallel-track UE5 + Cesium for Unreal for the walkable version. Free; same Cesium tilesets we'd host anyway.
- **Phase 5 delivery**: Blender for print hero stills, UE5 for walkthrough video, Cesium ion + CesiumJS for web URL.

---

## 11. Cartographic / 2D map polish

### Open-source
- **QGIS** — print layout designer; we should redo the property map cartography here for legal-grade output (legend, scale bar, projection box, north arrow with declination).
- **GRASS GIS** — backbone for raster ops, especially `r.watershed`.
- **MapServer / GeoServer** — host WMS / WFS endpoints if we want a self-hosted tile server.
- **Tilemaker / Tippecanoe** — generate vector tilesets from our GeoJSON.

### Web cartography
- **Felt** — collaborative web maps; drag-drop our GeoJSONs. Free tier handles a small project.
- **Mapbox Studio** — design vector tile styles; Mapbox-hosted.
- **MapTiler Cloud** — like Mapbox but with self-host option.
- **Maputnik** — open style editor for MapLibre.

### Print
- **MapBox print → Affinity Designer / Inkscape / Illustrator** for final polish.
- **QGIS Atlas** — generate a multi-page map book (one page per Phase-1 cabin site, etc.).

---

## 12. Asset libraries — trees, rocks, ground

| Library | Cost | What | Why |
|---|---|---|---|
| **Quixel Megascans** | Free for UE5; $19/mo standalone | Photoreal scanned trees, plants, rocks, ground | Highest-fidelity botanical assets globally |
| **Poly Haven** | Free (CC0) | HDRIs, textures, models | We already use it |
| **BlenderKit** | Free / $13.5/mo | Massive Blender-native library | One-click drop-in |
| **The Grove 3D** | €128 | Procedural tree generator | Genus-aware tree generation |
| **Botaniq** | €179 | 850+ botanical models | Drag-drop botanical library |
| **MTree** | Free | Procedural trees in Blender | Free Sapling replacement |
| **GraswaldGS / Botaniq Ultra** | €99–349 | Grass + understorey | Ground vegetation |
| **3D-Trees.com** (Maxtree) | €30–€600 | High-poly tree models | Hero foreground trees |
| **Vegetation Engine** (UE5) | $250 | UE5 ground vegetation system | UE5 path only |
| **TreeIt** | Free | Procedural tree exporter | FBX export to anywhere |
| **SpeedTree** | $19/mo (Indie) | Industry standard | If we go AAA |

For Paraguay-specific species, we should **generate lapacho + pindo palm + mango + tree fern + bamboo + agave variants ourselves** using MTree + reference photos, save as `.blend` library — extends what `lqv/flora/` already does.

---

## 13. AI / ML accelerators (foundation models + datasets)

| Tool | Purpose | Cost |
|---|---|---|
| **Segment Anything 2 (SAM2, Meta)** | Zero-shot segmentation of buildings, crowns, water, anything | Free |
| **Geo-SAM (QGIS plugin)** | SAM2 inside QGIS for click-segmentation | Free |
| **samgeo** | SAM2 for georasters in Python | Free |
| **DINOv2 (Meta)** | Embeddings for similarity search across imagery | Free |
| **TorchGeo (Microsoft)** | Datasets + models for remote sensing | Free |
| **Raster Vision** (Azavea) | Pipelines for satellite ML | Free |
| **Restor.eco** | Pre-computed biome-level forest analytics | Free for non-commercial |
| **Global Forest Watch (WRI)** | Tree-cover loss alerts | Free API |
| **Hansen Global Forest Change** | Annual tree-cover delta 2000– | Free GEE asset |
| **FAO WaPOR** | Evapotranspiration + biomass for Africa + Middle East (not us) | Free |
| **Google DeepMind Tropical Forests team** | Research outputs occasionally usable | Free papers |

**For tree detection specifically**, the combo `NICFI → DeepForest → detectree2 → samgeo polishing` is the free-stack frontier.

---

## 14. GPS / photo-anchoring hardware

- **Phone EXIF** — Wesley's phone with location services on (≈ ±5 m accuracy). Fine for stream-crossing tagging.
- **Garmin handheld GPS** (eTrex 32x) — ~$300, ±3 m, durable.
- **Emlid Reach RS3 RTK** — ~$2,400, ±1 cm with NTRIP correction. Overkill for tagging but necessary for ground control points during drone flights.
- **DJI RC Pro with RTK** — built into Phantom 4 RTK / Mavic 3 RTK.
- **GeoTrack EXIF tools** — `exiftool`, `Photo-EXIFTool`, `gpicsync`, `geotag` (R package).

---

## 15. Concrete v2 roadmap — what we do, in what order

### Phase 0 — Free uplift (this week, 0 spend)
1. **Earth Engine** account → `earthengine authenticate` on this machine.
2. **NICFI Planet** account → register at https://www.planet.com/nicfi/.
3. Install Python packages:
   ```bash
   pip install earthengine-api pystac-client planetary-computer eodag \
               pyflwdir whitebox deepforest segment-anything-2 samgeo \
               leafmap geopandas rasterio rio-cogeo
   ```
4. New driver `scripts/build_property_map_v2.py`:
   - Pull NICFI 4.77 m mosaic for polygon AOI (most recent, then 12-month median).
   - Pull S2 12-date median via GEE.
   - Pull S1 SAR VV/VH median.
   - DeepForest crown detection on NICFI tile.
   - detectree2 Mask R-CNN for crown polygons.
   - Compose new map: NICFI base + crown polygons + existing OSM + existing D8 streams.
5. Add `vector/crowns_v1_nicfi.geojson` to `docs/site_data/property_map/vector/`.
6. Update `index.md` + `photo_verification.md` for v2 deliverables.
7. Commit + push.

### Phase 1 — Photo intake (T+30 → T+60, ~$50)
1. When Wesley's photos arrive, run the existing intake checklist (`docs/site_data/client_photos/2026-06_post_escritura/index.md`).
2. Geo-SAM in QGIS to vectorize structures + tracks from sat tiles + photos.
3. Annotate `vector/photo_anchored.geojson`.
4. Promote 🛰️ → ✅ / ❌ in `photo_verification.md`.
5. Update post_escritura_site_knowledge.md §3 + §6 + DECISIONS.md.

### Phase 2 — Drone RGB flight (T+60 → T+90, ~$800–2,500)
1. Hire AGROCAD / Geoinformática Paraguay / FCA-UNA for one Mavic 3M or Mavic 3E flight.
2. Process orthomosaic + DSM in WebODM.
3. DeepForest + detectree2 on 5 cm orthomosaic → crown polygons.
4. WhiteboxTools D8 on cm-scale DTM → high-res stream centerlines.
5. Output `property_map_v3.png` + `vector/crowns_v2_drone.geojson`.

### Phase 3 — Drone LiDAR + botany (T+90 → T+150, ~$4,000–9,000)
1. Hire LiDAR operator (Zenmuse L2 + M350 RTK).
2. lidR ITD on 200 pts/m² cloud → per-stem positions + heights.
3. Hire UNA botanist for 2-day field walk → 200–400 sample IDs.
4. Pl@ntNet + iNaturalist for non-sampled stems.
5. Output `vector/trees_v3.geojson` — full tree inventory, ~80 % genus, ~10 % species.

### Phase 4 — 3D twin (T+90 onward, parallel)
1. **Blender path**: `lqv/world/` new submodule. BlenderGIS terrain import; Geometry Nodes tree scatter from `crowns_v3.geojson`; Cycles render.
2. **UE5 path**: new `unreal/` directory (sibling to `lqv/`). UE5 project + Cesium for Unreal + Megascans + PCG.
3. **Web path**: CesiumJS viewer; host tiles on Cesium ion ($95/mo) or self-host.

### Phase 5 — Delivery (T+150)
1. Print hero map: QGIS print layout, A0, professional cartography.
2. Hero stills: Cycles 4K, current 18-shot manifest re-rendered with photoreal terrain.
3. Walkthrough video: UE5 Movie Render Queue, 4K 60 fps, 2–3 min.
4. Web URL: CesiumJS embed Wesley can DM neighbours.

---

## 16. Spend ceiling — to scope conversations with Wesley

| Phase | Min spend | Max spend |
|---|---|---|
| 0 | $0 | $0 |
| 1 | $0 | $50 (storage + a battery pack for the photo walk) |
| 2 | $400 | $2,500 |
| 3 | $4,000 | $9,000 |
| 4 (3D twin software) | $0 | $300/mo recurring (Cesium ion paid) |
| 5 (delivery) | $0 | $300 (print, hosting) |
| **Total v3 ceiling** | **~$4,400** | **~$12,150 + ~$300/mo recurring** |

For comparison, a typical Atlantic-Forest 3D twin project (academic + agency) lands in the **$15,000–$40,000** range — we get there for $5k–$12k by reusing free tooling at every stage.

---

## 17. What stays satellite-only forever

Some things genuinely cannot be improved with more spend:

- **Continuous monthly NDVI time-series** stays Sentinel-2 because nothing else has the cadence.
- **Tree-cover loss alerts** stay Hansen / GFW.
- **Climate baseline** stays ERA5 / WorldClim.
- **Regional context** (neighbour parcels, watershed-scale flow accumulation) stays Cop30 / NICFI.

Drone + LiDAR replace satellite for the **30.9 ha** polygon, not for the regional context. v3 keeps the satellite layers as the wider-context base map.

---

## 18. Anti-recommendations (things to skip)

- **Hyperspectral drone sensors** — $50k+, marginal gain for genus-level on Atlantic Forest. Skip.
- **Fixed-wing survey drones** (WingtraOne) — overkill at 30 ha. Skip.
- **Maxar single-image purchase** — $50–100 useful only as a one-off cartographic flourish; drone gets us 100× resolution for 10× the cost. Skip until v4.
- **Building a custom species classifier from scratch** — DeepForest + detectree2 + Pl@ntNet already cover 80 % at zero training cost. Skip custom training unless v3 reveals a specific failure mode.
- **CityEngine / Bentley iTwin / ArcGIS Pro** — enterprise tools; no client-side ROI for us. Skip.
- **Unity over UE5** — UE5 has Cesium for Unreal + Megascans + Nanite, all free. Unity has no clear edge at our scale. Skip.

---

## 19. Index of related docs

- `docs/site_data/property_map/index.md` — v1 layer manifest
- `docs/site_data/property_map/photo_verification.md` — 14-row shot-list cross-ref
- `docs/RESEARCH_GAPS.md` — R01 (photos) and R35 (LiDAR / sub-1 m imagery)
- `docs/post_escritura_site_knowledge.md` — current knowledge baseline
- `docs/research/GEDI_L2A_RESEARCH.md` — spaceborne LiDAR baseline (already on disk)
- `docs/research/BLENDER_GIS_3D_LANDSCAPE_RESEARCH.md` — earlier 3D terrain research
- `docs/research/2026-06-10_vegetation_3d_research.md` — vegetation-in-Blender research
- `docs/research/ASSET_RESEARCH_2026-06-13.md` — asset-library audit
- `docs/research/REPO_CATALOG.md` — 141-repo catalogue

---

## 20. Open decisions for Wesley (parked, do not ask yet — wait for photo intake)

1. Drone budget cap for v2 — single flight ($800–2,500) or full multispec + LiDAR ($6k–9k)?
2. UE5 walkthrough — Wesley's interest in a walkable browser scene vs. happy with stills?
3. Tile hosting — self-host Cesium tilesets, or $95/mo Cesium ion?
4. Species-ID field walk — UNA botanist hire, or wait until Wesley's own forest walks identify the bigger ones?

These belong in `docs/DECISIONS.md` once Phase-0 ships and we have a v2 map to point at.
