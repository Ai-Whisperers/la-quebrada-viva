"""Shared parcel geometry, output paths, and HTTP retry for site-data ingests.

Single source of truth for the 62-ha bbox and parcel-center point so each
module agrees on what "the property" means.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
SITE_DATA_DIR = REPO_ROOT / "docs" / "site_data"
HEIGHTMAP_SIDECAR = REPO_ROOT / "assets" / "terrain" / "escobar_height.json"


@dataclass(frozen=True)
class Bbox:
    """WGS84 bbox. Convention: left=west=min lon, bottom=south=min lat."""
    left: float
    bottom: float
    right: float
    top: float

    @property
    def center(self) -> tuple[float, float]:
        return ((self.left + self.right) / 2.0, (self.bottom + self.top) / 2.0)

    @property
    def corners(self) -> list[tuple[float, float]]:
        return [
            (self.left, self.bottom), (self.right, self.bottom),
            (self.right, self.top), (self.left, self.top),
        ]

    def as_geojson_polygon(self) -> dict[str, Any]:
        return {
            "type": "Polygon",
            "coordinates": [[
                [self.left, self.bottom], [self.right, self.bottom],
                [self.right, self.top], [self.left, self.top],
                [self.left, self.bottom],
            ]],
        }


def parcel_bbox() -> Bbox:
    """Tight 62-ha parcel bbox from the heightmap sidecar.

    Falls back to the canonical literal if the sidecar disappears — but the
    sidecar is canonical so this branch is for tooling sanity only.
    """
    if HEIGHTMAP_SIDECAR.exists():
        meta = json.loads(HEIGHTMAP_SIDECAR.read_text())
        b = meta["bbox"]
        return Bbox(b["left"], b["bottom"], b["right"], b["top"])
    return Bbox(-57.034496, -25.634054, -57.025504, -25.625946)


def search_bbox() -> Bbox:
    """3.3 km wider bbox used for satellite scene search / cross-validation."""
    if HEIGHTMAP_SIDECAR.exists():
        meta = json.loads(HEIGHTMAP_SIDECAR.read_text())
        b = meta.get("source_bbox") or meta["bbox"]
        return Bbox(b["left"], b["bottom"], b["right"], b["top"])
    return Bbox(-57.045, -25.645, -57.015, -25.615)


def parcel_center() -> tuple[float, float]:
    """(lon, lat) center of the parcel bbox."""
    return parcel_bbox().center


def out_dir(name: str) -> Path:
    d = SITE_DATA_DIR / name
    d.mkdir(parents=True, exist_ok=True)
    return d


def http_get(url: str, *, params: dict[str, Any] | None = None,
             headers: dict[str, str] | None = None,
             timeout: int = 60, max_attempts: int = 4,
             stream: bool = False) -> requests.Response:
    """GET with exponential backoff. Raises after final attempt."""
    delay = 2.0
    last: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            r = requests.get(url, params=params, headers=headers,
                             timeout=timeout, stream=stream)
            if r.status_code in (429, 502, 503, 504):
                raise requests.HTTPError(f"transient {r.status_code}: {url}")
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            last = e
            if attempt == max_attempts:
                break
            time.sleep(delay)
            delay *= 2
    assert last is not None
    raise last


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, default=str, ensure_ascii=False))


def env_required(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        raise SystemExit(
            f"[site_data] {name} not set — see tools/site_data/README.md for auth setup")
    return v
