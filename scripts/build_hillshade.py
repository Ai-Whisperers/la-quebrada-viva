"""Generate hillshade GeoTIFF (PNG via PNG export) covering the LQV 20 km
box, derived from Copernicus GLO-30 DEM.

Outputs:
  splats/exports/web/data/hillshade_20km.png  — 16-bit grayscale tile
  splats/exports/web/data/hillshade_bounds.json — {min_lon, min_lat, max_lon, max_lat}
"""
import sys
from pathlib import Path
import urllib.request
import io

import rasterio
from rasterio.transform import from_bounds
import numpy as np

ROOT = Path("/root/la-quebrada-viva")
OUT = ROOT / "splats/exports/web/data"
OUT.mkdir(parents=True, exist_ok=True)
BIG = ROOT / "splats/exports/big_data_excluded_from_deploy"
BIG.mkdir(parents=True, exist_ok=True)

BBOX = (-25.787336, -57.231502, -25.427336, -56.839502)
# Copernicus GLO-30 tiles for this bbox:
TILES = [
    ("S26", "W058"),
    ("S26", "W057"),
]
URL = "https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_{S}_00_{W}_00_DEM/Copernicus_DSM_COG_10_{S}_00_{W}_00_DEM.tif"

# Output image: 4096 wide × tall, dark hillshade RGBA
OUT_W = 4096


def fetch(tile):
    S, W = tile
    url = URL.format(S=S, W=W).replace("S26", "S26").replace("W057", "W057")
    url = f"https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_{S}_00_{W}_00_DEM/Copernicus_DSM_COG_10_{S}_00_{W}_00_DEM.tif"
    print(f"fetch {url}", file=sys.stderr)
    with urllib.request.urlopen(url, timeout=60) as r:
        return rasterio.open(io.BytesIO(r.read()))


def main():
    # Load 2 tiles
    dem_arrays = []
    bounds = []
    for tile in TILES:
        with fetch(tile) as ds:
            dem_arrays.append((ds.read(1).astype(np.float32), ds.transform))
            bounds.append(ds.bounds)
    # Compute mosaic bounds (union)
    min_x = min(b.left for b in bounds)
    max_y = max(b.top for b in bounds)
    max_x = max(b.right for b in bounds)
    min_y = min(b.bottom for b in bounds)
    mosaic_h = dem_arrays[0][0].shape[0] + dem_arrays[1][0].shape[0]
    mosaic_w = max(dem_arrays[0][0].shape[1], dem_arrays[1][0].shape[1])
    mosaic = np.full((mosaic_h, mosaic_w), np.nan, dtype=np.float32)
    mosaic[:dem_arrays[0][0].shape[0], :dem_arrays[0][0].shape[1]] = dem_arrays[0][0]
    mosaic[dem_arrays[0][0].shape[0]:, :dem_arrays[1][0].shape[1]] = dem_arrays[1][0]
    # Compute hillshade
    from numpy import gradient
    # Sun at azimuth 315°, altitude 45° — common default for north-west light
    azimuth = 315.0
    altitude = 45.0
    az_rad = np.radians(360.0 - azimuth)
    alt_rad = np.radians(altitude)
    # The DEM is in WGS84 degrees; for a single-pixel hillshade we use
    # simple degree-based gradients (sufficient for visualisation).
    z = 1.0 / (10.0 * np.cos(np.radians(mosaic / 111000)))
    # gradients in row/col
    dy, dx = np.gradient(mosaic)
    slope = np.arctan(np.sqrt(dx*dx + dy*dy))
    aspect = np.arctan2(-dx, dy)
    hs = (np.cos(alt_rad) * np.cos(slope)
          + np.sin(alt_rad) * np.sin(slope) * np.cos(az_rad - aspect))
    hs = np.clip(hs, 0, 1)
    # Mask NaN
    valid = ~np.isnan(mosaic)
    hs[~valid] = 0
    # Crop to LQV bbox + small margin
    src_transform = dem_arrays[0][1]
    src_crs = "EPSG:4326"
    # Crop by reading a window
    from rasterio.windows import from_bounds
    win = from_bounds(BBOX[1], BBOX[0], BBOX[3], BBOX[2], src_transform)
    r0 = int(win.row_off)
    c0 = int(win.col_off)
    r1 = min(int(win.row_off + win.height), hs.shape[0])
    c1 = min(int(win.col_off + win.width), hs.shape[1])
    hs_crop = hs[r0:r1, c0:c1]
    print(f"hillshade crop: {hs_crop.shape}", file=sys.stderr)
    # Downscale to OUT_W wide
    from PIL import Image
    img = Image.fromarray((hs_crop * 255).astype(np.uint8))
    new_w = OUT_W
    new_h = int(hs_crop.shape[0] * new_w / hs_crop.shape[1])
    img = img.resize((new_w, new_h), Image.LANCZOS)
    # Convert to RGBA with hillshade gradient (dark gray base + light gray high)
    arr = np.array(img.convert("L"))
    rgba = np.zeros((new_h, new_w, 4), dtype=np.uint8)
    rgba[..., 0] = 60     # base r
    rgba[..., 1] = 60     # base g
    rgba[..., 2] = 60     # base b
    # Brighten proportionally to hillshade value
    rgba[..., 0] = np.clip(rgba[..., 0] + arr * 1.0, 0, 255)
    rgba[..., 1] = np.clip(rgba[..., 1] + arr * 1.0, 0, 255)
    rgba[..., 2] = np.clip(rgba[..., 2] + arr * 1.0, 0, 255)
    rgba[..., 3] = (arr.astype(np.float32) * 0.95).astype(np.uint8)
    Image.fromarray(rgba, mode="RGBA").save(OUT / "hillshade_20km.png")
    # Save bounds for viewer
    import json
    (OUT / "hillshade_bounds.json").write_text(json.dumps({
        "min_lon": BBOX[1],
        "min_lat": BBOX[0],
        "max_lon": BBOX[3],
        "max_lat": BBOX[2],
        "size": [new_w, new_h],
    }, indent=2))
    print(f"wrote {OUT / 'hillshade_20km.png'} ({new_w}x{new_h}, RGBA)", file=sys.stderr)


if __name__ == "__main__":
    main()