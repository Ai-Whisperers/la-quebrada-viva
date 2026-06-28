# Cataratas del Monday — Data Inventory

> **Site:** Cataratas del Monday (Monday Ytororõ), Presidente Franco, Alto Paraná, Paraguay
> **Center:** −25.561944, −54.631389 (WGS84) — UTM 21J E 737960 N 7170703
> **AOI:** 6 km × 6 km box, 3 km radius from the cascade
> **Acquired:** 2026-06-11 (Bram's request — high-detail Blender-ready dataset)
> **Total tracked:** 54 MB; with raw archives: 171 MB (regenerable)

## Site context

- 3 main drops, ~40 m height, ~120 m wide (Wikipedia)
- Black basaltic bedrock, **negras piedras basálticas** (Wikipedia)
- Río Monday (Spanish: "robbing water" / "stolen water") draining to Río Paraná
- Urban edge: Presidente Franco + Ciudad del Este (33% built-up in AOI)
- Forest cover: 41% of AOI is Atlantic Forest remnant (ESA WorldCover 2021)
- Air: 21°C mean, 38°C max; rainfall highest in Paraguay

## What's in this directory

### 1. DEM (terrain elevation) — `dem/`
| File | Resolution | Source | Notes |
|------|-----------|--------|-------|
| `terrarium_monday_2_5m_utm21j.tif` | **2.5 m** | AWS terrain-rgb (SRTM-derived) | 6 km × 6.1 km, UTM 21J, 2440×2452 px, **primary terrain for Blender** |
| `terrarium_monday_10m_utm21j.tif` | 10 m | ditto | Same as above, native z=13 tile size |
| `terrarium_monday_10m.tif` | 10 m | ditto | WGS84 version |
| `nasadem_elevation.tif` | 30 m | NASA / Planetary Computer | 1°×1° raw tile (85 MB, gitignored) |
| `alos-dem_data.tif` | 30 m | JAXA / Planetary Computer | Cross-check |
| `cop-dem-glo-30_data.tif` | 30 m | ESA Copernicus | Cross-check |
| `terrarium_z13/*.png` | ~10 m raw | AWS | 4 source tiles at z=13 (regenerable) |

**Cascade area relief (1 km box around center):** 117 → 235 m AMSL (118 m drop)
**Maximum slope detected:** 90° (cliff face)
**Espacement-line coupling:** cliff runs east-west along 25°33′43″S

### 2. Sentinel-2 multispectral (10 m optical) — `sentinel2/`
- Scene: `S2B_MSIL2A_20251120T133829_R124_T21JYM`
- Date: 2025-11-20 13:38 UTC
- Cloud cover: **0.002%** (essentially perfect)
- Bands: B02 (blue), B03 (green), B04 (red), B08 (NIR), SCL (scene class) at 10/20 m
- Bands gitignored (240-290 MB each, regenerable via `fetch_sentinel2.py`)
- Composites built in `analysis/`

### 3. HD satellite imagery — `hd_imagery/`
- **Esri World Imagery** (ArcGIS REST tile service, no key needed)
- `esri_z17_stitched.png` — 1.19 m/pixel, 2.5 km × 2.5 km centered on cascade (7×7 = 49 tiles, 5.4 MB)
- `esri_z16_stitched.png` — 2.38 m/pixel, 5.0 km × 5.0 km wider context (5.8 MB)
- This is the **"ultra-HD"** aerial source for the cascade and surrounds
- Source attribution: © Esri, Maxar, Earthstar Geographics, and the GIS User Community

### 4. Analysis composites (Blender-ready) — `analysis/`
| File | Type | Notes |
|------|------|-------|
| `rgb_truecolor_utm21j.tif` | GeoTIFF RGB 10m | **albedo for Blender** |
| `rgb_truecolor_2_5m.png` | 2452×2408 upsampled | 4× upscaled version |
| `rgb_truecolor_10m.png` | 588×613 PNG | quick view |
| `nir_falsecolor_10m.png` | 10m | vegetation discrimination |
| `ndvi_utm21j.tif` | float32 10m | per-pixel vegetation index |
| `ndvi_10m.png` | 8-bit visualisation | |
| `landcover_from_ndvi.png` | derived (NDVI-binned) | water/soil/grass/forest classes |
| `hillshade_2_5m_az315_sunNW.png` | 2.5m | terrain shading, NW sun |
| `hillshade_2_5m_az045_sunNE.png` | 2.5m | NE sun |
| `hillshade_2_5m_az225_sunSW.png` | 2.5m | SW sun |
| `hillshade_10m_*.png` | 10m | same at 10m |
| `slope_2_5m.png` | 2.5m | slope 0-60° (white) |
| `slope_10m.png` | 10m | |
| `heightmap_10m.png` | 10m | elevation 0-255 (visual) |
| `cliff_mask_2_5m.png` | 2.5m | slope >35° = white |
| `cliff_mask_30m.png` | 30m | ditto on NASADEM |
| `cliff_crest_visualization.png` | 30m | crest edge = red, cliff = grey |
| `cliff_crest_utm21j.csv` | CSV | 20,876 (E, N, elev, slope) crestline points |
| `elev_30m_aoi.png` | 30m | elevation visualisation of AOI |
| `slope_cliff_3km.png` | 3km box | red = cliff >40° |

### 5. OSM attribution data — `osm/`
- `overpass_monday.json` — 43,779 elements, 35 MB
- Breakdown: 59 waterways, 29,979 buildings, 2,048 highways, 12,598 natural features, 9 tourism, 8 bridges
- Useful for: real river path, real building footprints (Parque Municipal Monday + urban edge), real roads

### 6. Land cover — `landcover/`
- `esa_worldcover_utm21j.tif` — 10m land cover, ESA WorldCover 2021 v200
- `esa_worldcover_utm21j.png` — coloured classification
- `landcover_from_ndvi.png` — derived 4-class (water/soil/grass/forest)
- **Land-cover distribution in AOI:** tree 41% · built-up 33% · grassland 11% · cropland 9% · water 2% · bare 0.2%

### 7. Blender driver — `blender_import_monday.py`
- Standalone Python script (bpy + numpy + rasterio)
- Imports the 2.5m DEM, applies the S2 albedo as base color, builds a terrain mesh
- Adds a cascade feature water plane and a sun + camera pointing at the falls
- Run: `blender --background --python blender_import_monday.py`

## How to regenerate

```bash
cd /root/la-quebrada-viva/docs/site_data_monday
python3 fetch_dem_pc.py        # pull NASADEM + ALOS + COP30 from Planetary Computer
python3 build_dem_10m.py        # merge terrarium 10m tiles
python3 fetch_sentinel2.py      # pull best S2 scene (free, 0.002% cloud)
python3 fetch_osm.py            # OSM water/forest/buildings
python3 build_composites.py     # build RGB / NDVI / hillshade composites
python3 fetch_hd_imagery.py     # pull Esri World Imagery 1.2m
```

## What this data lets you do in Blender

1. **Real terrain** at 2.5m horizontal × ~5m vertical resolution across 36 km²
2. **Real albedo** from Sentinel-2 (10m) overlaid with 1.2m Esri imagery on the cascade
3. **Real water/forest/urban classification** → assign different materials in Cycles
4. **Real cliff geometry** → cliff mask + crestline CSV → 3D edge mesh
5. **Real river path** → OSM waterway polylines → curve → swept tube
6. **Real vegetation heights** → NDVI → scatter leaves (next step: 3D canopy model)
7. **Real sun angle** at Asunción, Paraguay on 2026-06-27 (escritura date) — use for hero shot

## Known limitations / next steps

- GEDI L2A shots **not pulled** — only available via NASA Earthdata auth, not Planetary Computer. Canopy height map will need that. **Replacement: Tolan 2024 global 1m forest height** is not yet mirrored on PC for our tile.
- **10m COP-10 DSM** (better than SRTM/SRTM-derived terrarium) needs Copernicus Data Space Ecosystem auth — would give true 10m surface model. Not pulled.
- **Anthurium & epiphyte texture detail** at the cascade base (Wikipedia mentions Atlantic Forest remnant) — would need drone survey or higher-res imagery
- **Real basáltica rock texture** at the cliff face — would need either drone oblique or field photography
- **3D forest models** (pindo palm, lapacho) — same library as LQV, available on Sketchfab / Quaternius

## Data sources & attribution

- **Microsoft Planetary Computer** — free, no key, signed URLs — DEMs + S2 + ESA WorldCover
- **AWS terrain-tiles** (terrarium SRTM-derived) — public, no key
- **ArcGIS REST tile service (Esri World Imagery)** — public tiles, attribution: Esri, Maxar, Earthstar Geographics
- **OpenStreetMap** (Overpass API) — © OpenStreetMap contributors, ODbL
- **Sentinel-2** — ESA Copernicus, free + open
