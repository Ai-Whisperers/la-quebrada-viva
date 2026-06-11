"""Export ALOS AW3D30 GeoTIFF → 16-bit PNG + sidecar JSON for Blender displace.

One-shot artifact builder. Reads docs/site_data/alos_aw3d30_dem.tif (108×108
int16 elevation in metres, EPSG:4326, ~3.0 km bbox around the LQV parcel),
normalizes to [0,1] against the canonical 116-380 m relief range, and writes:

  assets/terrain/escobar_height.png   (16-bit grayscale, displace input)
  assets/terrain/escobar_height.json  (sidecar — bbox, z range, source SHA)

PIL-only — no imageio dependency. Idempotent. Run from project root:

  python3 scripts/make_terrain_heightmap.py
"""
from __future__ import annotations

import hashlib
import json
import os

import numpy as np
import rasterio
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(PROJECT_ROOT, "docs", "site_data", "alos_aw3d30_dem.tif")
DST_DIR = os.path.join(PROJECT_ROOT, "assets", "terrain")

Z_MIN = 116.0
Z_MAX = 380.0


def main() -> None:
    os.makedirs(DST_DIR, exist_ok=True)

    with rasterio.open(SRC) as src:
        z = src.read(1).astype(np.float32)
        bounds = src.bounds
        crs = str(src.crs)
        shape = list(z.shape)

    z_clip = np.clip(z, Z_MIN, Z_MAX)
    z_norm = (z_clip - Z_MIN) / (Z_MAX - Z_MIN)
    png16 = (z_norm * 65535.0).astype(np.uint16)
    png_path = os.path.join(DST_DIR, "escobar_height.png")
    Image.fromarray(png16, mode="I;16").save(png_path)

    sha = hashlib.sha256(open(SRC, "rb").read()).hexdigest()
    meta = {
        "source": os.path.relpath(SRC, PROJECT_ROOT),
        "source_sha256": sha,
        "z_min_m": Z_MIN,
        "z_max_m": Z_MAX,
        "z_observed_min_m": float(z.min()),
        "z_observed_max_m": float(z.max()),
        "z_observed_mean_m": float(z.mean()),
        "shape": shape,
        "crs": crs,
        "bbox": {
            "left": bounds.left,
            "bottom": bounds.bottom,
            "right": bounds.right,
            "top": bounds.top,
        },
    }
    json_path = os.path.join(DST_DIR, "escobar_height.json")
    with open(json_path, "w") as f:
        json.dump(meta, f, indent=2)

    print(f"[heightmap] wrote {png_path} ({shape[0]}x{shape[1]} 16-bit)")
    print(f"[heightmap] wrote {json_path}")
    print(f"[heightmap] z range: {z.min():.0f}–{z.max():.0f} m, mean {z.mean():.1f} m")


if __name__ == "__main__":
    main()
