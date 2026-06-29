# Penman-Monteith reference ET₀ — La Quebrada Viva parcel

Phase-0 §12 #17 v1.1 — closes the ET gap flagged in `climate_cube.md` v1.

Method: FAO-56 Penman-Monteith (Allen et al. 1998, Eq. 6). Daily inputs from
`nasa_power_daily.csv` 1990-01-01 → 2025-12-31 at lon -57.030, lat -25.630,
elevation 350 m. Wind: POWER WS10M converted to u₂ via FAO-56 log-profile
(Eq. 47) — POWER WS2M (≈0.38 m/s mean) reflects the ½° cell's mixed
forest+farmland roughness rather than the FAO-56 reference grass surface.

n_days computed: 13,149.  skipped rows: 0.

## Monthly climatology (mean of 36 years)

| Month | ET₀ mm/day | ET₀ mm/month | CHIRPS P mm/month | P − ET₀ mm/month |
| --- | ---: | ---: | ---: | ---: |
| Jan | 5.43 | 168.4 | 136.5 | -31.9 |
| Feb | 4.88 | 137.9 | 142.3 | +4.4 |
| Mar | 4.13 | 128.1 | 156.6 | +28.5 |
| Apr | 3.01 | 90.3 | 157.0 | +66.7 |
| May | 1.99 | 61.8 | 158.7 | +96.9 |
| Jun | 1.60 | 48.0 | 77.7 | +29.7 |
| Jul | 1.84 | 57.0 | 64.7 | +7.7 |
| Aug | 2.60 | 80.6 | 41.0 | -39.6 |
| Sep | 3.40 | 101.9 | 76.4 | -25.5 |
| Oct | 4.09 | 126.7 | 174.0 | +47.3 |
| Nov | 4.80 | 144.0 | 174.9 | +30.9 |
| Dec | 5.23 | 162.2 | 172.7 | +10.5 |
| **Annual** | — | **1307** | **1532** | **+226** |

## Annual ET₀ (full-year stations only)

- Mean: **1307 mm/yr** over 36 full years.
- Range: 1167 → 1471 mm/yr.

## Engineering hooks

- **Water-balance closure**: CHIRPS annual P − POWER annual ET₀ = 
  1532 − 1307 = **+226 mm/yr** surplus.
  Positive surplus → recharge + runoff supply the quebrada and any cistern overflow.
- **Driest-month gap**: August surplus = 
  41 − 81 = **-40 mm**.
  Negative or near-zero values size the cistern's August draw-down floor.
- **Irrigation demand cap** (worst-case dry-season days): the highest daily ET₀
  in the record is the irrigation system's instantaneous-capacity sizing target.
  Read `et0_daily.csv` and pick the 95th percentile of October-January days.

## Files

```
docs/site_data/nasa_power/penman_monteith_et0/
├── et0_daily.csv          (date, ET0_mm)
├── et0_monthly.csv        (year_month, ET0_mm_sum, n_days)
├── et0_climatology.json   (monthly + annual stats)
└── summary.md             (this file)
```

## Caveats

- POWER is ~½° (~50 km) — not parcel-scale. ET₀ here is a regional reference,
  not a parcel-microclimate value. The Cordillera ridge to the NE shades the
  parcel in late afternoon, slightly lowering real ET₀ vs this estimate.
- ET₀ is the **reference** ET (short-grass surface). For cob-roof living-sod or
  forested canopy actual ET, scale by crop coefficients (FAO-56 K_c) or pull
  MOD16A2 (queued, NASA Earthdata token available — AppEEARS auth still gated).
- WS10M-derived u₂ assumes the log profile holds over the POWER cell — a ~30%
  bias either way is plausible at this resolution. Sensitivity: a ±0.5 m/s
  swing in u₂ shifts annual ET₀ by ~80 mm.
- Daily POWER ALLSKY_SFC_SW_DWN is a 1981-onwards CERES-like product;
  pre-2000 values carry larger uncertainty (~10%).

## Cross-references

- Climate cube v1: `docs/site_data/climate_cube.md`
- POWER brochure: `docs/site_data/nasa_power/nasa_power_brochure.md`
- CHIRPS rainfall: `docs/site_data/chirps/chirps_summary.json`
