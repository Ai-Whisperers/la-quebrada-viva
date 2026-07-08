"""Rebuild elevation_grid.json from extended_dem_lod2.tif (full 10km coverage).

Replaces the broken elevation_grid.json that was generated from cop30_dem.tif
(which only covers 3.3km × 5.5km, leaving 80% of the 10km box as 0-elevation
flat zones — that's why the cerros looked like pyramids floating on a flat
plane).
"""
import json
from pathlib import Path

import numpy as np
import rasterio
from rasterio.windows import from_bounds

ROOT = Path("/root/la-quebrada-viva")
SRC = ROOT / "docs/site_data/extended_aoi/dem/extended_dem_lod2.tif"
OUTS = [
    ROOT / "splats/exports/web/data/elevation_grid.json",
    ROOT / "splats/exports/web/game_assets_lite/elevation_grid.json",
    Path("/root/.hermes/lqv-splat/exports/web/data/elevation_grid.json"),
    Path("/root/.hermes/lqv-splat/exports/web/game_assets_lite/elevation_grid.json"),
]

BBOX_WSEN = (-57.130, -25.698, -56.931, -25.518)  # W, S, E, N


def main():
    with rasterio.open(SRC) as ds:
        win = from_bounds(*BBOX_WSEN, ds.transform)
        r0 = max(0, int(win.row_off))
        c0 = max(0, int(win.col_off))
        r1 = min(ds.height, int(win.row_off + win.height))
        c1 = min(ds.width, int(win.col_off + win.width))
        dem = ds.read(1, window=((r0, r1), (c0, c1))).astype(np.float32)
        tf = rasterio.windows.transform(((r0, r1), (c0, c1)), ds.transform)
        nodata = ds.nodata

        # Slope and aspect (Horn's method, 9-point stencil)
        dy, dx = np.gradient(dem, tf.e, tf.a)
        slope_pct = np.sqrt(dy**2 + dx**2) * 100
        aspect_rad = np.arctan2(-dy, dx)
        aspect_deg = (np.degrees(aspect_rad) + 360) % 360

    # Handle any nodata (shouldn't be many with lod2, but defensive)
    if nodata is not None:
        n_nodata = int((dem == nodata).sum())
        print(f"  nodata pixels in 10km box: {n_nodata}/{dem.size} ({100*n_nodata/dem.size:.2f}%)")
        if n_nodata > 0:
            valid_mask = dem != nodata
            if valid_mask.any():
                median = float(dem[valid_mask].median())
            else:
                median = 200.0
            # Bilinear-ish fill: use scipy if available
            try:
                from scipy.ndimage import generic_filter
                filled = dem.copy()
                # Simple 5x5 mean filter for nodata
                mask = (dem == nodata)
                if mask.any():
                    # Pad and compute mean of valid neighbors
                    padded = np.pad(dem, 3, mode='edge')
                    padded_mask = np.pad(mask, 3, mode='constant', constant_values=True)
                    # Use mean of valid 7x7 around each pixel
                    from scipy.ndimage import uniform_filter
                    valid_count = uniform_filter((~padded_mask).astype(np.float32), size=7)
                    valid_sum = uniform_filter(np.where(padded_mask, 0, padded), size=7)
                    mean_around = np.where(valid_count > 0, valid_sum / np.maximum(valid_count, 1e-9), median)
                    # Crop back
                    mean_around = mean_around[3:-3, 3:-3]
                    dem = np.where(mask, mean_around, dem)
                    print(f"  filled {n_nodata} nodata pixels via 7x7 mean (median fallback = {median:.0f}m)")
            except ImportError:
                dem = np.where(dem == nodata, median, dem)
                print(f"  filled {n_nodata} nodata pixels with median {median:.0f}m (no scipy)")

    print(f"  shape: {dem.shape}")
    print(f"  elev range: {dem.min():.0f} - {dem.max():.0f}m ({dem.max()-dem.min():.0f}m relief)")

    # Quantize
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
        "source": "extended_dem_lod2.tif (334x335 cells, ~23m/pixel, full 10km box coverage)",
    }

    for out_path in OUTS:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(out, separators=(",", ":")))
        print(f"wrote {out_path} ({out_path.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
