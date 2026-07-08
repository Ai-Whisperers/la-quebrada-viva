# La Quebrada Viva — 3D Map Upgrade Plan

**Date:** 2026-07-08
**Engine target:** CesiumJS (browser, no GPU) + UE5.7 (production, GPU server)
**Current state:** Phase 2 complete — `escobar3d.html` live with 3-tier LOD terrain

This document tracks every upgrade queued for the LQV 3D viewer. Each item
has a status (✅ done · 🔄 in progress · ⏳ queued · 🚫 blocked) and the
URL where it lives.

---

## Phase 1 — Visual upgrades (no new data needed)

| # | Item | Status | Deliverable |
|---|---|---|---|
| 1.1 | Hillshade overlay toggle | 🔄 next | Add shaded-relief derived from heightmap (computed in JS from PNG16, no new fetch) |
| 1.2 | Contour lines toggle | 🔄 next | Generate 10 m contours client-side from heightmap via @turf/contour |
| 1.3 | Camera presets (top/south/oblique) | ⏳ | Buttons: top-down, oblique south, oblique north, oblique cliff |
| 1.4 | Distance ruler tool | ⏳ | Click two points → show geodesic distance in metres |
| 1.5 | 3D compass widget | ⏳ | Replace 2D Cesium compass with custom HTML widget showing bearing + pitch |
| 1.6 | Mini-map (overview inset) | ⏳ | Bottom-right 200×150 inset showing where you are on the AOI |
| 1.7 | Help overlay (first visit) | ⏳ | Modal: "Drag to rotate, right-click drag to zoom, scroll to zoom" |
| 1.8 | Loading spinner | ⏳ | Show while LOD tiles load |
| 1.9 | Smooth LOD transitions | ⏳ | Fade between LOD heights instead of snap-switch |
| 1.10 | Day/night sun (Cesium clock) | ⏳ | Use real LQV time + sun position |

## Phase 2 — Data upgrades (require fetching new public datasets)

| # | Item | Status | Notes |
|---|---|---|---|
| 2.1 | Sentinel-2 NDVI as biome layer | ⏳ | Fetch 1 cloud-free scene, render as semi-transparent overlay |
| 2.2 | Hansen tree cover (forest loss animation) | ⏳ | 2000 → 2024 yearly layers, toggleable animation |
| 2.3 | MapBiomas land cover (6 classes color-coded) | ⏳ | 1985 vs 2023 toggle |
| 2.4 | Slope heatmap | ⏳ | Derive from LOD0 heightmap, color-code 0-15-30+% |
| 2.5 | Aspect (sun direction) heatmap | ⏳ | Derive from LOD0 heightmap, color-code N/NE/E/SE/S/SW/W/NW |
| 2.6 | Historical parcel borders | ⏳ | KML from Catastro if available |
| 2.7 | Power lines + utilities (ANTEL/ANDE) | ⏳ | OSM power=line features |
| 2.8 | Soil classification overlay | ⏳ | SoilGrids 250 m, color by clay/sand/pH |
| 2.9 | Climate normals overlay | ⏳ | CHELSA precipitation, fade between dry/wet season |
| 2.10 | Soil erosion risk (RUSLE-derived) | ⏳ | Combine slope + rainfall + land cover |

## Phase 3 — Narrative + interaction upgrades

| # | Item | Status | Notes |
|---|---|---|---|
| 3.1 | Hotspot tour mode | ⏳ | Guided 5-stop walk: gate → quebrada confluence → waterfall → high point → flat zone |
| 3.2 | Decision moment | ⏳ | "Where would you put the cob house?" — drop pin, validate against buildability |
| 3.3 | Compare modes (slider) | ⏳ | Before/after slider: Esri HD vs hillshade, 1985 vs 2023 |
| 3.4 | Share view via URL | ⏳ | Encode camera lon/lat/alt/pitch/heading as URL params, restore on load |
| 3.5 | Annotations | ⏳ | Click anywhere → add a note (saved to localStorage) |
| 3.6 | Print/export PNG | ⏳ | Save current view as PNG for reports |
| 3.7 | Bookmarkable locations | ⏳ | User saves favorite camera positions |

## Phase 4 — Production engine upgrade (UE5.7 + Cesium for Unreal)

| # | Item | Status | Notes |
|---|---|---|---|
| 4.1 | Provision GPU server | 🚫 blocked | Waiting on Hetzner token / cloud GPU access |
| 4.2 | Install UE 5.7 + Cesium plugin | 🚫 blocked | `tools/bootstrap_lqv_on_laptop.sh` or `tools/install_ue5_on_gpu.sh` |
| 4.3 | Run `build_lqv_level.py` | 🚫 blocked | Assembles LQV_Main.umap with Nanite landscape + house + waterfall |
| 4.4 | Package for Pixel Streaming | 🚫 blocked | `tools/deploy_lqv_pixstream.sh` on cloud GPU |
| 4.5 | Live embed `play.html` | ⏳ | Replace game launcher modal iframe with Pixel Stream iframe |
| 4.6 | First-person walkable | 🚫 blocked | After Pixel Streaming deploy |

---

## Live URLs

| URL | What | Status |
|---|---|---|
| `https://lqv-walkthrough.pages.dev/escobar3d` | **3D terrain viewer (LOD-switched)** | ✅ live |
| `https://lqv-walkthrough.pages.dev/cesium_preview` | Flat Cesium preview (validation) | ✅ live |
| `https://lqv-walkthrough.pages.dev/play` | Game launcher | ✅ live |
| `https://lqv-walkthrough.pages.dev/mapa` | Existing Leaflet 10 km map | ✅ live |
| `https://github.com/Ai-Whisperers/la-quebrada-viva` | Repo (commit `db90fba`) | ✅ |

## Critical numbers

| Metric | Value | Source |
|---|---|---|
| LOD0 parcel coverage | 1.5 km × 1.5 km @ 1.5 m/px | ALOS DEM + bilinear |
| LOD1 Escobar coverage | 7.7 km × 7.7 km @ 15 m/px | AWS terrain-rgb + bicubic |
| LOD2 regional coverage | 23 km × 23 km @ 60 m/px | AWS terrain-rgb (z=11) |
| Esri HD at LOD0 | 1.07 m/px, 1792×1792 | server.arcgisonline.com |
| Total lite bundle size | 11.03 MB, 30 files | post-deploy verified |
| Total repo game_assets | 67 MB, 39 files | pre-deploy source |
| Cloudflare Pages deploy | 141 files in 2.87s | wrangler output |

## Execution priority (this session)

Items I'll work on NOW (don't need GPU):

1. ✅ **1.1 Hillshade overlay** (computed client-side from LOD0 PNG)
2. ✅ **1.2 Contour lines** (using @turf/contour or custom D3 isolines)
3. ✅ **1.3 Camera presets** (4 buttons: top, south, north, cliff)
4. ✅ **1.4 Distance ruler** (click two points)
5. ✅ **1.7 Help overlay** (first-visit modal)
6. ✅ **1.8 Loading spinner** (per-LOD tile load)
7. ✅ **3.4 Share via URL** (camera params in URL)
8. ✅ **3.6 Print/export PNG** (Cesium scene → canvas → PNG)

After GPU server is available (separate session):

9. UE5.7 + Cesium for Unreal assembly
10. Pixel Streaming deploy
11. Live first-person walkable game

---

## Open questions

1. **Hillshade style?** Soft (multi-directional) vs hard (single sun) vs combined
2. **Contour interval?** 5 m, 10 m, 25 m? (regional USGS standard is 10 m or 20 ft)
3. **Camera presets by name?** "Approach from gate", "Above quebrada", "Cliff view", "Top-down planning"
4. **Annotations shared across users?** (would need backend, deferred)
5. **Cesium ion token?** Free Bing aerial or use local Esri only?