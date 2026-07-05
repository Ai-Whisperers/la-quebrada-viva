# LQV scripts

The 12 active scripts that build and maintain the LQV 20 km context viewer
at https://lqv-walkthrough.pages.dev/mapa-10km.html.

Run order to rebuild everything from scratch:

```bash
# 1. Pull OSM data for the 10 km box (~90 s)
python3 scripts/fetch_osm_10km.py

# 2. Build the raster-derived layers in parallel (~3 min each):
python3 scripts/build_10km_layers.py       # DEM quebrada + NDVI canopy + flow arrows
python3 scripts/build_hillshade.py         # hillshade_10km.jpg (1.94 MB)
python3 scripts/build_dem_contours.py       # 50 m contours + colour-relief
python3 scripts/build_10km_fullcover.py    # MapBiomas + Hansen loss/gain
python3 scripts/build_woodland_merged.py   # MapBiomas + Hansen + OSM fused

# 3. Build client GPS layers (idempotent):
python3 scripts/build_client_gps_layers.py

# 4. Audit wetlands + JRC (cross-validates OSM × DEM × JRC):
python3 scripts/audit_wetlands_10km.py
python3 scripts/audit_jrc_waterbodies.py

# 5. Fuse all water sources:
python3 scripts/build_combined_waterway.py

# 6. Validate + clip every GeoJSON to the 10 km box:
python3 scripts/clean_geometries.py

# 7. Deploy:
cd splats/exports/web && wrangler pages deploy . --project-name lqv-walkthrough
```

## Files that produce each layer

| Layer | Script | Source data |
|---|---|---|
| `dem_streams_10km.geojson` | `build_10km_layers.py` | Copernicus GLO-30 DEM, D8 flow |
| `ndvi_canopy_10km.geojson` | `build_10km_layers.py` | Sentinel-2 L2A via MS Planetary Computer |
| `dem_streams_arrows_10km.geojson` | `build_10km_layers.py` | derived from dem_streams |
| `dem_contours_10km.geojson` | `build_dem_contours.py` | Copernicus GLO-30, scikit-image marching-squares |
| `dem_color_relief_10km.jpg` | `build_dem_contours.py` | colour-relief composite |
| `hillshade_10km.jpg` | `build_hillshade.py` | Copernicus GLO-30, Lambertian shading |
| `mapbiomas_2023_10km.geojson` | `build_10km_fullcover.py` | MapBiomas Paraguay Collection 2 (2023) |
| `hansen_loss_10km.geojson` | `build_10km_fullcover.py` | Hansen GFC v1.12 2001-2024 |
| `hansen_gain_10km.geojson` | `build_10km_fullcover.py` | Hansen GFC v1.12 gain band 2000-2012 |
| `woodland_merged_10km.geojson` | `build_woodland_merged.py` | MapBiomas + Hansen + OSM fused |
| `surface_water_10km.geojson` | `audit_wetlands_10km.py` | OSM × JRC × DEM, 11-class taxonomy |
| `lqv_jrc_waterbodies_10km.geojson` | `audit_jrc_waterbodies.py` | JRC Global Surface Water (1984-2024) |
| `water_combined_10km.geojson` | `build_combined_waterway.py` | OSM ways + DEM + JRC + OSM polygons |
| `osm_10km/*.geojson` | `fetch_osm_10km.py` | Overpass API (8 endpoints) |
| `client_gps/*.geojson` | `build_client_gps_layers.py` | Guru Maps share (KML / GeoJSON / GPX) |

## 10 km box

- Centre: (-57.030381, -25.608231) — LQV parcel centroid
- Lat span: ±0.0898° (±10 km)
- Lon span: ±0.0996° (±10 km, with cos(25.6°) correction)
- BBOX (S, W, N, E): (-25.698062, -57.129997, -25.518400, -56.930765)
- ~385 km² total area

## Archived

The `_archive/` folder holds 70+ scripts for one-off deliverables
(BOQ, contact sheets, escritura deck, pelton siting, etc.) and
prior raster pulls. They are not part of the viewer maintenance
loop.