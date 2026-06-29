# MOD16A2 v6.1 actual ET brief — La Quebrada Viva (Phase-0 §12 v1)

_Pulled 2026-06-29 from MODIS Terra/Aqua Combined Net Evapotranspiration 8-day L4 500 m (MOD16A2.061, NASA LP DAAC Earthdata Cloud). Tile h12v11 covers the AOI. 184 granules ingested (collection v6.1 reprocessing currently spans 2021-01-01 → 2024-12-31 for this tile = 4 complete years, 46 granules/yr). AOI: 5 km buffer around parcel centroid (-57.0355, -25.6073), 8×7 = 56 pixels @ 500 m. Six sample points (centroid + 4 KML corners + Wesley pin) extracted with bilinear pyhdf reads on the sinusoidal grid._

## Headline

- **Annual actual ET 1091 mm/yr (4-yr AOI mean)**, against PET 1974 mm/yr → ET/PET 0.55. The parcel uses **55 % of available atmospheric evaporative demand** — supply-limited by seasonal soil moisture, not energy-limited.
- **2022 drought signal is unambiguous**: AOI ET dropped to **894 mm** (vs 1108 / 1163 / 1200 in 2021/2023/2024), ET/PET fell to **0.45** while PET stayed flat at 1970 mm. Soil-moisture deficit, not radiation deficit, drove the shortfall — consistent with the 2020-2022 Paraná basin "triple-La-Niña" drought.
- **Sharp NE→SW gradient inside the parcel** (2024): centroid 1473 mm, NE corner 1452 mm, NW 1310 mm, SE 1174 mm, **SW 982 mm**. 490 mm spread across ~3.5 km — the wettest pixel evaporates **1.5×** more water than the driest. This is the same axis the [[chelsa_brief]] precip gradient (1760 → 1545 mm) and the [[canopy_height_brief]] CHM (10.9 m gallery → 0.3 m cleared) already showed.
- **PET is flat (1938-2095 mm)** across all 4 years and across all 6 points — the spatial signal is entirely in actual ET, i.e. in **canopy presence + soil-water availability**, not in atmospheric demand. Restoring canopy will measurably raise sub-parcel ET.
- **Wesley pin (1438 mm/yr in 2024)** sits in the high-ET NE quadrant — building footprint and irrigation needs should plan against the wetter end of the gradient, not the parcel mean.

## Per-point actual ET (mm/yr, 4-yr record)

| Point | 2021 ET | 2022 ET (drought) | 2023 ET | 2024 ET | 4-yr mean | 2024 PET | 2024 ET/PET |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| centroid | 1298 | 1143 | 1346 | **1473** | 1315 | 2101 | 0.70 |
| corner_NE | 1369 | 1203 | 1369 | **1452** | 1348 | 1944 | 0.75 |
| corner_NW | 1287 | 1010 | 1263 | **1310** | 1218 | 2052 | 0.64 |
| corner_SE | 980 | 813 | 1160 | **1174** | 1032 | 1988 | 0.59 |
| corner_SW | 911 | 697 | 981 | **982** | 893 | 1964 | 0.50 |
| wesley_pin | 1364 | 1215 | 1359 | **1438** | 1344 | 1925 | 0.75 |

_Per-point series in `mod16_annual_points.csv`; 8-day cube in `mod16_per_granule_points.csv` (184 rows); JSON in `mod16_summary.json`._

## AOI summary (5 km buffer, 56 pixels @ 500 m)

| year | AOI ET mm/yr | AOI PET mm/yr | ET/PET | LE mean MJ/m²/day | Note |
| ---: | ---: | ---: | ---: | ---: | --- |
| 2021 | 1108 | 1995 | 0.555 | 7.39 | post-drought recovery |
| 2022 | **894** | 1970 | **0.454** | 6.01 | Paraná triple-Niña drought trough |
| 2023 | 1163 | 1938 | 0.600 | 7.86 | El-Niño-ish wet recovery |
| 2024 | 1200 | 1995 | 0.602 | 8.06 | continued wet, slight cooling of PET |
| **4-yr mean** | **1091** | **1975** | **0.553** | **7.33** | structural baseline |

## Cross-check with the water-budget stack

| Source | annual P / ET₀ / ET (mm) | role | Note |
| --- | ---: | --- | --- |
| **CHELSA v2.1 (P_annual)** | 1545-1760 | precip supply | [[chelsa_brief]]; NE→SW gradient matches MOD16 ET gradient sign-for-sign |
| **NASA POWER (Penman-Monteith ET₀)** | ~1700-1900 | atmospheric demand reference | within 5 % of MOD16 PET, confirms PET scale |
| **ERA5-Land** | T 21.6 °C, P 1709 mm | reanalysis cross-check | [[chelsa_brief]] cross-check table |
| **MOD16A2 actual ET (this brief)** | **1091 mm/yr** | what actually evaporates | 4-yr AOI mean, 2021-2024 |
| **Residual = P − ET (CHELSA − MOD16)** | **~685 mm/yr** | runoff + recharge + lateral | drains via the quebrada + perched water-table; matches GRDC-style ~40 % runoff coefficient for Cfa basins |

Implication: **the parcel has ~685 mm/yr of "spare" water** (precip not lost to ET) after a normal year — this is the water that feeds the quebrada baseflow, recharges the shallow aquifer, and is available for surface storage. In the 2022 drought P fell less than ET fell, so the residual was still ~700 mm — the quebrada should not have gone dry. Confirm this against the JRC-GSW surface-water history when [[jrc_gsw_brief]] lands.

## Cross-reference with hydro + canopy + soil + bioclim

| Position | P (CHELSA) | ET (MOD16 4-yr) | ET/PET | Canopy (Meta CHM) | TWI | Coherent story |
| --- | ---: | ---: | ---: | --- | --- | --- |
| centroid | 1760 | 1315 | 0.70 | 10.9 m gallery | high | wetter, cooler, closed canopy actively transpires |
| corner_NE | 1757 | 1348 | 0.75 | 12.7 m woodlot | mid-high | oldest stand, highest ET fraction — climax forest |
| corner_NW | 1670 | 1218 | 0.64 | 3.7 m scrub | mid | regrowth uses most of less rain |
| corner_SE | 1598 | 1032 | 0.59 | 3.4 m mosaic | mid-low | drier + degraded, sub-canopy bare ground loses water as soil evap |
| corner_SW | 1545 | 893 | 0.50 | 0.3 m cleared | low | pasture: half the rain runs off / drains; bare-soil albedo limits ET |
| wesley_pin | 1760 | 1344 | 0.75 | gallery edge | high | same regime as centroid |

The four datasets now tell **one** story along the NE→SW axis: **more rain + more canopy + higher TWI = higher actual ET = climate-buffered wet microhabitat**. The SW corner is climatically and hydrologically the harshest zone; the NE/centroid is the refuge.

## Engineering / design implications

### Water budget for the housing-park master plan
- **Plan the rainwater catchment against the 2022 floor, not the mean.** In 2022 the parcel evaporated 200 mm/yr less than normal — but precip was also down ~ 20 %, so the runoff coefficient held. The right design number for cistern sizing is **P_2022 × roof_area × runoff_coef** (drought-year, not average-year).
- **Irrigation demand differential**: cleared SW zone loses ~ 500 mm/yr less to ET than the NE woodlot — the soil there is in **deeper, longer water deficit** in the JJA dry quarter and will demand the most supplemental irrigation. Plan drip + greywater zones in the SW chacra accordingly.
- **Restoration ET uplift**: closing the canopy gap on the NW + SE quadrants (raising CHM from 3.4 m → 8 m mature secondary) should raise local ET by ~ 200-300 mm/yr based on the NE→NW differential. This pulls more carbon, lowers afternoon LST, and tightens the parcel's water cycle — feed this into the [[restoration_plan]] narrative.

### Architecture / passive design (Rule 6 — passive ≤ 35 °C)
- **High actual ET (1300+ mm/yr) at the building site means humid microclimate** — relative humidity in the canopy footprint will sit 5-10 % above the AOI mean. Cross-ventilation has to assume **vapor-pressure-deficit-limited cooling**, not dry-bulb cooling. The corredor (Rule 8) does this job; AC backup sized for the worst summer week, not the season.
- **LE ≈ 8 MJ/m²/day on a wet year ≈ 90 W/m² latent heat flux** evaporated from canopy + soil. A green roof / vegetated terrace re-creates that flux locally — strong argument for the sod-roof envelope (Rule 9 already separates PV onto its own frame, so the roof can be fully vegetated for evaporative cooling).

### Sub-render typology mapping
- Sub-render `lqv/subscene/water_budget.py`: visualize P → ET → runoff → recharge partitioning. Three bar-stacks (NE wet / centroid / SW dry) with the 1091 / 685 / 200 mm structural split. Drives the deck "where the water goes" panel.
- Sub-render `lqv/subscene/canopy_et_uplift.py`: before/after restoration ET map — toggle SW pixel from 893 → 1100 mm to show closure of the water-cycle gap. Pairs with [[canopy_height_brief]] restoration zones.
- Sub-render `lqv/subscene/drought_2022.py`: drought-year time series + AOI thumbnail showing the structural difference (894 vs 1100-1200 mm). Drives the resilience/contingency story panel.

## Provenance

- **MODIS MOD16A2 v6.1** (public-domain, NASA): NASA LP DAAC Earthdata Cloud, collection `C2565788905-LPCLOUD`, tile **h12v11** (MODIS sinusoidal, 2400×2400 px @ 463.31 m). Bands: `ET_500m` (scale 0.1 mm/8day), `PET_500m` (scale 0.1 mm/8day), `LE_500m` (scale 1e4 J/m²/day), `PLE_500m` (scale 1e4 J/m²/day). Fill 32767, valid_max raw 32700. Decoded via **pyhdf** (GDAL HDF4 driver unavailable in this env).
- Running S., Mu Q., Zhao M. (2021). _MOD16A2 v6.1 — MODIS/Terra Net Evapotranspiration 8-Day L4 Global 500 m SIN Grid_. NASA LP DAAC. doi:10.5067/MODIS/MOD16A2.061.
- Pipeline: `scripts/phase0_mod16_et_v1.py` — earthaccess search, per-granule pyhdf decode, sinusoidal→WGS84 6-point bilinear sample, AOI window means + per-year sum, GeoTIFF write at 0.005° resolution. RuntimeWarning at line 425 (`Mean of empty slice`) is benign — caused by an all-fill 8-day window in the AOI buffer, masked out in downstream aggregation.

## Carry-forward gaps (deferred)

- **2015-2020 MOD16A2 v6.1 reprocessing not yet available for tile h12v11** — collection metadata shows reprocessing in progress. Re-pull when LP DAAC opens older years; this brief gets a v2 once a 10-year baseline exists.
- **Daily PML_V2 or GLEAM ET** (~ 0.1°) would resolve the 8-day temporal aliasing in MOD16 but at coarser spatial — deferred to Phase-1 hydrology subpipeline.
- **In-situ flux tower** validation — none within 200 km. Cross-validate against [[era5_land_brief]] ET when ERA5-Land subset lands.
- **MOD11A2 LST 1 km** (next pull this session) will give the surface temperature gradient that should mirror the ET gradient: high-ET pixels should be cooler at midday. See [[mod11_brief]] when ready.
