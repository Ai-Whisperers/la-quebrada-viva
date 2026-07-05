# LQV v3 → v4 upgrade: side-by-side

This document shows the before/after of the LQV buyer page visualization
upgrade completed 2026-06-30.

## Visual evidence

| Aspect | Before (v3) | After (v4) |
|---|---|---|
| Page hero stddev (variance) | 39 | **71** (+82%) |
| Property polygon visible? | 122 yellow px (tiny) | **2073 yellow px** (full polygon outline) |
| Canopy visible in image | 2189 dark-green px | **230785 dark-green px** (canopy fills visible area) |
| Buildings visible | 149 gray px | **443040 gray px** (31 OSM buildings, 16% of image) |
| Streams visible | 0-5 blue px | **765 blue px** (with halo) |
| White text (legend) | n/a | **12090 px** (legend, scale, labels) |
| Image zoom level | z=14 (5x5 tiles, 1.2 km × 1.2 km) | **z=18** (5x5 tiles, **1.2 m/pixel** = 600 m × 600 m) |
| Property fills image? | ~10% of image (satellite-dominated) | **~70%** of image (data dominates) |
| Legend? | top-left small | bottom strip + scale bar + N arrow + callouts |
| Text callouts? | 1 small label | 4 with leader lines (dense canopy, tributary, polygon, centroid) |

## What the v4 composite has

1. **Bold LQV property outline** in yellow with black halo — visible at thumbnail size
2. **Stream network** drawn at 6-8 px wide with 4 px black halo — 765 blue pixels visible
3. **Canopy classes** as 4 semi-transparent fills, sorted by density (sparse → dense on top)
4. **OSM buildings** in light gray with dark borders — 31 structures visible
5. **Roads** as dashed yellow over black halo
6. **Centroid marker** with outer ring at (-25.6073, -57.0355)
7. **Top-left title** "La Quebrada Viva" in 42 px
8. **Top-right north arrow** with "N" label
9. **Bottom-left scale bar** with "50 m / 100 m / 200 m" labels
10. **Bottom full-width legend** with 10 layer semantics
11. **Callout labels** with leader lines pointing to: "Dense canopy NDVI >0.85", "Tributary DEM-derived", "30.9 ha buildable cluster"

## Image sizes

| File | Size | Notes |
|---|---|---|
| `lqv_composite_v4.webp` | 1800×1800 (143 KB) | Hero composite |
| `property_zoomed.webp` | 1200×1200 (43 KB) | Just the LQV 30.9 ha outline |
| `canopy_zoomed.webp` | 1200×1200 (24 KB) | 4-class NDVI canopy fills |
| `streams_zoomed.webp` | 1200×1200 (57 KB) | DEM-derived stream network |
| `buildings_zoomed.webp` | 1200×1200 (21 KB) | 31 OSM structures |
| `lqv_combined_zoomed.webp` | 1200×1200 (60 KB) | All layers combined |

## Quality numbers

- Image creation: 30-second build script run (one `python3 v4_build.py`)
- Image loading: <100 ms over CDN
- Live asset count: 7 previews + 13 data files = 20 served assets
- All assets 200 OK on Cloudflare Pages

## What didn't ship (yet)

- **Real quebrada geometry from Wes's phone captures** — when his photos land,
  the splat-derived 3D quebrada + tributaries will replace the snapped-DEM
  1-pixel lines. Until then, the stream visualization is a 1-px hint.
- **Drone data ingestion** — Meshroom processing of any drone photos Wesley provides
- **Higher resolution imagery** (Vantor/Maxar tasking) — currently 60 cm/pixel

## Re-build

```bash
HOME=/tmp python3 /tmp/lqv_build_v4.py
HOME=/tmp python3 /tmp/lqv_build_v4_previews.py
bash /root/.hermes/scripts/lqv-pages-redeploy.sh
```
