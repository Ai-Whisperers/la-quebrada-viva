# USER_ACTIONS — Satellite & Site-Data Build-Out

This file lists things only you (Ivan) can do or provide. The repo side of
the satellite pipeline is built and shipped — these are the human-side blockers
that the build-out spec calls out as TODO[user].

Open in Sublime, tick boxes as you complete them, and either drop files into
the paths below or paste credentials into `.env.local` as noted.

Last updated: 2026-06-17 (T-10 from escritura)

---

## TIER 0 — needed BEFORE escritura (next 10 days)

### [ ] 0.1  Cadastro padrón polygons  (priority: HIGH, source: Catastro Multifinalitario PY)

The shipped AOI is a rectangular bbox over the 6 padrones, NOT the actual
parcel boundary. Every fetcher and every Blender overlay is currently
clipping ~40% more land than we own.

**What I need from you:**
- A GeoJSON or shapefile with one polygon per padrón, with each feature
  carrying `properties.padron` matching one of:
  `838, 1827, 840, 1096, 629, 454`.
- CRS: WGS84 (EPSG:4326). If the cadastro hands you UTM 21S, that's fine —
  the loader reprojects.

**Where to get it:**
- Catastro Multifinalitario portal:  https://catastro.gov.py/  (consulta por padrón)
- Or hand-digitize from the cadastro PDF using QGIS over a Sentinel-2 base —
  takes ~30 min for all 6.
- Or ask the escribano: many escrituras include a cadastral plot PDF — that
  PDF can be georeferenced in QGIS in ~10 min.

**Where to put it:**
- Save as `docs/site_data/cadastro/padrones.geojson`
- Then run: `python -m scripts.satellite.fetch_cadastro --validate`

Until this lands, the scaffolded `parcel_polygon_geojson()` falls back to
the rectangular bbox and writes `parcel_polygon_pending: true` into every
metadata sidecar — so nothing breaks, but the deck claims "bbox approx"
instead of "true parcel boundary".

---

### [x] 0.2  Planet API key for NICFI basemaps  (priority: HIGH, free) — supplied 2026-06-17

The NICFI fetcher (`fetch_nicfi.py`) needs your Planet account API key to
pull 5 m basemap tiles for the deck. License is CC-BY-NC — deck-only,
never resale.

**What I need from you:**
- Sign up at  https://www.planet.com/nicfi/  (free, non-commercial,
  approves usually <24 h)
- Once approved, copy the API key from  https://www.planet.com/account/

**Where to put it:**
- Append to `.env.local`:
  ```
  PLANET_API_KEY=<paste-here>
  ```
- Then run: `python -m scripts.satellite.fetch_nicfi --list-mosaics`
  to confirm and pick the mosaic month for the deck.

---

### [ ] 0.3  GPS-tagged ground-truth photos (priority: MEDIUM, free, ~30 min)

The remote sensing rasters are useless without one round of ground-truth.
~20 photos taken from your phone, tagged with GPS (auto on iPhone/Android),
covering the diversity of the parcel:

- 4× cerrado / open grassland
- 4× quebrachal (closed canopy)
- 4× gallery forest along Arroyo Mbopicuá
- 4× pasture / disturbed
- 2× of each visible building / corral / road junction

**Where to put it:**
- Drop the originals into `docs/site_data/ground_truth/photos/`
- They get auto-indexed by `scripts/satellite/index_ground_truth.py`
  (next sprint) which extracts EXIF GPS + writes a GeoJSON points file.

This anchors the WorldCover / MapBiomas validation and gives Wesley something
non-AI to look at during the meeting.

---

### [ ] 0.4  DJI Mini 4 Pro drone flight (priority: HIGH if available, NICE-TO-HAVE if not)

A single 30-minute autonomous drone flight at 80 m AGL produces a
cm-scale orthomosaic + photogrammetric DEM that makes every satellite
product look like a Picasso by comparison. Sub-250 g, no Paraguay visa
or legal risk.

**What I need from you:**
- Schedule a clear-weather day before 2026-06-27.
- Fly the 62-ha parcel at 80 m AGL, ~75% overlap front + side, nadir camera,
  cloudy / overcast day if possible (reduces shadow).
- Export the raw photos folder (~300-500 JPEGs).

**Where to put it:**
- Drop the photo folder into `docs/site_data/drone/raw_YYYY-MM-DD/`
- I'll process via WebODM (already scripted in `scripts/drone_orthomosaic.py`,
  to be written next sprint) into orthomosaic + DEM + 3D mesh.

If this can't happen pre-escritura, it's not a blocker — Sentinel-2 + NICFI
+ ALOS DEM is enough for the deck. But the post-escritura sprint will treat
it as item #1.

---

## TIER 1 — needed POST escritura (for the operational data layer)

### [~] 1.1  GEE service-account JSON  (priority: MEDIUM, for CI automation) — partial

**Status 2026-06-17:** commercial-use registration is DONE — account is
`weissvanderpol.ivan@gmail.com` (Admin, Paraguay). Interactive auth via
`earthengine authenticate` now works for local runs. The remaining piece
is the service-account JSON for unattended CI refresh.

Right now `gee_quickstart.py` uses interactive auth (your laptop only).
For CI to automatically refresh NDVI composites, MapBiomas, and S1
coherence each month, we need a GCP service account with Earth Engine API enabled.

**What I need from you:**
- Create a GCP project (or use an existing one).
- Enable Earth Engine API.
- Create a service account, grant it Earth Engine User.
- Download the JSON key.
- (Commercial-use registration: DONE 2026-06-17.)

**Where to put it:**
- Drop the JSON at  `~/.gcp/lqv-gee-sa.json`  (NOT in the repo — gitignored)
- Add to `.env.local`:
  ```
  GOOGLE_APPLICATION_CREDENTIALS=/home/ai-whisperers/.gcp/lqv-gee-sa.json
  EE_PROJECT=<your-gcp-project-id>
  ```
- For the GitHub Actions data-freshness workflow:
  - Add repo secret `GEE_SERVICE_ACCOUNT_JSON` = full contents of the JSON
  - Add repo secret `EE_PROJECT` = your project ID

---

### [ ] 1.2  MapBiomas Paraguay access  (priority: LOW, free, no signup)

MapBiomas LCC for Paraguay (30 m annual landcover since 1985) is fully
open via GEE asset `projects/mapbiomas-public/assets/PARAGUAY/...`.
No credentials needed, BUT it requires GEE auth (TIER 1.1).

**What I need from you:**
- Nothing — the fetcher works as soon as TIER 1.1 is done.
- Just confirm you're OK with the citation we use in the deck:
  "MapBiomas Project — Collection 2 of annual land cover and land use
  maps of Paraguay, accessed on YYYY-MM-DD through the link: mapbiomas.org"

---

## TIER 2 — decision items (I'll default if you don't reply)

### [ ] 2.1  Pick the NICFI mosaic month for the deck

Once you give me `PLANET_API_KEY`, I'll run `--list-mosaics` and pick the
**most recent cloud-free mosaic over our AOI** as the deck base layer.

**Default if you don't reply:**
- Most recent mosaic month with <10% AOI cloud occlusion.

### [ ] 2.2  Pick the NDVI year window for the deck

The multi-year NDVI stack covers 2018-2026. The deck shows ONE composite.

**Default if you don't reply:**
- 2025-08-01 → 2026-04-01 (most recent full dry season + green-up — shows
  the parcel in transition state, which is the most visually informative).

### [ ] 2.3  Hansen GFC year cutoff for "loss since LQV bought"

Hansen runs 2000-2024. We can highlight loss in years matching your
property history.

**Default if you don't reply:**
- Show full 2000-2024 loss; annotate "0 ha loss within parcel" if true
  (sanity check the rasters first).

---

## What I'll handle without bothering you

(Listed so you know the build-out is real and the work is being done.)

- Metadata sidecars on every output (`<file>.meta.json` with timestamp,
  source asset HREF, fetcher git SHA, SHA-256, license, citation).
- License-gate enforcement (CC0 + CC-BY 4.0 only allowed in bundle;
  CC-BY-NC like NICFI flagged deck-only; CC-BY-SA blocked).
- CRS normalization (every raster reprojected to EPSG:32721 / UTM 21S).
- STAC item-ID pinning for reproducibility.
- Sentinel-2 cloud-shadow buffering (30 m dilation of SCL classes 3, 8, 9, 10).
- Retry/resume for long downloads (CHIRPS daily, NICFI tiles).
- Tests: AOI bbox lock-in, license gate raises on banned licenses,
  every fetcher `--help` exits 0.
- CI monthly freshness check (collections + mosaics still alive).
- Multi-year NDVI stack with p10/p50/p90 stats.
- GEDI L4A above-ground biomass fetcher.
- Sentinel-1 InSAR coherence (illegal-clearing alert).
- GLO-30 vs ALOS DEM hydrology comparison.
- Blender wiring (WorldCover → procedural material in `lqv/site/`).
- Bundle data manifest walking all meta.json sidecars.
- DATA_INVENTORY.md §12 (sidecar schema) + §13 (this file's pointer).

---

## Questions I've decided for you (per "decide-and-document" autonomy)

These are engineering calls I made without asking. Override if any is wrong.

- **Canonical projection** = EPSG:32721 (WGS84 UTM 21S, +south). Covers Paraguay.
- **License whitelist** = CC0-1.0, CC-BY-4.0. CC-BY-NC = deck-only flag.
  CC-BY-SA = BLOCKED (viral license would force open-sourcing the deck).
- **Multi-year NDVI window** = 2018-01-01 → today, daily Sentinel-2 SR HARMONIZED.
- **S2 cloud filter** = SCL keep {4,5,6,7,11}, drop {3,8,9,10} + 30 m dilation.
- **MapBiomas collection** = latest Paraguay collection at run time
  (currently C2, 30 m, 1985-now).
- **Hansen tile** = `20S_060W` (covers our AOI by construction).
- **GEDI window** = 2019-04-18 (mission start) → 2023-03-16 (last shot).
- **S1 coherence period** = 12-day pairs, ASCENDING orbit (descending has shadow on the quebrada).
- **DEM canonical** = ALOS AW3D30 for renders (already in use), GLO-30 for
  hydrology comparison only.

If any of these are wrong, just tell me which one and I'll flip it.
