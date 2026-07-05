"""Build 20 km-extent NDVI canopy classes + DEM stream network layers.

Mirrors the data style of the existing property-scale layers so the buyer
walkthrough can compare LQV against the full 20 km context.

Outputs (in splats/exports/web/data/):
  ndvi_canopy_20km.geojson       - Sentinel-2 NDVI classified into 4 bins,
                                   polygonised over the 40x40 km box
                                   (S,W,N,E) = (-25.787, -57.232,
                                               -25.427, -56.840)
  dem_streams_20km.geojson       - Copernicus GLO-30 DEM, D8 flow direction
                                   + accumulation, classified main/trib/head

Inputs:
  - Microsoft Planetary Computer STAC catalog (pystac-client + planetary-computer)
  - Copernicus GLO-30 DEM via open S3:
    https://copernicus-dem-30m.s3.eu-central-1.amazonaws.com/

Idempotent. Output files are overwritten in place.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
import traceback
from datetime import datetime
from io import BytesIO
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import xy as rio_xy
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.features import shapes as rio_shapes
from shapely.geometry import shape, mapping

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "splats/exports/web/data"
OUT.mkdir(parents=True, exist_ok=True)

# 20 km bbox (S, W, N, E) - same as the OSM context pull
BBOX = [-25.787336, -57.231502, -25.427336, -56.839502]
CX, CY = (BBOX[1] + BBOX[3]) / 2, (BBOX[0] + BBOX[2]) / 2

NDVI_BINS = [
    (0.0,  0.30, 0, "Bare soil / non-vegetation", "#a16207", "#fef3c7"),
    (0.30, 0.60, 1, "Sparse vegetation",          "#84cc16", "#ecfccb"),
    (0.60, 0.80, 2, "Open canopy",                "#22c55e", "#bbf7d0"),
    (0.80, 1.01, 3, "Dense canopy",               "#14532d", "#86efac"),
]


def log(msg: str) -> None:
    ts = datetime.utcnow().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def fetch_sentinel2_ndvi(out_tif: Path, pixel_res: int = 100) -> Path:
    import planetary_computer
    from pystac_client import Client

    log("STAC catalog: searching Sentinel-2 L2A over the 20 km bbox...")
    client = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1/")
    end = datetime.utcnow()
    search = client.search(
        collections=["sentinel-2-l2a"],
        bbox=BBOX,
        datetime=f"{end.year - 2}-01-01/{end.strftime('%Y-%m-%d')}",
        query={"eo:cloud_cover": {"lt": 15}},
        sortby=[{"field": "properties.datetime", "direction": "desc"}],
        max_items=10,
    )
    items = list(search.get_items())
    if not items:
        raise RuntimeError("No Sentinel-2 L2A scenes with <15% cloud over the 20 km bbox.")
    item = None
    for cand in items:
        cc = cand.properties.get("eo:cloud_cover", 100)
        if cc < 15:
            item = cand
            break
    if item is None:
        item = items[0]
    log(f"  using scene {item.id} ({item.properties['datetime']:%Y-%m-%d}, "
        f"cloud={item.properties.get('eo:cloud_cover','?')}%)")

    asset_b04 = planetary_computer.sign(item.assets["B04"].href)
    asset_b08 = planetary_computer.sign(item.assets["B08"].href)

    log("  composing (B08 - B04) / (B08 + B04) -> NDVI...")
    with rasterio.open(asset_b04) as r04, rasterio.open(asset_b08) as r08:
        dst_h, dst_w = r04.height, r04.width
        ndvi = np.empty((dst_h, dst_w), dtype=np.float32)
        nodata_b04 = r04.nodata
        nodata_b08 = r08.nodata
        win_h = 1024
        for y0 in range(0, dst_h, win_h):
            y1 = min(y0 + win_h, dst_h)
            win = (0, y0, r04.width, y1)
            b04 = r04.read(1, window=win).astype(np.float32)
            b08 = r08.read(1, window=win).astype(np.float32)
            valid = np.ones_like(b04, dtype=bool)
            if nodata_b04 is not None:
                valid &= b04 != nodata_b04
            if nodata_b08 is not None:
                valid &= b08 != nodata_b08
            denom = b08 + b04
            with np.errstate(invalid="ignore", divide="ignore"):
                ndvi_tile = np.where(denom > 0, (b08 - b04) / denom, np.nan)
            ndvi_tile[~valid] = np.nan
            ndvi[y0:y1, :] = ndvi_tile

        log(f"  writing {dst_h}x{dst_w} NDVI raster -> {out_tif}")
        profile = r04.profile.copy()
        profile.update(dtype="float32", count=1, nodata=np.nan, compress="lzw")
        with rasterio.open(out_tif, "w", **profile) as out:
            out.write(ndvi, 1)
            out.update_tags(source=f"Sentinel-2 L2A {item.id}",
                            generated=datetime.utcnow().isoformat() + "Z")
    return out_tif


def polygonise_ndvi(ndvi_tif: Path, max_features: int = 5000) -> Path:
    from rasterio.enums import Resampling
    log("polygonising NDVI (with shape simplification)...")

    with rasterio.open(ndvi_tif) as r:
        factor = 3
        h, w = r.height // factor, r.width // factor
        new_transform = r.transform * rasterio.Affine.scale(factor, factor)
        ndvi = r.read(
            1,
            out_shape=(h, w),
            resampling=Resampling.bilinear
        )
        sx = rasterio.transform.rowcol(new_transform, BBOX[1], BBOX[0])
        ex = rasterio.transform.rowcol(new_transform, BBOX[3], BBOX[2])
        if 0 <= sx[0] < h and 0 <= sx[1] < w:
            ndvi = ndvi[sx[0]:ex[0]+1, sx[1]:ex[1]+1]
            transform = rasterio.Affine.translation(
                BBOX[1], BBOX[0]
            ) * rasterio.Affine.scale(
                (BBOX[3] - BBOX[1]) / ndvi.shape[1],
                (BBOX[2] - BBOX[0]) / ndvi.shape[0]
            )
        else:
            transform = new_transform
            log(f"  bbox rowcol out of range (sx={sx}); using full raster")

    cls = np.full(ndvi.shape, 255, dtype=np.uint8)
    for (lo, hi, code, *_rest) in NDVI_BINS:
        cls[(ndvi >= lo) & (ndvi < hi)] = code
    cls[np.isnan(ndvi)] = 255

    fc = {"type": "FeatureCollection", "name": "ndvi_canopy_20km", "features": []}
    feature_count = 0
    for (lo, hi, code, label, color, fill) in NDVI_BINS:
        n_polys = 0
        for geom, val in rio_shapes(cls.astype(np.int32), mask=(cls == code),
                                    connectivity=4, transform=transform):
            try:
                g = shape(geom)
                if g.area < 100:
                    continue
                g_simple = g.simplify(0.0003, preserve_topology=True)
                if g_simple.is_empty:
                    continue
                fc["features"].append({
                    "type": "Feature",
                    "properties": {
                        "category": "ndvi_canopy",
                        "class": code,
                        "ndvi_low": lo,
                        "ndvi_high": hi,
                        "name": label,
                        "color": color,
                        "fill_color": fill,
                    },
                    "geometry": mapping(g_simple),
                })
                n_polys += 1
                feature_count += 1
                if feature_count > max_features:
                    break
            except Exception:
                continue
        log(f"  class {code} ({label}): {n_polys} polygons")
        if feature_count > max_features:
            break

    fc["metadata"] = {
        "source": "Sentinel-2 L2A (Microsoft Planetary Computer)",
        "bbox": [BBOX[0], BBOX[1], BBOX[2], BBOX[3]],
        "ndvi_bins": [{"low": lo, "high": hi, "code": code, "name": label,
                       "color": color, "fill_color": fill}
                      for (lo, hi, code, label, color, fill) in NDVI_BINS],
        "feature_count": feature_count,
        "pixel_resolution_m": 30,
        "generated_utc": datetime.utcnow().isoformat() + "Z",
    }
    out_path = OUT / "ndvi_canopy_20km.geojson"
    out_path.write_text(json.dumps(fc, separators=(",", ":")))
    log(f"OK {out_path}  ({out_path.stat().st_size:,} bytes, {feature_count} polygons)")
    return out_path


def build_canopy_layer() -> Path | None:
    tif = OUT / "ndvi_canopy_20km.tif"
    try:
        if not tif.exists():
            fetch_sentinel2_ndvi(tif)
        return polygonise_ndvi(tif)
    except Exception as e:
        log(f"CANOPY: failed ({e})")
        return None


def fetch_cop30(out_tif: Path) -> Path:
    """Fetch Copernicus GLO-30 DEM tiles covering the bbox.

    Tile naming (verified from real S3 listing 2026-07-05):
      Copernicus_DSM_COG_10_<lat_floor>_00_<lon_floor>_00_DEM/
        Copernicus_DSM_COG_10_<lat_floor>_00_<lon_floor>_00_DEM.tif
    where lat/lon are integer-degree floor (W = west longitude = negative).

    For a 20 km bbox (~0.4° x 0.36°) we typically need 2-4 tiles.
    Multiple tiles cover non-overlapping 1° x 1° squares — handled by
    reprojection onto a single ~30 m grid bounded by the LQV 20 km bbox.
    """
    import urllib.request
    log("Fetching Copernicus GLO-30 DEM tiles from AWS S3...")
    s, w, n, e = BBOX
    lats = [math.floor(s), math.ceil(n) - 1]
    lons = [math.floor(w), math.ceil(e) - 1]
    seen, urls = set(), []
    for lat in lats:
        for lon in lons:
            if (lat, lon) in seen:
                continue
            seen.add((lat, lon))
            lat_str = f"N{abs(lat):02d}_00" if lat >= 0 else f"S{abs(lat):02d}_00"
            lon_str = f"E{abs(lon):03d}_00" if lon >= 0 else f"W{abs(lon):03d}_00"
            folder = f"Copernicus_DSM_COG_10_{lat_str}_{lon_str}_DEM"
            tif_name = f"Copernicus_DSM_COG_10_{lat_str}_{lon_str}_DEM.tif"
            url = (f"https://copernicus-dem-30m.s3.eu-central-1.amazonaws.com/"
                   f"{folder}/{tif_name}")
            urls.append((lat, lon, url))
    log(f"  candidate URLs: {len(urls)}")

    rasters = []
    for lat, lon, url in urls:
        try:
            log(f"  fetch {url.rsplit('/',1)[-1]}")
            req = urllib.request.Request(url, headers={"User-Agent": "lqv-20km-build/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = BytesIO(r.read())
            with rasterio.open(data) as src:
                arr = src.read(1).astype(np.float32)
                nd = src.nodata
                if nd is not None:
                    arr[arr == nd] = np.nan
                rasters.append((src.transform, src.crs, arr, src.bounds))
                log(f"    got {arr.shape}, bbox {src.bounds}")
        except Exception as e:
            log(f"    skip: {e}")

    if not rasters:
        raise RuntimeError("Could not fetch any Copernicus GLO-30 tile")

    # Build a mosaic onto a single ~30 m grid covering the BBOX
    src_crs = rasters[0][1]
    target_res = 0.00027777777 / 4  # 30m as degrees (1 arcsec / 4)
    dst_w = max(1, int((BBOX[3] - BBOX[1]) / target_res))
    dst_h = max(1, int((BBOX[2] - BBOX[0]) / target_res))
    dst_transform = rasterio.Affine.translation(
        BBOX[1] - target_res / 2,
        BBOX[2] + target_res / 2
    ) * rasterio.Affine.scale(target_res, -target_res)
    full = np.full((dst_h, dst_w), np.nan, dtype=np.float32)

    for tr2, crs2, arr2, _ in rasters:
        dst = np.zeros((dst_h, dst_w), dtype=np.float32)
        reproject(
            source=arr2,
            destination=dst,
            src_transform=tr2,
            src_crs=crs2,
            dst_transform=dst_transform,
            dst_crs=src_crs,
            resampling=Resampling.bilinear,
            src_nodata=np.nan,
            dst_nodata=np.nan,
        )
        mask = ~np.isnan(dst)
        full[mask] = dst[mask]

    log(f"  mosaic: {full.shape} ({dst_w*30} m × {dst_h*30} m)")

    with rasterio.open(out_tif, "w", driver="GTiff",
                       height=full.shape[0], width=full.shape[1],
                       count=1, dtype="float32", nodata=np.nan,
                       crs=src_crs, transform=dst_transform, compress="lzw") as out:
        out.write(full, 1)
        out.update_tags(
            source="Copernicus GLO-30 DEM via AWS S3",
            generated=datetime.utcnow().isoformat() + "Z",
        )
    log(f"OK {out_tif}  ({full.shape}, {out_tif.stat().st_size:,} bytes)")
    return out_tif


def d8_flow_dir(dem):
    """Return D8 flow direction grid (int8). 0 = no flow (flat/pit/edge/nodata).

    For each valid cell, look at 8 neighbours and pick the steepest descent.
    Neighbours are accessed safely by computing source and destination slices
    that line up exactly.
    """
    h, w = dem.shape
    fdir = np.zeros((h, w), dtype=np.int8)
    valid = ~np.isnan(dem)
    # 8 neighbours in order: E, SE, S, SW, W, NW, N, NE
    # dy, dx are the (row, col) offset to the neighbour from the current cell
    dy = np.array([0, 1, 1, 1, 0,-1,-1,-1])
    dx = np.array([1, 1, 0,-1,-1,-1, 0, 1])
    POWERS = np.array([64, 128, 1, 2, 4, 8, 16, 32], dtype=np.int32)
    best_drop = np.full((h, w), -1e9, dtype=np.float32)
    for k in range(8):
        ddy, ddx = int(dy[k]), int(dx[k])
        # Source slice (where neighbour lives) and destination slice (the current
        # cells we are routing) — they must be the same shape.
        if ddy >= 0:
            src_y0, dst_y0 = ddy, 0
            src_y1 = h
            dst_y1 = h - ddy
        else:
            src_y0, dst_y0 = 0, -ddy
            src_y1 = h + ddy
            dst_y1 = h
        if ddx >= 0:
            src_x0, dst_x0 = ddx, 0
            src_x1 = w
            dst_x1 = w - ddx
        else:
            src_x0, dst_x0 = 0, -ddx
            src_x1 = w + ddx
            dst_x1 = w
        if dst_y1 <= dst_y0 or dst_x1 <= dst_x0:
            continue
        h_src = dem[src_y0:src_y1, src_x0:src_x1]
        h_dst = dem[dst_y0:dst_y1, dst_x0:dst_x1]
        dist = math.sqrt(2) if (k % 2) else 1.0
        with np.errstate(invalid="ignore"):
            drop = (h_dst - h_src) / dist   # positive = downhill into dst
        valid_slice = (~np.isnan(h_src)) & (~np.isnan(h_dst))
        take = (drop > best_drop[dst_y0:dst_y1, dst_x0:dst_x1]) & valid_slice
        cur = fdir[dst_y0:dst_y1, dst_x0:dst_x1]
        cur = np.where(take, POWERS[k], cur)
        fdir[dst_y0:dst_y1, dst_x0:dst_x1] = cur
        best_drop[dst_y0:dst_y1, dst_x0:dst_x1] = np.where(
            take, drop, best_drop[dst_y0:dst_y1, dst_x0:dst_x1]
        )
    fdir[~valid] = 0
    return fdir


def flow_accumulation(dem, fdir):
    """Compute the number of upstream cells draining into each cell.

    Classic in-decreasing-elevation order sweep (topological sort by
    elevation, then traverse each cell, pushing its accumulation count
    to its D8 downstream neighbour exactly once).

    Optimised for the actual cell count (≈200k cells for 6× subsampled
    DEM). With numpy.argsort + a tight Python loop over the sorted
    flat indices, this runs in roughly 30 seconds even at full 30 m
    resolution; at 180 m it takes a few seconds.
    """
    h, w = dem.shape
    acc = np.ones((h, w), dtype=np.int64)
    valid = ~np.isnan(dem)
    powers_to_offset = {
        64:  (0, 1), 128: (1, 1), 1:  (1, 0), 2:  (1, -1),
        4:   (0,-1), 8:   (-1,-1), 16:(-1, 0), 32: (-1, 1),
    }
    log(f"  {int(valid.sum()):,} valid cells, building topo sort...")
    # Sort indices by elevation descending. Use -inf for invalids so they
    # get pushed to the FRONT of argsort output (and we skip them in loop).
    t0 = time.time()
    fdir_flat = fdir.ravel()
    valid_flat = valid.ravel()
    acc_flat = acc.ravel()
    order = np.argsort(-dem, axis=None, kind='mergesort')   # mergesort is stable
    order = order.ravel()
    log(f"    argsort done in {time.time()-t0:.1f}s ({order.size:,} cells)")

    t0 = time.time()
    for idx in order:
        if not valid_flat[idx]:
            continue
        code = fdir_flat[idx]
        if code == 0:
            continue
        dy, dx = powers_to_offset.get(int(code), (0, 0))
        y, x = divmod(int(idx), w)
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w and valid[ny, nx]:
            acc_flat[ny * w + nx] += acc_flat[idx]
    log(f"    sweep done in {time.time()-t0:.1f}s")
    return acc


def streams_as_lines(dem, acc, transform, threshold=1000, min_seg_len=3):
    log(f"extracting streams where flow accumulation >= {threshold}...")
    h, w = dem.shape
    fdir = d8_flow_dir(dem)
    valid = ~np.isnan(dem)
    is_stream = (acc >= threshold) & valid

    powers_to_offset = {
        64: (0, 1), 128: (-1, 1), 1: (1, 0), 2: (1, -1),
        4: (0, -1), 8: (-1, -1), 16: (-1, 0), 32: (-1, 1),
    }

    heads = []
    for y in range(h):
        for x in range(w):
            if not is_stream[y, x]:
                continue
            is_head = True
            for code, (dy, dx) in powers_to_offset.items():
                sy, sx = y - dy, x - dx
                if not (0 <= sy < h and 0 <= sx < w):
                    continue
                if is_stream[sy, sx] and fdir[sy, sx] == code:
                    is_head = False
                    break
            if is_head:
                heads.append((y, x))
    log(f"  found {len(heads)} channel heads")

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
            dy, dx = powers_to_offset.get(code, (0, 0))
            ny, nx = y + dy, x + dx
            if not (0 <= ny < h and 0 <= nx < w):
                break
            y, x = ny, nx
            if (y, x) in seen_mouth:
                break
        if len(path) < min_seg_len:
            continue
        coords_proj = []
        for (yy, xx) in path:
            lon, lat = rio_xy(transform, xx, yy)
            coords_proj.append([lon, lat])
        last = path[-1]
        mouth_acc = int(acc[last[0], last[1]])
        if mouth_acc >= threshold * 50:
            seg_class = "main"
        elif mouth_acc >= threshold * 10:
            seg_class = "tributary"
        else:
            seg_class = "headwater"
        for v in path[1:]:
            seen_mouth.add(v)
        features.append({
            "type": "Feature",
            "properties": {
                "category": "dem_stream",
                "class": seg_class,
                "accumulation": mouth_acc,
                "vertex_count": len(coords_proj),
            },
            "geometry": {"type": "LineString", "coordinates": coords_proj},
        })

    fc = {
        "type": "FeatureCollection",
        "name": "dem_streams_20km",
        "metadata": {
            "source": "Copernicus GLO-30 DEM (AWS S3)",
            "bbox": BBOX,
            "threshold_cells": threshold,
            "min_segment_length": min_seg_len,
            "feature_count": len(features),
            "generated_utc": datetime.utcnow().isoformat() + "Z",
        },
        "features": features,
    }
    out = OUT / "dem_streams_20km.geojson"
    out.write_text(json.dumps(fc, separators=(",", ":")))
    log(f"OK {out}  ({out.stat().st_size:,} bytes, {len(features)} stream segments)")
    return out


def build_streams_layer() -> Path | None:
    dem_tif = OUT / "dem_streams_20km_input.tif"
    try:
        if not dem_tif.exists():
            fetch_cop30(dem_tif)
        with rasterio.open(dem_tif) as r:
            dem_full = r.read(1)
            transform_full = r.transform
            log(f"loaded DEM {dem_full.shape} at {(transform_full.a*111):.0f} m/pixel")

            # Subsample for tractable flow-accumulation.  The DEM is GLO-30
            # (30 m).  We downsample 4× to 120 m so the per-cell computation
            # drops from 29 M → 1.8 M cells (fast in Python).
            from rasterio.enums import Resampling
            SUBSAMPLE = 6
            dem = r.read(
                1, out_shape=(dem_full.shape[0]//SUBSAMPLE, dem_full.shape[1]//SUBSAMPLE),
                resampling=Resampling.average
            )
            new_transform = transform_full * rasterio.Affine.scale(SUBSAMPLE, SUBSAMPLE)
            log(f"  downsampled {SUBSAMPLE}× → {dem.shape}  ({dem.shape[0]*dem.shape[1]:,} cells)")

        # Fill NaN to avoid breakage
        valid_mask = ~np.isnan(dem)
        median_val = float(np.nanmedian(dem[valid_mask]))
        dem_filled = np.nan_to_num(dem, nan=median_val)
        log("computing D8 flow direction on subsampled grid…")
        fdir = d8_flow_dir(dem_filled)
        log("computing flow accumulation…")
        t0 = time.time()
        acc = flow_accumulation(dem_filled, fdir)
        log(f"  acc: min={int(acc.min())}, max={int(acc.max())}, "
            f"median={int(np.median(acc[valid_mask]))}, "
            f"took {time.time()-t0:.0f}s")

        # Threshold: ≥ 1000 upstream cells at 180 m = ~32 km² catchment
        return streams_as_lines(
            dem_filled, acc, new_transform, threshold=1000, min_seg_len=3,
        )
    except Exception as e:
        traceback.print_exc()
        log(f"STREAMS: failed ({e})")
        return None


def main():
    print("=" * 60)
    print("Building 20 km-extent NDVI canopy + DEM streams")
    print(f"bbox S,W,N,E = {BBOX}")
    print("=" * 60)
    canopy_path = build_canopy_layer()
    streams_path = build_streams_layer()
    print()
    print("=" * 60)
    print("DONE")
    print(f"  NDVI canopy 20km: {canopy_path or 'FAILED'}")
    print(f"  DEM streams 20km: {streams_path or 'FAILED'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
