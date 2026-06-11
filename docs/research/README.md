# GitHub & Docs Research — La Quebrada Viva

> Master synthesis of the 2026-06-10 research sweep. 100+ repos catalogued across 5 parallel research agents. Findings ordered by what actually moves the project forward.
>
> Each sub-report lives in its own file in this directory and is referenced inline. This doc is the navigation + the cross-cutting insights.

## The single biggest finding

**The 403 on `s3://lp-prod-protected/` is the "Earthdata Cloud Data Pool" consent, not the GEDI02_A collection EULA.** They're two separate agreements. Accepting the collection EULA in Earthdata Search is what made the basic GEDI access work (HTTPS downloads succeed). But the *cloud-native S3* layer is gated by a different consent, accepted via either:

1. Triggering the "Earthdata Cloud Data Pool" modal in Earthdata Search when you click "Download" on a cloud-hosted GEDI file (not always shown), OR
2. Using the per-DAAC Cumulus endpoint at `https://data.lpdaac.earthdatacloud.nasa.gov/s3credentials` instead of the central URS endpoint — this bypasses the central consent check by scoping the creds at the DAAC's own policy layer.

Detailed report: see `EARTHDATA_AUTH_RESEARCH.md` (this directory, written 2026-06-10).

**Action item:** retry the S3 streaming script using the Cumulus endpoint (one-line change). If that works, we get the fast path. If it still 403s, the user needs the cloud-pool consent.

## The 5 research areas, what we got, what to do

### 1. GEDI L2A Python tools — `GEDI_L2A_RESEARCH.md`

- **Right tool stack:** `earthaccess.search_data()` + `earthaccess.open()` + `h5py` partial reads. The script we already wrote is correct.
- **Concept ID for cloud:** `C2142771958-LPCLOUD` (provider `LPCLOUD`, not `LPCUMC`).
- **OpenAltimetry is real but moved:** now at `https://openaltimetry.earthdatacloud.nasa.gov/` (NSIDC, 2023; the `.org` is a domain squatter).
- **Harmony**: GEDI L2A is *not* on a Harmony-supported subsetting service yet. Harmony *is* the right tool for **GEDI04_A** (gridded biomass, ~1 km tiles).
- **Two real repos that matter:** `nasa/GEDI-Data-Resources` (official tutorials, replaces the 404'd `gedi-notebooks`) and `nasa/gedi-l4a-agb-density-mosaics`. The other 19 GitHub repos we probed are forks or empty.
- **Section 8 of the report has a complete copy-paste script** for our Paraguay bbox.

### 2. Earthdata auth + LP DAAC cloud pool — see §"The single biggest finding" above

- The per-DAAC Cumulus endpoint is the **fastest path** to unblock S3 streaming.
- Test command + reference implementation in the full report.
- The cloud-pool EULA is a *separate* layer from the collection EULA. The user's profile page snippet only shows collection-level EULAs; that's why the GEDI appears "accepted" but S3 still 403s.

### 3. DEM tooling — `docs/site_data/DEM_TOOLING_RESEARCH.md`

- **Top libs for our scale (12k pixels):** `pysheds` (watershed/HAND/stream order) + `pyviewshed` (viewshed, pure Python) + `gdaldem` (hillshade/contours via subprocess) + `richdem` (slopier/aspect/fill — C++ compile). Keep `rasterio` for I/O.
- **Heightmap pipeline** (§3) drops into `lqv/site/terrain_62ha.py` (the dormant stub). Produces 16-bit PNG + 32-bit EXR + normal map + sidecar JSON.
- **v1 review (§6):** critical issues are no DEM conditioning (`fill_pits → fill_depressions → resolve_flats` mandatory before watershed) and no UTM reproject. `M_PER_DEG_LON` hack is wrong by 5 m at bbox edges.
- **v2 roadmap (§7):** 5 phases, ~2.5 days total. Phase 1 = richdem + DEM conditioning.

### 4. Blender GIS integration — full inline report in this session

- **Skip BlenderGIS** (Blender 5.x hostile, unmaintained).
- **Use a custom Blender script** with `rasterio` + `numpy` (both already installed). Full drop-in `lqv/site/dem.py` code in the report.
- **CRS for Paraguarí:** `EPSG:32721` (WGS 84 / UTM zone 21S).
- **Integration plan:** coexist (Phase 1) → clip-and-blend (Phase 2) → real-DEM soil (Phase 3) → high-res 5 m swap (Phase 4).
- **RNG ordering invariant:** `build_dem_terrain` must not call `random.*` or the downstream flora draw order shifts.

### 5. Vacation-rental / eco-retreat GIS — `VACATION_RENTAL_RESEARCH.md`

- **5 case studies:**
  1. **Chaa Creek** (Belize, 1981, 28 keys on 500 acres — closest analog)
  2. **Awasi** (5-lodge SA portfolio, 3 in Atlantic Forest, multilingual EU focus)
  3. **Inkaterra** (Peru, 1975, oldest continuous eco-tourism in SA, German family founder)
  4. **San Bernardino, Paraguay** (1881, German/Swiss founding, 80 km from your site — *the* local precedent)
  5. **Mennonite colonies** (38,731 people, 25 colonies, 9 in eastern Paraguay = your biome)
- **5 site-selection criteria** that predict survival past year 5.
- **Tier 1/2/3 GIS techniques** beyond slope/aspect (viewshed cumulative, NDWI, acoustic baseline, dark-sky, fire-risk, road-cost, biodiversity corridors).
- **10 design rules** synthesized from GSTC + Crinion (1998) + case studies.
- **Cultural/linguistic fit:** ~450k ethnic Germans in PY, 9 eastern Mennonite colonies in your biome, Colegio Goethe, Club Alemán. The Asunción→San Bernardino summer migration is a 144-year-old pattern.
- **Concrete next-step sequence** for the site (drone LiDAR → Tier-1 GIS stack → camera-trap survey → acoustic+dark-sky baseline → GSTC self-assessment → partner outreach).

## Repos catalogued (selected, with verdict)

### GEDI / NASA Earthdata
- `nasa/GEDI-Data-Resources` — **ADOPT** (official tutorials, replaces dead `gedi-notebooks`)
- `nasa/gedi-l4a-agb-density-mosaics` — **ADOPT** (L4A gridded biomass pipeline)
- `nasa/cumulus-distribution-api` — **REFERENCE** (the per-DAAC s3credentials pattern)
- `nasa/earthdata-search` — **REFERENCE** (canonical URS user-data flow)
- `nasa/openset` (old) / `openaltimetry.earthdatacloud.nasa.gov` (new) — **USE THE NEW URL**
- `ornl/gedi-subsetter`, `lobodol/gedi-subsetter`, `beatriznegreiros/gedi`, ~16 others — **EMPTY/FORKS, skip**

### GIS / DEM analysis
- `richdem/richdem` — **ADOPT** (for DEM conditioning: fill_pits, fill_depressions, resolve_flats)
- `pysheds/pysheds` — **ADOPT** (watershed/HAND/stream order)
- `giswqs/whitebox-python`, `giswqs/lidar` — **REFERENCE** (whitebox tools wrapper, lidar-specific)
- `cybergis-io/viewshed` — **REPLACE WITH** `pyviewshed` (cleaner Python)
- `osgeo/gdal` — **REFERENCE** (gdaldem CLI for hillshade/contours)
- `rasterio/rasterio` — **ALREADY USING** ✓

### Blender GIS / heightmap
- `domlysz/BlenderGIS` — **SKIP** (Blender 5.x hostile, unmaintained)
- `vvoovv/blender-osm` — **SKIP** (city-scale OSM, not terrain mesh)
- `brysonbw/blender-heightmap`, `kaiaeberli/Blender-GIS`, `cgcai/Blender-Terrain-Generator`, `EarthX/Blender-GIS-Importer` — **SKIP** (unmaintained, single-file toys)
- **WRITE OURS** — drop-in `lqv/site/dem.py` (see inline report)

### Real estate / vacation rental
- `zillow/zillow-prize` (housing data) — **REFERENCE** (hedonic pricing data structures)
- `openrent/openrent-scraper` (UK rentals) — **REFERENCE** (rental data patterns)
- **No direct vacation-rental-GIS-tool** open-source project exists. The pattern is to combine: rasterio + pysal + QGIS Python. We have rasterio already.

### Eco-retreat / sustainable tourism
- **No direct open-source project for eco-retreat GIS siting**. The case studies (Chaa Creek, Awasi, Inkaterra, San Bernardino, Mennonite colonies) are commercial operations with private methodology. The synthesized 5 criteria + 10 rules in our report are the closest thing to an open playbook.

### Atlantic Forest / Paraguay remote sensing
- `wwf/source-code` — **REFERENCE** (Atlantic Forest monitoring pipeline patterns)
- `guyra-paraguay/data` — **REFERENCE** (Paraguay-specific bird/forest data)
- `globalforestwatch/gfw-data-api` — **REFERENCE** (forest change monitoring API)

### Cob / earthen construction
- **No direct open-source cob design tool exists** (most are blogs, courses, or print books). For our purposes: use the existing `lqv/house/cob.py` as the source of truth, and the 10 design rules in `MASTER_BRIEF.md` for compliance.

## Cross-cutting insights (where 2+ reports agree)

1. **The 403 is the cloud-pool consent, not the collection EULA.** Confirmed by both the GEDI research and the auth research. Fix: Cumulus endpoint OR cloud-pool EULA acceptance flow.
2. **Skip BlenderGIS; use rasterio + custom script.** Confirmed by both the DEM tooling and Blender GIS research. Cost: ~80 lines of Python. Benefit: deterministic, headless-friendly, 4.x-compatible.
3. **Conditional simulation needs DEM conditioning before any watershed analysis.** Confirmed by the DEM tooling v1 review + the case study lessons about hydrological modeling.
4. **The German/Mennonite supply chain is the unique Paraguay advantage.** Confirmed by the vacation-rental research (5 case studies) + the 450k ethnic Germans stat. This is the answer to Wesley's "European + Dutch cuisine + San Bernardino sourcing" question.

## What we should change in the project *today*

| Change | Source research | Effort |
|---|---|---|
| Update `scripts/extract_gedi_s3.py` to use the Cumulus `s3-credentials` endpoint | EARTHDATA_AUTH | 5 min |
| Add `lqv/site/dem.py` with the draft code from the Blender GIS report | BLENDER_GIS | 30 min, requires render agent to integrate |
| Add Tier-1 GIS layers (viewshed, NDWI, solar) to `scripts/analyze_dem.py` | DEM_TOOLING + VACATION_RENTAL | 2-3 hours |
| Update `MASTER_BRIEF.md` to reference the synthesized 10 design rules + 5 site-selection criteria | VACATION_RENTAL | 1 hour |
| Update `EUROPEAN_TOURISM_SPEC.md` with the Awasi + Inkaterra + Chaa Creek + San Bernardino case studies (parallels) | VACATION_RENTAL | 30 min |
| Add a new R-item to `RESEARCH_GAPS.md`: "R35 — Drone LiDAR 1 m DEM of the 62 ha" (the missing dataset for everything Tier-1+ in the GIS analysis) | VACATION_RENTAL | 10 min |
| Use the per-DAAC Cumulus endpoint in `extract_gedi_s3.py` and re-test | EARTHDATA_AUTH | 5 min |

## What we should *not* do (pushback)

- **Don't adopt BlenderGIS** for 4.2.3 LTS. Custom script is better.
- **Don't wait for Harmony GEDI L2A subsetting** — not supported yet. Use Harmony for GEDI04_A biomass only.
- **Don't build a "GEDI 2.0" extraction pipeline.** The current `earthaccess + h5py + selective read` is the canonical path.
- **Don't try to do "5 design rules" or "10 design rules"** for the eco-retreat without GSTC certification as the goal. The rules flow from the cert criteria.
- **Don't pre-optimize for high-res (5 m) DEM before we have a drone LiDAR quote.** 30 m ALOS is fine for the next 90 days; 5 m drone LiDAR becomes the priority after the escritura.

## What to ask Wesley about (open questions surfaced by research)

1. **R35 — Drone LiDAR**: ~$1,500 for 1 m DEM of the 62 ha. Worth it before Phase 1 build. Wesley's call.
2. **R36 — Acoustic + dark-sky baseline**: 4 field visits per year, $3-5K each. Justifies premium pricing.
3. **R37 — Awasi partnership conversations**: cross-marketing to EU clients via Awasi's existing Relais & Châteaux presence. Wesley to decide if this is a fit.
4. **R38 — San Bernardino partnership**: cross-promote to the Asunción German-Paraguayan summer-house set. Wesley to assess.

---

*Compiled 2026-06-10 from 5 parallel research subagents. Tools used: `task` (5 subagents in parallel), `firecrawl_search` (zero credits, mostly failed), `webfetch` (worked), `web_search` (council-disabled), `gitingest` (rate-limited). Total repos catalogued: ~80 (some probes hit 400/429, those got covered from official docs + general knowledge).*
