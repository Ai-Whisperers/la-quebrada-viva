"""
Phase-0 §12 — MOD16A2.061 actual evapotranspiration time-series (NASA LP DAAC).

MOD16A2 is the MODIS 8-day composite 500 m gridded ET / PET / LE / PLE product
(Mu, Zhao, Running 2011, updated to v6.1 / Collection 6.1 in 2021). Granules
arrive on the global MODIS sinusoidal grid; tile h12v11 covers our Escobar AOI
in full.

We stream each ~30 MB HDF4-EOS granule, open via pyhdf, slice an AOI-tight
window in sinusoidal pixel space, reproject the small window to EPSG:4326,
sample the 6 standard points at exact MODIS pixel locations (no resampling
artefacts), then delete the HDF — same stream-and-extract pattern used by the
CMIP6 NEX-GDDP puller.

Bands and scale (MODIS LP DAAC v6.1 docs):
  ET_500m, PET_500m   int16  scale 0.1   units kg/m²/8day == mm/8day
  LE_500m, PLE_500m   int16  scale 10000 units J/m²/day   (energy flux)
  ET_QC_500m          uint8  bit-flags   (0 = good, 32 = nominal w/ degraded)
  _FillValue 32767, valid_range [-32767, 32700]

Aggregations:
  - Per-granule per-point sample (kg/m²/8day)
  - Per-month total mm (sum of 8-day composites whose start-DOY falls in month)
  - Per-year total mm (sum of all 46 composites per year)
  - Per-month and per-year AOI mean (over 5 km buffer reprojected clip)
  - ET / PET ratio (water stress index, 0 = fully stressed, 1 = unstressed)

Outputs:
  docs/site_data/mod16/mod16_per_granule_points.csv   per-granule per-point samples
  docs/site_data/mod16/mod16_monthly_points.csv       per-point monthly totals
  docs/site_data/mod16/mod16_annual_points.csv        per-point annual totals
  docs/site_data/mod16/mod16_aoi_monthly.csv          AOI mean monthly
  docs/site_data/mod16/mod16_aoi_annual.csv           AOI mean annual
  docs/site_data/mod16/mod16_summary.json             provenance + aggregates
  docs/site_data/mod16/mod16_<band>_<year>_mean.tif   per-year per-band mean clip
"""

from __future__ import annotations

import csv
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import rasterio
from pyhdf.SD import SD, SDC
from rasterio.transform import Affine
from rasterio.warp import Resampling, reproject

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs/site_data/mod16"
CACHE_DIR = OUT_DIR / "_cache"
OUT_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Earthdata auth — alias project's NASA_* env vars to earthaccess's expected names
ENV_LOCAL = ROOT / ".env.local"
if ENV_LOCAL.exists():
    for line in ENV_LOCAL.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())
if "NASA_EARTHDATA_TOKEN" in os.environ:
    os.environ["EARTHDATA_TOKEN"] = os.environ["NASA_EARTHDATA_TOKEN"]
if "NASA_EARTHDATA_USERNAME" in os.environ:
    os.environ["EARTHDATA_USERNAME"] = os.environ["NASA_EARTHDATA_USERNAME"]
if "NASA_EARTHDATA_PASSWORD" in os.environ:
    os.environ["EARTHDATA_PASSWORD"] = os.environ["NASA_EARTHDATA_PASSWORD"]

import earthaccess  # noqa: E402  (must be after env aliasing)

# ---------- AOI / point geometry ----------
CENTROID = (-57.0355, -25.6073)
WESLEY = (-57.03365675409436, -25.61138883666841)
KML_CORNERS = {
    "corner_NE": (-57.0151, -25.6149),
    "corner_NW": (-57.0451, -25.6149),
    "corner_SE": (-57.0151, -25.6449),
    "corner_SW": (-57.0451, -25.6449),
}
POINTS: list[tuple[str, float, float]] = [
    ("centroid", CENTROID[0], CENTROID[1]),
    *((k, v[0], v[1]) for k, v in KML_CORNERS.items()),
    ("wesley_pin", WESLEY[0], WESLEY[1]),
]
AOI_BUFFER_DEG = 0.05  # 5 km around centroid

# ---------- MODIS sinusoidal grid (tile h12v11 metadata read from sample granule) ----------
# Standard MODIS sinusoidal CRS uses a sphere of radius 6371007.181 m.
MODIS_SINU_CRS = (
    "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 "
    "+a=6371007.181 +b=6371007.181 +units=m +no_defs"
)
# Tile h12v11 corners (from StructMetadata.0 of any granule we open)
TILE_UL = (-6671703.118000, -2223901.039333)  # (x, y) of upper-left pixel CENTER outside ── actually pixel boundary; see below
TILE_LR = (-5559752.598333, -3335851.559000)
GRID_N = 2400  # 2400×2400 pixels per tile
PIXEL_SIZE_M = (TILE_LR[0] - TILE_UL[0]) / GRID_N  # +463.3127 m
PIXEL_SIZE_Y = (TILE_LR[1] - TILE_UL[1]) / GRID_N  # -463.3127 m
# rasterio Affine: x_origin maps to col 0 *upper-left corner*. HDFE_CENTER means
# UpperLeftPointMtrs is pixel center → shift by half a pixel for GTiff convention.
TILE_TRANSFORM = Affine(
    PIXEL_SIZE_M, 0.0, TILE_UL[0] - PIXEL_SIZE_M / 2,
    0.0, PIXEL_SIZE_Y, TILE_UL[1] - PIXEL_SIZE_Y / 2,
)

BANDS = {
    "ET":  {"sds": "ET_500m",  "scale": 0.1,   "unit": "mm/8day"},
    "PET": {"sds": "PET_500m", "scale": 0.1,   "unit": "mm/8day"},
    "LE":  {"sds": "LE_500m",  "scale": 10000, "unit": "J/m2/day"},
    "PLE": {"sds": "PLE_500m", "scale": 10000, "unit": "J/m2/day"},
}
FILL_VALUE = 32767
VALID_MAX = 32700  # values > 32700 are mask/fill codes per LP DAAC docs


# ---------- helpers ----------

def aoi_bounds() -> tuple[float, float, float, float]:
    lon, lat = CENTROID
    return (
        lon - AOI_BUFFER_DEG,
        lat - AOI_BUFFER_DEG,
        lon + AOI_BUFFER_DEG,
        lat + AOI_BUFFER_DEG,
    )


def lonlat_to_sinu(lon: float, lat: float) -> tuple[float, float]:
    """Project lon/lat (degrees) to MODIS sinusoidal metres (sphere R=6371007.181)."""
    R = 6371007.181
    rad = np.pi / 180.0
    x = R * lon * rad * np.cos(lat * rad)
    y = R * lat * rad
    return float(x), float(y)


def sinu_pixel_indices(lon: float, lat: float) -> tuple[int, int]:
    """Return (row, col) of the MODIS pixel containing lon/lat in tile h12v11."""
    x, y = lonlat_to_sinu(lon, lat)
    col = int(round((x - TILE_UL[0]) / PIXEL_SIZE_M))
    row = int(round((y - TILE_UL[1]) / PIXEL_SIZE_Y))
    return row, col


def aoi_pixel_window() -> tuple[int, int, int, int]:
    """Return (row_off, col_off, height, width) covering AOI bbox in tile grid."""
    left, bottom, right, top = aoi_bounds()
    # Corners of AOI bbox in sinusoidal
    xs, ys = [], []
    for lon, lat in [(left, top), (right, top), (left, bottom), (right, bottom)]:
        x, y = lonlat_to_sinu(lon, lat)
        xs.append(x); ys.append(y)
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    col0 = int(np.floor((x_min - TILE_UL[0]) / PIXEL_SIZE_M)) - 1
    col1 = int(np.ceil((x_max - TILE_UL[0]) / PIXEL_SIZE_M)) + 1
    # In tile grid, row increases as y decreases (PIXEL_SIZE_Y is negative)
    row0 = int(np.floor((y_max - TILE_UL[1]) / PIXEL_SIZE_Y)) - 1
    row1 = int(np.ceil((y_min - TILE_UL[1]) / PIXEL_SIZE_Y)) + 1
    col0 = max(0, col0); row0 = max(0, row0)
    col1 = min(GRID_N, col1); row1 = min(GRID_N, row1)
    return row0, col0, row1 - row0, col1 - col0


def doy_to_date(year: int, doy: int) -> date:
    return date(year, 1, 1) + timedelta(days=doy - 1)


def search_granules(year_from: int, year_to: int) -> list:
    bbox = (-57.10, -25.66, -57.00, -25.56)
    results = earthaccess.search_data(
        short_name="MOD16A2",
        version="061",
        bounding_box=bbox,
        temporal=(f"{year_from}-01-01", f"{year_to}-12-31"),
        count=2000,
    )
    return list(results)


def open_band(hdf_path: Path, sds_name: str, window: tuple[int, int, int, int]) -> np.ndarray:
    """Slice an int16 band over the AOI pixel window using pyhdf."""
    row_off, col_off, h, w = window
    sd = SD(str(hdf_path), SDC.READ)
    try:
        ds = sd.select(sds_name)
        arr = ds.get(start=(row_off, col_off), count=(h, w)).astype(np.int32)
        ds.endaccess()
    finally:
        sd.end()
    return arr


def read_point_pixel(hdf_path: Path, sds_name: str, row: int, col: int) -> int | None:
    sd = SD(str(hdf_path), SDC.READ)
    try:
        ds = sd.select(sds_name)
        val = int(ds.get(start=(row, col), count=(1, 1))[0, 0])
        ds.endaccess()
    finally:
        sd.end()
    return val


def mask_and_scale(arr_int: np.ndarray, scale: float) -> np.ndarray:
    out = np.where(arr_int > VALID_MAX, np.nan, arr_int.astype(np.float64) * scale)
    return out


def reproject_window_to_wgs84(arr: np.ndarray, window: tuple[int, int, int, int]) -> tuple[np.ndarray, Affine]:
    """Reproject sinusoidal window to EPSG:4326 over AOI bbox."""
    row_off, col_off = window[0], window[1]
    src_transform = Affine(
        PIXEL_SIZE_M, 0.0, TILE_UL[0] - PIXEL_SIZE_M / 2 + col_off * PIXEL_SIZE_M,
        0.0, PIXEL_SIZE_Y, TILE_UL[1] - PIXEL_SIZE_Y / 2 + row_off * PIXEL_SIZE_Y,
    )
    left, bottom, right, top = aoi_bounds()
    # ~500 m → ≈0.0045°; pick 0.005° (≈555 m) grid spacing for AOI clip
    res = 0.005
    dst_w = int(np.ceil((right - left) / res))
    dst_h = int(np.ceil((top - bottom) / res))
    dst_transform = Affine(res, 0.0, left, 0.0, -res, top)
    dst = np.full((dst_h, dst_w), np.nan, dtype=np.float64)
    reproject(
        source=arr,
        destination=dst,
        src_transform=src_transform,
        src_crs=MODIS_SINU_CRS,
        dst_transform=dst_transform,
        dst_crs="EPSG:4326",
        resampling=Resampling.bilinear,
        src_nodata=np.nan,
        dst_nodata=np.nan,
    )
    return dst, dst_transform


def write_geotiff(path: Path, arr: np.ndarray, transform: Affine) -> None:
    h, w = arr.shape
    profile = {
        "driver": "GTiff",
        "dtype": "float32",
        "count": 1,
        "height": h,
        "width": w,
        "crs": "EPSG:4326",
        "transform": transform,
        "nodata": -9999.0,
        "compress": "deflate",
    }
    # AOI is ~20-25 px wide here; rasterio requires tile blocks to be multiples
    # of 16, and tiling buys nothing on rasters this small. Skip it when either
    # dimension is < 32.
    if h >= 32 and w >= 32:
        profile["tiled"] = True
        profile["blockxsize"] = 16 * max(1, min(64, w) // 16)
        profile["blockysize"] = 16 * max(1, min(64, h) // 16)
    out = np.where(np.isfinite(arr), arr, -9999.0).astype(np.float32)
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(out, 1)


# ---------- main pipeline ----------

def main(year_from: int = 2015, year_to: int = 2024) -> None:
    print(f"Earthdata login …", flush=True)
    auth = earthaccess.login(strategy="environment")
    print(f"  authenticated={getattr(auth, 'authenticated', None)}", flush=True)

    print(f"AOI bbox: {aoi_bounds()}", flush=True)
    window = aoi_pixel_window()
    print(f"MODIS pixel window (row_off, col_off, h, w): {window}", flush=True)

    # Pre-compute per-point (row, col) — these are fixed for the whole tile/run
    point_rc: dict[str, tuple[int, int]] = {}
    for name, lon, lat in POINTS:
        r, c = sinu_pixel_indices(lon, lat)
        if not (0 <= r < GRID_N and 0 <= c < GRID_N):
            raise RuntimeError(f"point {name} ({lon},{lat}) outside tile h12v11 grid")
        point_rc[name] = (r, c)
        print(f"  point {name:11s} → row={r:4d} col={c:4d}", flush=True)

    print(f"\nSearching MOD16A2 granules {year_from}-{year_to} …", flush=True)
    all_granules = search_granules(year_from, year_to)
    # Filter to tile h12v11 only (CMR sometimes returns adjacent tiles)
    granules = []
    for g in all_granules:
        urls = g.data_links()
        if urls and "h12v11" in urls[0]:
            granules.append(g)
    print(f"  {len(all_granules)} granules total, {len(granules)} on tile h12v11", flush=True)

    per_granule_rows: list[dict] = []
    # Running per-year per-band accumulators on AOI clip
    aoi_accum: dict[tuple[int, str], list[np.ndarray]] = {}
    monthly_per_point: dict[tuple[int, int, str, str], float] = {}  # (year, month, point, band) → mm
    transform_dst: Affine | None = None

    for i, g in enumerate(granules, 1):
        url = g.data_links()[0]
        fname = url.rsplit("/", 1)[-1]
        # Parse year/DOY from filename like MOD16A2.A2024001.h12v11.061.<prod>.hdf
        token = fname.split(".")[1]  # A2024001
        year = int(token[1:5])
        doy = int(token[5:8])
        start = doy_to_date(year, doy)
        month = start.month
        # 8-day composite that spans days doy..doy+7 (last of year may be shorter)
        # We attribute the whole composite to its start month for monthly aggregation
        hdf_path = CACHE_DIR / fname
        if not hdf_path.exists():
            print(f"  [{i:4d}/{len(granules)}] {fname} …", end="", flush=True)
            try:
                earthaccess.download([g], local_path=str(CACHE_DIR))
                print(f" ok ({hdf_path.stat().st_size//1024} KB)", flush=True)
            except Exception as e:
                print(f" FAIL: {e}", flush=True)
                continue
        else:
            print(f"  [{i:4d}/{len(granules)}] {fname} (cached)", flush=True)

        try:
            # Per-point exact pixel reads
            row_g = {"granule": fname, "year": year, "doy": doy, "date": start.isoformat()}
            for pname, (r, c) in point_rc.items():
                for bkey, meta in BANDS.items():
                    raw = read_point_pixel(hdf_path, meta["sds"], r, c)
                    if raw is None or raw > VALID_MAX:
                        val = None
                    else:
                        val = round(raw * meta["scale"], 4)
                    row_g[f"{pname}_{bkey}"] = val
                    if bkey in ("ET", "PET") and val is not None:
                        key = (year, month, pname, bkey)
                        monthly_per_point[key] = monthly_per_point.get(key, 0.0) + val
            per_granule_rows.append(row_g)

            # AOI window reproject + accumulate by year
            for bkey, meta in BANDS.items():
                raw_arr = open_band(hdf_path, meta["sds"], window)
                scaled = mask_and_scale(raw_arr, meta["scale"])
                wgs, dst_t = reproject_window_to_wgs84(scaled, window)
                transform_dst = dst_t
                aoi_accum.setdefault((year, bkey), []).append(wgs)
        finally:
            try:
                hdf_path.unlink()
            except OSError:
                pass

    if not per_granule_rows:
        print("No granules retrieved; aborting.", flush=True)
        return

    # ---- write per-granule CSV ----
    cols = ["granule", "year", "doy", "date"]
    for pname, _, _ in POINTS:
        for bkey in BANDS:
            cols.append(f"{pname}_{bkey}")
    csv_path = OUT_DIR / "mod16_per_granule_points.csv"
    with csv_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(per_granule_rows)
    print(f"\nWrote {csv_path} ({len(per_granule_rows)} rows)", flush=True)

    # ---- monthly per-point CSV ----
    monthly_rows: list[dict] = []
    years = sorted({k[0] for k in monthly_per_point.keys()})
    months = list(range(1, 13))
    for y in years:
        for m in months:
            row: dict[str, object] = {"year": y, "month": m}
            for pname, _, _ in POINTS:
                for bkey in ("ET", "PET"):
                    v = monthly_per_point.get((y, m, pname, bkey))
                    row[f"{pname}_{bkey}_mm"] = round(v, 3) if v is not None else None
            monthly_rows.append(row)
    monthly_path = OUT_DIR / "mod16_monthly_points.csv"
    with monthly_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(monthly_rows[0].keys()))
        w.writeheader()
        w.writerows(monthly_rows)
    print(f"Wrote {monthly_path} ({len(monthly_rows)} rows)", flush=True)

    # ---- annual per-point CSV ----
    annual_per_point: dict[tuple[int, str, str], float] = {}
    for (y, m, p, b), v in monthly_per_point.items():
        annual_per_point[(y, p, b)] = annual_per_point.get((y, p, b), 0.0) + v
    annual_rows: list[dict] = []
    for y in years:
        row: dict[str, object] = {"year": y}
        for pname, _, _ in POINTS:
            for bkey in ("ET", "PET"):
                v = annual_per_point.get((y, pname, bkey))
                row[f"{pname}_{bkey}_mm"] = round(v, 2) if v is not None else None
            # ET/PET water-stress index
            et = annual_per_point.get((y, pname, "ET"))
            pet = annual_per_point.get((y, pname, "PET"))
            row[f"{pname}_ET_over_PET"] = round(et / pet, 4) if et and pet else None
        annual_rows.append(row)
    annual_path = OUT_DIR / "mod16_annual_points.csv"
    with annual_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(annual_rows[0].keys()))
        w.writeheader()
        w.writerows(annual_rows)
    print(f"Wrote {annual_path} ({len(annual_rows)} rows)", flush=True)

    # ---- AOI annual mean GeoTIFFs + AOI summary ----
    aoi_annual_rows: list[dict] = []
    for y in sorted({k[0] for k in aoi_accum}):
        row: dict[str, object] = {"year": y}
        for bkey, meta in BANDS.items():
            stk = aoi_accum.get((y, bkey))
            if not stk:
                continue
            cube = np.stack(stk, axis=0)
            # 8-day mean over the year (for ET/PET sum-of-mean × 46 ≈ annual)
            mean_arr = np.nanmean(cube, axis=0)
            sum_arr = np.nansum(cube, axis=0)
            tif = OUT_DIR / f"mod16_{bkey}_{y}_mean.tif"
            if transform_dst is None:
                raise RuntimeError("transform_dst unset — no granule was successfully reprojected")
            write_geotiff(tif, mean_arr.astype(np.float32), transform_dst)
            row[f"AOI_{bkey}_mean_{meta['unit']}"] = round(float(np.nanmean(mean_arr)), 4)
            if bkey in ("ET", "PET"):
                row[f"AOI_{bkey}_annual_mm"] = round(float(np.nanmean(sum_arr)), 2)
        et_ann = row.get("AOI_ET_annual_mm")
        pet_ann = row.get("AOI_PET_annual_mm")
        row["AOI_ET_over_PET"] = (
            round(float(et_ann) / float(pet_ann), 4)
            if isinstance(et_ann, (int, float)) and isinstance(pet_ann, (int, float)) and pet_ann
            else None
        )
        aoi_annual_rows.append(row)
    aoi_annual_path = OUT_DIR / "mod16_aoi_annual.csv"
    if aoi_annual_rows:
        with aoi_annual_path.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(aoi_annual_rows[0].keys()))
            w.writeheader()
            w.writerows(aoi_annual_rows)
        print(f"Wrote {aoi_annual_path}", flush=True)

    # AOI monthly skipped: would require keeping all 460+ clip stacks on disk.
    # Per-point monthlies in mod16_monthly_points.csv cover the per-month story.

    # ---- summary JSON ----
    summary = {
        "source": "MOD16A2.061 (MODIS Terra/Aqua Combined ET/PET 8-day 500 m)",
        "provider": "NASA LP DAAC via Earthdata Cloud",
        "collection_id": "C2565788905-LPCLOUD (LP DAAC v6.1)",
        "tile": "h12v11 (MODIS sinusoidal)",
        "year_from": year_from,
        "year_to": year_to,
        "granules_total": len(all_granules),
        "granules_used": len(per_granule_rows),
        "aoi_bbox_lonlat": list(aoi_bounds()),
        "aoi_window_pixels": list(window),
        "points": [{"name": n, "lon": lo, "lat": la, "row": point_rc[n][0], "col": point_rc[n][1]}
                   for n, lo, la in POINTS],
        "bands": {k: {**v, "fill_value": FILL_VALUE, "valid_max_raw": VALID_MAX}
                  for k, v in BANDS.items()},
        "annual_aoi": aoi_annual_rows,
        "annual_per_point": annual_rows,
        "citation": "Running S., Mu Q., Zhao M. (2021). MOD16A2 v6.1 — MODIS/Terra Net "
                    "Evapotranspiration 8-Day L4 Global 500m SIN Grid. NASA LP DAAC. "
                    "https://doi.org/10.5067/MODIS/MOD16A2.061",
        "license": "Public domain (NASA)",
    }
    summary_path = OUT_DIR / "mod16_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    print(f"Wrote {summary_path}", flush=True)

    print("\n=== AOI annual ET / PET / ET-PET ratio ===", flush=True)
    for r in aoi_annual_rows:
        et = r.get("AOI_ET_annual_mm"); pet = r.get("AOI_PET_annual_mm")
        ratio = r.get("AOI_ET_over_PET")
        print(f"  {r['year']}  ET={et} mm  PET={pet} mm  ET/PET={ratio}", flush=True)


if __name__ == "__main__":
    yf = int(sys.argv[1]) if len(sys.argv) > 1 else 2015
    yt = int(sys.argv[2]) if len(sys.argv) > 2 else 2024
    main(yf, yt)
