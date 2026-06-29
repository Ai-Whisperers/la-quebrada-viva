#!/usr/bin/env python3
"""Phase-0 §12 (NEW 2026-06-28 ask): tiered topology cube for the eventual
3D digital twin.

User directive (verbatim):
> "we want good topology for the property and low poly for the nearby
> surroundings we want to include the important nearby geograhy into maps so
> we can make a good digital version later but we mostly care about the
> property we want real and complete as high deginition for there and the rest
> can be les hd more poly"

Tier 1 — core (polygon + 100 m buffer): fuse the 4 best-available open DEMs
(ALOS AW3D30 + Cop30 + SRTM GL1 + NASADEM) via per-pixel median, then
resample to a 5 m grid via cubic spline. Source resolution is still 30 m;
the upsample yields a smooth high-density grid suitable for Blender
displacement / dense-mesh export. R35 drone-LiDAR will drop in later as
`dem_lidar_*.tif` and supersede the fused surface in this tier only.

Tier 2 — local context (~5 km buffer around polygon centroid): Cop30 at
native ~30 m, fetched via OpenTopography API. Used for ridge / valley
context immediately around the parcel.

Tier 3 — regional macro (25 km buffer matching biodiversity AOI): Cop30
decimated to ~90 m via mean-pooling for low-poly Blender geometry of the
wider landscape (Mbopicua cluster, Cerro Mbatoví, Cerro Hu, Lago Ypoá).

Outputs land in docs/site_data/topology_lod/:
- core/dem_fused_5m.tif + dem_fused_30m.tif + sources_used.json + hillshade.png
- local/cop30_30m.tif + hillshade.png
- regional/cop30_90m.tif + hillshade.png
- tier_manifest.md
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import rasterio
import requests
from rasterio.enums import Resampling
from rasterio.transform import from_bounds
from rasterio.warp import reproject

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "site_data" / "topology_lod"
CORE = OUT / "core"
LOCAL = OUT / "local"
REGIONAL = OUT / "regional"
for d in (CORE, LOCAL, REGIONAL):
    d.mkdir(parents=True, exist_ok=True)

CENTROID_LON, CENTROID_LAT = -57.0355, -25.6073
DEG_PER_KM_LAT = 1.0 / 111.0
DEG_PER_KM_LON = 1.0 / (111.0 * math.cos(math.radians(CENTROID_LAT)))

# Polygon bbox (Wesley's 30.9 ha) + ~100 m buffer
POLY_W, POLY_S, POLY_E, POLY_N = -57.050, -25.625, -57.020, -25.595
BUF_DEG_100M = 100.0 * DEG_PER_KM_LAT / 1000.0  # convert m → degrees lat
CORE_W = POLY_W - BUF_DEG_100M
CORE_S = POLY_S - BUF_DEG_100M
CORE_E = POLY_E + BUF_DEG_100M
CORE_N = POLY_N + BUF_DEG_100M

# Tier 2 — ~5 km buffer around polygon centroid
LOCAL_BUF_KM = 5.0
LOCAL_W = CENTROID_LON - LOCAL_BUF_KM * DEG_PER_KM_LON
LOCAL_S = CENTROID_LAT - LOCAL_BUF_KM * DEG_PER_KM_LAT
LOCAL_E = CENTROID_LON + LOCAL_BUF_KM * DEG_PER_KM_LON
LOCAL_N = CENTROID_LAT + LOCAL_BUF_KM * DEG_PER_KM_LAT

# Tier 3 — 25 km buffer matching biodiversity AOI
REG_BUF_KM = 25.0
REG_W = CENTROID_LON - REG_BUF_KM * DEG_PER_KM_LON
REG_S = CENTROID_LAT - REG_BUF_KM * DEG_PER_KM_LAT
REG_E = CENTROID_LON + REG_BUF_KM * DEG_PER_KM_LON
REG_N = CENTROID_LAT + REG_BUF_KM * DEG_PER_KM_LAT

EXISTING_DEMS = {
    "alos_aw3d30": ROOT / "docs/site_data/extended_aoi/alos_aw3d30_dem.tif",
    "cop30": ROOT / "docs/site_data/extended_aoi/cop30_dem.tif",
    "srtm_gl1": ROOT / "docs/site_data/extended_aoi/srtm_gl1_dem.tif",
    "nasadem": ROOT / "docs/site_data/extended_aoi/nasadem_dem.tif",
}

# OpenTopography
OT_KEY = os.environ.get("OPENTOPOGRAPHY_API_KEY", "")
if not OT_KEY:
    # parse .env.local if present
    env = ROOT / ".env.local"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("OPENTOPOGRAPHY_API_KEY="):
                OT_KEY = line.split("=", 1)[1].strip()
                break


def fetch_cop30(west: float, south: float, east: float, north: float, out_path: Path) -> bool:
    if not OT_KEY:
        print(f"  ! no OPENTOPOGRAPHY_API_KEY; skipping {out_path.name}")
        return False
    if out_path.exists():
        print(f"  ✓ {out_path.name} already exists; skipping fetch")
        return True
    url = "https://portal.opentopography.org/API/globaldem"
    params = {
        "demtype": "COP30",
        "south": south,
        "north": north,
        "west": west,
        "east": east,
        "outputFormat": "GTiff",
        "API_Key": OT_KEY,
    }
    print(f"  → OpenTopography Cop30 fetch {west:.4f},{south:.4f},{east:.4f},{north:.4f}")
    for attempt in range(4):
        try:
            r = requests.get(url, params=params, timeout=300)
            if r.status_code == 200 and r.content[:4] in (b"II*\x00", b"MM\x00*"):
                out_path.write_bytes(r.content)
                print(f"  ✓ wrote {out_path.name} ({len(r.content)/1e6:.1f} MB)")
                return True
            print(f"  ! status {r.status_code} attempt {attempt+1}: {r.text[:160]}")
        except requests.exceptions.RequestException as e:
            print(f"  ! {type(e).__name__} attempt {attempt+1}: {e}")
        time.sleep(2 ** attempt)
    return False


def warp_to_grid(src_path: Path, w: float, s: float, e: float, n: float, res_m: float) -> tuple[np.ndarray, dict]:
    """Reproject src raster onto a regular geographic grid (EPSG:4326) where
    res_m is the *target spatial resolution in metres*. We approximate with
    lat-degree spacing (1 m ≈ 1/111e3 deg)."""
    res_deg = res_m / 111000.0
    cols = max(2, int(round((e - w) / res_deg)))
    rows = max(2, int(round((n - s) / res_deg)))
    dst_transform = from_bounds(w, s, e, n, cols, rows)
    dst = np.full((rows, cols), np.nan, dtype="float32")
    with rasterio.open(src_path) as src:
        reproject(
            source=rasterio.band(src, 1),
            destination=dst,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=dst_transform,
            dst_crs="EPSG:4326",
            resampling=Resampling.cubic,
            dst_nodata=np.nan,
        )
    profile = {
        "driver": "GTiff",
        "dtype": "float32",
        "count": 1,
        "height": rows,
        "width": cols,
        "crs": "EPSG:4326",
        "transform": dst_transform,
        "nodata": float("nan"),
        "compress": "deflate",
        "predictor": 3,
    }
    return dst, profile


def write_raster(arr: np.ndarray, profile: dict, path: Path) -> None:
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(arr.astype("float32"), 1)


def hillshade(z: np.ndarray, dx: float = 1.0, dy: float = 1.0, az: float = 315.0, alt: float = 45.0) -> np.ndarray:
    z = np.where(np.isnan(z), np.nanmedian(z), z)
    gy, gx = np.gradient(z, dy, dx)
    slope = np.pi / 2.0 - np.arctan(np.hypot(gx, gy))
    aspect = np.arctan2(-gx, gy)
    az_rad = np.deg2rad(360.0 - az + 90.0)
    alt_rad = np.deg2rad(alt)
    shaded = np.sin(alt_rad) * np.sin(slope) + np.cos(alt_rad) * np.cos(slope) * np.cos(az_rad - aspect)
    shaded = np.clip(shaded, 0, 1)
    return (shaded * 255).astype("uint8")


def write_hillshade_png(z: np.ndarray, path: Path) -> None:
    try:
        from PIL import Image
    except ImportError:
        print(f"  ! PIL unavailable; skipping {path.name}")
        return
    hs = hillshade(z)
    Image.fromarray(hs, mode="L").save(path)


def mean_pool(arr: np.ndarray, factor: int) -> np.ndarray:
    h, w = arr.shape
    nh, nw = h // factor, w // factor
    trimmed = arr[: nh * factor, : nw * factor]
    return np.nanmean(
        trimmed.reshape(nh, factor, nw, factor),
        axis=(1, 3),
    )


def build_tier1_core() -> dict:
    """Fuse 4 open DEMs over the core AOI; output 30 m fused + 5 m smooth."""
    print("[Tier 1 / core] fusing", list(EXISTING_DEMS.keys()))
    # 30 m baseline grid
    stack = []
    sources = {}
    for name, path in EXISTING_DEMS.items():
        if not path.exists():
            print(f"  ! missing {path}")
            continue
        arr = warp_to_grid(path, CORE_W, CORE_S, CORE_E, CORE_N, res_m=30.0)[0]
        stack.append(arr)
        sources[name] = {
            "path": str(path.relative_to(ROOT)),
            "min": float(np.nanmin(arr)),
            "max": float(np.nanmax(arr)),
            "mean": float(np.nanmean(arr)),
        }
    if not stack:
        raise RuntimeError("no source DEMs found for tier 1 fusion")
    fused30 = np.nanmedian(np.stack(stack, axis=0), axis=0)
    _, prof30 = warp_to_grid(EXISTING_DEMS["cop30"], CORE_W, CORE_S, CORE_E, CORE_N, res_m=30.0)
    write_raster(fused30, prof30, CORE / "dem_fused_30m.tif")
    write_hillshade_png(fused30, CORE / "dem_fused_30m_hillshade.png")
    # 5 m smooth (cubic upsample of one source then replace values with the
    # cubic-resampled fused). We reproject *each* source individually to 5 m
    # then take the median again — preserves more detail than upsampling the
    # median directly.
    stack5 = []
    prof5: dict | None = None
    for name, path in EXISTING_DEMS.items():
        if not path.exists():
            continue
        arr5, prof5 = warp_to_grid(path, CORE_W, CORE_S, CORE_E, CORE_N, res_m=5.0)
        stack5.append(arr5)
    if prof5 is None:
        raise RuntimeError("no source DEMs found for tier 1 5 m resample")
    fused5 = np.nanmedian(np.stack(stack5, axis=0), axis=0)
    write_raster(fused5, prof5, CORE / "dem_fused_5m.tif")
    write_hillshade_png(fused5, CORE / "dem_fused_5m_hillshade.png")
    (CORE / "sources_used.json").write_text(
        json.dumps(
            {
                "bbox": [CORE_W, CORE_S, CORE_E, CORE_N],
                "buffer_m": 100,
                "sources": sources,
                "fused_30m_shape": list(fused30.shape),
                "fused_5m_shape": list(fused5.shape),
                "fused_5m_min": float(np.nanmin(fused5)),
                "fused_5m_max": float(np.nanmax(fused5)),
                "fused_5m_mean": float(np.nanmean(fused5)),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return {
        "shape_30m": fused30.shape,
        "shape_5m": fused5.shape,
        "min": float(np.nanmin(fused5)),
        "max": float(np.nanmax(fused5)),
        "mean": float(np.nanmean(fused5)),
    }


def build_tier2_local() -> dict:
    """Cop30 over ~5 km buffer around centroid."""
    print("[Tier 2 / local] Cop30 30 m over 5 km buffer")
    raw = LOCAL / "cop30_raw.tif"
    fetch_cop30(LOCAL_W, LOCAL_S, LOCAL_E, LOCAL_N, raw)
    if not raw.exists():
        return {"status": "missing"}
    arr, prof = warp_to_grid(raw, LOCAL_W, LOCAL_S, LOCAL_E, LOCAL_N, res_m=30.0)
    write_raster(arr, prof, LOCAL / "cop30_30m.tif")
    write_hillshade_png(arr, LOCAL / "cop30_30m_hillshade.png")
    return {
        "shape": arr.shape,
        "min": float(np.nanmin(arr)),
        "max": float(np.nanmax(arr)),
        "mean": float(np.nanmean(arr)),
    }


def build_tier3_regional() -> dict:
    """Cop30 over 25 km buffer, decimated to ~90 m for low-poly geometry."""
    print("[Tier 3 / regional] Cop30 over 25 km buffer → 90 m decimation")
    raw = REGIONAL / "cop30_raw.tif"
    fetch_cop30(REG_W, REG_S, REG_E, REG_N, raw)
    if not raw.exists():
        return {"status": "missing"}
    arr30, prof30 = warp_to_grid(raw, REG_W, REG_S, REG_E, REG_N, res_m=30.0)
    arr90 = mean_pool(arr30, factor=3)
    prof90 = dict(prof30)
    prof90["height"], prof90["width"] = arr90.shape
    prof90["transform"] = from_bounds(REG_W, REG_S, REG_E, REG_N, arr90.shape[1], arr90.shape[0])
    write_raster(arr30, prof30, REGIONAL / "cop30_30m.tif")
    write_raster(arr90, prof90, REGIONAL / "cop30_90m.tif")
    write_hillshade_png(arr30, REGIONAL / "cop30_30m_hillshade.png")
    write_hillshade_png(arr90, REGIONAL / "cop30_90m_hillshade.png")
    return {
        "shape_30m": arr30.shape,
        "shape_90m": arr90.shape,
        "min": float(np.nanmin(arr90)),
        "max": float(np.nanmax(arr90)),
        "mean": float(np.nanmean(arr90)),
    }


def write_manifest(t1: dict, t2: dict, t3: dict) -> None:
    md = [
        "# Topology LOD cube — tier manifest",
        "",
        "Driver: `scripts/phase0_topology_lod_cube.py`",
        "Generated: " + time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
        "",
        "User directive (2026-06-28): *high-fidelity topology inside the polygon, low-poly for surroundings, include important nearby geography for the eventual 3D digital twin.*",
        "",
        "All rasters EPSG:4326 (lon/lat) with nodata=NaN, deflate-compressed.",
        "Future drone-LiDAR (R35) drops into `core/dem_lidar_*.tif` and supersedes",
        "the fused 5 m surface for Tier 1 only — Tiers 2 and 3 remain Cop30-based.",
        "",
        "## Tier 1 — property core",
        "",
        f"- AOI: polygon ({POLY_W:.4f},{POLY_S:.4f},{POLY_E:.4f},{POLY_N:.4f}) + ~100 m buffer",
        f"- Source: per-pixel **median** of ALOS AW3D30 + Cop30 + SRTM GL1 + NASADEM",
        f"- Native source resolution: ~30 m; resampled to **5 m grid** via cubic spline",
        f"- 30 m baseline: `core/dem_fused_30m.tif` shape {t1.get('shape_30m')}",
        f"- 5 m smooth: `core/dem_fused_5m.tif` shape {t1.get('shape_5m')}",
        f"- Elevation: min {t1.get('min'):.1f} m, max {t1.get('max'):.1f} m, mean {t1.get('mean'):.1f} m",
        f"- Hillshade quicklook: `core/dem_fused_5m_hillshade.png`",
        f"- **Honest caveat**: source data is 30 m. Upsampling to 5 m yields a smooth high-density grid suitable for Blender displacement / dense-mesh export but does **not** add real detail. True high-fidelity awaits drone-LiDAR (R35).",
        f"- Recommended Blender mesh: 600×600 grid (~360 k tris) from 5 m raster as displacement map",
        "",
        "## Tier 2 — local context (5 km buffer)",
        "",
        f"- AOI: ({LOCAL_W:.4f},{LOCAL_S:.4f},{LOCAL_E:.4f},{LOCAL_N:.4f})",
        f"- Source: Copernicus Cop30 (~30 m) via OpenTopography",
        f"- Output: `local/cop30_30m.tif` shape {t2.get('shape')}",
        f"- Elevation: min {t2.get('min'):.1f} m, max {t2.get('max'):.1f} m, mean {t2.get('mean'):.1f} m" if t2.get("status") != "missing" else "- ⚠️ missing",
        f"- Recommended Blender mesh: 300×300 grid (~90 k tris) — medium-detail surround for views of the parcel against immediate hills",
        "",
        "## Tier 3 — regional macro (25 km buffer)",
        "",
        f"- AOI: ({REG_W:.4f},{REG_S:.4f},{REG_E:.4f},{REG_N:.4f}) — matches biodiversity AOI",
        f"- Source: Copernicus Cop30 decimated 3× via mean-pooling → ~90 m grid",
        f"- 30 m raw: `regional/cop30_30m.tif`; 90 m low-poly: `regional/cop30_90m.tif` shape {t3.get('shape_90m')}",
        f"- Elevation: min {t3.get('min'):.1f} m, max {t3.get('max'):.1f} m, mean {t3.get('mean'):.1f} m" if t3.get("status") != "missing" else "- ⚠️ missing",
        f"- Recommended Blender mesh: 200×200 grid (~40 k tris) — distant context (Cerro Mbatoví, Cerro Hu, Lago Ypoá, Mbopicua ridge)",
        "",
        "## Future drop-ins",
        "",
        "- **R35 drone-LiDAR** (post-photo intake): `core/dem_lidar_0p5m.tif` would supersede `dem_fused_5m.tif`; rebuild Tier 1 mesh at 0.5 m → ~6 M tris (decimate to taste for Blender).",
        "- **Photogrammetric drone DEM** (cheaper alternative to LiDAR): `core/dem_drone_phot_0p1m.tif` if R35 budget unavailable.",
        "- **R-series municipal cadastral DEM**: if Esc municipalidad publishes 1 m LiDAR, ingest into `core/dem_cad_1m.tif`.",
        "",
        "## Blender import recipe",
        "",
        "1. **Tier 1 (core)**: import `dem_fused_5m.tif` as displacement texture on a 600×600 subdivided plane sized to the core AOI footprint in metres (≈ 3.3 km × 3.6 km). Modifier: Displace → Texture (Image, Non-Color), Strength = (max-min) m, Midlevel = (mean-min)/(max-min).",
        "2. **Tier 2 (local)**: same recipe with `local/cop30_30m.tif` on a 300×300 plane sized to 10 km × 10 km.",
        "3. **Tier 3 (regional)**: `regional/cop30_90m.tif` on 200×200 plane sized to 50 km × 50 km.",
        "4. Align all three to the polygon centroid (-57.0355, -25.6073) → UTM 21S origin so they nest correctly. Set Tier 1 to render in foreground, Tiers 2–3 with lower subdivision modifier strength and a fall-off texture to blend horizons.",
        "",
    ]
    (OUT / "tier_manifest.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"  → {OUT / 'tier_manifest.md'}")


def main() -> int:
    t1 = build_tier1_core()
    t2 = build_tier2_local()
    t3 = build_tier3_regional()
    write_manifest(t1, t2, t3)
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
