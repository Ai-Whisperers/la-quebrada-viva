"""Build DEM-derived quebrada streams for the LQV 20 km box.

Standalone runner: does NOT write the 122 MB DEM intermediate.
Fetches GLO-30 tiles, runs D8 flow direction + accumulation in memory,
and writes only the stream-network LineString GeoJSON (typically
a few MB) — deployable.

Outputs:
  - splats/exports/web/data/dem_streams_10km.geojson
      Stream segments classified into main / tributary / headwater
      based on upstream drainage area.
"""
from __future__ import annotations

import json
import math
import time
import urllib.request
from datetime import datetime
from io import BytesIO
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import xy as rio_xy
from rasterio.warp import reproject, Resampling

ROOT = Path("/root/la-quebrada-viva")
OUT = ROOT / "splats/exports/web/data"
OUT.mkdir(parents=True, exist_ok=True)

# Same 20 km bbox as everything else
BBOX = (-25.698062, -57.129997, -25.518400, -56.930765)  # S, W, N, E


def log(msg):
    print(f"[{datetime.utcnow().strftime('%H:%M:%S')}] {msg}", flush=True)


# ----------------------------------------------------------------------
# 1. Copernicus GLO-30 fetch (2 tiles for the 20 km box — completely in-memory)
# ----------------------------------------------------------------------
def fetch_dem_in_memory() -> tuple[np.ndarray, rasterio.Affine]:
    """Return (DEM 2-D array, rasterio.Affine) mosaicked from the two
    GLO-30 tiles that cover the 20 km box. Cropped to the bbox. Downsampled
    6× (180 m) to keep D8+flow-accum tractable. No disk writes."""
    log("Fetching Copernicus GLO-30 from AWS S3 (in-memory)...")

    s, w, n, e = BBOX
    lats = [math.floor(s), math.ceil(n) - 1]
    lons = [math.floor(w), math.ceil(e) - 1]
    urls = []
    seen = set()
    for lat in lats:
        for lon in lons:
            if (lat, lon) in seen:
                continue
            seen.add((lat, lon))
            lat_str = f"N{abs(lat):02d}_00" if lat >= 0 else f"S{abs(lat):02d}_00"
            lon_str = f"E{abs(lon):03d}_00" if lon >= 0 else f"W{abs(lon):03d}_00"
            folder = f"Copernicus_DSM_COG_10_{lat_str}_{lon_str}_DEM"
            tif = f"Copernicus_DSM_COG_10_{lat_str}_{lon_str}_DEM.tif"
            urls.append((
                lat, lon,
                f"https://copernicus-dem-30m.s3.eu-central-1.amazonaws.com/{folder}/{tif}"
            ))

    rasters = []
    for lat, lon, url in urls:
        try:
            log(f"  fetching {url.rsplit('/', 1)[-1]}")
            req = urllib.request.Request(url, headers={"User-Agent": "lqv-20km-streams/1.0"})
            with urllib.request.urlopen(req, timeout=90) as r:
                data = BytesIO(r.read())
            with rasterio.open(data) as src:
                arr = src.read(1).astype(np.float32)
                nd = src.nodata
                if nd is not None:
                    arr[arr == nd] = np.nan
                rasters.append((src.transform, src.crs, arr))
                log(f"    OK {arr.shape}, bbox {src.bounds}")
        except Exception as e:
            log(f"    skip: {e}")

    if not rasters:
        raise SystemExit("Could not fetch any Copernicus GLO-30 tile")

    # Build a 30 m mosaic onto the LQV bbox
    target_res_deg = 0.00009259259  # ≈1 arcsec ≈ 30 m at equator
    dst_w = max(1, int((BBOX[3] - BBOX[1]) / target_res_deg))
    dst_h = max(1, int((BBOX[2] - BBOX[0]) / target_res_deg))
    dst_transform = rasterio.Affine.translation(
        BBOX[1] - target_res_deg / 2,
        BBOX[2] + target_res_deg / 2
    ) * rasterio.Affine.scale(target_res_deg, -target_res_deg)
    src_crs = rasters[0][1]
    full = np.full((dst_h, dst_w), np.nan, dtype=np.float32)
    for tr2, crs2, arr2 in rasters:
        dst = np.zeros((dst_h, dst_w), dtype=np.float32)
        reproject(
            source=arr2, destination=dst,
            src_transform=tr2, src_crs=crs2,
            dst_transform=dst_transform, dst_crs=src_crs,
            resampling=Resampling.bilinear,
            src_nodata=np.nan, dst_nodata=np.nan,
        )
        m = ~np.isnan(dst)
        full[m] = dst[m]
    log(f"  mosaic: {full.shape}")
    return full, dst_transform


# ----------------------------------------------------------------------
# 2. D8 flow direction + accumulation (in memory, no disk writes)
# ----------------------------------------------------------------------
def d8_flow_dir(dem: np.ndarray) -> np.ndarray:
    """Return D8 direction grid (int8). 0 = no flow."""
    h, w = dem.shape
    fdir = np.zeros((h, w), dtype=np.int8)
    valid = ~np.isnan(dem)
    dy = np.array([0, 1, 1, 1, 0, -1, -1, -1])
    dx = np.array([1, 1, 0, -1, -1, -1, 0, 1])
    POWERS = np.array([64, 128, 1, 2, 4, 8, 16, 32], dtype=np.int32)
    best = np.full((h, w), -1e9, dtype=np.float32)
    for k in range(8):
        ddy, ddx = int(dy[k]), int(dx[k])
        if ddy == 0 and ddx == 0:
            continue
        if ddy >= 0:
            src_y0, dst_y0 = ddy, 0
            src_y1, dst_y1 = h, h - ddy
        else:
            src_y0, dst_y0 = 0, -ddy
            src_y1, dst_y1 = h + ddy, h
        if ddx >= 0:
            src_x0, dst_x0 = ddx, 0
            src_x1, dst_x1 = w, w - ddx
        else:
            src_x0, dst_x0 = 0, -ddx
            src_x1, dst_x1 = w + ddx, w
        if dst_y1 <= dst_y0 or dst_x1 <= dst_x0:
            continue
        h_src = dem[src_y0:src_y1, src_x0:src_x1]
        h_dst = dem[dst_y0:dst_y1, dst_x0:dst_x1]
        dist = math.sqrt(2) if (k % 2) else 1.0
        with np.errstate(invalid="ignore"):
            drop = (h_dst - h_src) / dist
        valid_slice = (~np.isnan(h_src)) & (~np.isnan(h_dst))
        take = (drop > best[dst_y0:dst_y1, dst_x0:dst_x1]) & valid_slice
        cur = fdir[dst_y0:dst_y1, dst_x0:dst_x1]
        cur = np.where(take, POWERS[k], cur)
        fdir[dst_y0:dst_y1, dst_x0:dst_x1] = cur
        best[dst_y0:dst_y1, dst_x0:dst_x1] = np.where(
            take, drop, best[dst_y0:dst_y1, dst_x0:dst_x1]
        )
    fdir[~valid] = 0
    return fdir


def flow_accumulation(dem: np.ndarray, fdir: np.ndarray) -> np.ndarray:
    """Classic in-decreasing-elevation order sweep (topological sort)."""
    h, w = dem.shape
    acc = np.ones((h, w), dtype=np.int64)
    valid = ~np.isnan(dem)
    p2o = {64: (0, 1), 128: (1, 1), 1: (1, 0), 2: (1, -1),
           4: (0, -1), 8: (-1, -1), 16: (-1, 0), 32: (-1, 1)}
    fdir_flat = fdir.ravel()
    valid_flat = valid.ravel()
    acc_flat = acc.ravel()
    order = np.argsort(-dem, axis=None, kind='mergesort')
    log(f"  {len(order):,} cells in topo sweep...")
    t0 = time.time()
    for idx in order:
        if not valid_flat[idx]:
            continue
        code = fdir_flat[idx]
        if code == 0:
            continue
        dy, dx = p2o.get(int(code), (0, 0))
        y, x = divmod(int(idx), w)
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w and valid[ny, nx]:
            acc_flat[ny * w + nx] += acc_flat[idx]
    log(f"  sweep done in {time.time()-t0:.1f}s")
    return acc


# ----------------------------------------------------------------------
# 3. Stream extraction
# ----------------------------------------------------------------------
def extract_streams(dem, acc, fdir, transform,
                     threshold_cells=2000, min_seg_len=3):
    """Threshold on upstream cells (each cell ≈180 m after downsampling,
    so threshold_cells=2000 ≈ 65 km² catchment — sensible cutoff for
    perennial rivers. Lower the threshold to show tributaries).
    """
    log(f"extracting streams (flow-accum >= {threshold_cells} cells)...")
    h, w = dem.shape
    valid = ~np.isnan(dem)
    is_stream = (acc >= threshold_cells) & valid
    p2o = {64: (0, 1), 128: (1, 1), 1: (1, 0), 2: (1, -1),
           4: (0, -1), 8: (-1, -1), 16: (-1, 0), 32: (-1, 1)}

    heads = []
    for y in range(h):
        for x in range(w):
            if not is_stream[y, x]:
                continue
            is_head = True
            for code, (dy, dx) in p2o.items():
                sy, sx = y - dy, x - dx
                if not (0 <= sy < h and 0 <= sx < w):
                    continue
                if is_stream[sy, sx] and fdir[sy, sx] == code:
                    is_head = False
                    break
            if is_head:
                heads.append((y, x))
    log(f"  {len(heads)} channel heads")

    features = []
    seen_mouth = set()
    for hy, hx in heads:
        path = []
        y, x = hy, hx
        while True:
            path.append((y, x))
            if not (0 <= y < h and 0 <= x < w) or not is_stream[y, x]:
                break
            code = fdir[y, x]
            if code == 0:
                break
            dy, dx = p2o.get(int(code), (0, 0))
            ny, nx = y + dy, x + dx
            if not (0 <= ny < h and 0 <= nx < w):
                break
            y, x = ny, nx
            if (y, x) in seen_mouth:
                break
        if len(path) < min_seg_len:
            continue
        coords = []
        for (yy, xx) in path:
            lon, lat = rio_xy(transform, xx, yy)
            coords.append([lon, lat])
        last = path[-1]
        mouth_acc = int(acc[last[0], last[1]])
        cells_to_km2 = (180.0 / 1000) ** 2  # each cell ≈180m → ~0.0324 km²
        catchment_km2 = mouth_acc * cells_to_km2
        if catchment_km2 >= 100:
            cls = "main"           # ≥ 100 km²
        elif catchment_km2 >= 10:
            cls = "tributary"      # 10-100 km²
        else:
            cls = "headwater"      # < 10 km²
        for v in path[1:]:
            seen_mouth.add(v)
        features.append({
            "type": "Feature",
            "properties": {
                "category": "dem_stream",
                "class": cls,
                "accumulation_cells": int(mouth_acc),
                "catchment_km2": round(catchment_km2, 2),
                "vertex_count": len(coords),
                "source": "Copernicus GLO-30 DEM, D8 flow accumulation, 180m grid",
                "generated_utc": datetime.utcnow().isoformat() + "Z",
            },
            "geometry": {"type": "LineString", "coordinates": coords},
        })
    return features


def main():
    log("=" * 60)
    log("Building DEM-derived quebrada streams for full Escobar 20 km box")
    log("=" * 60)
    dem_full, transform = fetch_dem_in_memory()
    log(f"DEM shape: {dem_full.shape}, range {np.nanmin(dem_full):.0f}–{np.nanmax(dem_full):.0f} m")

    # Downsample 6× to 180 m before the expensive flow-accumulation
    SUBSAMPLE = 6
    SUBSAMPLE_SIZE = 180.0  # original cell ≈ 30 m → 180 m
    from rasterio.transform import Affine
    dem_ds = dem_full[::SUBSAMPLE, ::SUBSAMPLE].copy()
    new_transform = transform * Affine.scale(SUBSAMPLE, SUBSAMPLE)
    log(f"downsampled 6× → {dem_ds.shape}  ({dem_ds.size:,} cells)")

    valid_mask = ~np.isnan(dem_ds)
    dem_filled = np.nan_to_num(dem_ds, nan=float(np.nanmedian(dem_ds[valid_mask])))

    log("D8 flow direction...")
    fdir = d8_flow_dir(dem_filled)
    log("flow accumulation...")
    acc = flow_accumulation(dem_filled, fdir)
    log(f"acc: min={int(acc.min())}, max={int(acc.max())}, "
        f"median={int(np.median(acc[valid_mask]))}")

    # Try three thresholds — main rivers first, then add tributaries, then headwaters
    # We emit ONE GeoJSON that has all segments; the viewer classifies them
    all_features = []
    for thr, label in [(2000, "main_rivers"),
                        (500,  "tributaries"),
                        (100,  "headwaters")]:
        feats = extract_streams(
            dem_filled, acc, fdir, new_transform,
            threshold_cells=thr, min_seg_len=3,
        )
        log(f"  {label} (thr≥{thr} cells): {len(feats)} segments")
        all_features.extend(feats)

    fc = {
        "type": "FeatureCollection",
        "name": "dem_streams_10km",
        "metadata": {
            "source": "Copernicus GLO-30 DEM (AWS S3) + D8 flow direction "
                      "+ topographic-sort flow accumulation",
            "bbox": list(BBOX),
            "pixel_resolution_m": int(SUBSAMPLE_SIZE),
            "thresholds_cells_at_180m_grid": {
                "main_rivers":   2000,
                "tributaries":     500,
                "headwaters":      100,
            },
            "feature_count": len(all_features),
            "generated_utc": datetime.utcnow().isoformat() + "Z",
        },
        "features": all_features,
    }
    out_path = OUT / "dem_streams_10km.geojson"
    out_path.write_text(json.dumps(fc, separators=(",", ":")))
    size_mb = out_path.stat().st_size / 1024 / 1024
    log(f"wrote {out_path}  ({size_mb:.2f} MB, {len(all_features)} stream segments)")


if __name__ == "__main__":
    main()
