#!/usr/bin/env python3
"""Phase-0 §12.12: extend the existing point-only SoilGrids sample
(docs/site_data/soilgrids/) into a polygon-coverage profile cube. Samples a
regular grid of ~25 points across the polygon AOI bbox, returning every
property × every depth slice at each location.

Outputs land in docs/site_data/soilgrids/cube/:
- points_grid.geojson — sampling locations
- profiles.json — full raw REST response per point
- profiles_long.csv — flat property/depth/value/uncertainty rows
- summary.md — mean ± sd per property/depth across the grid
"""

from __future__ import annotations

import csv
import json
import statistics
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "site_data" / "soilgrids" / "cube"
OUT.mkdir(parents=True, exist_ok=True)

# Polygon bbox (Wesley's 30.9 ha buildable) +1 km buffer to catch ridge soil:
W, S, E, N = -57.050, -25.625, -57.020, -25.595
GRID_N = 5  # 5×5 = 25 points

PROPERTIES = ["phh2o", "soc", "clay", "sand", "silt", "bdod", "cec", "cfvo", "nitrogen"]
DEPTHS = ["0-5cm", "5-15cm", "15-30cm", "30-60cm", "60-100cm", "100-200cm"]
VALUES = ["mean", "uncertainty"]

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "lqv-phase0/1.0 (research; weissvanderpol.ivan@gmail.com)"})


def sample_point(lon: float, lat: float) -> dict:
    params: list[tuple[str, str]] = []
    for p in PROPERTIES:
        params.append(("property", p))
    for d in DEPTHS:
        params.append(("depth", d))
    for v in VALUES:
        params.append(("value", v))
    params.append(("lon", str(lon)))
    params.append(("lat", str(lat)))
    r = SESSION.get(
        "https://rest.isric.org/soilgrids/v2.0/properties/query",
        params=params,
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


def main() -> int:
    # build a regular lon/lat grid
    grid: list[tuple[float, float]] = []
    for i in range(GRID_N):
        for j in range(GRID_N):
            lon = W + (E - W) * (i + 0.5) / GRID_N
            lat = S + (N - S) * (j + 0.5) / GRID_N
            grid.append((round(lon, 6), round(lat, 6)))

    # write geojson of points
    fc = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": {"grid_id": k},
            }
            for k, (lon, lat) in enumerate(grid)
        ],
    }
    (OUT / "points_grid.geojson").write_text(json.dumps(fc, indent=2), encoding="utf-8")
    print(f"Grid: {len(grid)} points")

    profiles: list[dict] = []
    rows: list[dict] = []
    for k, (lon, lat) in enumerate(grid):
        try:
            data = sample_point(lon, lat)
        except Exception as e:
            print(f"  point {k} ({lon},{lat}) failed: {type(e).__name__}: {e}")
            time.sleep(2)
            continue
        profiles.append({"grid_id": k, "lon": lon, "lat": lat, "response": data})
        for layer in data.get("properties", {}).get("layers", []):
            pname = layer.get("name")
            unit = (layer.get("unit_measure") or {}).get("mapped_units")
            d_factor = (layer.get("unit_measure") or {}).get("d_factor") or 1
            for d in layer.get("depths", []):
                vals = d.get("values") or {}
                row = {
                    "grid_id": k,
                    "lon": lon,
                    "lat": lat,
                    "property": pname,
                    "depth": d.get("label"),
                    "unit": unit,
                    "d_factor": d_factor,
                    "mean": vals.get("mean"),
                    "uncertainty": vals.get("uncertainty"),
                }
                rows.append(row)
        if k % 5 == 4:
            print(f"  {k+1}/{len(grid)} done")
        time.sleep(0.6)  # be polite to ISRIC

    (OUT / "profiles.json").write_text(
        json.dumps(profiles, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    csv_path = OUT / "profiles_long.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "grid_id",
                "lon",
                "lat",
                "property",
                "depth",
                "unit",
                "d_factor",
                "mean",
                "uncertainty",
            ],
        )
        w.writeheader()
        w.writerows(rows)
    print(f"CSV → {csv_path} ({len(rows)} rows)")

    # summary stats by (property, depth)
    agg: dict[tuple[str, str], list[float]] = {}
    for r in rows:
        v = r["mean"]
        if v is None:
            continue
        agg.setdefault((r["property"], r["depth"]), []).append(v)
    md = ["# SoilGrids 250 m profile cube — 5×5 grid over polygon AOI", ""]
    md.append(f"BBox W{W} S{S} E{E} N{N}; sample n={len(grid)}; ISRIC REST v2.0")
    md.append("")
    md.append("> Values shown as `mean ± sd` of the n sampled points, in the native d_factor units.")
    md.append("> Real-world units = mean / d_factor (e.g., phh2o d_factor=10, so reported 50 ≈ pH 5.0).")
    md.append("")
    md.append("| Property | Depth | n | Mean | SD | Min | Max |")
    md.append("|---|---|---:|---:|---:|---:|---:|")
    for (prop, depth), vals in sorted(agg.items()):
        if not vals:
            continue
        md.append(
            f"| {prop} | {depth} | {len(vals)} | {statistics.fmean(vals):.1f} | "
            f"{(statistics.pstdev(vals) if len(vals)>1 else 0):.1f} | "
            f"{min(vals):.0f} | {max(vals):.0f} |"
        )
    (OUT / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("summary.md written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
