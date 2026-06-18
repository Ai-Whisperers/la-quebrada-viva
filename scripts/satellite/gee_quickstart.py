#!/usr/bin/env python3
"""Google Earth Engine quickstart for La Quebrada Viva.

Why this script exists: GEE is the heaviest-lifting platform for
multi-year time series + server-side reductions over collections that
PC doesn't always carry comfortably (CHIRPS daily, Hansen Forest
Change global mosaic, MODIS Terra/Aqua daily LST, GEDI L4A). It
also runs cloud-side reducers (median / mean / count) so you don't
pay the bandwidth of downloading every scene.

This module produces two deliverables:

  1. Sentinel-2 NDVI median composite (`ndvi_<start>_<end>.tif`) with
     SCL cloud/shadow mask + N-pixel dilation buffer (gap #6).
  2. Multi-year NDVI p10/p50/p90 percentile stack
     (`ndvi_percentiles_<start>_<end>.tif`, gap #14) — gives the deck
     a "drought-floor / typical / peak-greenness" triad instead of a
     single composite that erases interannual variability.

Both land as 10 m GeoTIFFs under ``docs/site_data/gee/``.

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
    python -m scripts.satellite.gee_quickstart --download    # median NDVI GeoTIFF
    python -m scripts.satellite.gee_quickstart --percentiles --start 2020-01-01 --end 2026-06-01
    python -m scripts.satellite.gee_quickstart --percentiles --download

Refs:
  - https://developers.google.com/earth-engine/guides/python_install
  - https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

from scripts.satellite._aoi import aoi_bbox, aoi_polygon_geojson
from scripts.satellite._crs import to_canonical_inplace_path
from scripts.satellite._license import assert_compatible, classify
from scripts.satellite._meta import write_sidecar
from scripts.satellite._retry import skip_if_exists, with_retry

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = _PROJECT_ROOT / "docs" / "site_data" / "gee"

GEE_COLLECTION = "copernicus-s2-sr-harmonized"

# Copernicus Sentinel-2 L2A (HARMONIZED) is bundle-eligible under the ESA
# Legal Notice on the use of Copernicus Sentinel data — equivalent to
# CC-BY-4.0 attribution requirements. See LICENSE_BUNDLE.md §3.
GEE_LICENSE_ID = "CC-BY-4.0"
GEE_CITATION = (
    "Contains modified Copernicus Sentinel data, processed by ESA, "
    "accessed via Google Earth Engine collection "
    "'COPERNICUS/S2_SR_HARMONIZED'. CC-BY-4.0-equivalent per Copernicus "
    "Sentinel ESA Legal Notice."
)

# SCL dilation (gap #6): the Sen2Cor scene-classification layer is sharp at
# 20 m but tends to under-mask the *edges* of clouds and shadows. Dilating
# the invalid-pixel mask by N pixels of S2 native resolution (10 m) gives a
# ~20 m safety buffer that catches the soft transition pixels which would
# otherwise pollute the NDVI composite.
SCL_DILATION_PIXELS = 2

# Cloud-cover prefilter on the scene metadata BEFORE the per-pixel mask.
# 30% is the standard PC/element84 default; the SCL mask handles the rest.
SCENE_CLOUD_COVER_MAX = 30


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
    except Exception as exc:
        print(
            f"[gee] init failed: {type(exc).__name__}: {exc}\n"
            f"      Run `earthengine authenticate` or set "
            f"GOOGLE_APPLICATION_CREDENTIALS + EE_PROJECT.",
            file=sys.stderr,
        )
        return None
    return ee


def _mask_scl(ee, img):
    """Mask cloud/shadow/cirrus per SCL, then dilate the invalid mask.

    SCL class codes:
      Keep: vegetation(4), bare(5), water(6), unclassified(7), snow(11)
      Drop: saturated(1), shadow(3), cloud-med(8), cloud-high(9), cirrus(10)
    """
    scl = img.select("SCL")
    valid = scl.eq(4).Or(scl.eq(5)).Or(scl.eq(6)).Or(scl.eq(7)).Or(scl.eq(11))

    # Gap #6: dilate the *invalid* region (cloud/shadow), then re-invert.
    # focal_max on the invalid mask grows it by SCL_DILATION_PIXELS pixels
    # of the native 10 m resolution → ~20 m safety buffer.
    invalid = valid.Not()
    invalid_dilated = invalid.focal_max(
        radius=SCL_DILATION_PIXELS, units="pixels",
    )
    valid_dilated = invalid_dilated.Not()
    return img.updateMask(valid_dilated)


def _s2_collection(ee, start: str, end: str, aoi_geom):
    """Cloud-filtered, SCL-dilated Sentinel-2 SR HARMONIZED collection."""
    return (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(aoi_geom)
        .filterDate(start, end)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", SCENE_CLOUD_COVER_MAX))
        .map(lambda img: _mask_scl(ee, img))
    )


def build_ndvi_composite(ee, start: str, end: str):
    """Sentinel-2 SR HARMONIZED median NDVI over AOI, SCL-dilated."""
    aoi_geom = ee.Geometry(aoi_polygon_geojson())
    collection = _s2_collection(ee, start, end, aoi_geom)
    ndvi = collection.map(
        lambda img: img.normalizedDifference(["B8", "B4"]).rename("NDVI")
    ).median().clip(aoi_geom)
    return ndvi, aoi_geom


def build_ndvi_percentiles(
    ee, start: str, end: str, percentiles: tuple[int, ...] = (10, 50, 90),
):
    """Multi-year NDVI percentile stack (gap #14).

    Returns a multi-band image with bands ``NDVI_p10``, ``NDVI_p50``,
    ``NDVI_p90`` (or whatever percentiles are requested). The triad
    captures the drought floor, typical greenness, and peak greenness
    across the requested window — critical for a multi-year window
    spanning wet/dry interannual variability.
    """
    aoi_geom = ee.Geometry(aoi_polygon_geojson())
    collection = _s2_collection(ee, start, end, aoi_geom).map(
        lambda img: img.normalizedDifference(["B8", "B4"]).rename("NDVI"),
    )
    stack = collection.reduce(
        ee.Reducer.percentile(list(percentiles)),
    ).clip(aoi_geom)
    return stack, aoi_geom


@with_retry()
def _download_url_to(url: str, out: Path) -> None:
    """Stream a getDownloadURL response to ``out`` atomically via .tmp."""
    import requests
    tmp = out.with_suffix(out.suffix + ".tmp")
    with requests.get(url, stream=True, timeout=600) as r:
        r.raise_for_status()
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 64):
                f.write(chunk)
    tmp.replace(out)


def _download_geotiff(
    image, aoi_geom, out: Path, *, scale: int = 10,
    sidecar_extra: dict | None = None,
) -> bool:
    """getDownloadURL → atomic write → CRS normalize → sidecar.

    Idempotent: a cached output still re-runs CRS normalize and rewrites
    the sidecar so older partial outputs get upgraded on re-run.
    """
    # License gate before we touch the network.
    bundle_class = classify(GEE_LICENSE_ID)
    assert_compatible(GEE_LICENSE_ID)

    w, s, e, n = aoi_bbox()
    out.parent.mkdir(parents=True, exist_ok=True)

    if skip_if_exists(out):
        print(f"[gee] cached → {out} ({out.stat().st_size//1024} KB)")
    else:
        url = image.getDownloadURL({
            "scale": scale,
            "region": [[w, s], [e, s], [e, n], [w, n], [w, s]],
            "crs": "EPSG:4326",
            "format": "GEO_TIFF",
        })
        print(f"[gee] downloading {url[:80]}…")
        t0 = time.time()
        try:
            _download_url_to(url, out)
        except Exception as exc:
            print(f"[gee] download FAILED: {type(exc).__name__}: {exc}")
            return False
        print(f"[gee] saved {out} ({out.stat().st_size//1024} KB, "
              f"{time.time()-t0:.1f}s)")

    try:
        to_canonical_inplace_path(out)
    except Exception as exc:
        print(f"[gee] WARN CRS normalize skipped: {type(exc).__name__}: {exc}")

    base_extra = {
        "scale_m": scale,
        "scene_cloud_cover_max_pct": SCENE_CLOUD_COVER_MAX,
        "scl_dilation_pixels": SCL_DILATION_PIXELS,
        "bundle_eligibility": bundle_class,
        "aoi_bbox_wsen": [w, s, e, n],
    }
    if sidecar_extra:
        base_extra.update(sidecar_extra)
    write_sidecar(
        out,
        source="https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED",
        collection=GEE_COLLECTION,
        license_id=GEE_LICENSE_ID,
        citation=GEE_CITATION,
        fetcher="scripts.satellite.gee_quickstart",
        extra=base_extra,
    )
    return True


def _print_stats(ee, image, aoi_geom, label: str) -> None:
    stats = image.reduceRegion(
        reducer=ee.Reducer.minMax().combine(ee.Reducer.mean(), sharedInputs=True),
        geometry=aoi_geom, scale=10, maxPixels=1e9,
    ).getInfo()
    print(f"[gee] {label} stats over AOI:")
    for k, v in stats.items():
        print(f"      {k}: {v}")


def main():
    ap = argparse.ArgumentParser(
        description="GEE quickstart — Sentinel-2 NDVI over LQV AOI.",
    )
    ap.add_argument("--start", default="2025-01-01")
    ap.add_argument("--end", default="2026-06-01")
    ap.add_argument("--download", action="store_true",
                    help="Pull the GeoTIFF via getDownloadURL (small AOI only).")
    ap.add_argument("--percentiles", action="store_true",
                    help="Build the multi-year NDVI p10/p50/p90 stack instead "
                         "of (in addition to, with --download) the median.")
    ap.add_argument("--percentiles-list", default="10,50,90",
                    help="Comma-separated percentile values (default: 10,50,90).")
    args = ap.parse_args()

    ee = _init_ee()
    if ee is None:
        return 1

    rc = 0

    if args.percentiles:
        pct_values = tuple(int(p.strip()) for p in args.percentiles_list.split(",")
                           if p.strip())
        stack, aoi_geom = build_ndvi_percentiles(
            ee, args.start, args.end, percentiles=pct_values,
        )
        _print_stats(ee, stack, aoi_geom, f"NDVI percentiles {pct_values}")
        if args.download:
            out = OUT_DIR / f"ndvi_percentiles_{args.start}_{args.end}.tif"
            if not _download_geotiff(
                stack, aoi_geom, out,
                sidecar_extra={
                    "product": "ndvi_percentiles",
                    "percentiles": list(pct_values),
                    "datetime_range": f"{args.start}/{args.end}",
                },
            ):
                rc = 1
    else:
        ndvi, aoi_geom = build_ndvi_composite(ee, args.start, args.end)
        _print_stats(ee, ndvi, aoi_geom, f"NDVI median {args.start} → {args.end}")
        if args.download:
            out = OUT_DIR / f"ndvi_{args.start}_{args.end}.tif"
            if not _download_geotiff(
                ndvi, aoi_geom, out,
                sidecar_extra={
                    "product": "ndvi_median",
                    "datetime_range": f"{args.start}/{args.end}",
                },
            ):
                rc = 1

    return rc


if __name__ == "__main__":
    sys.exit(main())
