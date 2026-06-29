# CHELSA v2.1 bioclim brief — La Quebrada Viva (Phase-0 §12 v1)

_Pulled 2026-06-29 from CHELSA v2.1 1981-2010 climatologies, 30-arcsec (~1 km) global grid, via the Switch.ch zhdk mirror (WorldClim UC Davis hosts are dead this session). AOI: 5 km buffer around parcel centroid (-57.0355, -25.6073). 19 standard BIO vars + 6 sample points (centroid + 4 KML corners + Wesley pin). 144 pixels @ ~1 km in the AOI window._

## Headline

- **Mean annual temperature 21.4 °C, annual precip 1776 mm** at the AOI — subtropical humid, Köppen **Cfa** boundary (no dry season; warm summer).
- **Warmest month** (≈ January): 30.7 °C daily max; **coldest month** (≈ July): 12.3 °C daily min. Annual range 18.5 °C — typical eastern-Paraguay continental gradient.
- **Wettest quarter** (austral spring-summer, ≈ Oct-Mar): 580 mm. **Driest quarter** (austral winter, ≈ Apr-Sep): 255 mm. P_CV 30 % — well-distributed but with summer max.
- **Spatial gradient inside the parcel**: NE→SW the AOI gets warmer (+0.3 °C) and drier (−215 mm/yr). Centroid + NE corner sit in the wetter, cooler valley-bottom microclimate (gallery forest zone) vs. SW corner on the dry, warm ridge (cleared pasture).
- Cross-validates ERA5 baseline (21.6 °C, 1709 mm) and NASA POWER (21.8 °C, 1681 mm) within 0.4 °C / 100 mm — CHELSA adds 1 km spatial detail the coarser products cannot resolve.

## Per-point bioclim (CHELSA pixel value at point)

| Point | T_annual °C | T_warm_max °C | T_cold_min °C | P_annual mm | P_wet_qtr mm | P_dry_qtr mm | P_CV % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| centroid | 21.75 | 31.65 | 12.75 | 1760 | 580 | 254 | 29.9 |
| corner_NE | 21.05 | 30.55 | 12.05 | 1757 | 580 | 254 | 29.7 |
| corner_NW | 21.75 | 31.45 | 12.45 | 1670 | 547 | 240 | 29.8 |
| corner_SE | 21.95 | 31.65 | 12.55 | 1598 | 525 | 230 | 29.4 |
| corner_SW | 22.05 | 31.65 | 12.55 | 1545 | 502 | 224 | 29.7 |
| wesley_pin | 21.75 | 31.65 | 12.75 | 1760 | 580 | 254 | 29.9 |

_Per-point values stored in `chelsa_points.csv`; raw windowed rasters in `chelsa_<label>.tif`; JSON in `chelsa_summary.json`._

## AOI summary (5 km buffer, 144 pixels @ ~1 km)

| BIO | mean | p05 | p95 | unit | meaning |
| --- | ---: | ---: | ---: | --- | --- |
| bio01 Annual mean T | 21.37 | 20.75 | 22.05 | °C | warm humid subtropical |
| bio02 Diurnal range | 8.90 | 8.80 | 9.00 | °C | moderate diurnal — humid moderation |
| bio03 Isothermality | 0.48 | 0.47 | 0.49 | % | 48 % — strong seasonality vs. diurnal |
| bio04 T seasonality | 345.1 | 329.7 | 362.1 | °C×100 | stdev 3.45 °C — Cfa range |
| bio05 T max warmest | 30.73 | 29.85 | 31.65 | °C | January peak |
| bio06 T min coldest | 12.26 | 11.85 | 12.75 | °C | July low (no frost) |
| bio07 T annual range | 18.48 | 18.00 | 19.00 | °C | wide continental swing |
| bio08 T wettest qtr | 23.62 | 22.85 | 24.45 | °C | summer rains warm |
| bio09 T driest qtr | 16.87 | 16.45 | 17.35 | °C | winter dry season cool |
| bio10 T warmest qtr | 25.47 | 24.65 | 26.35 | °C | DJF |
| bio11 T coldest qtr | 16.87 | 16.45 | 17.35 | °C | JJA |
| bio12 Annual precip | 1776 | 1521 | 1980 | mm | wet subtropical |
| bio13 P wettest month | 201.7 | 172.1 | 226.8 | mm | spring max (Oct/Nov) |
| bio14 P driest month | 68.7 | 58.5 | 76.9 | mm | winter min (Jul/Aug) — no true dry season |
| bio15 P CV | 30.2 | 29.5 | 30.8 | % | moderate seasonality |
| bio16 P wettest qtr | 580.1 | 493.7 | 651.5 | mm | OND or ONJ peak |
| bio17 P driest qtr | 254.8 | 220.0 | 281.6 | mm | JJA |
| bio18 P warmest qtr | 527.8 | 452.8 | 588.7 | mm | summer rains ≈ wettest |
| bio19 P coldest qtr | 254.8 | 220.0 | 281.6 | mm | winter dry ≈ driest |

## Cross-check with on-disk climate stack

| Source | T annual °C | P annual mm | Spatial res | Note |
| --- | ---: | ---: | --- | --- |
| **CHELSA v2.1 1981-2010** | **21.37** | **1776** | **1 km** | this brief — primary high-res baseline |
| ERA5-Land (`climate_era5/`) | 21.6 | 1709 | ~9 km | reanalysis, longer record |
| NASA POWER (`nasa_power/`) | 21.8 | 1681 | ~50 km | MERRA-2 modeled |
| CHIRPS v2.0 (`chirps/`) | — | ~1700 | ~5 km | precip-only, gauge-blended |

CHELSA sits within 0.4 °C / 100 mm of the reanalysis stack and is the only product that captures the **NE→SW precip gradient inside the parcel** (1760 → 1545 mm). This sub-parcel gradient is hydrologically real — it tracks the local relief from the valley-bottom drift up to the dry ridge — and is what drives the canopy pattern in [[canopy_height_brief]] (10 m gallery forest at NE / centroid, 0.3 m cleared pasture at SW).

## Cross-reference with hydro + canopy + soil

| Position | T_annual | P_annual | Canopy (Meta CHM) | TWI | Story |
| --- | ---: | ---: | --- | --- | --- |
| centroid | 21.75 | 1760 | 10.9 m gallery forest | high | wetter, cooler, closed-canopy quebrada head |
| corner_NE | 21.05 | 1757 | 12.7 m mature woodlot | mid-high | wettest, coolest, oldest stand |
| corner_NW | 21.75 | 1670 | 3.7 m scrub | mid | drier shoulder, regrowth |
| corner_SE | 21.95 | 1598 | 3.4 m degraded mosaic | mid-low | warmer, drier, fragmented |
| corner_SW | 22.05 | 1545 | 0.3 m cleared | low | hottest, driest, pasture |

The bioclim + canopy + TWI triplet now tells a single coherent story: the **NE/centroid quadrant is the wetter, cooler, mature-forest refuge** worth preserving, the **SW quadrant is the dry, hot, cleared ridge** suitable for PV / orchard / chacra. This will drive the housing-park site plan zoning.

## Engineering / design implications

### Habitat suitability (for the restoration & fauna-attraction work)
- Mean annual T 21.4 °C + Pn 1776 mm + no frost places the parcel inside the **Upper Paraná Atlantic Forest** climate envelope (BSAPF). All target restoration species (lapacho rosado, yvyrá-pytá, peterevy, ka'á he'ẽ, timbó) sit well within their bioclim niche here — no risk of climate-misplaced plantings.
- **bio06 (min cold) = 12.3 °C** means rare frost risk; species marginal on cold tolerance (mango, some cacao varieties) can survive but won't thrive. **Citrus, palta (avocado), guayaba, mamón (papaya), pacurí, yerba mate** are safe.
- **bio14 (driest month) = 69 mm** means even in the worst month the parcel gets > 2 mm/day average — irrigation is supplemental, not survival-critical, for native species. Annuals (huerta, tomato, melon) will still need supplementary watering in the JJA window.

### Architecture / passive design (deck Rule 8 reciprocity)
- **Annual diurnal range 8.9 °C + cool winter (Tmin 12 °C) + hot summer (Tmax 31 °C)** → high thermal-mass walls + cross-ventilation + deep overhangs. This is the canonical Cfa Paraguayan vernacular: thick adobe / quincha, wide galleries, high pitched roof with vented ridge. NOT Mediterranean (too humid), NOT tropical-Bali (too cool in winter), NOT Earthship (too humid for buried walls).
- **528 mm precip in the warmest quarter** → roof shedding + gutters sized for ≈ 200 mm/month design storm. Critical for rainwater harvesting yields: at 1776 mm/yr and 150 m² roof, gross collection ≈ 240 m³/yr — enough to supply a 4-person household at WHO-baseline 50 L/p/d.
- **bio15 P_CV 30 %** is moderate — rainwater harvesting can buffer through the JJA dry months with a ~ 25 m³ cistern + dry-season top-up from the well or quebrada.

### Sub-render typology mapping
- Sub-render `lqv/subscene/climate_summer_rains.py`: target heavy convective storm scene (DJF), 200 mm/month rainfall, ~ 25 °C ambient. Use for stormwater visualization.
- Sub-render `lqv/subscene/climate_winter_dry.py`: target dry winter scene (JJA), 60 mm/month, cool 17 °C, low sun angle. Use for solar-gain analysis & passive-heating story.

## Provenance

- **CHELSA v2.1 1981-2010** (CC-BY-4.0): `https://os.zhdk.cloud.switch.ch/chelsav2/GLOBAL/climatologies/1981-2010/bio/CHELSA_bio<N>_1981-2010_V.2.1.tif` (live anonymous mirror; UC Davis hosts dead). Karger D.N. et al. (2017). Climatologies at high resolution for the earth's land surface areas. _Scientific Data_ 4, 170122. doi:10.1038/sdata.2017.122. Tech doc with scale/offset specs: https://chelsa-climate.org/wp-admin/download-page/CHELSA_tech_specification_V2.pdf
- Pipeline: `scripts/phase0_chelsa_v1.py` — `/vsicurl/` windowed read, AOI = 0.1° × 0.1° around centroid, per-point single-pixel sample, scale + offset applied per BIO_META table.

## Carry-forward gaps (deferred)

- **CHELSA monthly tas/tasmin/tasmax/pr** (48 vars) — not pulled this batch; monthlies covered by ERA5-Land and NASA POWER stacks. Pull only if a deck panel needs CHELSA 1 km monthly resolution specifically.
- **CHELSA future projections (CMIP6 downscaled to 1 km)** — covered by Phase-0 [[cmip6]] NEX-GDDP pull (in progress at time of this brief).
- **WorldClim 2.1 cross-validation** — UC Davis hosts dead (HTTP 000) both at `geodata.ucdavis.edu` and `biogeo.ucdavis.edu`; S3 mirror 404. Skip; CHELSA is the live successor anyway.
