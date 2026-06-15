"""Export ALOS AW3D30 GeoTIFF → 16-bit PNG + sidecar JSON for Blender displace.

v3 (2026-06-11): crops the source DEM to a 900 m × 900 m square centred on the
parcel (matches WORLD_SIZE in `lqv/subscene/terrain_62ha.py`), then resamples
to 512×512 so the displace UV gets ~1.8 m / px effective sampling. Reads
docs/site_data/alos_aw3d30_dem.tif (108×108 int16 elevation in metres,
EPSG:4326, ~3.0 km bbox), windows to the parcel core, normalizes against the
*cropped* relief range, and writes:

  assets/terrain/escobar_height.png   (16-bit grayscale, displace input)
  assets/terrain/escobar_height.json  (sidecar — cropped bbox, z range, SHA)

PIL-only — no imageio dependency. Idempotent. Run from project root:

  python3 scripts/make_terrain_heightmap.py
"""
from __future__ import annotations

import hashlib
import json
import math
import os

import numpy as np
import rasterio
from rasterio.windows import from_bounds
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SRC = os.path.join(PROJECT_ROOT, "docs", "site_data", "alos_aw3d30_dem.tif")
DST_DIR = os.path.join(PROJECT_ROOT, "assets", "terrain")

# Env overrides — swap DEM source without editing this file.
#   LQV_DEM_SRC : absolute or PROJECT_ROOT-relative path to source GeoTIFF
#                 (default: ALOS AW3D30). Use to swap in COP30 etc.
#   LQV_DEM_TAG : output suffix; "" overwrites the default
#                 escobar_height.png/.json, "cop30" writes
#                 escobar_height_cop30.png/.json side-by-side so the
#                 ALOS baseline stays on disk for A/B comparisons.
_env_src = os.environ.get("LQV_DEM_SRC", "").strip()
if _env_src:
    SRC = _env_src if os.path.isabs(_env_src) else os.path.join(PROJECT_ROOT, _env_src)
else:
    SRC = DEFAULT_SRC
_TAG = os.environ.get("LQV_DEM_TAG", "").strip()
_SUFFIX = f"_{_TAG}" if _TAG else ""

# Parcel-focused crop. WORLD_SIZE in the Blender scene is 900 m, so the PNG
# must represent exactly that. Center = source DEM center (the .tif was fetched
# centered on the parcel). Half-extent = 450 m.
HALF_EXTENT_M = 450.0
TARGET_PX = 512


def main() -> None:
    os.makedirs(DST_DIR, exist_ok=True)

    with rasterio.open(SRC) as src:
        src_bounds = src.bounds
        cx = 0.5 * (src_bounds.left + src_bounds.right)
        cy = 0.5 * (src_bounds.bottom + src_bounds.top)
        dlat = HALF_EXTENT_M / 111000.0
        dlon = HALF_EXTENT_M / (111000.0 * math.cos(math.radians(cy)))
        crop_left = cx - dlon
        crop_right = cx + dlon
        crop_bottom = cy - dlat
        crop_top = cy + dlat

        window = from_bounds(crop_left, crop_bottom, crop_right, crop_top,
                             transform=src.transform)
        z_crop = src.read(1, window=window).astype(np.float32)
        crs = str(src.crs)

    z_min = float(z_crop.min())
    z_max = float(z_crop.max())
    z_range = max(1.0, z_max - z_min)
    z_norm = (z_crop - z_min) / z_range
    z_norm = np.clip(z_norm, 0.0, 1.0)
    img_lo = Image.fromarray((z_norm * 65535.0).astype(np.uint16), mode="I;16")
    img_hi = img_lo.resize((TARGET_PX, TARGET_PX), resample=Image.Resampling.BILINEAR)

    png_path = os.path.join(DST_DIR, f"escobar_height{_SUFFIX}.png")
    img_hi.save(png_path)

    sha = hashlib.sha256(open(SRC, "rb").read()).hexdigest()
    meta = {
        "source": os.path.relpath(SRC, PROJECT_ROOT),
        "source_sha256": sha,
        "z_min_m": z_min,
        "z_max_m": z_max,
        "z_observed_min_m": z_min,
        "z_observed_max_m": z_max,
        "z_observed_mean_m": float(z_crop.mean()),
        "shape": [TARGET_PX, TARGET_PX],
        "source_shape": list(z_crop.shape),
        "crs": crs,
        "crop_half_extent_m": HALF_EXTENT_M,
        "bbox": {
            "left": crop_left,
            "bottom": crop_bottom,
            "right": crop_right,
            "top": crop_top,
        },
        "source_bbox": {
            "left": src_bounds.left,
            "bottom": src_bounds.bottom,
            "right": src_bounds.right,
            "top": src_bounds.top,
        },
    }
    json_path = os.path.join(DST_DIR, f"escobar_height{_SUFFIX}.json")
    with open(json_path, "w") as f:
        json.dump(meta, f, indent=2)

    print(f"[heightmap] cropped {z_crop.shape[0]}x{z_crop.shape[1]} → {TARGET_PX}x{TARGET_PX} 16-bit")
    print(f"[heightmap] bbox lon=[{crop_left:.5f},{crop_right:.5f}] lat=[{crop_bottom:.5f},{crop_top:.5f}]")
    print(f"[heightmap] z range: {z_min:.0f}–{z_max:.0f} m, mean {z_crop.mean():.1f} m")
    print(f"[heightmap] wrote {png_path}")
    print(f"[heightmap] wrote {json_path}")


if __name__ == "__main__":
    main()
