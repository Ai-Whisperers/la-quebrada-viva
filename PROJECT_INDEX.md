# PROJECT_INDEX — La Quebrada Viva

Full-repo navigation and review. Generated from a structural sweep (`git ls-files`, `wc -l`, `du -sh`).

This file is the cold-start map: tells a reader what the repo holds, where the load-bearing code lives, what the docs are, and what to be careful about. For escritura-day operational order, read [`docs/INDEX.md`](docs/INDEX.md) (escritura tier 0); for module architecture, read [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md); for build invariants, read [`CLAUDE.md`](CLAUDE.md).

---

## 1. What this project is

A Blender-driven photoreal model of a 62-ha parcel in Escobar/Paraguarí, Paraguay, owned 75/25 by Wesley van de Camp and Thijs. Deliverables (in priority order):

1. **18 finals** (A/B/C × hero/cliff/dusk/petal_macro/stream_up/terrace) — shipped at commit `85e86aa` (renderer byte-frozen).
2. **62-ha digital twin (T-DT)** — ALOS AW3D30 DEM + Sentinel-2 albedo + GEDI canopy, with COP30/SRTM/NASADEM cross-checks (shipped `4409dba`).
3. **Escritura technical pack** — 28-page PDF deck v6, Bill of Quantities (175 items), Pelton micro-hydro feasibility, signing 2026-06-27.
4. **Housing-park master plan** — 15 housing typologies + 4 amenities + 3 typology-package amenity stubs for European/1st-world ecotourism.

The project is "dual-scope": the original La Quebrada Viva cob house, plus Wesley's expanded housing-park concept.

---

## 2. Top-level layout

`git ls-files | wc -l` → **1,186 tracked files**. Top-level layout (`du -sh`):

| Path | Size | Purpose |
|---|---:|---|
| `assets/` | 37 G | Poly Haven + AmbientCG textures, models, HDRIs, terrain DEM/heightmap. **Not all tracked** — `.gitignore` excludes raw heavies; only metadata + thumbnails land in git. |
| `renders/` | 4.1 G | Finals (18 shipped + 5 previews), sub-renders (`sub/runs/<RUN_ID>_…` + `sub/latest/`). |
| `docs/` | 1.4 G | 60 root markdown + 8 subdirs; the escritura-deck PDFs, site-data, research, email drafts, finance. |
| `dist/` | 543 M | Bundles for delivery: `wesley_bundle_20260616-1715.zip` + `print_pack_2026-06-27/`. |
| `_archive/` | 5.4 M | Frozen historical artefacts (e.g. `build_scene.py.pre-refactor.bak` — **do not delete**). |
| `lqv/` | 2.8 M | The Python package — everything the renderer imports. **Source-of-truth code.** |
| `logs/` | 1.8 M | Run logs (render driver output, CI smoke logs). |
| `scripts/` | 876 K | 56 standalone scripts (build_*, fetch_*, render_*, contact_sheet_*, analyze_*). |
| `LICENSES/` | 1.2 M | Per-asset license bundles (CC0 / CC-BY 4.0 only — CC-BY-SA blocked, CC-BY-NC deck-only). |
| `tests/` | 60 K | 3 test files (boq rollup, RNG invariants, typology contract). |
| `__pycache__/` | 12 K | Bytecode cache. |
| `docs/references/wesley_2026-06-11/` | 15 M | Client-supplied reference imagery (41 jpegs). |

### Top-level files

| File | Size | Purpose |
|---|---:|---|
| `build_scene.py` | 4.2 K | **Frozen byte-identical at `85e86aa`** — single Blender driver entry. Do not edit. |
| `scene.blend` | 69 M | Saved scene. Smoke test backs up to `scene.blend.session-backup`. |
| `scene.blend1` | 13 M | Blender auto-save. |
| `CLAUDE.md` | 19 K | Project-local agent instructions — 10 design rules, invariants, plant species, sub-render workflow. |
| `STATUS.md` | 30 K | Canonical state document. Render manifest, milestone log, dual-scope summary. |
| `ARCHITECTURE.md` | — | (in `docs/` — module layout, RNG invariant). |
| `LICENSE_BUNDLE.md` | 9.4 K | License gate for everything Wesley receives. |
| `PROVENANCE.md` | 11 K | DEM + sat data licenses, SHA-256, bbox, retrieval dates. |
| `Makefile` | 2 K | `make boq`, `make deck`, etc. |
| `pyproject.toml` | 1.9 K | Python project metadata. |
| `CREDITS.md` | — | Asset author attributions. |
| `LICENSE` | — | Top-level repo license. |

---

## 3. LOC summary

Aggregated from `git ls-files`:

| Language | Files | LOC |
|---|---:|---:|
| Python | 210 | 34,550 |
| Markdown | 95 | 20,770 |
| Shell | 15 | 560 |
| JSON | 18 | (data) |
| YAML | 3 | (CI) |
| TIFF/PNG/JPG | 671 | (binary) |

Python is the load-bearing surface; markdown is heavy because the escritura deck has long source-of-truth markdown.

### Top 30 Python files by LOC

```
1788  scripts/mushroom_cob_house.py            ← single biggest file
1398  scripts/build_escritura_deck.py
 795  lqv/site/terrain_dsl.py
 775  lqv/typologies/bamboo_container_4pax.py
 748  lqv/amenities/eco_retreat_modern_oasis.py
 696  lqv/typologies/bamboo_beton_family_rectangular.py
 679  lqv/typologies/bamboo_beton_family_curved.py
 679  lqv/amenities/eco_pool.py
 653  lqv/subscene/terrain_62ha_photoreal.py
 644  scripts/download_polyhaven_assets.py
 634  lqv/subscene/terrain_62ha.py
 627  lqv/typologies/italian_stone_small_v2.py
 607  lqv/typologies/bamboo_river_house.py
 563  lqv/boq.py
 539  lqv/typologies/bamboo_wigwam_lodge.py
 527  lqv/amenities/floating_dining.py
 523  lqv/typologies/bamboo_beton_28.py
 504  lqv/typologies/italian_river_house_4pax.py
 483  lqv/house/stone_wall.py
 465  lqv/typologies/bamboo_beton_30.py
 455  lqv/typologies/bamboo_boomhut_treehouse.py
 446  lqv/typologies/italian_stone_small_v1.py
 444  lqv/typologies/hobbit_house.py
 400  lqv/amenities/labrisa_lounge.py
 393  lqv/house/bamboo_frame.py
 388  scripts/analyze_assets.py
 326  scripts/satellite/gee_quickstart.py
 325  lqv/house/cob.py
 318  scripts/download_ambientcg_assets.py
```

### Top markdown files by LOC

```
1480  docs/claude_code_blender_best_practices.md
 968  docs/DEM_TOOLING_RESEARCH.md
 743  docs/TOOLING_AUDIT_AND_OPPORTUNITIES.md
 640  docs/paraguay_clay_house_research.md
 640  docs/_archive/2026-06-1X/MODELS_ROAST.md
 639  docs/ASSETS_INTEGRATION_PLAN.md
 588  docs/prompt_location_scene.md
 564  docs/EUROPEAN_TOURISM_SPEC.md
 539  docs/prompt_house_render.md
 529  docs/TERRAIN_PIVOT.md
 491  docs/MASTER_BRIEF.md
 482  docs/SESSION_LOG.md
 446  docs/HOUSING_PARK_CONCEPT.md
```

---

## 4. `lqv/` package — the source of truth

Total: **1,204 LOC** at the package root plus **~25,500 LOC** across 12 subpackages.

### `lqv/` root modules

| File | LOC | Role |
|---|---:|---|
| `__init__.py` | 1 | Package marker. |
| `asset_loader.py` | 192 | Loads Poly Haven + AmbientCG assets from `assets/` with metadata lookups. |
| `boq.py` | 563 | Bill of Quantities engine — substring-keyword category inference, CSV + markdown writers. Read by `scripts/build_boq.py`. |
| `cameras.py` | 64 | Six named cameras: `hero`, `stream_up`, `terrace`, `cliff`, `dusk`, `petal_macro`. |
| `config.py` | 66 | Env-var control surface — `RENDER_VARIANT`, `RENDER_CAM`, `RENDER_RES`, `RENDER_SAMPLES`, `RENDER_SKIP`. Res presets: `preview/720` (1280×720), `final/1080` (1920×1080), `hero/1440` (2560×1440). `SEED = 20260609`. |
| `engine.py` | 85 | Cycles + GPU setup, with CPU fallback gated by `LQV_ALLOW_CPU_FALLBACK`. |
| `geometry.py` | 28 | Geometry helpers. |
| `lighting.py` | 190 | Sun + HDRI + variant-specific lighting (A/B/C). |
| `render.py` | 15 | Render dispatch. |

### `lqv/subscene/` — 53 files, ~4,300 LOC

The sub-render-first workflow. Each new asset/typology/amenity gets a thin driver here **before** any composite scene touch. Top 15:

```
653  terrain_62ha_photoreal.py    ← canonical 62-ha builder (ALOS DEM + albedo)
634  terrain_62ha.py              ← availability gate + dispatcher facade
275  base.py                      ← shared scaffolding (RENDER_RUN_ID + folder convention)
212  elevation_dutch.py           ← elevation/Dutch-angle sweep (68 PNGs)
146  boulder_cluster.py
119  bamboo_beton_family_rectangular.py
111  hdri_dusk_compare.py
103  terrain_house_scale.py
 97  material_wall_compare.py
 93  bamboo_container_4pax.py
 86  hobbit_house.py
 84  bamboo_river_house.py
 75  bamboo_wigwam_lodge.py
 74  italian_river_house_4pax.py
```

The remaining ~33 files are thin (<70 LOC) per-asset drivers — one for each typology, amenity, and inspectable detail. **Sub-renders land in** `renders/sub/runs/<RENDER_RUN_ID>_<asset>[_<tag>]/<variant>.png` (mirrored to `renders/sub/latest/`).

### `lqv/typologies/` — 19 files, ~8,260 LOC (heaviest subpackage)

15 buildable housing typologies (bamboo + Italian + hobbit + Wesley phase-2 villa + clay-terracotta estate) plus 3 typology-package amenity stubs (`TYPOLOGY_AMENITIES`: bamboo_portal, bamboo_outdoor_shower, candle_path). Housing builders are 444–775 LOC each (substantial parametric geometry); phase-2 additions are 176–265 LOC (simpler signature shapes).

| File | LOC |
|---|---:|
| `bamboo_container_4pax.py` | 775 |
| `bamboo_beton_family_rectangular.py` | 696 |
| `bamboo_beton_family_curved.py` | 679 |
| `italian_stone_small_v2.py` | 627 |
| `bamboo_river_house.py` | 607 |
| `bamboo_wigwam_lodge.py` | 539 |
| `bamboo_beton_28.py` | 523 |
| `italian_river_house_4pax.py` | 504 |
| `bamboo_beton_30.py` | 465 |
| `bamboo_boomhut_treehouse.py` | 455 |
| `italian_stone_small_v1.py` | 446 |
| `hobbit_house.py` | 444 |
| `clay_terracotta_estate.py` *(phase-2, §3.15)* | 265 |
| `bamboo_outdoor_shower.py` *(phase-2, TYPOLOGY_AMENITIES)* | 256 |
| `bamboo_curved_roof_villa.py` *(phase-2, §3.14)* | 243 |
| `bamboo_portal.py` *(phase-2, TYPOLOGY_AMENITIES)* | 220 |
| `candle_path.py` *(phase-2, TYPOLOGY_AMENITIES)* | 176 |
| `__init__.py` | 63 |

### `lqv/amenities/` — 6 files, 2,626 LOC

Pool, lounge, restaurant, dining, retreat. The two heaviest:

| File | LOC |
|---|---:|
| `eco_retreat_modern_oasis.py` | 748 |
| `eco_pool.py` | 679 |
| `floating_dining.py` | 527 |
| `labrisa_lounge.py` | 400 |

### `lqv/house/` — 12 files, 1,616 LOC

The original La Quebrada Viva cob house components:

| File | LOC |
|---|---:|
| `stone_wall.py` | 483 |
| `bamboo_frame.py` | 393 |
| `cob.py` | 325 |
| (8 more, each <100 LOC) | ~415 |

### `lqv/site/` — 9 files, 1,205 LOC

| File | LOC | Role |
|---|---:|---|
| `terrain_dsl.py` | 795 | Procedural terrain DSL (largest site file). |
| `terrain_62ha.py` | 66 | Facade — gates on `assets/terrain/escobar_height.{png,json}` and delegates to `lqv.subscene.terrain_62ha_photoreal`. |
| (7 more) | ~344 | Stream, terrace, cliff, vegetation placement. |

### `lqv/flora/` — 15 files, 1,159 LOC

Plant species: lapacho (rosado/amarillo), jacaranda, ceibo, palo borracho, yvyra pytã, etc. Species accuracy is enforced by `lqv/util/ten_rules_check.py`.

### `lqv/materials/` — 9 files, 735 LOC

Cycles material library — wood, mud-cob, stone, water, sky. Built **before** `random.seed()` per the RNG invariant.

### `lqv/util/` — 5 files, 443 LOC

| File | Role |
|---|---|
| `ten_rules_check.py` | Audit module run by `scripts/smoke_test.sh`. Returns non-zero on rule violations. |
| (4 more) | Logging, RNG helpers, file IO. |

### `lqv/finance/` — 1 file, 91 LOC

`get_usd_to_pyg()` reads `docs/finance/fx.json` (BCP ref rate). Single source of truth for currency conversion in the escritura deck.

### `lqv/output/`, `lqv/restaurant/`, `lqv/animation/`

Thin. 2–4 files each. Output writers, restaurant builder, animation helpers.

---

## 5. `scripts/` — 56 standalone scripts, 10,318 LOC

Grouped by purpose. None of these are imported by `build_scene.py`; all run via `python3 scripts/<name>.py` or via `make` targets.

### Build / pack

| Script | LOC | Purpose |
|---|---:|---|
| `build_escritura_deck.py` | 1398 | Chrome-headless `--print-to-pdf` from `escritura_deck.md` source. Emits v6 PDF (28 pp, 10.8 MB). |
| `build_boq.py` | — | Wraps `lqv.boq` for outside-Blender execution (bpy stub shim). |
| `build_pelton_siting.py` | 293 | Pelton micro-hydro head map from COP30 DEM. |
| `build_pelton_head_map.py` | — | Standalone head map. |
| `build_wesley_bundle.py` | — | Builds `dist/wesley_bundle_*.zip` (idempotent). |

### Render

| Script | LOC | Purpose |
|---|---:|---|
| `mushroom_cob_house.py` | 1788 | **Single biggest script.** Mushroom-shaped cob house variant. (Standalone builder, not in `lqv/`.) |
| `render_models_gallery.py` | 260 | Asset-gallery contact sheet. |
| `render_all.sh` (etc) | — | Bash wrappers for batch render. |

### Fetch / acquire

| Script | LOC | Purpose |
|---|---:|---|
| `download_polyhaven_assets.py` | 644 | Bulk PH download (HDRIs, textures, models). |
| `download_ambientcg_assets.py` | 318 | AmbientCG mirror. |
| `fetch_copernicus_lcover.py` | 248 | Copernicus landcover. |
| `extract_gedi_https.py` | 259 | GEDI L2A canopy heights (HTTPS path). |
| `extract_gedi_s3.py` | 235 | GEDI via S3 (needs Earthdata cloud-pool EULA — see STATUS.md 2026-06-10). |
| `extract_gedi.py` | 219 | Dispatcher. |
| `make_terrain_heightmap.py` | — | Bake DEM TIFF → normalized 16-bit PNG + JSON sidecar at `assets/terrain/escobar_height.*`. |

### Analyze

| Script | LOC | Purpose |
|---|---:|---|
| `analyze_assets.py` | 388 | Inventory + cross-reference Poly Haven assets vs lqv usage. |
| `analyze_dem.py` | 214 | DEM stats (elevation histogram, buildable-area %). |
| `contact_sheet_pelton.py` | 246 | Pelton viridis + 30 m/80 m contour + histogram contact. |
| `contact_sheet_satellite_overlay_ab.py` | 203 | A/B Sentinel-2 albedo overlay sheet. |

### Smoke / CI

| Script | LOC | Purpose |
|---|---:|---|
| `smoke_test.sh` | 36 | `RENDER_SKIP=1 RENDER_RES=preview blender --background --python build_scene.py`. Backs up `scene.blend`. Sets `LQV_ALLOW_CPU_FALLBACK=1` for CI runners (CPU-only). Audits via `lqv.util.ten_rules_check`. Exit 2 → design-rule violations; exit 1 → traceback. |

### `scripts/satellite/` — 13 files, 2,133 LOC

| File | LOC | Role |
|---|---:|---|
| `gee_quickstart.py` | 326 | Google Earth Engine helpers. |
| `fetch_climate.py` | 271 | ERA5/CHIRPS climate data. |
| `fetch_landcover.py` | 267 | ESA WorldCover. |
| `fetch_nicfi.py` | 248 | Planet NICFI (deck-only license). |
| `fetch_sentinel2.py` | 237 | Sentinel-2 L2A. |
| `pc_stac_quickstart.py` | 199 | Planetary Computer STAC. |
| `_aoi.py` | 125 | AOI bbox helper. |
| `_retry.py` | 114 | Retry/backoff. |
| `_meta.py` | 103 | Provenance metadata writer. |
| `test_stac.py` | 86 | Tests for STAC. |
| `_license.py` | 67 | License gate. |
| `_crs.py` | 67 | CRS reprojection. |
| `__init__.py` | 18 | |
| `conftest.py` | 5 | Pytest fixtures. |

---

## 6. `tests/` — 3 files

Surprisingly thin given 34K LOC of Python (see §10 observations).

| File | Purpose |
|---|---|
| `test_boq_rollup.py` | BoQ category inference + grand total. |
| `test_rng_invariants.py` | Validates `random.seed()` ordering — must fire **after** `materials.build_materials()` and **before** the first `build_*` call. |
| `test_typology_contract.py` | Each typology builder must accept `(parent, anchor, variant)` and return a Blender object. |

---

## 7. `docs/` — 60 root files + 8 subdirs

Authoritative navigation entry: [`docs/INDEX.md`](docs/INDEX.md) (tiered escritura-first).

### Subdirectories

| Subdir | Files | Purpose |
|---|---:|---|
| `docs/boq/` | 3 | `boq_rollup.{csv,md,pdf}` — 175 line items, $231,280.98 USD / Gs. 1,688,351,154 @ 7300. |
| `docs/email_drafts/` | 7 | Per-recipient escritura-day emails (Peña ES, Wesley EN, Thijs ES, Burgos ES, share links, errata template, sent_archive/). |
| `docs/escritura_deck/` | 8 | `escritura_deck.md` source + PDFs (v1 → v6). v6 is canonical (28 pp, 10.8 MB, SHA-256 `2e4c265c…`). |
| `docs/finance/` | 1 | `fx.json` — BCP USD/PYG ref rate. **Refresh on T-0 ~07:00.** |
| `docs/research/` | 6 | 5 sub-reports (~80 repos surveyed) + README. |
| `docs/satellite/` | 1 | Satellite tooling notes. |
| `docs/site_data/` | 31 | DEM TIFFs, contact sheets, GEDI CSV, satdata_brief, sentinel2/ (**deck-only license — do not stage to git**). |
| `docs/site_data_2026-06-13_snapshot/` | 18 | Monday-only working set (2026-06-13/14 snapshot). |

### Escritura-day quick reference

- `docs/MASTER_BRIEF.md` — project North Star.
- `docs/CLIENT.md` — Wesley (75%) + Thijs (25%) + Burgos (intermediary).
- `docs/contract_summary.md` — boleto 2026-04-28 quick-reference.
- `docs/CLOSING_DAY_PREP.md` — T-7/T-5/T-2/T-0 legal checklist.
- `docs/MORNING_RUNBOOK_2026-06-27.md` — laptop-side 07:00 → 10:00 mechanical runbook.
- `docs/CONTINGENCIES.md` — C1–C10 risk register.
- `docs/ROLLBACK_RUNBOOK.md` — errata / postponement.
- `dist/print_pack_2026-06-27/INTEGRITY.md` — canonical SHA/page-count pins.
- `dist/print_pack_2026-06-27/WALLET_CARD.txt` — pocket reference.

### Engineering / research depth

- `docs/ARCHITECTURE.md` — `lqv/` module layout + RNG invariant + sub-render-first rule.
- `docs/asset_plan.md` — per-typology / per-amenity asset plan.
- `docs/sub_render_strategy.md` — 31-target sub-render queue + driver template.
- `docs/PROVENANCE.md` — license + URL + SHA-256 + bbox + retrieval for ALOS / COP30 / Sentinel-2 / GEDI / OSM / SRTM / NASADEM.
- `docs/site_data/satdata_brief.md` — S1–S4 satellite pipeline reader.
- `docs/research/README.md` — research synthesis.
- `docs/RESEARCH_GAPS.md` — open gaps + close plan.
- `docs/_archive/2026-06-1X/CRITIQUE_2026-06-10.md` — honest-roast critique snapshot (archived; Tier-0 carry-forward landed).
- `docs/_archive/2026-06-1X/UPGRADE_PLAN.md` — Tier 0/1/2/3 derived from CRITIQUE (archived; carry-forward items live in `docs/DEFERRED_BUGS.md` + TaskList #34–#50).
- `docs/_archive/MANIFEST.md` — archive index + provenance table.

---

## 8. `renders/` — 4.1 G, ~851 PNG/JPG

### Finals at root (23 files)

The deliverable 18:

```
A_hero, A_stream_up, A_terrace, A_cliff, A_dusk, A_petal_macro
B_hero, B_stream_up, B_terrace, B_cliff, B_dusk, B_petal_macro
C_hero, C_stream_up, C_terrace, C_cliff, C_dusk, C_petal_macro
```

Plus 5 preview cache files (`_preview_A_hero.png` etc).

- Hero finals: 512 spp, 2560×1440.
- All others: 256 spp, 1920×1080.
- All verified against ten-rules check.

### Sub-renders

- `renders/sub/runs/<RENDER_RUN_ID>_<asset>[_<tag>]/<variant>.png` — primary store, grouped by run.
- `renders/sub/latest/<asset>_<variant>.png` — mirror of latest run for each asset (escritura deck reads from here).
- Parallelism = **1** (one Blender process at a time; ~4.3 GB RSS, OOMs at ×3 on 14 GB host).
- Folder convention is enforced by `lqv/subscene/base.py`.

### Render catalogue (browse the 901 PNGs)

- [`docs/render_catalogue/INDEX.md`](docs/render_catalogue/INDEX.md) — roster of 53 asset buckets with totals, latest date, and a contact-sheet gallery.
- [`docs/render_catalogue/by_asset/`](docs/render_catalogue/by_asset/) — per-asset markdown with embedded contact sheet + chronological tile list.
- [`docs/render_catalogue/contact_sheets/`](docs/render_catalogue/contact_sheets/) — ≤9-tile 3-column thumbnail JPGs, one per asset.
- `docs/render_catalogue/catalogue.json` — machine-readable sidecar (totals, by_source, per-asset records). Stable across re-runs.
- Rebuild via `make catalogue` (runs `make sheets` first; requires ImageMagick `montage`).

---

## 9. `dist/` — 543 M

Final deliverable bundles, all SHA-pinned.

### `wesley_bundle_20260616-1715.zip` (266 MB, 37 files)

| Path | Contents |
|---|---|
| `01_brief/` | `wesley_brief_onepager.pdf` (321 KB) |
| `02_escritura_deck/` | `escritura_deck_v6.pdf` (10.8 MB, 28 pp) |
| `03_renders_finals/` | 18 finals at `85e86aa` |
| `04_terrain_digital_twin/` | 6 T-DT v5_arrowfix renders |
| `05_dem_ab/` | ALOS vs COP30 cross-check |
| `06_pelton_feasibility/` | head map + JSON + contact sheet |
| `07_boq/` | `boq_rollup.{csv,md,pdf}` |
| `08_provenance/` | `PROVENANCE.md`, `satdata_brief.md` |

SHA-256: `9ce96b859620201bee7dadc7e8f164c4177613e69e7fb66e30bc14085724a53c`. Regenerable via `python3 scripts/build_wesley_bundle.py`.

### `dist/print_pack_2026-06-27/`

The notary-table package. Includes `INTEGRITY.md`, `audit_log.txt`, `VERIFY.sh` (one-liner check), `WALLET_CARD.txt`, `BUNDLE_README.txt`, `MORNING_RUNBOOK_2026-06-27.md`, `PRINT_MANIFEST.txt`, plus a copy of the bundle + escritura deck.

### Pelton headline (Rule 7)

- `head_max = 182.6 m`, `head_mean = 33.4 m`, `head_p95 = 108.1 m`.
- **31.2 %** of footprint above 30 m (Pelton minimum); **10.7 %** above 80 m.
- Computed from COP30 DEM (108×108 px, ~30 m/pixel, sha256 `10e6459c…`).

---

## 10. `assets/` — 37 G

Not all tracked (too heavy). `.gitignore` excludes the raw heavies.

| Subdir | Files | Size | Notes |
|---|---:|---:|---|
| `assets/hdris/` | 30 | 1.5 G | Poly Haven HDRIs (variant A/B/C dusk + day). |
| `assets/textures/` | 1,603 | 20 G | Poly Haven + AmbientCG PBR materials (~125 sets × multiple resolutions). |
| `assets/models/` | 1,036 | 16 G | Poly Haven models — plants, props, rocks, jugs, barrels, lanterns, etc. |
| `assets/terrain/` | 10 | 1.2 M | `escobar_height.png` + `escobar_height.json` (ALOS-derived heightmap) + DEM TIFFs (not all tracked). |

License gate: CC0 + CC-BY 4.0 only in the shipped bundle. CC-BY-SA blocked. CC-BY-NC = deck-only. Planet NICFI = deck-only. See [`LICENSE_BUNDLE.md`](LICENSE_BUNDLE.md) + [`CREDITS.md`](CREDITS.md).

---

## 11. Critical observations (review)

### Hot spots (size concentration)

- **`scripts/mushroom_cob_house.py` at 1,788 LOC** is the single biggest source file in the repo — bigger than `build_scene.py` (4.2 KB) and bigger than any `lqv/` module. It's a standalone variant builder that never moved into `lqv/`. Candidate for refactor into `lqv/typologies/mushroom_cob_house.py` (if/when scope permits — **NOT** before the escritura).
- **`scripts/build_escritura_deck.py` at 1,398 LOC** does template subst + Chrome PDF generation + per-asset thumbnail injection. Heavy because it owns the whole deck pipeline; reasonable cohesion given it's the single deliverable build path.
- **`lqv/typologies/` averages 500–800 LOC per typology for the original 13** (12 files in the 444–775 LOC band). Wesley phase-2 added 2 signature villas + 3 amenity stubs at 176–265 LOC each — these are simpler shapes so the lighter LOC is intentional. Each is a parametric geometry builder. This is correct distribution — no further normalization needed.
- **`lqv/subscene/` has 48 files averaging 86 LOC** (4,120 LOC / 48). Two outliers (`terrain_62ha_photoreal.py` 653, `terrain_62ha.py` 634 — the digital twin) dominate. The other 46 are thin drivers, as the sub-render-first workflow intends. Good shape.

### Test coverage gap

**Only 3 test files for 34,550 LOC of Python** = ~0.01 tests per LOC. Coverage is intentionally narrow (BoQ rollup, RNG invariants, typology contract) — the real validation surface is `scripts/smoke_test.sh` + `lqv/util/ten_rules_check.py` running against the actually-built scene. **This is a deliberate trade-off**, not a bug: visual Blender output is the acceptance criterion, and tests for that live in the render-diff sense, not unit-test sense.

### Doc/code ratio is unusual

- Markdown is **60% of Python LOC** (20,770 vs 34,550). Most projects sit at 5–15%. The escritura deck (1,398 LOC builder + multi-tier source markdown) and the research synthesis (`docs/research/`, `docs/DEM_TOOLING_RESEARCH.md`, etc) explain it. **The repo is half-document, half-renderer** — appropriate given the deliverable is a legal/technical pack, not just imagery.

### Freeze + facade pattern

`build_scene.py` is byte-frozen at `85e86aa`. The way new typologies/amenities land **without** touching it: `lqv/subscene/<asset>.py` driver + sub-render-first workflow. `lqv/site/terrain_62ha.py` is a thin facade that delegates to `lqv.subscene.terrain_62ha_photoreal` — same pattern. Anything new should follow this.

### Asset weight in git

- `assets/` is 37 G but **most is gitignored**; only metadata + thumbnails are tracked.
- `renders/` is 4.1 G — 18 finals + 5 previews at root, plus sub-renders. **Finals are tracked**; `sub/runs/` follows the same convention.
- Beware: never `git add -A` / `git add .` — explicit staging only. Banned-from-staging paths: `scripts/mcp_daemon.py`, `docs/site_data/sentinel2/*.tif`, `docs/*_boleto_*.pdf`, `docs/*_escritura_*.pdf`, `docs/2026-*_*.pdf`.

### CI

GitHub Actions workflows in `.github/workflows/`: `smoke_test.sh` (build-only audit) + `lint.yml`. CI runners are **CPU-only** — `LQV_ALLOW_CPU_FALLBACK=1` is set in the smoke shell so engine setup doesn't gate the runner (fix landed in commit `f087c05`).

### Repo hygiene state

As of the latest sweep:
- No banned paths tracked.
- `.gitignore` comprehensive (raw assets, render caches, session backups, MCP daemon).
- No stale branches.
- No orphan empty directories.
- `_archive/build_scene.py.pre-refactor.bak` retained — **do not delete**.

### Known fragile spots

- `lqv/scatter_lapacho_petals*` — referenced but **do not touch** per project rule.
- Hidden `WindowCut_*` cutters — **do not touch**.
- `PARCEL_CLIP_END_M = 20000.0`, `HOUSE_CLIP_END_M = 1000` — parcel-scale sub-renders that don't go through `base.run()` MUST set `cam.data.clip_end` >> 100 m default, or render returns only the HDRI.
- RNG order invariant: `random.seed()` fires **after** `materials.build_materials()` and **before** the first `build_*` call. Tested by `tests/test_rng_invariants.py`.
- Render parallelism = 1 (~4.3 GB RSS per Blender process; 14 GB host OOMs at ×3).

---

## 12. Document map (where to read what)

| Question | Read |
|---|---|
| What does this project ship? | [`STATUS.md`](STATUS.md), [`docs/MASTER_BRIEF.md`](docs/MASTER_BRIEF.md) |
| How is the code laid out? | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), this file §4 |
| What's the agent contract? | [`CLAUDE.md`](CLAUDE.md) |
| What's the escritura day plan? | [`docs/MORNING_RUNBOOK_2026-06-27.md`](docs/MORNING_RUNBOOK_2026-06-27.md) |
| What's in the Wesley bundle? | [`dist/print_pack_2026-06-27/INTEGRITY.md`](dist/print_pack_2026-06-27/INTEGRITY.md), [`dist/print_pack_2026-06-27/BUNDLE_README.txt`](dist/print_pack_2026-06-27/BUNDLE_README.txt) |
| How do I add a new asset/typology? | [`docs/sub_render_strategy.md`](docs/sub_render_strategy.md), `lqv/subscene/base.py` |
| What are the design rules? | [`CLAUDE.md`](CLAUDE.md) (10 rules), `lqv/util/ten_rules_check.py` |
| What sat-data licenses apply? | [`PROVENANCE.md`](PROVENANCE.md), [`LICENSE_BUNDLE.md`](LICENSE_BUNDLE.md) |
| What was critiqued? | [`docs/_archive/MANIFEST.md`](docs/_archive/MANIFEST.md) — index over archived critiques (`CRITIQUE_2026-06-10.md`, `MODELS_ROAST.md`, `HOUSES_REVIEW_2026-06-14.md`, etc.) |
| What's the deliverable bundle SHA/page-count? | [`dist/print_pack_2026-06-27/INTEGRITY.md`](dist/print_pack_2026-06-27/INTEGRITY.md), [`dist/print_pack_2026-06-27/WALLET_CARD.txt`](dist/print_pack_2026-06-27/WALLET_CARD.txt) |
| What are the BoQ totals? | [`docs/boq/boq_rollup.md`](docs/boq/boq_rollup.md) |
| What's the Pelton head map? | `dist/wesley_bundle_…/06_pelton_feasibility/`, `scripts/build_pelton_siting.py` |

---

## 13. One-glance facts (sanity card)

- 1,186 tracked files / 34,550 Py LOC / 20,770 md LOC.
- 18 finals shipped at `85e86aa`; renderer byte-frozen.
- 62-ha digital twin shipped at `4409dba`.
- 175 BoQ line items, $231,280.98 USD / Gs. 1,688,351,154 @ 7300.
- Escritura deck v6: 28 pp, 10.8 MB, SHA `2e4c265c…`.
- Wesley bundle: 266 MB, 37 files, SHA `9ce96b85…`.
- Escritura signing: 2026-06-27, 10:00 -03.
- Render parallelism: 1. Render resolutions: `preview|720`, `final|1080`, `hero|1440`.
- RNG seed: 20260609. Order: materials → seed → builds.
- License gate: CC0 + CC-BY 4.0 only. CC-BY-SA blocked. NC = deck-only.
- 4-DEM cross-check: ALOS AW3D30 (canonical) / COP30 / SRTM / NASADEM.
