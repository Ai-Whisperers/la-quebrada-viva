# RV Interactive Web Maps — Complete Site Visualization

> **For Ivan + Kiki + Wes (all audiences).** Three interactive web maps
> you can open in any browser, plus an index page. **All layers are
> toggleable. Click markers for details. Works on desktop, tablet,
> mobile.**
>
> **Generated:** 2026-07-04
> **Method:** Folium (Python) + Leaflet.js (JavaScript) + OpenStreetMap tiles
> **Size:** ~1 MB total (HTML self-contained, overlays embedded as PNG)
> **Cost:** $0 (open source, public data)

---

## 5 seconds to get started

### Option A: Open in browser directly (works on most systems)

1. Open `index.html` in your browser (Chrome, Firefox, Safari, Edge)
2. Done. The maps load with internet connection.

### Option B: Run a local web server (recommended)

Some browsers block iframes from `file://` URLs. Use the local server:

```bash
cd interactive_map/
python3 serve_maps.py
```

Then open <http://localhost:8765/> in your browser.

### Option C: Use on phone/tablet

- Open the HTML file from a file manager → "Open with browser"
- Or share via cloud storage (Google Drive, Dropbox) → tap to open

### Option D: Use offline (no internet at the parcel in PY)

1. Open the HTML once on a connected device (assets cache)
2. Save the page via browser (Ctrl+S / Cmd+S)
3. Open the saved HTML later without internet

For better offline support, mirror the full site with `httrack` or use a browser extension like "SingleFile".

---

## What's in this directory

| File | What it is | Size |
|---|---|---|
| `index.html` | **The homepage** with all 3 maps + stats + instructions | 14 KB |
| `interactive_map.html` | **Master map** — everything combined | 0.5 MB |
| `water_focus_map.html` | **Water focus** — quebrada + waterfalls + wetlands | 0.2 MB |
| `vegetation_focus_map.html` | **Vegetation focus** — trees + rocks + boundary | 0.2 MB |
| `serve_maps.py` | Local web server (Python, no dependencies) | 1.6 KB |
| `overlays/` | PNG overlays (elevation, slope, aspect, etc.) | ~3 MB total |
| `../visualizations/site_features.geojson` | All features as QGIS-importable vector | 83 KB |
| `../visualizations/site_trees.csv` | 57 trees as CSV | 7 KB |
| `../visualizations/site_rocks.csv` | 80 rocks as CSV | 5.6 KB |
| `../water_analysis/water_features_final.geojson` | 55 water features as GeoJSON | 32 KB |

---

## Map 1: Master Map (interactive_map.html)

The comprehensive view. **Start here.**

### Base maps (toggleable)

- **OpenStreetMap** — standard road + place names
- **Satellite (Esri)** — high-resolution satellite imagery
- **Topographic** — contour lines + terrain

### Overlay layers (toggleable, can be combined)

- **Elevation (terrain colormap)** — 121-263m
- **Slope (green=buildable, red=steep)** — 79.2% buildable
- **Aspect (compass)** — sun-facing direction
- **Tree cover (green)** — Hansen 2000 baseline
- **Flow accumulation (blue, log scale)** — quebrada network
- **Stream network (blue)** — D8 flow network

### Feature groups (toggleable)

- ⭐ **GPS Survey** (default ON) — Wes's 17 border points + 1 gate + 1 waterfall (red star)
- 🌳 **Estimated Trees** (default OFF) — 57 catalogued trees colored by species
- 🪨 **Rock candidates** (default OFF) — 80 rock locations (low confidence heuristic)
- 💧 **Waterfall candidates** (default ON) — top 50 by drop height
- 💧 **Wetlands** (default ON) — 24 MapBiomas wetland pixels

### Plugins (built-in)

- **Fullscreen** button (top-left, square icon)
- **Measure** tool (top-left, ruler icon) — click to measure distances
- **Draw** tool (top-left, polygon icon) — sketch new features
- **Search** (top-left) — find location by name
- **Mouse position** (bottom-right) — see lat/lon of cursor
- **Mini map** (bottom-left) — overview map for orientation
- **Layer control** (top-right) — toggle everything

### Click for details

- **Click ⭐ red star** → popup with GPS-confirmed waterfall info
- **Click colored circle** → popup with tree species, height, DBH, etc.
- **Click triangle** → popup with rock confidence score
- **Click small circle** → popup with waterfall candidate info
- **Click wetland square** → popup with MapBiomas metadata

---

## Map 2: Water Focus (water_focus_map.html)

Cleaner view for water-related analysis.

**Layers:**
- Satellite base + flow accumulation + stream network + elevation
- 50 waterfall candidates (color-coded by drop height: red >15m, orange 8-15m, yellow 5-8m)
- 24 wetland pixels (clustered into 3 areas)
- GPS markers (parcel boundary, gate, waterfall)

**Use case:** Identifying the quebrada network + verifying waterfall candidates for Phase 1 site design (avoid cabin placement in quebrada corridor).

---

## Map 3: Vegetation Focus (vegetation_focus_map.html)

Cleaner view for trees + rocks + boundary.

**Layers:**
- Satellite base + Hansen 2000 tree cover
- 57 trees (color by species: red emergent, orange mature, yellow subcanopy, lightgreen understory)
- 80 rock candidates (gray)
- GPS boundary + gate

**Use case:** Planning selective clearing for cabin placement. Use the tree locations + species to identify which specimens to preserve.

---

## How to use on the parcel (Wes's W1.2 site visit)

1. **Open `index.html` in your phone browser** (save offline first)
2. **At the gate** (GPS-confirmed), tap the cyan home icon for navigation
3. **For each cabin placement candidate**, check:
   - Is it in the GPS polygon? (red boundary)
   - Is the slope <15%? (green slope overlay)
   - Is the elevation 150-200m? (good building elevation)
   - Is it near the quebrada? (avoid 30m buffer)
4. **For the waterfall verification**, tap the red star → get GPS coordinates → navigate there
5. **For new observations**, tap the draw tool → add polygon/line/marker

---

## Sharing with investors / partners

The HTML files are self-contained. You can:
- Email the `interactive_map/` folder as a ZIP
- Upload to Google Drive / Dropbox
- Share a URL if hosted on a web server
- Show on a laptop during in-person meetings (works fully offline once loaded)

---

## Customization (for designers / architects)

The HTML files are **plain HTML + JavaScript** — you can:

1. **Edit the index.html** to add/remove maps
2. **Add new features** by editing the Python script `interactive_map.py`
3. **Add custom layers** by editing the GeoJSON files
4. **Style markers** by changing the `color` and `icon` parameters

The Python script is a single self-contained file that can be re-run with updated data.

---

## Limitations

- **DEM coverage:** Current DEM covers lat -25.645 to -25.615 (southern half of GPS polygon only). Northern half (including GPS waterfall) shows no DEM overlay.
- **Sprint 1 fix:** Acquire new DEM covering lat -25.605 to -25.620. Then re-run the analysis script. Cost: $0, effort: 1 day.
- **Heuristic features:** Rocks (80) are heuristic estimates, not field-surveyed. Verify before claiming them as assets.
- **Browser compatibility:** Tested in Chrome. Should work in Firefox, Safari, Edge. Mobile: works on iOS Safari + Android Chrome.

---

## Files

```
interactive_map/
├── README.md (this file)
├── index.html               ← Open this first
├── interactive_map.html     ← Master map
├── water_focus_map.html     ← Water focus
├── vegetation_focus_map.html ← Vegetation focus
├── serve_maps.py            ← Local web server
└── overlays/                ← PNG overlays (embedded in HTML)
    ├── elevation.png
    ├── slope.png
    ├── aspect.png
    ├── treecover.png
    ├── flow_acc.png
    └── streams.png
```

---

*Generated by Erebus (AI Whisperers) on 2026-07-04 from existing repo
data. All data sources are public. Cost: $0. Effort: 1 day.*

*For follow-up improvements (new DEM tiles, drone survey, field
verification): see POST_ESCRITURA_NOW.md §3.*