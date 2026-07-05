"""Build full 20 km NDVI canopy + DEM streams for the LQV context map.

Streamed end-to-end (no 122 MB DEM intermediate on disk — Cloudflare
Pages has a 25 MB file-size cap). Emits two small GeoJSONs:
  splats/exports/web/data/dem_streams_20km.geojson
  splats/exports/web/data/ndvi_canopy_20km.geojson

Run order:
  1. Sentinel-2 L2A fetch via Planetary Computer → NDVI raster in memory
  2. Polygonise to 4-class canopy polygons in memory → write GeoJSON
  3. Copernicus GLO-30 fetch → D8 flow direction → accumulation →
     stream LineStrings (typed main / tributary / headwater)
  4. Optional: marching-squares contours at 20 m for terrain visualisation

Both datasets cover the full 40×40 km LQV 20 km context box.
"""
from __future__ import annotations

import io
import json
import math
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import xy as rio_xy
from rasterio.warp import reproject, Resampling
from rasterio.features import shapes as rio_shapes
from shapely.geometry import shape, mapping

ROOT = Path("/root/la-quebrada-viva")
OUT = ROOT / "splats/exports/web/data"
OUT.mkdir(parents=True, exist_ok=True)

BBOX = (-25.787336, -57.231502, -25.427336, -56.839502)  # S, W, N, E
# STAC expects [W, S, E, N] (min_lon, min_lat, max_lon, max_lat)
STAC_BBOX = (BBOX[1], BBOX[0], BBOX[3], BBOX[2])

NDVI_BINS = [
    (0.0, 0.25, 0, "Bare / grassland",   "#a16207", "Bare soil, dry grass or row crops — no woody vegetation."),
    (0.25, 0.45, 1, "Sparse woody",      "#84cc16", "Scattered trees, woodland edges, agroforestry — visible canopy not closed."),
    (0.45, 0.60, 2, "Open forest",        "#22c55e", "Open canopy forest such as the LQV parcel — partial cover."),
    (0.60, 1.01, 3, "Dense forest",      "#14532d", "Tightly closed canopy (e.g. riparian gallery forests along streams)."),
]
CLASS_INFO = {
    0: "Distinct man-made and very-sparse landscape. Look for roads, fields, exposed rock.",
    1: "Inhabited countryside with trees scattered around fields and roads.",
    2: "Forest that is open (you can see ground between tree crowns) — typical Atlantic Forest highland in Paraguay.",
    3: "Tightly closed canopy — gallery forest along quebradas, deep ravines.",
}


def log(msg):
    print(f"[{datetime.utcnow().strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


# ================================================================
# Sentinel-2 NDVI → 4-class polygons (full 20 km box)
# ================================================================
def fetch_sentinel2_ndvi_memory() -> tuple | None:
    """Fetch + mosaic clear Sentinel-2 L2A tiles over the bbox, compute NDVI.
    Returns (ndvi_2d, transform, crs) in UTM CRS of the first tile,
    not WGS84. The caller reprojects to WGS84.

    The LQV 20 km box straddles 2 tiles: T21JWM (NW) and T21JVM (SE).
    """
    try:
        import planetary_computer
        from pystac_client import Client
    except ImportError:
        log("  ⚠ planetary-computer / pystac-client not installed")
        return None
    log("STAC search: most recent clear Sentinel-2 L2A scenes over the bbox...")
    try:
        client = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1/")
    except Exception as e:
        log(f"  ⚠ STAC open failed: {e}")
        return None
    end = datetime.utcnow()
    start = f"{end.year - 1}-01-01"
    endstr = end.strftime('%Y-%m-%d')
    log(f"  STAC range: {start}/{endstr}, bbox={list(STAC_BBOX)}, "
        f"cloud_lt=20, max=20")
    try:
        search = client.search(
            collections=["sentinel-2-l2a"],
            bbox=list(STAC_BBOX),
            datetime=f"{start}/{endstr}",
            query={"eo:cloud_cover": {"lt": 20}},
            sortby=[{"field": "properties.datetime", "direction": "desc"}],
            max_items=20,
        )
        items = list(search.items())
    except Exception as e:
        log(f"  ⚠ STAC search failed: {e}")
        return None
    if not items:
        log("  ⚠ no Sentinel-2 L2A scenes found")
        return None
    log(f"  STAC returned {len(items)} items; first 5 IDs:")
    for it in items[:5]:
        log(f"    {it.id}")
    # Keep only items whose MGRS tile is T21J* (UTM 21J = Paraguay).
    items_t21j = [it for it in items if "_T21J" in it.id]
    log(f"  filtered to {len(items_t21j)} T21J scenes")
    items = items_t21j
    if not items:
        log("  ⚠ no T21J scenes found")
        return None
    # Pick ONE day where both MGRS tiles (JWM + JVM) have data so we can
    # mosaic seamlessly. Group by date, sorted desc, then find first day
    # where both keys are present.
    by_date = {}
    for it in items:
        d = it.properties["datetime"][:10]
        mg = it.id.split("_")[4]    # T21JWM / T21JVM / ...
        by_date.setdefault(d, {})[mg] = it
    chosen = None
    for d in sorted(by_date.keys(), reverse=True):
        mg_items = by_date[d]
        jwm = mg_items.get("T21JWM")
        jvm = mg_items.get("T21JVM")
        if jwm and jvm:
            chosen = (d, jwm, jvm)
            log(f"  picked date {d} with both T21JWM + T21JVM")
            break
    if chosen is None:
        # Fallback: just use the single most recent cloud-clearest tile
        chosen = ("unknown", items[0], None)
        log("  ⚠ no date with both tiles — using single newest tile")
    log(f"  using date {chosen[0]} (T21JWM) "
        f"+ T21JVM={'yes' if chosen[2] else 'no'}")

    items_to_use = [chosen[1]] + ([chosen[2]] if chosen[2] else [])
    item = chosen[1]   # primary tileset

    def calc_ndvi_for(item):
        """Read B04+B08 in 1024-row tiles, compute NDVI, return (ndvi, t, c)."""
        log(f"  composing NDVI for {item.id} (cloud={item.properties.get('eo:cloud_cover','?')}%)...")
        a04 = planetary_computer.sign(item.assets["B04"].href)
        a08 = planetary_computer.sign(item.assets["B08"].href)
        with rasterio.open(a04) as r04, rasterio.open(a08) as r08:
            dst_h, dst_w = r04.height, r04.width
            ndvi = np.empty((dst_h, dst_w), dtype=np.float32)
            from rasterio.windows import Window
            win_h = 1024
            for y0 in range(0, dst_h, win_h):
                y1 = min(y0 + win_h, dst_h)
                w04 = Window(col_off=0, row_off=y0, width=r04.width, height=y1 - y0)
                w08 = Window(col_off=0, row_off=y0, width=r08.width, height=y1 - y0)
                b04 = r04.read(1, window=w04).astype(np.float32)
                b08 = r08.read(1, window=w08).astype(np.float32)
                valid = (b04 > 0) & (b08 > 0)
                denom = (b08 + b04)
                with np.errstate(invalid="ignore", divide="ignore"):
                    ndvi_tile = np.where(valid & (denom > 0),
                                         (b08 - b04) / denom, np.nan)
                ndvi[y0:y1, :] = ndvi_tile
            return ndvi, r04.transform, r04.crs

    try:
        ndvi1, transform1, crs1 = calc_ndvi_for(items_to_use[0])
    except Exception as e:
        log(f"  ⚠ NDVI compute (tile 1) failed: {e}")
        return None
    if len(items_to_use) > 1:
        try:
            ndvi2, transform2, crs2 = calc_ndvi_for(items_to_use[1])
            # Mosaic: reproject ndvi2 onto the same grid as ndvi1
            mosaic = np.full_like(ndvi1, np.nan)
            reproject(source=ndvi2, destination=mosaic,
                      src_transform=transform2, src_crs=crs2,
                      dst_transform=transform1, dst_crs=crs1,
                      resampling=Resampling.average,
                      src_nodata=np.nan, dst_nodata=np.nan)
            full_ndvi = np.where(np.isnan(mosaic), ndvi1, mosaic)
            log(f"  mosaic {len(items_to_use)} tiles: {full_ndvi.shape}")
        except Exception as e:
            log(f"  ⚠ tile 2 mosaic failed: {e} — using tile 1 only")
            full_ndvi = ndvi1
    else:
        full_ndvi = ndvi1
    return full_ndvi, transform1, crs1


def polygonise_ndvi(ndvi: np.ndarray, transform, crs) -> int:
    """Classify NDVI array into 4 bins, polygonise, write GeoJSON.
    Returns polygon count written.
    """
    log("polygonising NDVI (4 classes, ≤5000 polygons)...")
    log(f"  CRS: {crs}, transform: {transform}")

    # Reproject from the SRC's CRS (often UTM) to WGS84 (EPSG:4326) at 100 m
    # pixel resolution so the polygons are ship-ready and small enough to
    # deploy fast.
    DST_CRS = "EPSG:4326"
    DST_RES_DEG = 0.0009   # ≈100 m at the equator (≈90 m in Paraguay)
    dst_w = max(1, int((BBOX[3] - BBOX[1]) / DST_RES_DEG) + 4)
    dst_h = max(1, int((BBOX[2] - BBOX[0]) / DST_RES_DEG) + 4)
    # Centre the destination on the 20 km bbox
    dst_transform = rasterio.Affine.translation(
        BBOX[1] - DST_RES_DEG / 2,
        BBOX[2] + DST_RES_DEG / 2
    ) * rasterio.Affine.scale(DST_RES_DEG, -DST_RES_DEG)
    ndvi_wgs = np.full((dst_h, dst_w), np.nan, dtype=np.float32)
    reproject(
        source=ndvi, destination=ndvi_wgs,
        src_transform=transform, src_crs=crs,
        dst_transform=dst_transform, dst_crs=DST_CRS,
        resampling=Resampling.average,
        src_nodata=None, dst_nodata=np.nan,
    )
    ndvi_sub = ndvi_wgs
    new_transform = dst_transform
    log(f"  WGS84 NDVI grid: {ndvi_wgs.shape}, range "
        f"{np.nanmin(ndvi_wgs):.3f}–{np.nanmax(ndvi_wgs):.3f}")

    # Clip to a tiny margin inside the bbox so polygonise ignores neighbours
    cls = np.full(ndvi_sub.shape, 255, dtype=np.uint8)
    for (lo, hi, code, *_rest) in NDVI_BINS:
        cls[(ndvi_sub >= lo) & (ndvi_sub < hi)] = code
    cls[np.isnan(ndvi_sub)] = 255
    log(f"  class counts: {np.array(np.unique(cls, return_counts=True)).T[:6]}")

    # Clip class raster to bbox in pixel coords using the bbox SW + NE
    # corners. Note: top row of the transform is the northern edge
    # (smallest lat). rowcol returns (row, col).
    from rasterio.transform import rowcol
    bbox_tf_top = BBOX[2]   # northernmost lat
    bbox_tf_bot = BBOX[0]   # southernmost
    bbox_tf_lft = BBOX[1]
    bbox_tf_rgt = BBOX[3]
    r_top_left,   c_top_left   = rowcol(new_transform, bbox_tf_lft, bbox_tf_top)
    r_bot_right,  c_bot_right  = rowcol(new_transform, bbox_tf_rgt, bbox_tf_bot)
    r0 = min(r_top_left, r_bot_right)
    r1 = max(r_top_left, r_bot_right)
    c0 = min(c_top_left, c_bot_right)
    c1 = max(c_top_left, c_bot_right)
    r0 = max(0, r0); r1 = min(cls.shape[0], r1 + 1)
    c0 = max(0, c0); c1 = min(cls.shape[1], c1 + 1)
    log(f"  bbox crop: rows {r0}-{r1}, cols {c0}-{c1}, total {r1-r0}×{c1-c0}")
    if r1 <= r0 or c1 <= c0:
        raise SystemExit("bbox crop is empty")
    cls_crop = cls[r0:r1, c0:c1]
    tf_crop = new_transform * rasterio.Affine.translation(c0, r0)

    features = []
    for (lo, hi, code, label, color, desc) in NDVI_BINS:
        n = 0
        for geom, val in rio_shapes(cls_crop.astype(np.int32),
                                    mask=(cls_crop == code),
                                    connectivity=4,
                                    transform=tf_crop):
            try:
                g = shape(geom)
                if g.area < 1e-9:        # < ~100 m²
                    continue
                g_simple = g.simplify(0.0002, preserve_topology=True)
                if g_simple.is_empty:
                    continue
                features.append({
                    "type": "Feature",
                    "properties": {
                        "category": "ndvi_canopy",
                        "class": code,
                        "ndvi_low": lo,
                        "ndvi_high": hi,
                        "name": label,
                        "color": color,
                        "fill_color": color,
                        "description": desc,
                        "source": "Sentinel-2 L2A NDVI 4-class polygonised",
                    },
                    "geometry": mapping(g_simple),
                })
                n += 1
                if len(features) >= 4500:
                    break
            except Exception:
                continue
        log(f"  class {code} ({label}): {n} polygons")
        if len(features) >= 4500:
            log("  hit cap; stopping")
            break

    fc = {
        "type": "FeatureCollection",
        "name": "ndvi_canopy_20km",
        "metadata": {
            "source": "Sentinel-2 L2A NDVI, polygonised at 30 m (3× downsampled)",
            "bbox": list(BBOX),
            "classes": [
                {"low": lo, "high": hi, "code": code,
                 "name": label, "color": color, "description": desc}
                for (lo, hi, code, label, color, desc) in NDVI_BINS
            ],
            "feature_count": len(features),
            "generated_utc": datetime.utcnow().isoformat() + "Z",
        },
        "features": features,
    }
    out_path = OUT / "ndvi_canopy_20km.geojson"
    out_path.write_text(json.dumps(fc, separators=(",", ":")))
    sz = out_path.stat().st_size
    log(f"wrote {out_path}  ({sz/1024:.0f} KB, {len(features)} polygons)")
    return len(features)


# ================================================================
# Copernicus GLO-30 → D8 → flow accumulation → streams
# ================================================================
def fetch_dem_in_memory() -> tuple[np.ndarray, rasterio.Affine]:
    log("Fetching Copernicus GLO-30 (2 tiles, in-memory)...")
    s, w, n, e = BBOX
    lats = [math.floor(s), math.ceil(n) - 1]
    lons = [math.floor(w), math.ceil(e) - 1]
    urls = []
    seen = set()
    for lat in lats:
        for lon in lons:
            if (lat, lon) in seen: continue
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
            log(f"  fetch {url.rsplit('/',1)[-1]}")
            req = urllib.request.Request(url, headers={"User-Agent": "lqv-20km/1.0"})
            with urllib.request.urlopen(req, timeout=90) as r:
                data = io.BytesIO(r.read())
            with rasterio.open(data) as src:
                arr = src.read(1).astype(np.float32)
                nd = src.nodata
                if nd is not None:
                    arr[arr == nd] = np.nan
                rasters.append((src.transform, src.crs, arr))
                log(f"    OK {arr.shape}")
        except Exception as e:
            log(f"    skip: {e}")

    if not rasters:
        raise SystemExit("Could not fetch any Copernicus GLO-30 tile")

    target_res_deg = 0.00009259259  # ≈30 m
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
    log(f"  mosaic: {full.shape}, range "
        f"{np.nanmin(full):.0f}–{np.nanmax(full):.0f} m")
    return full, dst_transform


def d8_flow_dir(dem: np.ndarray) -> np.ndarray:
    h, w = dem.shape
    fdir = np.zeros((h, w), dtype=np.int8)
    valid = ~np.isnan(dem)
    dy = np.array([0, 1, 1, 1, 0, -1, -1, -1])
    dx = np.array([1, 1, 0, -1, -1, -1, 0, 1])
    POWERS = np.array([64, 128, 1, 2, 4, 8, 16, 32], dtype=np.int32)
    best = np.full((h, w), -1e9, dtype=np.float32)
    for k in range(8):
        ddy, ddx = int(dy[k]), int(dx[k])
        if ddy >= 0:
            sy0, dy0 = ddy, 0; sy1, dy1 = h, h - ddy
        else:
            sy0, dy0 = 0, -ddy; sy1, dy1 = h + ddy, h
        if ddx >= 0:
            sx0, dx0 = ddx, 0; sx1, dx1 = w, w - ddx
        else:
            sx0, dx0 = 0, -ddx; sx1, dx1 = w + ddx, w
        if dy1 <= dy0 or dx1 <= dx0:
            continue
        h_src = dem[sy0:sy1, sx0:sx1]
        h_dst = dem[dy0:dy1, dx0:dx1]
        dist = math.sqrt(2) if (k % 2) else 1.0
        with np.errstate(invalid="ignore"):
            drop = (h_dst - h_src) / dist
        valid_slice = (~np.isnan(h_src)) & (~np.isnan(h_dst))
        take = (drop > best[dy0:dy1, dx0:dx1]) & valid_slice
        cur = fdir[dy0:dy1, dx0:dx1]
        cur = np.where(take, POWERS[k], cur)
        fdir[dy0:dy1, dx0:dx1] = cur
        best[dy0:dy1, dx0:dx1] = np.where(take, drop,
                                            best[dy0:dy1, dx0:dx1])
    fdir[~valid] = 0
    return fdir


def flow_accumulation(dem: np.ndarray, fdir: np.ndarray) -> np.ndarray:
    h, w = dem.shape
    acc = np.ones((h, w), dtype=np.int64)
    valid = ~np.isnan(dem)
    p2o = {64: (0, 1), 128: (1, 1), 1: (1, 0), 2: (1, -1),
           4: (0, -1), 8: (-1, -1), 16: (-1, 0), 32: (-1, 1)}
    fdir_flat = fdir.ravel()
    valid_flat = valid.ravel()
    acc_flat = acc.ravel()
    order = np.argsort(-dem, axis=None, kind='mergesort')
    log(f"  topo sweep over {len(order):,} cells...")
    t0 = time.time()
    for idx in order:
        if not valid_flat[idx]:
            continue
        code = fdir_flat[idx]
        if code == 0: continue
        dy, dx = p2o.get(int(code), (0, 0))
        y, x = divmod(int(idx), w)
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w and valid[ny, nx]:
            acc_flat[ny * w + nx] += acc_flat[idx]
    log(f"  sweep done in {time.time()-t0:.1f}s")
    return acc


def extract_streams(dem, acc, fdir, transform,
                    threshold_cells, min_seg_len=3, label=""):
    h, w = dem.shape
    valid = ~np.isnan(dem)
    is_stream = (acc >= threshold_cells) & valid
    p2o = {64: (0, 1), 128: (1, 1), 1: (1, 0), 2: (1, -1),
           4: (0, -1), 8: (-1, -1), 16: (-1, 0), 32: (-1, 1)}
    # Find channel heads
    is_head = np.zeros((h, w), dtype=bool)
    is_stream_arr = is_stream
    for y in range(h):
        for x in range(w):
            if not is_stream_arr[y, x]:
                continue
            for code, (dy, dx) in p2o.items():
                sy, sx = y - dy, x - dx
                if not (0 <= sy < h and 0 <= sx < w):
                    continue
                if is_stream_arr[sy, sx] and fdir[sy, sx] == code:
                    break
            else:
                is_head[y, x] = True
    head_y, head_x = np.nonzero(is_head)
    log(f"    {label}: {len(head_y)} channel heads")
    # Trace each head down to its mouth, build a path, classify.
    feats = []
    seen_mouth = set()
    cell_km2 = (180.0 / 1000) ** 2   # 180 m cells
    MAX_PATH_LEN = 2000           # safety: at 180 m/cell = 360 km
    n_traced = 0
    for hy, hx in zip(head_y.tolist(), head_x.tolist()):
        path = []
        y, x = hy, hx
        steps = 0
        while steps < MAX_PATH_LEN:
            path.append((y, x))
            if not (0 <= y < h and 0 <= x < w) or not is_stream[y, x]:
                break
            code = fdir[y, x]
            if code == 0: break
            dy, dx = p2o.get(int(code), (0, 0))
            ny, nx = y + dy, x + dx
            if not (0 <= ny < h and 0 <= nx < w):
                break
            y, x = ny, nx
            if (y, x) in seen_mouth:
                break
            steps += 1
        if len(path) < min_seg_len:
            continue
        # Vertex decimation: keep every Nth point (and always the last).
        # At 180 m between cells, every-5th vertex ≈ 900 m spacing which is
        # still smooth at 20 km context but cuts the file size ~5x.
        DECIM = 5
        if len(path) > 20:
            decimated_idx = list(range(0, len(path) - 1, DECIM)) + [len(path) - 1]
            decim_path = [path[i] for i in decimated_idx]
            decim_coords_target = True
        else:
            decim_path = path
            decim_coords_target = False
        # Vectorised coord conversion (single C call vs per-vertex loop):
        path_arr = np.asarray(decim_path, dtype=int)
        cols = path_arr[:, 1].tolist()
        rows = path_arr[:, 0].tolist()
        lons, lats = rio_xy(transform, cols, rows)
        coords = [[lon, lat] for lon, lat in zip(lons, lats)]
        last = path[-1]
        mouth_acc = int(acc[last[0], last[1]])
        cath_km2 = mouth_acc * cell_km2
        # Classification tuned for the LQV 20 km box: even the largest
        # stream catchments in this region sit in the 10-50 km² range,
        # not 100 km². Use ≥ 25 km² as the threshold for "main river".
        if   cath_km2 >= 25:  cls = "main"
        elif cath_km2 >= 5:   cls = "tributary"
        elif cath_km2 >= 1:   cls = "creek"
        else:                 cls = "rill"
        for v in path[1:]:
            seen_mouth.add(v)
        # Drop degenerate LineStrings — those with <2 distinct points
        # (rasterio polygons fed to .shapes can yield MultiLineStrings
        # where one component is a single Point, breaking Leaflet)
        unique_pts = []
        for pt in coords:
            if not unique_pts or pt[0] != unique_pts[-1][0] or pt[1] != unique_pts[-1][1]:
                unique_pts.append(pt)
        if len(unique_pts) < 2:
            continue
        feats.append({
            "type": "Feature",
            "properties": {
                "category": "dem_stream",
                "class": cls,
                "threshold_label": label,
                "catchment_km2": round(cath_km2, 2),
                "accumulation_cells": int(mouth_acc),
                "vertex_count": len(coords),
                "decimated": decim_coords_target,
                "source": "Copernicus GLO-30 DEM at 180 m, D8 flow accumulation",
            },
            "geometry": {"type": "LineString", "coordinates": coords},
        })
        n_traced += 1
    log(f"    {label}: traced {n_traced} → {len(feats)} LineString features")
    return feats


def extract_flow_arrows(streams, transform):
    """Drop a small point feature every ~50 vertices along main_rivers and
    ~80 along tributaries, capped at ~1500 total markers, so the viewer
    can render arrowheads pointing in the direction of flow without
    overloading Leaflet with 30,000 divIcons."""
    feats = []
    for s in streams:
        coords = s["geometry"]["coordinates"]
        cls = s["properties"]["class"]
        if cls == "main":
            step = 50
        elif cls == "tributary":
            step = 80
        else:
            continue  # skip creek and rill
        for i in range(0, len(coords) - 2, step):
            x1, y1 = coords[i]
            x2, y2 = coords[i + 1]
            # Skip degenerate (zero-length) segments
            if abs(x1 - x2) < 1e-9 and abs(y1 - y2) < 1e-9:
                continue
            feats.append({
                "type": "Feature",
                "properties": {
                    "category": "flow_arrow",
                    "class": cls,
                    "from": [x1, y1],
                    "to": [x2, y2],
                },
                "geometry": {"type": "Point", "coordinates": coords[i]},
            })
            if len(feats) >= 1500:
                break
        if len(feats) >= 1500:
            break
    return feats


def main():
    log("=" * 60)
    log("Building 20 km NDVI canopy + DEM streams")
    log(f"bbox S,W,N,E = {BBOX}")
    log("=" * 60)
    skip_ndvi = "--skip-ndvi" in sys.argv
    if not skip_ndvi:
        log("--- 1. Sentinel-2 NDVI ---")
        ndvi_pack = fetch_sentinel2_ndvi_memory()
        if ndvi_pack is not None:
            ndvi_arr, ndvi_transform, ndvi_crs = ndvi_pack
            log(f"  NDVI shape: {ndvi_arr.shape}, "
                f"range {np.nanmin(ndvi_arr):.3f}–{np.nanmax(ndvi_arr):.3f}")
            polygonise_ndvi(ndvi_arr, ndvi_transform, ndvi_crs)
        else:
            log("  ⚠ NDVI skipped (STAC unavailable)")
    else:
        log("--- 1. Sentinel-2 NDVI --- SKIPPED")

    log("\n--- 2. Copernicus GLO-30 -> streams ---")
    dem_full, transform = fetch_dem_in_memory()
    # Subsample 6× to 180 m before flow-accumulation
    SUBSAMPLE = 6
    dem_ds = dem_full[::SUBSAMPLE, ::SUBSAMPLE].copy()
    new_transform = transform * rasterio.Affine.scale(SUBSAMPLE, SUBSAMPLE)
    log(f"  DEM downsampled 6× → {dem_ds.shape} ({dem_ds.size:,} cells)")
    valid_mask = ~np.isnan(dem_ds)
    dem_filled = np.nan_to_num(dem_ds, nan=float(np.nanmedian(dem_ds[valid_mask])))

    log("  D8 flow direction...")
    fdir = d8_flow_dir(dem_filled)
    log("  flow accumulation...")
    acc = flow_accumulation(dem_filled, fdir)
    log(f"  acc min={int(acc.min())}, max={int(acc.max())}, "
        f"median={int(np.median(acc[valid_mask]))}")

    all_feats = []
    for thr, label in [(500, "main_rivers ≥ 500 cells"),    # ≥ 16 km²
                        (200,  "tributaries ≥ 200 cells"),   # ≥ 6 km²
                        (80,   "headwaters ≥ 80 cells")]:    # ≥ 2.6 km²
        feats = extract_streams(dem_filled, acc, fdir, new_transform,
                                threshold_cells=thr, label=label)
        log(f"  {label}: {len(feats)} segments")
        all_feats.extend(feats)
    arrow_feats = extract_flow_arrows(all_feats, new_transform)
    log(f"  flow arrows: {len(arrow_feats)} segments")

    arrow_path = OUT / "dem_streams_arrows_20km.geojson"
    fc_arrows = {
        "type": "FeatureCollection",
        "name": "dem_streams_arrows_20km",
        "metadata": {
            "source": "Derived from dem_streams_20km.geojson",
            "purpose": "Point markers every ~1.5 km along main_rivers and "
                       "tributaries so the viewer can render arrowheads "
                       "pointing in the direction of flow.",
            "feature_count": len(arrow_feats),
            "generated_utc": datetime.utcnow().isoformat() + "Z",
        },
        "features": arrow_feats,
    }
    arrow_path.write_text(json.dumps(fc_arrows, separators=(",", ":")))
    log(f"  wrote {arrow_path}  ({len(arrow_feats)} arrows)")

    fc = {
        "type": "FeatureCollection",
        "name": "dem_streams_20km",
        "metadata": {
            "source": "Copernicus GLO-30 (AWS S3) + D8 flow accumulation",
            "bbox": list(BBOX),
            "pixel_resolution_m": 180,
            "thresholds": {
                "main_rivers_cells": 500, "tributaries_cells": 200,
                "headwaters_cells": 80,
            },
            "feature_count": len(all_feats),
            "generated_utc": datetime.utcnow().isoformat() + "Z",
        },
        "features": all_feats,
    }
    out = OUT / "dem_streams_20km.geojson"
    out.write_text(json.dumps(fc, separators=(",", ":")))
    log(f"  wrote {out}  ({out.stat().st_size/1024/1024:.2f} MB, "
        f"{len(all_feats)} stream segments)")


if __name__ == "__main__":
    main()
