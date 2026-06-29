"""
Phase-0 §12 — CHELSA v2.1 1981-2010 bioclimatic indicators windowed AOI pull.

CHELSA (Climatologies at High resolution for the Earth's Land Surface Areas)
v2.1 provides global 30-arcsec (~1 km) bioclim normals 1981-2010. We pull
the 19 standard WorldClim-equivalent BIO variables via /vsicurl/ windowed
reads from the live Switch.ch zhdk mirror — replaces dead UC Davis WorldClim.

Scale factors (CHELSA v2.1 tech doc):
  bio1, 5, 6, 8, 9, 10, 11: scale 0.1, offset -273.15  → °C
  bio2, 7:                   scale 0.1, offset 0       → °C (diurnal/annual range)
  bio3:                      scale 0.1, offset 0       → %  (isothermality)
  bio4:                      scale 0.1, offset 0       → °C×100 (seasonality stdev)
  bio12-14, 16-19:           scale 0.1, offset 0       → mm   (precip totals)
  bio15:                     scale 0.1, offset 0       → %   (precip CV)

Outputs:
  docs/site_data/chelsa/chelsa_bio_AOI_<N>.tif  (windowed AOI rasters)
  docs/site_data/chelsa/chelsa_points.csv       (per-point sample)
  docs/site_data/chelsa/chelsa_summary.json     (AOI stats + provenance)
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import rasterio
from rasterio.windows import from_bounds

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs/site_data/chelsa"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE = (
    "https://os.zhdk.cloud.switch.ch/chelsav2/GLOBAL/climatologies/1981-2010/bio/"
    "CHELSA_bio{n}_1981-2010_V.2.1.tif"
)

# (name, scale, offset, unit, description)
BIO_META: dict[int, tuple[str, float, float, str, str]] = {
    1:  ("bio01_mean_annual_T",        0.1, -273.15, "degC",  "Annual mean temperature"),
    2:  ("bio02_diurnal_range",        0.1, 0.0,     "degC",  "Mean diurnal range"),
    3:  ("bio03_isothermality",        0.1, 0.0,     "pct",   "Isothermality (bio2/bio7)*100"),
    4:  ("bio04_T_seasonality",        0.1, 0.0,     "degCx100", "Temperature seasonality (stdev*100)"),
    5:  ("bio05_T_max_warmest",        0.1, -273.15, "degC",  "Max temp of warmest month"),
    6:  ("bio06_T_min_coldest",        0.1, -273.15, "degC",  "Min temp of coldest month"),
    7:  ("bio07_T_annual_range",       0.1, 0.0,     "degC",  "Temp annual range (bio5-bio6)"),
    8:  ("bio08_T_wettest_qtr",        0.1, -273.15, "degC",  "Mean temp of wettest quarter"),
    9:  ("bio09_T_driest_qtr",         0.1, -273.15, "degC",  "Mean temp of driest quarter"),
    10: ("bio10_T_warmest_qtr",        0.1, -273.15, "degC",  "Mean temp of warmest quarter"),
    11: ("bio11_T_coldest_qtr",        0.1, -273.15, "degC",  "Mean temp of coldest quarter"),
    12: ("bio12_annual_precip",        0.1, 0.0,     "mm",    "Annual precipitation"),
    13: ("bio13_P_wettest_month",      0.1, 0.0,     "mm",    "Precip of wettest month"),
    14: ("bio14_P_driest_month",       0.1, 0.0,     "mm",    "Precip of driest month"),
    15: ("bio15_P_seasonality_CV",     0.1, 0.0,     "pct",   "Precip seasonality (CV)"),
    16: ("bio16_P_wettest_qtr",        0.1, 0.0,     "mm",    "Precip of wettest quarter"),
    17: ("bio17_P_driest_qtr",         0.1, 0.0,     "mm",    "Precip of driest quarter"),
    18: ("bio18_P_warmest_qtr",        0.1, 0.0,     "mm",    "Precip of warmest quarter"),
    19: ("bio19_P_coldest_qtr",        0.1, 0.0,     "mm",    "Precip of coldest quarter"),
}

CENTROID = (-57.0355, -25.6073)
WESLEY = (-57.03365675409436, -25.61138883666841)
KML_CORNERS = {
    "corner_NE": (-57.0151, -25.6149),
    "corner_NW": (-57.0451, -25.6149),
    "corner_SE": (-57.0151, -25.6449),
    "corner_SW": (-57.0451, -25.6449),
}
POINTS = [
    ("centroid", CENTROID[0], CENTROID[1]),
    *((k, v[0], v[1]) for k, v in KML_CORNERS.items()),
    ("wesley_pin", WESLEY[0], WESLEY[1]),
]

# 5 km buffer (≈0.05°) around centroid for AOI window
AOI_BUFFER_DEG = 0.05


def aoi_bounds() -> tuple[float, float, float, float]:
    lon, lat = CENTROID
    return (
        lon - AOI_BUFFER_DEG,
        lat - AOI_BUFFER_DEG,
        lon + AOI_BUFFER_DEG,
        lat + AOI_BUFFER_DEG,
    )


def fetch_bio(n: int) -> Path:
    name = BIO_META[n][0]
    url = f"/vsicurl/{BASE.format(n=n)}"
    dst = OUT_DIR / f"chelsa_{name}.tif"
    left, bottom, right, top = aoi_bounds()
    with rasterio.open(url) as src:
        window = from_bounds(left, bottom, right, top, transform=src.transform)
        window = window.round_offsets().round_lengths()
        arr = src.read(1, window=window)
        transform = src.window_transform(window)
        profile = src.profile.copy()
        profile.update(
            height=arr.shape[0],
            width=arr.shape[1],
            transform=transform,
            compress="deflate",
            tiled=True,
            blockxsize=128,
            blockysize=128,
        )
        with rasterio.open(dst, "w", **profile) as out:
            out.write(arr, 1)
    return dst


def sample_points(rasters: dict[int, Path]) -> list[dict]:
    rows: list[dict] = []
    opened = {n: rasterio.open(p) for n, p in rasters.items()}
    try:
        for name, lon, lat in POINTS:
            row: dict = {"point": name, "lon": lon, "lat": lat}
            for n, src in opened.items():
                label = BIO_META[n][0]
                scale = BIO_META[n][1]
                offset = BIO_META[n][2]
                col, r = ~src.transform * (lon, lat)
                col = int(round(col))
                r = int(round(r))
                if 0 <= col < src.width and 0 <= r < src.height:
                    nodata = src.nodata
                    arr = src.read(1, window=((r, r + 1), (col, col + 1))).astype(np.float64).ravel()
                    if nodata is not None:
                        arr = arr[arr != nodata]
                    if arr.size:
                        raw = float(arr[0])
                        val = raw * scale + offset
                        row[label] = round(val, 3)
                    else:
                        row[label] = None
                else:
                    row[label] = None
            rows.append(row)
    finally:
        for src in opened.values():
            src.close()
    return rows


def aoi_summary(rasters: dict[int, Path]) -> dict:
    summary: dict = {}
    for n, p in rasters.items():
        label, scale, offset, unit, desc = BIO_META[n]
        with rasterio.open(p) as src:
            nodata = src.nodata
            arr = src.read(1).astype(np.float64)
            if nodata is not None:
                arr = arr[arr != nodata]
            arr = arr[np.isfinite(arr)]
            if arr.size == 0:
                summary[label] = None
                continue
            scaled = arr * scale + offset
            summary[label] = {
                "unit": unit,
                "description": desc,
                "mean": round(float(np.mean(scaled)), 3),
                "median": round(float(np.median(scaled)), 3),
                "p05": round(float(np.percentile(scaled, 5)), 3),
                "p95": round(float(np.percentile(scaled, 95)), 3),
                "min": round(float(np.min(scaled)), 3),
                "max": round(float(np.max(scaled)), 3),
                "pixels": int(arr.size),
            }
    return summary


def main() -> None:
    print(f"AOI bounds: {aoi_bounds()}")
    rasters: dict[int, Path] = {}
    for n in BIO_META:
        label = BIO_META[n][0]
        print(f"  fetching {label} …", flush=True)
        rasters[n] = fetch_bio(n)
        size_kb = rasters[n].stat().st_size // 1024
        print(f"    → {rasters[n].name} ({size_kb} KB)")

    rows = sample_points(rasters)
    summary = aoi_summary(rasters)

    csv_path = OUT_DIR / "chelsa_points.csv"
    fieldnames = ["point", "lon", "lat", *(BIO_META[n][0] for n in BIO_META)]
    with csv_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {csv_path}")

    summary_path = OUT_DIR / "chelsa_summary.json"
    payload = {
        "source": "CHELSA v2.1 — 1981-2010 climatologies, 30-arcsec (~1 km) global",
        "mirror": "https://os.zhdk.cloud.switch.ch/chelsav2/GLOBAL/climatologies/1981-2010/bio/",
        "filename_template": "CHELSA_bio<N>_1981-2010_V.2.1.tif",
        "aoi_bounds": list(aoi_bounds()),
        "buffer_deg": AOI_BUFFER_DEG,
        "scale_offset_doc": "https://chelsa-climate.org/wp-admin/download-page/CHELSA_tech_specification_V2.pdf",
        "license": "CC-BY-4.0",
        "citation": "Karger, D.N. et al. (2017). Climatologies at high resolution for the earth's land surface areas. Scientific Data 4, 170122. doi:10.1038/sdata.2017.122",
        "vars": [
            {"n": n, "label": BIO_META[n][0], "scale": BIO_META[n][1],
             "offset": BIO_META[n][2], "unit": BIO_META[n][3],
             "description": BIO_META[n][4]}
            for n in BIO_META
        ],
        "aoi_summary": summary,
        "points": rows,
    }
    with summary_path.open("w") as fh:
        json.dump(payload, fh, indent=2)
    print(f"Wrote {summary_path}")

    print("\n=== Per-point bioclim (centroid + 4 corners + Wesley) ===")
    for r in rows:
        b1 = r.get("bio01_mean_annual_T")
        b12 = r.get("bio12_annual_precip")
        b15 = r.get("bio15_P_seasonality_CV")
        print(f"  {r['point']:12s}  T_annual={b1}°C  P_annual={b12}mm  P_CV={b15}%")

    print("\n=== AOI summary (5 km buffer) ===")
    for label, s in summary.items():
        if s is None:
            continue
        print(f"  {label:30s} mean={s['mean']:8.3f} {s['unit']:6s} "
              f"(p05={s['p05']:.2f}, p95={s['p95']:.2f}, n={s['pixels']})")


if __name__ == "__main__":
    main()
