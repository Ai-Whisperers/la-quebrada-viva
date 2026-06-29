"""SoilGrids 2.0 multi-point pull at the KML-derived 30.9 ha Mbopicua cluster.

Replaces the 2026-06-18 single-point pull (which was at the pre-KML centroid
-57.030,-25.630 and rendered an empty brochure table). New pull samples 6
locations across the polygon to capture sub-parcel soil variability for
foundation engineering, septic siting, and earth-construction feasibility.
"""

from __future__ import annotations

import csv
import json
import time
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "site_data" / "soilgrids"
OUT.mkdir(parents=True, exist_ok=True)

# KML-derived sample points (2026-06-28). All on or inside the 8-vertex polygon
# from docs/site_data/escobar_property_polygon.kml.
POINTS = [
    {"id": "centroid",   "lon": -57.0355,    "lat": -25.6073,    "note": "polygon centroid"},
    {"id": "nw_high",    "lon": -57.03844,   "lat": -25.60542,   "note": "NW corner (high ridge)"},
    {"id": "ne_corner",  "lon": -57.02928,   "lat": -25.60940,   "note": "NE corner (east boundary)"},
    {"id": "sw_corner",  "lon": -57.03781,   "lat": -25.60748,   "note": "SW corner (drainage side)"},
    {"id": "se_corner",  "lon": -57.03356,   "lat": -25.61172,   "note": "SE corner (lowest)"},
    {"id": "wes_pin",    "lon": -57.03365,   "lat": -25.61138,   "note": "Wesley interior pin (166.3 m AMSL)"},
]

PROPERTIES = ["clay", "sand", "silt", "phh2o", "bdod", "cec", "nitrogen", "ocd", "soc"]
DEPTHS = ["0-5cm", "5-15cm", "15-30cm", "30-60cm", "60-100cm", "100-200cm"]

ENDPOINT = "https://rest.isric.org/soilgrids/v2.0/properties/query"

session = requests.Session()
retry = Retry(
    total=6,
    backoff_factor=2.0,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=("GET",),
    raise_on_status=False,
)
session.mount("https://", HTTPAdapter(pool_connections=2, pool_maxsize=2, max_retries=retry))
session.headers.update({"User-Agent": "lqv-phase0/1.0 (research; weissvanderpol.ivan@gmail.com)"})


def pull_point(lon: float, lat: float) -> dict:
    params = [("lon", f"{lon}"), ("lat", f"{lat}"), ("value", "mean")]
    for p in PROPERTIES:
        params.append(("property", p))
    r = session.get(ENDPOINT, params=params, timeout=60)
    r.raise_for_status()
    return r.json()


def extract_value(feature: dict, prop: str, depth_label: str) -> tuple[float | None, str, str]:
    """Return (target-units value, target_units, mapped_units) or (None, '', '') if missing."""
    for layer in feature["properties"]["layers"]:
        if layer["name"] != prop:
            continue
        d_factor = layer["unit_measure"].get("d_factor", 1) or 1
        target_units = layer["unit_measure"].get("target_units", "")
        mapped_units = layer["unit_measure"].get("mapped_units", "")
        for d in layer["depths"]:
            if d["label"] != depth_label:
                continue
            mean = d["values"].get("mean")
            if mean is None:
                return None, target_units, mapped_units
            return mean / d_factor, target_units, mapped_units
    return None, "", ""


def main() -> None:
    # 1. Pull every point sequentially.
    pulled: dict[str, dict] = {}
    for pt in POINTS:
        print(f"-> {pt['id']:10s} lon={pt['lon']:.5f} lat={pt['lat']:.5f}")
        feat = pull_point(pt["lon"], pt["lat"])
        pulled[pt["id"]] = feat
        time.sleep(1.0)
    raw_path = OUT / "soilgrids_multipoint_raw.json"
    raw_path.write_text(json.dumps({"points": POINTS, "features": pulled}, indent=2))

    # 2. Flat CSV: one row per (point, property, depth).
    flat_path = OUT / "soilgrids_multipoint_flat.csv"
    with flat_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["point_id", "lon", "lat", "note", "property", "depth", "value", "target_units", "mapped_units"])
        for pt in POINTS:
            feat = pulled[pt["id"]]
            for prop in PROPERTIES:
                for d in DEPTHS:
                    val, target_u, mapped_u = extract_value(feat, prop, d)
                    w.writerow([pt["id"], pt["lon"], pt["lat"], pt["note"], prop, d,
                                "" if val is None else f"{val:.3f}", target_u, mapped_u])

    # 3. Per-depth pivot CSVs (one per depth) — easy to scan visually.
    for d in DEPTHS:
        path = OUT / f"soilgrids_depth_{d.replace('-', '_').replace('cm','cm')}.csv"
        with path.open("w", newline="") as f:
            w = csv.writer(f)
            header = ["point_id", "lon", "lat"] + PROPERTIES
            w.writerow(header)
            for pt in POINTS:
                feat = pulled[pt["id"]]
                row = [pt["id"], pt["lon"], pt["lat"]]
                for prop in PROPERTIES:
                    val, _, _ = extract_value(feat, prop, d)
                    row.append("" if val is None else f"{val:.2f}")
                w.writerow(row)

    # 4. Parcel-mean per (property, depth) — single source of truth.
    means_path = OUT / "soilgrids_parcel_means.csv"
    with means_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["property", "depth", "mean", "min", "max", "n_points", "target_units"])
        for prop in PROPERTIES:
            for d in DEPTHS:
                vals = []
                t_units = ""
                for pt in POINTS:
                    v, t_units2, _ = extract_value(pulled[pt["id"]], prop, d)
                    if v is not None:
                        vals.append(v)
                    if t_units2:
                        t_units = t_units2
                if vals:
                    mean = sum(vals) / len(vals)
                    w.writerow([prop, d, f"{mean:.3f}", f"{min(vals):.3f}", f"{max(vals):.3f}", len(vals), t_units])
                else:
                    w.writerow([prop, d, "", "", "", 0, t_units])

    # 5. Soil brief — deck/engineering grade narrative.
    brief = []
    brief.append("# Soil brief — La Quebrada Viva (30.9 ha Mbopicua cluster)\n")
    brief.append("Source: ISRIC SoilGrids 2.0 REST API (250 m raster), CC-BY 4.0  ")
    brief.append(f"Pulled: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}  ")
    brief.append(f"Sampling: {len(POINTS)} points across the KML polygon (centroid + 4 corners + Wesley pin)  ")
    brief.append("Raw layered JSON: `soilgrids_multipoint_raw.json` · Flat CSV: `soilgrids_multipoint_flat.csv` · Per-depth pivots: `soilgrids_depth_*.csv`\n")

    def parcel_mean(prop: str, depth: str) -> float | None:
        vals = []
        for pt in POINTS:
            v, _, _ = extract_value(pulled[pt["id"]], prop, depth)
            if v is not None:
                vals.append(v)
        return sum(vals) / len(vals) if vals else None

    # Construction-relevant slice
    brief.append("## Construction-relevant slice (0-30 cm parcel-mean)\n")
    brief.append("| Property | 0-5 cm | 5-15 cm | 15-30 cm | Target units |")
    brief.append("| --- | --- | --- | --- | --- |")
    prop_units = {
        "clay": "% (g/kg ÷ 10)", "sand": "% (g/kg ÷ 10)", "silt": "% (g/kg ÷ 10)",
        "phh2o": "pH unit", "bdod": "kg/dm³", "cec": "cmol(c)/kg",
        "nitrogen": "g/kg", "ocd": "kg/m³", "soc": "g/kg",
    }
    for prop in PROPERTIES:
        cells = []
        for d in ("0-5cm", "5-15cm", "15-30cm"):
            v = parcel_mean(prop, d)
            cells.append("n/a" if v is None else f"{v:.2f}")
        brief.append(f"| **{prop}** | {cells[0]} | {cells[1]} | {cells[2]} | {prop_units[prop]} |")

    # Footing-depth slice
    brief.append("\n## Footing-depth slice (30-200 cm parcel-mean)\n")
    brief.append("| Property | 30-60 cm | 60-100 cm | 100-200 cm | Target units |")
    brief.append("| --- | --- | --- | --- | --- |")
    for prop in PROPERTIES:
        cells = []
        for d in ("30-60cm", "60-100cm", "100-200cm"):
            v = parcel_mean(prop, d)
            cells.append("n/a" if v is None else f"{v:.2f}")
        brief.append(f"| **{prop}** | {cells[0]} | {cells[1]} | {cells[2]} | {prop_units[prop]} |")

    # Engineering flags
    brief.append("\n## Engineering flags (auto-derived)\n")
    flags = []
    c_top = parcel_mean("clay", "0-5cm")
    c_60 = parcel_mean("clay", "30-60cm")
    c_100 = parcel_mean("clay", "60-100cm")
    s_top = parcel_mean("sand", "0-5cm")
    pH_top = parcel_mean("phh2o", "0-5cm")
    bd_top = parcel_mean("bdod", "0-5cm")
    soc_top = parcel_mean("soc", "0-5cm")
    n_top = parcel_mean("nitrogen", "0-5cm")
    cec_top = parcel_mean("cec", "0-5cm")

    if c_top is not None:
        flags.append(f"- **Topsoil texture:** clay={c_top:.1f}%, sand={s_top:.1f}% → "
                     + ("clay-rich (cob mix viable, low sand bulking needed)" if c_top > 35
                        else "clay-loam (typical sand bulking required for cob)" if c_top > 25
                        else "sandy-loam (significant clay supplementation needed)"))
    if c_60 is not None and c_100 is not None:
        max_sub = max(c_60, c_100)
        if max_sub > 40:
            flags.append(f"- **Expansive-soil risk (30-200 cm):** clay peaks at {max_sub:.1f}% → "
                         "design strip/pad footings below active zone; consider reinforced concrete grade beam.")
        else:
            flags.append(f"- **Subsoil clay (30-200 cm):** max {max_sub:.1f}% → moderate shrink-swell risk, "
                         "standard isolated footings acceptable with 60 cm minimum depth.")
    if pH_top is not None:
        flags.append(f"- **Topsoil pH:** {pH_top:.2f} → "
                     + ("acidic — cement-stabilised earth blocks need extra lime (CSEB lime dose +50%)" if pH_top < 5.5
                        else "near-neutral — standard CSEB lime dose acceptable" if pH_top < 6.5
                        else "neutral/alkaline — no lime adjustment needed"))
    if bd_top is not None:
        flags.append(f"- **Topsoil bulk density (0-5 cm):** {bd_top:.2f} kg/dm³ → "
                     + ("very loose, strip and stockpile before any compaction" if bd_top < 1.2
                        else "moderate density, normal stripping protocol" if bd_top < 1.4
                        else "dense — minimal compaction loss expected"))
    if soc_top is not None and n_top is not None:
        flags.append(f"- **Topsoil fertility (0-5 cm):** SOC={soc_top:.1f} g/kg, N={n_top:.2f} g/kg, "
                     f"CEC={cec_top:.1f} cmol(c)/kg → "
                     + ("high fertility — preserve A-horizon for orchard/pasture" if soc_top > 25
                        else "moderate fertility — typical of degraded pasture, amendments required for intensive cropping" if soc_top > 12
                        else "low fertility — significant amendments needed for cultivation"))
    if c_60 is not None:
        flags.append(f"- **Septic-leach-field feasibility (30-60 cm):** clay={c_60:.1f}% → "
                     + ("impermeable, conventional leach field not viable, design ETA bed or constructed wetland" if c_60 > 40
                        else "marginal permeability, sized leach field 30% larger than standard" if c_60 > 25
                        else "acceptable percolation, standard leach field viable"))

    # Sub-parcel variability flag
    flags.append("\n### Sub-parcel variability (point-to-point spread)\n")
    flags.append("| Property | Depth | Min | Mean | Max | Spread |")
    flags.append("| --- | --- | --- | --- | --- | --- |")
    for prop in ("clay", "sand", "phh2o", "soc"):
        for d in ("0-5cm", "30-60cm"):
            vals = [extract_value(pulled[pt["id"]], prop, d)[0] for pt in POINTS]
            vals = [v for v in vals if v is not None]
            if vals:
                spread = max(vals) - min(vals)
                flags.append(f"| {prop} | {d} | {min(vals):.2f} | {sum(vals)/len(vals):.2f} | "
                             f"{max(vals):.2f} | {spread:.2f} |")

    brief.extend(flags)

    brief.append("\n## Methodology notes\n")
    brief.append("- SoilGrids 2.0 native raster resolution is 250 m, so 6 points within a 30.9 ha "
                 "(~556 m × 556 m equivalent) parcel may sample 2-4 distinct raster cells. Point-to-point "
                 "spread reflects actual sub-parcel variability where present.")
    brief.append("- All values are predictive (Quantile Random Forest) — they are *not* substitutes for "
                 "in-situ geotechnical drilling. Use as design-stage screening to plan where to drill.")
    brief.append("- d_factor scaling already applied: clay/sand/silt reported in % (raw is g/kg × 10), "
                 "phh2o in pH units (raw is pH × 10), all others in their target units per SoilGrids docs.")
    brief.append("- For foundation engineering: confirm subsoil cohesion with at least 2 hand-auger holes "
                 "to 2 m depth before pouring footings, especially at NE and SE corners where the SoilGrids "
                 "draw-down may underrepresent the actual clay content of the Mbopicua geological substrate.")

    (OUT / "soil_brief.md").write_text("\n".join(brief) + "\n")

    # 6. Summary
    summary = [
        f"# Soil brief — SoilGrids 2.0 multi-point pull (KML-derived)",
        f"- Points sampled: {len(POINTS)} (centroid + 4 corners + Wesley pin)",
        f"- Properties: {', '.join(PROPERTIES)}",
        f"- Depths: {', '.join(DEPTHS)}",
        f"- Total values written: {len(POINTS) * len(PROPERTIES) * len(DEPTHS)}",
    ]
    if c_top is not None and pH_top is not None and bd_top is not None:
        summary.append(f"- Headline: topsoil clay {c_top:.1f}%, pH {pH_top:.2f}, bulk-density {bd_top:.2f} kg/dm³")
    if c_60 is not None:
        summary.append(f"- Footing-depth clay (30-60 cm): {c_60:.1f}%")
    (OUT / "soilgrids_v2_summary.txt").write_text("\n".join(summary) + "\n")

    print(f"\nDone. {len(POINTS)} points × {len(PROPERTIES)} properties × {len(DEPTHS)} depths = "
          f"{len(POINTS)*len(PROPERTIES)*len(DEPTHS)} values written to {OUT}")


if __name__ == "__main__":
    main()
