#!/usr/bin/env python3
"""
La Quebrada Viva → Esri World Imagery HD downloader for Cesium for Unreal.

Pulls a 7×7 tile grid of Esri World Imagery at z=17 around the LQV centroid.
At lat -25.63°, z=17 gives ~1.19 m/pixel resolution — photoreal satellite
imagery matching what Cesium for Unreal expects as the Bing/Esri aerial layer.

Output: docs/game_assets/textures/lqv_esri_z17_2km.png (~6 MB stitched)

Attribution (required): © Esri, Maxar, Earthstar Geographics, and the GIS User Community.
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

# LQV centroid (from aoi_62ha.geojson metadata)
CENTROID_LON = -57.030
CENTROID_LAT = -25.630
ZOOM = 17  # 1.19 m/pixel at this latitude
TILE_GRID = 7  # 7×7 tiles covers ~2.4 km × 2.4 km


def lonlat_to_tile(lon: float, lat: float, z: int) -> tuple[int, int]:
    """Slippy-map tile coords (matches Cesium's URL convention)."""
    n = 2 ** z
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int(
        (1.0 - math.log(math.tan(math.radians(lat)) + 1.0 / math.cos(math.radians(lat))) / math.pi)
        / 2.0
        * n
    )
    return xtile, ytile


def fetch_tile(z: int, x: int, y: int, retries: int = 3) -> Image.Image:
    """Fetch a single 256×256 tile from Esri World Imagery."""
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
            raise RuntimeError(f"Failed to fetch tile {z}/{y}/{x} after {retries} tries: {e}")


def main() -> int:
    print(f"Fetching Esri World Imagery z={ZOOM}, {TILE_GRID}×{TILE_GRID} grid around LQV centroid")
    print(f"Centroid: ({CENTROID_LON}, {CENTROID_LAT})")

    cx, cy = lonlat_to_tile(CENTROID_LON, CENTROID_LAT, ZOOM)
    print(f"Center tile: x={cx}, y={cy}, z={ZOOM}")

    # Compute tile bounds
    half = TILE_GRID // 2
    tiles = []
    for dy in range(-half, half + 1):
        row = []
        for dx in range(-half, half + 1):
            tx, ty = cx + dx, cy + dy
            row.append((tx, ty))
        tiles.append(row)

    # Fetch all tiles
    print(f"\nFetching {TILE_GRID * TILE_GRID} tiles...")
    images = []
    for row in tiles:
        img_row = []
        for tx, ty in row:
            try:
                img = fetch_tile(ZOOM, tx, ty)
                img_row.append(img)
                print(f"  ✓ tile z{ZOOM}/{ty}/{tx}", end="\r", flush=True)
            except Exception as e:
                print(f"\n  ✗ tile z{ZOOM}/{ty}/{tx}: {e}")
                # Fallback: black tile
                img_row.append(Image.new("RGB", (256, 256), (0, 0, 0)))
        images.append(img_row)
    print()

    # Stitch
    canvas = Image.new("RGB", (256 * TILE_GRID, 256 * TILE_GRID), (0, 0, 0))
    for r, row in enumerate(images):
        for c, img in enumerate(row):
            canvas.paste(img, (c * 256, r * 256))

    # Compute approximate ground resolution
    deg_per_tile = 360 / (2 ** ZOOM)
    m_per_tile_x = deg_per_tile * 111000 * math.cos(math.radians(CENTROID_LAT))
    m_per_tile_y = deg_per_tile * 111000
    m_per_pixel_x = m_per_tile_x / 256
    m_per_pixel_y = m_per_tile_y / 256

    out_path = OUT_DIR / "lqv_esri_z17_2km.png"
    canvas.save(out_path, optimize=True)
    print(f"\n✓ Wrote {out_path}")
    print(f"  Canvas: {canvas.size[0]}×{canvas.size[1]} px")
    print(f"  Ground coverage: ~{TILE_GRID * m_per_tile_x / 1000:.2f} km × ~{TILE_GRID * m_per_tile_y / 1000:.2f} km")
    print(f"  Ground resolution: {m_per_pixel_x:.2f} m/pixel (x), {m_per_pixel_y:.2f} m/pixel (y)")
    print(f"  File size: {out_path.stat().st_size / 1024 / 1024:.2f} MB")
    print(f"\nAttribution: © Esri, Maxar, Earthstar Geographics, and the GIS User Community")

    # Also write a small README for the textures dir
    readme = OUT_DIR / "README.md"
    readme.write_text(f"""# LQV Game Textures

This directory holds the photoreal satellite/imagery textures for the
Unreal Engine 5.7 + Cesium for Unreal build.

## Files

- `lqv_esri_z17_2km.png` — {TILE_GRID}×{TILE_GRID} tile grid from Esri World
  Imagery at z={ZOOM}, ~1.19 m/pixel at LQV latitude. Covers ~{TILE_GRID * m_per_tile_x / 1000:.1f} km
  × ~{TILE_GRID * m_per_tile_y / 1000:.1f} km centered on the LQV parcel centroid
  ({CENTROID_LON}, {CENTROID_LAT}).

## Attribution (required)

© Esri, Maxar, Earthstar Geographics, and the GIS User Community.

## How to use

Two options for Cesium for Unreal:

1. **Easiest**: Cesium ion Bing aerial layer (free tier, get a token at
   https://cesium.com/ion/tokens). Apply directly in the Cesium World Terrain +
   Bing Aerial combination.

2. **Offline**: import this PNG as a UE Texture2D, drape over the
   `Cesium3DTileset` terrain as a decal/material overlay. This works without
   any cloud token but is lower fidelity.

## Provenance

Generated by `tools/lqv_fetch_esri_hd.py` on-demand. The Esri tile server is
publicly accessible (no key) but rate-limited — if many users hit it
simultaneously you'll see HTTP 429. The script retries 3× with exponential
backoff.
""")
    print(f"  ✓ Wrote {readme}")
    return 0


if __name__ == "__main__":
    sys.exit(main())