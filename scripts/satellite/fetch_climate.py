#!/usr/bin/env python3
"""Climate data fetcher for La Quebrada Viva.

Pulls two climate products via Microsoft Planetary Computer STAC,
clipped to the AOI, written under ``docs/site_data/climate/``:

  1. CHIRPS daily rainfall (0.05° ≈ 5 km, 1981-present).
     Aggregated to monthly totals over the requested window.
  2. TerraClimate monthly water-balance climate (~4 km, 1958-present).
     Variables: pet, ppt, tmin, tmax, vap, soil moisture.

Why this script exists: the deck and the site-management plan need
defensible numbers for "how dry is the dry season" and "what's the
trend over the last 10 years" — that's CHIRPS + TerraClimate, not
forecast data. These are the canonical references the IPCC AR6
authors cite.

Auth: PC STAC is auth-free; downloads use signed asset HREFs via
``planetary_computer.sign_inplace``.

Usage:
    python -m scripts.satellite.fetch_climate
    python -m scripts.satellite.fetch_climate --only chirps --start 2024-01-01 --end 2026-06-01
    python -m scripts.satellite.fetch_climate --only terraclimate --start 2015-01-01

Outputs:
  docs/site_data/climate/chirps_<start>_<end>_monthly.tif
  docs/site_data/climate/terraclimate_<var>_<start>_<end>.tif
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts.satellite._aoi import aoi_bbox

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = _PROJECT_ROOT / "docs" / "site_data" / "climate"

PC_STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"

TERRACLIMATE_VARS_DEFAULT = ["ppt", "pet", "tmin", "tmax", "soil"]


def _need(pkg: str) -> str:
    return (
        f"Missing dep: {pkg!r}.\n"
        f"  pip install planetary-computer pystac-client rioxarray xarray\n"
    )


def _open_catalog():
    try:
        import planetary_computer as pc
        from pystac_client import Client
    except ImportError as e:
        print(_need(e.name or "planetary-computer/pystac-client"), file=sys.stderr)
        return None
    return Client.open(PC_STAC_URL, modifier=pc.sign_inplace)


def fetch_chirps(catalog, start: str, end: str):
    try:
        import rioxarray  # noqa: F401  (rio accessor registration)
        import xarray as xr
    except ImportError:
        print(_need("rioxarray/xarray"), file=sys.stderr)
        return False

    w, s, e, n = aoi_bbox()
    search = catalog.search(
        collections=["chirps"],
        bbox=[w, s, e, n],
        datetime=f"{start}/{end}",
    )
    items = list(search.items())
    if not items:
        print("  [chirps] no items found.")
        return False
    print(f"  [chirps] {len(items)} daily items found; aggregating to monthly…")

    # CHIRPS items expose a single 'data' asset (GeoTIFF per day).
    arrays = []
    for it in items:
        if "data" not in it.assets:
            continue
        href = it.assets["data"].href
        da = (
            xr.open_dataarray(href, engine="rasterio")
            .squeeze(drop=True)
            .rio.clip_box(minx=w, miny=s, maxx=e, maxy=n, crs="EPSG:4326")
        )
        da = da.assign_coords(time=it.datetime).expand_dims("time")
        arrays.append(da)
    if not arrays:
        print("  [chirps] no usable assets — skipping.")
        return False

    stack = xr.concat(arrays, dim="time").sortby("time")
    monthly = stack.resample(time="1MS").sum()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"chirps_{start}_{end}_monthly.tif"
    monthly.rio.to_raster(out, compress="DEFLATE", tiled=True)
    print(f"  [chirps] → {out} ({out.stat().st_size//1024} KB)")
    return True


def fetch_terraclimate(catalog, start: str, end: str, variables: list[str]):
    try:
        import rioxarray  # noqa: F401
        import xarray as xr
    except ImportError:
        print(_need("rioxarray/xarray"), file=sys.stderr)
        return False

    w, s, e, n = aoi_bbox()
    search = catalog.search(
        collections=["terraclimate"],
        bbox=[w, s, e, n],
        datetime=f"{start}/{end}",
    )
    items = list(search.items())
    if not items:
        print("  [terraclimate] no items found.")
        return False
    print(f"  [terraclimate] {len(items)} items found "
          f"for variables: {variables}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ok_any = False
    for var in variables:
        arrays = []
        for it in items:
            if var not in it.assets:
                continue
            href = it.assets[var].href
            da = (
                xr.open_dataarray(href, engine="rasterio")
                .squeeze(drop=True)
                .rio.clip_box(minx=w, miny=s, maxx=e, maxy=n, crs="EPSG:4326")
            )
            da = da.assign_coords(time=it.datetime).expand_dims("time")
            arrays.append(da)
        if not arrays:
            print(f"  [terraclimate] {var}: no assets — skipping.")
            continue
        stack = xr.concat(arrays, dim="time").sortby("time")
        out = OUT_DIR / f"terraclimate_{var}_{start}_{end}.tif"
        stack.rio.to_raster(out, compress="DEFLATE", tiled=True)
        print(f"  [terraclimate] {var} → {out} ({out.stat().st_size//1024} KB)")
        ok_any = True
    return ok_any


def main():
    ap = argparse.ArgumentParser(
        description="Climate data (CHIRPS + TerraClimate) for LQV AOI.",
    )
    ap.add_argument("--only", choices=["chirps", "terraclimate"],
                    help="Run only one source instead of both.")
    ap.add_argument("--start", default="2020-01-01")
    ap.add_argument("--end", default="2026-06-01")
    ap.add_argument("--vars", default=",".join(TERRACLIMATE_VARS_DEFAULT),
                    help="Comma-separated TerraClimate variables.")
    args = ap.parse_args()

    catalog = _open_catalog()
    if catalog is None:
        return 1

    todo = ["chirps", "terraclimate"]
    if args.only:
        todo = [args.only]
    tc_vars = [v.strip() for v in args.vars.split(",") if v.strip()]

    results: dict[str, bool] = {}
    if "chirps" in todo:
        results["chirps"] = fetch_chirps(catalog, args.start, args.end)
    if "terraclimate" in todo:
        results["terraclimate"] = fetch_terraclimate(
            catalog, args.start, args.end, tc_vars,
        )

    print("\nSummary:")
    for k, v in results.items():
        print(f"  {k:14s} {'OK' if v else 'FAILED'}")
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
