# LQV viewer — open task list (2026-07-05)

Grounded in the v19 audit. Prioritized by user-visible impact.
Status legend: ☐ todo · ◐ in-progress · ☑ done · ✕ blocked/cancelled

> **⚠️ 2026-07-06 update (Erebus):** `splats/exports/web/mapa-10km.html` was renamed to `splats/exports/web/mapa.html` with a radius picker (parcel / 5 / 10 / 20 / 30 km). Old URLs (`mapa-10km.html`, `mapa-20km.html`) → meta-refresh redirect to `mapa.html` (and `?r=20`). All task locations below should be updated when accessed. Refactor rationale: single source of truth for the map viewer, with the radius-as-a-setting rather than two separate files.

---

## P0 — critical (visible to user today, actually broken)

### P0-1 ☐ Lower DEM quebrada headwater threshold so the user's quebrada shows
- **What**: DEM quebrada stream network uses headwater threshold of **80 cells (≥2.6 km²)**. The LQV quebrada's catchment is ~0.1-0.2 km². **0 streams cross the parcel, 0 flow arrows inside.**
- **Where**: `scripts/build_10km_layers.py:623-633` (extract_streams thresholds)
- **Acceptance**: ≥1 DEM quebrada stream crosses the parcel; ≥5 flow arrows inside the polygon at z=14+
- **Estimate**: 30 min — patch the threshold tuple, re-run `python3 scripts/build_10km_layers.py`, run cleaner, deploy
- **Tests**: visual check at z=14 on parcel; re-run parcel-containment script

### P0-2 ☐ Re-extract NDVI canopy from a true 10 km Sentinel-2 mosaic
- **What**: `ndvi_canopy_10km.geojson` was built from a 62 ha parcel-extended AOI raster that has NaN outside the parcel. File is 10 km-named but **0 of 743 polygons intersect the parcel**. The label is misleading.
- **Where**: `scripts/build_10km_layers.py` — replace the source raster reference
- **Acceptance**: ≥1 NDVI polygon intersects the parcel; values at centroid cross-check with the 0.78 NDVI implied by MapBiomas Forest class 3
- **Estimate**: 1 hour — fetch new Sentinel-2 from MS Planetary Computer, mosaic to 10 km box, classify
- **Tests**: verify centroid NDVI matches Hansen 98% canopy × MapBiomas class 3

### P0-3 ☐ Add "Coverage" indicator to every layer row
- **What**: Layer rows show counts (e.g. "5,510 polygons") but don't say **how many intersect the parcel**. The user can't tell at a glance whether a layer is actually useful for the property vs. just regional context.
- **Where**: `splats/exports/web/js/lqv-inline.js` — extend `setLayerCount()` to show "X · Y inside parcel"
- **Acceptance**: every layer row in sidebar shows total + inside-parcel count. Hidden layers (off by default) show count only on hover or when toggled.
- **Estimate**: 1 hour — add parcel-poly check in JS, count features per layer once on load
- **Tests**: hover each layer in the sidebar — confirm count appears

### P0-4 ☐ Fix tooltip precision overflow
- **What**: Already capped to 2 decimals in v19 for MapBiomas + woodland-merged. But the **Hansen loss/gain tooltips use `areaHa.toFixed(1)` which is fine for area**, but the lat-aware shoelace approximation can still show wildly wrong values for tiny patches near the equator. Need to verify + cap.
- **Where**: `splats/exports/web/mapa-10km.html` — verify lines around 1426, 1465 (the Hansen handlers)
- **Acceptance**: every tooltip shows "X.X ha" with the X being reasonable for the polygon size
- **Estimate**: 20 min
- **Tests**: hover several small Hansen polygons, verify ha values are sane

### P0-5 ☐ Confirm parcel-zoom mode hides layers that don't fit
- **What**: At z=15+ on the parcel, regional layers (Hansen, MapBiomas, big-area OSM) become visual noise. Auto-hide them when z>14 on a small bbox.
- **Where**: `splats/exports/web/js/lqv-inline.js` — add `map.on('zoomend')` handler
- **Acceptance**: when user zooms past z=14 inside the parcel bbox, MapBiomas + Hansen layers dim to 30% opacity or hide; on zoom-out, restore
- **Estimate**: 45 min
- **Tests**: visual at z=12 vs z=15

---

## P1 — important (improves correctness, no new bugs)

### P1-1 ☐ Add HAND (Height Above Nearest Drainage) layer
- **What**: HAND is the standard wetland-floodplain mapper. Current JRC 30m misses 5-25m quebradas; HAND at 30m + D8 drainage direction catches the property-scale hydrology.
- **Where**: new `scripts/build_hand.py`
- **Acceptance**: HAND raster covering 10 km box, classified into 5 bins (0-1m, 1-5m, 5-15m, 15-30m, >30m) — polygonised as 4,000-6,000 features
- **Estimate**: 4 hours (DEM fetch + D8 already exists, just compute HAND)
- **Tests**: pixel at LQV centroid should be in 5-15m bin (steep slope) but quebrada-adjacent pixels in 0-1m

### P1-2 ☐ Extract a "Local Quebradas" layer from Wes's GPS path
- **What**: The user's walking track hugs the quebrada. We can derive the quebrada polyline from the GPS path + a 5 m buffer to identify "side-of-quebrada" walks.
- **Where**: `scripts/build_client_gps_layers.py` — extend or new script
- **Acceptance**: a Quebrada polyline feature with attributes for upstream/downstream, visible as a thick gold line in the parcel
- **Estimate**: 2 hours
- **Tests**: visual at z=16 — line traces the quebrada visibly

### P1-3 ☐ Re-pull OSM with `natural=stream` (not just `waterway`)
- **What**: Currently `osm_10km/waterways.geojson` has 182 features but 0 cross the parcel. Many small quebradas are tagged only as `natural=stream` (not `waterway=stream`).
- **Where**: `scripts/fetch_osm_10km.py` — add a new query
- **Acceptance**: ≥1 natural=stream feature crosses the parcel
- **Estimate**: 30 min
- **Tests**: visual + parcel-intersection count

### P1-4 ☐ Add NDVI legend with actual class thresholds
- **What**: Currently the legend says `< 0.25 bare/grass`. The build script actually uses `<0.25 / 0.25–0.45 / 0.45–0.60 / >0.60`. Verify and align.
- **Where**: `splats/exports/web/mapa-10km.html` (legend) and `scripts/build_10km_layers.py` (thresholds)
- **Acceptance**: legend matches actual thresholds exactly
- **Estimate**: 10 min
- **Tests**: hover a polygon of each class, verify tooltip class matches legend

### P1-5 ☐ Service worker: cache OSM tile prefix
- **What**: SW currently skips external origins (OSM, Esri). On second visit, every pan/zoom re-fetches tiles. Cache the first 100 tiles per session.
- **Where**: `splats/exports/web/sw.js` — add a "tile cache" with LRU eviction
- **Acceptance**: second visit within 30 days doesn't re-fetch tiles already seen
- **Estimate**: 3 hours
- **Tests**: open DevTools → Application → Cache Storage → verify OSM tiles present

### P1-6 ☐ Show parcel scale + cursor elevation in real-time
- **What**: At cursor hover, show DEM elevation / slope / aspect. The parcel is at 213 m / 17.6% slope / S aspect — meaningful info for a buyer.
- **Where**: `splats/exports/web/js/lqv-inline.js` — add `map.on('mousemove')` + DEM-sample
- **Acceptance**: small bottom-left HUD shows lon/lat/elev/slope/aspect at cursor
- **Estimate**: 4 hours (need DEM sampling in JS, or pre-compute a 256-tile elevation service)
- **Tests**: hover various points, verify values change

---

## P2 — quality of life (nice to have)

### P2-1 ☐ Add a "Property Coverage Matrix" in About section
- **What**: A small table showing layer × inside-parcel count. Honest disclosure.
- **Where**: `splats/exports/web/mapa-10km.html` About section
- **Acceptance**: a 6-column table: layer / total features / inside parcel / sources / last updated / license
- **Estimate**: 1 hour

### P2-2 ☐ Mobile drawer polish
- **What**: The mobile sidebar drawer works but has some overlap with the map zoom controls. Polish it.
- **Where**: `splats/exports/web/mapa-10km.html` CSS + drawer handlers
- **Acceptance**: mobile view (375×667) — drawer slides cleanly, no overlap with map controls
- **Estimate**: 2 hours

### P2-3 ☐ Improve the walking-track replay UX
- **What**: The replay button works but the user can't tell how long it'll take. Show estimated duration + a progress indicator.
- **Where**: `splats/exports/web/js/lqv-inline.js` replay handler
- **Acceptance**: clicking "Replay walk" shows a progress bar + remaining time
- **Estimate**: 1 hour

### P2-4 ☐ Add a "share" button that copies URL with current state
- **What**: Currently URL state is set via `#z=12&l=parcel,streams-10km...`. There's no UI for users to grab a shareable link.
- **Where**: Actions section + JS handler
- **Acceptance**: clicking "Share view" copies current URL to clipboard, shows toast
- **Estimate**: 30 min

### P2-5 ☐ Print-friendly view
- **What**: `@media print` CSS that hides the sidebar, makes the map full-width, removes animations. For sending PDF to a buyer.
- **Where**: `splats/exports/web/mapa-10km.html` `<style>`
- **Acceptance**: Ctrl+P shows clean map with title + scale + legend visible
- **Estimate**: 1 hour

### P2-6 ☐ Add per-layer opacity persistence to localStorage
- **What**: User changes stream opacity to 0.6 → reload → resets to default 0.85. Save/restore.
- **Where**: `splats/exports/web/js/lqv-inline.js` opacity handler
- **Acceptance**: opacity changes persist across page reloads
- **Estimate**: 30 min

### P2-7 ☐ Add MapBiomas forest-change timeline (1985 → 2023)
- **What**: We have MapBiomas rasters for 1985, 2000, 2005, 2010, 2020, 2023. Build a "forest cover 1985 vs 2023" comparison layer.
- **Where**: new `scripts/build_forest_change_timeline.py`
- **Acceptance**: a toggle "Forest change 1985-2023" that highlights polygons that lost/gained forest
- **Estimate**: 4 hours

### P2-8 ☐ Add "Annotations" layer for hand-marked features
- **What**: User mentioned waterfall, gate, summit — those are already in `client_gps_features`. But allow free-form annotations (e.g. "good camping spot", "flood line").
- **Where**: `splats/exports/web/js/lqv-inline.js` — annotation drawing tool
- **Acceptance**: user can click on map → enter note → it persists in localStorage as a yellow pin
- **Estimate**: 3 hours

### P2-9 ☐ Property-detail mode (URL: `#parcel`)
- **What**: A simplified single-page view focused only on the parcel, with just GPS data + MapBiomas + NDVI + DEM. Hides everything else. Useful for buyer emails.
- **Where**: new `mapa-parcel.html` (smaller sibling of mapa-10km.html)
- **Acceptance**: opens directly at z=16 on the parcel, only 4 toggles, less than 200 KB
- **Estimate**: 4 hours (mostly a stripped-down copy of mapa-10km.html)

---

## P3 — maintenance / cleanup (no user-visible change but important)

### P3-1 ☐ Consolidate the 12 active build scripts into 1 orchestrator
- **What**: Right now you have to remember the run order (fetch_osm_10km → build_10km_layers → build_hillshade → build_dem_contours → build_10km_fullcover → build_woodland_merged → build_client_gps → audit_wetlands_10km → audit_jrc_waterbodies → build_combined_waterway → clean_geometries). Build a single `make_all.py` or `make.py` Makefile target.
- **Where**: new `scripts/make.py`
- **Acceptance**: `python3 scripts/make.py` rebuilds everything from scratch in correct order
- **Estimate**: 2 hours

### P3-2 ☐ Add a smoke-test script that validates the deployed data
- **What**: After every rebuild, verify counts match expectations, all geojsons valid, all files ≤25MB.
- **Where**: new `scripts/smoke_test.py`
- **Acceptance**: `python3 scripts/smoke_test.py` exits 0 if all data passes, non-zero otherwise
- **Estimate**: 2 hours

### P3-3 ☐ Add CI (GitHub Actions) to run smoke_test.py + the audit on every commit
- **What**: Catch regressions before they reach the deployed map.
- **Where**: `.github/workflows/lqv-viewer-ci.yml`
- **Acceptance**: PRs failing if any data file fails the audit
- **Estimate**: 3 hours

### P3-4 ☐ Move scripts/_archive/ contents to a separate branch or repo
- **What**: 71 archived Python files (26K LOC) bloat the main repo. Move to `lqv-archive` branch or repo.
- **Where**: git branch + git-filter-repo
- **Acceptance**: `git clone https://github.com/Ai-Whisperers/la-quebrada-viva` produces a slim repo with only the 12 active scripts + deploy
- **Estimate**: 1 hour

### P3-5 ☐ Add a `LICENSE` file
- **What**: Currently the repo has no LICENSE. The viewer is CC-BY-4.0 for data but the code license is undefined.
- **Where**: `LICENSE` at root
- **Acceptance**: MIT for code, CC-BY-4.0 for data
- **Estimate**: 5 min

### P3-6 ☐ Add data-provenance manifest
- **What**: A `DATA_PROVENANCE.md` documenting every data source, license, date acquired, processing steps.
- **Where**: `docs/DATA_PROVENANCE.md`
- **Acceptance**: every GeoJSON in deploy dir has a corresponding provenance entry
- **Estimate**: 2 hours

### P3-7 ☐ Backfill `client_gps_corner` etc. with metadata about Wes's walks
- **What**: `client_gps_corners.geojson` has the 17 corners but no metadata about which walking session they came from.
- **Where**: `scripts/build_client_gps_layers.py` — add `walk_session` field
- **Acceptance**: each corner has `walk_session: '06-22'` or `'06-28'`
- **Estimate**: 30 min (already partly done in `walk_session` property)

### P3-8 ☐ Add a script that pulls latest OSM monthly (not just on demand)
- **What**: New buildings, new roads, etc. appear in OSM monthly. A cron job could refresh.
- **Where**: new `scripts/cron_refresh_osm.py` + cron entry
- **Acceptance**: cron job runs monthly, pushes updated osm_10km/ to repo
- **Estimate**: 2 hours

---

## Won't do (explicit non-goals)

- ❌ **Replace Leaflet with MapLibre GL / deck.gl** — would require a 1-week refactor; the canvas renderer already handles 21K features at 60fps
- ❌ **Add user accounts / login** — this is a public context map, not a private portal
- ❌ **Implement real-time data streaming** — none of the data sources provide streaming
- ❌ **Make a mobile app** — the viewer is responsive enough for mobile browser
- ❌ **Translate to Spanish UI** — possible later if a Spanish-speaking buyer needs it; current sidebar is technical English

---

## Total estimated effort

| Priority | Tasks | Hours |
|---|---|---:|
| P0 | 5 | ~4 hours |
| P1 | 6 | ~16 hours |
| P2 | 9 | ~17 hours |
| P3 | 8 | ~13 hours |
| **Total** | **28 tasks** | **~50 hours** |

Two days of focused work to clear P0 + P1. One week to clear everything through P2. P3 is steady-state maintenance.

---

## What I'd actually do (if given 1 week)

Week 1 priorities, in order:

1. **P0-1** (30 min) — lower DEM quebrada threshold. Single biggest win.
2. **P0-3** (1 hour) — Coverage indicator on every layer.
3. **P1-2** (2 hours) — Local Quebradas from GPS path.
4. **P1-1** (4 hours) — HAND layer for wetlands.
5. **P0-2** (1 hour) — re-extract NDVI from 10 km Sentinel-2.
6. **P1-3** (30 min) — natural=stream OSM re-pull.
7. **P2-1** (1 hour) — Property Coverage Matrix in About.
8. **P2-7** (4 hours) — Forest change 1985→2023 timeline.
9. **P2-9** (4 hours) — mapa-parcel.html for buyer emails.
10. **P3-1** (2 hours) — `make.py` orchestrator.
11. **P3-2** (2 hours) — `smoke_test.py`.
12. **P3-6** (2 hours) — DATA_PROVENANCE.md.

After that, the viewer goes from "regional context" to "property-scale decision tool" and the documentation is auditable.