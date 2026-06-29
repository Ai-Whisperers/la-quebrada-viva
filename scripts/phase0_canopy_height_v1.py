"""
Phase-0 §12 — Meta/Tolan 2024 1 m Canopy Height Model (CHM) windowed AOI pull.

Source: AWS Open Data Registry `dataforgood-fb-data` bucket, anonymous S3 read
via /vsicurl/. EPSG:4326 reprojected 10° tile mosaic
`alsgedi_global_v6_float_epsg4326_v3_10deg`.

For our centroid (-57.0355, -25.6073), the covering tile is
`meta_chm_lat=-20.0_lon=-60.0_<stat>.tif` (covers lon -60 to -50,
lat -30 to -20). Native CHM is 1 m equivalent; the 10° resampled
product carries summary stats per pixel.

Outputs:
  docs/site_data/canopy_height/meta_chm_aoi_<stat>.tif  (windowed AOI rasters)
  docs/site_data/canopy_height/canopy_points.csv        (per-point sample)
  docs/site_data/canopy_height/canopy_summary.json      (AOI stats)
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import rasterio
from rasterio.windows import from_bounds

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs/site_data/canopy_height"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BUCKET = (
    "https://dataforgood-fb-data.s3.amazonaws.com/forests/v1/"
    "alsgedi_global_v6_float_epsg4326_v3_10deg/"
)
TILE_TAG = "meta_chm_lat=-20.0_lon=-60.0"
STATS = ("avg", "median", "p95", "cover", "cover5m", "stdev", "count")

# Tolan 2024 EPSG:4326 10° tiles are uint16 with packed units:
#   heights (avg/median/p95/stdev): centimeters -> ×0.01 = meters
#   cover/cover5m: per-mille (0..1000) -> ×0.1 = percent
#   count: raw integer count of native CHM observations contributing
SCALE = {
    "avg": 0.01,
    "median": 0.01,
    "p95": 0.01,
    "stdev": 0.01,
    "cover": 0.1,
    "cover5m": 0.1,
    "count": 1.0,
}
UNIT = {
    "avg": "m",
    "median": "m",
    "p95": "m",
    "stdev": "m",
    "cover": "%",
    "cover5m": "%",
    "count": "n",
}

CENTROID = (-57.0355, -25.6073)
WESLEY = (-57.03365675409436, -25.61138883666841)
KML_CORNERS = {
    "corner_NE": (-57.0151, -25.6149),
    "corner_NW": (-57.0451, -25.6149),
    "corner_SE": (-57.0151, -25.6449),
    "corner_SW": (-57.0451, -25.6449),
}
POINTS = [
    ("centroid", CENTROID[0], CENTROID[1]),
    *((k, v[0], v[1]) for k, v in KML_CORNERS.items()),
    ("wesley_pin", WESLEY[0], WESLEY[1]),
]

# 5 km buffer around centroid for AOI window
AOI_BUFFER_DEG = 0.05  # ~5.5 km in latitude


def aoi_bounds() -> tuple[float, float, float, float]:
    lon, lat = CENTROID
    return (
        lon - AOI_BUFFER_DEG,
        lat - AOI_BUFFER_DEG,
        lon + AOI_BUFFER_DEG,
        lat + AOI_BUFFER_DEG,
    )


def fetch_stat(stat: str) -> Path:
    url = f"/vsicurl/{BUCKET}{TILE_TAG}_{stat}.tif"
    dst = OUT_DIR / f"meta_chm_aoi_{stat}.tif"
    left, bottom, right, top = aoi_bounds()
    with rasterio.open(url) as src:
        window = from_bounds(left, bottom, right, top, transform=src.transform)
        window = window.round_offsets().round_lengths()
        arr = src.read(1, window=window)
        transform = src.window_transform(window)
        profile = src.profile.copy()
        profile.update(
            height=arr.shape[0],
            width=arr.shape[1],
            transform=transform,
            compress="deflate",
            tiled=True,
            blockxsize=256,
            blockysize=256,
        )
        with rasterio.open(dst, "w", **profile) as out:
            out.write(arr, 1)
    return dst


def sample_points(rasters: dict[str, Path]) -> list[dict]:
    rows: list[dict] = []
    opened = {stat: rasterio.open(p) for stat, p in rasters.items()}
    try:
        for name, lon, lat in POINTS:
            row: dict = {"point": name, "lon": lon, "lat": lat}
            for stat, src in opened.items():
                col, r = ~src.transform * (lon, lat)
                col = int(round(col))
                r = int(round(r))
                if 0 <= col < src.width and 0 <= r < src.height:
                    # 3x3 window mean (≈1.6 km @ 0.005° pixel — fine for 10°-resampled CHM)
                    c0 = max(0, col - 1)
                    c1 = min(src.width, col + 2)
                    r0 = max(0, r - 1)
                    r1 = min(src.height, r + 2)
                    arr = src.read(1, window=((r0, r1), (c0, c1))).astype(np.float64)
                    arr = arr[np.isfinite(arr)]
                    val = float(np.nanmean(arr)) * SCALE[stat] if arr.size else float("nan")
                else:
                    val = float("nan")
                row[stat] = round(val, 3)
            rows.append(row)
    finally:
        for src in opened.values():
            src.close()
    return rows


def aoi_summary(rasters: dict[str, Path]) -> dict:
    summary: dict = {}
    for stat, p in rasters.items():
        with rasterio.open(p) as src:
            arr = src.read(1).astype(np.float64)
            arr = arr[np.isfinite(arr)]
            if arr.size == 0:
                summary[stat] = None
                continue
            s = SCALE[stat]
            summary[stat] = {
                "unit": UNIT[stat],
                "mean": round(float(np.mean(arr)) * s, 3),
                "median": round(float(np.median(arr)) * s, 3),
                "p95": round(float(np.percentile(arr, 95)) * s, 3),
                "max": round(float(np.max(arr)) * s, 3),
                "min": round(float(np.min(arr)) * s, 3),
                "pixels": int(arr.size),
            }
    return summary


def main() -> None:
    print(f"AOI bounds: {aoi_bounds()}")
    rasters: dict[str, Path] = {}
    for stat in STATS:
        print(f"  fetching {stat} …", flush=True)
        rasters[stat] = fetch_stat(stat)
        size_kb = rasters[stat].stat().st_size // 1024
        print(f"    → {rasters[stat].name} ({size_kb} KB)")
    rows = sample_points(rasters)
    summary = aoi_summary(rasters)

    csv_path = OUT_DIR / "canopy_points.csv"
    fieldnames = ["point", "lon", "lat", *STATS]
    with csv_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {csv_path}")

    summary_path = OUT_DIR / "canopy_summary.json"
    payload = {
        "source": "Tolan et al. 2024 — Meta High-Resolution Canopy Height 1 m (EPSG:4326 10° resampled)",
        "bucket": "dataforgood-fb-data/forests/v1/alsgedi_global_v6_float_epsg4326_v3_10deg",
        "tile": TILE_TAG,
        "aoi_bounds": list(aoi_bounds()),
        "buffer_deg": AOI_BUFFER_DEG,
        "stats": STATS,
        "aoi_summary": summary,
        "points": rows,
    }
    with summary_path.open("w") as fh:
        json.dump(payload, fh, indent=2)
    print(f"Wrote {summary_path}")

    print("\n=== Per-point canopy — 3x3 mean of 28m pixels around point ===")
    print("    height stats in meters; cover stats in percent of pixel canopy area")
    for r in rows:
        print(
            f"  {r['point']:12s}  avg={r['avg']:5.2f}m  median={r['median']:5.2f}m  "
            f"p95={r['p95']:5.2f}m  cover={r['cover']:5.1f}%  cover5m={r['cover5m']:5.1f}%"
        )

    print("\n=== AOI summary (5 km buffer around centroid) ===")
    for stat, s in summary.items():
        if s is None:
            continue
        print(
            f"  {stat:8s} ({s['unit']})  mean={s['mean']:7.2f}  median={s['median']:7.2f}  "
            f"p95={s['p95']:7.2f}  max={s['max']:7.2f}  pixels={s['pixels']}"
        )


if __name__ == "__main__":
    main()
