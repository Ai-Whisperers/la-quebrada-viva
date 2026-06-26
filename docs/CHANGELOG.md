# CHANGELOG — La Quebrada Viva

Internal version log. Tracks renderer + material registry + camera helpers + delivery bundle status. **Not** a full git log — `git log --oneline` is canonical for that. This is the at-a-glance "what state are we in".

Conventions: ISO dates, present-tense bullets, file-level granularity only when a change affects external consumers (renderer determinism, sub-render protocol, bundle integrity).

---

## [Unreleased] — post-escritura sprint backlog

**Freeze status:** Renderer byte-freeze at `85e86aa` was scoped to the print-pack contents. Print-pack at `dist/print_pack_2026-06-27/` is SHA-pinned independently on disk, so the post-`85e86aa` polish work cannot retroactively change shipped bytes. Material-registry work is OPEN since 2026-06-15 (commit `78433a7`, Ivan-authorized escritura beauty sprint). `build_scene.py` composite path remains untouched pending escritura close (2026-06-27).

Planned (P1.A residue + P1.B):
- ~~`lqv/typologies/*` — Rule 4 stone-foundation plinth pass~~ — audit 2026-06-26 confirmed all 18 typologies satisfy Rule 4 in code (explicit foundation builders in 11; villa footings/pier blocks/PIER_LIFT/explicit sandstone course in 4; 3 exempt — boomhut treehouse, outdoor shower, candle_path). Pre-78433a7 "~13 missing" figure was stale.
- HDRI swap to cerrado / Atlantic-Forest-edge — asset-researcher pass, CC0 / CC-BY 4.0 (P1.A.5)
- `apply_xray_override` material swap (HOUSE_IMAGERY_SHOTLIST §3)
- Per-variant lighting differentiation T1.6 + background-tree replacement (P1.C)

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
| Sub-render protocol (`lqv/subscene/`) | v1 | 2026-06-14 | `RENDER_RUN_ID` + runs/latest mirror; `RENDER_VIEW` planned post-freeze |
| Camera helpers | v1 | 2026-06-26 | `cameras.make_view_camera(cfg, ...)` public dispatcher; `RENDER_VIEW={hero3q,elevation,plan,section,interior}`; 22 bypass-pattern drivers migrated |
| BoQ scope filter | v1 | 2026-06-15 | `LQV_BOQ_SCOPE=escritura` ($268,685.45) vs `=full` ($288,056) |
| Wesley bundle | `20260616-1715` | 2026-06-16 | SHA-pinned, do not rebuild pre-escritura |
| Escritura deck | v6 | 2026-06-16 | 28pp, SHA-pinned in print-pack |
