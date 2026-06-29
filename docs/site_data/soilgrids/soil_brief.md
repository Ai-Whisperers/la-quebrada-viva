# Soil brief — La Quebrada Viva (30.9 ha Mbopicua cluster)

Source: ISRIC SoilGrids 2.0 REST API (250 m raster), CC-BY 4.0  
Pulled: 2026-06-29T18:10:57Z  
Sampling: 6 points across the KML polygon (centroid + 4 corners + Wesley pin)  
Raw layered JSON: `soilgrids_multipoint_raw.json` · Flat CSV: `soilgrids_multipoint_flat.csv` · Per-depth pivots: `soilgrids_depth_*.csv`

## Construction-relevant slice (0-30 cm parcel-mean)

| Property | 0-5 cm | 5-15 cm | 15-30 cm | Target units |
| --- | --- | --- | --- | --- |
| **clay** | 19.48 | 21.47 | 22.03 | % (g/kg ÷ 10) |
| **sand** | 57.30 | 55.77 | 55.22 | % (g/kg ÷ 10) |
| **silt** | 23.25 | 22.78 | 22.72 | % (g/kg ÷ 10) |
| **phh2o** | 5.40 | 5.37 | 5.33 | pH unit |
| **bdod** | 1.18 | 1.23 | 1.27 | kg/dm³ |
| **cec** | 20.55 | 20.65 | 19.17 | cmol(c)/kg |
| **nitrogen** | 3.09 | 2.03 | 1.26 | g/kg |
| **ocd** | 40.72 | 30.70 | 21.50 | kg/m³ |
| **soc** | 37.63 | 26.93 | 19.82 | g/kg |

## Footing-depth slice (30-200 cm parcel-mean)

| Property | 30-60 cm | 60-100 cm | 100-200 cm | Target units |
| --- | --- | --- | --- | --- |
| **clay** | 28.28 | 30.58 | 31.97 | % (g/kg ÷ 10) |
| **sand** | 50.70 | 48.35 | 47.73 | % (g/kg ÷ 10) |
| **silt** | 21.00 | 21.08 | 20.28 | % (g/kg ÷ 10) |
| **phh2o** | 5.35 | 5.33 | 5.35 | pH unit |
| **bdod** | 1.28 | 1.31 | 1.32 | kg/dm³ |
| **cec** | 18.88 | 18.65 | 18.32 | cmol(c)/kg |
| **nitrogen** | 0.75 | 0.52 | 0.47 | g/kg |
| **ocd** | 11.32 | 6.53 | 3.82 | kg/m³ |
| **soc** | 9.58 | 7.60 | 8.43 | g/kg |

## Engineering flags (auto-derived)

- **Topsoil texture:** clay=19.5%, sand=57.3% → sandy-loam (significant clay supplementation needed)
- **Subsoil clay (30-200 cm):** max 30.6% → moderate shrink-swell risk, standard isolated footings acceptable with 60 cm minimum depth.
- **Topsoil pH:** 5.40 → acidic — cement-stabilised earth blocks need extra lime (CSEB lime dose +50%)
- **Topsoil bulk density (0-5 cm):** 1.18 kg/dm³ → very loose, strip and stockpile before any compaction
- **Topsoil fertility (0-5 cm):** SOC=37.6 g/kg, N=3.09 g/kg, CEC=20.6 cmol(c)/kg → high fertility — preserve A-horizon for orchard/pasture
- **Septic-leach-field feasibility (30-60 cm):** clay=28.3% → marginal permeability, sized leach field 30% larger than standard

### Sub-parcel variability (point-to-point spread)

| Property | Depth | Min | Mean | Max | Spread |
| --- | --- | --- | --- | --- | --- |
| clay | 0-5cm | 19.10 | 19.48 | 20.50 | 1.40 |
| clay | 30-60cm | 27.20 | 28.28 | 29.20 | 2.00 |
| sand | 0-5cm | 52.50 | 57.30 | 60.50 | 8.00 |
| sand | 30-60cm | 46.10 | 50.70 | 54.00 | 7.90 |
| phh2o | 0-5cm | 5.40 | 5.40 | 5.40 | 0.00 |
| phh2o | 30-60cm | 5.30 | 5.35 | 5.40 | 0.10 |
| soc | 0-5cm | 36.40 | 37.63 | 39.10 | 2.70 |
| soc | 30-60cm | 8.10 | 9.58 | 11.30 | 3.20 |

## Methodology notes

- SoilGrids 2.0 native raster resolution is 250 m, so 6 points within a 30.9 ha (~556 m × 556 m equivalent) parcel may sample 2-4 distinct raster cells. Point-to-point spread reflects actual sub-parcel variability where present.
- All values are predictive (Quantile Random Forest) — they are *not* substitutes for in-situ geotechnical drilling. Use as design-stage screening to plan where to drill.
- d_factor scaling already applied: clay/sand/silt reported in % (raw is g/kg × 10), phh2o in pH units (raw is pH × 10), all others in their target units per SoilGrids docs.
- For foundation engineering: confirm subsoil cohesion with at least 2 hand-auger holes to 2 m depth before pouring footings, especially at NE and SE corners where the SoilGrids draw-down may underrepresent the actual clay content of the Mbopicua geological substrate.
