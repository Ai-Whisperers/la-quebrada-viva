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
CADASTRO_GEOJSON_PATH = _PROJECT_ROOT / "docs" / "site_data" / "cadastro" / "padrones.geojson"

# Last-ditch fallback if the GeoJSON is missing/corrupt — matches the
# constant the repo carried for months in scripts/fetch_sentinel2.py and
# scripts/test_stac.py, so downstream output stays consistent.
FALLBACK_BBOX = (-57.045, -25.645, -57.015, -25.615)

PADRON_IDS = ("838", "1827", "840", "1096", "629", "454")


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


def cadastro_available() -> bool:
    """True if the user-supplied cadastro padron polygons are in place."""
    return CADASTRO_GEOJSON_PATH.exists()


def parcel_polygon_geojson() -> dict:
    """Return the true parcel boundary as a GeoJSON geometry.

    Resolution order:
      1. Union of features in ``docs/site_data/cadastro/padrones.geojson``
         (user-supplied via USER_ACTIONS_satellite.md §0.1).
      2. Fallback: rectangular AOI polygon from ``aoi_62ha.geojson`` —
         the same bbox the repo has shipped for months. Every metadata
         sidecar flags ``parcel_polygon_pending: true`` until #1 lands.

    The fallback is a real polygon (rectangle), NOT just a bbox tuple — so
    every fetcher can clip against geometry uniformly and switch to the
    real boundary by dropping a file at the cadastro path with zero code
    changes.
    """
    if cadastro_available():
        try:
            with open(CADASTRO_GEOJSON_PATH, encoding="utf-8") as f:
                doc = json.load(f)
            features = doc.get("features", [])
            if not features:
                raise ValueError("padrones.geojson has no features")
            geoms = [feat["geometry"] for feat in features if feat.get("geometry")]
            if len(geoms) == 1:
                return geoms[0]
            return {"type": "GeometryCollection", "geometries": geoms}
        except (OSError, KeyError, ValueError, json.JSONDecodeError) as e:
            import sys
            print(
                f"[scripts.satellite._aoi] WARN failed to read {CADASTRO_GEOJSON_PATH}: "
                f"{type(e).__name__}: {e}; falling back to rectangular AOI",
                file=sys.stderr,
            )
    return aoi_polygon_geojson()


def parcel_polygon_pending() -> bool:
    """Mirror of _meta._parcel_polygon_pending() exposed for fetchers."""
    import os
    return not cadastro_available() or os.environ.get("LQV_FORCE_BBOX_AOI") == "1"


def _geoms_from_geojson(geom: dict) -> list[dict]:
    """Flatten a GeometryCollection into a list rio.clip can consume."""
    if geom.get("type") == "GeometryCollection":
        return list(geom.get("geometries", []))
    return [geom]


def clip_to_parcel(da, *, crs: str = "EPSG:4326"):
    """Clip a rioxarray DataArray to the true parcel polygon.

    Falls back to the rectangular AOI when cadastro is missing (which is
    the current state until Anexo I post-escritura), so callers don't
    need a code change once polygons land — just drop the cadastro file.

    ``all_touched=True`` keeps boundary pixels — important at 10 m/30 m
    resolutions where a half-pixel slice can drop a whole stream bank.
    """
    geom = parcel_polygon_geojson()
    return da.rio.clip(_geoms_from_geojson(geom), crs, drop=True, all_touched=True)
