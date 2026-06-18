"""62-ha terrain model — availability gate + dispatcher to the active heightmap builder.

The original stub here gated on a 5 m DEM TIFF that was never sourced; the
project pivoted to a 30 m DEM (ALOS AW3D30 canonical, with COP30 / SRTM /
NASADEM cross-checks) baked into a normalized 16-bit PNG + JSON sidecar pair
under ``assets/terrain/``. The active builder lives in
``lqv.subscene.terrain_62ha_photoreal`` (renderable as a sub-render with
albedo overlay and Displace + SUBSURF stack).

This module stays so that the rest of the codebase has a stable
``lqv.site.terrain_62ha`` entry point (``is_available`` + ``build_terrain``).
It now gates on the heightmap pair, and delegates building to the photoreal
subscene module rather than reimplementing.
"""
from __future__ import annotations

import os
from typing import Any

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TERRAIN_DIR = os.path.join(_REPO_ROOT, "assets", "terrain")
HEIGHTMAP_PNG = os.path.join(TERRAIN_DIR, "escobar_height.png")
HEIGHTMAP_JSON = os.path.join(TERRAIN_DIR, "escobar_height.json")


def is_available() -> bool:
    """True iff the canonical heightmap pair (PNG + JSON) is on disk."""
    return os.path.exists(HEIGHTMAP_PNG) and os.path.exists(HEIGHTMAP_JSON)


def build_terrain(parent: Any = None, exaggeration: float = 1.5) -> Any:
    """Build the 62-ha parcel terrain by delegating to the photoreal subscene.

    Returns the terrain Blender object so callers can re-parent or annotate.
    The ``exaggeration`` arg overrides ``Z_EXAGGERATION`` for this build only;
    pass 1.0 for true scale, 1.5 for the project default.
    """
    if not is_available():
        raise FileNotFoundError(
            f"heightmap pair missing — expected {HEIGHTMAP_PNG} and {HEIGHTMAP_JSON}. "
            "Run `python3 scripts/make_terrain_heightmap.py` to bake from "
            "docs/site_data/alos_aw3d30_dem.tif."
        )

    from lqv.subscene import terrain_62ha_photoreal as photoreal

    builder = getattr(photoreal, "_build_terrain_mesh", None)
    if builder is None:
        raise RuntimeError(
            "lqv.subscene.terrain_62ha_photoreal._build_terrain_mesh is missing — "
            "the photoreal subscene module has been refactored; update this facade."
        )

    prev = getattr(photoreal, "Z_EXAGGERATION", None)
    photoreal.Z_EXAGGERATION = float(exaggeration)
    try:
        obj = builder()
    finally:
        if prev is not None:
            photoreal.Z_EXAGGERATION = prev

    if parent is not None and obj is not None:
        obj.parent = parent
    return obj
