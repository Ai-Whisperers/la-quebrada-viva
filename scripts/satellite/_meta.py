"""Metadata sidecar writer for satellite outputs.

Every raster / vector / tile written by ``scripts/satellite/*`` gets a
``<output>.meta.json`` sidecar with timestamp, source asset HREF,
fetcher git SHA, SHA-256 of the file, license, citation, and the
license-gate classification ('bundle' / 'deck_only' / 'unknown').

The bundle manifest (``scripts/bundle_data_manifest.py``) walks all
sidecars at distribution time and uses ``classification`` to decide
which files go into the USB / Drive bundle.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from scripts.satellite._license import assert_compatible


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _git_sha() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True,
            cwd=Path(__file__).resolve().parents[2],
            timeout=5,
        )
        return out.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        return "unknown"


def write_sidecar(
    output_path: Path | str,
    *,
    source: str,
    collection: str,
    license_id: str,
    citation: str,
    fetcher: str,
    extra: dict[str, Any] | None = None,
) -> Path:
    """Write ``<output_path>.meta.json`` next to the produced file.

    Args:
        output_path: the file just written (raster, GeoJSON, tile, ...).
        source: canonical asset HREF or upstream URL.
        collection: STAC collection ID (or 'hansen-gfc-v1.11', 'mapbiomas-py-c2', ...).
        license_id: SPDX-style ID (CC0-1.0, CC-BY-4.0, CC-BY-NC-4.0, ...).
        citation: human-readable citation line for the deck.
        fetcher: module path of the calling script (e.g. 'scripts.satellite.fetch_landcover').
        extra: optional dict merged into the sidecar (item ID, band names, etc.).

    Returns:
        Path to the written sidecar.

    Raises:
        LicenseBlocked: if license_id is on the BLOCKED list.
    """
    output_path = Path(output_path)
    classification = assert_compatible(license_id)
    sidecar_path = output_path.with_suffix(output_path.suffix + ".meta.json")

    payload: dict[str, Any] = {
        "schema_version": 1,
        "output": output_path.name,
        "timestamp_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "source": source,
        "collection": collection,
        "license": license_id,
        "license_classification": classification,
        "citation": citation,
        "fetcher": fetcher,
        "git_sha": _git_sha(),
        "sha256": _sha256(output_path) if output_path.exists() else None,
        "size_bytes": output_path.stat().st_size if output_path.exists() else None,
        "aoi_geojson": "docs/site_data/aoi_62ha.geojson",
        "parcel_polygon_pending": _parcel_polygon_pending(),
    }
    if extra:
        payload.update(extra)

    sidecar_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return sidecar_path


def _parcel_polygon_pending() -> bool:
    """True if the cadastro padron polygons haven't landed yet."""
    cadastro = Path(__file__).resolve().parents[2] / "docs" / "site_data" / "cadastro" / "padrones.geojson"
    return not cadastro.exists() or os.environ.get("LQV_FORCE_BBOX_AOI") == "1"
