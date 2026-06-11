# UPGRADE_PLAN — Fix Plan Derived from CRITIQUE_2026-06-10

Comprehensive fix plan for everything identified in `docs/CRITIQUE_2026-06-10.md`. Organized into four priority tiers by **escritura-criticality (2026-06-27, 17 days out)** and **delivery value**. Each item names: the defect (back-pointer to critique section), the fix, the acceptance criterion, the rough effort, and dependencies.

This is the action list. `docs/CRITIQUE_2026-06-10.md` is the diagnosis. `docs/sub_render_strategy.md` is the workflow that lets us execute Tier 1/2 in parallel without re-rendering the monolithic scene every time.

Companion documents:
- `CRITIQUE_2026-06-10.md` — source roast.
- `sub_render_strategy.md` — the new modular render workflow.
- `CLAUDE.md` — self-upgrade with the standing rules below.
- `STATUS.md` §4 — task ledger #32-#46 derives from this file.

---

## Tier 0 — escritura-critical, ship in the next 17 days

These directly de-risk the 2026-06-27 closing. None of them require an MCP socket or external dependency.

### T0.1 — Push to GitHub remote (CRITIQUE §1)

- **Defect**: no remote, single-disk SPOF. Hardware failure deletes the deliverable.
- **Fix**: create private GitHub repo `ai-whisperers/house-field`, `git remote add origin git@github.com:ai-whisperers/house-field.git`, `git push -u origin master`.
- **Acceptance**: `git remote -v` shows `origin`; the latest commit is browsable on github.com.
- **Effort**: 5 minutes.
- **Dependency**: a GitHub account with `gh auth status` working, or an SSH key registered.
- **Owner default**: AI Whisperers session executes; Ivan provides the credential confirmation.
- **Risk if deferred**: catastrophic deliverable loss on disk failure.

### T0.2 — `.gitignore` defensive additions (CRITIQUE §1)

- **Defect**: `__pycache__/` untracked-but-not-ignored; `_preview_*.png` clutter renders/; `scene.blend.session-backup` clutters working tree; `.env.local` is only protected by staging discipline.
- **Fix**: append to `.gitignore`:
  ```
  __pycache__/
  *.pyc
  renders/_preview_*.png
  scene.blend.session-backup
  .env.local
  ```
- **Acceptance**: `git check-ignore __pycache__ scene.blend.session-backup .env.local renders/_preview_A_hero.png` returns all four; no behaviour change on tracked finals.
- **Effort**: 2 minutes.

### T0.3 — Wesley PDF one-pager generation (CRITIQUE §3)

- **Defect**: `docs/wesley_brief_onepager.md` is markdown only. Wesley will sign at a notary's office; he needs a printable PDF.
- **Fix**: `pandoc docs/wesley_brief_onepager.md -o docs/wesley_brief_onepager.pdf --pdf-engine=xelatex` with a minimal page-margin preamble. If `pandoc` is not installed, use a Python `markdown` → `weasyprint` pipeline.
- **Acceptance**: `docs/wesley_brief_onepager.pdf` exists, ≤ 4 pages, embeds the hero render thumbnail.
- **Effort**: 30 minutes (most of it is layout polish).
- **Dependency**: pandoc + a TeX engine, OR weasyprint. Check `which pandoc` first.

### T0.4 — STATUS.md "Known Defects" section (CRITIQUE §4)

- **Defect**: Task #1 (petal floating on A/B/C `_petal_macro`) is a shipped defect with no public-facing flag.
- **Fix**: add a `## Known defects` section to `STATUS.md` listing the petal defect, its trigger (`scatter_lapacho_petals` mesh-Y vs ground-plane Y mismatch), its visual impact ("subtle — petals float ~3-5 cm above ground in macro frames"), and the planned remediation date.
- **Acceptance**: STATUS.md has the section; Wesley reading it knows what to expect.
- **Effort**: 15 minutes.

### T0.5 — BOM in PYG alongside USD (CRITIQUE §5)

- **Defect**: `docs/bom.md` carries USD figures only; closing meeting and Paraguayan suppliers price in PYG.
- **Fix**: add a PYG column at current exchange (≈ 7300 PYG/USD as of 2026-06; verify against `melizeche/dolarPy` or BCP daily reference); add a footer noting the FX assumption.
- **Acceptance**: every row has both currencies; an "exchange rate assumed" footer is present.
- **Effort**: 30 minutes.

### T0.6 — Wire `ten_rules_check` into `smoke_test.sh` (CRITIQUE §2)

- **Defect**: `lqv/util/ten_rules_check.py` (122 lines) exists but never runs.
- **Fix**: at the end of `scripts/smoke_test.sh`, append `RENDER_SKIP=1 blender --background --python -c "import lqv.util.ten_rules_check as t; t.audit_scene()"` and propagate the exit code.
- **Acceptance**: `bash scripts/smoke_test.sh` runs the audit and fails on rule violation.
- **Effort**: 45 minutes.

---

## Tier 1 — high-value, 1-2 weeks (parallel to escritura prep)

These unblock the long-term housing-park work and harden the codebase. None require user judgment calls.

### T1.1 — Sub-render framework build-out (CRITIQUE §2, §4)

- **Defect**: monolithic `build_scene.py` makes every iteration cost the full scene build + 256 to 512 samples. Per-asset iteration is hours.
- **Fix**: build `lqv/subscene/` per the architecture in `docs/sub_render_strategy.md`. First three drivers: `cob_walls.py`, `bottle_wall.py`, `tatakuá.py`. Each renders the single asset in isolation at 128 samples, 1280×720, with a neutral grey ground + the project HDRI.
- **Acceptance**: `python -m lqv.subscene.cob_walls` produces `renders/sub/cob_walls_A.png` in under 5 minutes on CPU.
- **Effort**: 1 day for framework + first 3 drivers; ~2 hours per additional driver.
- **Dependency**: T0.6 (audit hook) so each sub-render is rule-checked.

### T1.2 — RNG invariant test (CRITIQUE §2)

- **Defect**: the seed-ordering invariant in `build_scene.py` is documented in ARCHITECTURE.md but not enforced.
- **Fix**: add `tests/test_rng_invariants.py`. Approach: parse `build_scene.py` AST, assert that the index of `random.seed(` call is greater than the index of `materials.build_materials(` call and less than the index of the first `build_*` call. Also a smoke check that a known fixed call sequence produces a known SHA-256 of the post-seed random stream.
- **Acceptance**: `pytest tests/` runs green; deliberately reordering `build_scene.py` makes it fail.
- **Effort**: 2 hours.

### T1.3 — Split `lqv/materials.py` (CRITIQUE §2)

- **Defect**: 341 lines, single global `MAT` dict, mixed concerns.
- **Fix**: split into `lqv/materials/__init__.py` (re-exports + `MAT`), `lqv/materials/principled.py` (the factory), `lqv/materials/textures.py` (`_load_image`, `_TEX_DIR`, file resolution), `lqv/materials/procedural.py` (`add_noise_displacement`, `add_color_variegation`). Re-exports preserve every call site.
- **Acceptance**: `scripts/smoke_test.sh` byte-identical render hash before/after.
- **Effort**: 3 hours.

### T1.4 — `pyproject.toml` + `ruff` baseline (CRITIQUE §2)

- **Defect**: no static checks, no formatting policy, no dependency manifest.
- **Fix**: minimal `pyproject.toml` with `[tool.ruff]` configured for `E`, `F`, `I` (imports), `B` (bugbear), `UP` (pyupgrade), line length 100. No `mypy` yet (Blender API stubs are messy); revisit at Tier 2.
- **Acceptance**: `ruff check lqv/ scripts/ build_scene.py` runs; baseline violations fixed in the same commit.
- **Effort**: 2 hours.

### T1.5 — Doc consolidation pass (CRITIQUE §3)

- **Defect**: 4 overlapping research docs, 3-copy 10-rules drift, duplicated `AI_WHISPERERS_STYLE.md` line in CLAUDE.md, `SESSION_LOG.md` archaeology.
- **Fix**:
  - Promote `MASTER_BRIEF.md` §14 as the single source of truth for the 10 rules; have `CLAUDE.md` + `docs/research/README.md` link instead of duplicating.
  - Merge `paraguay_clay_house_research.md` + `EUROPEAN_TOURISM_SPEC.md` "Paraguay-specific" sections into a single `docs/paraguay_context.md`; cross-reference from the other two.
  - Fix the duplicated AI_WHISPERERS_STYLE.md line in CLAUDE.md.
  - Add an "archived ticks" link at the top of `SESSION_LOG.md` pointing to historical entries; cap visible tail at last 5 ticks.
- **Acceptance**: each doc has exactly one authoritative section; the rules text appears once.
- **Effort**: half a day.
- **Constraint**: per standing "additions-only, don't remove" directive, **consolidation in this tier MUST preserve every existing line** by moving + linking, not deleting. Removals deferred to Tier 2 once Wesley confirms.

### T1.6 — Per-variant lighting differentiation (CRITIQUE §4)

- **Defect**: A/B/C differ only by exposure + sun rotation. The brief asks for distinct atmospheres.
- **Fix**:
  - Variant B: add Cycles volume scatter to the master world volume (density tied to elevation, denser below y=20 m to mimic valley mist).
  - Variant C: add a separate moonlight key + cool rim ramp, distinct from the existing "low sun energy" hack.
  - Document in `lqv/lighting.py` why each variant differs.
- **Acceptance**: re-rendered hero frames show clearly different atmospheric reads.
- **Effort**: 1 day.
- **Caveat**: this regenerates renders → byte-identity breaks. **Schedule AFTER escritura** unless Wesley explicitly requests pre-escritura.

### T1.7 — Add `Makefile` for the common commands (CRITIQUE §7)

- **Defect**: `scripts/render_*.sh` are fine but discoverability is poor; the canonical entry points are not unified.
- **Fix**: `Makefile` with `make smoke`, `make preview VARIANT=A CAM=hero`, `make final VARIANT=A CAM=hero`, `make finals`, `make audit`, `make pdf`, `make sub ASSET=cob_walls`.
- **Acceptance**: `make help` lists everything; `make smoke` runs the smoke test.
- **Effort**: 1 hour.

---

## Tier 2 — medium-value, post-escritura

These improve the long-term architecture but are not on the escritura critical path.

### T2.1 — Populate or delete the 14 stub files (CRITIQUE §2)

- **Defect**: 8 typology stubs + 6 amenity stubs are dormant scaffolding.
- **Fix**: drive each through the sub-render framework (T1.1). For each stub, build the minimal procedural geometry (single box + roof + door cutout for typologies; single mesh for amenities), wire a sub-render driver, render an isolation frame. After all 14 are renderable in isolation, decide which to include in the final composite.
- **Acceptance**: each stub either has a real `build_*()` function with a sub-render output OR is deleted.
- **Effort**: ~1 week (1 hour per stub × 14, plus integration).
- **Dependency**: T1.1.

### T2.2 — Dedupe `extract_gedi_*.py` variants (CRITIQUE §1)

- **Defect**: 3 redundant scripts.
- **Fix**: pick the one that works (HTTPS variant, per `STATUS.md` 2026-06-10 mid-session note), rename to `extract_gedi.py`, delete the other two. Update `docs/site_data/README.md` if present.
- **Acceptance**: `ls scripts/extract_gedi*` returns one file.
- **Effort**: 20 minutes.

### T2.3 — Tier-1 surveyor commission (CRITIQUE §5)

- **Defect**: 62 ha, no real survey. Procedural terrain only.
- **Fix**: Wesley commissions a Paraguayan agrimensor per `docs/site_data_spike.md` §"Tier 1". AI Whisperers role: provide the SoW (AOI in WGS84, deliverables, deadline). Cost: USD 1500-3000.
- **Acceptance**: SoW exists at `docs/surveyor_sow.md`; Wesley has the contact details and budget approval.
- **Effort**: AI Whisperers produces the SoW in 2 hours; Wesley executes externally.
- **Outcome**: Tier-1 DEM at `assets/site_data/escobar_dem_5m.tif`; `lqv/site/terrain_62ha.py` activates.

### T2.4 — Populate `assets/references/` (CRITIQUE §5)

- **Defect**: no on-site reference photography in the repo.
- **Fix**: collect photos from Wesley's existing trip + add any future on-site shoots. Apply the license framework in `docs/photographic_references.md`. Add to `CREDITS.md`.
- **Acceptance**: 20+ reference photos with attribution + license columns in `docs/photographic_references.md` index table.
- **Effort**: 1 day once Wesley sends the photos.

### T2.5 — Asset checksums in `docs/external_assets.md` (CRITIQUE §7)

- **Defect**: downloaded assets are not reproducibility-verifiable.
- **Fix**: add a SHA-256 column to the `[USED]` table; populate via `find assets/ -type f -exec sha256sum {} \;`.
- **Acceptance**: every `[USED]` row has a hash; a `scripts/asset_manifest_check.py` extension verifies them on every smoke run.
- **Effort**: 2 hours.

### T2.6 — Populate `lqv/site/terrain_62ha.py` against existing DEMs (CRITIQUE §5)

- **Defect**: dormant module; the SRTM/ALOS/Copernicus DEMs were fetched but not wired into the renderer.
- **Fix**: implement `is_available()` and `build_terrain()` per the plan in `docs/site_data_spike.md` §"Render-side integration plan". Use the Tier-2 DEMs until Tier-1 (T2.3) lands.
- **Acceptance**: `RENDER_VARIANT=A RENDER_CAM=hero blender --background --python build_scene.py` with `USE_REAL_DEM=1` produces a render with the real topography.
- **Effort**: 1 day.

---

## Tier 3 — research and long-tail

Lowest priority but tracked here so they do not get forgotten.

### T3.1 — MCP socket revival
- Diagnose why the MCP socket is dead; document the failure mode in `docs/CLAUDE.md` or a new `docs/mcp_runbook.md`. Unblocks Tasks #10, #12.

### T3.2 — Micro-hydro head verification — depends on T2.3.

### T3.3 — Cob structural review — engage a structural engineer; not an AI Whisperers task.

### T3.4 — Bottle-wall thermal mass computation — hand calc + Blender thermal-mass material attribution.

### T3.5 — Tatakuá fire-clearance — add to `docs/cultural_notes.md` with a citation.

### T3.6 — Dengue prevention protocol expansion — extend Rule 3, document mesh standards + drainage angles in `docs/MASTER_BRIEF.md` §14.

### T3.7 — PV summer-shadow study — Blender sun animation + per-pad insolation export.

### T3.8 — MERCOSUR carbon-credit eligibility — desk research.

### T3.9 — 75/25 ownership contingency — legal question, defer to Wesley.

### T3.10 — Notary mensura clarification — depends on T2.3 SoW.

### T3.11 — CI on GitHub Actions — once T0.1 lands, add a `lint + smoke` workflow.

---

## Standing rules learned (folded into `CLAUDE.md`)

The critique surfaced four standing rules worth promoting to project policy:

1. **`git add -A` is banned**. Stage files explicitly by name. `scripts/mcp_daemon.py` must never appear in a commit.
2. **Doc consolidation > doc extension**. Before adding a new back-pointer or research doc, ask: can the existing doc absorb this? If yes, edit there.
3. **RNG invariant must be tested before any `build_scene.py` touch**. T1.2 is the precondition.
4. **Sub-render-first is the default workflow** for any new asset, typology, or amenity. The monolithic `build_scene.py` is only for final composite passes.

See `CLAUDE.md` ("Critique-derived standing rules") for the canonical wording.

---

## Tier mapping → STATUS.md tasks

| Tier | Tasks |
|---|---|
| 0 | #41 (push remote), #42 (gitignore), #46 (Wesley PDF), STATUS known-defects, #45-part (BOM PYG), #43 (audit wire) |
| 1 | #36-#40 (sub-render framework + sub-renders), #44 (RNG test), #45 (split materials), #32-35 are the docs themselves |
| 2 | #37+#38 (stubs population), dedupe scripts, surveyor SoW, references population, asset checksums, terrain_62ha activation |
| 3 | MCP revival, hydro verification, structural review, thermal mass, fire clearance, dengue protocol, PV shadow, carbon credit, ownership contingency, notary mensura, CI |

Numbered tasks (#32-#46) are created via TaskCreate in the same session this document lands.

---

## Cross-references

- `docs/CRITIQUE_2026-06-10.md` — the diagnosis this plan is the response to.
- `docs/sub_render_strategy.md` — the architectural shift that enables T1.1 + T2.1.
- `CLAUDE.md` — standing rules folded in.
- `STATUS.md` §4 — task ledger.
- `docs/SESSION_LOG.md` tick 21 — landing audit.
- `docs/site_data_spike.md` — T2.3 surveyor scope.
- `docs/wesley_brief_onepager.md` — T0.3 source.
- `docs/bom.md` — T0.5 target.
- `docs/external_assets.md` — T2.5 target.
- `docs/photographic_references.md` — T2.4 framework.
- `lqv/util/ten_rules_check.py` — T0.6 entry point.
- `lqv/materials.py` — T1.3 target.
- `lqv/site/terrain_62ha.py` — T2.6 target.
- `lqv/subscene/` (to be created) — T1.1 target directory.
