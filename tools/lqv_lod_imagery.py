#!/usr/bin/env python3
"""
Generate distance-based satellite textures for the 3-tier LOD viewer.

Strategy:
  LOD0 (parcel, 0-500m):       Esri HD z=17 — 1.07 m/pixel, 1792×1792 (already exists)
  LOD1 (Escobar, 500m-5km):    Esri z=15  — 4.3 m/pixel, 1024×1024 (NEW)
  LOD2 (regional, 5-30km):     Esri z=11  — 70 m/pixel, 512×512 (NEW)

For LOD1 and LOD2 we fetch fresh Esri tiles covering the wider AOI.
Esri tiles are free (no key), used under attribution.
"""
from __future__ import annotations

import io
import math
import sys
import time
from pathlib import Path

import requests
from PIL import Image

REPO = Path("/root/la-quebrada-viva")
OUT_DIR = REPO / "docs" / "game_assets" / "textures" / "lods"
OUT_DIR.mkdir(parents=True, exist_ok=True)

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
    n = 2 ** z
    lon = x / n * 360.0 - 180.0
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    return lon, lat


def fetch_esri_tile(z: int, x: int, y: int, retries: int = 3) -> Image.Image:
    """Fetch a single 256×256 Esri World Imagery tile."""
    url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=30, headers={"User-Agent": "LQV-Pipeline/1.0"})
            r.raise_for_status()
            return Image.open(io.BytesIO(r.content)).convert("RGB")
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"Tile {z}/{y}/{x} failed after {retries} tries: {e}")


def fetch_aoi_imagery(west: float, south: float, east: float, north: float, zoom: int, target_px: int = 1024) -> tuple[Image.Image, dict]:
    """Fetch + stitch Esri imagery for an AOI at given zoom."""
    x_min, y_min = lonlat_to_tile(west, north, zoom)
    x_max, y_max = lonlat_to_tile(east, south, zoom)
    n_cols = x_max - x_min + 1
    n_rows = y_max - y_min + 1
    print(f"    z={zoom}: tile range x=[{x_min}, {x_max}] y=[{y_min}, {y_max}] = {n_cols}×{n_rows} tiles")

    canvas = Image.new("RGB", (n_cols * 256, n_rows * 256), (40, 40, 40))
    for r in range(n_rows):
        for c in range(n_cols):
            x = x_min + c
            y = y_min + r
            try:
                img = fetch_esri_tile(zoom, x, y)
                canvas.paste(img, (c * 256, r * 256))
            except Exception as e:
                print(f"      ⚠ tile {zoom}/{y}/{x}: {e} — black placeholder")
        print(f"    Fetched row {r + 1}/{n_rows}")

    # Crop to AOI
    tl_lon, tl_lat = tile_to_lonlat(x_min, y_min, zoom)
    tr_lon, _ = tile_to_lonlat(x_min + 1, y_min, zoom)
    _, bl_lat = tile_to_lonlat(x_min, y_min + 1, zoom)
    res_lon = (tr_lon - tl_lon) / 256
    res_lat = (tl_lat - bl_lat) / 256

    col_start = max(0, int(round((west - tl_lon) / res_lon)))
    col_end = min(canvas.width, int(round((east - tl_lon) / res_lon)))
    row_start = max(0, int(round((tl_lat - north) / res_lat)))
    row_end = min(canvas.height, int(round((tl_lat - south) / res_lat)))
    cropped = canvas.crop((col_start, row_start, col_end, row_end))
    print(f"    Cropped to AOI: {cropped.size}")

    # Resize to target
    if cropped.size[0] != target_px or cropped.size[1] != target_px:
        # Maintain aspect ratio
        aspect = cropped.size[0] / cropped.size[1]
        if aspect > 1:
            new_w = target_px
            new_h = int(target_px / aspect)
        else:
            new_h = target_px
            new_w = int(target_px * aspect)
        cropped = cropped.resize((new_w, new_h), Image.LANCZOS)

    new_tl_lon = tl_lon + col_start * res_lon
    new_tl_lat = tl_lat - row_start * res_lat
    new_res_lon = (tr_lon - tl_lon) * (256 / canvas.width)  # adjusted
    new_res_lat = (tl_lat - bl_lat) * (256 / canvas.height)
    # Recompute from actual cropped transform
    res_lon = (east - west) / cropped.size[0]
    res_lat = (north - south) / cropped.size[1]

    meta = {
        "bounds_wgs84": [west, south, east, north],
        "tile_zoom": zoom,
        "n_tiles": n_cols * n_rows,
        "resolution_m_per_pixel": abs(res_lon) * 111000 * math.cos(math.radians(CENTROID_LAT)),
        "size_pixels": list(cropped.size),
    }
    return cropped, meta


def main() -> int:
    print("=" * 60)
    print("LQV → Distance-based satellite textures")
    print(f"Output: {OUT_DIR}")
    print("=" * 60)

    # LOD1 — Escobar scale (~7.7 km, Esri z=15)
    lod1_path = OUT_DIR / "lod1_imagery.jpg"
    if lod1_path.exists() and lod1_path.stat().st_size > 1000:
        print(f"\n[LOD1] Already exists ({lod1_path.stat().st_size / 1024:.0f} KB) — skipping")
    else:
        half = 3850
        dlat = half / 111000
        dlon = half / (111000 * math.cos(math.radians(CENTROID_LAT)))
        w, e = CENTROID_LON - dlon, CENTROID_LON + dlon
        s, n = CENTROID_LAT - dlat, CENTROID_LAT + dlat
        print(f"\n[LOD1] AOI: ({w:.4f}, {s:.4f}, {e:.4f}, {n:.4f})")
        try:
            img, meta = fetch_aoi_imagery(w, s, e, n, zoom=15, target_px=1024)
            img.save(lod1_path, "JPEG", quality=85, optimize=True)
            print(f"    ✓ Wrote {lod1_path.name} ({lod1_path.stat().st_size / 1024:.0f} KB)")
            print(f"    Resolution: ~{meta['resolution_m_per_pixel']:.1f} m/pixel")
        except Exception as e:
            print(f"    ✗ Failed: {e}")

    # LOD2 — Regional scale (~23 km, Esri z=11)
    lod2_path = OUT_DIR / "lod2_imagery.jpg"
    if lod2_path.exists() and lod2_path.stat().st_size > 1000:
        print(f"\n[LOD2] Already exists ({lod2_path.stat().st_size / 1024:.0f} KB) — skipping")
    else:
        half = 11500
        dlat = half / 111000
        dlon = half / (111000 * math.cos(math.radians(CENTROID_LAT)))
        w, e = CENTROID_LON - dlon, CENTROID_LON + dlon
        s, n = CENTROID_LAT - dlat, CENTROID_LAT + dlat
        print(f"\n[LOD2] AOI: ({w:.4f}, {s:.4f}, {e:.4f}, {n:.4f})")
        try:
            img, meta = fetch_aoi_imagery(w, s, e, n, zoom=11, target_px=512)
            img.save(lod2_path, "JPEG", quality=80, optimize=True)
            print(f"    ✓ Wrote {lod2_path.name} ({lod2_path.stat().st_size / 1024:.0f} KB)")
            print(f"    Resolution: ~{meta['resolution_m_per_pixel']:.1f} m/pixel")
        except Exception as e:
            print(f"    ✗ Failed: {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())