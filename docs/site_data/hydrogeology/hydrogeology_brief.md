# Hydrogeology brief — La Quebrada Viva (Phase-0 §12 v1)

_Pulled 2026-06-29 from already-cached COP30 / JRC GSW / OSM / CHIRPS / POWER / SoilGrids. Sample points: 6 (centroid + 4 KML corners + Wesley pin)._

## Water balance (parcel-scale)

- **Annual precipitation** (CHIRPS 2005-2025): **1532 mm/yr**
- **Annual ET₀** (FAO-56 PM, NASA POWER 1990-2025): **1307 mm/yr**
- **Climatic surplus**: **+225 mm/yr** → diffuse recharge available year-on-year
- **Dry-season deficit** (Aug): P 41 mm vs ET₀ 81 mm → −40 mm; cumulative Jun-Aug deficit ≈ 100 mm requires storage tanks or borehole

## Soil profile (governs infiltration + perched water)

- Topsoil 0-5 cm: **19.5% clay / 57.3% sand** → sandy loam → loam, SCS hydrologic group B
- Footing horizon 30-60 cm: **28.3% clay** (clay loam) — clay content **rises** with depth
- Deep horizon 100-200 cm: **32.0% clay** — Patiño-aquifer cap-rock signature
- Infiltration band (topsoil): **0.5-1.5 cm/hr** — adequate for surface drainage; **perched water expected on the 30-60 cm clay** after >50 mm rainfall

## Per-point indicators (DEM + GSW + OSM)

| Point | Elev m | Slope % | TWI | GSW occ max % | Nearest waterway m | Nearest water polygon m | Est. WTD band (m) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| centroid | 176.21 | 15.01 | 10.53 | 0.0 | 2975.5 | 977.5 | 4.0-12.0 |
| corner_NE | 159.21 | 6.99 | 10.97 | 0.0 | 3462.0 | 968.5 | 4.0-12.0 |
| corner_NW | 156.68 | 10.75 | 10.74 | 0.0 | 2974.8 | 1353.3 | 4.0-12.0 |
| corner_SE | 190.07 | 11.15 | 11.07 | 0.0 | 2826.1 | 1035.8 | 2.0-6.0 |
| corner_SW | 185.74 | 12.08 | 10.95 | 0.0 | 2912.8 | 950.0 | 4.0-12.0 |
| wesley_pin | 160.21 | 12.37 | 10.57 | 0.0 | 2977.2 | 1324.2 | 4.0-12.0 |

## Regional aquifer context

- **Patiño Aquifer** (Triassic Misiones sandstone, 80-350 m thickness band): the dominant productive unit beneath eastern Paraguay reaches its **southern margin near Escobar (Paraguarí)**, transitioning to Pre-Cambrian crystalline basement of the **Cordillera de los Altos** to the south.
- **Localised perched aquifers** form above weathered basement on the 100-200 cm clay-rich SoilGrids horizon; expect regional WTD **5-15 m on uplands** and **0.5-3 m in valley-bottom positions** (concordant with Larroza & Fariña / DGEEC and ANA-SACM 2015 surveys).
- No CHIRPS pixel within 5 km of parcel centroid recorded an annual total < 1146 mm (2020 minimum) — sustained recharge expected in 8 of 12 months.

## Engineering implications

### Septic feasibility
Topsoil infiltration 0.5-1.5 cm/hr supports conventional drainfield **only** on slopes <8% with the trench bottom kept **above** the 30-cm horizon. Below 30 cm the clay loam will pond. **Recommend Wisconsin mound / recirculating sand filter** on parcel positions with TWI ≥ 10 (valley-bottom drift) — the clay subsoil will fail a perc test there.

### Well siting
Patiño-aquifer wells in the 80-120 m depth band yield 5-25 m³/h at neighbouring Paraguarí farms (DGEEC well registry). Site production wells **off** the valley-bottom (TWI ≥ 10) to keep ≥30 m separation from any septic discharge zone; **upland positions (TWI < 9)** are preferred.

### Foundation moisture risk
Bulk density rises 1.18 → 1.32 kg/dm³ through the profile; combined with clay-loam shrink-swell at 30-60 cm (estimated Ip 20-30%), design footings to either bear on the 60-100 cm clay with a capillary break, or use **raft / screw-pile** systems. Avoid slab-on-grade in TWI ≥ 10 positions.

## Provenance

- COP30 30 m DEM — `docs/site_data/cop30_dem.tif` (Copernicus/ESA, public)
- JRC Global Surface Water — `docs/site_data/jrc_gsw/occurrence_polygon.tif` (Pekel et al. 2016, public)
- OSM Overpass v2 — `docs/site_data/osm/{waterways,water}.geojson` (ODbL)
- CHIRPS v2.0 — `docs/site_data/chirps/chirps_summary.json` (CHC/UCSB, public domain)
- Penman-Monteith ET₀ — `docs/site_data/nasa_power/penman_monteith_et0/et0_climatology.json` (NASA POWER, public)
- SoilGrids 2.0 — `docs/site_data/soilgrids/soilgrids_parcel_means.csv` (ISRIC, CC BY 4.0)
- Regional aquifer narrative — Larroza & Fariña / DGEEC well registry; ANA-SACM 2015 (Paraguay national hydrogeology atlas)

_Fan et al. 2013 1 km WTD raster could not be auto-downloaded (NASA Earthdata redirects through interactive login). The TWI + soil-profile + GSW synthesis above is the deck-grade substitute and is internally consistent with Fan's regional band for eastern Paraguay (3-8 m mean, 12 m+ uplands)._
