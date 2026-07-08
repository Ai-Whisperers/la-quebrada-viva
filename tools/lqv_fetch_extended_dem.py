#!/usr/bin/env python3
"""
Fetch wider DEMs for LQV LOD1 (Escobar, 7.7 km) and LOD2 (regional, 23 km)
using AWS terrain-rgb tiles + slippy-map math. No API key needed.

AWS terrain-rgb: https://elevation-tiles-prod.s3.amazonaws.com/terrarium/{z}/{x}/{y}.png
Decoding: elevation_m = R * 256 + G + B / 256 - 32768

Tile coverage at LQV latitude (-25.63):
  z=12:  ~10 km/tile (good for LOD2 regional)
  z=13:  ~5 km/tile (good for LOD1 Escobar)
  z=14:  ~2.5 km/tile (overkill for our LODs, but useful for verification)

Outputs:
  docs/site_data/extended_aoi/dem/extended_dem_lod1.tif  (7.7 km, 15 m/pixel)
  docs/site_data/extended_aoi/dem/extended_dem_lod2.tif  (23 km, 60 m/pixel)
"""
from __future__ import annotations

import io
import math
import sys
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import Affine
import requests
from PIL import Image

REPO = Path("/root/la-quebrada-viva")
DEM_OUT_DIR = REPO / "docs" / "site_data" / "extended_aoi" / "dem"
DEM_OUT_DIR.mkdir(parents=True, exist_ok=True)

CENTROID_LON = -57.030
CENTROID_LAT = -25.630


def lonlat_to_tile(lon: float, lat: float, z: int) -> tuple[int, int]:
    n = 2 ** z
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int(
        (1.0 - math.log(math.tan(math.radians(lat)) + 1.0 / math.cos(math.radians(lat))) / math.pi)
        / 2.0
        * n
    )
    return xtile, ytile


def tile_to_lonlat(x: int, y: int, z: int) -> tuple[float, float]:
    """Top-left corner of tile (x, y, z) in WGS84."""
    n = 2 ** z
    lon = x / n * 360.0 - 180.0
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    return lon, lat


def fetch_tile(z: int, x: int, y: int, retries: int = 3) -> np.ndarray:
    """Fetch a single terrain-rgb PNG tile and decode to elevation array."""
    url = f"https://elevation-tiles-prod.s3.amazonaws.com/terrarium/{z}/{x}/{y}.png"
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=30, headers={"User-Agent": "LQV-Pipeline/1.0"})
            r.raise_for_status()
            img = np.array(Image.open(io.BytesIO(r.content)).convert("RGB"))
            # Decode RGB to elevation: R*256 + G + B/256 - 32768
            R = img[:, :, 0].astype(np.float32)
            G = img[:, :, 1].astype(np.float32)
            B = img[:, :, 2].astype(np.float32)
            elev = R * 256.0 + G + B / 256.0 - 32768.0
            return elev
        except Exception as e:
            if attempt < retries - 1:
                import time
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"Tile {z}/{x}/{y} failed after {retries} tries: {e}")


def fetch_aoi_elevation(west: float, south: float, east: float, north: float, zoom: int, max_pixels: int = 4096) -> tuple[np.ndarray, Affine]:
    """Fetch + stitch terrain-rgb tiles for an AOI at given zoom level.

    Returns: (elevation_array, affine_transform)
    """
    # Compute tile range
    x_min, y_min = lonlat_to_tile(west, north, zoom)  # top-left
    x_max, y_max = lonlat_to_tile(east, south, zoom)  # bottom-right (inclusive)
    print(f"    z={zoom}: tile range x=[{x_min}, {x_max}] y=[{y_min}, {y_max}] = {x_max - x_min + 1}×{y_max - y_min + 1} tiles")

    n_cols = x_max - x_min + 1
    n_rows = y_max - y_min + 1
    total_px = n_rows * 256 * n_cols * 256
    if total_px > max_pixels * max_pixels:
        print(f"    ⚠ Total pixels {total_px} exceeds limit — lowering zoom")
        zoom -= 1
        x_min, y_min = lonlat_to_tile(west, north, zoom)
        x_max, y_max = lonlat_to_tile(east, south, zoom)
        n_cols = x_max - x_min + 1
        n_rows = y_max - y_min + 1
        print(f"    New z={zoom}: {n_cols}×{n_rows} tiles")

    # Stitch
    canvas = np.full((n_rows * 256, n_cols * 256), np.nan, dtype=np.float32)
    for r in range(n_rows):
        for c in range(n_cols):
            x = x_min + c
            y = y_min + r
            try:
                elev = fetch_tile(zoom, x, y)
                canvas[r * 256:(r + 1) * 256, c * 256:(c + 1) * 256] = elev
            except Exception as e:
                print(f"      ⚠ tile {zoom}/{y}/{x}: {e}")
                # Leave as NaN
        print(f"    Fetched row {r + 1}/{n_rows}")

    # Compute AOI transform
    # Top-left of canvas = top-left of (x_min, y_min)
    tl_lon, tl_lat = tile_to_lonlat(x_min, y_min, zoom)
    res_lon = (tile_to_lonlat(x_min + 1, y_min, zoom)[0] - tl_lon) / 256
    res_lat = (tl_lat - tile_to_lonlat(x_min, y_min + 1, zoom)[1]) / 256
    transform = Affine(res_lon, 0, tl_lon, 0, -res_lat, tl_lat)

    # Crop to requested AOI
    col_start = int(round((west - tl_lon) / res_lon))
    col_end = int(round((east - tl_lon) / res_lon))
    row_start = int(round((tl_lat - north) / res_lat))
    row_end = int(round((tl_lat - south) / res_lat))
    col_start = max(0, col_start)
    row_start = max(0, row_start)
    col_end = min(canvas.shape[1], col_end)
    row_end = min(canvas.shape[0], row_end)
    cropped = canvas[row_start:row_end, col_start:col_end]

    # Recompute transform for cropped array
    new_tl_lon = tl_lon + col_start * res_lon
    new_tl_lat = tl_lat - row_start * res_lat
    cropped_transform = Affine(res_lon, 0, new_tl_lon, 0, -res_lat, new_tl_lat)

    # Fill any NaN with the mean
    nan_count = np.isnan(cropped).sum()
    if nan_count > 0:
        print(f"    Filling {nan_count} NaN pixels with mean")
        mean_elev = float(np.nanmean(cropped))
        cropped = np.where(np.isnan(cropped), mean_elev, cropped)

    return cropped, cropped_transform


def write_geotiff(arr: np.ndarray, transform: Affine, path: Path) -> None:
    with rasterio.open(
        path, "w",
        driver="GTiff",
        height=arr.shape[0],
        width=arr.shape[1],
        count=1,
        dtype="float32",
        crs="EPSG:4326",
        transform=transform,
        compress="lzw",
    ) as dst:
        dst.write(arr, 1)
    size_kb = path.stat().st_size / 1024
    print(f"    ✓ Wrote {path.name} ({size_kb:.1f} KB, shape={arr.shape})")


def fetch_lod(lod_id: int, half_extent_m: float, zoom: int, out_path: Path) -> None:
    print(f"\n[LOD{lod_id}] half_extent={half_extent_m} m, z={zoom}, target: {out_path.name}")
    if out_path.exists() and out_path.stat().st_size > 1000:
        print(f"  Already exists ({out_path.stat().st_size / 1024:.0f} KB) — skipping")
        return
    dlat = half_extent_m / 111000
    dlon = half_extent_m / (111000 * math.cos(math.radians(CENTROID_LAT)))
    west = CENTROID_LON - dlon
    east = CENTROID_LON + dlon
    south = CENTROID_LAT - dlat
    north = CENTROID_LAT + dlat
    print(f"  AOI: ({west:.4f}, {south:.4f}, {east:.4f}, {north:.4f})")
    try:
        arr, transform = fetch_aoi_elevation(west, south, east, north, zoom)
        write_geotiff(arr, transform, out_path)
    except Exception as e:
        print(f"  ✗ Failed: {e}")


def main() -> int:
    print("=" * 60)
    print("LQV → Extended DEM fetch (LOD1 + LOD2) via AWS terrain-rgb")
    print("=" * 60)

    # LOD1: 7.7 km extent at z=13 (each tile ~5 km → 3×3 grid = ~15 km)
    fetch_lod(
        lod_id=1,
        half_extent_m=3850,
        zoom=13,  # each tile ~5 km at this lat → 3×3 tiles = ~15 km wide
        out_path=DEM_OUT_DIR / "extended_dem_lod1.tif",
    )

    # LOD2: 23 km extent at z=11 (each tile ~20 km → 3×3 grid = ~60 km)
    fetch_lod(
        lod_id=2,
        half_extent_m=11500,
        zoom=11,  # each tile ~20 km at this lat → 3×3 tiles = ~60 km wide
        out_path=DEM_OUT_DIR / "extended_dem_lod2.tif",
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())