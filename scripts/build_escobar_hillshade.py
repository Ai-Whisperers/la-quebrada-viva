#!/usr/bin/env python3
"""
Build an Escobar-District-scale hillshade from the regional 30m Copernicus DEM.

Source DEM: docs/site_data/topology_lod/regional/cop30_30m.tif (~50x50 km box)
Target extent: actual Escobar District + 5 km buffer (Dpto Paraguarí).
Outputs:
  data/hillshade_escobar.jpg       — JPEG (web, ~50-200 KB)
  data/hillshade_escobar.png       — PNG fallback (higher quality)
  data/hillshade_escobar_bounds.json

Run as: python3 scripts/build_escobar_hillshade.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import rasterio
from rasterio.windows import Window
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC_DEM = ROOT / 'docs/site_data/topology_lod/regional/cop30_30m.tif'
DATA_DIR = ROOT / 'splats/exports/web/data'

# Real Escobar District bounds (Paraguarí dept) — from DGEEC Limits data,
# with a 5 km buffer so views have visual context.
W, S, E, N = -57.22, -25.78, -57.00, -25.46


def horn_hillshade(dem: np.ndarray, dx: float, dy: float,
                   azimuth: float = 315, altitude: float = 45,
                   nodata: float = 0) -> np.ndarray:
    """Classic Horn (1981) hillshade. dx/dy in the same units as `dem`."""
    az_rad = np.deg2rad(360 - azimuth + 90) % (2 * np.pi)
    alt_rad = np.deg2rad(altitude)

    # Pad dem to handle edges (replicate edge to avoid dark borders)
    p = np.pad(dem.astype(np.float64), 1, mode='edge')
    a = p[:-2, :-2]; b = p[:-2, 1:-1]; c = p[:-2, 2:]
    d = p[1:-1, :-2];             f = p[1:-1, 2:]
    g = p[2:, :-2];   h = p[2:, 1:-1];  i = p[2:, 2:]

    z_e = (c + 2*f + i) - (a + 2*d + g)
    z_n = (g + 2*h + i) - (a + 2*b + c)

    slope = np.arctan(np.sqrt(z_e*z_e + z_n*z_n) / (8 * max(dx, dy)))
    aspect = np.arctan2(z_e, z_n)

    hs = (np.cos(alt_rad) * np.cos(slope) +
          np.sin(alt_rad) * np.sin(slope) * np.cos(az_rad - aspect))
    hs = np.clip(hs * 255, 0, 255)
    invalid = (dem == nodata) | np.isnan(dem)
    hs[invalid] = 0
    return hs.astype(np.uint8)


def main():
    if not SRC_DEM.exists():
        sys.exit(f'source DEM not found: {SRC_DEM}')

    with rasterio.open(SRC_DEM) as src:
        # Compute pixel window for target extent.
        # Source is in EPSG:4326 (lon/lat), res is in degrees.
        res_lon = (src.bounds.right - src.bounds.left) / src.width
        res_lat = (src.bounds.top - src.bounds.bottom) / src.height

        col_min = max(0, int((W - src.bounds.left) / res_lon))
        col_max = min(src.width, int((E - src.bounds.left) / res_lon))
        row_min = max(0, int((src.bounds.top - N) / res_lat))
        row_max = min(src.height, int((src.bounds.top - S) / res_lat))
        width = col_max - col_min
        height = row_max - row_min
        print(f'Window: {width} × {height} pixels '
              f'({width * res_lon * 111:.1f} km × {height * res_lat * 111:.1f} km)')

        win = Window(col_min, row_min, width, height)
        dem = src.read(1, window=win)
        transform = src.window_transform(win)
        nodata = src.nodata if src.nodata is not None else 0
        valid = dem != nodata
        if not valid.any():
            sys.exit('window is entirely nodata — bounds may be wrong')
        print(f'DEM range: {dem[valid].min()}..{dem[valid].max()} m')

        # Cell size in degrees (close enough to uniform at this latitude).
        dx_deg = abs(transform.a)
        dy_deg = abs(transform.e)
        # Hillshade uses metres, so convert deg→m at this latitude.
        import math
        mid_lat_rad = math.radians((S + N) / 2)
        m_per_deg_lon = 111_320 * math.cos(mid_lat_rad)
        m_per_deg_lat = 111_320
        dx_m = dx_deg * m_per_deg_lon
        dy_m = dy_deg * m_per_deg_lat

        hs = horn_hillshade(dem, dx_m, dy_m, nodata=nodata)
        print(f'Hillshade shape: {hs.shape}')

        # Resize to a sensible web width. 4096 px = fine for the full district
        # at this size, keeps the JPG under 1 MB.
        max_w = 4096
        if hs.shape[1] > max_w:
            scale = max_w / hs.shape[1]
            new_h = max(1, int(hs.shape[0] * scale))
            img = Image.fromarray(hs, mode='L').resize((max_w, new_h), Image.LANCZOS)
        else:
            img = Image.fromarray(hs, mode='L')

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out_png = DATA_DIR / 'hillshade_escobar.png'
    out_jpg = DATA_DIR / 'hillshade_escobar.jpg'
    out_bounds = DATA_DIR / 'hillshade_escobar_bounds.json'

    img.save(out_png, 'PNG', optimize=True)
    img.convert('RGB').save(out_jpg, 'JPEG', quality=82, optimize=True, progressive=True)

    png_size = out_png.stat().st_size
    jpg_size = out_jpg.stat().st_size
    print(f'Wrote {out_png.name}: {png_size/1024:.0f} KB')
    print(f'Wrote {out_jpg.name}: {jpg_size/1024:.0f} KB')

    bounds = {'min_lon': W, 'min_lat': S, 'max_lon': E, 'max_lat': N}
    with open(out_bounds, 'w') as f:
        json.dump(bounds, f, indent=2)
    print(f'Wrote {out_bounds.name}: {bounds}')

    print('\nDone. Reload /mapa and the new "Escobar-wide hillshade" layer will appear.')


if __name__ == '__main__':
    main()
