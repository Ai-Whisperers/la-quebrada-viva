#!/usr/bin/env python3
"""Phase-0 §12 #17 v1.1: FAO-56 Penman-Monteith reference evapotranspiration
ET₀ from NASA POWER daily 1990-2025 at the La Quebrada Viva parcel centroid.

Closes the largest remaining gap in `docs/site_data/climate_cube.md` v1:
ET₀ is the demand side of the water balance and the input the irrigation /
cistern / passive-cooling sizing all need. Uses the parcel's POWER daily
record on disk — no new fetch, no auth, no network.

Method: FAO Irrigation and Drainage Paper 56 (Allen et al. 1998), equation 6.
Inputs per day:
  - T2M_MAX, T2M_MIN, T2M  (°C)        from POWER
  - RH2M                   (%)         from POWER
  - WS10M → u₂             (m/s)       FAO-56 log profile (Eq. 47)
  - ALLSKY_SFC_SW_DWN → R_s (MJ/m²/d)  POWER kWh × 3.6
  - Latitude φ = -25.63°               parcel centroid
  - Elevation z = 350 m                parcel centroid (deck constant)

WS10M-derived u₂ is preferred over POWER's WS2M (=0.38 m/s mean) because
POWER's near-surface wind reflects the ½° cell's mixed forest+farmland
roughness, while FAO-56 assumes a short-grass reference surface — the
log-profile conversion from 10 m re-establishes that reference.

Outputs under docs/site_data/nasa_power/penman_monteith_et0/:
  - et0_daily.csv          date, ET0_mm
  - et0_monthly.csv        year_month, ET0_mm  (sum over month)
  - et0_climatology.json   monthly mean ET₀ + annual stats
  - summary.md             narrative + headline table for the cube
"""

from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs/site_data/nasa_power/nasa_power_daily.csv"
OUT = ROOT / "docs/site_data/nasa_power/penman_monteith_et0"
OUT.mkdir(parents=True, exist_ok=True)

LAT_DEG = -25.63
ELEV_M = 350.0
ALBEDO = 0.23
SIGMA = 4.903e-9  # MJ K^-4 m^-2 d^-1
G_SC = 0.0820     # MJ m^-2 min^-1


def sat_vp(t_c: float) -> float:
    return 0.6108 * math.exp(17.27 * t_c / (t_c + 237.3))


def u2_from_u10(u10: float) -> float:
    return u10 * 4.87 / math.log(67.8 * 10.0 - 5.42)


def day_of_year(yyyymmdd: str) -> int:
    d = date(int(yyyymmdd[:4]), int(yyyymmdd[4:6]), int(yyyymmdd[6:8]))
    return d.timetuple().tm_yday


def et0_fao56(t_max, t_min, t_mean, rh_mean, u10, rs_mj, j_doy):
    phi = math.radians(LAT_DEG)
    dr = 1.0 + 0.033 * math.cos(2.0 * math.pi * j_doy / 365.0)
    decl = 0.409 * math.sin(2.0 * math.pi * j_doy / 365.0 - 1.39)
    ws = math.acos(max(-1.0, min(1.0, -math.tan(phi) * math.tan(decl))))
    ra = (24.0 * 60.0 / math.pi) * G_SC * dr * (
        ws * math.sin(phi) * math.sin(decl)
        + math.cos(phi) * math.cos(decl) * math.sin(ws)
    )
    rso = (0.75 + 2e-5 * ELEV_M) * ra

    p = 101.3 * pow((293.0 - 0.0065 * ELEV_M) / 293.0, 5.26)
    gamma = 0.665e-3 * p
    es_tmax = sat_vp(t_max)
    es_tmin = sat_vp(t_min)
    es = (es_tmax + es_tmin) / 2.0
    ea = es * rh_mean / 100.0
    delta = 4098.0 * sat_vp(t_mean) / pow(t_mean + 237.3, 2)

    u2 = u2_from_u10(u10)
    rns = (1.0 - ALBEDO) * rs_mj
    rs_ratio = min(1.0, rs_mj / rso) if rso > 0 else 1.0
    tmax_k4 = pow(t_max + 273.16, 4)
    tmin_k4 = pow(t_min + 273.16, 4)
    rnl = SIGMA * (tmax_k4 + tmin_k4) / 2.0 * (0.34 - 0.14 * math.sqrt(max(0.0, ea))) * (1.35 * rs_ratio - 0.35)
    rn = rns - rnl

    num = 0.408 * delta * rn + gamma * (900.0 / (t_mean + 273.0)) * u2 * (es - ea)
    den = delta + gamma * (1.0 + 0.34 * u2)
    return num / den


def main() -> None:
    daily: list[tuple[str, float]] = []
    skipped = 0
    with SRC.open() as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            try:
                t_max = float(row["T2M_MAX"])
                t_min = float(row["T2M_MIN"])
                t_mean = float(row["T2M"])
                rh = float(row["RH2M"])
                u10 = float(row["WS10M"])
                rs_kwh = float(row["ALLSKY_SFC_SW_DWN"])
            except (ValueError, KeyError):
                skipped += 1
                continue
            rs_mj = rs_kwh * 3.6
            j = day_of_year(row["date"])
            et0 = et0_fao56(t_max, t_min, t_mean, rh, u10, rs_mj, j)
            daily.append((row["date"], et0))

    with (OUT / "et0_daily.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "ET0_mm"])
        for d, e in daily:
            w.writerow([d, f"{e:.4f}"])

    monthly_sum: dict[str, float] = defaultdict(float)
    monthly_n: dict[str, int] = defaultdict(int)
    annual_sum: dict[str, float] = defaultdict(float)
    annual_n: dict[str, int] = defaultdict(int)
    clim_sum = [0.0] * 12
    clim_days = [0] * 12

    for d, e in daily:
        ym = f"{d[:4]}-{d[4:6]}"
        y = d[:4]
        m = int(d[4:6]) - 1
        monthly_sum[ym] += e
        monthly_n[ym] += 1
        annual_sum[y] += e
        annual_n[y] += 1
        clim_sum[m] += e
        clim_days[m] += 1

    with (OUT / "et0_monthly.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year_month", "ET0_mm_sum", "n_days"])
        for ym in sorted(monthly_sum):
            w.writerow([ym, f"{monthly_sum[ym]:.2f}", monthly_n[ym]])

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    days_in_month = [31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    clim_mean_daily = [clim_sum[i] / clim_days[i] if clim_days[i] else 0.0 for i in range(12)]
    clim_monthly_total = [clim_mean_daily[i] * days_in_month[i] for i in range(12)]

    years_full = [y for y, n in annual_n.items() if n >= 360]
    annual_totals = sorted(annual_sum[y] for y in years_full)
    annual_mean = sum(annual_totals) / len(annual_totals) if annual_totals else 0.0

    clim = {
        "lat": LAT_DEG,
        "lon": -57.03,
        "elev_m": ELEV_M,
        "method": "FAO-56 Penman-Monteith (Allen et al. 1998, Eq. 6)",
        "wind_source": "POWER WS10M converted to u2 via FAO-56 log profile (Eq. 47)",
        "albedo": ALBEDO,
        "window": "1990-01-01 to 2025-12-31",
        "n_days": len(daily),
        "skipped_rows": skipped,
        "monthly_climatology_mm_per_day": {months[i]: round(clim_mean_daily[i], 3) for i in range(12)},
        "monthly_climatology_mm_per_month": {months[i]: round(clim_monthly_total[i], 1) for i in range(12)},
        "annual_mean_mm_per_year": round(annual_mean, 1),
        "annual_min_mm_per_year": round(annual_totals[0], 1) if annual_totals else None,
        "annual_max_mm_per_year": round(annual_totals[-1], 1) if annual_totals else None,
        "annual_n_years_full": len(years_full),
    }
    with (OUT / "et0_climatology.json").open("w") as f:
        json.dump(clim, f, indent=2)

    chirps_clim = [136.5, 142.3, 156.6, 157.0, 158.7, 77.7, 64.7, 41.0, 76.4, 174.0, 174.9, 172.7]
    surplus = [chirps_clim[i] - clim_monthly_total[i] for i in range(12)]
    chirps_annual = sum(chirps_clim)

    md_lines = [
        "# Penman-Monteith reference ET₀ — La Quebrada Viva parcel",
        "",
        "Phase-0 §12 #17 v1.1 — closes the ET gap flagged in `climate_cube.md` v1.",
        "",
        "Method: FAO-56 Penman-Monteith (Allen et al. 1998, Eq. 6). Daily inputs from",
        "`nasa_power_daily.csv` 1990-01-01 → 2025-12-31 at lon -57.030, lat -25.630,",
        "elevation 350 m. Wind: POWER WS10M converted to u₂ via FAO-56 log-profile",
        "(Eq. 47) — POWER WS2M (≈0.38 m/s mean) reflects the ½° cell's mixed",
        "forest+farmland roughness rather than the FAO-56 reference grass surface.",
        "",
        f"n_days computed: {len(daily):,}.  skipped rows: {skipped}.",
        "",
        "## Monthly climatology (mean of 36 years)",
        "",
        "| Month | ET₀ mm/day | ET₀ mm/month | CHIRPS P mm/month | P − ET₀ mm/month |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for i in range(12):
        md_lines.append(
            f"| {months[i]} | {clim_mean_daily[i]:.2f} | {clim_monthly_total[i]:.1f} | "
            f"{chirps_clim[i]:.1f} | {surplus[i]:+.1f} |"
        )
    annual_et0 = sum(clim_monthly_total)
    md_lines.extend([
        f"| **Annual** | — | **{annual_et0:.0f}** | **{chirps_annual:.0f}** | **{chirps_annual - annual_et0:+.0f}** |",
        "",
        "## Annual ET₀ (full-year stations only)",
        "",
        f"- Mean: **{annual_mean:.0f} mm/yr** over {len(years_full)} full years.",
        f"- Range: {clim['annual_min_mm_per_year']:.0f} → {clim['annual_max_mm_per_year']:.0f} mm/yr.",
        "",
        "## Engineering hooks",
        "",
        "- **Water-balance closure**: CHIRPS annual P − POWER annual ET₀ = ",
        f"  {chirps_annual:.0f} − {annual_et0:.0f} = **{chirps_annual - annual_et0:+.0f} mm/yr** surplus.",
        "  Positive surplus → recharge + runoff supply the quebrada and any cistern overflow.",
        "- **Driest-month gap**: August surplus = ",
        f"  {chirps_clim[7]:.0f} − {clim_monthly_total[7]:.0f} = **{surplus[7]:+.0f} mm**.",
        "  Negative or near-zero values size the cistern's August draw-down floor.",
        "- **Irrigation demand cap** (worst-case dry-season days): the highest daily ET₀",
        "  in the record is the irrigation system's instantaneous-capacity sizing target.",
        "  Read `et0_daily.csv` and pick the 95th percentile of October-January days.",
        "",
        "## Files",
        "",
        "```",
        "docs/site_data/nasa_power/penman_monteith_et0/",
        "├── et0_daily.csv          (date, ET0_mm)",
        "├── et0_monthly.csv        (year_month, ET0_mm_sum, n_days)",
        "├── et0_climatology.json   (monthly + annual stats)",
        "└── summary.md             (this file)",
        "```",
        "",
        "## Caveats",
        "",
        "- POWER is ~½° (~50 km) — not parcel-scale. ET₀ here is a regional reference,",
        "  not a parcel-microclimate value. The Cordillera ridge to the NE shades the",
        "  parcel in late afternoon, slightly lowering real ET₀ vs this estimate.",
        "- ET₀ is the **reference** ET (short-grass surface). For cob-roof living-sod or",
        "  forested canopy actual ET, scale by crop coefficients (FAO-56 K_c) or pull",
        "  MOD16A2 (queued, NASA Earthdata token available — AppEEARS auth still gated).",
        "- WS10M-derived u₂ assumes the log profile holds over the POWER cell — a ~30%",
        "  bias either way is plausible at this resolution. Sensitivity: a ±0.5 m/s",
        "  swing in u₂ shifts annual ET₀ by ~80 mm.",
        "- Daily POWER ALLSKY_SFC_SW_DWN is a 1981-onwards CERES-like product;",
        "  pre-2000 values carry larger uncertainty (~10%).",
        "",
        "## Cross-references",
        "",
        "- Climate cube v1: `docs/site_data/climate_cube.md`",
        "- POWER brochure: `docs/site_data/nasa_power/nasa_power_brochure.md`",
        "- CHIRPS rainfall: `docs/site_data/chirps/chirps_summary.json`",
    ])
    (OUT / "summary.md").write_text("\n".join(md_lines) + "\n")

    print(f"daily rows: {len(daily):,}  skipped: {skipped}")
    print(f"annual ET₀ (clim): {annual_et0:.0f} mm/yr")
    print(f"annual ET₀ (mean of full years): {annual_mean:.0f} mm/yr "
          f"[{clim['annual_min_mm_per_year']:.0f} → {clim['annual_max_mm_per_year']:.0f}]")
    print(f"surplus (CHIRPS P − ET₀): {chirps_annual - annual_et0:+.0f} mm/yr")
    for i, m in enumerate(months):
        print(f"  {m}: ET₀ {clim_mean_daily[i]:.2f} mm/d → {clim_monthly_total[i]:.0f} mm/mo  "
              f"(P {chirps_clim[i]:.0f}, surplus {surplus[i]:+.0f})")


if __name__ == "__main__":
    main()
