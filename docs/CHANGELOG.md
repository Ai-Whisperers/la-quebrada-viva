# CHANGELOG — La Quebrada Viva

Internal version log. Tracks renderer + material registry + camera helpers + delivery bundle status. **Not** a full git log — `git log --oneline` is canonical for that. This is the at-a-glance "what state are we in".

Conventions: ISO dates, present-tense bullets, file-level granularity only when a change affects external consumers (renderer determinism, sub-render protocol, bundle integrity).

---

## [Unreleased] — post-escritura sprint backlog

**Freeze status:** Renderer byte-freeze at `85e86aa` was scoped to the print-pack contents. Print-pack at `dist/print_pack_2026-06-27/` is SHA-pinned independently on disk, so the post-`85e86aa` polish work cannot retroactively change shipped bytes. Material-registry work is OPEN since 2026-06-15 (commit `78433a7`, Ivan-authorized escritura beauty sprint). `build_scene.py` composite path remains untouched pending escritura close (2026-06-27).

Planned (P1.A residue + P1.B):
- ~~`lqv/typologies/*` — Rule 4 stone-foundation plinth pass~~ — audit 2026-06-26 confirmed all 18 typologies satisfy Rule 4 in code (explicit foundation builders in 11; villa footings/pier blocks/PIER_LIFT/explicit sandstone course in 4; 3 exempt — boomhut treehouse, outdoor shower, candle_path). Pre-78433a7 "~13 missing" figure was stale.
- ~~HDRI swap to cerrado / Atlantic-Forest-edge — asset-researcher pass, CC0 / CC-BY 4.0 (P1.A.5)~~ — landed 2026-06-26 (see below).
- ~~`apply_xray_override` material swap (HOUSE_IMAGERY_SHOTLIST §3)~~ — landed 2026-06-26 (P1.B.3, see below).
- Per-variant lighting differentiation T1.6 + background-tree replacement (P1.C)

---

## [2026-06-26] — CC-DOC.6 render catalogue (asset, view, variant) restructure

- **docs** `scripts/build_render_catalogue.py` — new protocol-v2 `view` axis added end-to-end. `PROTOCOL_V2_VIEWS = ("hero3q", "elevation", "plan", "section", "interior", "xray")` constant + `DEFAULT_VIEW = "hero3q"` for legacy back-compat. New regexes `VARIANT_VIEW_RE = ^(A|B|C)_(<view>)\.png$` and `STEM_V2_RE = ^(.+?)_(A|B|C)_(<view>)$` parse the new filename grammar. `Render` dataclass gains `view: str` field between `variant` and `date`; flows through `asdict(r)` into `catalogue.json`. All 5 collectors (`collect_canonical_finals`, `collect_sub_flat`, `collect_sub_runs`, `collect_sub_latest`, `collect_monday`) populate `view` from protocol-v2 stems where present, default `hero3q` otherwise.
- **docs** `docs/render_catalogue/INDEX.md` — regenerated (926 renders / 53 assets). New "## View distribution (protocol-v2 axis)" table at top (`hero3q`=908, `elevation`=3, `plan`=3, `section`=3, `interior`=6, `xray`=3). Per-asset roster gains a `Views covered` column listing protocol-v2 views in canonical order. New "## Per-asset × view matrix" section emits a 6-column count grid per asset with `—` for uncovered cells; `bamboo_river_house` shows the full 6-view coverage backbone (26/3/3/3/3/3) from CC-TOOL.8 deterministic harness, `bamboo_beton_28` shows `hero3q`=24/`interior`=3.
- **docs** `docs/render_catalogue/by_asset/*.md` — 53 per-asset pages regenerated. New "Coverage by view" table at top. Section headers tagged `view=<view>`. Sort and group keys extended to `(date, run_tag, view, sub_variant, variant)`; intro line updated to "Grouped by run (date + tag), then view, then variant."
- **docs** `docs/render_catalogue/catalogue.json` — re-emitted with `view` field on every render entry. Closes MASTER_TODO CC-DOC.6.

---

## [2026-06-26] — CC-DOC.3 RESULTS_GUIDE multi-view shotlist

- **docs** `docs/RESULTS_GUIDE.md` — new §5 "Multi-view shotlist (`RENDER_VIEW` protocol v2)" inserted between the gallery (§4) and the legacy "How to read everything together" (renumbered to §6); old "Known gaps" renumbered §6 → §7. Subsections: §5.1 six core views table (`hero3q | elevation | plan | section | interior | xray`) with projection + what-it-shows columns and explicit asset-vs-scene scope note; §5.2 filename-grammar diagram parsing `cob_walls_B_elevation.png` into asset-slug × variant × view; §5.3 output landing patterns (canonical `renders/sub/runs/<RENDER_RUN_ID>_<asset>[_<tag>]/<variant>_<view>.png`, latest-mirror `renders/sub/latest/<asset>_<variant>_<view>.png`, flat back-compat `renders/sub/<asset>_<variant>.png` for `RENDER_VIEW=hero3q` only); §5.4 parcel-scale-driver migration note (22 drivers honour `RENDER_VIEW` via `make_view_camera` post-2026-06-26); §5.5 cross-references to `docs/sub_render_strategy.md` §3.5, `docs/HOUSE_IMAGERY_SHOTLIST.md` §5.1, `lqv/cameras.py`, `lqv/furniture.py`. Closes MASTER_TODO CC-DOC.3.

---

## [2026-06-26] — CC-DOC.1 top-level README

- **docs** `README.md` — created (was missing at repo root; only `LICENSES/README.md` + `.pytest_cache/README.md` existed). Cold-start entry: parcel location + ownership, 4-deliverable priority table (18 finals shipped at `85e86aa`, 62-ha digital twin at `4409dba`, escritura pack frozen at tag `escritura-2026-06-27` / `0081129`, housing-park master plan in progress), doc-pointer order (PROJECT_INDEX → STATUS → CLAUDE → ARCHITECTURE → docs/INDEX → MASTER_TODO → DEFERRED_BUGS), quick-run examples for `scripts/render_*.sh` + `make sub|boq|deck`, variant + HDRI map, 14 GB host serialization + AMD CPU-fallback constraints, MIT vs per-asset license split, GitHub remote pointer. Closes MASTER_TODO CC-DOC.1.

---

## [2026-06-26] — CC-TOOL.5 pyright actionable-diagnostic pass

- **fix** `lqv/amenities/eco_retreat_modern_oasis.py`, `lqv/subscene/hobbit_house.py`, `lqv/typologies/bamboo_wigwam_lodge.py`, `lqv/typologies/italian_stone_small_v1.py` — removed 5 dead-expression diagnostics (4 statement-expressions discarded by pyright as unused; no runtime semantics change).
- **fix** `scripts/fetch_copernicus_lcover.py:191-193` — `assert YEARS` + explicit `year = YEARS[0]` defensive init before the year-search loop, so the post-loop `year` reference cannot be `Unbound` on an empty input list.
- **fix** `scripts/stamp_license_stubs.py:30-37` — local `loader` binding + assert chain to narrow `spec.loader` from `Optional[Loader]` before `exec_module` call.
- **chore** `pyrightconfig.json` — added `"reportMissingImports": "none"`. Rationale: `bpy`, `mathutils`, `bmesh`, and `bl_math` ship no upstream type stubs, which would otherwise flood the diagnostic stream with ~100 false positives that mask real bugs. Cascade rules (`reportAttributeAccessIssue`, `reportIndexIssue`, `reportOperatorIssue`, `reportCallIssue`) stay at default since they legitimately catch real bugs in numpy/matplotlib/rasterio/h5py call paths.
- **docs** `docs/DEFERRED_BUGS.md` — appended low-priority post-escritura section logging the 4 legit non-cascade residuals (`bamboo_boomhut_treehouse.py:327` None-iter, `fetch_opentopo_dem.py:60/63` Optional-return, `analyze_dem.py:155/156` + `fetch_opentopo_dem.py:102` + `satellite/fetch_sentinel2.py:205` matplotlib `imshow(extent=…)` list-vs-tuple). Total cleanup effort ~30 min, none gate any render or escritura deliverable.
- Final pyright state: **101 errors, 0 warnings, 0 informations**. All 101 are cascade hits from the bpy stub-gap; no actionable in-tree work remains under CC-TOOL.5.

---

## [2026-06-26] — CC-TOOL.1 MCP socket retire decision

- **docs** `docs/MCP_STATUS.md` (new) — diagnostic + retire decision for the BlenderMCP `localhost:9876` socket. Confirmed dead (`Connection refused`, no `:9876` listener, no Blender daemon process). Decision: **retire for escritura phase** rather than revive — sub-render workflow does not need it and the ~4 GB daemon RSS contends with the 4.3 GB per-render peak on a 14 GB host. Revival recipe (`blender --background --python scripts/mcp_daemon.py`) preserved for post-escritura selective use. `scripts/mcp_daemon.py` stays gitignored. Closes CC-TOOL.1 as resolved-by-retire.

---

## [2026-06-26] — P1.A.5 HDRI swap to cerrado / Atlantic-Forest-edge biome

- **feat** `lqv/lighting.py:16-23` — `_HDRI_BY_VARIANT` rotated from African-savanna / boreal stock to Paraguarí ~26.6°S Atlantic-Forest-edge / cerrado transition reads. New picks: A=`bryanston_park_sunrise_4k.exr` @ 0.8 (dry-season warm sunrise), B=`xanderklinge_4k.exr` @ 1.4 (overcast wet-season midday gallery forest), C=`kloppenheim_07_4k.exr` @ 0.5 (civil-twilight blue hour with residual sky tone for firefly read). Variant-strength multipliers preserved — only the EXR filenames changed, so the existing Sun-lamp / sky-fallback paths are unmoved.
- **chore** `scripts/download_polyhaven_assets.py` — `EXTRA_HDRIS` appended with the 3 new primaries + 5 CC0 backups (`magalies_field_sunset`, `near_the_river_02`, `niederwihl_forest`, `belfast_open_field`, `kloppenheim_04`) for QA fallbacks. Single `python3 scripts/download_polyhaven_assets.py --only hdris` invocation lands all 8 EXRs into `assets/hdris/` (21 ok / 17 skip / 0 fail / 1812.9 MiB total).
- **chore** `assets/hdris/_unused_wrong_biome/` — quarantined the 3 displaced HDRIs (`kiara_1_dawn_4k.exr`, `misty_pines_4k.exr`, `qwantani_dusk_2_4k.exr`) — African savanna / boreal pines read against Paraguarí parcel was the dominant wrong-biome complaint. Files kept on disk per attribution-traceability (CC0 still credited even when retired).
- Smoke `italian_river_house_4pax` A/B/C serial @ preview / 64 spp / CPU fallback → `renders/sub/runs/hdri_cerrado_smoke_20260626_italian_river_house_4pax/{A,B,C}.png` at 5,150,432 / 5,066,946 / 4,759,927 bytes (non-black, biome-correct read confirmed).

Subsystem bump: Lighting dispatcher v2 → v3 (biome-correct HDRI rotation).

---

## [2026-06-26] — P1.B.1 interior furniture stubs wired across the 15 typology registry

- **feat** `lqv/furniture.py` — `furnish_interior(col, *, footprint_w, footprint_l, origin_xy, floor_z, pax, style, variant, name_prefix)` builds bed (1 or pair depending on `pax`) + bedside + dining table + 2 stools + shelf + variant-emissive lantern from procedural primitives. Style chains: `bamboo` / `lapacho` / `stone` / `cob` / `container`. Variant-keyed emission `{A: 0.0, B: 0.6, C: 1.0}` carries the dawn/inspection/dusk read into the interior view without forking the registry. Early-returns on footprints < 1.5 m to skip un-furnishable amenity stubs.
- **feat** all 15 entries of `lqv.typologies.TYPOLOGIES` now invoke `furnish_interior(...)` before `return col`, with floor-z anchored to each typology's habitable storey (foundation top / plinth top / pier lift / arched-base course / dome foundation) and footprint derived per-typology with wall-thickness margin:
  - `bamboo_beton_28`, `bamboo_beton_30`, `bamboo_river_house`, `bamboo_curved_roof_villa`, `bamboo_wigwam_lodge`, `bamboo_beton_family_curved`, `bamboo_beton_family_rectangular`, `bamboo_boomhut_treehouse`, `bamboo_container_4pax` → `style='bamboo'` / `'container'` as appropriate.
  - `container_river_house` → `style='container'`, floor on `PIER_LIFT`.
  - `clay_terracotta_estate` → `style='stone'`, floor on plinth + 10 cm GF slab.
  - `hobbit_house` → `style='cob'`, 3 × 3 m inscribed in the 3 m dome, floor on `FOUNDATION_H`.
  - `italian_river_house_4pax` → `style='stone'`, floor on `_BASE_HEIGHT` (atop arched foundation course).
  - `italian_stone_small_v1` / `italian_stone_small_v2` → `style='stone'`, floor on `_FOUNDATION_HEIGHT`.
- **fix** signature drift — `build_<typology>(origin, ...)` builders that previously dropped the `variant` kwarg from the wrapper's call now accept and forward `variant: str = 'A'`. Wrappers `build(parent, location, variant)` route variant through correctly so the interior lantern can read dawn/inspection/dusk emission.
- pytest 16/16 green; typology-contract + smoke tests unchanged. No render-byte regressions expected outside `RENDER_VIEW=interior` (default hero3q / elevation / plan / section / xray paths render the furniture but at parcel scale it falls below the resolution floor).

Subsystem bump: Typology registry v3 → v4 (variant-aware interior furniture).

---

## [2026-06-26] — P1.B.3 `apply_xray_override` shipped

- **feat** `lqv/subscene/base.py` — `apply_xray_override(scene, asset_collection=None, except_materials=None, alpha=0.15)` swaps non-opaque material slots to a shared Transparent BSDF + low-weight Principled mix shader. Paired `clear_xray_override()` restores originals from per-object `_lqv_xray_orig_<slot>` stash for symmetric teardown.
- **feat** `XRAY_OPAQUE_MATERIALS` frozenset — default opaque allowlist covers structural bamboo/lapacho, steel/mesh, services (micro_hydro_turbine, lifepo4_rack, cistern_shell, plumbing, fireplace_stack, mosquito_mesh — aspirational keys forward-compatible), water shaders (pool_water/water_reflective/stream_bed), glass (PV + bottles), and emissive accents (window_glow/firefly/lantern_paper_warm).
- **feat** `lqv/config.py` — `VALID_VIEWS` adds `'xray'`. `cfg.output_filename` already honours arbitrary non-`hero3q` views as `_<view>` suffix; legacy flat path stays back-compat.
- **chore** `save_subrender()` — fires `apply_xray_override(scene)` immediately before `render.run(scene)` when `cfg.view == 'xray'`. No effect on hero3q/elevation/plan/section/interior paths.
- Smoke `bamboo_river_house` variant B → 169 material slots swapped, `B_xray.png` = 4,933,755 bytes (distinct from B hero3q 5,070,274). pytest 16/16 green.

---

## [2026-06-26] — P1.B.2 camera-view dispatcher promoted to public API

- **feat** `lqv/cameras.py` — `make_view_camera(cfg, target, distance, height, lens)` public dispatcher honouring `cfg.view ∈ {hero3q, elevation, plan, section, interior}`. Replaces the private `_make_view_camera` previously living in `lqv/subscene/base.py`.
- **fix** `lqv/subscene/bamboo_river_house.py` + 22 other bypass-pattern drivers — migrated from `cameras.subscene_camera(...)` to `cameras.make_view_camera(cfg, ...)` so parcel-scale drivers that bypass `base.run()` honour `RENDER_VIEW`. Pre-fix all four "views" produced identical 5,070,274-byte renders because the dispatcher never fired on the bypass path.
- **chore** `lqv/subscene/base.py` — `run()` now calls the public dispatcher; `save_subrender()` retains `_<view>` filename suffix (default `hero3q` omits the suffix → legacy flat `renders/sub/<asset>_<variant>.png` invariant preserved).
- Smoke batch (`bamboo_river_house`, variant B, 4 views) → 4 distinct PNG sizes (2,912,071 / 4,634,966 / 2,744,759 / 3,795,393). Hero3q regression render preserved exact 5,070,274-byte baseline. pytest 16/16 green.

Subsystem bump: Camera helpers v0 → v1.

---

## [2026-06-15] — post-review polish wave at `78433a7`

Three high-leverage shader/loader bugs from the critic pass shipped under Ivan-authorized escritura beauty sprint carve-out. Print-pack SHA pinning unaffected (independent on-disk artefacts).

- **fix** `lqv/materials/glass.py` — `water_reflective` dielectric Principled (base 0.02/0.06/0.10, IOR 1.333, transmission 1.0, roughness 0.04); `make_pool_water()` Principled + Volume Absorption stack. Closes DEFERRED_BUGS Bug 1.
- **fix** `lqv/materials/wood.py` — `lapacho_timber` upgraded from flat principled to `textured_principled('old_planks_02')` PBR trio tinted toward heartwood palette + secondary Voronoi color variation; bamboo split into culm/leaf/grass with node-ring shader helper. Closes DEFERRED_BUGS Bug 2.
- **fix** `lqv/flora/photoreal.py` — `_LOADED_HEROES` cache + `cached.copy()` deep-copy pattern replaces re-append-and-suffix path. Closes DEFERRED_BUGS Bug 3 (no more `.003` LOD-name collisions; `RENDER_FLORA_PHOTOREAL=1` clean across 51 subscene jobs).
- **feat** subscene drivers / typologies / amenities polish wave landed in the same omnibus commit (see `git show 78433a7 --stat`).

---

## [2026-06-25] — T-2 freeze-safe maintenance

- **add** `docs/MASTER_TODO.md` — single consolidated multi-phase TODO covering P0a through P5 + cross-cutting tracks
- **add** `docs/HOUSE_IMAGERY_SHOTLIST.md` — 24-shot matrix × 16 typologies, exterior + plan + section + interior + x-ray spec, gated on freeze lift
- **add** `scripts/gc_render_runs.py` — dry-run-default GC for `renders/sub/runs/` with protected-tag retention. Do NOT run with `--apply` pre-escritura.
- **add** `scripts/organize_sub_renders.py` — browse-friendly symlink tree at `renders/sub_by_category/` over the flat `renders/sub/` path
- **fix** `scripts/download_polyhaven_assets.py` — lowercase Poly Haven slug IDs (case-sensitive on the API)
- **chore** `.gitignore` — exclude regenerable `renders/sub_by_category/` symlink tree

No renderer code touched. Pytest invariants: 16/16 green at `85e86aa`.

---

## [2026-06-17] — escritura print-pack T-10 verified — tag `escritura-t10-verified-2026-06-17`

- print-pack frozen at `dist/print_pack_2026-06-27/`
- Wesley bundle `wesley_bundle_20260616-1715.zip` SHA `9ce96b85…85724a53c` pinned across 15+ docs
- escritura deck v6 SHA `2e4c265c…1eba5c0860701137` (28 pages)
- VERIFY.sh: 3/3 green
- POSTMORTEM, DECISIONS, ROLLBACK, WALLET_CARD, BUNDLE_README, Reply-To landed

## [2026-06-16] — GitHub remote landed

- remote pushed to `Ai-Whisperers/la-quebrada-viva` (private)
- closes archived UPGRADE_PLAN T0.1 (single-disk SPOF mitigation pre-escritura)

## [2026-06-14] — escritura v-final candidate frozen — tag `escritura-v-final-candidate-aecb1af`

- 18/18 finals at `85e86aa`; pytest 16/16 invariants green
- DEFERRED_BUGS.md captures Bug 1 (water shader), Bug 2 (lapacho timber), Bug 3 (flora LOD collision) for post-freeze sprint

## [2026-06-11] — 62-ha digital twin shipped at `4409dba`

- ALOS-AW3D30 DEM + Sentinel-2 albedo + features sub-render
- terrain variants A/B/C rendered

## [2026-06-10] — 18/18 finals shipped at `85e86aa`

- byte-freeze established here; renderer locked until escritura signs

---

## Subsystems tracked

When a subsystem version bumps, increment its tag and add a one-line entry above.

| Subsystem | Version | Last touched | Notes |
|---|---|---|---|
| `build_scene.py` | frozen | 2026-06-10 (`85e86aa`) | composite path byte-identity preserved through 2026-06-27 |
| Material registry (`lqv/materials.py`) | v2 | 2026-06-15 (`78433a7`) | water dielectric + lapacho_timber PBR + bamboo split landed; DEFERRED_BUGS 1+2 closed |
| Flora loader (`lqv/flora/photoreal.py`) | v2 | 2026-06-15 (`78433a7`) | `_LOADED_HEROES` deep-copy cache; DEFERRED_BUGS 3 closed |
| Sub-render protocol (`lqv/subscene/`) | v2 | 2026-06-26 | v1 `RENDER_RUN_ID` + runs/latest mirror; v2 adds `apply_xray_override` + `XRAY_OPAQUE_MATERIALS` (P1.B.3) — `RENDER_VIEW=xray` now legal |
| Camera helpers | v1 | 2026-06-26 | `cameras.make_view_camera(cfg, ...)` public dispatcher; `RENDER_VIEW={hero3q,elevation,plan,section,interior,xray}`; 22 bypass-pattern drivers migrated |
| BoQ scope filter | v1 | 2026-06-15 | `LQV_BOQ_SCOPE=escritura` ($268,685.45) vs `=full` ($288,056) |
| Wesley bundle | `20260616-1715` | 2026-06-16 | SHA-pinned, do not rebuild pre-escritura |
| Escritura deck | v6 | 2026-06-16 | 28pp, SHA-pinned in print-pack |
