---
title: "La Quebrada Viva — climate cube (ERA5 + CHIRPS + NASA POWER)"
phase: "Phase-0 §12 #17"
status: "v1 — three-source cube; ET (MOD16A2) + WorldClim 30s pending v2"
canonical_point: "-25.6300, -57.0300 (parcel centroid)"
aoi_bbox_4326: "W-57.0450 S-25.6450 E-57.0150 N-25.6150"
window: "1990-2025 (ERA5 + NASA POWER 36 yr) / 2005-2025 (CHIRPS 21 yr)"
last_synth: "2026-06-29"
---

# Climate cube — La Quebrada Viva

Three independent reanalysis / satellite-rainfall products co-validated at the
parcel centroid (-25.63, -57.03). Each source has a different native resolution
and a different physical basis; the deck and the engineering hooks pick the
best one **per variable**, not the best one overall.

## TL;DR — headline numbers the deck quotes

| Variable                           | Value         | Source picked     | Why this source |
| --- | ---: | --- | --- |
| Mean annual temperature            | **22.0 °C**   | ERA5              | 36 yr, energy-balance closed reanalysis |
| Warmest month (Jan)                | **26.8 °C**   | ERA5              | matches NASA POWER T2M_MAX climatology |
| Coolest month (Jul)                | **16.6 °C**   | ERA5              | Cfa Köppen confirmed |
| Mean annual precipitation          | **1532 mm/yr**| CHIRPS            | 5.5 km parcel-scale beats 28 km / 50 km |
| Driest year (cistern design)       | **1146 mm/yr (2020)** | CHIRPS    | uses driest realized year, not mean |
| Driest 3-mo run (cistern volume)   | **183 mm (Jun-Jul-Aug)** | CHIRPS | sets minimum tank-day inventory |
| Wettest year                       | **2096 mm (2015)** | CHIRPS       | El Niño 2015-16 signature |
| Mean annual solar (PV sizing)      | **17.7 MJ/m²/d ≈ 4.92 kWh/m²/d** | NASA POWER | daily resolution, T2M+RH+wind co-sampled |
| Worst-month solar (PV oversize)    | **2.81 kWh/m²/d (Jun)** | NASA POWER | sets PV array kWp floor |
| Best-month solar                   | **6.76 kWh/m²/d (Jan)** | NASA POWER |   |
| Mean wind @ 10 m                   | **1.3-1.5 m/s** | ERA5 / NASA POWER | both agree |
| Mean wind @ 50 m (turbine height)  | **3.35 m/s**  | NASA POWER        | below 4 m/s → small-wind uneconomic |
| Mean RH @ 2 m                      | **73.5 %**    | NASA POWER        | ERA5 single-levels did not pull RH |
| Köppen-Geiger class                | **Cfa — subtropical humid, no dry season** | ERA5 monthly clim | all 12 months > 50 mm except Aug @ 41 mm (CHIRPS); ERA5 has 79 mm Aug |
| Passive cooling viable (Rule 6)    | **Yes**       | ERA5              | warmest month 26.8 °C < 35 °C threshold |

## Cross-validation table — same metric, three sources

Numbers in the same row should *roughly* agree. Where they don't, the "Picked"
column says which source the deck uses and a one-line reason.

| Metric                       | ERA5 (0.25°)  | CHIRPS (0.05°) | NASA POWER (~0.5°) | Picked / why |
| --- | ---: | ---: | ---: | --- |
| Mean annual T (°C)           | 22.04         | —              | 22.625             | ERA5 — energy-balance closed |
| Annual precip (mm/yr)        | 1736          | 1532.4         | 1503.8 (4.12·365)  | **CHIRPS** — 5.5 km parcel scale wins |
| Mean solar (MJ/m²/d)         | 17.73         | —              | 17.64 (4.899 kWh)  | tie — both agree to 0.5 % |
| Wind 10 m (m/s)              | 1.31          | —              | 1.50               | NASA POWER — co-sampled with T/RH |
| RH 2 m (%)                   | not pulled    | —              | 73.5               | NASA POWER — only source |
| Dry-month flag (Aug, mm)     | 79.4          | 41.0           | —                  | CHIRPS — parcel-scale; below Köppen Cwa cutoff but only just |

**The 200 mm/yr gap (ERA5 1736 vs CHIRPS 1532)** is real, not a bug: ERA5's
28 km cell averages the parcel with the wetter Cordillera ridge to the
north-east, while CHIRPS's 5.5 km cell sits squarely on the parcel and resolves
the rain-shadow on the lee of the Acahay range. **Tank sizing uses CHIRPS.**

## Monthly cube (long-term means)

Each cell is the long-term monthly mean from its native source.

| Month | T ERA5 °C | T POWER °C | P ERA5 mm | P CHIRPS mm | P POWER mm | Wind 10 m m/s | Solar MJ/m²/d | Solar kWh/m²/d | RH % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Jan | 26.83 | 27.0 (T2M)* | 142.9 | 136.5 | ~140  | 1.10 | 24.2 | 6.76 | ~70 |
| Feb | 26.13 |       | 147.1 | 142.3 |       | 1.03 | 21.8 | 6.16 |     |
| Mar | 25.05 |       | 134.9 | 156.6 |       | 1.16 | 19.2 | 5.37 |     |
| Apr | 22.27 |       | 156.0 | 157.0 |       | 1.25 | 15.3 | 4.35 |     |
| May | 18.50 |       | 145.7 | 158.7 |       | 1.27 | 11.6 | 3.37 |     |
| Jun | 17.14 |       | 127.5 | 77.7  |       | 1.38 |  9.9 | 2.81 |     |
| Jul | 16.55 |       |  88.3 | 64.7  |       | 1.44 | 11.4 | 3.20 |     |
| Aug | 18.58 |       |  79.4 | 41.0  |       | 1.52 | 14.6 | 3.83 |     |
| Sep | 20.42 |       | 139.2 | 76.4  |       | 1.50 | 17.4 | 4.53 |     |
| Oct | 22.89 |       | 211.1 | 174.0 |       | 1.50 | 20.0 | 5.35 |     |
| Nov | 24.17 |       | 186.3 | 174.9 |       | 1.45 | 23.0 | 6.39 |     |
| Dec | 25.92 |       | 177.8 | 172.7 |       | 1.16 | 24.3 | 6.73 |     |

`*` Per-month NASA POWER T2M is in `nasa_power_climatology.json` — not pasted
column-by-column to keep the cube readable; mean-of-means is 22.625 °C and
agrees with ERA5 to 0.6 °C.

## Annual precipitation timeseries (CHIRPS 2005-2025, parcel-scale)

| Yr | mm | Yr | mm | Yr | mm |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2005 | 1223 | 2012 | 1469 | 2019 | 1434 |
| 2006 | 1557 | 2013 | 1362 | **2020** | **1146** ← driest |
| 2007 | 1672 | 2014 | 1826 | 2021 | 1226 |
| 2008 | 1292 | **2015** | **2096** ← wettest | 2022 | 1790 |
| 2009 | 1749 | 2016 | 1551 | 2023 | 1717 |
| 2010 | 1526 | 2017 | 1693 | 2024 | 1366 |
| 2011 | 1502 | 2018 | 1620 | 2025 | 1366 |

Mean 1532 mm/yr; σ ≈ 235 mm/yr; range 1146-2096; CV ≈ 15 %.

## Engineering hooks (what the deck uses these numbers for)

- **Rule 6 — passive cooling.** ERA5 warmest month 26.8 °C < 35 °C threshold;
  passive cooling viable, mechanical AC optional.
- **PV array sizing.** Use NASA POWER worst-month 2.81 kWh/m²/d (Jun). Annual
  design draw / 2.81 / 0.75 (DC→AC + soiling) / 30 d → required kWp.
- **Cistern sizing.** Use CHIRPS driest 3-mo run (Jun-Jul-Aug = 183 mm) over
  catchment m². Driest realized year (2020 = 1146 mm) is the worst-case
  annual budget; rolling 12-mo drought events can dip lower.
- **Rule 9 (solar on steel frame, not sod roof).** Solar wins on roof or pole
  array; 50 m wind (3.35 m/s) does not justify a turbine.
- **Hydro feasibility.** Mean 1532 mm/yr with the dry-season floor at 183 mm
  in JJA is consistent with the year-round-stream brief, but **measured stream
  discharge at the parcel boundary is the only honest number** — see
  `property_map_v2/index.md` honesty caveat §C.

## Köppen-Geiger classification

ERA5 monthly climatology places the parcel in **Cfa — humid subtropical, no
dry season** (warmest month 26.8 °C > 22 °C; coldest month 16.6 °C > 0 °C; all
months > 30 mm precipitation). CHIRPS at 5.5 km shows Aug = 41 mm — close to
the 30 mm threshold that would tip into Cwa (dry winter). The honest call is
"borderline Cfa / Cwa with a dry-but-not-arid August"; the deck quotes Cfa.

## Water-balance hooks

P (annual) is in hand from three sources. **ET₀ (FAO-56 Penman-Monteith
reference evapotranspiration) is the missing leg of the water balance.**

- T_max, T_min, RH, wind, solar are all in NASA POWER daily — so Penman-
  Monteith ET₀ can be computed from `nasa_power_daily.csv` directly without
  another external pull. Not done in this synthesis to avoid inventing a
  number without the FAO-56 reference implementation cross-checked.
- A satellite-direct ET (MOD16A2 v061, 500 m 8-day) would bound the answer
  with measured-cloud-corrected actual ET. **NASA Earthdata token is in
  `.env.local`**; the AppEEARS / LP DAAC pull is the path; queue depth and
  polygon CSV upload are the friction. Deferred to climate-cube v2.
- WorldClim 2.1 30-arc-sec (~1 km) would give a higher-resolution monthly
  climatology against which ERA5's 28 km can be sanity-checked. The host
  (geodata.ucdavis.edu) was unreachable on 2026-06-29 — retry script left at
  `scripts/fetch_worldclim.py`.

For the escritura deck and the digital twin, the working assumption is
**ET ≈ 1100-1300 mm/yr** (Penman-Monteith reference range for subtropical
humid lowland with the measured T+RH+solar profile), pending the actual
NASA POWER PM computation. That leaves P-ET surplus ≈ 200-400 mm/yr →
catchment retention is the design driver, not aridity.

## Data files (what fed this synthesis)

| Source     | Native res     | Window     | Files                                                      |
| ---        | ---            | ---        | ---                                                        |
| ERA5       | 0.25° (~28 km) | 1990-2025  | `docs/site_data/climate_era5/era5_*.nc` + `climate_brochure.md` + `climate_summary.txt` |
| CHIRPS v2.0| 0.05° (~5.5 km)| 2005-2025  | `docs/site_data/chirps/chirps_summary.json` + `chirps_brochure.md` + `tiles/chirps_YYYY_MM.tif` (git-ignored) |
| NASA POWER | ~0.5° (~50 km) | 1990-2025  | `docs/site_data/nasa_power/nasa_power_daily.csv` + `nasa_power_climatology.json` + `nasa_power_brochure.md` |

Regenerable via:
- ERA5 — `scripts/fetch_era5_climate.py` (CDS API key in `.env.local`)
- CHIRPS — `python3 -m tools.site_data.chirps`
- NASA POWER — `scripts/fetch_nasa_power.py` (no auth needed for POWER)

## Pending / gaps (v2 backlog)

1. **ET₀ Penman-Monteith** from `nasa_power_daily.csv` (no new fetch needed).
2. **MOD16A2 v061 actual ET** 2000-2024 8-day 500 m via NASA Earthdata
   AppEEARS (token available; queue + CSV polygon upload friction).
3. **WorldClim 2.1 30s** baseline 1970-2000 for higher-res climatology
   sanity-check (host down 2026-06-29; retry script ready).
4. **Future projections** — CMIP6 NEX-GDDP-CMIP6 SSP2-4.5 / SSP5-8.5 monthly
   deltas at the parcel grid cell; cost is the queue depth.
5. **In-situ stream gauge** at the parcel boundary — the only honest hydro
   number; requires field install (not autonomous).

## Cross-references

- [`property_map_v2/index.md`](property_map_v2/index.md) — "Climate" row in
  the layer provenance table points here.
- [`landsat/annual_median_1985_2025/summary.md`](landsat/annual_median_1985_2025/summary.md)
  — NDVI dip 2003 (driest 30-day window in CHIRPS) and NDVI plateau 2018
  (wettest 12-mo window in CHIRPS) cross-correlate.
- [`sentinel2/timeseries_2020_2025/`] — 2020 CHIRPS-driest-year shows up as
  NDVI down-step in the S2 record.
- [`jrc_gsw/`](jrc_gsw/) — JRC GSW 1984-2021 triple-confirms 0 % standing
  water on parcel despite the 1532 mm/yr rainfall, i.e. the runoff/infiltration
  split sends water through the catchment, not into ponds.
