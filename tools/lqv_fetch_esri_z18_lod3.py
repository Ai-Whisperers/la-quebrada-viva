#!/usr/bin/env python3
"""
LQV → Esri World Imagery z=18 HD downloader for the close-zoom LOD3.

At -25.63° lat, z=18 gives ~0.6 m/pixel resolution.
9x9 tile grid covers ~1.4 km x 1.4 km centered on the parcel centroid.

Output: docs/game_assets/textures/lqv_esri_z18_lod3.png
"""
from __future__ import annotations

import io
import math
import os
import sys
import time
from pathlib import Path

import requests
from PIL import Image

REPO_ROOT = Path("/root/la-quebrada-viva")
OUT_DIR = REPO_ROOT / "docs" / "game_assets" / "textures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CENTROID_LON = -57.030
CENTROID_LAT = -25.630
ZOOM = 18  # ~0.6 m/pixel
TILE_GRID = 9  # 9×9 = ~1.4 km × 1.4 km


def lonlat_to_tile(lon, lat, z):
    n = 2 ** z
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int(
        (1.0 - math.log(math.tan(math.radians(lat)) + 1.0 / math.cos(math.radians(lat))) / math.pi)
        / 2.0 * n
    )
    return xtile, ytile


def tile_to_lonlat(x, y, z):
    """Return (west, north, east, south) of a slippy tile."""
    n = 2 ** z
    west = x / n * 360.0 - 180.0
    east = (x + 1) / n * 360.0 - 180.0
    north_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    north = math.degrees(north_rad)
    south_rad = math.atan(math.sinh(math.pi * (1 - 2 * (y + 1) / n)))
    south = math.degrees(south_rad)
    return west, north, east, south


def fetch_tile(z, x, y, retries=3):
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
            raise RuntimeError(f"Failed z{z}/{y}/{x}: {e}")


def main():
    print(f"Esri z={ZOOM}, {TILE_GRID}×{TILE_GRID} tiles around LQV centroid")
    cx, cy = lonlat_to_tile(CENTROID_LON, CENTROID_LAT, ZOOM)
    print(f"Center tile: {cx}, {cy}")

    half = TILE_GRID // 2
    tiles = []
    for dy in range(-half, half + 1):
        row = []
        for dx in range(-half, half + 1):
            tx, ty = cx + dx, cy + dy
            row.append((tx, ty))
        tiles.append(row)

    images = []
    for row in tiles:
        img_row = []
        for tx, ty in row:
            try:
                img = fetch_tile(ZOOM, tx, ty)
                img_row.append(img)
                print(f"  ✓ z{ZOOM}/{ty}/{tx}", end="\r", flush=True)
            except Exception as e:
                print(f"\n  ✗ z{ZOOM}/{ty}/{tx}: {e}")
                img_row.append(Image.new("RGB", (256, 256), (90, 90, 90)))  # gray fallback
        images.append(img_row)
    print()

    canvas = Image.new("RGB", (256 * TILE_GRID, 256 * TILE_GRID))
    for r, row in enumerate(images):
        for c, img in enumerate(img_row if False else enumerate(row) and [im for _, im in enumerate(row)] if False else [(0, row)]):
            pass  # placeholder

    # simpler stitch:
    canvas = Image.new("RGB", (256 * TILE_GRID, 256 * TILE_GRID))
    for r, row in enumerate(images):
        for c, img in enumerate(row):
            canvas.paste(img, (c * 256, r * 256))

    # Compute bounds
    half_t = TILE_GRID // 2
    west, north, _, _ = tile_to_lonlat(cx - half_t, cy - half_t, ZOOM)
    _, _, east, south = tile_to_lonlat(cx + half_t, cy + half_t, ZOOM)

    # Compute ground resolution
    deg_per_tile = 360 / (2 ** ZOOM)
    m_per_tile_x = deg_per_tile * 111000 * math.cos(math.radians(CENTROID_LAT))
    m_per_pixel_x = m_per_tile_x / 256

    out_path = OUT_DIR / "lqv_esri_z18_lod3.png"
    canvas.save(out_path, optimize=True)
    print(f"✓ Wrote {out_path}")
    print(f"  {canvas.size[0]}×{canvas.size[1]} px")
    print(f"  Bounds: W={west:.6f} S={south:.6f} E={east:.6f} N={north:.6f}")
    print(f"  Resolution: {m_per_pixel_x:.3f} m/pixel")
    print(f"  Size: {out_path.stat().st_size / 1024 / 1024:.2f} MB")

    # Also write bounds JSON for the viewer
    import json
    bounds_path = OUT_DIR / "lqv_esri_z18_lod3_bounds.json"
    bounds_path.write_text(json.dumps({
        "west": west, "south": south, "east": east, "north": north,
        "width": canvas.size[0], "height": canvas.size[1],
        "resolution_m_per_pixel": m_per_pixel_x,
        "source": "Esri World Imagery z=18",
        "attribution": "© Esri, Maxar, Earthstar Geographics",
    }, indent=2))
    print(f"  Bounds: {bounds_path}")

    # Copy to game_assets_lite/assets/textures/ + textures/lods/
    lite_path = REPO_ROOT / "splats/exports/web/game_assets_lite/assets/textures/lqv_esri_z18_lod3.png"
    lite_path.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy(out_path, lite_path)
    print(f"✓ Copied to {lite_path}")


if __name__ == "__main__":
    sys.exit(main())
