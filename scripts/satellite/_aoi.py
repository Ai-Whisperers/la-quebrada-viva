"""Canonical AOI loader for all scripts/satellite/* modules.

Reads ``docs/site_data/aoi_62ha.geojson`` and returns the bbox as a
``(west, south, east, north)`` tuple — the order STAC search bodies and
most raster libraries expect. Centralising this means a one-line change
when the real parcel polygon arrives with Anexo I post-escritura.
"""
from __future__ import annotations

import json
from pathlib import Path

# Repo root = three levels up from this file (scripts/satellite/_aoi.py).
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
AOI_GEOJSON_PATH = _PROJECT_ROOT / "docs" / "site_data" / "aoi_62ha.geojson"

# Last-ditch fallback if the GeoJSON is missing/corrupt — matches the
# constant the repo carried for months in scripts/fetch_sentinel2.py and
# scripts/test_stac.py, so downstream output stays consistent.
FALLBACK_BBOX = (-57.045, -25.645, -57.015, -25.615)


def aoi_bbox() -> tuple[float, float, float, float]:
    """Return AOI as (west, south, east, north)."""
    try:
        with open(AOI_GEOJSON_PATH, encoding="utf-8") as f:
            doc = json.load(f)
        b = doc["metadata"]["bbox"]
        bbox = (float(b["west"]), float(b["south"]), float(b["east"]), float(b["north"]))
        # Sanity-bound: AOI must sit inside Paraguay's national bounds.
        if not (-63.0 <= bbox[0] <= -54.0 and -28.0 <= bbox[1] <= -19.0):
            raise ValueError(f"AOI bbox {bbox} falls outside Paraguay")
        return bbox
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as e:
        import sys
        print(
            f"[scripts.satellite._aoi] WARN failed to read {AOI_GEOJSON_PATH}: "
            f"{type(e).__name__}: {e}; using fallback bbox {FALLBACK_BBOX}",
            file=sys.stderr,
        )
        return FALLBACK_BBOX


def aoi_polygon_geojson() -> dict:
    """Return the AOI Polygon geometry (GeoJSON dict)."""
    with open(AOI_GEOJSON_PATH, encoding="utf-8") as f:
        doc = json.load(f)
    return doc["features"][0]["geometry"]


def aoi_centroid() -> tuple[float, float]:
    """Return (lon, lat) of the AOI centroid."""
    w, s, e, n = aoi_bbox()
    return ((w + e) / 2.0, (s + n) / 2.0)
