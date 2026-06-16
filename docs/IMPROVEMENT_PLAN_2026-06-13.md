# LQV Improvement Plan — 2026-06-13

Numbered actions derived from `docs/CRITIQUE_2026-06-13.md`. Renderer at `85e86aa` is byte-frozen; no item below modifies `lqv/build_scene.py`. P0 items are escritura blockers (deadline 2026-06-27).

> **Status @ 2026-06-15:** P0 sweep (#1–#8) **DONE in commit `78433a7`** (post-review polish wave) with foundation work at `de5d5d8` (terrain DSL + Wesley catalog). BoQ rollup last regenerated at `0f44cf5` after `bamboo_container_4pax` takeoff split.
> **P1 partial sweep @ 2026-06-15 (T-12 to escritura):** items #14 (`per_material_rollup` per-(material,unit) split + regression tests), #15 (`_iter_modules` sorted for deterministic BoQ row order), #16 (pandoc PDF magic-byte guard), #17 (per-module rollup exceptions logged + re-raised) all ✅ DONE. Verified against current code at `lqv/boq.py:145-152, 168, 208-238, 354` and `tests/test_boq_rollup.py` (2 passed). `make boq` regenerated 2026-06-15 23:45 with deterministic ordering: 159 lines, 17 assets, $268,685.45 USD / Gs. 1,961,403,785 @ `docs/boq/boq_rollup.{csv,md,pdf}`.
> **Day-2/3 deliverables @ 2026-06-15 (T-12):** DEM A/B cross-check `docs/site_data/dem_ab_contact.png` (34 KB) ✅, Pelton head feasibility map `docs/site_data/pelton_head_map.{png,json}` ✅ (300 m penstock radius on COP30: head_max=182.6 m, mean=33.4 m, 31.2% pixels ≥ 30 m Pelton-min, 10.7% ≥ 80 m good-Pelton), Wesley deliverable bundle `dist/wesley_bundle_20260615-2352.zip` ✅ (271 MB, 34 files, sha256=1b0b4d5a56fee9dc…, manifest sidecar). Bundle contents: brief PDF, escritura deck v6, 18 hero finals (A/B/C × 6 cams), 6 T-DT renders (birdseye+oblique × A/B/C), DEM contact sheet, Pelton head map, BoQ trio, PROVENANCE.md, satdata brief. No missing expected files.
> Plan body below is left verbatim for audit trail — do not re-trigger P0 fixes; verify against current code first. Remaining P1 items (#9-#13, #18+) and P2 deferred post-escritura.

---

### #1 — Repair broken TYPOLOGIES contract
**Priority**: P0
**File(s)**: `lqv/typologies/__init__.py:21`
**Problem**: `TYPOLOGIES` tuple includes `'cob_bottle_lqv'`, but no `lqv/typologies/cob_bottle_lqv.py` exists; the implementation lives at `lqv/subscene/cob_bottle_lqv.py`. Any importer that maps `TYPOLOGIES` through `importlib.import_module(f"lqv.typologies.{name}")` crashes on the first entry.
**Action**: Decide whether `cob_bottle_lqv` is a typology or a subscene. If typology: move `lqv/subscene/cob_bottle_lqv.py` to `lqv/typologies/` and update its `MATERIAL_TAKEOFF` registration site. If subscene-only: remove `'cob_bottle_lqv'` from the `TYPOLOGIES` tuple and from any docs that claim 13 typologies. Add a unit test in `tests/` that asserts every name in `TYPOLOGIES` resolves via `importlib`.
**Estimated effort**: S

### #2 — Fix `_infer_qty` silent zero fallback
**Priority**: P0
**File(s)**: `lqv/boq.py:119-123`; `lqv/typologies/bamboo_container_4pax.py:180-184`
**Problem**: When `_infer_qty` finds no recognized qty key it returns `(0.0, 'count')` with no warning. `shipping_container_20ft` ships with only `count` + `unit_cost_usd` and silently rolls up as quantity 0, understating the BoQ by a 20-ft container.
**Action**: Add `'count'` to `_QTY_FIELDS` (or a new `_COUNT_FIELDS` map that pairs with `'unit': 'count'`). If no key is found, raise a `ValueError` naming the offending material key and module rather than returning zero. Re-generate `docs/boq/boq_rollup.md` and diff against the previous run to find every silently-zeroed line; expect the bamboo container line to reappear with a real number.
**Estimated effort**: S

### #3 — Make `validate_geo` houses-under-water check meaningful
**Priority**: P0
**File(s)**: `lqv/site/terrain_dsl.py:414-427`
**Problem**: Sampling `sample_height` at footprint corners after `_incise_channel` has carved the heightfield checks the carved-around surface, not the un-carved one. Any creek that clips a foundation is hidden by the carve.
**Action**: Snapshot the pre-carve heightfield in `_build_heightmap` before any channel incision, store as `self._pre_carve_heights`. In `validate_geo`, sample both pre- and post-carve and report when the pre-carve sample is below `creek.z + safety_margin_m` at any corner. Keep the current post-carve sample as an informational secondary check.
**Estimated effort**: M

### #4 — Replace `except RuntimeError: pass` in hobbit_house modifier-apply
**Priority**: P0
**File(s)**: `lqv/typologies/hobbit_house.py:192-197, 293-296`
**Problem**: Modifier-apply failures (bad context, no active object, modifier disabled) are silently swallowed. The hero hobbit-house dome can ship with an un-applied modifier stack and the BoQ/render pipeline will never report it.
**Action**: Replace both bare `pass` blocks with logged retries: wrap in `with bpy.context.temp_override(active_object=obj, selected_objects=[obj]):` and call `bpy.ops.object.modifier_apply(modifier=mod.name)`; on `RuntimeError`, log the modifier name + object name at WARNING and re-raise. If a legitimate failure mode exists (e.g. modifier already applied earlier), guard explicitly with `if mod.name not in obj.modifiers: continue` rather than try/except.
**Estimated effort**: S

### #5 — Remove silent except blocks in `eco_retreat_modern_oasis`
**Priority**: P0
**File(s)**: `lqv/amenities/eco_retreat_modern_oasis.py:596, 605-606, 618, 627-628`
**Problem**: Four `except Exception:` blocks, two of which are bare `pass`. Material lookups, modifier ops, and boolean ops can silently no-op on the most prominent amenity. Banned per project-wide CLAUDE.md.
**Action**: For each except, identify the specific exception expected. Replace bare `pass` with a `logger.warning` that names the operation and the object, then either continue with an explicit fallback or re-raise. If the block is genuinely guarding a known-optional operation, guard with an explicit feature probe (e.g. `if hasattr(obj.modifiers, 'apply')`) rather than try/except.
**Estimated effort**: S

### #6 — Delete dead `roof_faces` block with literal-typo bug
**Priority**: P0
**File(s)**: `lqv/subscene/terrain_62ha.py:398-406`
**Problem**: `roof_faces` is assigned twice; the first assignment contains a placeholder tuple `(3, 7 - 0, 0, 0)` — an arithmetic expression that resolves to a `(3, 7, 0, 0)` quad and is then overwritten. Dead code with a typo in a hero file undermines confidence in the rest of the module.
**Action**: Delete the first assignment outright. If git-blame confirms it was an in-progress experiment, file an issue and link the commit; if it was a copy-paste from another typology, audit the source for the same typo.
**Estimated effort**: XS

### #7 — Unify USD_TO_PYG into a single FX source
**Priority**: P0
**File(s)**: `lqv/boq.py:42`; `scripts/build_escritura_deck.py:57, 331, 711, 761`
**Problem**: FX rate is duplicated as `7300.0` (boq) and `7300` (deck). Same name, different type, two update sites. When the rate moves between now and 2026-06-27, only one will get updated.
**Action**: Create `docs/finance/fx.json` with `{"USD_PYG": 7300.0, "as_of": "2026-06-13", "source": "<bank-or-BCP-quote>"}`. Add `lqv.finance.get_usd_to_pyg()` that reads it and caches. Replace both literal `USD_TO_PYG` constants with calls to this function; delete the local constants. Stamp the `as_of` date into the escritura deck so the notary sees the source.
**Estimated effort**: S

### #8 — Stop hardcoding `TODAY_ISO`
**Priority**: P0
**File(s)**: `scripts/build_escritura_deck.py:58`
**Problem**: Date is baked as a string literal. Any rerun after 2026-06-13 stamps yesterday onto the escritura artefact.
**Action**: Replace with `TODAY_ISO = os.environ.get('LQV_TODAY_ISO') or datetime.date.today().isoformat()`. Keep the env-var override so deterministic regression tests can pin the date.
**Estimated effort**: XS

### #9 — Define `PARCEL_CLIP_END_M` constant and replace 20 magic numbers
**Priority**: P1
**File(s)**: `lqv/subscene/base.py:147`; 19 driver files (bamboo_beton_family_curved.py:59, bamboo_wigwam_lodge.py:73, floating_dining.py:48, italian_river_house_4pax.py:67, bamboo_beton_28.py:53, bamboo_boomhut_treehouse.py:36, bamboo_container_4pax.py:91, bamboo_beton_30.py:49, bamboo_beton_family_rectangular.py:116, boulder_cluster.py:144, bamboo_river_house.py:78, eco_pool.py:46, eco_retreat_modern_oasis.py:60, container_river_house.py:54, flora_jacaranda.py:63, flora_pachira.py:53, hobbit_house.py:78, flora_anthurium.py:63, italian_stone_small_v2.py:53, labrisa_lounge.py:60); `lqv/subscene/terrain_62ha.py:635`
**Problem**: Default `clip_end=1000.0` is wrong for parcel scale; 20 files independently override to `20000.0`. The next driver author forgets and renders a black HDRI.
**Action**: Add `PARCEL_CLIP_END_M = 20000.0` to `lqv/subscene/base.py` (module-level). Change `run(...)` default to `clip_end=PARCEL_CLIP_END_M`. Sed-replace `cam.data.clip_end = 20000.0` across the 20 files with `cam.data.clip_end = base.PARCEL_CLIP_END_M`. Verify A/B/C re-render byte-identical against the byte-frozen baseline `85e86aa`.
**Estimated effort**: S

### #10 — Fix `cut` snap mode to actually cut
**Priority**: P1
**File(s)**: `lqv/site/terrain_dsl.py:352`
**Problem**: `target_z = float(min(corner_heights))` raises low cells to the minimum corner when the minimum is above existing terrain; this is "flatten-to-min", not "cut".
**Action**: Add a third mode `'cut'` that only lowers cells (`new_h = min(existing_h, target_z)`) and rename current behavior to `'flatten_to_min'`. Audit callers in `lqv/site/parcels.py` and any T-DT subscene to pick the intended mode. Default to `'flatten_to_min'` to preserve existing renders; switch creek-side pads to `'cut'`.
**Estimated effort**: S

### #11 — Add sign check to creek slope validator
**Priority**: P1
**File(s)**: `lqv/site/terrain_dsl.py:451`
**Problem**: Uses absolute `drop / length`; no sign. An uphill polyline with the same magnitude passes the threshold the same way a downhill one does.
**Action**: Compute `signed_slope = (end_z - start_z) / length_m` and flag `signed_slope > -0.005` (i.e. anything not falling at ≥0.5%) as "still water risk", with a separate explicit "creek flows uphill" issue for `signed_slope > 0`.
**Estimated effort**: XS

### #12 — Replace AABB-on-rotated-rect overlap with SAT or shapely
**Priority**: P1
**File(s)**: `lqv/site/terrain_dsl.py:464-471, 474-485`
**Problem**: AABB-vs-AABB on rotated footprints produces false positives on diagonals; scatter polygon vs house AABB does the same. The audit log fills with noise that hides real issues.
**Action**: Add a `_polygons_overlap(poly_a, poly_b)` helper using a Separating Axis Theorem implementation (or `shapely.geometry.Polygon(...).intersects(...)` if `shapely` is acceptable in the build env — it is pure Python from PyPI). Replace both checks. Keep the AABB pass as a fast pre-filter.
**Estimated effort**: M

### #13 — Kill three-level silent material fallback in `_grammar`
**Priority**: P1
**File(s)**: `lqv/amenities/_grammar.py:128`; `lqv/typologies/hobbit_house.py:140`
**Problem**: `_mat('lantern_paper_warm') or _mat('pv_glass') or _mat('glass')` silently substitutes when keys are missing; renamed or deleted materials disappear without a log line.
**Action**: Replace the `or`-chain with an explicit `_require_mat(name)` that raises `KeyError(f"material {name!r} missing")` if absent. Where a real fallback is intentional, expose it via `_mat_with_fallback(primary, fallback)` that logs `WARNING` when the fallback is used. Audit all call sites in `_grammar.py:51,63,101,133,146,186` and `hobbit_house.py:140` and convert each to one or the other.
**Estimated effort**: S

### #14 — Make `per_material_rollup` mixed-unit handling honest
**Priority**: P1
**Status**: ✅ DONE @ 2026-06-15. Implementation now at `lqv/boq.py:208-238` (rollup keyed on `(material, unit)`, no more `'mixed'` bucket). Regression guard at `tests/test_boq_rollup.py::test_no_mixed_zero_qty_row` + USD-desc sort invariant at `tests/test_boq_rollup.py::test_rollup_deterministic_usd_desc`. Both PASS.
**File(s)**: `lqv/boq.py:208-238`
**Problem**: Mixed-unit groups are emitted as `unit='mixed', quantity=0.0`. Any reader sees quantity 0 on a real material; the notary will flag it.
**Action**: Split mixed-unit groups into one row per unit (`bamboo (m)`, `bamboo (kg)`) instead of collapsing. Keep a single `material` column for grouping/sort, but emit per-unit quantity correctly. Add a unit test that asserts no rollup row has `quantity == 0.0 and unit == 'mixed'`.
**Estimated effort**: S

### #15 — Sort `by_module` for reproducible BoQ
**Priority**: P1
**Status**: ✅ DONE @ 2026-06-15. Actual fix site is `lqv/boq.py:145-152` (`_iter_modules` helper, not the `:295-297` line range originally cited — that pointer was stale). `pkgutil.iter_modules(...)` is now wrapped in `sorted(..., key=lambda m: m.name)`. `make boq` re-run 2026-06-15 23:45 produced deterministic `docs/boq/boq_rollup.{csv,md,pdf}` (159 lines, 17 assets, $268,685.45 USD).
**File(s)**: `lqv/boq.py:145-152`
**Problem**: `pkgutil.iter_modules` returns filesystem order; row order in the escritura BoQ drifts between machines.
**Action**: Wrap the iteration in `sorted(..., key=lambda m: m.name)`. Add a test that runs `collect_all()` twice and asserts row order is stable. Re-render `docs/boq/boq_rollup.md` and commit the (now deterministic) output.
**Estimated effort**: XS

### #16 — Verify pandoc PDF output by magic bytes
**Priority**: P1
**Status**: ✅ DONE @ 2026-06-15 (verified pre-existing in code at `lqv/boq.py:354`). After pandoc returns, output is opened binary-mode and the first 5 bytes are asserted `== b'%PDF-'`; on mismatch the actual first 32 bytes are logged and a `RuntimeError` is raised.
**File(s)**: `lqv/boq.py:354`
**Problem**: `rc == 0 and size > 0` accepts a non-PDF fallback file. A pandoc misconfig that emits HTML still "succeeds".
**Action**: After pandoc returns, open the output binary and assert the first 5 bytes are `b'%PDF-'`. On mismatch, log the actual first 32 bytes and raise. Same check belongs in any other artefact-generating script before `subprocess.run` returns.
**Estimated effort**: XS

### #17 — Stop swallowing BoQ rollup exceptions
**Priority**: P1
**Status**: ✅ DONE @ 2026-06-15 (verified pre-existing in code at `lqv/boq.py:168`). Per-module rollup exceptions are now logged with `logger.error(..., exc_info=True)`, recorded in a failure-list, and re-raised after the loop completes with a summary listing every failed module. No silent module-row vanishing.
**File(s)**: `lqv/boq.py:168`
**Problem**: `except Exception as e:` with no log; a typo in any typology's `MATERIAL_TAKEOFF` literal vanishes the whole module's rows.
**Action**: Replace with `except Exception as e: logger.error("BoQ rollup failed for %s: %s", module_name, e, exc_info=True); raise`. If the intent is to keep collecting from other modules after one fails, log + record the failure and re-raise after the loop with a summary of all failed modules.
**Estimated effort**: XS

### #18 — Pin `RENDER_RUN_ID` or fail loudly
**Priority**: P1
**File(s)**: `lqv/subscene/base.py:36`
**Problem**: Falls back to a timestamp when env var is unset; batch renders desync into separate folders.
**Action**: If `os.environ.get('RENDER_RUN_ID')` is unset and `os.environ.get('LQV_ALLOW_TIMESTAMP_RUN_ID') != '1'`, raise with a clear message. Update `scripts/smoke_test.sh` and `scripts/render_queue.py` to set `RENDER_RUN_ID` explicitly. Document the override in `docs/render-runs.md`.
**Estimated effort**: XS

### #19 — Centralise A/B/C variant parameters
**Priority**: P1
**File(s)**: `lqv/subscene/base.py:120-125`; plus HDRI/sun overrides across driver files
**Problem**: `(-0.2, 0.3, 0.6)` exposure offsets are duplicated by per-driver overrides for HDRI rotation, sun strength, etc. No single source of truth.
**Action**: Define `VARIANT_PROFILES: dict[str, dict] = {'A': {...}, 'B': {...}, 'C': {...}}` in `base.py`. Each profile carries exposure, sun strength multiplier, HDRI rotation delta, and any other A/B/C knob. Driver files read `base.VARIANT_PROFILES[variant]` rather than re-deriving from variant name.
**Estimated effort**: M

### #20 — Replace triple-write copy with symlinks
**Priority**: P2
**File(s)**: `lqv/subscene/base.py:137-138`
**Problem**: `shutil.copy2` triple-writes every render (run folder + `latest/` + legacy flat). 3× disk + 3× I/O per save.
**Action**: Write the canonical file once into `renders/sub/runs/<run>/<variant>.png`. Make `latest/<variant>.png` a relative symlink (or hardlink, where filesystems disagree). Drop legacy flat path or, if downstream tools depend on it, generate it once at end-of-run via a single `make_legacy_aliases()` pass.
**Estimated effort**: S

### #21 — Replace nested-list heightmap with numpy array
**Priority**: P2
**File(s)**: `lqv/subscene/terrain_62ha.py:158-161`
**Problem**: `list[list[float]]` for a 4K heightmap is ~64 MB of Python objects + GC overhead; the headless renderer machine will swap.
**Action**: Load as `np.asarray(heightmap, dtype=np.float32)` immediately after parsing. Replace downstream `[y][x]` indexing with `heightmap[y, x]`. Profile peak RSS before/after with `tracemalloc` to confirm.
**Estimated effort**: S

### #22 — Route `terrain_62ha` materials through the MAT registry
**Priority**: P2
**File(s)**: `lqv/subscene/terrain_62ha.py:193-226`
**Problem**: Local `_emission_material` / `_principled_material` helpers bypass the `MAT` registry; two material-creation paths in the same project guarantee drift.
**Action**: Move those helpers to `lqv/materials/emission.py` and `lqv/materials/principled.py` with a `build(MAT)` entry point each. Call them from `lqv/materials/__init__.py`. Replace the local calls in `terrain_62ha.py` with `MAT['<key>']` lookups.
**Estimated effort**: M

### #23 — Replace `i % N` pseudo-randomness with seeded RNG
**Priority**: P2
**File(s)**: `lqv/subscene/terrain_62ha.py:462`; `lqv/amenities/_grammar.py:185`
**Problem**: `1.0 + 0.18 * ((i % 3) - 1)` and `r = boulder_radius_m * (0.85 + 0.30 * ((i * 37) % 7) / 7.0)` are deterministic only by coincidence; visible cyclic banding at large `i`.
**Action**: Replace with `np.random.default_rng(seed=SEED_BASE + i)` calls and uniform sampling in the documented range. Keeps determinism, removes the visible 3- and 7-period bands.
**Estimated effort**: XS

### #24 — Bring `make_pool_water` into the `build(MAT)` pattern
**Priority**: P2
**File(s)**: `lqv/materials/glass.py:41`; `lqv/materials/__init__.py:47`
**Problem**: `MAT['pool_water'] = glass.make_pool_water()` is a one-off insertion outside the standard `submodule.build(MAT)` fanout used by earth/wood/foliage/props.
**Action**: Either move `pool_water` to a new `lqv/materials/water.py` with `build(MAT)`, or extend `glass.build(MAT)` to register it under `MAT['pool_water']`. Delete the one-off line in `__init__.py`.
**Estimated effort**: XS

### #25 — Guard Blender 4.2 `Transmission Weight` socket name
**Priority**: P2
**File(s)**: `lqv/materials/glass.py:56`
**Problem**: `bsdf.inputs['Transmission Weight']` raises `KeyError` if Blender ever reverts or renames the socket. No fallback.
**Action**: Add a helper `def _set_socket(bsdf, names: list[str], value)` that tries each name in order and logs the one used. Call sites: `_set_socket(bsdf, ['Transmission Weight', 'Transmission'], 1.0)`. Same helper covers any future rename and reads as a feature probe rather than swallowed-exception code.
**Estimated effort**: XS

### #26 — Replace `_PermissiveNS` bpy stub with a documented test double
**Priority**: P2
**File(s)**: `scripts/build_boq.py:26-69`
**Problem**: `_PermissiveNS` silently returns truthy for any attribute access; isinstance/issubclass checks against `bpy.types.*` return falsy with no signal. A future typology with import-time bpy usage will drop rows silently.
**Action**: Either (a) replace the stub with `unittest.mock.MagicMock(spec=...)` and lock down the surface, or (b) actually run BoQ collection inside a headless Blender (`blender --background --python ...`) and drop the stub entirely. Option (b) is more robust but slower; option (a) is faster but requires per-attribute spec.
**Estimated effort**: M

### #27 — Delete `_install_materials_stub` no-op
**Priority**: P2
**File(s)**: `scripts/build_boq.py:75-84`
**Problem**: Dead-ish function kept for back-compat; confuses the next contributor.
**Action**: Search the repo for any caller; if none, delete the function and its call site. If a caller exists, replace it with the real materials stub it claims to be backstopping.
**Estimated effort**: XS

### #28 — Harden `render_queue` regex against STATUS.md drift
**Priority**: P2
**File(s)**: `scripts/render_queue.py:28`
**Problem**: Regex is coupled to exact `STATUS.md` table format; a column rename silently returns `0 pending` and the operator thinks the queue is empty.
**Action**: After parsing, assert `parsed_rows > 0 if STATUS_MD.read_text().strip() else True` and raise `RuntimeError("STATUS.md present but regex matched 0 rows; format may have changed")`. Add a small fixture-based test in `tests/` covering the current STATUS table format.
**Estimated effort**: XS

### #29 — Pick one BoQ source for the deck builder
**Priority**: P2
**File(s)**: `scripts/build_escritura_deck.py:22, 31-32`
**Problem**: Reads `lqv.boq.collect_all()` AND parses `docs/boq/boq_rollup.md` text; two parsers, two drift paths.
**Action**: Keep `lqv.boq.collect_all()` as the single source. Delete the markdown-parsing path. If the markdown is needed for human review, generate it from `collect_all()` and treat the rendered file as a build artefact (gitignored or stamped).
**Estimated effort**: S

### #30 — Split `build_escritura_deck.py` along section boundaries
**Priority**: P2
**File(s)**: `scripts/build_escritura_deck.py` (842 lines total)
**Problem**: Largest file in the repo and one of two artefacts the notary sees. Hardest to review.
**Action**: Extract per-slide builders (`_build_overview`, `_build_typology_pages`, `_build_boq_pages`, `_build_finance_pages`) into `scripts/deck/*.py` modules with a thin `build_escritura_deck.py` orchestrator (target ≤200 lines). Do this AFTER 2026-06-27 (renderer-and-deck freeze) to avoid escritura risk.
**Estimated effort**: L

### #31 — Add typology/amenity consistency tests
**Priority**: P2
**File(s)**: `lqv/typologies/__init__.py`; `lqv/amenities/__init__.py`; new `tests/test_module_consistency.py`
**Problem**: Hand-maintained `TYPOLOGIES` / `AMENITIES` tuples can drift from the directory contents (see item #1 for the proof).
**Action**: Write `test_module_consistency.py` that asserts:
1. Every entry in `TYPOLOGIES` resolves via `importlib.import_module`.
2. Every `.py` file in `lqv/typologies/` (excluding `__init__.py`, `_*.py`) is listed in `TYPOLOGIES`.
3. Same two checks for `AMENITIES`.
Run in CI on every commit.
**Estimated effort**: S

### #32 — Repo hygiene pass
**Priority**: P2
**File(s)**: repo root
**Problem**: `wes example ideas images ` folder has a trailing space (breaks shell tab-completion); `STATUS.md` + `AUTONOMOUS_PLAN.md` parallel at root; `_archive/build_scene.py.pre-refactor.bak` next to the byte-frozen renderer is a foot-gun.
**Action**: Rename the folder to `wes_example_ideas_images/` (or move under `docs/inspiration/`). Move `AUTONOMOUS_PLAN.md` to `docs/plans/AUTONOMOUS_PLAN_2026-06-13.md` and link from `STATUS.md`. Move `_archive/build_scene.py.pre-refactor.bak` to `_archive/build_scene.py.pre-refactor.85e86aa.bak` and add a `_archive/README.md` warning that nothing under `_archive/` should ever be diffed-into-place.
**Estimated effort**: XS

### #33 — Replace `bpy.ops`-heavy primitives with `bpy.data` constructors
**Priority**: P2
**File(s)**: `lqv/amenities/_grammar.py:51, 63, 101, 133, 146, 186`; `lqv/typologies/hobbit_house.py:167-204`
**Problem**: `bpy.ops.mesh.primitive_*` and `bpy.context.active_object` depend on operator context; headless renders are notoriously fragile under context overrides.
**Action**: Replace each primitive op with `bpy.data.meshes.new(...)` + manual `from_pydata` + `bpy.data.objects.new(...)` + `bpy.context.scene.collection.objects.link(...)`. For `_half_dome` in `hobbit_house.py:167-204`, generate vertices/faces analytically (UV sphere top-half) rather than ops chain. Re-render `hobbit_house` A/B/C and bit-compare against the frozen baseline; expect identical output.
**Estimated effort**: L

### #34 — Rotate `scene.blend.session-backup`
**Priority**: P2
**File(s)**: `scripts/smoke_test.sh:6`
**Problem**: Single backup slot, overwritten every run; if a smoke test corrupts the scene, the backup is the corrupted scene.
**Action**: Replace with `cp scene.blend "scene.blend.session-backup.$(date +%Y%m%d_%H%M%S)"` and a tail-N cleanup (`ls -t scene.blend.session-backup.* | tail -n +6 | xargs rm -f`). Keep last 5 backups.
**Estimated effort**: XS

### #35 — Make `cam.data.clip_end` set unconditional in `terrain_dsl`
**Priority**: P2
**File(s)**: `lqv/site/terrain_dsl.py:628-630`
**Problem**: Asymmetric `if cam.data.clip_end < self.z_clip_end` — only raises, never lowers; documented invariant in `MEMORY.md` says "set", not "max".
**Action**: Replace conditional with unconditional assignment `cam.data.clip_end = self.z_clip_end`. If anything downstream depends on the asymmetric behavior, surface that in a docstring and a comment with the why; otherwise enforce the invariant.
**Estimated effort**: XS
