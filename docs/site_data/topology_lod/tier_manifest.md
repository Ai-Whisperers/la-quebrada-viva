# Topology LOD cube — tier manifest

Driver: `scripts/phase0_topology_lod_cube.py`
Generated: 2026-06-29 04:13 UTC

User directive (2026-06-28): *high-fidelity topology inside the polygon, low-poly for surroundings, include important nearby geography for the eventual 3D digital twin.*

All rasters EPSG:4326 (lon/lat) with nodata=NaN, deflate-compressed.
Future drone-LiDAR (R35) drops into `core/dem_lidar_*.tif` and supersedes
the fused 5 m surface for Tier 1 only — Tiers 2 and 3 remain Cop30-based.

## Tier 1 — property core

- AOI: polygon (-57.0500,-25.6250,-57.0200,-25.5950) + ~100 m buffer
- Source: per-pixel **median** of ALOS AW3D30 + Cop30 + SRTM GL1 + NASADEM
- Native source resolution: ~30 m; resampled to **5 m grid** via cubic spline
- 30 m baseline: `core/dem_fused_30m.tif` shape (118, 118)
- 5 m smooth: `core/dem_fused_5m.tif` shape (706, 706)
- Elevation: min 132.1 m, max 354.5 m, mean 237.3 m
- Hillshade quicklook: `core/dem_fused_5m_hillshade.png`
- **Honest caveat**: source data is 30 m. Upsampling to 5 m yields a smooth high-density grid suitable for Blender displacement / dense-mesh export but does **not** add real detail. True high-fidelity awaits drone-LiDAR (R35).
- Recommended Blender mesh: 600×600 grid (~360 k tris) from 5 m raster as displacement map

## Tier 2 — local context (5 km buffer)

- AOI: (-57.0855,-25.6523,-56.9855,-25.5623)
- Source: Copernicus Cop30 (~30 m) via OpenTopography
- Output: `local/cop30_30m.tif` shape (333, 370)
- Elevation: min 103.7 m, max 433.8 m, mean 250.8 m
- Recommended Blender mesh: 300×300 grid (~90 k tris) — medium-detail surround for views of the parcel against immediate hills

## Tier 3 — regional macro (25 km buffer)

- AOI: (-57.2853,-25.8325,-56.7857,-25.3821) — matches biodiversity AOI
- Source: Copernicus Cop30 decimated 3× via mean-pooling → ~90 m grid
- 30 m raw: `regional/cop30_30m.tif`; 90 m low-poly: `regional/cop30_90m.tif` shape (555, 616)
- Elevation: min 65.4 m, max 501.9 m, mean 167.9 m
- Recommended Blender mesh: 200×200 grid (~40 k tris) — distant context (Cerro Mbatoví, Cerro Hu, Lago Ypoá, Mbopicua ridge)

## Future drop-ins

- **R35 drone-LiDAR** (post-photo intake): `core/dem_lidar_0p5m.tif` would supersede `dem_fused_5m.tif`; rebuild Tier 1 mesh at 0.5 m → ~6 M tris (decimate to taste for Blender).
- **Photogrammetric drone DEM** (cheaper alternative to LiDAR): `core/dem_drone_phot_0p1m.tif` if R35 budget unavailable.
- **R-series municipal cadastral DEM**: if Esc municipalidad publishes 1 m LiDAR, ingest into `core/dem_cad_1m.tif`.

## Blender import recipe

1. **Tier 1 (core)**: import `dem_fused_5m.tif` as displacement texture on a 600×600 subdivided plane sized to the core AOI footprint in metres (≈ 3.3 km × 3.6 km). Modifier: Displace → Texture (Image, Non-Color), Strength = (max-min) m, Midlevel = (mean-min)/(max-min).
2. **Tier 2 (local)**: same recipe with `local/cop30_30m.tif` on a 300×300 plane sized to 10 km × 10 km.
3. **Tier 3 (regional)**: `regional/cop30_90m.tif` on 200×200 plane sized to 50 km × 50 km.
4. Align all three to the polygon centroid (-57.0355, -25.6073) → UTM 21S origin so they nest correctly. Set Tier 1 to render in foreground, Tiers 2–3 with lower subdivision modifier strength and a fall-off texture to blend horizons.

