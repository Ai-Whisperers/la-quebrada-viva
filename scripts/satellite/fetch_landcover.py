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

from scripts.satellite._aoi import aoi_bbox, clip_to_parcel
from scripts.satellite._crs import to_canonical_inplace_path
from scripts.satellite._license import assert_compatible
from scripts.satellite._meta import write_sidecar
from scripts.satellite._retry import skip_if_exists, with_retry

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = _PROJECT_ROOT / "docs" / "site_data" / "landcover"

PC_STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"

WORLDCOVER_COLLECTION = "esa-worldcover"
JRC_GSW_COLLECTION = "jrc-gsw"
HANSEN_COLLECTION = "hansen-gfc-v1.11"

# ESA WorldCover — CC-BY-4.0 per ESA WorldCover product license.
WORLDCOVER_LICENSE_ID = "CC-BY-4.0"
WORLDCOVER_CITATION = (
    "Zanaga, D. et al. (2022) ESA WorldCover 10 m 2021 v200. "
    "doi:10.5281/zenodo.7254221. CC-BY-4.0; accessed via Microsoft "
    "Planetary Computer STAC collection 'esa-worldcover'."
)

# JRC Global Surface Water — CC-BY-4.0 per JRC reuse policy.
JRC_GSW_LICENSE_ID = "CC-BY-4.0"
JRC_GSW_CITATION = (
    "Pekel, J-F., Cottam, A., Gorelick, N., Belward, A.S. (2016) "
    "High-resolution mapping of global surface water and its long-term "
    "changes. Nature 540, 418-422. CC-BY-4.0; accessed via Microsoft "
    "Planetary Computer STAC collection 'jrc-gsw'."
)

# Hansen Global Forest Change v1.11 — CC-BY-4.0 per GLAD/UMD terms.
HANSEN_LICENSE_ID = "CC-BY-4.0"
HANSEN_CITATION = (
    "Hansen, M.C. et al. (2013) High-Resolution Global Maps of 21st-Century "
    "Forest Cover Change. Science 342:850-853. Data v1.11 (2023 release) "
    "via earthenginepartners-hansen public bucket. CC-BY-4.0."
)


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


@with_retry()
def _download_clipped(href: str, out: Path, label: str) -> bool:
    """Clip remote COG to AOI bbox and atomically write GeoTIFF."""
    try:
        import rioxarray
    except ImportError:
        print(_need("rioxarray"), file=sys.stderr)
        return False

    print(f"  [{label}] opening {href[:80]}…")
    da = rioxarray.open_rasterio(href, masked=True, chunks={"x": 1024, "y": 1024})
    try:
        clipped = clip_to_parcel(da)
    except Exception as exc:
        print(f"  [{label}] clip failed: {type(exc).__name__}: {exc}")
        return False
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    clipped.rio.to_raster(tmp, compress="DEFLATE", tiled=True)
    tmp.replace(out)
    print(f"  [{label}] → {out} ({out.stat().st_size//1024} KB)")
    return True


def _clip_and_save(
    href: str,
    out: Path,
    label: str,
    *,
    license_id: str,
    citation: str,
    collection: str,
    extra: dict | None = None,
) -> bool:
    """Open a remote COG, clip to AOI, write GeoTIFF + sidecar.

    Steps: license gate → cached-skip → atomic download → CRS normalize
    → write sidecar. CRS normalize and sidecar are idempotent so re-runs
    upgrade older partial outputs.
    """
    assert_compatible(license_id)

    if skip_if_exists(out):
        print(f"  [{label}] cached → {out} ({out.stat().st_size//1024} KB)")
    else:
        if not _download_clipped(href, out, label):
            return False

    try:
        to_canonical_inplace_path(out)
    except Exception as exc:
        print(f"  [{label}] WARN CRS normalize skipped: {type(exc).__name__}: {exc}")

    sidecar_extra = {"source_href": href}
    if extra:
        sidecar_extra.update(extra)
    write_sidecar(
        out,
        source=href,
        collection=collection,
        license_id=license_id,
        citation=citation,
        fetcher="scripts.satellite.fetch_landcover",
        extra=sidecar_extra,
    )
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
        if _clip_and_save(
            item.assets["map"].href,
            out,
            f"worldcover {year}",
            license_id=WORLDCOVER_LICENSE_ID,
            citation=WORLDCOVER_CITATION,
            collection=WORLDCOVER_COLLECTION,
            extra={"year": year, "item_id": item.id},
        ):
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
    return _clip_and_save(
        item.assets[asset_key].href,
        out,
        "jrc-gsw",
        license_id=JRC_GSW_LICENSE_ID,
        citation=JRC_GSW_CITATION,
        collection=JRC_GSW_COLLECTION,
        extra={"asset_key": asset_key, "item_id": item.id},
    )


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
    return _clip_and_save(
        lossyear_url,
        out,
        "hansen",
        license_id=HANSEN_LICENSE_ID,
        citation=HANSEN_CITATION,
        collection=HANSEN_COLLECTION,
        extra={"tile": "20S_060W", "version": "GFC-2023-v1.11"},
    )


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
