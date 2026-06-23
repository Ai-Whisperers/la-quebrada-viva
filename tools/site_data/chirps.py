"""CHIRPS v2.0 monthly precipitation — parcel-scale (5 km) rainfall.

CHIRPS = Climate Hazards Group InfraRed Precipitation with Stations.
Free, no auth, public-domain (CHC). 5 km grid is meaningfully better
than ERA5's ~28 km for sub-parcel runoff + tank sizing on 62 ha.

Source: https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/tifs/
File pattern: `chirps-v2.0.YYYY.MM.tif.gz`  (gzipped GeoTIFF, ~3 MB each)

Behaviour:
  - downloads `START_YEAR..END_YEAR` monthly TIFFs into a cache dir
  - clips each to a tile bbox around the parcel and stores a small TIFF
  - aggregates to per-year and per-month climatologies → brochure

Run:
    python3 -m tools.site_data.chirps
    YEARS=2020:2025 python3 -m tools.site_data.chirps    # narrower window
"""
from __future__ import annotations

import datetime as dt
import gzip
import io
import os
import statistics
from pathlib import Path

import rasterio
from rasterio.windows import from_bounds

from .common import (
    http_get, out_dir, parcel_center, search_bbox, write_json,
)

BASE = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/tifs"

DEFAULT_START = 2005
DEFAULT_END = 2025


def parse_years() -> tuple[int, int]:
    raw = os.environ.get("YEARS")
    if not raw:
        return DEFAULT_START, DEFAULT_END
    a, b = raw.split(":")
    return int(a), int(b)


def download_month(year: int, month: int, cache: Path) -> Path:
    """Download + gunzip a CHIRPS monthly TIFF if not cached."""
    out_tif = cache / f"chirps-v2.0.{year}.{month:02d}.tif"
    if out_tif.exists() and out_tif.stat().st_size > 0:
        return out_tif
    url = f"{BASE}/chirps-v2.0.{year}.{month:02d}.tif.gz"
    r = http_get(url, timeout=120, stream=True)
    gz = io.BytesIO(r.content)
    with gzip.open(gz, "rb") as f:
        out_tif.write_bytes(f.read())
    return out_tif


def clip_to_parcel(src_tif: Path, out_tif: Path) -> None:
    """Crop the global TIFF to the parcel search-area bbox (~3.3 km × 3.3 km).

    CHIRPS is 0.05° resolution — clipping to the parcel gives a 1–2 px tile,
    which we store mainly so a future map render can pull it without a refetch.
    """
    b = search_bbox()
    with rasterio.open(src_tif) as src:
        window = from_bounds(b.left, b.bottom, b.right, b.top, src.transform)
        data = src.read(1, window=window)
        transform = src.window_transform(window)
        profile = src.profile.copy()
        profile.update(
            height=data.shape[0], width=data.shape[1],
            transform=transform, compress="deflate",
        )
        with rasterio.open(out_tif, "w", **profile) as dst:
            dst.write(data, 1)


def sample_at_point(src_tif: Path, lon: float, lat: float) -> float | None:
    """Single-pixel sample at the parcel center; returns mm for that month."""
    with rasterio.open(src_tif) as src:
        for v in src.sample([(lon, lat)]):
            val = float(v[0])
            if val < 0:    # CHIRPS nodata is −9999
                return None
            return val
    return None


def main() -> None:
    start_y, end_y = parse_years()
    out = out_dir("chirps")
    cache = out / "_cache"
    tiles = out / "tiles"
    cache.mkdir(parents=True, exist_ok=True)
    tiles.mkdir(parents=True, exist_ok=True)
    lon, lat = parcel_center()

    print(f"[chirps] downloading {start_y}-{end_y} monthly TIFFs (5 km, ~3 MB each)")
    series: list[tuple[int, int, float | None]] = []
    for y in range(start_y, end_y + 1):
        for m in range(1, 13):
            try:
                tif = download_month(y, m, cache)
            except Exception as e:
                print(f"[chirps] skip {y}-{m:02d}: {e}")
                series.append((y, m, None))
                continue
            tile = tiles / f"chirps_{y}_{m:02d}.tif"
            if not tile.exists():
                clip_to_parcel(tif, tile)
            val = sample_at_point(tif, lon, lat)
            series.append((y, m, val))

    # Per-year totals.
    yearly: dict[int, float] = {}
    monthly: dict[int, list[float]] = {m: [] for m in range(1, 13)}
    for y, m, v in series:
        if v is None:
            continue
        yearly[y] = yearly.get(y, 0.0) + v
        monthly[m].append(v)

    annual_mean = round(statistics.fmean(yearly.values()), 1) if yearly else 0.0
    annual_min = round(min(yearly.values()), 1) if yearly else 0.0
    annual_max = round(max(yearly.values()), 1) if yearly else 0.0

    summary = {
        "source": "CHIRPS v2.0 monthly, CHC/UCSB (public domain)",
        "resolution_deg": 0.05,
        "resolution_km_approx": 5.5,
        "parcel_center": [lon, lat],
        "window": [start_y, end_y],
        "yearly_total_mm": yearly,
        "monthly_mean_mm": {
            m: round(statistics.fmean(vs), 1) for m, vs in monthly.items() if vs
        },
        "annual_total_mean_mm": annual_mean,
        "annual_total_min_mm": annual_min,
        "annual_total_max_mm": annual_max,
        "n_months_with_data": sum(1 for _, _, v in series if v is not None),
    }
    write_json(out / "chirps_summary.json", summary)

    months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    brochure = [
        "# CHIRPS monthly precipitation — La Quebrada Viva parcel",
        "",
        f"Source: CHIRPS v2.0 (Climate Hazards Group, UCSB), public domain  ",
        f"Resolution: 0.05° (~5.5 km)  ",
        f"Window: {start_y}-{end_y}  ",
        f"Point: lon={lon:.5f}, lat={lat:.5f}  ",
        f"Pulled: {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "",
        "## Annual totals",
        "",
        f"- Mean: **{annual_mean} mm/yr**",
        f"- Min:  {annual_min} mm/yr",
        f"- Max:  {annual_max} mm/yr",
        "",
        "## Monthly climatology (mm, long-term mean)",
        "",
        "| Month | mm |",
        "| --- | ---:|",
    ]
    for m in range(1, 13):
        vs = monthly[m]
        if vs:
            brochure.append(f"| {months[m]} | {round(statistics.fmean(vs), 1)} |")
    brochure += [
        "",
        "## Interpretation hooks",
        "",
        "- Tank sizing: design against the *driest-year* total, not the mean — see `chirps_summary.json` → `annual_total_min_mm`.",
        "- The driest 3-month run drives cistern volume; pick the lowest three consecutive months in the table above.",
        "- Compare against `docs/site_data/climate_era5/` precip series — if CHIRPS is meaningfully drier, trust CHIRPS at parcel scale (5 km beats 28 km).",
        "- Clipped per-month TIFFs: `tiles/chirps_YYYY_MM.tif` (small).",
    ]
    (out / "chirps_brochure.md").write_text("\n".join(brochure))

    summary_txt = [
        f"CHIRPS monthly {start_y}-{end_y}",
        f"n_months_with_data: {summary['n_months_with_data']}",
        f"annual mean: {annual_mean} mm/yr",
        f"annual min:  {annual_min} mm/yr",
        f"annual max:  {annual_max} mm/yr",
    ]
    (out / "chirps_summary.txt").write_text("\n".join(summary_txt) + "\n")
    print(f"[chirps] wrote {out}")


if __name__ == "__main__":
    main()
