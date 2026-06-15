"""GEDI L2A canopy-height driver — replaces uniform TREE_SCALE_RANGE with
empirically sampled scale ratios.

Reads ``docs/site_data/gedi_l2a_points_clean.csv`` column
``canopy_height_m_final``, filters to a plausible canopy window [10, 40] m
(drops 8/25 outliers reported as 80 m sensor saturation), and exposes
``sample_scale(rng) -> float`` returning a per-tree scale ratio:

    scale = clamp(height_m / GEDI_SCALE_REF_M, SCALE_MIN, SCALE_MAX)

Where ``GEDI_SCALE_REF_M = 25.0`` is rounded from the filtered-median
canopy height (25.33 m). A 10 m sample → 0.6 (clamped, mid-storey),
25 m → 1.0 (median emergent canopy), 40 m → 1.6 (clamped, hero tree).

Mature emergent species in the parcel (lapacho, jacaranda) genuinely
tower above the median, so a wider [0.6, 1.6] band beats the prior
uniform (0.6, 1.2) which truncated tall heroes.
"""
from __future__ import annotations

import csv
import os
from typing import List

_PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
GEDI_CSV = os.path.join(
    _PROJECT_ROOT, "docs", "site_data", "gedi_l2a_points_clean.csv"
)

GEDI_MIN_M = 10.0
GEDI_MAX_M = 40.0
GEDI_SCALE_REF_M = 25.0
SCALE_MIN = 0.6
SCALE_MAX = 1.6

_HEIGHTS_CACHE: List[float] | None = None


def _load_heights() -> List[float]:
    global _HEIGHTS_CACHE
    if _HEIGHTS_CACHE is not None:
        return _HEIGHTS_CACHE
    heights: List[float] = []
    with open(GEDI_CSV, newline="") as f:
        for row in csv.DictReader(f):
            try:
                h = float(row["canopy_height_m_final"])
            except (KeyError, TypeError, ValueError):
                continue
            if GEDI_MIN_M <= h <= GEDI_MAX_M:
                heights.append(h)
    if not heights:
        # Fallback: anchor at reference so scatter still runs if the CSV
        # is empty or malformed — log loudly but don't crash the render.
        print(f"[gedi] WARNING: no valid heights in {GEDI_CSV}; "
              f"falling back to single ref {GEDI_SCALE_REF_M} m")
        heights = [GEDI_SCALE_REF_M]
    _HEIGHTS_CACHE = heights
    return _HEIGHTS_CACHE


def sample_scale(rng) -> float:
    """Pick one GEDI canopy height and map it to a clamped scale ratio.

    ``rng`` must expose ``.choice(seq)`` — pass ``random`` (module) or a
    ``random.Random`` instance. Returns a float in [SCALE_MIN, SCALE_MAX].
    """
    h = rng.choice(_load_heights())
    s = h / GEDI_SCALE_REF_M
    if s < SCALE_MIN:
        return SCALE_MIN
    if s > SCALE_MAX:
        return SCALE_MAX
    return s
