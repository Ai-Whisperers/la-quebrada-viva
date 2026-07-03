# W0.5 — Drone LiDAR pilots in PY (with DJI L1/L2)

**Method:** URL fetch (Brave search) + training data
**Confidence:** Medium (need direct quotes for specific pricing)
**Date:** 2026-06-30

## What Wes needs

A drone LiDAR survey of the 62 ha LQV parcel for:
- Sub-meter vertical accuracy terrain model
- Used for cabin siting (B02, B03 placement tool)
- Water-shed analysis
- Road + utility planning
- Insurance underwriting
- Pre-build documentation

**Typical equipment:** DJI Matrice 300 RTK + DJI Zenmuse L1 or L2 LiDAR sensor
**Typical cost:** $1,500-3,000 USD for 50-100 ha survey
**Lead time:** 2-4 weeks from booking to delivery
**Output:** DEM, point cloud, hillshade, orthomosaic

## Drone service providers in PY (2026)

| Provider | Coverage | Equipment | Notes |
|---|---|---|---|
| **Agniforge Survey** (mapping.agniforge.com) | All PY, includes Alto Paraguay | DJI Matrice 300 RTK + L1/L2 | **Top candidate.** International drone survey company with PY presence. |
| **UAVSphere PY** (uavsphere.com/countries/paraguay) | All PY | DJI Phantom 4 RTK, Matrice 300 RTK, WingtraOne | Marketplace platform — find local pilots |
| **GLOBHE** (globhe.com) | All PY | Various | Marketplace for drone service providers |
| **Local Asunción firms** (not web-indexed well) | PY urban + peri-urban | Various | Need direct outreach |

## Recommended vendors (priority order)

1. **Agniforge Survey** — most established for survey-grade work, has PY presence
2. **UAVSphere** — marketplace with multiple PY pilots, can compare quotes
3. **Direct local outreach** via PY agricultural associations (drone spraying is big in PY agriculture)

## What to ask for in quotes

For the 62 ha LQV parcel:
- **DEM (Digital Elevation Model)** at 0.5m or 1m grid spacing
- **Point cloud** (raw LiDAR returns)
- **Orthomosaic** (RGB photo mosaic at 5cm/px)
- **Hillshade** (visualization of slopes)
- **Volume calculations** if relevant (e.g. for road cut/fill)
- **Survey-grade GPS control** (RTK or PPK)
- **Processing in GIS-ready formats** (.las, .tif, .shp)

**Quote should include:**
- Per-hectare cost (or per-flight cost)
- Travel to property (Escobar, Paraguarí — ~150 km from Asunción)
- Equipment used (DJI L1 vs L2, etc.)
- Processing pipeline (raw → classified ground points → DEM)
- Deliverable formats
- Turnaround time (typically 1-2 weeks for processing after flight)

## Expected cost breakdown (PY, 2026)

| Item | Cost USD |
|---|---:|
| Flight + capture (62 ha) | 800-1,500 |
| GCP setup + RTK post-processing | 200-400 |
| DEM + ortho processing | 300-500 |
| Volume calcs + classification | 200-300 |
| Travel + accommodation | 200-400 |
| **Total** | **1,700-3,100** |

**Mid-estimate: $2,200** for a complete 62 ha survey.

## Wes's action (W0.5)

1. **Email 3 vendors for quotes** (Agniforge, UAVSphere, 1 local via drone association)
2. **Specify:** 62 ha in Escobar, Paraguarí; need ortho + DEM + hillshade; need survey-grade accuracy
3. **Schedule for next PY visit** (May-Oct dry season)
4. **Bring processed outputs back** for Ivan to use in B02/B03 placement tool + insurance underwriting + 3D renders

**Time cost:** 2-3 hours of email back-and-forth + $2,200 for the survey

## Bonus: alternative use cases for the same survey data

- **VR walkthrough** (B01) — orthomosaic + DEM → Three.js scene for buyers
- **Marketing video** (M06) — drone flyover of the actual property
- **Insurance** — show insurers the actual property layout
- **Sonja meeting** — bring drone photos to your next Sonja call
- **3DGS pipeline** (B07) — even if you don't get 5 phone videos, drone photogrammetry from this survey feeds the 3DGS pipeline

**Same survey, 5+ uses.** Strong ROI.

## Sources
- Agniforge: https://mapping.agniforge.com/index.php/paraguay
- UAVSphere: https://www.uavsphere.com/countries/paraguay
- GLOBHE: https://www.globhe.com/drone-service-providers-and-operators-per-country/paraguay

## Status

✅ Research done. Wes needs to email 3 vendors and get quotes. Best done in coordination with W1.2 site visit (the LiDAR survey happens during the same PY trip).
