#!/usr/bin/env python3
"""Google Earth Engine quickstart for La Quebrada Viva.

Why this script exists: GEE is the heaviest-lifting platform for
multi-year time series + server-side reductions over collections that
PC doesn't always carry comfortably (CHIRPS daily, Hansen Forest
Change global mosaic, MODIS Terra/Aqua daily LST, GEDI L4A). It
also runs cloud-side reducers (median / mean / count) so you don't
pay the bandwidth of downloading every scene.

This module produces ONE deliverable per run: a Sentinel-2 NDVI
median composite for the AOI over a configurable window, with the
SCL cloud-mask applied. Output lands in
``docs/site_data/gee/ndvi_<start>_<end>.tif`` as a 10 m GeoTIFF.

Authentication — pick ONE:
  (a) Interactive (one-off, for Ivan locally):
      ``earthengine authenticate`` once, then ``python -m scripts.satellite.gee_quickstart``.
  (b) Service account (for CI / headless):
      Set ``GOOGLE_APPLICATION_CREDENTIALS`` to the JSON key file.
      Set ``EE_PROJECT`` to the GCP project ID with Earth Engine API enabled.

Decision (per "decide-and-document" autonomy): default to (a). The
escritura-T-10 use-case is exploratory analysis on Ivan's laptop, not
CI. CI gets a clear-message skip in ``main()`` if neither auth path
is configured.

Usage:
    python -m scripts.satellite.gee_quickstart --start 2025-01-01 --end 2026-06-01
    python -m scripts.satellite.gee_quickstart --download    # actually pulls the GeoTIFF

Refs:
  - https://developers.google.com/earth-engine/guides/python_install
  - https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from scripts.satellite._aoi import aoi_bbox, aoi_polygon_geojson

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = _PROJECT_ROOT / "docs" / "site_data" / "gee"


def _init_ee():
    try:
        import ee
    except ImportError:
        print(
            "Missing dep: 'earthengine-api'. Install with:\n"
            "  pip install earthengine-api\n"
            "Then run `earthengine authenticate` once.",
            file=sys.stderr,
        )
        return None

    sa_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    ee_project = os.environ.get("EE_PROJECT") or "earthengine-legacy"

    try:
        if sa_creds and Path(sa_creds).is_file():
            credentials = ee.ServiceAccountCredentials(
                email=None, key_file=sa_creds,
            )
            ee.Initialize(credentials, project=ee_project)
            print(f"[gee] auth: service account, project={ee_project}")
        else:
            ee.Initialize(project=ee_project)
            print(f"[gee] auth: interactive (cached), project={ee_project}")
    except Exception as e:
        print(
            f"[gee] init failed: {type(e).__name__}: {e}\n"
            f"      Run `earthengine authenticate` or set "
            f"GOOGLE_APPLICATION_CREDENTIALS + EE_PROJECT.",
            file=sys.stderr,
        )
        return None
    return ee


def build_ndvi_composite(ee, start: str, end: str):
    """Sentinel-2 SR HARMONIZED median NDVI over AOI, SCL-masked."""
    aoi_geom = ee.Geometry(aoi_polygon_geojson())

    def _mask_scl(img):
        scl = img.select("SCL")
        # Keep: vegetation(4), bare(5), water(6), unclassified(7), snow(11)
        # Drop: saturated(1), shadow(3), cloud-med(8), cloud-high(9), cirrus(10)
        valid = scl.eq(4).Or(scl.eq(5)).Or(scl.eq(6)).Or(scl.eq(7)).Or(scl.eq(11))
        return img.updateMask(valid)

    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(aoi_geom)
        .filterDate(start, end)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 30))
        .map(_mask_scl)
    )

    ndvi = collection.map(
        lambda img: img.normalizedDifference(["B8", "B4"]).rename("NDVI")
    ).median().clip(aoi_geom)

    return ndvi, aoi_geom


def main():
    ap = argparse.ArgumentParser(
        description="GEE quickstart — Sentinel-2 NDVI median over LQV AOI.",
    )
    ap.add_argument("--start", default="2025-01-01")
    ap.add_argument("--end", default="2026-06-01")
    ap.add_argument("--download", action="store_true",
                    help="Pull the GeoTIFF via getDownloadURL (small AOI only).")
    args = ap.parse_args()

    ee = _init_ee()
    if ee is None:
        return 1

    ndvi, aoi_geom = build_ndvi_composite(ee, args.start, args.end)
    stats = ndvi.reduceRegion(
        reducer=ee.Reducer.minMax().combine(ee.Reducer.mean(), sharedInputs=True),
        geometry=aoi_geom, scale=10, maxPixels=1e9,
    ).getInfo()
    print(f"[gee] NDVI stats over AOI ({args.start} → {args.end}):")
    for k, v in stats.items():
        print(f"      {k}: {v}")

    if args.download:
        w, s, e, n = aoi_bbox()
        url = ndvi.getDownloadURL({
            "scale": 10,
            "region": [[w, s], [e, s], [e, n], [w, n], [w, s]],
            "crs": "EPSG:4326",
            "format": "GEO_TIFF",
        })
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        out = OUT_DIR / f"ndvi_{args.start}_{args.end}.tif"
        try:
            import requests
        except ImportError:
            print(f"[gee] requests missing; download URL = {url}", file=sys.stderr)
            return 1
        print(f"[gee] downloading {url[:80]}…")
        with requests.get(url, stream=True, timeout=600) as r:
            r.raise_for_status()
            with open(out, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 64):
                    f.write(chunk)
        print(f"[gee] saved {out} ({out.stat().st_size//1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
