"""Sentinel-2 NDVI → 8-bit grayscale density mask for flora scatter.

NDVI = (NIR - Red) / (NIR + Red). Healthy vegetation reads high (>0.5);
bare laterite, water, structures read low. We sample the same parcel bbox
as the heightmap/albedo (read from escobar_height.json) so the texture
aligns 1:1 with displace + base color, then re-map NDVI into a [0,1]
density signal that the tree scatter loop multiplies against random.random().

Output is a single-channel 512² 8-bit PNG; load in Blender as Non-Color.

Inputs:
  docs/site_data/sentinel2/S2B_21JVM_20260512_0_L2A_{red,nir}.tif
  assets/terrain/escobar_height.json

Output:
  assets/terrain/escobar_ndvi.png   (512² 8-bit single-channel)
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
DST_PNG = os.path.join(PROJECT_ROOT, "assets", "terrain", "escobar_ndvi.png")

TARGET_PX = 512
DN_FULL = 10000.0
EPS = 1e-6

# NDVI re-map: clip to [NDVI_FLOOR, NDVI_CEIL] then rescale to [0,1].
# Parcel is ~93% dense canopy (NDVI median 0.87, 5th pct 0.68). Floor=0.40
# excludes laterite paths / built / water (<1.5% of pixels) → 0 density.
# Ceil=0.85 is the parcel median, so anything denser saturates at 1.
NDVI_FLOOR = 0.40
NDVI_CEIL = 0.85


def main() -> None:
    with open(HEIGHT_JSON) as f:
        meta = json.load(f)
    bbox = meta["bbox"]

    bands = {}
    for color in ("red", "nir"):
        path = os.path.join(SENTINEL_DIR, f"{PREFIX}_{color}.tif")
        with rasterio.open(path) as src:
            left, bottom, right, top = transform_bounds(
                "EPSG:4326", src.crs,
                bbox["left"], bbox["bottom"], bbox["right"], bbox["top"],
            )
            window = from_bounds(left, bottom, right, top, transform=src.transform)
            arr = src.read(1, window=window).astype(np.float32) / DN_FULL
        bands[color] = arr

    red = bands["red"]
    nir = bands["nir"]
    ndvi = (nir - red) / (nir + red + EPS)
    ndvi = np.clip(ndvi, -1.0, 1.0)

    density = np.clip(
        (ndvi - NDVI_FLOOR) / (NDVI_CEIL - NDVI_FLOOR), 0.0, 1.0
    )

    img = Image.fromarray((density * 255.0).astype(np.uint8), mode="L")
    img = img.resize((TARGET_PX, TARGET_PX), resample=Image.Resampling.BILINEAR)
    img.save(DST_PNG)

    arr = np.asarray(img, dtype=np.float32) / 255.0
    print(f"[ndvi] wrote {DST_PNG} ({arr.shape[0]}x{arr.shape[1]} 8-bit L)")
    print(f"[ndvi] floor={NDVI_FLOOR} ceil={NDVI_CEIL} "
          f"mean={arr.mean():.3f} >0.5 frac={(arr > 0.5).mean():.3f}")


if __name__ == "__main__":
    main()
