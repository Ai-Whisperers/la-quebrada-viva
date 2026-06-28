"""Compose Sentinel-2 RGB × hillshade → 8-bit PNG cropped to the parcel core.

v3 (2026-06-11): reads the parcel-cropped bbox from escobar_height.json
(900 m × 900 m), windows each Sentinel-2 reflectance band to that bbox,
gain-corrects, then multiplies by a hillshade derived from the cropped DEM so
small relief reads visibly under the satellite albedo. Output is upsampled to
match the 512×512 heightmap, so Blender's Image Texture sampling aligns 1:1
between displace and base color.

Inputs:
  docs/site_data/sentinel2/S2B_21JVM_20260512_0_L2A_{red,green,blue}.tif
                                                    (10980² uint16, EPSG:32721)
  assets/terrain/escobar_height.json                 (cropped bbox + z range)
  assets/terrain/escobar_height.png                  (cropped 16-bit heightmap)

Output:
  assets/terrain/escobar_albedo.png                  (512² 8-bit RGB)

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
HEIGHT_PNG = os.path.join(PROJECT_ROOT, "assets", "terrain", "escobar_height.png")
DST_PNG = os.path.join(PROJECT_ROOT, "assets", "terrain", "escobar_albedo.png")

GAIN = 9.0
DN_FULL = 10000.0
TARGET_PX = 512

# Hillshade — sun NNW, low elevation to bias toward the same lighting as the
# winter golden-hour Variant A. Mixed at low strength so the satellite colors
# stay dominant.
SUN_AZIMUTH_DEG = 340.0
SUN_ELEVATION_DEG = 35.0
HILLSHADE_MIX = 0.30
HILLSHADE_GAMMA = 1.4


def _hillshade(z: np.ndarray, pixel_size_m: float) -> np.ndarray:
    dzdx = np.gradient(z, axis=1) / pixel_size_m
    dzdy = np.gradient(z, axis=0) / pixel_size_m
    slope = np.arctan(np.hypot(dzdx, dzdy))
    aspect = np.arctan2(-dzdx, dzdy)
    az = np.deg2rad(360.0 - SUN_AZIMUTH_DEG + 90.0)
    alt = np.deg2rad(SUN_ELEVATION_DEG)
    shade = (np.sin(alt) * np.cos(slope)
             + np.cos(alt) * np.sin(slope) * np.cos(az - aspect))
    return np.clip(shade, 0.0, 1.0)


def main() -> None:
    with open(HEIGHT_JSON) as f:
        meta = json.load(f)
    bbox = meta["bbox"]
    z_min = float(meta["z_min_m"])
    z_max = float(meta["z_max_m"])

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

    rgb_img = Image.fromarray((rgb_norm * 255.0).astype(np.uint8), mode="RGB")
    rgb_img = rgb_img.resize((TARGET_PX, TARGET_PX),
                             resample=Image.Resampling.BILINEAR)
    rgb_hi = np.asarray(rgb_img, dtype=np.float32) / 255.0

    z_norm = np.asarray(Image.open(HEIGHT_PNG), dtype=np.float32) / 65535.0
    z_m = z_min + z_norm * (z_max - z_min)
    pixel_size_m = (2.0 * meta["crop_half_extent_m"]) / TARGET_PX
    shade = _hillshade(z_m, pixel_size_m)
    shade = np.power(shade, 1.0 / HILLSHADE_GAMMA)
    shade_rgb = shade[..., None]
    blended = rgb_hi * ((1.0 - HILLSHADE_MIX) + HILLSHADE_MIX * shade_rgb)
    blended = np.clip(blended, 0.0, 1.0)

    out = (blended * 255.0).astype(np.uint8)
    Image.fromarray(out, mode="RGB").save(DST_PNG)
    print(f"[albedo] wrote {DST_PNG} ({out.shape[0]}x{out.shape[1]} 8-bit RGB)")
    print(f"[albedo] gain={GAIN} hillshade_mix={HILLSHADE_MIX} "
          f"pixel_size={pixel_size_m:.2f}m → mean L={blended.mean():.3f}")


if __name__ == "__main__":
    main()
