"""Compute DEM contours every 25m elevation over the LQV 20 km box
using Copernicus GLO-30 in memory.

Output: splats/exports/web/data/dem_contours_20km.geojson
        splats/exports/web/data/dem_hillshade_color_20km.jpg  (color relief)
"""
import sys
from pathlib import Path
import json
import urllib.request
import io

import numpy as np
import rasterio
from rasterio.transform import xy as rio_xy
from rasterio.features import shapes as rio_shapes
from PIL import Image

ROOT = Path("/root/la-quebrada-viva")
OUT = ROOT / "splats/exports/web/data"

BBOX = (-25.787336, -57.231502, -25.427336, -56.839502)

URL_TEMPLATE = (
    "https://copernicus-dem-30m.s3.amazonaws.com/"
    "Copernicus_DSM_COG_10_{S}_00_{W}_00_DEM/"
    "Copernicus_DSM_COG_10_{S}_00_{W}_00_DEM.tif"
)
TILES = [("S26", "W058"), ("S26", "W057")]

ELEV_STEPS = [
    (100,  "#f0f9ff", "100 m"),
    (150,  "#bae6fd", "150 m"),
    (200,  "#7dd3fc", "200 m"),
    (250,  "#38bdf8", "250 m"),
    (300,  "#0ea5e9", "300 m"),
    (350,  "#0284c7", "350 m"),
    (400,  "#0369a1", "400 m"),
    (450,  "#075985", "450 m"),
    (500,  "#0c4a6e", "500 m"),
]


def log(m):
    print(f"[contour] {m}", file=sys.stderr, flush=True)


def fetch_tile(s, w):
    url = URL_TEMPLATE.format(S=s, W=w)
    log(f"  fetch {s} {w}")
    with urllib.request.urlopen(url, timeout=60) as r:
        return rasterio.open(io.BytesIO(r.read()))


def compute_contours():
    """Return list of LineString features, each a contour at a given elevation.
    Loads each tile independently, then crops each to the 20 km box and
    runs marching-squares on the union (avoids needing a stitched mosaic).
    """
    # Build mosaic by stitching the two tiles along the boundary
    srcs = [fetch_tile(s, w) for s, w in TILES]
    arrs = []
    bounds = []
    tfs = []
    for ds in srcs:
        arrs.append(ds.read(1).astype(np.float32))
        tfs.append(ds.transform)
        bounds.append(ds.bounds)
        ds.close()
    # Determine layout: W057 is west, W058 is east. Both cover same
    # south-to-north span. So horizontal mosaic.
    # Both tiles: same height (3600 rows), same transform row step.
    assert abs(arrs[0].shape[0] - arrs[1].shape[0]) < 5, "tile rows mismatch"
    dem_full = np.hstack([arrs[0], arrs[1]])
    # Transform for the stitched mosaic: a = pixel size (e.g. 0.000277),
    # c = left edge of W057 = bounds[0].left, f = top edge of W057
    t_west = tfs[0]   # W057
    transform = rasterio.Affine(
        t_west.a, 0.0,
        t_west.c, 0.0, t_west.e, t_west.f,
    )
    log(f"  mosaic shape: {dem_full.shape}")
    log(f"  elevation range: {np.nanmin(dem_full):.0f} – {np.nanmax(dem_full):.0f} m")
    # Crop to 20km box
    win = rasterio.windows.from_bounds(BBOX[1], BBOX[0], BBOX[3], BBOX[2], transform)
    r0 = max(0, int(win.row_off)); c0 = max(0, int(win.col_off))
    r1 = min(dem_full.shape[0], int(win.row_off + win.height))
    c1 = min(dem_full.shape[1], int(win.col_off + win.width))
    dem_crop = dem_full[r0:r1, c0:c1]
    crop_transform = rasterio.windows.transform(
        ((r0, r1), (c0, c1)), transform)
    log(f"  cropped: {dem_crop.shape}")
    # Make sure np.nan are replaced
    valid = ~np.isnan(dem_crop)
    median = float(np.nanmedian(dem_crop[valid]))
    dem_crop_filled = np.where(valid, dem_crop, median).astype(np.float32)
    # Polygonise contours at every 25m
    contours = []
    for elev, color, label in ELEV_STEPS:
        # rasterio.features.shapes with mask = (elevation >= elev) gives
        # polygon "areas above elev" — we need to invert.
        # Instead we use the technique of masking = (cell == elev) which
        # gives just those pixels, but that loses smoothness.
        # Use marching-squares via skimage to get clean line contours.
        try:
            from skimage import measure
        except ImportError:
            log("  ⚠ scikit-image not installed — skipping contour lines")
            return contours
        # Pad dem by 1px on edges so closed contours don't go missing
        padded = np.pad(dem_crop_filled, 1, mode="edge")
        try:
            cs = measure.find_contours(padded, level=elev)
        except Exception:
            continue
        # Convert pixel (row, col) back to lon/lat using the cropped transform
        # Since padded added 1 pixel at top + 1 left, subtract 1 from each.
        log(f"  {label}: {len(cs)} contour segments")
        for seg_idx, contour in enumerate(cs):
            # contour is shape (N, 2) of (row, col) in padded coords
            seg_pts = []
            for r, c in contour:
                rr, cc = r - 1, c - 1
                if not (0 <= rr < dem_crop.shape[0] and 0 <= cc < dem_crop.shape[1]):
                    continue
                lon, lat = rio_xy(crop_transform, cc, rr)
                seg_pts.append([float(lon), float(lat)])
            if len(seg_pts) < 2:
                continue
            contours.append({
                "type": "Feature",
                "properties": {
                    "category": "elevation_contour",
                    "elev_m": elev,
                    "elev_label": label,
                    "color": color,
                    "source": "Copernicus GLO-30 DEM, marching-squares contour",
                    "pixel_resolution_m": 30,
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": seg_pts,
                },
            })
    log(f"  total: {len(contours)} contour segments")
    return contours, dem_crop, crop_transform


def color_relief(dem_crop, transform):
    """Build a color-relief raster (RGBA PNG) from the elevation."""
    # Linear normalisation 0-1 across observed range
    valid = ~np.isnan(dem_crop)
    emin = float(np.nanmin(dem_crop[valid]))
    emax = float(np.nanmax(dem_crop[valid]))
    log(f"  relief range: {emin:.0f} – {emax:.0f} m")
    norm = (dem_crop - emin) / (emax - emin)
    norm = np.clip(norm, 0, 1)
    # Green-brown ramp — low = green flatland, high = brown upland
    r = (1.0 - norm) * 180 + norm * 145   # 180 -> 145
    g = (1.0 - norm) * 200 + norm * 90
    b = (1.0 - norm) * 150 + norm * 60
    rgba = np.zeros((dem_crop.shape[0], dem_crop.shape[1], 4), dtype=np.uint8)
    rgba[..., 0] = np.where(valid, r, 0).astype(np.uint8)
    rgba[..., 1] = np.where(valid, g, 0).astype(np.uint8)
    rgba[..., 2] = np.where(valid, b, 0).astype(np.uint8)
    rgba[..., 3] = np.where(valid, 80, 0).astype(np.uint8)
    # Save as JPEG via PIL
    img = Image.fromarray(rgba, mode="RGBA")
    # Resize down to keep file size small
    new_w = 4096
    new_h = int(img.height * new_w / img.width)
    img2 = img.resize((new_w, new_h), Image.LANCZOS)
    rgb = img2.convert("RGB")
    out_jpg = OUT / "dem_color_relief_20km.jpg"
    rgb.save(out_jpg, "JPEG", quality=80)
    log(f"  wrote {out_jpg} ({out_jpg.stat().st_size/1024/1024:.2f} MB)")
    # Save bounds JSON for viewer
    (OUT / "dem_color_relief_bounds.json").write_text(json.dumps({
        "min_lon": BBOX[1], "min_lat": BBOX[0],
        "max_lon": BBOX[3], "max_lat": BBOX[2],
        "elev_min": emin, "elev_max": emax,
    }, indent=2))


def main():
    log("=" * 60)
    log("DEM contours + colour relief — 20 km box")
    log("=" * 60)
    contours, dem_crop, transform = compute_contours()
    fc = {
        "type": "FeatureCollection",
        "name": "dem_contours_20km",
        "metadata": {
            "source": "Copernicus GLO-30 DEM, scikit-image marching-squares",
            "bbox": list(BBOX),
            "pixel_resolution_m": 30,
            "elev_steps_m": [s[0] for s in ELEV_STEPS],
            "feature_count": len(contours),
            "generated_utc": "2026-07-05",
        },
        "features": contours,
    }
    out = OUT / "dem_contours_20km.geojson"
    out.write_text(json.dumps(fc, separators=(",", ":")))
    log(f"wrote {out} ({out.stat().st_size/1024/1024:.2f} MB, {len(contours)} contour segments)")
    color_relief(dem_crop, transform)


if __name__ == "__main__":
    main()