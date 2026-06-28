#!/usr/bin/env python3
"""Microsoft Planetary Computer STAC quickstart for La Quebrada Viva.

Why this script exists: element84's earth-search catalog (used by
``fetch_sentinel2.py``) is fine for a one-off Sentinel-2 grab, but
Planetary Computer (PC) carries far more collections under a single
auth-free STAC API:

  - sentinel-2-l2a            (10/20 m, 5-day revisit)
  - sentinel-1-rtc            (10 m C-band SAR, all-weather, day+night)
  - sentinel-1-grd            (raw SAR, useful for backscatter ts)
  - landsat-c2-l2             (30 m, since 1984 — historical baseline)
  - hls2-l30 / hls2-s30       (harmonized Landsat+Sentinel-2, 30 m, 2-3 day)
  - io-lulc-9-class           (Impact Observatory landcover, 2017-2023)
  - esa-worldcover            (10 m global landcover, 2020/2021)
  - jrc-gsw                   (JRC global surface water occurrence)
  - cop-dem-glo-30            (Copernicus GLO-30 DEM — already have it)
  - chirps                    (rainfall, 0.05° daily, 1981-present)
  - terraclimate              (climate water balance, monthly, 1958-)
  - modis-*                   (LST, NDVI, etc — 250-1000 m)

PC asset HREFs come back **unsigned** — you can list/search anon, but the
download URL needs to be signed via ``planetary_computer.sign()``. The
dependency ``planetary-computer`` handles this; ``pystac-client`` handles
the search; ``stackstac`` lazy-loads bands as xarray for analysis.

Usage:
    python -m scripts.satellite.pc_stac_quickstart --list-collections
    python -m scripts.satellite.pc_stac_quickstart --collection sentinel-2-l2a --days 90
    python -m scripts.satellite.pc_stac_quickstart --collection sentinel-1-rtc --days 365 --max 10

Outputs go to ``docs/site_data/pc_search/<collection>/index.json``
(STAC search results, not downloaded scenes — keep the repo small).

Refs:
  - https://planetarycomputer.microsoft.com/docs/concepts/stac/
  - https://github.com/microsoft/PlanetaryComputer
  - https://stackstac.readthedocs.io/
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

from scripts.satellite._aoi import aoi_bbox

PC_STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"

DEFAULT_COLLECTIONS = [
    "sentinel-2-l2a",
    "sentinel-1-rtc",
    "esa-worldcover",
    "jrc-gsw",
    "landsat-c2-l2",
    "hls2-s30",
    "chirps",
]

# Repo root = three levels up from this file.
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = _PROJECT_ROOT / "docs" / "site_data" / "pc_search"


def _need(pkg: str) -> str:
    return (
        f"Missing dep: {pkg!r}. Install with:\n"
        f"  pip install planetary-computer pystac-client stackstac rioxarray\n"
        f"Auth-free for search; downloads need pc.sign(). See module docstring."
    )


def list_collections():
    try:
        from pystac_client import Client
    except ImportError:
        print(_need("pystac-client"))
        return 1
    catalog = Client.open(PC_STAC_URL)
    cols = sorted(c.id for c in catalog.get_collections())
    print(f"Planetary Computer carries {len(cols)} collections.")
    print(f"Collections matching the LQV use-case ({len(DEFAULT_COLLECTIONS)}):")
    for c in DEFAULT_COLLECTIONS:
        present = " ✓" if c in cols else " ✗ (not found)"
        print(f"  {c:30s}{present}")
    return 0


def _print_cached_items(path: Path) -> int:
    """Print the same summary `search()` would, from a cached index.json.

    Lets you re-inspect a previously-fetched STAC search without burning
    the round-trip — handy when the network's flaky or you want a diff
    against an earlier run. Reads the file `search()` writes; format is
    fixed by the literal dict assembled below.
    """
    if not path.exists():
        print(f"items-file not found: {path}", file=sys.stderr)
        return 1
    try:
        index = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"failed to read {path}: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    items = index.get("items", [])
    print(f"  {len(items)} items ← {path} (cached)")
    print(f"  collection: {index.get('collection')}")
    print(f"  bbox: {index.get('bbox')}")
    print(f"  datetime_range: {index.get('datetime_range')}")
    if items:
        first = items[0]
        print(f"  example: {first.get('id')}")
        print(f"           assets: {first.get('assets', [])[:8]}")
    return 0


def search(collection: str, days: int, max_items: int, cloud_pct: float):
    try:
        import planetary_computer as pc
        from pystac_client import Client
    except ImportError as e:
        print(_need(e.name or "planetary-computer/pystac-client"))
        return 1

    w, s, e_lon, n = aoi_bbox()
    end = datetime.now(UTC)
    start = end - timedelta(days=days)

    catalog = Client.open(PC_STAC_URL, modifier=pc.sign_inplace)
    query: dict = {}
    # Optical collections support eo:cloud_cover; SAR / climate don't.
    if collection in ("sentinel-2-l2a", "landsat-c2-l2", "hls2-s30", "hls2-l30"):
        query = {"eo:cloud_cover": {"lt": cloud_pct}}

    search = catalog.search(
        collections=[collection],
        bbox=[w, s, e_lon, n],
        datetime=f"{start.isoformat()}/{end.isoformat()}",
        query=query or None,
        max_items=max_items,
    )
    items = list(search.items())
    items.sort(
        key=lambda it: it.properties.get("eo:cloud_cover", -1),
        reverse=False,
    )
    out_dir = OUT_DIR / collection
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "index.json"
    index = {
        "collection": collection,
        "bbox": [w, s, e_lon, n],
        "datetime_range": f"{start.isoformat()}/{end.isoformat()}",
        "found": len(items),
        "items": [
            {
                "id": it.id,
                "datetime": it.properties.get("datetime"),
                "cloud_cover": it.properties.get("eo:cloud_cover"),
                "assets": sorted(it.assets.keys()),
                "self_href": it.self_href,
            }
            for it in items
        ],
    }
    out.write_text(json.dumps(index, indent=2, default=str))
    print(f"  {len(items)} items → {out}")
    if items:
        print(f"  example: {items[0].id}")
        print(f"           assets: {sorted(items[0].assets.keys())[:8]}")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="Microsoft Planetary Computer STAC quickstart for La Quebrada Viva."
    )
    ap.add_argument("--list-collections", action="store_true",
                    help="Probe PC for the LQV-relevant collections and exit.")
    ap.add_argument("--collection", default="sentinel-2-l2a")
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--max", type=int, default=20)
    ap.add_argument("--cloud", type=float, default=20.0,
                    help="Max cloud cover %% (optical collections only).")
    ap.add_argument("--items-file", type=Path, default=None,
                    help="Load a pre-fetched index.json instead of hitting the network.")
    args = ap.parse_args()

    if args.list_collections:
        return list_collections()
    if args.items_file is not None:
        return _print_cached_items(args.items_file)
    return search(args.collection, args.days, args.max, args.cloud)


if __name__ == "__main__":
    sys.exit(main())
