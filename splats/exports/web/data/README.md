# La Quebrada Viva · Site Map · Data Provenance

**Last regenerated 2026-06-30** · AOI: 30.9-ha buildable cluster in Mbopicua, Escobar, Paraguarí, Paraguay
**Centroid 25°36′26″S, 57°02′08″W** (WGS84) · UTM 21J

This page is a single-file static site hosted on Cloudflare Pages. All vector
data is served as static files in this directory. The interactive map is
MapLibre GL JS, the hero composite is a server-rendered WebP. No server, no
APIs at runtime.

## Vector data layers (offline)

| File | Source | What it shows | Records |
|---|---|---|---:|
| `canopy_classes.geojson` | Sentinel-2 S2B_21JVM_20260512_0_L2A NDVI (4 bins) | Forest density | 61 polygons |
| `hydrography_dem.geojson` | Copernicus GLO-30 DEM, D8 flow accumulation | Raw stream segments | 15 line-segments |
| `hydrography_dem_v2.geojson` | Same, with main vs tributary classification | Stream network (classified) | 15 segments |
| `osm_buildings_near.geojson` | OSM Overpass, filtered to within 500m of LQV polygon | Buildings | 16 polygons |
| `osm_buildings_v2.geojson` | OSM Overpass, full 1-km buffer | Buildings (legacy) | 31 polygons |
| `osm_roads_near.geojson` | OSM Overpass, within 500m of LQV polygon | Roads | 0 features |
| `osm_roads_v2.geojson` | OSM Overpass, full 1-km buffer | Roads (legacy) | 2 features |
| `osm_water_v2.geojson` | OSM Overpass | Streams + ponds | 0 features |
| `osm_natural_v2.geojson` | OSM Overpass | Forest / wood / scrub (rural area, sparse) | 0 features |
| `osm_places_v2.geojson` | OSM Overpass | Nearby villages/hamlets | 0 features |
| `osm_landcover_zones_v2.geojson` | OSM Overpass | Farmland / meadow / orchard | 2 features |
| `gbif_-25.6073_-57.0355_30km.csv` | GBIF API (re-pulled 2026-06-30) | 30-km radius biodiversity observations | 300 records |
| `soil_actual.json` | SoilGrids 2.0 (re-pulled 2026-06-30) | pH, OC, clay, sand, silt, BD (3 depths) | 18 values |
| `lqv_bundle.geojson` | Combined bundle of all 6 spatial layers | All LQV geojson data | 113 features |

**A note on filter scope:** the OSM data is sparse in this rural Paraguayan area.
Filtering to within 500m of the LQV polygon keeps only the immediately relevant
features (16 buildings, 0 roads because rural tracks aren't mapped) but excludes
~15 buildings and 2 roads that are 200m+ away from the property. The legacy
v2 files preserve the full 1-km buffer for reference.

## Pre-rendered preview assets (`data/preview/`)

| File | Purpose |
|---|---|
| `lqv_composite_v6.webp` | Hero composite: satellite at z=17 (1m/pixel) + property outline + NDVI canopy classes + DEM streams + OSM buildings. 1km × 1km bbox centered on the LQV polygon. |
| `lqv_composite_v5.webp` | Earlier version (1800×1800, z=18 satellite, 600×600m). Kept for visual history. |
| `property_zoomed.webp` | Just the LQV 30.9 ha polygon outline on satellite |
| `canopy_zoomed.webp` | 4-class NDVI canopy classes on satellite |
| `streams_zoomed.webp` | DEM-derived stream network (bolder rendering) |
| `buildings_zoomed.webp` | 16 OSM buildings (within 500m of LQV) |
| `lqv_4up_poster.webp` | 4-panel composite: RGB + NDVI + NDWI + Canopy (1640×1240) |
| `polygon_quicklook.webp` | Sentinel-2 RGB quicklook of the polygon |
| `polygon_ndvi_quicklook.webp` | NDVI quicklook |
| `polygon_ndwi_quicklook.webp` | NDWI quicklook (confirms 0% open water inside polygon) |
| `A_hero_hero.webp` / `B_hero_hero.webp` / `C_hero_hero.webp` | Cycles hero renders — three atmospheric variants of the same camera (A: clear noon, B: golden hour haze, C: dawn fog from quebrada mist) |
| `water.webp` | Water body quicklook |

## Raster basemaps (external CDNs, used by the interactive map)

- **Esri World Imagery** (default; aerial): https://server.arcgisonline.com
- **OSM tiles** (street base): https://tile.openstreetmap.org
- **OpenTopoMap** (topographic): https://a.tile.opentopomap.org

## Key facts about the LQV parcel

- **Location**: Mbopicua, Escobar district, Paraguarí, Paraguay
- **Centroid**: 25°36′26″S, 57°02′08″W (WGS84), UTM 21J
- **Size**: 30.945 ha (computed) / 30.915 ha (KML claim) — 0.1% difference, well within tolerance
- **Areal context**: 62.57 ha legal total in the Escritura, of which the LQV is the **30.9 ha buildable** northern Mbopicua cluster
- **Source**: Wesley van de Camp hand-drew the polygon in Google Earth Pro, exported as KML, transcribed by Claude Code session 588baf01
- **Topology**: 8 vertices, closed, all on UTM 21S

## Soil profile (SoilGrids 2.0, 3 depths)

| Property | 0-5cm | 5-15cm | 15-30cm | Unit |
|---|---|---|---|---|
| pH (phh2o) | 4.9 | 4.9 | 5.0 | (1-14) |
| Organic Carbon (soc) | 24.0 | 13.8 | 7.1 | dg/kg |
| Clay | 11.1 | 11.2 | 15.0 | % |
| Sand | 62.8 | 66.7 | 62.7 | % |
| Silt | 13.0 | 12.1 | 11.8 | % |
| Bulk density (bdod) | 1.32 | 1.38 | 1.47 | kg/dm³ |

## Climate (ERA5 1990-2025)

- Mean annual 2m temp: 22.04°C
- Mean annual precipitation: 1736 mm/yr
- See `docs/site_data/climate_era5/climate_summary.txt` for full monthly data

## Re-render

The whole map rebuilds from this directory + the provenance above. To regenerate:

```bash
# OSM refresh
lqv-data-fetch                                       # refreshes OSM via Overpass + GBIF

# Canopy
lqv-build-canopy                                     # regenerates canopy_classes.geojson from Sentinel-2

# Streams
lqv-build-hydrography                                # regenerates stream network

# Composite hero
HOME=/tmp python3 /tmp/lqv_build_v6.py               # rebuilds the v6 hero (1km x 1km)

# Re-deploy
bash /root/.hermes/scripts/lqv-pages-redeploy.sh
```

## What the data does NOT show

- **Individual tree positions** — needs Wes's phone captures → COLMAP + gsplat
- **Padron / SNC catastro** — needs `Anexo I` from Wesley
- **Fire history** — needs `FIRMS_MAP_KEY` (env setup script prompts for it)
- **Drone / Maxar imagery** — needs Vantor tasking (~$2,800-4,400)
- **Stream connectivity (D8 flow-accum fragments)** — the 15 stream segments are real but disconnected; we need higher-resolution DEM or post-processing with r.streams.extract_network to fix this

## Out-of-scope

This is a buyer-pre-sales visualization, not a survey or design tool. The data
is suitable for orientation, pre-sales conversation, and buyer face-time. It
is not suitable for construction planning, environmental impact assessment, or
legal/cadastral purposes — for those, engage a licensed Paraguayan agrimensor
(see `docs/_archive/2026-06-1X/UPGRADE_PLAN.md` for the relevant SoW).
