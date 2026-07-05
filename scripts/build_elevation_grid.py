"""Build elevation_grid.json (270 KB) — DEM + slope + aspect sampled at
0.0003° resolution for the LQV 10 km box.

Used by the cursor HUD in mapa-10km.html (P1-6) to display elevation,
slope, and aspect in real time as the user pans the map.

The grid is 180×108 cells (WGS84). Values are quantized to uint16:
  - dem:    rounded to nearest metre
  - slope:  percentage × 10 (1 decimal precision)
  - aspect: 0-360 degrees
"""
import json
from pathlib import Path
import numpy as np
import rasterio
from rasterio.windows import from_bounds

ROOT = Path("/root/la-quebrada-viva")
OUT = ROOT / "splats/exports/web/data"

BBOX_WSEN = (-57.130, -25.698, -56.931, -25.518)  # W, S, E, N


def main():
    src = ROOT / "docs/site_data/extended_aoi/dem/cop30_dem.tif"
    with rasterio.open(src) as ds:
        win = from_bounds(*BBOX_WSEN, ds.transform)
        r0 = max(0, int(win.row_off)); c0 = max(0, int(win.col_off))
        r1 = min(ds.height, int(win.row_off + win.height))
        c1 = min(ds.width, int(win.col_off + win.width))
        dem = ds.read(1, window=((r0, r1), (c0, c1))).astype(np.float32)
        tf = rasterio.windows.transform(((r0, r1), (c0, c1)), ds.transform)
        # Compute slope and aspect (DEM gradient)
        dy, dx = np.gradient(dem, tf.e, tf.a)
        slope_pct = np.sqrt(dy**2 + dx**2) * 100
        aspect_rad = np.arctan2(-dy, dx)
        aspect_deg = (np.degrees(aspect_rad) + 360) % 360

    dem_q = np.round(dem).astype(np.uint16)
    slope_q = np.clip(np.round(slope_pct * 10), 0, 65535).astype(np.uint16)
    aspect_q = np.clip(np.round(aspect_deg), 0, 360).astype(np.uint16)

    out = {
        "bounds": list(BBOX_WSEN),
        "width": int(dem.shape[1]),
        "height": int(dem.shape[0]),
        "dem": dem_q.tolist(),
        "slope": slope_q.tolist(),
        "aspect": aspect_q.tolist(),
    }
    out_path = OUT / "elevation_grid.json"
    out_path.write_text(json.dumps(out, separators=(",", ":")))
    print(f"wrote {out_path} ({dem.shape[1]}x{dem.shape[0]} = "
          f"{dem.size:,} px, "
          f"{out_path.stat().st_size/1024:.0f} KB)")
    print(f"  elev range: {dem.min():.0f} - {dem.max():.0f} m")
    print(f"  slope range: {slope_pct.min():.1f} - {slope_pct.max():.1f} %")


if __name__ == "__main__":
    main()