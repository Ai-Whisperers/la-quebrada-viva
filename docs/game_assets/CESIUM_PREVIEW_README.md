# LQV Game Assets — Cesium JS Preview

This folder contains all the UE5.7 + Cesium-ready assets for La Quebrada
Viva. Open `cesium_preview.html` in a browser to validate the data
pipeline before touching UE5.

```
open cesium_preview.html    # macOS
xdg-open cesium_preview.html # Linux
start cesium_preview.html   # Windows
```

## What you should see

- Top-down oblique view of the LQV parcel at ~1.2 km altitude
- Esri HD satellite imagery (1.07 m/pixel) covering ~1.9 × 2.1 km
- 5 waterfall candidates (blue dots with labels showing drop height)
- 62-ha property polygon outlined in gold
- 1100-ha AOI bbox outlined in dim gold
- Quebrada stream network (light blue polygons)
- Solar PV zones (yellow polygons)
- Camera controls: drag to rotate, right-click drag to zoom, middle-click drag to pan

## What this validates

✓ All GeoJSONs load without errors
✓ Esri HD PNG aligns to the lat/lon rectangle
✓ Coordinate system (WGS84) is consistent across layers
✓ Asset packaging (PNG + GeoJSONs) is web-compatible
✓ Cesium JS works without an ion token using SingleTileImageryProvider

## What this does NOT include

- The real heightmap terrain (Cesium JS doesn't render heightmaps easily —
  UE5 Landscape import handles that)
- The cob house (it's a 3D mesh — use UE5 GLB import)
- Photoreal materials (Cesium JS uses flat shading)
- First-person navigation (use UE5)

For those, run `tools/bootstrap_lqv_on_laptop.sh` on the gaming laptop.
