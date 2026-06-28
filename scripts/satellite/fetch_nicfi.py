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
import time
from pathlib import Path

from scripts.satellite._aoi import aoi_bbox
from scripts.satellite._license import assert_compatible, classify
from scripts.satellite._meta import write_sidecar
from scripts.satellite._retry import MIN_VALID_BYTES, with_retry

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = _PROJECT_ROOT / "docs" / "site_data" / "nicfi"

PLANET_BASEMAPS_API = "https://api.planet.com/basemaps/v1/mosaics"

NICFI_COLLECTION = "planet-nicfi-basemaps"

# Planet NICFI basemaps — non-commercial use only per the NICFI Participant
# License Agreement. classify() returns 'deck_only' so the bundle manifest
# excludes these tiles; the deck includes them with the required credit.
NICFI_LICENSE_ID = "Planet-NICFI-Non-Commercial"
NICFI_CITATION = (
    "Planet Labs Inc. NICFI Tropical Forest Monitoring Basemaps. "
    "© Planet Labs Inc., released under the NICFI Participant License "
    "Agreement (non-commercial use). https://www.planet.com/nicfi/."
)


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


@with_retry()
def _download_tile(url: str, out: Path) -> str:
    """Fetch one PNG tile to ``out`` atomically.

    Returns "ok" on 200, "missing" on 404 (outside mosaic — not retried),
    or raises on any other HTTP / transport error so @with_retry can back off.
    HTTP 429 is logged with the server's Retry-After header before raising.
    """
    import requests
    r = requests.get(url, timeout=60)
    if r.status_code == 200:
        tmp = out.with_suffix(out.suffix + ".tmp")
        tmp.write_bytes(r.content)
        tmp.replace(out)
        return "ok"
    if r.status_code == 404:
        return "missing"
    if r.status_code == 429:
        retry_after = r.headers.get("Retry-After", "?")
        print(f"  [nicfi] HTTP 429 rate-limited (Retry-After={retry_after}s); "
              "letting @with_retry back off")
    r.raise_for_status()
    return "ok"  # unreachable


def fetch_tiles(mosaic: str, zoom: int):
    if not _api_key():
        return _need_key()
    try:
        import requests  # noqa: F401  (probe — _download_tile imports for real)
    except ImportError:
        print("Missing dep: requests. pip install requests", file=sys.stderr)
        return 1

    # License gate — NICFI is non-commercial; classify() returns "deck_only"
    # without raising. Captured for the sidecar so the bundle manifest can
    # honor the deck-only flag.
    bundle_class = classify(NICFI_LICENSE_ID)
    assert_compatible(NICFI_LICENSE_ID)

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
    skipped_cached = 0
    skipped_missing = 0
    failed = 0
    t0 = time.time()

    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            out = out_dir / f"{x}_{y}.png"
            if out.exists() and out.stat().st_size >= MIN_VALID_BYTES:
                skipped_cached += 1
                continue
            url = (
                f"https://tiles.planet.com/basemaps/v1/planet-tiles/{mosaic}"
                f"/gmap/{zoom}/{x}/{y}.png?api_key={_api_key()}"
            )
            try:
                status = _download_tile(url, out)
            except Exception as exc:
                print(f"  [fail] tile {x},{y} {type(exc).__name__}: {exc}")
                failed += 1
                continue
            if status == "ok":
                fetched += 1
            elif status == "missing":
                skipped_missing += 1

    elapsed = time.time() - t0
    print(
        f"[nicfi] {fetched} new tiles saved under {out_dir} "
        f"(cached={skipped_cached}, 404={skipped_missing}, failed={failed}, "
        f"{elapsed:.1f}s)"
    )

    # One per-mosaic sidecar at the mosaic root — per-tile sidecars would
    # explode the manifest (hundreds of tiles per fetch).
    sidecar_target = out_dir / "_nicfi.meta.json"
    sidecar_target.parent.mkdir(parents=True, exist_ok=True)
    if not sidecar_target.exists():
        sidecar_target.touch()
    write_sidecar(
        sidecar_target,
        source=f"{PLANET_BASEMAPS_API}?name__contains={mosaic}",
        collection=NICFI_COLLECTION,
        license_id=NICFI_LICENSE_ID,
        citation=NICFI_CITATION,
        fetcher="scripts.satellite.fetch_nicfi",
        extra={
            "mosaic": mosaic,
            "zoom": zoom,
            "tile_x_range": [x_min, x_max],
            "tile_y_range": [y_min, y_max],
            "tile_count_expected": total,
            "tile_count_fetched_this_run": fetched,
            "tile_count_cached": skipped_cached,
            "tile_count_404": skipped_missing,
            "tile_count_failed": failed,
            "bundle_eligibility": bundle_class,
            "tile_srs": "EPSG:3857",
        },
    )
    return 0 if failed == 0 else 1


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
