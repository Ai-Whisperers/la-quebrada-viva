"""Pelton micro-hydro available-head map from the COP30 DEM.

For each cell of the COP30 DEM that covers the LQV parcel + upslope catchment,
computes the available gross head: the elevation difference between the highest
point within a ~300 m horizontal radius (penstock length ceiling for a low-cost
HDPE run) and the cell itself. The result is the head a Pelton turbine sited at
that cell could harvest by tapping the nearest upslope ridge with ≤300 m of pipe.

Outputs:
  docs/site_data/pelton_head_map.png   8-bit greyscale head map, hot=more head
  docs/site_data/pelton_head_map.json  stats + provenance sidecar

Justification: Wesley's energy-budget brief (docs/energy_budget.md) targets a
micro-hydro contribution in the off-grid stack. Rule 7 ("critical systems
outage-proof") requires the head feasibility to be evidence-backed, not a
narrative claim. This map shows where on the 62-ha parcel a Pelton install is
geometrically possible (and where it isn't).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image
from scipy.ndimage import maximum_filter


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEM_TIF = PROJECT_ROOT / "docs/site_data/cop30_dem.tif"
OUT_PNG = PROJECT_ROOT / "docs/site_data/pelton_head_map.png"
OUT_JSON = PROJECT_ROOT / "docs/site_data/pelton_head_map.json"

PENSTOCK_RADIUS_M = 300.0
PELTON_MIN_HEAD_M = 30.0
PELTON_GOOD_HEAD_M = 80.0


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    with rasterio.open(DEM_TIF) as src:
        dem = src.read(1).astype(np.float32)
        bounds = src.bounds
        res_deg_y = abs(src.res[1])

    lat_mid = 0.5 * (bounds.top + bounds.bottom)
    m_per_deg_lat = 111320.0
    m_per_deg_lon = 111320.0 * float(np.cos(np.deg2rad(lat_mid)))
    px_size_m_y = res_deg_y * m_per_deg_lat
    px_size_m_x = abs(src.res[0]) * m_per_deg_lon if False else abs(bounds.right - bounds.left) / dem.shape[1] * m_per_deg_lon

    px_size_m = 0.5 * (px_size_m_x + px_size_m_y)
    radius_px = max(1, int(round(PENSTOCK_RADIUS_M / px_size_m)))
    window = 2 * radius_px + 1

    upslope_max = maximum_filter(dem, size=window, mode="nearest")
    head = np.clip(upslope_max - dem, 0.0, None)

    head_max = float(head.max())
    head_mean = float(head.mean())
    head_p95 = float(np.percentile(head, 95))
    pct_above_min = float((head >= PELTON_MIN_HEAD_M).mean() * 100.0)
    pct_above_good = float((head >= PELTON_GOOD_HEAD_M).mean() * 100.0)

    head_norm = head / max(head_max, 1.0)
    img8 = np.clip(head_norm * 255.0, 0, 255).astype(np.uint8)
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(img8, mode="L").save(OUT_PNG, optimize=True)

    sidecar = {
        "source_dem": str(DEM_TIF.relative_to(PROJECT_ROOT)),
        "source_dem_sha256": _sha256(DEM_TIF),
        "penstock_radius_m": PENSTOCK_RADIUS_M,
        "pelton_min_head_m": PELTON_MIN_HEAD_M,
        "pelton_good_head_m": PELTON_GOOD_HEAD_M,
        "px_size_m_approx": round(px_size_m, 2),
        "radius_px": radius_px,
        "window_px": window,
        "head_max_m": round(head_max, 2),
        "head_mean_m": round(head_mean, 2),
        "head_p95_m": round(head_p95, 2),
        "pct_pixels_above_min_head": round(pct_above_min, 1),
        "pct_pixels_above_good_head": round(pct_above_good, 1),
        "dem_shape": list(dem.shape),
        "dem_bounds_wgs84": {
            "left": bounds.left, "right": bounds.right,
            "top": bounds.top, "bottom": bounds.bottom,
        },
        "method": (
            "scipy.ndimage.maximum_filter on COP30 with square window of "
            f"{window}×{window} px (~{2 * radius_px * px_size_m:.0f} m a side); "
            "head = max_in_window − own_z, clipped ≥0."
        ),
    }
    OUT_JSON.write_text(json.dumps(sidecar, indent=2) + "\n")

    print(
        f"WROTE {OUT_PNG.relative_to(PROJECT_ROOT)}  "
        f"({OUT_PNG.stat().st_size // 1024} KB)\n"
        f"WROTE {OUT_JSON.relative_to(PROJECT_ROOT)}\n"
        f"head_max={head_max:.1f} m  mean={head_mean:.1f} m  p95={head_p95:.1f} m  "
        f"{pct_above_min:.1f}% ≥ {PELTON_MIN_HEAD_M:.0f} m, "
        f"{pct_above_good:.1f}% ≥ {PELTON_GOOD_HEAD_M:.0f} m"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
