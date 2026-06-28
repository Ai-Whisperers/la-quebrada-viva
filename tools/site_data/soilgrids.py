"""SoilGrids 250 m point query for the parcel center.

ISRIC's free REST API. No auth. CC-BY 4.0.
Returns clay / sand / silt / bulk-density / pH / SOC at 6 depth slices —
the inputs the structural engineer asks for when validating cob walls and
strip-footing depth on the 62-ha block.

API: https://rest.isric.org/soilgrids/v2.0/properties/query
Docs: https://www.isric.org/explore/soilgrids/faq-soilgrids

Run:
    python3 -m tools.site_data.soilgrids
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path

from .common import http_get, out_dir, parcel_center, write_json

ENDPOINT = "https://rest.isric.org/soilgrids/v2.0/properties/query"

PROPERTIES = [
    "bdod", "cec", "cfvo", "clay", "nitrogen", "ocd",
    "phh2o", "sand", "silt", "soc",
]
DEPTHS = ["0-5cm", "5-15cm", "15-30cm", "30-60cm", "60-100cm", "100-200cm"]
VALUES = ["mean", "uncertainty"]


def fetch(lon: float, lat: float) -> dict:
    # requests serialises list values as repeated query params,
    # which matches the SoilGrids contract: ?property=clay&property=sand…
    params = {
        "lon": lon,
        "lat": lat,
        "property": PROPERTIES,
        "depth": DEPTHS,
        "value": VALUES,
    }
    r = http_get(ENDPOINT, params=params, timeout=90)
    return r.json()


def summarise(payload: dict) -> dict:
    """Pull mean values into a flat table for the deck."""
    flat = {}
    for layer in payload.get("properties", {}).get("layers", []):
        name = layer["name"]
        d_factor = layer["unit_measure"]["d_factor"]
        target_units = layer["unit_measure"]["target_units"]
        for depth in layer.get("depths", []):
            label = depth["label"]
            mean = depth["values"].get("mean")
            if mean is None:
                continue
            flat[f"{name}_{label}_{target_units}"] = round(mean / d_factor, 3)
    return flat


def write_brochure(out: Path, flat: dict, lon: float, lat: float) -> None:
    """Engineer-readable summary."""
    lines = [
        "# SoilGrids 250 m — La Quebrada Viva parcel",
        "",
        "Source: ISRIC SoilGrids v2.0 (https://soilgrids.org), CC-BY 4.0  ",
        f"Point: lon={lon:.5f}, lat={lat:.5f} (parcel centroid)  ",
        f"Pulled: {dt.datetime.now(dt.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "",
        "## Construction-relevant slices (0-30 cm)",
        "",
        "| Property | Value |",
        "| --- | --- |",
    ]
    construction = [
        ("clay_0-5cm_g/kg",   "clay 0-5 cm"),
        ("clay_5-15cm_g/kg",  "clay 5-15 cm"),
        ("clay_15-30cm_g/kg", "clay 15-30 cm"),
        ("sand_0-5cm_g/kg",   "sand 0-5 cm"),
        ("sand_15-30cm_g/kg", "sand 15-30 cm"),
        ("silt_15-30cm_g/kg", "silt 15-30 cm"),
        ("bdod_0-5cm_cg/cm³", "bulk density 0-5 cm"),
        ("phh2o_0-5cm_pH",    "pH(H2O) 0-5 cm"),
        ("soc_0-5cm_dg/kg",   "soil org C 0-5 cm"),
    ]
    for key, label in construction:
        v = flat.get(key)
        if v is not None:
            lines.append(f"| {label} | {v} |")
    lines += [
        "",
        "## Footing-depth slices (30-200 cm)",
        "",
        "| Property | Value |",
        "| --- | --- |",
    ]
    footing = [
        ("clay_30-60cm_g/kg",   "clay 30-60 cm"),
        ("clay_60-100cm_g/kg",  "clay 60-100 cm"),
        ("clay_100-200cm_g/kg", "clay 100-200 cm"),
        ("bdod_30-60cm_cg/cm³", "bulk density 30-60 cm"),
        ("bdod_100-200cm_cg/cm³", "bulk density 100-200 cm"),
    ]
    for key, label in footing:
        v = flat.get(key)
        if v is not None:
            lines.append(f"| {label} | {v} |")
    lines += [
        "",
        "## Interpretation hooks",
        "",
        "- Clay > 350 g/kg in any 0-30 cm slice → cob mix viable without sand bulking.",
        "- Clay > 400 g/kg at 30-100 cm → expansive-soil risk: design strip footings"
        " below the active zone.",
        "- pH < 5.5 → cement-stabilised earth blocks need extra lime; check before specifying.",
        "- Bulk density < 1.2 g/cm³ at 0-5 cm → topsoil to strip and stockpile before"
        " any compaction.",
        "",
        "Raw layered JSON: `soilgrids_point.json`.",
    ]
    out.write_text("\n".join(lines))


def main() -> None:
    lon, lat = parcel_center()
    out = out_dir("soilgrids")
    print(f"[soilgrids] querying lon={lon:.5f}, lat={lat:.5f}")
    payload = fetch(lon, lat)
    write_json(out / "soilgrids_point.json", payload)
    flat = summarise(payload)
    write_json(out / "soilgrids_flat.json", flat)
    write_brochure(out / "soilgrids_brochure.md", flat, lon, lat)
    summary_path = out / "soilgrids_summary.txt"
    summary_lines = [
        f"SoilGrids 250 m point query — lon={lon:.5f}, lat={lat:.5f}",
        f"{len(flat)} property×depth values written",
    ]
    headline = [
        ("clay_0-5cm_g/kg", "clay 0-5 cm"),
        ("sand_0-5cm_g/kg", "sand 0-5 cm"),
        ("phh2o_0-5cm_pH",  "pH 0-5 cm"),
        ("clay_30-60cm_g/kg", "clay 30-60 cm"),
        ("bdod_30-60cm_cg/cm³", "bulk density 30-60 cm"),
    ]
    for key, label in headline:
        v = flat.get(key)
        if v is not None:
            summary_lines.append(f"  {label}: {v}")
    summary_path.write_text("\n".join(summary_lines) + "\n")
    print(f"[soilgrids] wrote {out}")


if __name__ == "__main__":
    main()
