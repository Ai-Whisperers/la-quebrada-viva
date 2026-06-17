#!/usr/bin/env python3
"""Landcover + surface-water + forest-change fetcher for La Quebrada Viva.

Pulls three thematic rasters via Microsoft Planetary Computer STAC,
clipped to the AOI, written under ``docs/site_data/landcover/``:

  1. ESA WorldCover 10 m (2020 + 2021) — 11-class global landcover.
  2. JRC Global Surface Water — water occurrence / change (1984-).
  3. Hansen Global Forest Change — tree-cover loss year (2000-).

Why this script exists: the deck needs an objective "what does the
land look like today" + "what changed in the last 20 years" answer
without us hand-drawing it. WorldCover gives the snapshot; Hansen
gives the loss map; JRC GSW flags wet zones we'd otherwise miss.

Auth: PC STAC is auth-free; downloads use signed asset HREFs via
``planetary_computer.sign_inplace``.

Usage:
    python -m scripts.satellite.fetch_landcover
    python -m scripts.satellite.fetch_landcover --only worldcover
    python -m scripts.satellite.fetch_landcover --only jrc-gsw
    python -m scripts.satellite.fetch_landcover --only hansen

Outputs:
  docs/site_data/landcover/worldcover_<year>.tif
  docs/site_data/landcover/jrc_gsw_occurrence.tif
  docs/site_data/landcover/hansen_lossyear.tif
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts.satellite._aoi import aoi_bbox

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = _PROJECT_ROOT / "docs" / "site_data" / "landcover"

PC_STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"


def _need(pkg: str) -> str:
    return (
        f"Missing dep: {pkg!r}.\n"
        f"  pip install planetary-computer pystac-client rioxarray rasterio\n"
    )


def _open_catalog():
    try:
        import planetary_computer as pc
        from pystac_client import Client
    except ImportError as e:
        print(_need(e.name or "planetary-computer/pystac-client"), file=sys.stderr)
        return None
    return Client.open(PC_STAC_URL, modifier=pc.sign_inplace)


def _clip_and_save(href: str, out: Path, label: str):
    """Open a remote COG, clip to AOI, write GeoTIFF."""
    try:
        import rioxarray
    except ImportError:
        print(_need("rioxarray"), file=sys.stderr)
        return False

    w, s, e, n = aoi_bbox()
    print(f"  [{label}] opening {href[:80]}…")
    da = rioxarray.open_rasterio(href, masked=True, chunks={"x": 1024, "y": 1024})
    # Reproject AOI bbox to raster's CRS if not EPSG:4326.
    try:
        clipped = da.rio.clip_box(minx=w, miny=s, maxx=e, maxy=n, crs="EPSG:4326")
    except Exception as exc:
        print(f"  [{label}] clip failed: {type(exc).__name__}: {exc}")
        return False
    out.parent.mkdir(parents=True, exist_ok=True)
    clipped.rio.to_raster(out, compress="DEFLATE", tiled=True)
    print(f"  [{label}] → {out} ({out.stat().st_size//1024} KB)")
    return True


def fetch_worldcover(catalog):
    w, s, e, n = aoi_bbox()
    search = catalog.search(
        collections=["esa-worldcover"],
        bbox=[w, s, e, n],
    )
    items = list(search.items())
    if not items:
        print("  [worldcover] no items found.")
        return False
    ok = False
    for item in items:
        year = item.properties.get("start_datetime", "?")[:4]
        if "map" not in item.assets:
            continue
        out = OUT_DIR / f"worldcover_{year}.tif"
        if _clip_and_save(item.assets["map"].href, out, f"worldcover {year}"):
            ok = True
    return ok


def fetch_jrc_gsw(catalog):
    w, s, e, n = aoi_bbox()
    search = catalog.search(
        collections=["jrc-gsw"],
        bbox=[w, s, e, n],
    )
    items = list(search.items())
    if not items:
        print("  [jrc-gsw] no items found.")
        return False
    item = items[0]
    asset_key = "occurrence" if "occurrence" in item.assets else next(iter(item.assets))
    out = OUT_DIR / "jrc_gsw_occurrence.tif"
    return _clip_and_save(item.assets[asset_key].href, out, "jrc-gsw")


def fetch_hansen(_catalog):
    # Hansen GFC isn't on PC under a single canonical id at time of writing.
    # Fallback: pull lossyear COG straight from the public URL pattern.
    # Hansen GFC v1.11 (latest, 2024 release): tile naming is by 10° lat/lon corner.
    # Our AOI (~25.6°S, 57.0°W) → tile 20S_060W.
    lossyear_url = (
        "https://storage.googleapis.com/earthenginepartners-hansen/"
        "GFC-2023-v1.11/Hansen_GFC-2023-v1.11_lossyear_20S_060W.tif"
    )
    out = OUT_DIR / "hansen_lossyear.tif"
    return _clip_and_save(lossyear_url, out, "hansen")


def main():
    ap = argparse.ArgumentParser(
        description="Landcover + surface water + forest change for LQV AOI.",
    )
    ap.add_argument("--only", choices=["worldcover", "jrc-gsw", "hansen"],
                    help="Run only one source instead of all three.")
    args = ap.parse_args()

    catalog = _open_catalog()
    if catalog is None:
        return 1

    todo = ["worldcover", "jrc-gsw", "hansen"]
    if args.only:
        todo = [args.only]

    results: dict[str, bool] = {}
    if "worldcover" in todo:
        results["worldcover"] = fetch_worldcover(catalog)
    if "jrc-gsw" in todo:
        results["jrc-gsw"] = fetch_jrc_gsw(catalog)
    if "hansen" in todo:
        results["hansen"] = fetch_hansen(catalog)

    print("\nSummary:")
    for k, v in results.items():
        print(f"  {k:12s} {'OK' if v else 'FAILED'}")
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
