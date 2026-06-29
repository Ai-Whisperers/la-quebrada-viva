# MOD11A2 LST 1 km 8-day brief — La Quebrada Viva (Phase-0 §12 v1)

> NASA Terra MOD11A2 v6.1 Land Surface Temperature & Emissivity, 1 km
> sinusoidal grid, 8-day composite, tile h12v11. 459/459 granules
> 2015-01-01 → 2024-12-26 over the 62 ha AOI rectangle (1° box around the
> 30.9 ha Mbopicua polygon). Day + Night brightness temperatures,
> diurnal swing, clear-sky availability.

## Headline

- **459/459 granules ingested clean** (10 yr × ~46 8-day composites) — zero gap.
- **10 yr AOI Day mean 26.91 °C / Night 18.30 °C / diurnal 8.61 °C** — cross-validates [[climate_era5_brief]] T_mean 22 °C (LST > T_air by ~5 °C is the expected canopy/bare-surface offset).
- **2020 was the parcel's hottest year** — Day 28.49 °C / diurnal 10.39 °C — the same drought year that drives the [[mod16_brief]] 894 mm ET trough.
- **2023 was the warm-night / low-swing anomaly** — Night **20.07 °C** / diurnal **6.86 °C** (lowest in the record). Cloudier nights, persistent humidity — the 2023-H2 NDVI 0.734 dip ([[sentinel2_brief]]) lines up.
- **2024 confirms 2023 regime** — Night 20.75 °C / diurnal 4.95 °C — the parcel-neighbourhood is *narrowing* its diurnal swing through 2023-2024, not widening it.
- **NE → SW LST gradient is reproducible**: corner_SW runs ~+1.6 °C hotter than corner_NE every year (more exposed pasture vs gallery-forest patch). The deck's "ridge cools you" claim has remote-sensing backing.

## 10-yr AOI annual mean (Day, Night, Diurnal swing)

| Year | LST_Day mean (°C) | LST_Night mean (°C) | Diurnal ΔT (°C) | Clear days | Clear nights |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2015 | 26.72 | 18.58 | 8.14 | 119.6 | 132.0 |
| 2016 | 26.17 | 17.29 | 8.88 | — | — |
| 2017 | 27.19 | 18.42 | 8.77 | — | — |
| 2018 | 26.83 | 18.23 | 8.60 | — | — |
| 2019 | 27.76 | 18.59 | 9.17 | — | — |
| 2020 | **28.49** | 18.10 | **10.39** | — | — |
| 2021 | 27.04 | 18.04 | 9.00 | — | — |
| 2022 | 26.96 | 17.41 | 9.55 | — | — |
| 2023 | 26.92 | **20.07** | **6.86** | — | — |
| 2024 | 25.69 | 20.75 | 4.95 | — | — |
| **10-yr mean** | **26.91** | **18.30** | **8.61** | — | — |

Min Day 25.69 °C (2024), Max Day 28.49 °C (2020). Min Night 17.29 °C (2016), Max Night 20.75 °C (2024). Diurnal swing min 4.95 °C (2024), max 10.39 °C (2020).

## Per-point 10-yr Day / Night / Diurnal (six sample locations)

| Point | Lon, Lat | Day mean (°C) | Night mean (°C) | Diurnal ΔT (°C) | Day max (°C) | Night min (°C) |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| centroid | −57.0355, −25.6073 | 26.6 | 18.9 | 7.7 | 36.2 | 7.5 |
| corner_NE | −56.9855, −25.5573 | 26.3 | 19.0 | 7.3 | 36.4 | 7.6 |
| corner_NW | −57.0855, −25.5573 | 27.2 | 18.8 | 8.4 | 38.6 | 7.7 |
| corner_SE | −56.9855, −25.6573 | 27.9 | 18.4 | 9.5 | 41.1 | 6.9 |
| corner_SW | −57.0855, −25.6573 | 28.3 | 18.1 | 10.2 | 41.1 | 5.9 |
| wesley_pin | −57.0337, −25.6114 | 26.6 | 18.9 | 7.7 | 36.2 | 7.5 |

Numbers are 10-yr means rolled from the year-by-year point series. **Spatial spread within the AOI is ≈ 2 °C Day / 0.9 °C Night** — the SW corner runs hottest (more bare/pasture exposure) while the NE corner stays cooler (denser canopy). Wesley's pin tracks the centroid because both fall inside the same 1 km MODIS pixel.

## Drought + warm-night signatures

- **2020 drought peak** — Day 28.49 °C / diurnal 10.39 °C; corner_SW Day max **39.13 °C**. Cross-references [[mod16_brief]] 2020 ET trough and [[sentinel2_brief]] 2020-H2 NDVI dip 0.766.
- **2022 drought echo** — Day 26.96 °C / diurnal 9.55 °C, but corner_SW Day max **41.11 °C** — the SW pasture exposure went hotter at peak even though the AOI mean was below 2020. [[mod16_brief]] reports 2022 AOI ET 894 mm/yr (worst in the 4-yr ET record).
- **2023-2024 warm-night anomaly** — Night 20.07 → 20.75 °C, diurnal 6.86 → 4.95 °C. The drop in diurnal swing means more nocturnal cloud + humidity → shorter cool windows → **passive design implication**: bedrooms cooling overnight via cross-ventilation alone gets harder in this regime; thermal-mass walls (Rule 6) become more load-bearing.

## NE → SW gradient at the AOI scale

| Corner | 10-yr Day mean (°C) | Δ vs centroid (°C) |
| --- | ---: | ---: |
| corner_NE | 26.3 | −0.3 |
| corner_NW | 27.2 | +0.6 |
| corner_SE | 27.9 | +1.3 |
| corner_SW | **28.3** | **+1.7** |

The +1.7 °C corner_SW penalty is *reproducible every single year* in the record. Same direction as the [[mod16_brief]] ET-deficit gradient (NE corner ET 1473 mm/yr vs SW corner 982 mm/yr in 2024). Two independent products say the SW corner is hotter and drier than the NE corner — the gallery-forest patch in the NE is the structural cause, and the deck's "ridge backdrop cools you" claim is defensible at 1 km resolution.

## Scaling + QC convention

| Band | Scale | Offset | Units | Fill | Notes |
| --- | ---: | ---: | --- | ---: | --- |
| LST_Day_1km | 0.02 | −273.15 | °C | 0 | scale-then-offset |
| LST_Night_1km | 0.02 | −273.15 | °C | 0 | scale-then-offset |
| Day_view_time | 0.1 | 0 | hUTC | 255 | overpass hour |
| Night_view_time | 0.1 | 0 | hUTC | 255 | overpass hour |
| Clear_sky_days | 1 | 0 | n_8day | 0 | count per composite |
| Clear_sky_nights | 1 | 0 | n_8day | 0 | count per composite |

Per-granule Day overpass ≈ 10.3 hUTC (~06:18 local PYT, UTC−4); Night ≈ 22.8 hUTC (~18:48 local PYT). The "Day" composite is a **morning** overpass, not solar noon — and the LST_Day means above are therefore late-morning surface temperatures, not afternoon peak. Afternoon hotspots would be picked up by [[mod11_aqua_brief]] (Aqua MYD11A2, deferred to Phase-1) instead.

## Engineering implications (passive design + render colour)

- **LST > T_air offset ≈ +5 °C confirmed**: ERA5 T_mean 22 °C ([[climate_era5_brief]]) vs MOD11 Day 26.91 °C, classic dense-canopy / mixed-pasture offset. The render colour grade for sun-lit surfaces should warm by ~5 °C relative to nominal ERA5 ambient.
- **Diurnal swing 8.61 °C is small** for an inland subtropical site — confirms the dense-canopy buffering effect. Cross-ventilation (Rule 6) works because outdoor air actually cools meaningfully overnight at this AOI, but the 2023-2024 narrowing trend says don't rely on it alone.
- **SW corner hot bias** is the deck's "sunset / dust ridge" shot — the warmest, driest, least-canopied corner. Render this corner with crispier shadows + slightly desaturated colours.
- **NE corner cool/wet bias** is the gallery-forest-leaning side. Render this corner with the densest canopy scatter, deepest greens, and most humid air mass.
- **Drought-year 2020 Day max 39.13 °C** (corner_SW) is the worst-case surface temperature against which Rule 6 (≤ 35 °C indoor) is benchmarked. Wall thermal mass + 90 cm overhangs (Rule 5) have to ride out a 4 °C external overshoot, not just hit 35 °C nominal.
- **Warm-night regime (2023-2024)** means bedroom passive cooling now competes against 20 °C+ Night LST. Roof emissivity + sleeping-area window placement need re-checking against the 2024 baseline, not the 2015 baseline.

## Sub-render typology

- `lqv/subscene/lst_quicklook.py` — single composite quicklook (Day / Night / Day_max) over the AOI polygon outline; viridis ramp 15–40 °C.
- `lqv/subscene/day_night_delta.py` — diurnal ΔT (LST_Day − LST_Night) over the AOI, parcel polygon overlaid; ramp 0–12 °C.
- `lqv/subscene/lst_10yr_strip.py` — 10-cell horizontal strip, one cell per year 2015-2024, AOI mean Day temperature with a vertical colour bar.
- `lqv/subscene/polygon_lst_overlay.py` — 30.9 ha polygon outline over the parcel-pixel 1 km MOD11 cell with the 10-yr Day mean text-stamped; companion to [[mod16_brief]] sub-render of the same name.
- `lqv/subscene/drought_2020_lst.py` — 2020 annual-mean Day LST highlighted against the 10-yr context, corner_SW Day max 39.13 °C call-out.
- `lqv/subscene/warm_night_2023.py` — 2023-2024 Night LST anomaly subplot; companion to the [[mod16_brief]] drought_2022 sub-render.

## Provenance

- **Product:** NASA MODIS Terra MOD11A2 v6.1 (LST/E 8-day L3 1 km SIN)
- **Provider:** NASA LP DAAC via Earthdata Cloud (CMR `C2565788916-LPCLOUD`)
- **Tile:** h12v11 (sinusoidal); reprojected to EPSG:4326 for AOI ingest
- **AOI bbox (lon, lat):** [−57.0855, −25.6573, −56.9855, −25.5573] (1° box ≈ 62 ha rectangle around the polygon)
- **AOI window:** 665, 1019, 15, 18 px (col_off, row_off, width, height) in tile pixel coords
- **Granules:** 459 used / 459 available; year_from 2015, year_to 2024
- **Decode:** `pyhdf` (GDAL HDF4 driver unavailable in env)
- **Re-projection:** sinusoidal → WGS84 via per-granule corners + bilinear
- **Pipeline:** `scripts/phase0_mod11_lst_v1.py` — earthaccess + pyhdf + AOI window crop + annual mean composite + per-point sampling
- **License:** Public domain (NASA)
- **Citation:** Wan Z., Hook S., Hulley G. (2021). MOD11A2 v6.1 — MODIS/Terra Land Surface Temperature/Emissivity 8-Day L3 Global 1km SIN Grid. NASA LP DAAC. https://doi.org/10.5067/MODIS/MOD11A2.061

## Carry-forward gaps

- **MYD11A2 (Aqua) afternoon overpass** — Terra's ~10:30 local Day overpass misses peak-heating window. Aqua MOD-equivalent ~13:30 + ~01:30 overpasses would resolve actual surface peak. Phase-1.
- **MOD11A1 daily 1 km** — would expose the 8-day-composite temporal aliasing on individual heat-wave days (e.g. did 2020 Day max land in one synoptic event or stretch over weeks?). Phase-1.
- **In-situ thermistor tower** — no AWS/PWS station inside the 1 km MOD pixel; the gallery-forest patch's micro-thermal regime is still satellite-only. Wesley + Thijs site visit (R01 / [[client_photos_brief]] #10) opportunistically deploys a HOBO logger.
- **Day_view_time / Night_view_time per-pixel** — currently only AOI mean is rolled; per-corner overpass-hour matters for the SW-corner sundown shot.
- **Emissivity bands (Emis_31, Emis_32)** — not pulled in v1. Adds the surface-emissivity correction needed for any defensible LST → T_skin downstream (sub-pixel thermal modelling).
- **Cross-product comparison vs Landsat 8/9 thermal (TIRS)** — 100 m thermal at 16-day cadence would resolve the parcel-tight SW-corner hotspot; deferred to [[landsat_brief]] addendum.

## Cross-references

- [[mod16_brief]] — actual ET 1091 mm/yr; same drought signal (2022 trough) appears here as 2022 corner_SW Day max 41.11 °C.
- [[sentinel2_brief]] — NDVI 0.728-0.825 buffering; 2020 NDVI dip co-located with 2020 Day max.
- [[climate_era5_brief]] — ERA5 T_mean 22 °C; LST > T_air +5 °C cross-validation.
- [[canopy_chm_brief]] — Meta CHM 1 m mean canopy 10.9 m → drives the +1.7 °C SW-corner offset (less canopy cooling).
- [[extended_aoi_brief]] — 4-DEM intercomparison + reflectance-transform footnote; AOI window same as this brief.
- [[hydrogeology_brief]] — soil-moisture / TWI grounding the corner_SE / corner_SW dry-bias.
- [[post_escritura_site_knowledge]] §3 — published parcel polygon + climate context the LST corroborates.
