"""Compose Sentinel-2 RGB (red+green+blue) → 8-bit PNG cropped to the DEM bbox.

Reads docs/site_data/sentinel2/S2B_21JVM_20260512_0_L2A_{red,green,blue}.tif
(10980×10980 uint16 surface-reflectance DN at 10 m, EPSG:32721 UTM 21S),
crops to the WGS84 bbox of the canonical ALOS DEM, gain-corrects to a
viewable LDR range, and writes:

  assets/terrain/escobar_albedo.png   (8-bit RGB, ground texture for Blender)

Run from project root:

  python3 scripts/make_terrain_albedo.py
"""
from __future__ import annotations

import json
import os

import numpy as np
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SENTINEL_DIR = os.path.join(PROJECT_ROOT, "docs", "site_data", "sentinel2")
PREFIX = "S2B_21JVM_20260512_0_L2A"
HEIGHT_JSON = os.path.join(PROJECT_ROOT, "assets", "terrain", "escobar_height.json")
DST_PNG = os.path.join(PROJECT_ROOT, "assets", "terrain", "escobar_albedo.png")

GAIN = 3.5
DN_FULL = 10000.0


def main() -> None:
    with open(HEIGHT_JSON) as f:
        meta = json.load(f)
    bbox = meta["bbox"]

    bands = []
    for color in ("red", "green", "blue"):
        path = os.path.join(SENTINEL_DIR, f"{PREFIX}_{color}.tif")
        with rasterio.open(path) as src:
            left, bottom, right, top = transform_bounds(
                "EPSG:4326", src.crs,
                bbox["left"], bbox["bottom"], bbox["right"], bbox["top"],
            )
            window = from_bounds(left, bottom, right, top, transform=src.transform)
            arr = src.read(1, window=window).astype(np.float32)
        bands.append(arr)

    rgb = np.stack(bands, axis=-1)
    rgb_norm = np.clip((rgb / DN_FULL) * GAIN, 0.0, 1.0)
    rgb8 = (rgb_norm * 255.0).astype(np.uint8)
    Image.fromarray(rgb8, mode="RGB").save(DST_PNG)
    print(f"[albedo] wrote {DST_PNG} ({rgb8.shape[0]}x{rgb8.shape[1]} 8-bit RGB)")
    print(f"[albedo] gain={GAIN} dn_full={DN_FULL} → "
          f"mean luminance {rgb_norm.mean():.3f}")


if __name__ == "__main__":
    main()
