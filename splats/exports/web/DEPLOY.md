# La Quebrada Viva · Site Map — Deployment Record

**Deployed: 2026-06-30** · **URL: https://lqv-walkthrough.pages.dev**

## What was deployed

A 12-layer interactive site map (`splats/exports/web/index.html` + `data/`)
to Cloudflare Pages:
- 16 vector + raster + CSV files (290 KB total)
- MapLibre GL JS viewer
- 3 basemaps (Aerial / Hybrid / Topo)
- Toggle panel for every layer
- Camera + disclaimer placeholders for the buyer perspective

## Verified live assets

| Path | Status | Size |
|---|---|---:|
| `/index.html` | 200 | 6277 b |
| `/lqv-map.js` | 200 | 12021 b |
| `/data/README.md` | 200 | 4.3 KB |
| `/data/canopy_classes.geojson` | 200 | 130 KB |
| `/data/hydrography_dem.geojson` | 200 | 20 KB |
| `/data/buildings_osm.geojson` | 200 | 7.4 KB |
| `/data/osm_water_overpass.geojson` | 200 | 50 KB |
| `/data/osm_roads_overpass.geojson` | 200 | 21 KB |
| `/data/osm_natural_overpass.geojson` | 200 | 6 KB |
| `/data/roads_osm.geojson` | 200 | 1.5 KB |
| `/data/landcover_zones.geojson` | 200 | 5 KB |
| `/data/gbif_-26.6000_-56.8000_30km.csv` | 200 | 56 KB |
| `/data/soil_-26.6000_-56.8000.json` | 200 | 538 b |

## Auto-redeploy

`~/.hermes/scripts/lqv-pages-redeploy.sh` runs every 6 hours (`hermes cron
lqv-pages-redeploy`). To re-deploy manually:

```bash
bash ~/.hermes/scripts/lqv-pages-redeploy.sh
```

## Adding more layers (just append)

1. Drop the new geojson/csv/json into `/tmp/lqv-scan/splats/exports/web/data/`.
2. Mirror to `~/.hermes/lqv-splat/splats/exports/web/data/`.
3. Append a `loadAndAdd(...)` block in `lqv-map.js`.
4. Run `bash ~/.hermes/scripts/lqv-pages-redeploy.sh`.

## Future photos — Wes's album

When Wes hands over the Google Photos album and `self_host_train.py` produces
PLY files in `splats/exports/ply/`:

1. Drop PLYs in `/tmp/lqv-scan/splats/exports/web/data/splats/`.
2. Add a `loadAndAdd()` for `splat_scene` to load Luma/gaussian-splat-format files
   on top of the satellite base map.
3. Re-deploy.

(TODO bump: copy `threejs_export.py` v0.2 logic — already in
`splats/tools/threejs_export.py` — to produce a Three.js viewer overlay.)
