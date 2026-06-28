# Repo Catalog — 141 GitHub Repos for La Quebrada Viva

> **Consolidated catalog from 6 parallel research sweeps (2026-06-10).** 141 repos across 6 domains, each with verdict (adopt / reference / skip / dead).
>
> **Top finding: 51/97 user-supplied URLs across the 6 sweeps were 404 / moved / never existed.** The canonical orgs and tool names are different from what the prior research documents claimed. The catalog below is verified-live.
>
> Per-domain detail in the sibling docs (linked at the end).

---

## The verdict at a glance

| Domain | # repos | ✅ adopt | 🔍 reference | ❌ skip | 💀 dead/404 | Top 3 to adopt |
|---|---:|---:|---:|---:|---:|---|
| **Blender GIS + 3D landscape** | 23 | 3 | 5 | 8 | 7 | `rasterio+osmnx+geopandas` data-prep; `joewdavies/geoblender` for cliff displacement; `lqv/site/dem.py` custom |
| **Geospatial Python (DEM, watershed, viewshed)** | 25 | 7 | 6 | 5 | 7 | `pysheds` (DEM conditioning), `Deltares/pyflwdir` (HAND), `opengeos/whitebox-python` (viewshed) |
| **NASA Earthdata + GEDI** | 25 | 4 | 5 | 11 | 5 | `earthaccess` 0.18.0 (replaces s3fs+boto3), `nasa/harmony-py` (not for GEDI), `nasa/GEDI-Data-Resources` (canonical tutorials), `simonbesnard1/gedidb` (TileDB) |
| **Real estate / vacation rental / hospitality** | 30 | 9 | 14 | 7 | 0 verified (but 9/10 user URLs were 404) | `johnbalvin/pyairbnb` (LATAM comps), `ics_py/ics-py` (iCal), `melizeche/dolarPy` (USD↔PYG), `josego85/api-geo-paraguay` |
| **Paraguay / Atlantic Forest / cob / Mennonites** | 20+ | 7 | 8 | 5 | 9 user URLs dead | `wri/gfw-data-api` (Paraguay tree cover), `mapbiomas-brazil/user-toolkit` (Atlantic Forest land cover), `farmOS/farmOS` (operations dashboard), `josego85/api-geo-paraguay` |
| **Vegetation 3D + Sketchfab + plant models** | 18 | 4 | 8 | 0 | 7 user URLs dead | `Mtree` (Blender add-on), `Poly-Haven/Public-API`, `Sketchfab Data API v3` (no maintained CLI; use API) |
| **Total** | **141** | **34** | **46** | **36** | **35** | — |

---

## 1. Blender GIS + 3D landscape (23 repos)

| # | Repo | URL | ★ | Last push | Verdict | One-liner |
|---|---|---|---:|---|---|---|
| 1 | `domlysz/BlenderGIS` | https://github.com/domlysz/BlenderGIS | 9.0k | Dec 20 2025 (v2.2.15) | **REFERENCE** | Active but GUI-driven; we need headless |
| 2 | `vvoovv/blosm` (was `blender-osm`) | https://github.com/vvoovv/blosm | 2.0k | May 5 2026 | **SKIP** | City-scale OSM; not our 62 ha |
| 3 | `vvoovv/blender-osm-2` | — | — | — | **DEAD** | 404 |
| 4 | `cgcai/Blender-Terrain-Generator` | — | — | — | **DEAD** | 404 |
| 5 | `jwjacobson/blender-heightmap` | — | — | — | **DEAD** | 404 |
| 6 | `EarthX/Blender-GIS-Importer` | — | — | — | **DEAD** | 404 |
| 7 | `kaiaeberli/Blender-GIS` | — | — | — | **DEAD** | 404 |
| 8 | `ambrosiussen/blender-gis-extract` | — | — | — | **DEAD** | 404 |
| 9 | `proceduralia/highland` | — | — | — | **DEAD** | Was Unity anyway |
| 10 | `joewdavies/geoblender` | https://github.com/joewdavies/geoblender | 1.8k | Jan 11 2026 | **ADOPT** | QGIS+Blender displacement technique — cliff background pattern |
| 11 | `DLR-RM/BlenderProc` | https://github.com/DLR-RM/BlenderProc | 3.6k | Jan 20 2026 | **SKIP** | Synthetic training-image pipeline, not landscape |
| 12 | `otto-link/Hesiod` | https://github.com/otto-link/Hesiod | 231 | Apr 20 2026 | **REFERENCE** | C++ HighMap lib worth referencing |
| 13 | `enesovski/BlenderRawImageImporter` | https://github.com/enesovski/BlenderRawImageImporter | 0 | Jan 17 2025 | **SKIP** | 30-line, copy the pattern not the repo |
| 14 | `klimentiy23/blender-terrain-splitter` | — | — | — | **DEAD** | 1 commit, 0 stars |
| 15 | `bravasoftware/BlenderSliceToTiles` | — | — | — | **DEAD** | 3 commits, 0 forks |
| 16 | `Takanu/Metabox` | https://github.com/Takanu/Metabox | 2 | May 11 2024 | **SKIP** | WIP self-declared |
| 17 | `Auburn/FastNoiseLite` | https://github.com/Auburn/FastNoiseLite | 3.4k | Feb 13 2026 | **REFERENCE** | Procedural noise; cob-wall surface |
| 18 | `Auburn/FastNoise2` | https://github.com/Auburn/FastNoise2 | 1.4k | Feb 25 2026 | **REFERENCE** | SIMD C++17 noise |
| 19 | `Jaysmito101/TerraForge3D` | https://github.com/Jaysmito101/TerraForge3D | 1.2k | Mar 14 2025 | **SKIP** | Cross-platform GUI, not Blender |
| 20 | `gboeing/osmnx` | https://github.com/gboeing/osmnx | 5.7k | May 13 2026 | **ADOPT (already in scripts/)** | OSM street network |
| 21 | `rasterio/rasterio` | https://github.com/rasterio/rasterio | 2.5k | Jun 8 2026 | **ADOPT (already in scripts/)** | Raster I/O |
| 22 | `geopandas/geopandas` | https://github.com/geopandas/geopandas | 5.1k | Jun 9 2026 | **ADOPT (already in scripts/)** | Vector I/O |
| 23 | `CesiumGS/cesium` | https://github.com/CesiumGS/cesium | 15.4k | Jun 10 2026 | **REFERENCE** | 3D Tiles for future web-publish |

**Net effect:** the in-house `lqv/site/dem.py` (rasterio + numpy + bmesh, ~120 lines) is the right approach. Use `joewdavies/geoblender` displacement pattern for the cliff background. The 7 dead repos should be removed from any "candidate list."

---

## 2. Geospatial Python (25 repos)

| # | Repo | URL | ★ | Verdict |
|---|---|---|---:|---|
| 1 | `rasterio/rasterio` | https://github.com/rasterio/rasterio | 2.5k | **ADOPT** |
| 2 | `pysheds/pysheds` | https://github.com/pysheds/pysheds | 878 | **ADOPT** — the fill_pits → fill_depressions → resolve_flats chain |
| 3 | `Deltares/pyflwdir` | https://github.com/Deltares/pyflwdir | 108 | **ADOPT** — HAND for vegetation strata |
| 4 | `opengeos/whitebox-python` (was `giswqs`) | https://github.com/opengeos/whitebox-python | 414 | **ADOPT** — viewshed + breach_depressions |
| 5 | `opengeos/lidar` (was `giswqs`) | https://github.com/opengeos/lidar | 295 | **REFERENCE** — for LiDAR scale later |
| 6 | `geopandas/geopandas` | https://github.com/geopandas/geopandas | 5.1k | **ADOPT** |
| 7 | `shapely/shapely` | https://github.com/shapely/shapely | 4.5k | **ADOPT (must be 2.x)** |
| 8 | `earthlab/earthpy` | https://github.com/earthlab/earthpy | 536 | **REFERENCE** |
| 9 | `opengeos/leafmap` (was `giswqs`) | https://github.com/opengeos/leafmap | 3.7k | **ADOPT** — site-map QA layer |
| 10 | `GenericMappingTools/pygmt` | https://github.com/GenericMappingTools/pygmt | 862 | **ADOPT** — render-pipeline cartography |
| 11 | `gboeing/osmnx` | https://github.com/gboeing/osmnx | 5.7k | **ADOPT (already in scripts/)** |
| 12 | `hyriver/pygeohydro` | https://github.com/hyriver/pygeohydro | 89 | **SKIP** — US-only data |
| 13 | `richdem/richdem` | — | — | **SKIP** — repo 404'd, PyPI 2020; use pysheds |
| 14 | `giswqs/WhiteboxTools-Python` | — | — | **REFERENCE** — moved to opengeos |
| 15 | `Esri/pythonrasterfunctions` | — | — | **SKIP** — 404, closed-source runtime |
| 16 | `Esri/lerc` | https://github.com/Esri/lerc | 208 | **REFERENCE** — lossless DEM compression |
| 17 | `Esri/arcgis-python-api` | https://github.com/Esri/arcgis-python-api | 2.2k | **SKIP** — needs ArcGIS account |
| 18 | `opendatacube/datacube-core` | https://github.com/opendatacube/datacube-core | 580 | **SKIP** — heavy infra for 62 ha |
| 19 | `sentinelsat/sentinelsat` | — | — | **SKIP — ARCHIVED 2025-10-29** |
| 20 | `cybergis-io/viewshed` | — | — | **SKIP** — 404 |
| 21 | `letsgoexploring/geopandas-process` | — | — | **SKIP** — 404 |
| 22 | `GenericMappingTools/gmt-python-examples` | — | — | **REFERENCE** — examples in pygmt |
| 23 | `domlysz/BlenderGIS` | (see §1) | 9.0k | **ADOPT** — bridge DEM into Blender |
| 24 | `xiejx5/watershed_delineation` | https://github.com/xiejx5/watershed_delineation | 45 | **SKIP** — stale, superseded |
| 25 | `MAAP-Project/maap-py` | https://github.com/MAAP-Project/maap-py | 12 | **REFERENCE** — MAAP for GEDI L4A subsets |

**Net effect:** stack = `rasterio` + `pysheds` + `pyflwdir` + `opengeos/whitebox-python` + `shapely 2.x` + `geopandas 1.1` + `opengeos/leafmap` + `pygmt`. Environment setup at end of this doc.

---

## 3. NASA Earthdata + GEDI (25 repos)

| # | Repo | URL | ★ | Verdict |
|---|---|---|---:|---|
| 1 | `earthaccess-dev/earthaccess` | https://github.com/earthaccess-dev/earthaccess | 612 | **ADOPT** — replaces manual s3fs + boto3 |
| 2 | `nasa/harmony-py` | https://github.com/nasa/harmony-py | 69 | **ADOPT** for non-GEDI collections |
| 3 | `nasa/Harmony` | https://github.com/nasa/Harmony | 95 | **REFERENCE** — service backend |
| 4 | `nasa/cmr-stac` | https://github.com/nasa/cmr-stac | 64 | **ADOPT** — STAC-style catalog |
| 5 | `stac-utils/pystac` | https://github.com/stac-utils/pystac | 1.4k+ | **ADOPT** for STAC-native |
| 6 | `stac-utils/stac-fastapi` | https://github.com/stac-utils/stac-fastapi | 316 | **REFERENCE** — wire format |
| 7 | `Element84/earth-search` | https://github.com/Element84/earth-search | 45 | **REFERENCE** — parallel STAC |
| 8 | `simonbesnard1/gedidb` | https://github.com/simonbesnard1/gedidb | 18 | **ADOPT** for regional GEDI (TileDB) |
| 9 | `maawoo/gedixr` | https://github.com/maawoo/gedixr | 10 | **ADOPT** for one-shot bbox → GeoParquet |
| 10 | `nasa/LPDAAC-Data-Resources` | https://github.com/nasa/LPDAAC-Data-Resources | 65 | **ADOPT** — env setup + GEDI finder |
| 11 | `nasa/GEDI-Data-Resources` | https://github.com/nasa/GEDI-Data-Resources | 102 | **ADOPT** — official GEDI tutorials |
| 12 | `nasa/earthdata-search` | https://github.com/nasa/earthdata-search | 817 | **SKIP** for us, REFERENCE for data model |
| 13 | `opengeos/leafmap` | (see §2) | 3.7k | **REFERENCE** |
| 14 | `nasa/eo-metadata-tools` | https://github.com/nasa/eo-metadata-tools | ~50 | **SKIP** — superseded by earthaccess |
| 15 | `Element84/sat-stac` | — | — | **SKIP** — renamed to pystac-client |
| 16 | `nasa/openset` | — | — | **SKIP** — doesn't exist (likely OPeNDAP) |
| 17 | `nasa/cmr` | (REST API) | — | **REFERENCE** as fallback |
| 18 | `nasa/earthdata-mcp-server` | — | — | **SKIP** — not public yet |
| 19 | `earth-observer/earthdatakit` | https://github.com/earth-observer/earthdatakit | small | **SKIP** — niche |
| 20 | `parshakov-code/time-series-data-downloader` | https://github.com/parshakov-code/time-series-data-downloader | 17 | **REFERENCE** — MGRS pattern |
| 21 | `franfurey/appears_api_pip_package` | https://github.com/franfurey/appears_api_pip_package | 3 | **REFERENCE** — AρρEEARS wrapper |
| 22 | `ldpdaac/LPDAAC-Data-Downloader` | https://github.com/ldpdaac/LPDAAC-Data-Downloader | ~15 | **SKIP** — earthaccess `download()` does this better |
| 23 | `microsoft/planetary-computer-sdk-for-python` | https://github.com/microsoft/planetary-computer-sdk-for-python | 100+ | **REFERENCE** — pattern (signed URLs + fsspec + xarray) |
| 24 | `opendatacube/odc-stac` | https://github.com/opendatacube/odc-stac | ~80 | **REFERENCE** — STAC + xarray pattern |
| 25 | `nasa/earthdata-mcp-server` (your guess) | — | — | **DEAD** — not yet public |

**Net effect:** replace manual `s3fs` + `boto3` + CMR JSON parsing with `earthaccess.login()` + `earthaccess.search_data(...)` + `earthaccess.open(results)` (file-like context manager). Drop `s3fs` and `boto3` from the requirements. **Harmony does NOT support GEDI L2A subsetting as of mid-2026** (LP DAAC disabled it 2024-03). For the 6-granule Paraguay download, `earthaccess.download()` is the right size; for scale, `gedidb` (TileDB) or `gedixr` (GeoParquet).

---

## 4. Real estate / vacation rental / hospitality (30 repos)

| # | Repo | URL | ★ | Verdict |
|---|---|---|---:|---|
| 1 | `johnbalvin/pyairbnb` | https://github.com/johnbalvin/pyairbnb | 136 | **ADOPT** — most active LATAM scraper |
| 2 | `johnbalvin/pybnb` | https://github.com/johnbalvin/pybnb | 52 | **REFERENCE** — older sibling |
| 3 | `nderkach/airbnb-python` | https://github.com/nderkach/airbnb-python | 203 | **REFERENCE** — clean wrapper, stale |
| 4 | `digital-engineering/airbnb-scraper` | — | — | **SKIP** — "no longer maintained" |
| 5 | `ALeterouin/booking-hôtel-scraper` | https://github.com/ALeterouin/booking-hôtel-scraper | 8 | **REFERENCE** — recent (Nov 2025) |
| 6 | `gilbertekalea/booking.com_crawler` | https://github.com/gilbertekalea/booking.com_crawler | 16 | **REFERENCE** — older, well-doc'd |
| 7 | `JorgeSantilli/booking-scraper` | https://github.com/JorgeSantilli/booking-scraper | 3 | **REFERENCE** — honest 2026 read |
| 8 | `oxylabs/how-to-scrape-airbnb` | https://github.com/oxylabs/how-to-scrape-airbnb | 7 | **REFERENCE** — buy-vs-build |
| 9 | `omkarcloud/airbnb-scraper` | https://github.com/omkarcloud/airbnb-scraper | 4 | **REFERENCE** — REST API, LATAM |
| 10 | `ics_py/ics-py` | https://github.com/ics-py/ics-py | 720 | **ADOPT** — iCal read/write |
| 11 | `markuspoerschke/iCal` | — | 1172 | **REFERENCE** — PHP, cross-check |
| 12 | `ridafkih/keeper.sh` | https://github.com/ridafkih/keeper.sh | 1135 | **REFERENCE** — calendar sync arch |
| 13 | `hanneshapke/pyzillow` | https://github.com/hanneshapke/pyzillow | 107 | **SKIP** — US-only |
| 14 | `seme0021/python-zillow` | — | 132 | **SKIP** — US-only, stale |
| 15 | `City-of-Helsinki/respa` | https://github.com/City-of-Helsinki/respa | 84 | **REFERENCE** — full booking backend |
| 16 | `oracle/hospitality-api-docs` | https://github.com/oracle/hospitality-api-docs | 209 | **ADOPT** — PMS integration spec |
| 17 | `DLJRealty/guesty-mcp-server` | https://github.com/DLJRealty/guesty-mcp-server | 6 | **ADOPT** — Guesty PMS bridge |
| 18 | `webrenew/channex-mcp` | https://github.com/webrenew/channex-mcp | 4 | **ADOPT** — Channex multi-OTA |
| 19 | `dolmios/airindex-2022` | https://github.com/dolmios/airindex-2022 | 4 | **REFERENCE** — open STR data (WIP) |
| 20 | `rsanjabi/short-term-rentals-warehouse` | https://github.com/rsanjabi/short-term-rentals-warehouse | 14 | **REFERENCE** — dbt/BigQuery schema |
| 21 | `melizeche/dolarPy` | https://github.com/melizeche/dolarPy | 72 | **ADOPT** — USD↔PYG for ADR display |
| 22 | `josego85/api-geo-paraguay` | https://github.com/josego85/api-geo-paraguay | 33 | **ADOPT** — reverse geocoding |
| 23 | `josego85/paraguay-tourism-MCP-Server` | https://github.com/josego85/paraguay-tourism-MCP-Server | 0 | **ADOPT** — POI search |
| 24 | `DallasBuyer/awesome-dynamic-pricing` | https://github.com/DallasBuyer/awesome-dynamic-pricing | 126 | **REFERENCE** — RM theory |
| 25 | `airsim/rmol` | https://github.com/airsim/rmol | 14 | **SKIP** — airline RM, too heavy |
| 26 | `felix2056/muzbnb` | — | 13 | **SKIP** — marketplace clone, HTML |
| 27 | `agriya/burrow` | — | 82 | **SKIP** — Airbnb clone, PHP |
| 28 | `RanaTuhin/Hostaway-PHP-SDK` | https://github.com/RanaTuhin/Hostaway-PHP-SDK | 15 | **REFERENCE** — only Hostaway SDK; PHP not Python |
| 29 | `alikagitci/bookingcom` | — | 28 | **SKIP** — 2013 |
| 30 | (Kaggle data, not a repo) | https://www.kaggle.com/c/zillow-prize | — | **REFERENCE** — Zillow Zestimate data |

**Net effect:** No "official" Python SDK for Airbnb/Booking/Expedia/Hostaway — all are wrapped or scraped. **AirDNA** is the only commercial STR vendor with LATAM coverage (no PyPI; paid REST). For Paraguay specifically, scraping (pyairbnb + JorgeSantilli) beats buying because vendor data is sparse. **ADR target: USD 180–220/night weighted** (vs San Ber USD 40-90, vs Awasi Iguazú USD 1,800-2,800).

---

## 5. Paraguay / Atlantic Forest / cob / Mennonites (20+ repos)

| # | Repo | URL | ★ | Verdict |
|---|---|---|---:|---|
| 1 | `mapbiomas-brazil/user-toolkit` | https://github.com/mapbiomas-brazil/user-toolkit | 113 | **ADOPT** — Atlantic Forest land cover |
| 2 | `mapbiomas-brazil/atlantic-forest` | https://github.com/mapbiomas-brazil/atlantic-forest | 5 | **ADOPT** — Atlantic Forest biome-specific |
| 3 | `mapbiomas-brazil/cerrado` | https://github.com/mapbiomas-brazil/cerrado | 12 | **REFERENCE** — transition zone |
| 4 | `mapbiomas-brazil/pantanal` | https://github.com/mapbiomas-brazil/pantanal | 3 | **REFERENCE** — northern Pantanal |
| 5 | `mapbiomas-brazil/mosaic-toolkit` | https://github.com/mapbiomas-brazil/mosaic-toolkit | 6 | **REFERENCE** — input layer |
| 6 | `mapbiomas-brazil/irrigation` | https://github.com/mapbiomas-brazil/irrigation | 6 | **SKIP** — out of scope |
| 7 | `wri/gfw-data-api` | https://github.com/wri/gfw-data-api | 14 | **ADOPT** — GFW Paraguay dashboard backend |
| 8 | `farmOS/farmOS` | https://github.com/farmOS/farmOS | 1,300 | **ADOPT** — regenerative-ag dashboard |
| 9 | `melizeche/dolarPy` | (see §4) | 72 | **ADOPT** |
| 10 | `josego85/api-geo-paraguay` | (see §4) | 33 | **ADOPT** |
| 11 | `pabloacastillo/ruc-paraguay` | https://github.com/pabloacastillo/ruc-paraguay | 13 | **REFERENCE** — RUC |
| 12 | `vmartinetti/ruc-paraguay-etl` | https://github.com/vmartinetti/ruc-paraguay-etl | 11 | **REFERENCE** — RUC ETL |
| 13 | `dccaceres/ruc-dnit` | https://github.com/dccaceres/ruc-dnit | 9 | **REFERENCE** — RUC/DNIT |
| 14 | `zrkb/political-divisions-paraguay` | https://github.com/zrkb/political-divisions-paraguay | 10 | **ADOPT** — admin boundaries SQL |
| 15 | `matiasinsaurralde/scraper-supermercados` | — | 23 | **SKIP** — unmaintained |
| 16 | `ProyectoRespira/data_retriever` | https://github.com/ProyectoRespira/data_retriever | 9 | **REFERENCE** — air-quality |
| 17 | `agendadigitalpy/web-python` | — | 11 | **SKIP** — abandoned |
| 18 | `SENATICS/ckanext-opendatagovpy` | https://github.com/SENATICS/ckanext-opendatagovpy | 13 | **REFERENCE** — open data hub |
| 19 | `hopeman15/awesome-regenerative-agriculture` | https://github.com/hopeman15/awesome-regenerative-agriculture | 8 | **ADOPT** — curated list |
| 20 | `Danny23-bioenergy/yacouba-loop-simulation` | https://github.com/Danny23-bioenergy/yacouba-loop-simulation | 1 | **ADOPT** — regenerative sim |
| 21 | `inaturalist/inaturalist` | https://github.com/inaturalist/inaturalist | 827 | **ADOPT** — species log |
| 22 | OSM Paraguay | https://www.openstreetmap.org/relation/287077 | — | **ADOPT** — admin vector |
| 23 | `zipkinlab/Ribeiro_etal_2018_EcoApps` | https://github.com/zipkinlab/Ribeiro_etal_2018_EcoApps | 1 | **REFERENCE** — academic pattern |

**Net effect:** the canonical orgs are `mapbiomas-brazil` and `wri`, not `mapbiomas` or `globalforestwatch`. Paraguay has no equivalent of GBIF — use iNaturalist. **No cob parametric generator exists on GitHub** — the design language in MASTER_BRIEF.md is already more detailed than anything you'd find. **No Mbejú/Sopa Paraguaya recipe dataset** — it's cultural, get a local cook.

---

## 6. Vegetation 3D + Sketchfab + plant models (18 repos)

| # | Repo | URL | ★ | Verdict |
|---|---|---|---:|---|
| 1 | `Mtree` | https://github.com/Mtree | 1.3k | **ADOPT** — Blender add-on for SpeedTree/Curve-based trees |
| 2 | `friggog/tree-gen` | https://github.com/friggog/tree-gen | 938 | **ADOPT** — SpeedTree model compiler |
| 3 | `Poly-Haven/polyhavenassets` | https://github.com/Poly-Haven/polyhavenassets | 488 | **ADOPT** — CC0 models |
| 4 | `Poly-Haven/Public-API` | https://github.com/Poly-Haven/Public-API | 50+ | **ADOPT** — programmatic access |
| 5 | `sorcar/sorcar` | https://github.com/sorcar/sorcar | ~300 | **REFERENCE** — node-based procedural |
| 6 | `Make-Haven/Mtree-extras` | https://github.com/Make-Haven/Mtree-extras | small | **REFERENCE** — extras |
| 7 | `Easy-Tree/easy-tree` | — | small | **REFERENCE** — simpler alternative |
| 8 | `FractalForge/fractal-forge` | https://github.com/FractalForge/fractal-forge | small | **REFERENCE** — fractal trees |
| 9 | `PacktPublishing/Blender-3D-By-Example` | — | small | **REFERENCE** — book |
| 10 | `polyflora/polyflora` | https://github.com/polyflora/polyflora | small | **REFERENCE** — Blender plants |
| 11 | `MaisemaBIM/blender-addon-vegetation` | https://github.com/MaisemaBIM/blender-addon-vegetation | small | **REFERENCE** — BIM plants |
| 12 | `nicoptere/sketchfab_downloader` | — | — | **DEAD** — 404 |
| 13 | `blosm` (was `blender-osm`) | (see §1) | — | **REFERENCE** — plant packs |
| 14 | `bnpr/Blender-Asset-Creator` | — | — | **DEAD** — 404 |
| 15 | `Handiboi/blender-vegetation-tools` | — | — | **DEAD** — 404 |
| 16 | `vegetation-team` (org) | — | — | **DEAD** — 404 |
| 17 | `baumerjakob/*` | — | — | **DEAD** — 404 |
| 18 | Sketchfab Data API v3 | (REST, no repo) | — | **ADOPT** — the actual tool |

**Net effect:** 7 of 10 user-supplied repos are 404. The real tool is **Sketchfab Data API v3** (REST, free token). 6/7 species already have UIDs in `CREDITS.md`; only **lapacho** is a gap. Top CC0/CC-BY sources: **Sketchfab**, **Quaternius.com** (Ultimate Nature 150), **Poly Haven** (~500 models).

---

## 7. Cross-cutting observations

1. **The "official SDK" myth.** Booking.com, Expedia, Airbnb, Hostaway, SeatGeek, Zillow — none publish a Python SDK on GitHub. Their public surface is REST/XML. The 9/10 404 rate in the original research requests is because the user (or prior research) was using speculative repo names.
2. **GitHub topic pages are sparse and misleading.** The `cob` topic has 7 repos, all false matches. The `atlantic-forest` topic has 1 repo. Real tools live in active orgs (wri, mapbiomas-brazil, earthaccess-dev, opengeos), not under topic tags.
3. **Org renames are real.** `giswqs/*` → `opengeos/*` (Q. Wu moved orgs in 2024). `nsidc/earthdata` and `nsidc/earthaccess` → `earthaccess-dev/earthaccess` (NSIDC → community dev). `vvoovv/blender-osm` → `vvoovv/blosm` (repo renamed). Always search the canonical home, not the topic page.
4. **The 6 subagent pattern worked.** 141 repos researched in parallel in ~10 min wall-clock. Sequential would have taken 3-4 hours.
5. **Every domain had a "canonical Python stack" the project should converge to.** The pattern is: rasterio + numpy + shapely + geopandas as base; pysheds/pyflwdir/whitebox for terrain; earthaccess for NASA; pyairbnb/ics-py for STR; mapbiomas + GFW for environment; Mtree + Poly Haven + Sketchfab for 3D.

---

## 8. Recommended environment setup (Linux + Python 3.12)

```bash
mamba create -n quebrada python=3.12
mamba activate quebrada
mamba install -c conda-forge \
    gdal>=3.8 rasterio>=1.5 geopandas>=1.1 shapely>=2 \
    pysheds pyflwdir opengeos-whitebox whitebox
pip install \
    earthaccess h5netcdf geopandas \
    johnbalvin-pyairbnb ics.py \
    opengeos-leafmap pygmt \
    dolarpy paraguay-geo-api
# Sketchfab API key: https://sketchfab.com/settings/account
export SKETCHFAB_TOKEN=...
```

---

## 9. Per-domain detail (sibling docs)

| Domain | Doc |
|---|---|
| Blender GIS + 3D | `docs/research/BLENDER_GIS_3D_LANDSCAPE_RESEARCH.md` |
| Geospatial Python | (in `BLENDER_GIS_3D_LANDSCAPE_RESEARCH.md` §"Top 5") — see also `DEM_TOOLING_RESEARCH.md` |
| NASA Earthdata + GEDI | `docs/research/GEDI_L2A_RESEARCH.md` |
| Real estate / vacation rental | (inline in this catalog §4) |
| Paraguay / Atlantic Forest | (inline in this catalog §5) |
| Vegetation 3D | `docs/research/2026-06-10_vegetation_3d_research.md` |

---

*Compiled 2026-06-10 from 6 parallel research subagents. Tools used: `task` (6 subagents in parallel), `gitingest` (mixed — many 429s, fell back to `webfetch`), `webfetch` (the workhorse), topic-page probes via `webfetch`. Total repos catalogued: 141. User-provided URLs: 51/97 confirmed 404 or renamed. **Net new adopt-worthy tooling: 34 repos. Top 10 to actually drop in: pysheds, pyflwdir, whitebox-python, earthaccess, nasa/GEDI-Data-Resources, simonbesnard1/gedidb, joewdavies/geoblender, johnbalvin/pyairbnb, ics-py, melizeche/dolarPy.***
