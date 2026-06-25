"""NASA POWER daily point query for the parcel center.

POWER (Prediction Of Worldwide Energy Resources) is free, no auth.
ERA5 already covers most of these vars at ~28 km — POWER's value here is
(a) ~50 km nearest-grid-cell at the parcel point, and (b) the engineering
deck wants a one-row-per-day CSV, which POWER ships natively.

API:  https://power.larc.nasa.gov/api/temporal/daily/point
Docs: https://power.larc.nasa.gov/docs/services/api/temporal/daily/

Run:
    python3 -m tools.site_data.nasa_power
"""
from __future__ import annotations

import csv
import datetime as dt
import statistics
from pathlib import Path

from .common import http_get, out_dir, parcel_center, write_json

ENDPOINT = "https://power.larc.nasa.gov/api/temporal/daily/point"

PARAMETERS = [
    "ALLSKY_SFC_SW_DWN",   # solar irradiance, kWh/m²/day
    "ALLSKY_KT",           # clearness index
    "T2M",                 # air temp at 2 m, °C
    "T2M_MAX",
    "T2M_MIN",
    "RH2M",                # relative humidity, %
    "WS2M",                # wind speed at 2 m, m/s
    "WS10M",
    "WS50M",
    "PRECTOTCORR",         # bias-corrected precip, mm/day
]

# Single 36-year window. POWER returns data through ~2 days before today.
START = "19900101"
END = "20251231"


def fetch(lon: float, lat: float) -> dict:
    params = {
        "parameters": ",".join(PARAMETERS),
        "community": "RE",   # renewable-energy community → calibrated for power calcs
        "longitude": f"{lon:.4f}",
        "latitude": f"{lat:.4f}",
        "start": START,
        "end": END,
        "format": "JSON",
    }
    r = http_get(ENDPOINT, params=params, timeout=180)
    return r.json()


def to_csv(payload: dict, out_csv: Path) -> int:
    """Pivot POWER's per-variable date dicts into one CSV row per day."""
    params = payload["properties"]["parameter"]
    dates = sorted(next(iter(params.values())).keys())
    rows = []
    for d in dates:
        row = {"date": d}
        for p in PARAMETERS:
            v = params[p].get(d)
            # POWER fills missing with -999. Skip but record.
            row[p] = "" if v is None or v <= -900 else v
        rows.append(row)
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date", *PARAMETERS])
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def climatology(payload: dict) -> dict:
    """Long-term mean / min / max per variable, for the brochure."""
    params = payload["properties"]["parameter"]
    out: dict[str, dict[str, float]] = {}
    for p, by_date in params.items():
        vals = [v for v in by_date.values() if v is not None and v > -900]
        if not vals:
            continue
        out[p] = {
            "mean": round(statistics.fmean(vals), 3),
            "min": round(min(vals), 3),
            "max": round(max(vals), 3),
            "n_days": len(vals),
        }
    return out


def monthly_solar(payload: dict) -> list[tuple[int, float]]:
    """Mean monthly solar (kWh/m²/day) → PV sizing input."""
    sw = payload["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
    buckets: dict[int, list[float]] = {m: [] for m in range(1, 13)}
    for date_str, v in sw.items():
        if v is None or v <= -900:
            continue
        month = int(date_str[4:6])
        buckets[month].append(v)
    return [(m, round(statistics.fmean(vs), 3)) for m, vs in buckets.items() if vs]


def write_brochure(out: Path, clim: dict, monthly: list[tuple[int, float]],
                   lon: float, lat: float) -> None:
    months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    lines = [
        "# NASA POWER daily climatology — La Quebrada Viva parcel",
        "",
        "Source: NASA POWER (https://power.larc.nasa.gov), US public domain  ",
        f"Point: lon={lon:.5f}, lat={lat:.5f} (nearest grid cell ~½°)  ",
        f"Window: {START}–{END}  ",
        f"Pulled: {dt.datetime.now(dt.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "",
        "## Long-term means (engineering-deck headline)",
        "",
        "| Variable | Mean | Min | Max | N days |",
        "| --- | ---:| ---:| ---:| ---:|",
    ]
    for p in PARAMETERS:
        c = clim.get(p)
        if not c:
            continue
        lines.append(f"| {p} | {c['mean']} | {c['min']} | {c['max']} | {c['n_days']} |")
    lines += [
        "",
        "## Monthly mean solar (ALLSKY_SFC_SW_DWN, kWh/m²/day) — PV sizing",
        "",
        "| Month | kWh/m²/day |",
        "| --- | ---:|",
    ]
    for m, v in monthly:
        lines.append(f"| {months[m]} | {v} |")
    worst = min(monthly, key=lambda kv: kv[1])
    best = max(monthly, key=lambda kv: kv[1])
    lines += [
        "",
        "## Interpretation hooks",
        "",
        f"- Worst-month solar: {months[worst[0]]} at {worst[1]} kWh/m²/day"
        " → size PV array against this.",
        f"- Best-month solar:  {months[best[0]]} at {best[1]} kWh/m²/day.",
        "- T2M_MAX mean above 32 °C → passive cooling design (Rule 6) is non-optional.",
        "- WS50M mean below 4 m/s → small wind is unlikely to beat PV economically.",
        "- Cross-check PRECTOTCORR against CHIRPS (5 km) before tank sizing.",
        "",
        "Raw daily series: `nasa_power_daily.csv` (one row per day).",
    ]
    out.write_text("\n".join(lines))


def main() -> None:
    lon, lat = parcel_center()
    out = out_dir("nasa_power")
    print(f"[nasa_power] querying lon={lon:.5f}, lat={lat:.5f}, {START}-{END}")
    payload = fetch(lon, lat)
    write_json(out / "nasa_power_raw.json", payload)
    n = to_csv(payload, out / "nasa_power_daily.csv")
    clim = climatology(payload)
    write_json(out / "nasa_power_climatology.json", clim)
    monthly = monthly_solar(payload)
    write_brochure(out / "nasa_power_brochure.md", clim, monthly, lon, lat)
    summary_lines = [
        f"NASA POWER daily {START}-{END}, n_days={n}",
        f"T2M mean: {clim['T2M']['mean']} °C",
        f"PRECTOTCORR mean: {clim['PRECTOTCORR']['mean']} mm/day",
        f"ALLSKY_SFC_SW_DWN mean: {clim['ALLSKY_SFC_SW_DWN']['mean']} kWh/m²/day",
        f"WS50M mean: {clim['WS50M']['mean']} m/s",
    ]
    (out / "nasa_power_summary.txt").write_text("\n".join(summary_lines) + "\n")
    print(f"[nasa_power] wrote {out}")


if __name__ == "__main__":
    main()
