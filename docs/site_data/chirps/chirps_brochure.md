# CHIRPS monthly precipitation — La Quebrada Viva parcel

Source: CHIRPS v2.0 (Climate Hazards Group, UCSB), public domain  
Resolution: 0.05° (~5.5 km)  
Window: 2005-2025  
Point: lon=-57.03000, lat=-25.63000  
Pulled: 2026-06-18T18:33:32Z

## Annual totals

- Mean: **1532.4 mm/yr**
- Min:  1146.3 mm/yr
- Max:  2095.7 mm/yr

## Monthly climatology (mm, long-term mean)

| Month | mm |
| --- | ---:|
| Jan | 136.5 |
| Feb | 142.3 |
| Mar | 156.6 |
| Apr | 157.0 |
| May | 158.7 |
| Jun | 77.7 |
| Jul | 64.7 |
| Aug | 41.0 |
| Sep | 76.4 |
| Oct | 174.0 |
| Nov | 174.9 |
| Dec | 172.7 |

## Interpretation hooks

- Tank sizing: design against the *driest-year* total, not the mean — see `chirps_summary.json` → `annual_total_min_mm`.
- The driest 3-month run drives cistern volume; pick the lowest three consecutive months in the table above.
- Compare against `docs/site_data/climate_era5/` precip series — if CHIRPS is meaningfully drier, trust CHIRPS at parcel scale (5 km beats 28 km).
- Clipped per-month TIFFs: `tiles/chirps_YYYY_MM.tif` (small).