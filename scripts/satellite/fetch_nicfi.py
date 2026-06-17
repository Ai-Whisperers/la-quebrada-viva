#!/usr/bin/env python3
"""Planet NICFI basemap fetcher for La Quebrada Viva.

NICFI = Norway's International Climate & Forest Initiative. Planet
publishes ~5 m monthly + biannual basemaps for the tropical belt
under NICFI for non-commercial use; the LQV 62-ha parcel at
Escobar, Paraguarí sits inside coverage.

Why this script exists: even at 10 m, Sentinel-2 averages out the
canopy textures we care about (lapacho clusters, gallery forest
edges, roof outlines). NICFI's 5 m basemap is a step closer to
"recognisable from a drone photo" without paying for SkySat/WorldView.

Authentication:
  Set ``PLANET_API_KEY`` in env (sign up at https://www.planet.com/nicfi).
  No key → ``main()`` prints the signup URL and exits cleanly.

Tile-server endpoint:
  https://tiles.planet.com/basemaps/v1/planet-tiles/{mosaic}/gmap/{z}/{x}/{y}.png?api_key=...
  Mosaics are named like ``planet_medres_normalized_analytic_2026-04_mosaic``.

Usage:
    python -m scripts.satellite.fetch_nicfi --list-mosaics
    python -m scripts.satellite.fetch_nicfi --mosaic planet_medres_visual_2026-04_mosaic --zoom 15

Refs:
  - https://www.planet.com/nicfi/
  - https://developers.planet.com/docs/basemaps/
"""
from __future__ import annotations

import argparse
import math
import os
import sys
from pathlib import Path

from scripts.satellite._aoi import aoi_bbox

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = _PROJECT_ROOT / "docs" / "site_data" / "nicfi"

PLANET_BASEMAPS_API = "https://api.planet.com/basemaps/v1/mosaics"


def _api_key() -> str | None:
    return os.environ.get("PLANET_API_KEY")


def _need_key() -> int:
    print(
        "Missing PLANET_API_KEY env var.\n"
        "Sign up (free for non-commercial / tropical-forest use):\n"
        "  https://www.planet.com/nicfi/\n"
        "Then `export PLANET_API_KEY=…` and rerun.",
        file=sys.stderr,
    )
    return 1


def list_mosaics():
    key = _api_key()
    if not key:
        return _need_key()
    try:
        import requests
    except ImportError:
        print("Missing dep: requests. pip install requests", file=sys.stderr)
        return 1

    params: dict = {"name__contains": "planet_medres"}
    r = requests.get(PLANET_BASEMAPS_API, auth=(key, ""), params=params, timeout=60)
    if r.status_code == 401:
        print("Planet API: 401 unauthorized. Check PLANET_API_KEY.", file=sys.stderr)
        return 1
    r.raise_for_status()
    mosaics = r.json().get("mosaics", [])
    print(f"Found {len(mosaics)} NICFI mosaics. Most recent 20:")
    mosaics.sort(key=lambda m: m.get("last_acquired") or "", reverse=True)
    for m in mosaics[:20]:
        print(f"  {m.get('name', '?')}  ({m.get('last_acquired', '?')[:10]})")
    return 0


def _tile_xyz(lon: float, lat: float, zoom: int) -> tuple[int, int]:
    """Convert lon/lat → XYZ tile coords at the given zoom."""
    lat_rad = math.radians(lat)
    n = 2 ** zoom
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return x, y


def fetch_tiles(mosaic: str, zoom: int):
    if not _api_key():
        return _need_key()
    try:
        import requests
    except ImportError:
        print("Missing dep: requests. pip install requests", file=sys.stderr)
        return 1

    w, s, e, n = aoi_bbox()
    x_min, y_max = _tile_xyz(w, s, zoom)
    x_max, y_min = _tile_xyz(e, n, zoom)
    if x_max < x_min:
        x_min, x_max = x_max, x_min
    if y_max < y_min:
        y_min, y_max = y_max, y_min

    out_dir = OUT_DIR / mosaic / f"z{zoom}"
    out_dir.mkdir(parents=True, exist_ok=True)
    total = (x_max - x_min + 1) * (y_max - y_min + 1)
    print(f"[nicfi] mosaic={mosaic} zoom={zoom} → {total} tiles "
          f"(x: {x_min}..{x_max}, y: {y_min}..{y_max})")

    fetched = 0
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            url = (
                f"https://tiles.planet.com/basemaps/v1/planet-tiles/{mosaic}"
                f"/gmap/{zoom}/{x}/{y}.png?api_key={_api_key()}"
            )
            out = out_dir / f"{x}_{y}.png"
            if out.exists() and out.stat().st_size > 1024:
                continue
            r = requests.get(url, timeout=60)
            if r.status_code == 200:
                out.write_bytes(r.content)
                fetched += 1
            elif r.status_code == 404:
                print(f"  [skip] tile {x},{y} 404 (outside mosaic)")
            else:
                print(f"  [fail] tile {x},{y} HTTP {r.status_code}")
    print(f"[nicfi] {fetched} new tiles saved under {out_dir}")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="Planet NICFI basemap fetcher for the LQV AOI.",
    )
    ap.add_argument("--list-mosaics", action="store_true")
    ap.add_argument("--mosaic",
                    help="Mosaic name, e.g. planet_medres_visual_2026-04_mosaic")
    ap.add_argument("--zoom", type=int, default=15,
                    help="XYZ tile zoom level (15 ≈ 5 m/px at the equator).")
    args = ap.parse_args()

    if args.list_mosaics:
        return list_mosaics()
    if not args.mosaic:
        print("Pass --mosaic <name> or --list-mosaics. See --help.", file=sys.stderr)
        return 2
    return fetch_tiles(args.mosaic, args.zoom)


if __name__ == "__main__":
    sys.exit(main())
