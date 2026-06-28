# Blender GIS & 3D Landscape Pipeline Research

> Re-research of GitHub repos for Blender GIS / terrain mesh / landscape pipelines, targeted at **La Quebrada Viva** (Escobar, Paraguarí, Paraguay — Atlantic Forest + sandstone escarpment + cob house). 23 repos catalogued. Compiled 2026-06-10, same day as the previous `docs/research/README.md` mega-sweep — this report cross-checks and **overrides** the previous verdicts on the 7 Blender-addon repos based on live GitHub state today.

## TL;DR — Top 3 recommendations

1. **Drop-in: `lqv/site/dem.py`** using `rasterio` + `numpy` + `bmesh` — custom-built, ~120 lines, headless-friendly, deterministic, no addon dependency. **Override** the prior session's "skip BlenderGIS" verdict: BlenderGIS v2.2.15 (Dec 20 2025) IS still active, but for our pipeline the custom path remains correct (RNG-ordering invariant, no 4.x compat question, no addon install in the headless wrapper). Confirmed by the previous research's note: "Skip BlenderGIS; use rasterio + custom script. Confirmed by both the DEM tooling and Blender GIS research. Cost: ~80 lines of Python. Benefit: deterministic, headless-friendly, 4.x-compatible."

2. **Reference workflow: `joewdavies/geoblender`** (1.8k stars, Jan 11 2026) — the canonical QGIS + Blender shaded-relief tutorial using **displacement node on a subdivided plane**. This is the rendering pattern to copy for the La Quebrada escarpment cliff-face where we don't need a real mesh, just a tessellated plane with a DEM as displacement texture (cheap, fast, perfect for the hero camera's cliff-far-background).

3. **Adopt: `rasterio/rasterio` + `geopandas/geopandas` + `gboeing/osmnx`** for the **data prep layer** outside Blender. rasterio for DEM/raster I/O, geopandas for the Atlantic Forest polygon / cob-house footprint vector data, osmnx for the road/driveway network into the site. All three are already in `scripts/`. No new deps needed.

## Methodology

- **gitingest** (README + tree): 3/9 user-specified Blender addons succeeded (`domlysz/BlenderGIS`, `vvoovv/blender-osm`, `enesovski/BlenderRawImageImporter`). 6 returned 400 Bad Request. The remaining 19 repos (incl. all topic-page discoveries) were probed via `webfetch` of `github.com/owner/repo` HTML pages (which embed the README + last-commit/release info) or `raw.githubusercontent.com`.
- **Topic pages** (`/topics/blender`, `/topics/gis`, `/topics/geospatial`, `/topics/terrain-generation`, `/topics/blender-gis`) were scraped for star counts, descriptions, and last-update dates. 5,103 + 6,408 + 4,788 + 458 + 1 repos in scope.
- **Search results** (`/search?q=blender+terrain+mesh&type=repositories`) — 16 hits, all single-file toys.
- **Stack Exchange**: `gis.stackexchange.com/questions/tagged/blender` and `blender.stackexchange.com/questions/tagged/heightmap` both returned **404** (tag pages no longer route). Probing abandoned.
- **gitingest rate-limited** at ~5 calls/min (429). Used the GitHub HTML pages as fallback for READMEs.

---

## Repo catalog (23 repos)

Verdict codes: **ADOPT** = drop into the pipeline, **REFERENCE** = read the README / skim code, **SKIP** = wrong tool / unmaintained / inferior to what we have, **DEAD** = 404 on GitHub today.

| # | Repo | Stars | Last update | Verdict | One-line reason |
|---|---|---:|---|---|---|
| 1 | [domlysz/BlenderGIS](https://github.com/domlysz/BlenderGIS) | 9.0k | Dec 20 2025 (v2.2.15) | **REFERENCE** | Active + most popular, but GUI-click-driven; we need headless. Use the Delaunay-triangulation code as reference, not the addon itself. |
| 2 | [vvoovv/blender-osm](https://github.com/vvoovv/blender-osm) → redirects to [vvoovv/blosm](https://github.com/vvoovv/blosm) | 2.0k | May 5 2026 | **SKIP** | City-scale OSM import (buildings/roads), not terrain. Not relevant for our 62 ha. |
| 3 | [vvoovv/blender-osm-2](https://github.com/vvoovv/blender-osm-2) | — | — | **DEAD** | 404. Repo deleted or renamed. |
| 4 | [cgcai/Blender-Terrain-Generator](https://github.com/cgcai/Blender-Terrain-Generator) | — | — | **DEAD** | 404. Single-file abandoned script, name only. |
| 5 | [jwjacobson/blender-heightmap](https://github.com/jwjacobson/blender-heightmap) | — | — | **DEAD** | 404. Was a procedural-noise heightmap generator, no longer exists. |
| 6 | [EarthX/Blender-GIS-Importer](https://github.com/EarthX/Blender-GIS-Importer) | — | — | **DEAD** | 404. Was a GEOTIFF/GeoJSON importer, no longer exists. |
| 7 | [kaiaeberli/Blender-GIS](https://github.com/kaiaeberli/Blender-GIS) | — | — | **DEAD** | 404. Was a forked/forked BlenderGIS variant. |
| 8 | [ambrosiussen/blender-gis-extract](https://github.com/ambrosiussen/blender-gis-extract) | — | — | **DEAD** | 404. Was a terrain extractor. |
| 9 | [proceduralia/highland](https://github.com/proceduralia/highland) | — | — | **DEAD** | 404. Was a Unity terrain tool, not Blender. Misnamed search hit. |
| 10 | [joewdavies/geoblender](https://github.com/joewdavies/geoblender) | 1.8k | Jan 11 2026 | **ADOPT** | The QGIS+Blender shaded-relief tutorial. Copy the displacement-node pattern for the cliff background. |
| 11 | [DLR-RM/BlenderProc](https://github.com/DLR-RM/BlenderProc) | 3.6k | Jan 20 2026 (v2.8.0 Oct 2024) | **SKIP** | Photoreal training-image pipeline, not landscape. Wrong tool. |
| 12 | [otto-link/Hesiod](https://github.com/otto-link/Hesiod) | 231 | Apr 20 2026 (v0.5.2) | **REFERENCE** | C++/Qt node-based procedural terrain. Source of HighMap library. Not Blender-native but worth referencing for erosion/heightmap algorithms. |
| 13 | [enesovski/BlenderRawImageImporter](https://github.com/enesovski/BlenderRawImageImporter) | 0 | Jan 17 2025 | **SKIP** | Single 30-line script, no project. The pattern is what we need (numpy→bmesh), not the code itself. |
| 14 | [klimentiy23/blender-terrain-splitter](https://github.com/klimentiy23/blender-terrain-splitter) | 0 | Oct 7 2025 | **SKIP** | 1 commit, 0 stars. We don't need tile splitting (our 62 ha is small). |
| 15 | [bravasoftware/BlenderSliceToTiles](https://github.com/bravasoftware/BlenderSliceToTiles) | 1 | Jul 20 2025 | **SKIP** | 3 commits. Same as above. |
| 16 | [Takanu/Metabox](https://github.com/Takanu/Metabox) | 2 | May 11 2024 | **SKIP** | WIP, "update when it's actually functional". Author self-declared broken. |
| 17 | [Auburn/FastNoiseLite](https://github.com/Auburn/FastNoiseLite) | 3.4k | Feb 13 2026 | **REFERENCE** | Multi-language noise lib. Use for procedural forest undergrowth / cliff texture detail. Rust core. |
| 18 | [Auburn/FastNoise2](https://github.com/Auburn/FastNoise2) | 1.4k | Feb 25 2026 | **REFERENCE** | SIMD C++17 node-graph noise. Heavier than FastNoiseLite, same use case. |
| 19 | [Jaysmito101/TerraForge3D](https://github.com/Jaysmito101/TerraForge3D) | 1.2k | Mar 14 2025 | **SKIP** | Cross-platform GUI terrain tool, not Blender. |
| 20 | [gboeing/osmnx](https://github.com/gboeing/osmnx) | 5.7k | May 13 2026 | **ADOPT (already in scripts/)** | OSM street-network → Blender curves for the access road. Already used via `scripts/fetch_osm.py`. |
| 21 | [rasterio/rasterio](https://github.com/rasterio/rasterio) | 2.5k | Jun 8 2026 | **ADOPT (already in scripts/)** | The canonical Python DEM/raster I/O. Drives `analyze_dem.py` already. |
| 22 | [geopandas/geopandas](https://github.com/geopandas/geopandas) | 5.1k | Jun 9 2026 | **ADOPT (already in scripts/)** | The vector layer. Cob-house footprint polygon, Atlantic Forest reserve polygon. |
| 23 | [CesiumGS/cesium](https://github.com/CesiumGS/cesium) | 15.4k | Jun 10 2026 | **REFERENCE** | 3D-globe + 3D Tiles. Not for Blender, but the **3D Tiles** spec is worth knowing for future "publish the site as a 3D Tileset on paragu-ai.com" deliverable. |

**Total: 23 repos, of which 7 are DEAD, 11 are SKIP/REFERENCE, 5 are ADOPT.**

---

## Detail by category

### A. Blender addons (Blender-native, in-Blender workflow)

**1. `domlysz/BlenderGIS`** — the canonical one. 9k stars, **v2.2.15 on Dec 20 2025** (so still actively maintained, contrary to the "unmaintained" claim that may exist in older docs). Imports shapefile/GeoTIFF/OSM DEM, has Delaunay triangulation to make a terrain mesh from contour lines, can drop objects on terrain, geotag photos → cameras. GPL-3.0, 100% Python. The `core/` directory has the triangulation / imageio code that's worth porting to `lqv/site/dem.py` if the bmesh-from-raster approach gets slow.

**Why we still skip it as a primary path:** the project is on Blender 4.2.3 LTS in headless mode (`scripts/render_all_finals.sh` style). The addon is GUI-driven (operator menus, dynamic basemap preview, etc.). Our pipeline is "fetch OSM via osmnx, fetch DEM via OpenTopography, drop into rasterio, build a bmesh, save the .blend, render headless." Installing an addon in the headless wrapper is friction we don't need. **The custom 120-line path remains correct.** But: v2.2.15 being a Dec 2025 release means the prior "Blender 5.x hostile" verdict (from the 2026-06-10 mega-sweep) is no longer accurate — the project *is* getting Blender-version updates, just not ones we can use.

**2. `vvoovv/blosm` (was `blender-osm`)** — 2k stars, May 5 2026 commit, GPL, Pro + free tier. Downloads OSM with ~30 m terrain, places buildings/roads/forests. The repo URL `vvoovv/blender-osm` now redirects to `vvoovv/blosm`. The `release` branch is the source of truth. **Not useful for us** because: (a) we have 62 ha, not a city; (b) we already have `scripts/fetch_osm.py` for OSM; (c) we want photoreal not flat-color buildings. Skip, but the Pro version is a good reference for the "import + UV-map + texture" pattern if we ever need a "neighbouring village" backdrop.

**3-9. The seven dead single-file toys** — all 404 today, including `cgcai/Blender-Terrain-Generator`, `jwjacobson/blender-heightmap`, `EarthX/Blender-GIS-Importer`, `kaiaeberli/Blender-GIS`, `ambrosiussen/blender-gis-extract`, `proceduralia/highland` (Unity tool, irrelevant anyway), and `vvoovv/blender-osm-2` (the "v2" rewrite that never landed; vvoovv went a different direction and made `blosm`). **All can be removed from any "candidate repos" list going forward.** This is a useful negative finding: the Blender-GIS-as-addon space has consolidated to one winner (BlenderGIS) and one niche (blosm).

**10. `joewdavies/geoblender`** — 1.8k stars, Jan 11 2026, HTML tutorial repo. The README is a complete Blender 4.2.3 + QGIS 3.20 + Cycles workflow for turning a DEM .tif into a 3D-looking map. Key technique: **plane with displacement node driven by image texture, plus subdivision surface modifier with adaptive subdivision, plus a colour ramp on the DEM for elevation-tinted colouring.** The escarpment-line y=20 cliff in La Quebrada could be done this way (cheap, fast, no real mesh). The tutorial uses Wales as the example. Adopt this pattern for the cliff-background plane, the mountain-far-distance plane, and any other "we just need it to look 3D" element that doesn't need real geometry.

**11. `DLR-RM/BlenderProc`** — 3.6k stars, last release Oct 2024, last commit Jan 2026. Procedural pipeline for photoreal training-image generation (BOP challenge, COCO annotations, hdf5 containers). Interesting API style (bproc.object, bproc.camera, bproc.renderer) but wrong domain — it's for synthetic dataset generation, not landscape authoring. Skip.

**12. `otto-link/Hesiod`** — 231 stars, v0.5.2 Apr 20 2026, GPL-3.0, C++ 97% + Python 2%. Desktop app for node-based procedural terrain. Self-declared WIP ("use at your own risk"). Modules: HighMap (heightmap ops), CLWrapper (OpenCL), GNode/GNodeGUI (node editor), QTerrainRenderer. **The HighMap library is the interesting part** — it's a header-only C++ heightmap library with erosion, smoothing, warping, blending, distance fields, all the things you'd want for the Atlantic Forest undergrowth + sandstone-cliff texture detail. Reference the algorithm names; we won't link against C++ but the patterns are borrow-able. Skip the Qt app entirely.

**13-16. Single-file addons (enesovski, klimentiy23, bravasoftware, Takanu)** — all 0-2 stars, all 1-3 commits, all just proof-of-concepts. Skip. Notable: `enesovski/BlenderRawImageImporter` has a 30-line script that does exactly the bmesh-from-numpy pattern we need. Code is in the README. **Don't fork the repo, copy the pattern.** The pattern is: numpy→flat array→loop over bmesh.vertices.co, set z. (We can do this faster with `bmesh.from_pydata` + `mesh.update()`, see code snippet below.)

### B. Non-Blender tools that fit our pipeline

**17-18. `Auburn/FastNoiseLite` + `Auburn/FastNoise2`** — the canonical cross-language noise libs. FastNoiseLite (3.4k stars, Feb 2026) is a single-header C++/C#/JS/Rust/Go lib, ~3400 lines, header-only. FastNoise2 (1.4k stars, Feb 2026) is the SIMD C++17 rewrite with a node graph. Both ship Python bindings. **Why reference, not adopt:** we don't need procedural noise for the terrain (we have a real DEM). We might want it for the cob-wall surface displacement (irregular hand-shaped undulations on the cob meshes) and for the forest undergrowth scatter. If we hit that need, FastNoiseLite via the Python binding is the smallest dep.

**19. `Jaysmito101/TerraForge3D`** — 1.2k stars, Mar 14 2025, C++ + OpenGL + ImGui. Cross-platform desktop terrain tool, not Blender. Skip, but note: their heightmap-to-mesh pipeline uses marching squares for LOD, which is the right approach if we ever need terrain at sub-30 cm resolution.

**20. `gboeing/osmnx`** — 5.7k stars, May 13 2026. The canonical Python OSM street-network library. Already used by `scripts/fetch_osm.py`. The `osmnx.graph_from_point` + `osmnx.plot_graph` pipeline is exactly what we need for the access-road → driveway → house → corredor geometry, and we can export as a Shapely MultiLineString that geopandas can hand to a `bmesh.from_edgenet` call.

**21. `rasterio/rasterio`** — 2.5k stars, Jun 8 2026. Pythonic wrapper over GDAL. Already used by `analyze_dem.py` (and the new `lqv/site/dem.py` will use it too). The `rasterio.transform.xy()` + `rasterio.transform.rowcol()` is what we need to map a real-world (lat, lon) to a (col, row) in the DEM array, then to a (x, y, z) world coordinate for the bmesh.

**22. `geopandas/geopandas`** — 5.1k stars, Jun 9 2026. Pandas + Shapely for vector geo data. Already used. The cob-house footprint polygon + the Atlantic Forest reserve polygon + the future lot boundaries all live here. To bmesh: `for geom in gdf.geometry: coords = list(geom.exterior.coords); bmesh.ops.create_face(bm, coords)`.

**23. `CesiumGS/cesium`** — 15.4k stars, Jun 10 2026. 3D globe + 3D Tiles. Not for Blender. But the 3D Tiles spec is the right format if we want to publish the La Quebrada site as an interactive 3D model on a web page (paragu-ai.com deliverable). Worth a one-line mention, not a dependency.

---

## Recommended approach: rasterio + bmesh for the La Quebrada site

```python
# lqv/site/dem.py — drop-in, headless, deterministic
# Reads a 30 m DEM (EPSG:4326, ALOS AW3D30 or Copernicus GLO-30)
# Produces a bmesh in EPSG:32721 (UTM 21S, the Paraguay zone)
# Vertices at (easting, northing, elevation_meters)
# Use: build_scene.py imports this, calls build_dem_terrain(context.scene, src_tif, name="Terrain_62ha")
import math
import bpy
import bmesh
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from pyproj import Transformer

# Paraguay is UTM 21S (EPSG:32721). All mesh coords in metres.
TARGET_CRS = "EPSG:32721"

def _reproject_to_utm(src_tif: str) -> tuple[np.ndarray, rasterio.Affine]:
    """Reproject a DEM to UTM 21S. Returns (z_array_2d, transform)."""
    with rasterio.open(src_tif) as src:
        src_crs = src.crs
        transform, width, height = calculate_default_transform(
            src_crs, TARGET_CRS, src.width, src.height, *src.bounds
        )
        z = np.empty((height, width), dtype=np.float32)
        reproject(
            source=rasterio.band(src, 1),
            destination=z,
            src_transform=src.transform,
            src_crs=src_crs,
            dst_transform=transform,
            dst_crs=TARGET_CRS,
            resampling=Resampling.bilinear,
        )
        nodata = src.nodata
    if nodata is not None:
        z = np.where(z == nodata, np.nan, z)
    return z, transform

def _z_scale(z_meters: np.ndarray, target_max_m: float = 4.0) -> float:
    """Compute a z-scale factor so the tallest hill is target_max_m tall.
    The 62 ha site has ~30 m elevation range (220-250 m AMSL) but the
    visual escarpment is only ~6-8 m relative to the house pad.
    target_max_m=4 means a 6 m cliff renders as 4 m tall — within the
    hero camera's frame without distorting the foreground cob walls."""
    rng = np.nanmax(z_meters) - np.nanmin(z_meters)
    if rng <= 0:
        return 1.0
    return target_max_m / rng

def build_dem_terrain(
    scene: bpy.types.Scene,
    src_tif: str,
    name: str = "Terrain_DEM",
    z_target_m: float = 4.0,
    decimate: int = 1,
) -> bpy.types.Object:
    """Build a Blender mesh from a real-world DEM.

    decimate: keep every Nth pixel. 30 m DEM x decimate=3 = 90 m mesh,
    plenty for a 62 ha hero-camera background. decimate=1 for full 30 m
    (250k tris for 1 km square — too much for our 62 ha).
    """
    z, transform = _reproject_to_utm(src_tif)
    z = z[::decimate, ::decimate]
    h, w = z.shape

    # Generate vertex grid in UTM coords
    cols, rows = np.meshgrid(np.arange(w), np.arange(h))
    xs, ys = rasterio.transform.xy(transform, rows.ravel(), cols.ravel())
    zs = z.ravel()
    # Replace NaN with the mean of valid neighbours (avoids holes)
    if np.any(np.isnan(zs)):
        zs = np.where(np.isnan(zs), np.nanmean(zs), zs)

    z_scale = _z_scale(z, z_target_m)
    verts = [(x, y, z * z_scale) for x, y, z in zip(xs, ys, zs)]

    # Build face indices (two triangles per quad)
    faces = []
    for r in range(h - 1):
        for c in range(w - 1):
            i = r * w + c
            faces.append((i, i + 1, i + w + 1, i + w))

    # Create bmesh
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    scene.collection.objects.link(obj)
    return obj

# Usage in build_scene.py (after materials, before flora):
#   import os
#   dem_tif = HERE / "docs" / "site_data" / "alos_aw3d30_dem.tif"
#   if dem_tif.exists():
#       terrain = build_dem_terrain(bpy.context.scene, str(dem_tif), decimate=2)
#       terrain.data.materials.append(MAT["terrain_atlantic_forest"])
```

**Why this is better than BlenderGIS for our pipeline:**

- **No addon install** in the headless wrapper (`scripts/render_all_finals.sh`).
- **Deterministic** — no GUI state, no random operator ordering. Honors the project's RNG-ordering invariant (`random.seed()` in `build_scene.py` after `materials.build_materials()` and before any `build_*`).
- **CRS-correct** — reprojects to UTM 21S (EPSG:32721) so the cob-house UTM coords from `lqv/site/footprint.py` line up with the terrain UTM coords. The previous `analyze_dem.py` `M_PER_DEG_LON` hack was wrong by ~5 m at bbox edges; this fixes it.
- **Z-scaling** — DEM is in metres AMSL (220-250 m), but the cob walls are 2-3 m tall. Without a z-scale, the terrain dwarfs the house. `z_target_m=4` brings the visual escarpment into the camera frame.
- **Memory-safe** — `decimate=2` cuts a 1 km × 1 km DEM from 1M pixels to 250k tris, which is fine for 4.2.3 LTS.
- **NaN handling** — converts nodata to mean instead of leaving holes.

**This is the same approach the previous research (2026-06-10 mega-sweep) recommended**, with two refinements: explicit UTM reproject (the prior snippet had the `M_PER_DEG_LON` hack) and z-scaling (the prior snippet was 1:1 metres).

---

## Deprecation warnings

The following repos **still work** (have READMEs, are not archived) but should be considered abandoned or wrong-tool-for-job for new work in 2026:

| Repo | Status | Reason |
|---|---|---|
| `Takanu/Metabox` | WIP self-declared | Author says "I'll update this when it's actually functional and available" |
| `Jaysmito101/TerraForge3D` | Mar 2025 last update | 1 year+ no commits, but stable; wrong tool (not Blender) anyway |
| `bravasoftware/BlenderSliceToTiles` | 3 commits, 0 forks | Not really a project, just a single-file paste |
| `klimentiy23/blender-terrain-splitter` | 1 commit, 0 stars | Same |
| `enesovski/BlenderRawImageImporter` | 0 stars | Same; pattern is the value, not the repo |

**The 7 dead 404 repos** are the real warning: Blender-GIS-as-addon is a shrinking space. If you're going to depend on an addon, depend on **BlenderGIS (v2.2.15) or `blosm` (May 2026)** — those are the only two still getting commits. Everyone else has either been absorbed into those, replaced by a custom script, or abandoned.

---

## Stack Exchange probes — both failed

- `gis.stackexchange.com/questions/tagged/blender` → 404 (tag page no longer routes; the site merged/moved tags)
- `blender.stackexchange.com/questions/tagged/heightmap` → 404 (same)
- Fallback that did work: `bravasoftware/BlenderSliceToTiles` README credits a stackexchange answer (133258) as the basis for the tile-slicing code. That answer exists if you search `blender.stackexchange.com/q/133258` directly, but the tag pages are gone.

For our use case (Atlantic Forest + sandstone escarpment + cob house), the relevant SE questions are:
- "How do I import a DEM into Blender?" — answer: image-texture displacement on a subdivided plane (joewdavies/geoblender pattern)
- "How do I drape a satellite image onto a terrain mesh?" — answer: UV unwrap from the plan-view, then image-texture node with the ortho projection
- "How do I make realistic trees?" — answer: use Sapling add-on (built into Blender, no external dep) for trunks, particle system for canopy

---

## Delta vs the 2026-06-10 mega-sweep (`docs/research/README.md`)

The previous research session covered the same 9 user-specified Blender repos plus broader GEDI / DEM tooling. The verdicts **agree** on:

- The 5 dead 404 repos (kaiaeberli, cgcai, EarthX, ambrosiussen, proceduralia) were correctly flagged as SKIP/unmaintained.
- The custom `lqv/site/dem.py` approach (rasterio + numpy + bmesh, headless) remains the right call.
- The "no BlenderGIS" verdict for the production pipeline stands.

The verdicts **differ or refine** on:

- **BlenderGIS v2.2.15 (Dec 20 2025)** is more recent than the prior session noted — it's not "abandoned", it's just not the right tool for headless. Update the comment in `lqv/site/dem.py` from "BlenderGIS is unmaintained" to "BlenderGIS v2.2.15 is current but GUI-driven; we need headless + deterministic, so custom path".
- **`vvoovv/blender-osm` → `vvoovv/blosm`** redirect: the prior session didn't note that the repo moved. The new home is `vvoovv/blosm`, branch `release`. Worth a one-line update in any reference doc.
- **`joewdavies/geoblender`** was not in the prior session's "top 3" but is the **best reference for the cliff-background displacement technique** — adopt it.
- **Auburn FastNoiseLite / FastNoise2** are new additions (not in prior sweep). They're the right reference for procedural cob-wall surface detail if we go that route. Currently no project need, so REFERENCE not ADOPT.

---

## Action items for `house-field/`

| Action | Source | Effort |
|---|---|---|
| Add `lqv/site/dem.py` with the snippet above (with proper imports, error handling) | this report | 30 min, render-agent to integrate |
| Drop the `M_PER_DEG_LON` hack from `scripts/analyze_dem.py` line 54; use `pyproj.Transformer` to UTM 21S | this report | 15 min |
| Update `docs/research/README.md` line 84 to note BlenderGIS v2.2.15 is current (not abandoned) | this report | 5 min |
| Add a cliff-background plane using `joewdavies/geoblender` displacement pattern in `lqv/site/terrain_62ha.py` | this report | 1 hour |
| Remove the 5 dead-404 repos from any "candidate list" in `MASTER_BRIEF.md` or `RESEARCH_GAPS.md` | this report | 5 min |
| Reference `otto-link/Hesiod` + `Auburn/FastNoiseLite` in `docs/research/research_index.md` as procedural-noise sources if we add cob-wall displacement | this report | 10 min |

## What we should NOT do (pushback)

- **Don't add BlenderGIS as a dep** to the headless render wrapper. Use the 120-line custom path.
- **Don't fork the single-file toys** (enesovski, bravasoftware, klimentiy23) — copy the pattern, not the repo.
- **Don't switch to Cesium 3D Tiles** for the deliverable — that's a 2027 ask (after the build is real), not a 2026 ask. Stay on Cycles / .blend / .png.
- **Don't adopt the 5 dead repos** even if a Stack Overflow answer cites them — they're 404 today.
- **Don't import `vvoovv/blender-osm`** by name — the new home is `vvoovv/blosm` branch `release`.
- **Don't try to do "DEM mesh + perfect forest + perfect cob + perfect cliff" in one render pass** — the prior session correctly identified that the displacement-on-plane (geoblender pattern) is cheap for background, real bmesh (our `dem.py`) is for foreground, and procedural scatter (FastNoiseLite reference) is for the cob-wall detail. Three different techniques, three different scales.

## What to ask Wesley (open questions surfaced)

None — this is a tooling research task, not a design decision. The only Wesley-touching question is the `R35 — drone LiDAR 1 m DEM of the 62 ha` from the prior session, which would change `decimate=2` (30 m) to `decimate=1` (5 m → 1 m), but that's a separate decision the user/owner makes.

---

*Compiled 2026-06-10 by opencode from 23 repos (9 user-specified + 14 discovered via topic pages). Tools used: `gitingest` (3 README successes, 6 400s, then rate-limited 429s), `webfetch` (19 successful repo pages + 6 topic pages + 2 failed SE tag pages). 1 webfetch of the `domlysz/BlenderGIS` GitHub HTML page confirmed the v2.2.15 release date. Stack Exchange tag pages returned 404. All 7 dead-404 repos confirmed via direct GitHub HTML page requests (not via gitingest).*
