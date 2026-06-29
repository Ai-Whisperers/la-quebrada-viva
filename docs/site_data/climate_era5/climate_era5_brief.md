# ERA5 reanalysis climate brief — La Quebrada Viva (Phase-0 §12 v1)

_Pulled 2026-06-11 (re-synthesized 2026-06-29) from ECMWF ERA5 single-levels monthly means via Copernicus C3S CDS, 1990-01 → 2025-12 (36 yr, 432 monthly samples). 0.25° grid (~31 km), nearest cell (-25.75, -57.0) ~12 km NE of parcel centroid (-25.6073, -57.0355). Four variables ingested as NetCDF: 2 m air temperature (`t2m`), total precipitation (`tp`), 10 m wind vectors (`u10`, `v10`), surface solar radiation downward (`ssrd`). Note: this is the **structural climate envelope** — 31 km grid blurs the parcel-scale gradients that show up in [[mod16_brief]] / [[chelsa_brief]] / [[canopy_height_brief]]; ERA5's role here is the long-baseline (1990 onward) trend + extreme value reference._

## Headline

- **Mean annual climate 22.0 °C / 1736 mm / 1.31 m/s / 17.7 MJ/m²/day** — Köppen Cfa subtropical-humid. Warmest month Jan 26.8 °C, coolest Jul 16.6 °C, no dry month (driest Aug = 79 mm > 50 mm threshold). **Passive cooling viable (Rule 6)**: monthly mean never crosses the 35 °C envelope.
- **+0.25 °C / decade warming** (OLS 1990-2025, n=36): 1990s mean 21.7 °C → 2020s 22.45 °C, **+0.75 °C in 35 years**. Consistent with global ~1.5× over land. The Jan peak month is warming faster than the annual mean (anecdotal — 2022-01 hit 29.5 °C, the hottest single month in the 432-sample record).
- **Prevailing wind 71 % from the E quadrant** (ESE 28 % + E 25 % + ENE 18 % of monthly mean direction tally), mean 1.31 m/s. Light easterly trade-wind regime year-round, windiest in JJA (1.5 m/s). Engineering implication: **orient corredor (Rule 8) on the E ↔ W axis, openings on the east face** for the trade-wind cross-ventilation.
- **2022 triple-La-Niña drought visible as 2nd-driest year in the 36-yr record** (P_2022 ≈ 1317 mm vs 36-yr mean 1736 mm = **−24 %**) coupled with the **highest annual SSRD on record** (19.1 vs 17.7 MJ/m²/day) — drought + cloud-free skies + January heat dome (29.5 °C peak). This matches the [[mod16_brief]] 2022 ET trough (−18 %) and the [[landsat_brief]] NDVI floor (0.747 — leaves stayed on but stomata closed).
- **2024-25 the wettest sub-decade** (P_2024 ≈ 2509 mm, the wettest year in the record) — post-drought relaxation. Cistern + spillway sizing should use the **2509 mm wet upper bound** AND the **1172 mm dry lower bound** (the 1995 minimum) as joint design envelopes.
- **Slight precip drying −6 mm / decade** (OLS 1990-2025) is **not statistically distinguishable from interannual noise** (σ ≈ 340 mm/yr); the climate has warmed but not (yet) dried at this site.

## Per-variable structural numbers (1990-2025, 36 yr)

| Variable | Mean | Min | Max | Std (interann.) | Decadal trend | Note |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| **T 2 m air (°C)** | 22.04 | 21.09 (1995) | 23.03 (2023) | 0.51 | **+0.25 °C/dec** | warming |
| **P annual (mm)** | 1736 | 1172 (1995) | 2509 (2024) | ~340 | −6 mm/dec (n.s.) | wide ±20 % spread |
| **Wind 10 m (m/s)** | 1.31 | 0.40 (calm month) | 2.62 (2017-07) | 0.36 | flat | light regime |
| **SSRD (MJ/m²/day)** | 17.7 | 7.75 (Jun winter) | 28.7 (Dec peak) | 5.18 (intra-yr) | flat | strong seasonal cycle |

_Monthly time-series in `era5_*.nc` (4 files); aggregated annual + monthly climatology in `climate_summary.txt`; marketing pull-quotes in `climate_brochure.md`._

## Monthly climatology (1990-2025 means)

| Month | T (°C) | P (mm) | Wind (m/s) | Solar (MJ/m²/day) | Role |
| --- | ---: | ---: | ---: | ---: | --- |
| Jan | 26.8 | 143 | 1.10 | 24.2 | hottest, sub-35 °C |
| Feb | 26.1 | 147 | 1.03 | 21.8 | summer |
| Mar | 25.0 | 135 | 1.16 | 19.2 | wet transition |
| Apr | 22.3 | 156 | 1.25 | 15.3 | comfort zone |
| May | 18.5 | 146 | 1.27 | 11.6 | cool wet |
| Jun | 17.1 | 127 | 1.38 | 9.9 | winter low solar |
| **Jul** | **16.6** | **88** | **1.44** | 11.4 | **coldest, driest qtr** |
| Aug | 18.6 | 79 | 1.52 | 14.6 | dry, **windiest** |
| Sep | 20.4 | 139 | 1.50 | 17.4 | spring |
| Oct | 22.9 | 211 | 1.50 | 20.0 | **wettest** |
| Nov | 24.2 | 186 | 1.45 | 23.0 | wet warm |
| **Dec** | 25.9 | 178 | 1.16 | **24.3** | **peak solar** |

## Decadal evolution (sub-baseline structural drift)

| Decade | T_mean (°C) | P_annual (mm) | Wind (m/s) | Note |
| --- | ---: | ---: | ---: | --- |
| 1990-1999 | 21.70 | 2035 | 1.26 | baseline |
| 2000-2009 | 22.00 | 1624 | 1.32 | drier swing |
| 2010-2019 | 22.16 | 1663 | 1.35 | recovery |
| 2020-2025 (6 yr) | 22.45 | ~1755 | 1.34 | hottest, post-drought wet rebound |

**Net 1990s → 2020s: +0.75 °C warming, ~−14 % precip (but driven by 2000s drought spell, not a monotonic trend).** Wind, surprisingly, +0.08 m/s — verandah cross-flow will remain light.

## Extremes (single-month records, 1990-2025)

| Record | Value | When | Engineering significance |
| --- | ---: | --- | --- |
| Hottest month | **29.5 °C** | 2022-01 | Jan-heat-dome event during triple-La-Niña → sets PV inverter derating + AC peak load |
| Coldest month | 12.6 °C | 2000-07 | sets minimum design indoor T for orchid greenhouse / cassava store |
| Windiest month | 2.6 m/s | 2017-07 | structural wind load remains low (Beaufort 2); no special bracing |
| Wettest year | **2509 mm** | 2024 | upper bound — spillway + drainage sizing |
| Driest year | **1172 mm** | 1995 | lower bound — cistern + irrigation backup sizing |
| Drought year | 1317 mm + SSRD 19.1 | 2022 | joint deficit (rain ↓ + sun ↑) — worst case for crop + canopy stress |

## Cross-check with the climate stack

| Source | T_mean | P_annual | Period | Scale | Note |
| --- | ---: | ---: | --- | --- | --- |
| **ERA5 (this brief)** | 22.04 °C | 1736 mm | 1990-2025 | 31 km | structural envelope |
| **[[chelsa_brief]] CHELSA v2.1** | ~21.6 °C | 1545-1760 (NE→SW) | 1981-2010 | 1 km | resolves intra-parcel gradient ERA5 cannot |
| **[[mod16_brief]] MOD16 actual ET** | — | 1091 mm/yr ET | 2021-2024 | 500 m | confirms 55 % ET/PET ratio under 1736 mm rain |
| **NASA POWER (Penman ET₀)** | ~22 °C | ~1700-1900 ET₀ | 1981-2024 | 0.5° | matches ERA5 T within 0.4 °C |
| **[[canopy_height_brief]] Meta CHM** | n/a | n/a | 2023 snapshot | 1 m | gradient amplified at parcel scale |

**Three-source convergence on the 22 °C / 1700 mm baseline** is tight. ERA5 supplies the 36-yr trend + extreme values; CHELSA + MOD16 supply the intra-parcel spatial structure ERA5's 31 km grid washes out.

## Wind direction structure (for verandah orientation)

Decomposed monthly mean wind vector (1990-2025):
- **E sector (ENE+E+ESE)** : 71 % of monthly samples (309/432)
- SE+NE sectors: 24 % (102/432)
- S+W+N sectors: < 5 % combined

**Engineering call:** corredor + main openings on the **east elevation**, leeward (W) terrace for evening shade. This matches the cultural Paraguayan typology (Rule 8) — corredor faces the patio, patio faces east, prevailing breeze flushes the corredor mid-afternoon. NO need to over-engineer for storm winds (max recorded monthly mean = 2.6 m/s = Beaufort 2; daily peak gusts are a Phase-1 hourly-data task).

## Engineering / design implications

### Rule 6 — Passive cooling envelope (≤ 35 °C)
- Warmest monthly mean **26.8 °C (Jan)**, all-time monthly max **29.5 °C (2022-01)**. Diurnal peak (not in monthly means) probably reaches **38-40 °C** on heat-dome days — confirm with NASA POWER hourly. Passive design + thermal mass + cross-ventilation handles 95 % of summers; AC sized to **clip the 5 % heat-dome days** (the 2022-01 envelope), not run continuously.
- LWR night-sky cooling viable Jun-Aug: monthly mean 16.6-18.6 °C → no heating needed, sleep is comfortable with mass + a wool blanket.

### Rule 7 — Micro-hydro flow budget
- ERA5 annual P 1736 mm − MOD16 ET 1091 mm = **645 mm/yr surplus** → matches the [[mod16_brief]] residual (685 mm) within 6 % (P source diff = CHELSA 1656 vs ERA5 1736).
- **Quebrada baseflow design**: drought-year residual = ERA5 P_1995 1172 mm − ET assumed 950 mm (drought-suppressed) ≈ 220 mm/yr surplus → minimum baseflow for the 62 ha catchment = 220 mm × 620000 m² / 365 days ≈ **3.7 L/s**. Size the micro-hydro nozzle to that floor, not the average.

### Rule 9 — PV sizing
- Dec SSRD **24.3 MJ/m²/day = 6.75 kWh/m²/day** (peak month). Annual mean **17.7 MJ/m²/day = 4.92 kWh/m²/day**.
- 4.5 kWp rooftop array (brochure) at 80 % system efficiency → 4.5 × 4.92 × 0.8 × 365 ≈ **6470 kWh/yr** annual energy. Sufficient for the household + EV charging budget the deck assumes.
- **2022 SSRD was the highest on record (19.1 MJ/m²/day)** → drought years also happen to be the highest-yield PV years (cloud-free sky). This is a positive correlation for energy-independence narrative.

### Rule 8 — Cultural-Paraguayan typology
- Trade-wind regime (E 71 %) is the structural justification for the corredor-on-east footprint. Already aligned with the patio-house + galpón cardinal layout; reinforces the design rather than challenging it.

### Sub-render typology mapping
- `lqv/subscene/climate_envelope.py` — 12-month bar chart panel (T + P bars + SSRD line + wind rose inset) for the deck "structural climate" section. Replaces the placeholder graphic in escritura deck v6.
- `lqv/subscene/wind_rose.py` — polar plot, ESE 28 % / E 25 % / ENE 18 % wedges, scaled by mean speed. Drives the verandah-orientation justification page.
- `lqv/subscene/heat_dome_2022.py` — focused panel on the 2022-01 heat dome (29.5 °C monthly mean), cross-cut with [[mod16_brief]] ET trough and [[landsat_brief]] NDVI plateau — the "resilience under climate stress" narrative.
- `lqv/subscene/pv_yield.py` — monthly SSRD × 4.5 kWp generation curve vs household load, shows energy independence margin. Pairs with the wallet card.

## Provenance

- **ECMWF ERA5 reanalysis** (open access via Copernicus C3S license): `reanalysis-era5-single-levels-monthly-means` collection; variables `2m_temperature`, `total_precipitation`, `10m_u_component_of_wind`, `10m_v_component_of_wind`, `surface_solar_radiation_downward`. 432 monthly samples (1990-01-01 → 2025-12-01), 5×5 lat/lon subset over `[-26.0, -25.0] × [-57.5, -56.5]`, nearest grid (-25.75, -57.0). GRIB → NetCDF via `cfgrib-0.9.1` 2026-06-11.
- **Citation:** Hersbach H. et al. (2020). _The ERA5 global reanalysis_. Q. J. R. Meteorol. Soc. 146:1999-2049. doi:10.1002/qj.3803.
- Pipeline: `scripts/fetch_era5_climate.py` → 4 NetCDFs + `climate_brochure.md` + `climate_summary.txt`. Re-synthesis 2026-06-29 read NetCDFs via `xarray + cfgrib`, computed annual aggregates, OLS trends, monthly extremes, wind-direction histograms.

## Carry-forward gaps (deferred)

- **Hourly diurnal cycle** — ERA5 hourly (vs monthly-mean used here) would give the actual heat-dome peak temperature (likely 38-40 °C) for AC sizing. ~150 GB pull for 36 yr; defer to Phase-1 with cohort filter (only DJF heat-dome candidate days).
- **Return-period extreme-value statistics** — Gumbel / GEV fit on the 36 annual maxima would give the 100-yr return-period rainfall + heat for civil + structural engineering. Tractable from existing monthly data; queue as a separate notebook.
- **ERA5-Land cross-validation** (9 km, land-surface specialized) — would give a partial 31 km vs 9 km comparison. Skip — MOD16/CHELSA/CHM already resolve sub-parcel structure better than ERA5-Land would.
- **CHIRPS daily precip** ([[chirps_brief]]) — 0.05° daily rain log, already pulled in `_cache/`. Will give daily extreme statistics ERA5 monthly cannot.
- **CMIP6 NEX-GDDP projections** ([[cmip6_brief]] — in progress, PID 457341, 224/450 cache files) — will let us project ERA5's +0.25 °C/decade trend forward to 2050/2100 under SSP2-4.5 / SSP5-8.5. Carry-forward link until that brief lands.
- **MOD11A2 LST cross-check** ([[mod11_brief]] — in progress, PID 519852 at 225/459 granules ≈ 49 %) — will give surface (not 2 m air) temperature, which is what the building skin actually sees.
- **Cross-link to [[landsat_brief]]** for the climate-vegetation coupling: 2022 hot + dry + sunny = ET trough + NDVI plateau (isohydric stomatal closure). Already cited.
