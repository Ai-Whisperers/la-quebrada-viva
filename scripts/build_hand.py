"""Compute HAND (Height Above Nearest Drainage) for the LQV 10 km box.

HAND is the standard wetland-floodplain mapper. For each pixel we find
the nearest cell with high flow-accumulation (a 'stream') and compute
the elevation difference. Pixels with HAND < 5m are floodplain,
5-15m are riparian wetlands, 15-30m are upland-transition, >30m
is upland.

This catches the property-scale hydrology that JRC 30m misses.

Inputs:
  - Copernicus GLO-30 DEM (already cached at docs/site_data/extended_aoi/dem/cop30_dem.tif)
  - Flow accumulation from scripts/build_10km_layers.py logic

Outputs:
  - splats/exports/web/data/hand_10km.geojson (4-class polygons)
  - splats/exports/web/data/hand_10km.png (continuous grayscale raster)
"""
import json
import sys
from pathlib import Path
import numpy as np
import rasterio
from rasterio.features import shapes as rio_shapes
from shapely.geometry import shape, mapping
from shapely.validation import make_valid
from pyproj import Geod

ROOT = Path("/root/la-quebrada-viva")
OUT = ROOT / "splats/exports/web/data"

BBOX_WSEN = (-57.130, -25.698, -56.931, -25.518)  # W, S, E, N

# HAND class bins (meters)
HAND_BINS = [
    (0,    1,   1, "Floodplain",        "#0ea5e9",
     "Standing water or frequently flooded"),
    (1,    5,   2, "Riparian wetland",  "#22d3ee",
     "Riparian zone, seasonal saturation"),
    (5,    15,  3, "Hillslope wetland", "#67e8f9",
     "Hillslope seeps, colluvial hollows"),
    (15,   100, 4, "Upland",            "#e2e8f0",
     "Upland — well-drained above local drainage"),
]

geod = Geod(ellps="WGS84")


def log(m):
    print(f"[hand] {m}", file=sys.stderr, flush=True)


def load_dem():
    """Load DEM for the 10 km box."""
    src = ROOT / "docs/site_data/extended_aoi/dem/cop30_dem.tif"
    with rasterio.open(src) as ds:
        from rasterio.windows import from_bounds
        win = from_bounds(*BBOX_WSEN, ds.transform)
        r0 = max(0, int(win.row_off)); c0 = max(0, int(win.col_off))
        r1 = min(ds.height, int(win.row_off + win.height))
        c1 = min(ds.width, int(win.col_off + win.width))
        dem = ds.read(1, window=((r0, r1), (c0, c1))).astype(np.float32)
        tf = rasterio.windows.transform(((r0, r1), (c0, c1)), ds.transform)
        return dem, tf


def flow_acc(dem):
    """D8 flow accumulation (cells contributing to each cell)."""
    h, w = dem.shape
    fdir = np.zeros_like(dem, dtype=np.int8)
    # D8 directions: 0=E, 1=SE, 2=S, 3=SW, 4=W, 5=NW, 6=N, 7=NE
    dyx = [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]
    for y in range(h):
        for x in range(w):
            best = -1
            best_dh = 0
            for i, (dy, dx) in enumerate(dyx):
                ny, nx = y+dy, x+dx
                if 0 <= ny < h and 0 <= nx < w:
                    dh = dem[y, x] - dem[ny, nx]
                    if dh > best_dh:
                        best_dh = dh
                        best = i
            fdir[y, x] = best

    acc = np.ones((h, w), dtype=np.int32)
    # Topological sort: process cells in descending elevation order
    order = np.argsort(-dem.ravel())
    flat_idx = np.arange(h*w).reshape(h, w)
    for idx in order:
        y, x = idx // w, idx % w
        d = fdir[y, x]
        if d < 0:
            continue
        dy, dx = dyx[d]
        ny, nx = y+dy, x+dx
        if 0 <= ny < h and 0 <= nx < w:
            acc[ny, nx] += acc[y, x]
    return acc, fdir


def nearest_drainage_height(dem, acc, threshold=200):
    """For each cell, find nearest drainage cell (acc >= threshold)
    and compute elevation difference."""
    h, w = dem.shape
    # Mark drainage cells
    is_drain = acc >= threshold
    if not is_drain.any():
        # Threshold too high — fall back to using lowest 10% of cells
        thresh = np.percentile(acc, 90)
        is_drain = acc >= thresh
    log(f"  drainage cells: {is_drain.sum():,} (threshold=acc≥{threshold})")
    # BFS from drainage cells outward, fill distances
    # Use a coarse distance transform via scipy if available
    try:
        from scipy.ndimage import distance_transform_edt
        # Distance in cells from nearest drainage
        dist_cells = distance_transform_edt(~is_drain)
        # For each cell, find nearest drainage elevation
        # Use a simple approach: assign nearest drainage elevation via
        # argmin of |dem - drain_elev| for each pixel in a small window
        # Too slow for big rasters; alternative: use a coarse local search
        # Quick approximation: take min of dem over a small kernel centred
        # on each pixel.
        from scipy.ndimage import minimum_filter
        # minimum_filter finds local minimum in a window — set window
        # to a function of distance: bigger window for pixels farther
        # from drainage.
        # Simpler: use a multi-scale minimum_filter via dilation.
        # We'll do 5 scales and take the minimum.
        drain_elev = dem.copy()
        drain_elev[~is_drain] = np.inf
        # Replace is_drain cells with their own elevation, propagate
        # outward via minimum_filter with growing window
        cur = drain_elev.copy()
        for r in [2, 4, 8, 16, 32, 64]:
            cur = minimum_filter(cur, size=r)
        # HAND = dem - nearest drainage elevation
        hand = dem - cur
        hand[~np.isfinite(hand)] = 0
        hand = np.clip(hand, 0, 200)
        return hand
    except ImportError:
        log("  scipy not available, falling back to simple per-cell BFS")
        hand = np.full(dem.shape, np.nan, dtype=np.float32)
        # Quick BFS from each cell to find nearest drainage
        for y in range(0, h, 4):
            for x in range(0, w, 4):
                if is_drain[y, x]:
                    hand[y, x] = 0
                    continue
                # Find nearest drainage cell
                # (Cheap approximation: scan outward in spirals)
                found = None
                for r in range(1, 50):
                    for dy in range(-r, r+1):
                        for dx in range(-r, r+1):
                            ny, nx = y+dy, x+dx
                            if 0 <= ny < h and 0 <= nx < w and is_drain[ny, nx]:
                                found = (ny, nx)
                                break
                        if found: break
                    if found: break
                if found:
                    hand[y, x] = max(0, dem[y, x] - dem[found])
                else:
                    hand[y, x] = 100  # fallback
        return hand


def main():
    log("Loading DEM...")
    dem, tf = load_dem()
    log(f"  DEM shape: {dem.shape}, range: {dem.min():.1f}-{dem.max():.1f} m")

    log("Computing flow accumulation (D8)...")
    acc, fdir = flow_acc(dem)
    log(f"  acc max: {acc.max()} cells, threshold {acc.max()//10}")

    log("Computing HAND...")
    hand = nearest_drainage_height(dem, acc, threshold=max(200, int(acc.max()/10)))
    log(f"  HAND range: {hand.min():.2f}-{hand.max():.2f} m")

    # Polygonise each class
    log("Polygonising HAND classes...")
    all_feats = []
    for lo, hi, code, name, color, desc in HAND_BINS:
        mask = (hand >= lo) & (hand < hi)
        n_px = int(mask.sum())
        log(f"  class {code} ({name}, {lo}-{hi} m): {n_px} px")
        for geom, val in rio_shapes(hand.astype(np.int32), mask=mask,
                                    connectivity=8, transform=tf):
            try:
                g = shape(geom)
                if not g.is_valid:
                    g = make_valid(g)
                if g.is_empty or g.area < 1e-7:
                    continue
                g_simple = g.simplify(0.0002, preserve_topology=True)
                # area in ha
                c_lat = g_simple.centroid.y
                deg_lat_m = 111320
                deg_lon_m = 111320 * math.cos(abs(c_lat) * math.pi/180)
                area_ha = (g_simple.area * deg_lat_m * deg_lon_m) / 10000
                all_feats.append({
                    "type": "Feature",
                    "properties": {
                        "category": "hand",
                        "class": code,
                        "name": name,
                        "color": color,
                        "hand_low_m": lo,
                        "hand_high_m": hi,
                        "description": desc,
                        "area_ha": round(area_ha, 2),
                    },
                    "geometry": mapping(g_simple),
                })
            except Exception:
                continue

    log(f"  total polygons: {len(all_feats):,}")
    fc = {
        "type": "FeatureCollection",
        "name": "hand_10km",
        "metadata": {
            "source": "Hand-computed HAND raster from Copernicus GLO-30 DEM + D8 flow accumulation",
            "method": "minimum_filter multi-scale nearest drainage lookup",
            "bbox_s_w_n_e": list(BBOX_WSEN[::-1]),
            "license": "Derived from Copernicus DEM (open)",
        },
        "features": all_feats,
    }
    out = OUT / "hand_10km.geojson"
    out.write_text(json.dumps(fc, separators=(",", ":")))
    log(f"wrote {out} ({out.stat().st_size/1024/1024:.2f} MB)")

    # Also save the HAND raster as a PNG for visual reference
    log("Rendering HAND PNG...")
    from PIL import Image
    h, w = hand.shape
    # Normalise to 0-255 (0=low HAND = wet, 255=high HAND = dry)
    hand_norm = ((hand - hand.min()) / (hand.max() - hand.min()) * 255).astype(np.uint8)
    img = Image.fromarray(hand_norm, mode='L')
    img_path = OUT / "hand_10km.png"
    img.save(img_path, optimize=True)
    log(f"wrote {img_path} ({img_path.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    import math
    main()