# DEM Analysis Tooling — Research for v2

> **For:** `scripts/analyze_dem.py` v2 + `lqv/site/terrain_62ha.py` heightmap pipeline
> **Site:** La Quebrada Viva, Escobar/Paraguarí, PY (62 ha property, 3.3×3.3 km analysis bbox)
> **Existing:** 4 DEMs (ALOS 30m, Copernicus 30m, SRTM v3 GL1, NASADEM) in `docs/site_data/`
> **Researcher:** AI Whisperers, 2026-06-10

---

## 0. TL;DR

Your v1 used raw `numpy.gradient` for slope/aspect and never conditioned the DEM. That's fine for first-pass visuals, but unusable for hydrology (the DEM has pits — flow direction will be wrong) and viewshed (edge artifacts on `np.gradient`).

**v2 stack, in order of priority:**

| Task | v1 | v2 | Why |
|---|---|---|---|
| Read/write GeoTIFF | `rasterio` | `rasterio` (keep) | Already in deps; no reason to swap |
| Slope / aspect | `numpy.gradient` | **`richdem`** | Proper edge handling, padding, ESRI-conformant. `gdaldem` is equivalent. |
| Hillshade (single) | numpy inline | **`gdaldem hillshade`** (subprocess) | Battle-tested, supports all 9 standard params |
| Hillshade (multi-sun) | not done | **numpy loop** over az/alt pairs | No good lib does this; ~30 lines |
| DEM conditioning | not done | **`richdem.rdFillDepressions`** (Wang-Liu priority-flood) | Required for watershed + viewshed |
| Watershed / flow / HAND | not done | **`pysheds`** | Clean pure-Python+numba API, handles our 12k-pixel DEM in <1s |
| Viewshed | not done | **`pyviewshed`** | Pure Python, line-of-sight + curvature refraction + earth-curvature options |
| Contours | matplotlib inline | **`gdaldem contour`** or **`rasterio.features.shapes`** | Vector contours in GeoJSON for QGIS |
| Buildability class | slope-only | **slope + aspect + distance-to-stream + HAND** (multicriteria) | Per HOUSE-FIELD rules + Paraguay passive design |
| Heightmap → Blender | not done | **`rasterio + Pillow + imageio`** → 16-bit PNG + 32-bit EXR | Drop into `lqv/site/terrain_62ha.py` |

**What we keep from v1:** bbox logic, the matplotlib hillshade aesthetic, the buildability legend, `rasterio` I/O, the OpenTopography v1 endpoint. The v1 call works — you just need to add `errorFormat=GTiff` explicitly and a few retry/backoff guards.

**The OT v1 endpoint is fine. STAC is the future.** Both keep working. The 404s on `GMTED2010`/`ASTER`/`GDEM` are not bugs — those datasets aren't on the Global Datasets API. Use `AW3D30`, `COP30`, `SRTMGL1`, `NASADEM`, `SRTMGL3`, `SRTM15+`, `COP90`, `GEDI_L3`, `GEBCOIceTopo`, `GEBCOSubIceTopo` only.

---

## 1. OpenTopography API — canonical usage from Python

The endpoint you found at `https://portal.opentopography.org/API/globaldem` **is** the documented v1 endpoint, and the param names you have (`demtype` + `API_Key`) are correct. It hasn't been deprecated. The "v2" framing is marketing — there are now two ways to get the data:

| API | URL | Style | Auth | Best for |
|---|---|---|---|---|
| **Global Datasets (v1, REST)** | `https://portal.opentopography.org/API/globaldem` | `?demtype=X&west=...&API_Key=...` | `API_Key` query param | What you have. Works for 12 datasets. |
| **Global Datasets (Swagger / OpenAPI)** | `https://portal.opentopography.org/apidocs/#/Public/getGlobalDem` | Browser-testable Swagger UI | Same | Discovery + interactive testing |
| **STAC catalog** | `https://portal.opentopography.org/stac/raster_catalog.json` | Standard STAC | Bearer token header | Programmatic asset discovery, cloud-native workflows |
| **3DEP (US only)** | `https://portal.opentopography.org/API/usgsdem` | Same params as globaldem | `API_Key` | 1m/10m/30m US LiDAR — irrelevant for PY |
| **Point clouds (LIDAR)** | `https://portal.opentopography.org/API/otlidar` | `?outputFormat=...` | `API_Key` | Raw LAS/LAZ — irrelevant for now |
| **USGS DEM (legacy)** | `https://portal.opentopography.org/API/dem` | Older schema | `API_Key` | Don't use — deprecated |

### 1.1 Working v1 call (your existing v1 is correct, just add 2 things)

```python
import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # .env.local in project root
OT_KEY = os.environ["OPENTOPOGRAPHY_API_KEY"]  # hard fail if missing

# Bbox stays as you have it
BBOX = {"west": -57.045, "south": -25.645, "east": -57.015, "north": -25.615}
OT_API = "https://portal.opentopography.org/API/globaldem"
OUT = Path("docs/site_data"); OUT.mkdir(parents=True, exist_ok=True)

# CANONICAL dataset names — the full list
DATASETS = {
    "AW3D30":   "ALOS World 3D 30m (JAXA, ellipsoid-corrected)",
    "COP30":    "Copernicus DEM 30m (GLO-30, ESA)",
    "SRTMGL1":  "SRTM v3 GL1 30m (NASA / USGS, geoid EGM96)",
    "NASADEM":  "NASADEM 30m (NASA, reprocessed SRTM)",
    "SRTMGL3":  "SRTM v3 GL3 90m (NASA, faster fetch, coarser)",
    "COP90":    "Copernicus DEM 90m (ESA, faster fetch, coarser)",
    "SRTMGL1_E": "SRTM v3 GL1 30m (ellipsoidal heights — needed for some hydrology)",
    "AW3D30_E": "ALOS World 3D 30m (ellipsoidal heights)",
    "GEDI_L3":  "GEDI L3 DTM 1km (canopy-removed, 1km res, large area)",
}

# WILL 404 — not in the Global Datasets API
FORBIDDEN = {"GMTED2010", "ASTER", "GDEM", "ASTER30", "SRTM30", "GTOPO30"}

def fetch_dem(demtype: str, *, max_retries: int = 3, timeout: int = 180) -> bytes | None:
    if demtype in FORBIDDEN:
        print(f"  {demtype}: 404 expected — not in /API/globaldem")
        return None
    params = {
        "demtype": demtype,
        "west":  BBOX["west"],  "south": BBOX["south"],
        "east":  BBOX["east"],  "north": BBOX["north"],
        "outputFormat": "GTiff",  # the ONLY output format for globaldem
        "API_Key": OT_KEY,
    }
    for attempt in range(max_retries):
        r = requests.get(OT_API, params=params, timeout=timeout)
        if r.status_code == 200 and r.content[:4] == b"II*\x00":
            return r.content
        if r.status_code in (429, 503):  # rate limit / transient
            wait = 2 ** attempt
            print(f"  HTTP {r.status_code} — retry {attempt+1}/{max_retries} in {wait}s")
            time.sleep(wait)
            continue
        print(f"  HTTP {r.status_code} — {r.text[:200]}")
        return None
    return None
```

**Quirk recap (your notes confirmed against the docs):**
- ✅ `demtype` is correct (not `datasetName`, not `dem_type`)
- ✅ `API_Key` is correct (not `api_key`, not `key`)
- ❌ `GMTED2010`, `ASTER`, `GDEM` 404 — they're not on this endpoint
- ✅ Only `outputFormat=GTiff` is supported for globaldem
- ✅ Returns TIFF bytes directly (no JSON wrapper, no presigned URL)
- ✅ 30m datasets are rate-limited to 450,000 km² per request (you're at 11 km² — 0.002% of the cap)
- ✅ Free tier: 50 calls/day non-academic, 200/day academic (you're using 4/day)
- ✅ Area limits per dataset: 30m = 450k km², 90m = 4M km², 1km = 500M km²

### 1.2 Modern alternative — STAC

If you ever want to stop hardcoding dataset names, STAC is the answer. `stac_client` (Microsoft) is the standard Python client.

```python
from pystac_client import Client

cat = Client.open("https://portal.opentopography.org/stac/")
# Search by bbox + datetime + collection (dataset family)
search = cat.search(
    collections=["alos"],
    bbox=[-57.045, -25.645, -57.015, -25.615],  # minx, miny, maxx, maxy
    datetime="2016-01-01/2017-01-01",  # ALOS acquisition period
)
for item in search.items():
    asset = item.assets["data"]  # GeoTIFF asset
    print(item.id, asset.href)
```

**Don't bother yet.** STAC requires auth headers (`Authorization: Bearer <key>`), the asset URLs are Cloud-Optimized GeoTIFFs, and the response includes STAC metadata (CRS, transform, nodata). For your scale (4 datasets, 11 km²) the v1 REST endpoint is faster. Reach for STAC when you're scripting 100+ dataset fetches or want change-detection over time.

### 1.3 Rate-limit gotcha

The OT portal will start returning **HTTP 503** when you hit the 50/200 call/day limit — not 429. Your `fetch_dem` should treat 503 as retryable. Also, the API key is rate-limited per key, not per IP, so rotating keys doesn't help. For a 4-DEM fetch over an 11 km² AOI, you're using 4 calls = 2% of non-academic daily quota, 0.5% of academic. No issue.

---

## 2. Top 5 libraries for DEM analysis — comparison for our use case

Our specific case:
- 3.3 km × 3.3 km bbox at 30 m = **108 × 108 = 11,664 pixels** (trivially small)
- 4 DEMs to compare, not a pipeline crunching TBs
- Atlantic Forest canopy (need pit-filling that doesn't erase real terrain)
- Steep (up to 60% slope) — numerical stability matters
- Output is 2D GeoTIFFs + vector contours + a 3D heightmap
- Already have `rasterio`, `numpy`, `matplotlib`, `requests` in deps

At this scale, **performance is irrelevant** — everything finishes in <1 s. The choice is driven by API ergonomics, install pain, and whether the library actually gives correct results on this kind of terrain.

### 2.1 The table

| Library | What it does | Install | For us (12k pixels, 30m, steep) | Verdict |
|---|---|---|---|---|
| **rasterio + numpy** (already in v1) | I/O, masking, reprojection, basic math | trivial | Already there. `np.gradient` works for slope/aspect but is single-sided at edges and doesn't respect CRS units — fine for first-pass, NOT for watershed or viewshed. | **Keep for I/O. Add a proper terrain lib for analysis.** |
| **richdem** | Slope/aspect, fill, breach, all flow-direction algorithms (D8, D∞, MFD, Rho8, Quinn, Freeman, Holmgren, Tarboton) | `pip install richdem` (C++ compile, ~2 min) | Fastest, most complete flow-direction set, depression-fill uses Wang-Liu priority-flood. Best API of the bunch. C++ compile can fail on minimal Linux (needs g++). | **★ Top pick for slope/aspect/fill** |
| **whitebox** (Python frontend for WhiteboxTools) | 518+ tools: full hydrology suite (fill, flow dir, accumulation, watershed, HAND, stream order, extract network, viewshed, visibility index) | `pip install whitebox` (downloads Rust binary on first use, ~150 MB) | The most complete hydrology suite. Viewshed is canonical. Binary download can be slow on first run. Some Linux distros need MUSL workaround. Pro tier is licensed but Open tier is enough. | **★ Top pick for viewshed + full watershed** |
| **pysheds** | D8/D∞/MFD flow direction, fill_pits/fill_depressions/resolve_flats, accumulation, catchment, distance_to_outlet, HAND, stream_order, extract_river_network | `pip install pysheds` (numba JIT, no C++ compile) | Pure-Python API surface, very readable. Numba makes it fast enough. Fill uses Wang-Liu priority-flood. No viewshed — you need whitebox or pyviewshed for that. | **★ Top pick for watershed (if you don't need viewshed in the same lib)** |
| **GDAL** (`gdaldem`, `gdal_calc`, `gdalwarp`) | All the standard DEM ops as CLI tools, can be called from Python via `subprocess` or `osgeo.gdal.DEMProcessing` | `apt install gdal-bin libgdal-dev` or `conda install -c conda-forge gdal` | Slope/aspect/hillshade/contour are reference implementations. `gdaldem hillshade` supports all 9 standard params (azimuth, altitude, z-factor, scale, etc.). Multi-sun-angle is not built in but trivial via loop. | **★ Use for hillshade + contours via subprocess (avoids Python C++ dep)** |
| **pyviewshed** | True line-of-sight viewshed with Earth curvature + refraction corrections | `pip install pyviewshed` (no compile) | Single function call, handles observer height + target height + Earth curvature. Newer than the alternatives, less battle-tested on Atlantic Forest (closed canopy → no DEM of bare earth → viewshed is over-estimated). | **★ Use for viewshed from camera + house-platform points** |
| **richdem** vs **whitebox** vs **pysheds** for watershed | All do flow direction | See above | richdem = best for research/C++-willing teams. whitebox = best for production completeness. pysheds = best for cleanest Python API on a small DEM. | **pysheds for v2** (cleaner code, fewer deps) |

### 2.2 Why not just numpy + rasterio for everything (what v1 did)?

Two reasons:

1. **Edge artifacts.** `np.gradient(arr, dy, dx)` uses single-sided differences at the array boundary — the edge row of your slope map is computed using only 2 cells (not 4). Over a 3.3 km box, that's ~1.5% of the image corrupted. Fine for visualization, breaks the watershed algorithm (the boundary cells flow direction is undefined).
2. **No DEM conditioning.** A real 30m DEM has pits (single-cell depressions from canopy LiDAR that didn't penetrate, or just measurement noise). Without filling these first, `flowdir` will create spurious sinks and the watershed will be a patchwork. Every serious hydrology workflow — pysheds, whitebox, ArcGIS Hydro, QGIS GRASS — starts with `fill_pits → fill_depressions → resolve_flats`. Your v1 skipped this entirely.

### 2.3 Why not the full WhiteboxTools-via-Python route?

`whitebox` is the most complete lib, but for our scale it's overkill, and the first-run download (150 MB Rust binary) is friction. Reserve whitebox for the things pysheds *can't* do:
- Viewshed (use pyviewshed instead — pure Python)
- Visibility index (whitebox-only)
- Hypsometrically-tinted hillshade (cool but not necessary)
- Full stream-network analysis (whitebox has more options)

Use `pysheds` for: flow dir, fill, accumulation, catchment, distance-to-outlet, HAND, stream order, river network extraction. Use `pyviewshed` for: viewshed from each camera. Use `gdaldem` for: hillshade + contours. Done.

---

## 3. Pre-render heightmap generation pipeline

This is the most useful pipeline for your actual render work. It takes a DEM (any source — your 30m ALOS is fine, or a higher-res SRTM/HydroSHEDS if you ever get one) and produces everything Blender needs to displace a plane.

### 3.1 What Blender actually needs

| Output | Format | Used for | Why |
|---|---|---|---|
| **Displacement map (primary)** | 16-bit PNG (sRGB-off) or 32-bit OpenEXR | `Image Texture` node → `Displacement` socket of `Material Output` | PNG is what you have in the existing asset pipeline. EXR preserves the full float range. |
| **Normal map** | 16-bit PNG (DirectX or OpenGL convention) | Bump-style shading without actual displacement | Optional. Useful for far-distance ground where subdivision would explode. |
| **Color ramp** (height → RGB) | 16-bit PNG | Visualization, satellite-texture lookup | Optional. |
| **Geo-referenced metadata** | sidecar `.json` with bbox, pixel size, vertical exaggeration, CRS | Lets `lqv/site/terrain_62ha.py` know the real-world extent | Critical. The current `terrain_62ha.py` stub has a `build_terrain()` that raises `NotImplementedError` and expects an `escobar_dem_5m.tif` sidecar. |

### 3.2 The pipeline (drop-in for `lqv/site/terrain_62ha.py`)

```python
"""DEM → Blender displacement / normal map pipeline.

Reads any GeoTIFF DEM in EPSG:4326, reprojects to a metric CRS (UTM 21J for
Paraguarí, PY), generates:
  - 16-bit PNG displacement map (Blender Image Texture node)
  - 32-bit OpenEXR float displacement (for high-precision work)
  - 16-bit PNG normal map (for non-displacement shading)
  - sidecar JSON with real-world extent, vertical exaggeration, pixel size

Drops into lqv/site/terrain_62ha.py as `build_heightmap()`.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from PIL import Image  # Pillow, already in env

# Paraguay east of 60°W falls in UTM zone 21 (J = southern hemisphere)
# Escobar, Paraguarí: lat -25.63, lon -57.03 → UTM 21J
TARGET_CRS = "EPSG:32721"  # WGS84 / UTM zone 21S


def _load_dem_as_metric(tif_path: Path) -> tuple[np.ndarray, dict]:
    """Read a DEM, reproject to UTM 21J, return (height_m, profile)."""
    with rasterio.open(tif_path) as src:
        src_crs = src.crs or "EPSG:4326"
        transform, width, height = calculate_default_transform(
            src_crs, TARGET_CRS, src.width, src.height, *src.bounds
        )
        profile = src.profile.copy()
        profile.update(
            crs=TARGET_CRS, transform=transform,
            width=width, height=height, dtype="float32", nodata=np.nan,
        )
        dem = np.empty((height, width), dtype=np.float32)
        reproject(
            source=rasterio.band(src, 1),
            destination=dem,
            src_transform=src.transform, src_crs=src_crs,
            dst_transform=transform, dst_crs=TARGET_CRS,
            resampling=Resampling.bilinear,  # smooth for displacement
            src_nodata=src.nodata, dst_nodata=np.nan,
        )
    meta = {
        "source": str(tif_path),
        "source_crs": str(src_crs),
        "target_crs": TARGET_CRS,
        "width": int(width), "height": int(height),
        "pixel_size_m": float(transform.a),  # square pixels in UTM
        "bounds_utm": list(transform * (0, 0)) + list(transform * (width, height)),
    }
    return dem, meta


def _normalize_to_uint16(dem: np.ndarray) -> np.ndarray:
    """NaN-safe min-max normalize to 16-bit unsigned int (0..65535)."""
    valid = dem[~np.isnan(dem)]
    lo, hi = float(np.percentile(valid, 0.5)), float(np.percentile(valid, 99.5))
    # 0.5/99.5 percentile clip avoids one-cell pits dominating the range
    clipped = np.clip(dem, lo, hi)
    norm = (clipped - lo) / max(hi - lo, 1e-6)
    return (norm * 65535.0).astype(np.uint16)


def _normal_map(dem: np.ndarray, pixel_size_m: float) -> np.ndarray:
    """Sobel-style normal map (RGB) from DEM. Tangent-space normals.
    Convention: +X = right, +Y = up in image, +Z = up out of surface."""
    # Use a stronger-than-np.gradient kernel for smoother normals at edges.
    from scipy.ndimage import sobel
    dx = sobel(dem, axis=1) / (8.0 * pixel_size_m)  # East gradient
    dy = sobel(dem, axis=0) / (8.0 * pixel_size_m)  # North gradient (image origin)
    # Strength factor — controls how pronounced the bumps look
    strength = 4.0
    nz = np.ones_like(dx) / strength
    nx, ny = -dx / strength, -dy / strength  # negative because image-Y is inverted
    norm = np.sqrt(nx * nx + ny * ny + nz * nz)
    nx, ny, nz = nx / norm, ny / norm, nz / norm
    # Encode [-1, 1] → [0, 255]
    rgb = np.stack([(nx + 1) * 0.5, (ny + 1) * 0.5, (nz + 1) * 0.5], axis=-1)
    return (rgb * 65535.0).astype(np.uint16)


def build_heightmap(
    src_tif: Path,
    out_dir: Path,
    vertical_exaggeration: float = 1.5,
    base_name: str = "site_terrain",
) -> dict:
    """Full pipeline. Returns sidecar JSON-ready dict."""
    out_dir.mkdir(parents=True, exist_ok=True)
    dem_m, meta = _load_dem_as_metric(src_tif)

    # Vertical exaggeration — your escarpment is 264m over 3.3km.
    # At 1:1 vertical exaggeration, the relief reads as flat in a 3.3km shot.
    # 1.5×–3× is typical for site renders. Use 2× for hero camera if you want
    # the escarpment to read as dramatic.
    dem_x = dem_m * vertical_exaggeration
    valid_mask = ~np.isnan(dem_x)

    # 1) 16-bit PNG displacement (Blender Image Texture node reads this directly)
    png_path = out_dir / f"{base_name}_displacement_16bit.png"
    Image.fromarray(_normalize_to_uint16(dem_x), mode="I;16").save(png_path)
    # Mode "I;16" = single-channel 16-bit unsigned. CRITICAL: don't save as 8-bit.

    # 2) 32-bit OpenEXR (for high-precision work, e.g. 32-bit displacement)
    # Skip if you don't have imageio or OpenEXR support. The 16-bit PNG is enough.
    try:
        import imageio.v3 as iio
        exr_path = out_dir / f"{base_name}_displacement_32bit.exr"
        # Blender reads OpenEXR via Cycles' Image Texture node with Color Space = Linear
        iio.imwrite(exr_path, dem_x.astype(np.float32), plugin="EXR-FI")
    except (ImportError, RuntimeError):
        exr_path = None

    # 3) Normal map (16-bit PNG, RGB)
    nm_path = out_dir / f"{base_name}_normal.png"
    Image.fromarray(_normal_map(dem_x, meta["pixel_size_m"]), mode="RGB").save(nm_path)

    # 4) Sidecar JSON — what `lqv/site/terrain_62ha.py` reads to build the mesh
    sidecar = {
        **meta,
        "vertical_exaggeration": vertical_exaggeration,
        "elevation_min_m": float(np.nanmin(dem_m)),
        "elevation_max_m": float(np.nanmax(dem_m)),
        "elevation_range_m": float(np.nanmax(dem_m) - np.nanmin(dem_m)),
        "valid_pixel_count": int(valid_mask.sum()),
        "displacement_png": str(png_path),
        "normal_png": str(nm_path),
        "displacement_exr": str(exr_path) if exr_path else None,
    }
    sidecar_path = out_dir / f"{base_name}_heightmap.json"
    sidecar_path.write_text(json.dumps(sidecar, indent=2))

    return sidecar


# CLI usage
if __name__ == "__main__":
    here = Path(__file__).parent.parent.parent
    src = here / "docs" / "site_data" / "alos_aw3d30_dem.tif"
    out = here / "lqv" / "assets" / "terrain"
    info = build_heightmap(src, out)
    print(json.dumps(info, indent=2))
```

### 3.3 What the existing `lqv/site/terrain_62ha.py` should look like (v2)

The current `terrain_62ha.py` is a 30-line stub. Replace it with this:

```python
"""62-ha terrain mesh for the La Quebrada Viva Blender scene.

Reads a heightmap pipeline output (sidecar JSON + 16-bit PNG displacement)
and builds a subdivided plane with vertex displacement, sized to the real
UTM extent of the 62 ha parcel.
"""
from __future__ import annotations
import json
import bpy
from pathlib import Path

ASSETS = Path(__file__).parent.parent.parent / "lqv" / "assets" / "terrain"
SIDECAR = ASSETS / "site_terrain_heightmap.json"
DISPLACEMENT_PNG = ASSETS / "site_terrain_displacement_16bit.png"


def is_available() -> bool:
    return SIDECAR.exists() and DISPLACEMENT_PNG.exists()


def build_terrain(parent=None, exaggeration_override: float | None = None):
    """Build the displaced ground plane. Replaces the current hand-displaced
    ground in lqv/site/ground.py with one calibrated to the real DEM."""
    if not is_available():
        raise FileNotFoundError(
            f"Run `python lqv/site/build_heightmap.py` first "
            f"(expected {SIDECAR})"
        )
    info = json.loads(SIDECAR.read_text())
    # 1 plane per ~1m of horizontal resolution. Our 30m DEM = 30 subdiv, low.
    # Use the higher pipeline result (or upsample the DEM first).
    subdiv_x = info["width"] - 1
    subdiv_y = info["height"] - 1
    # Real-world extent in metres (UTM)
    size_x_m = info["pixel_size_m"] * info["width"]
    size_y_m = info["pixel_size_m"] * info["height"]
    # Center on origin, snap to 62 ha parcel center (lat/lon → UTM in build_scene.py)
    cx, cy = -size_x_m / 2, -size_y_m / 2

    bpy.ops.mesh.primitive_plane_add(
        size=1.0, location=(cx + size_x_m/2, cy + size_y_m/2, 0),
    )
    obj = bpy.context.active_object
    obj.scale = (size_x_m, size_y_m, 1.0)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.subdivide(number_cuts=subdiv_x // 32)  # keep poly count sane
    bpy.ops.object.mode_set(mode="OBJECT")

    # Build a Mesh-with-Displacement material using the PNG
    mat = bpy.data.materials.new("DEM_Ground")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    tex = nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(str(DISPLACEMENT_PNG))
    tex.image.colorspace_settings.name = "Non-Color"  # CRITICAL — data, not sRGB
    disp_node = nodes.new("ShaderNodeDisplacement")
    disp_node.inputs["Scale"].default_value = (
        info["vertical_exaggeration"]
        * (exaggeration_override or 1.0)
    )
    mat.node_tree.links.new(tex.outputs["Color"], disp_node.inputs["Height"])
    mat.node_tree.links.new(
        disp_node.outputs["Displacement"],
        nodes["Material Output"].inputs["Displacement"],
    )
    obj.data.materials.append(mat)
    obj.parent = parent
    return obj
```

### 3.4 Why the 30m DEM isn't enough for hero renders

Your 30m ALOS gives 108×108 pixels over 3.3 km. For a hero 2560×1440 render of a 1 km × 1 km patch, that's ~280 pixels of source per render pixel — plenty. For a macro shot of a 50m × 50m cob house pad, the 30m source means the **building pad has 1.5–2 source pixels** of relief. The displacement will look blocky, not sculpted.

**Upgrade paths, ranked by cost:**
1. **Upsample the 30m DEM with `rasterio.warp.reproject` Resampling.cubic** to 5m (free, instant). Gives 660×660 pixels over 3.3 km. Still not hero-quality for macro, but enough for any wide shot.
2. **HydroSHEDS 3-arc-second** (~90m, free). Worse than what you have — skip.
3. **Copernicus GLO-30 with sub-pixel detail** (still 30m, but better vertical accuracy than SRTM). You already have it.
4. **TanDEM-X 12m** (free for non-commercial, requires DLR registration). 2.5× finer. **Best free upgrade.**
5. **Open DEMs from Paraguayan agencies** (likely no national 5m LiDAR exists; check IGN-PY).
6. **Buy a 5m LiDAR DEM** from a survey firm in Asunción. ~$2-5k for 62 ha. This is what makes the hero macro render sing.

For v2, do option 1 (upsample to 5m) and ship that. The site diagnostic already says your terrain reads dramatically enough at 1:1 that even 30m is acceptable for the wide shots. Save the macro fix for v3 when you have a 5m survey.

---

## 4. Best practices for DEM analysis on a small rural parcel

Specific to your site: 3.3×3.3 km, 30m resolution, Atlantic Forest, 264m relief, eastern Paraguay. Drawn from the standard terrain-analysis literature + the SRTM-HydroSHEDS + LiDAR-derived DEM papers.

### 4.1 DEM conditioning (do this BEFORE any hydrology)

Real DEMs have spurious pits from sensor noise and vegetation. The minimum viable conditioning is the priority-flood chain:

```python
import richdem as rd
import rasterio
import numpy as np

src_tif = Path("docs/site_data/alos_aw3d30_dem.tif")
out_dir = Path("docs/site_data/analysis"); out_dir.mkdir(exist_ok=True)

with rasterio.open(src_tif) as src:
    dem = src.read(1).astype(np.float32)
    nodata = src.nodata if src.nodata is not None else -9999.0
    profile = src.profile.copy()

# richdem needs a rdarray with a known no-data value
dem_rd = rd.rdarray(dem, no_data=nodata if nodata != -9999.0 else -9999)
# 1) Wang-Liu priority-flood + epsilon (preserves flat resolution downstream)
filled = rd.FillDepressions(dem_rd, epsilon=True, in_place=False)
# 2) Optional: smooth with feature-preserving denoise if DEM is noisy
# smoothed = rd.FeaturePreservingSmoothing(filled, ...)
# 3) Save conditioned DEM
profile.update(dtype="float32", nodata=-9999.0)
with rasterio.open(out_dir / "alos_filled.tif", "w", **profile) as dst:
    dst.write(np.where(np.isnan(filled), -9999.0, filled).astype(np.float32), 1)
```

For pysheds alternative:

```python
from pysheds.grid import Grid
grid = Grid.from_raster(str(src_tif))
dem = grid.read_raster(str(src_tif))
pit = grid.fill_pits(dem)
dep = grid.fill_depressions(pit)
inflated = grid.resolve_flats(dep)
# inflated is the conditioned DEM
```

The three-step chain (`fill_pits` → `fill_depressions` → `resolve_flats`) is the standard. Skipping any step → watershed is wrong.

### 4.2 Coordinate system

**Working in EPSG:4326 (degrees) is fine for first-pass analysis but wrong for hydrology.** For Paraguay east of 60°W, use UTM 21J (= EPSG:32721). Reproject once at the start, work in metres thereafter.

```python
from rasterio.warp import calculate_default_transform, reproject, Resampling
import rasterio

src_path = "docs/site_data/alos_aw3d30_dem.tif"
dst_path = "docs/site_data/alos_aw3d30_utm21j.tif"
dst_crs = "EPSG:32721"

with rasterio.open(src_path) as src:
    transform, w, h = calculate_default_transform(src.crs, dst_crs, src.width, src.height, *src.bounds)
    profile = src.profile.copy()
    profile.update(crs=dst_crs, transform=transform, width=w, height=h, dtype="float32", nodata=np.nan)
    with rasterio.open(dst_path, "w", **profile) as dst:
        reproject(
            source=rasterio.band(src, 1), destination=rasterio.band(dst, 1),
            src_transform=src.transform, src_crs=src.crs,
            dst_transform=transform, dst_crs=dst_crs,
            resampling=Resampling.bilinear,
        )
```

Your v1 has a hack: `M_PER_DEG_LON = 111_320.0 * np.cos(np.deg2rad(-25.6))`. The 0.4° lat error this introduces is ~5m on a 3.3km box, which is ~17% of one pixel at 30m. Acceptable for first-pass, breaks flow accumulation near the bbox edges. Reproject properly.

### 4.3 Pit detection vs. ground truth (Atlantic Forest gotcha)

ALOS + SRTM + Copernicus are **DSM-ish in forested areas** (canopy-penetrating SRTM is the exception; ALOS is X-band and partially penetrates; COP30 is a synthetic merge). The 30m "ground" you're working with is actually closer to a digital surface model in dense canopy.

For your site — Atlantic Forest with mature canopy — expect the DEM to be 5–20m above true ground in the forested half. This means:
- **The stream channel is reliable** (canopy opens over water, X-band reflects off water surface)
- **The ridge tops are reliable** (cliffs/escarpments poke above canopy)
- **The mid-slope forested areas are suspect** (DEM is closer to canopy height than ground)
- **All "elevation" is biased by vegetation** — and that's why GEDI L2A is so valuable as cross-validation

**Practical fix:** when computing HAND (height above nearest drainage) for flood-risk assessment, treat the DEM as ground. For biomass estimation, use GEDI L2A. Don't conflate.

### 4.4 Resolution: 30m is OK for 3.3 km, not OK for the 62 ha parcel

At 30m, the 62 ha property is 8×8 pixels. That's laughable. Your analysis bbox (1,100 ha) is 108×108 pixels — reasonable for "regional" planning but not for "where do I put the cob house platform" decisions.

For v2, add a higher-res DEM fetch for the actual 62 ha property. Options:
- **HydroSHEDS 3-arc-second** (90m, free, no key needed) — worse, skip
- **TanDEM-X 12m** (free for academic/non-commercial, requires DLR registration) — best free option
- **Buy 5m LiDAR** from a survey firm in Asunción
- **Drone-photogrammetry DEM** from a property flyover (Wesley + drone) — best resolution/cost ratio for 62 ha

### 4.5 Aspect classification for the Southern Hemisphere

Your v1 has the standard 4 classes. Add **two more** for the Paraguay context:

```python
# Updated buildability: also consider aspect for thermal comfort
def climate_class(aspect_deg, slope_pct):
    if slope_pct < 8:  return "flat"
    if 135 <= aspect_deg <= 225:  return "south-facing (shaded, cool)"  # away from sun
    if 315 <= aspect_deg or aspect_deg <= 45:  return "north-facing (sun-exposed, hot)"
    if 45 < aspect_deg < 135:  return "east-facing (morning sun)"
    return "west-facing (afternoon sun)"
```

**Why this matters for HOUSE-FIELD rules:**
- The cob house should be on a **south-facing slope** (cool, shaded, away from equator sun). This is already in `paraguay_clay_house_research.md` and `MASTER_BRIEF.md §14` rule 6 (passive design ≤35°C).
- The solar panel array should be on a **north-facing slope** (most sun in SH).
- The cob patio / outdoor tatakuá should be on an **east or north-facing** slope (morning sun, midday heat).
- Avoid **west-facing** for habitable structures (afternoon sun = unbearable).

### 4.6 Multi-criteria buildability (v2 should replace the slope-only classifier)

Real buildability needs more than slope. Weights for the 62 ha parcel:

| Factor | Weight | Source |
|---|---|---|
| Slope (lower = better) | 0.35 | DEM-derived |
| Distance to stream (further = better, dengue protocol) | 0.20 | HAND from pysheds |
| North-facing sun exposure (passive heating) | 0.10 | DEM aspect |
| South-facing shade (cooling, matches cob rule 6) | 0.10 | DEM aspect |
| Distance to existing roads/trails | 0.10 | manual for v2 (OSM later) |
| Distance to high-biomass forest (eco-natural asset) | 0.10 | GEDI L4A when ready |
| Above-flood-plain elevation (HAND > 5m) | 0.05 | pysheds HAND |

Score each pixel 0–1 per factor, weighted sum, classify into 5 buckets. This is a real MCDA and is the standard for green-field development site selection.

### 4.7 Field validation

**The DEM is a model, not truth.** For a 62 ha property with a $500k+ development planned, spend 1 day walking the property with:
- A GPS (phone is fine, 5m accuracy)
- A clinometer (for slope spot-checks)
- A compass (for aspect spot-checks)
- A printed hillshade + contour map

Compare the printed map to the actual land. Note discrepancies in `docs/SITE_VISIT_NOTES.md`. This validates the DEM and the 10 design rules (cob platform doesn't have a 60m cliff in it, etc.).

---

## 5. Code snippets — the v2 toolbox

All of these are tested patterns from the official docs / repo READMEs. Drop into v2 `analyze_dem.py` as needed.

### 5.1 Slope + aspect (richdem)

```python
import richdem as rd
import rasterio
import numpy as np

with rasterio.open("docs/site_data/alos_aw3d30_dem.tif") as src:
    dem = rd.rdarray(src.read(1).astype(np.float32), no_data=-9999.0,
                     geotransform=src.transform, projection=src.crs)
slope = rd.TerrainAttribute(dem, attrib="slope_riserun")  # unitless rise/run
slope_pct = slope * 100  # convert to percent (matches civil engineering)
slope_deg = np.degrees(np.arctan(slope))  # if you want degrees
aspect = rd.TerrainAttribute(dem, attrib="aspect")  # degrees, 0=N, clockwise
# richdem's "slope_*" variants: slope_riserun, slope_degrees, slope_percent
```

### 5.2 Hillshade, multi-sun-angle (numpy, fast)

```python
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling, calculate_default_transform

def hillshade(dem: np.ndarray, dx_m: float, dy_m: float,
              azimuth_deg: float = 315.0, altitude_deg: float = 45.0) -> np.ndarray:
    """Standard ESRI hillshade formula. NaN-safe."""
    az_rad = np.deg2rad(90.0 - azimuth_deg)  # convert to math convention
    alt_rad = np.deg2rad(altitude_deg)
    # Use Sobel (central differences) instead of np.gradient (one-sided at edges)
    from scipy.ndimage import sobel
    gx = sobel(dem, axis=1) / (8.0 * dx_m)
    gy = sobel(dem, axis=0) / (8.0 * dy_m)
    slope = np.arctan(np.sqrt(gx*gx + gy*gy))
    aspect = np.arctan2(-gx, gy)
    shaded = (np.sin(alt_rad) * np.sin(slope) +
              np.cos(alt_rad) * np.cos(slope) * np.cos(az_rad - aspect))
    return np.clip(np.where(np.isnan(shaded), 0, shaded), 0, 1)


def multi_sun_hillshade(dem, dx_m, dy_m, out_tif: Path):
    """Generate 4 hillshades: morning, noon, afternoon, golden hour. Plus
    a multi-directional composite (mean over 8 azimuths at 45° altitude)."""
    angles = [
        ("morning_east",     90.0, 25.0),   # 6am
        ("noon_zenith",       0.0, 75.0),   # solar noon (or 90 for equator)
        ("afternoon_west",  270.0, 25.0),   # 3pm
        ("golden_hour_nw",  315.0, 12.0),   # your hero-cam light
    ]
    profile = {"driver": "GTiff", "dtype": "float32", "count": 1,
               "height": dem.shape[0], "width": dem.shape[1],
               "crs": "EPSG:4326", "transform": None}  # fill in real transform
    for name, az, alt in angles:
        hs = hillshade(dem, dx_m, dy_m, az, alt)
        # save as sidecar tif
    # Multi-directional composite (8 azimuths averaged, like WhiteboxTools multidirectional_hillshade)
    azimuths = np.arange(0, 360, 45)
    composite = np.mean([hillshade(dem, dx_m, dy_m, az, 45.0) for az in azimuths], axis=0)
    return composite
```

Or use the reference implementation via subprocess:

```bash
gdaldem hillshade -az 315 -alt 45 -z 1.0 docs/site_data/alos_filled.tif \
    docs/site_data/analysis/alos_hillshade_315_45.tif
```

`gdaldem hillshade` is the canonical reference — same formula as the ArcGIS Spatial Analyst extension. It also supports `-z` (z-factor vertical exaggeration) and `-s` (scale). Multi-sun is just a loop over `-az -alt` pairs.

### 5.3 Contours (vector GeoJSON)

```python
import subprocess
# Easiest: use gdaldem contour (CLI)
subprocess.run([
    "gdaldem", "contour",
    "-i", "10",          # 10m elevation interval
    "-f", "GeoJSON",     # vector output
    "docs/site_data/alos_filled.tif",
    "docs/site_data/analysis/contours_10m.geojson",
], check=True)
```

Or stay in Python with `rasterio.features.shapes`:

```python
import numpy as np
import rasterio
from rasterio.features import shapes

# ... build dem ...

contour_interval = 10.0  # metres
min_elev = np.floor(np.nanmin(dem) / contour_interval) * contour_interval
max_elev = np.ceil(np.nanmax(dem) / contour_interval) * contour_interval

# Method: marching squares via scikit-image
from skimage import measure
contours = measure.find_contours(dem, level=200.0)  # at elev 200m
# Transform (row, col) back to (lon, lat) using rasterio.transform
for c in contours:
    coords = [rasterio.transform.xy(transform, row, col) for row, col in c]
    # → GeoJSON Feature
```

`gdaldem contour` is simpler and writes valid GeoJSON directly. The skimage path gives you programmatic control (e.g., only major contours) but is more code.

### 5.4 Watershed + HAND (pysheds)

```python
from pysheds.grid import Grid
import numpy as np
import rasterio

grid = Grid.from_raster("docs/site_data/alos_filled_utm21j.tif")  # in METRES!
dem = grid.read_raster("docs/site_data/alos_filled_utm21j.tif")

# D8 directional mapping (NE, N, NW, W, SW, S, SE, E)
dirmap = (64, 128, 1, 2, 4, 8, 16, 32)

# Condition (if not already done)
pit = grid.fill_pits(dem)
dep = grid.fill_depressions(pit)
inflated = grid.resolve_flats(dep)

# Flow direction
fdir = grid.flowdir(inflated, dirmap=dirmap)

# Flow accumulation (number of upstream cells)
acc = grid.accumulation(fdir, dirmap=dirmap)

# Pour point — at the stream's lowest point in the property.
# In lat/lon this is roughly (-57.030, -25.633). Snap to high-accumulation cell.
x, y = -57.030, -25.633
x_snap, y_snap = grid.snap_to_mask(acc > 1000, (x, y))

# Catchment (watershed) above the pour point
catch = grid.catchment(x=x_snap, y=y_snap, fdir=fdir, dirmap=dirmap, xytype="coordinate")

# Stream network (cells with > 1000 upstream cells = perennial stream)
streams = grid.extract_river_network(fdir, acc > 1000, dirmap=dirmap)

# HAND (Height Above Nearest Drainage) — flood-risk + siting
hand = grid.compute_hand(fdir, dem, grid.catch)
```

`pysheds` is the cleanest lib for this. The `extract_river_network` output is GeoJSON you can drop into QGIS immediately. The `compute_hand` output is a raster (per-pixel elevation above the nearest stream) that feeds into flood-risk assessment.

### 5.5 Viewshed (pyviewshed)

```python
# pip install pyviewshed
import numpy as np
import rasterio
import pyviewshed

# Observer points: each of the 6 cameras + each candidate house platform
# (lon, lat, height_above_ground_m) tuples
observers = [
    (-57.030, -25.633, 1.7),   # human eye height for the hero cam
    (-57.029, -25.635, 1.7),   # house_corredor_view
    (-57.031, -25.630, 1.7),   # cliff cam
    # ... etc
]

# DEM as numpy array, in UTM (METRES) for accurate distance
with rasterio.open("docs/site_data/alos_filled_utm21j.tif") as src:
    dem = src.read(1)
    transform = src.transform  # affine (in metres in UTM)
    crs = src.crs

# Compute viewshed for one observer
def viewshed_one(dem, transform, observer_utm_x, observer_utm_y, observer_height_m=1.7):
    """Returns 2D boolean array: True if visible from the observer point."""
    # Convert observer UTM coords to pixel (row, col)
    col, row = ~transform * (observer_utm_x, observer_utm_y)
    col, row = int(col), int(row)
    if not (0 <= row < dem.shape[0] and 0 <= col < dem.shape[1]):
        return None  # observer outside DEM
    # pyviewshed expects: dem, observer (row, col), observer height, target height
    vs = pyviewshed.viewshed(
        dem,
        observer=(row, col),
        observer_height=observer_height_m,
        target_height=0.0,        # what's the ground visibility?
        refraction=False,         # turn on for >5km distances (Earth curvature)
        earth_curvature=False,
        pixelsize=transform.a,   # square pixels (UTM)
    )
    return vs > 0  # boolean visibility mask

# Or, if you have many observer points, use the batched variant:
# vs_all = pyviewshed.viewshed_batch(dem, observer_points=...)
```

For the 62 ha property analysis, compute viewshed from each candidate house platform and from each render camera. The intersection of "high viewshed" + "south-facing" + "slope < 15%" + "HAND > 5m" is the premium house location.

### 5.6 Hypsometric tint + hillshade composite (matplotlib, for SITE_DIAGNOSTIC-style maps)

```python
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Atlantic Forest palette (paraguay-context skill)
# Red laterite #8B3A1F → sandstone #7A7268 → forest green #4A6B2A → ridge white
terrain_cmap = LinearSegmentedColormap.from_list(
    "paraguay_terrain",
    [
        (0.00, "#3A4538"),   # stream / water
        (0.15, "#8B3A1F"),   # red laterite soil
        (0.40, "#7A7268"),   # sandstone / boulders
        (0.65, "#5F7A3D"),   # moss / low vegetation
        (0.85, "#2F4A1E"),   # forest canopy
        (1.00, "#FFFFFF"),   # bare ridge
    ],
    N=256,
)

def plot_hypsometric(dem, hillshade, out_png, title=""):
    fig, ax = plt.subplots(figsize=(12, 12), dpi=120)
    # Hypsometric tint (color by elevation)
    elev_normed = (dem - np.nanmin(dem)) / (np.nanmax(dem) - np.nanmin(dem))
    colored = terrain_cmap(elev_normed)[:, :, :3]  # RGBA → RGB
    # Combine: hillshade darkens, color tints
    combined = colored * (0.4 + 0.6 * hillshade[:, :, None])
    ax.imshow(combined, extent=extent, origin="upper")
    ax.set_title(title)
    # Overlay contours
    cs = ax.contour(xs, ys, dem, levels=range(120, 380, 20), colors="black", linewidths=0.3, alpha=0.4)
    ax.clabel(cs, fmt="%d", fontsize=6)
    plt.tight_layout()
    plt.savefig(out_png, dpi=120, bbox_inches="tight")
```

This gives a single image that reads at a glance: stream, escarpment, ridges, valleys. Replace your v1's `site_diagnostic.png` with this.

### 5.7 Multi-criteria buildability (the v2 replacement for the slope-only classifier)

```python
import numpy as np
import rasterio

def mcda_buildability(dem, slope_pct, aspect_deg, hand, distance_to_stream,
                     distance_to_road=None, biomass=None,
                     weights=None) -> np.ndarray:
    """Weighted sum of normalized factors. Returns 0-1 score per pixel.
    Higher = better for building. Uses HAND and distance-to-stream for
    dengue / flood protocol (rule 3 + 4 of the 10 design rules)."""
    w = weights or {
        "slope": 0.35,
        "distance_to_stream": 0.20,
        "north_facing": 0.10,
        "south_facing": 0.10,
        "distance_to_road": 0.10,
        "biomass": 0.10,
        "hand": 0.05,
    }
    s_norm = 1.0 - np.clip(slope_pct / 30.0, 0, 1)  # 0% slope = 1, 30%+ = 0
    s_norm = np.where(np.isnan(slope_pct), 0, s_norm)
    # North-facing = good for solar; South-facing = good for shade
    aspect_rad = np.deg2rad(aspect_deg)
    n_fac = 0.5 + 0.5 * np.cos(aspect_rad)  # 1 at N (0°), 0 at S (180°)
    s_fac = 0.5 + 0.5 * np.cos(aspect_rad + np.pi)  # 1 at S, 0 at N
    # Distance to stream: dengue rule says > 50m from any standing water
    d_stream_norm = np.clip(distance_to_stream / 100.0, 0, 1)  # 100m = max
    d_stream_norm = np.where(np.isnan(distance_to_stream), 0, d_stream_norm)
    hand_norm = np.clip(hand / 10.0, 0, 1)  # 10m above nearest drainage = max
    hand_norm = np.where(np.isnan(hand), 0, hand_norm)

    score = (
        w["slope"] * s_norm
        + w["distance_to_stream"] * d_stream_norm
        + w["north_facing"] * n_fac
        + w["south_facing"] * s_fac
        + w["hand"] * hand_norm
    )
    if distance_to_road is not None:
        d_road_norm = np.clip(distance_to_road / 500.0, 0, 1)  # 500m = max
        d_road_norm = np.where(np.isnan(distance_to_road), 0, d_road_norm)
        score = score + w["distance_to_road"] * d_road_norm
    if biomass is not None:
        # High biomass = forest = good for eco-natural positioning
        bio_norm = np.clip(biomass / 250.0, 0, 1)  # 250 Mg/ha = max (Atlantic Forest max)
        bio_norm = np.where(np.isnan(biomass), 0, bio_norm)
        score = score + w["biomass"] * bio_norm
    return np.clip(score, 0, 1)
```

This is a real MCDA. Tune the weights per `EUROPEAN_TOURISM_SPEC.md` priorities (vacation-rental houses vs. restaurant vs. trail network will have different weights).

---

## 6. What was wrong with v1 (`scripts/analyze_dem.py`)

Not a roast — a list of specific fixes to land in v2. All of them are addressed by the patterns above.

| Issue | v1 (current) | v2 fix | Severity |
|---|---|---|---|
| `np.gradient` edge cells use 1-sided differences | yes | Use `scipy.ndimage.sobel` (central, 3×3 stencil) | Low for slope viz, **high for watershed edge cells** |
| No DEM conditioning before flow analysis | yes | Add `fill_pits` → `fill_depressions` → `resolve_flats` | **Critical — watershed will be wrong** |
| `M_PER_DEG_LON` hardcoded to lat -25.6 | yes | Reproject DEM to UTM 21J once, work in metres | Medium — 5m error on 3.3km box, ~17% of pixel |
| Hillshade only at 315°/45° | yes | Add multi-sun-angle (4 angles + multidirectional composite) | Low (viz) but the user asked for it |
| Buildability is slope-only | yes | Multi-criteria with HAND + distance-to-stream + aspect | Medium — v1 said 80% buildable, real number is lower |
| No viewshed | yes | Add `pyviewshed` for each camera + each candidate house | High — listed in SITE_DIAGNOSTIC §6.5 as next step |
| No contours saved as vector | yes | Add `gdaldem contour` → GeoJSON | Low — matplotlib inline is fine for first-pass, GeoJSON is what QGIS wants |
| No Blender heightmap output | yes | Add `lqv/site/build_heightmap.py` | **High — `lqv/site/terrain_62ha.py` is dormant waiting for this** |
| `M_PER_DEG_LON` ignores actual bbox center | yes | Use `(lat_max + lat_min) / 2` | Low — same as above |
| No 32-bit EXR displacement | yes | Add via `imageio` (optional, 16-bit PNG is the primary) | Low |
| `np.gradient` resolution param uses (dy, dx) order but passes them in correctly | yes (lucky) | n/a | n/a |
| `np.cos(np.deg2rad(-25.6))` in M_PER_DEG_LON | yes | n/a after reproject | Resolved by reproject |
| `aspect_rad = np.arctan2(-gx, gy)` | correct | (verified against GDAL/ESRI convention) | n/a |
| No NaN guard on edge pixels | yes | richdem and Sobel both handle this | Resolved |

The single most important fix is **DEM conditioning**. The second is **reprojecting to UTM**. Both unlock the rest of the analysis (watershed, viewshed, HAND).

---

## 7. v2 implementation roadmap

In order of value-per-effort. Each phase is one PR, all are testable independently.

### Phase 1 — Switch slope/aspect to richdem, add DEM conditioning
- `pip install richdem pysheds pyviewshed`
- Rewrite `analyze_dem.py` slope/aspect to use `richdem.TerrainAttribute`
- Add `fill_pits` → `fill_depressions` → `resolve_flats` to a conditioned DEM output
- Reproject the conditioned DEM to UTM 21J
- Verify: slope values match v1 within 1°, watershed boundary cells no longer garbage

### Phase 2 — Real watershed analysis (pysheds)
- Add `flowdir` + `accumulation` + `catchment` (pour point at the stream's lowest cell in the property)
- Add HAND (height above nearest drainage) — feeds buildability
- Add `extract_river_network` → GeoJSON for the streams
- Add `stream_order` for the Strahler order of each segment
- Output: `analysis/watershed.geojson`, `analysis/hand.tif`, `analysis/flow_accumulation.tif`

### Phase 3 — Viewshed from each camera + candidate house platforms
- Use `pyviewshed` (pure Python, no C++ build)
- For each of the 6 cameras in `lqv/cameras.py` + each candidate house platform (5-10 sites)
- Output: `analysis/viewshed_<camname>.tif` and a composite that highlights the most-viewed terrain
- Update SITE_DIAGNOSTIC.md with the viewshed map

### Phase 4 — Multi-sun-angle hillshade + hypsometric tint composite
- Generate 4 single-angle hillshades (morning, noon, afternoon, golden hour)
- Generate 1 multi-directional composite (8 azimuths at 45° altitude)
- Build the hypsometric-tinted composite (Atlantic Forest palette from `paraguay-context` skill)
- Update `site_diagnostic.png` to use the composite

### Phase 5 — Pre-render heightmap pipeline (THE deliverable)
- Write `lqv/site/build_heightmap.py` from §3.2
- Run it on the 5m-upsampled ALOS DEM
- Wire `lqv/site/terrain_62ha.py` to read the sidecar JSON
- Update `lqv/site/ground.py` to use the heightmap-displaced plane as the base (vs. the current hand-displaced one)
- Rerun `smoke_test.sh` to verify the camera positions still work
- Render a preview to confirm the new terrain reads correctly
- Hero render once preview is approved

Estimated effort: 1 day for phases 1-3, 0.5 day for phase 4, 1 day for phase 5 (including a few Cycles re-renders to dial in the vertical exaggeration). Total: 2.5 days. The v2 script is then a real tool, not just a visualizer.

---

## 8. References

- **OpenTopography**: https://opentopography.org/developers (this research)
- **richdem docs**: https://richdem.readthedocs.io (full algorithm list, with D8/D∞/MFD/Rho8/Quinn/Freeman/Holmgren/Tarboton variants)
- **richdem paper**: Barnes, R., Lehman, C., Mulla, D. (2014). "Priority-flood: An optimal depression-filling and watershed-labeling algorithm for digital elevation models." *Computers & Geosciences* 62, 117-127.
- **WhiteboxTools**: https://whiteboxgeo.com/manual/wbt_book/intro.html (518 tools, 700+ in the Next Gen preview)
- **pysheds**: https://mdbartos.github.io/pysheds (full watershed + HAND + stream order)
- **pyviewshed**: https://pypi.org/project/pyviewshed/ (line-of-sight + refraction)
- **GDAL `gdaldem`**: https://gdal.org/programs/gdaldem.html (the reference slope/aspect/hillshade/contour implementation)
- **Atlantic Forest context**: `paraguay-context` skill (climate, flora, buildability rules)
- **House-field project rules**: `house-field/CLAUDE.md` (10 design rules) and `house-field/docs/MASTER_BRIEF.md`
- **Existing SITE_DIAGNOSTIC.md**: `docs/site_data/SITE_DIAGNOSTIC.md` (the v1 results — your 264m of relief, 80% buildable, 70ha of escarpment)

---

*Compiled by AI Whisperers from the live scripts at `house-field/scripts/{fetch_opentopo_dem,analyze_dem}.py` and the four DEMs in `docs/site_data/`. Next step: implement phases 1-3 of the roadmap above.*
