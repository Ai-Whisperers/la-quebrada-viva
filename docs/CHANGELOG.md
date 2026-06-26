# CHANGELOG — La Quebrada Viva

Internal version log. Tracks renderer + material registry + camera helpers + delivery bundle status. **Not** a full git log — `git log --oneline` is canonical for that. This is the at-a-glance "what state are we in".

Conventions: ISO dates, present-tense bullets, file-level granularity only when a change affects external consumers (renderer determinism, sub-render protocol, bundle integrity).

---

## [Unreleased] — post-escritura sprint backlog

**Freeze status:** RENDERER BYTE-FROZEN until escritura signs 2026-06-27. No `build_scene.py`, material-registry, or shader-graph edits land in this window. Carry-forward queue in `docs/DEFERRED_BUGS.md` + `docs/MASTER_TODO.md` P1.A/P1.B/P1.C.

Planned (gated on freeze lift):
- `materials/water` — fix `pool_water` + `river_water` to dielectric BSDF (DEFERRED_BUGS Bug 1)
- `materials/lapacho_timber` — wire albedo/roughness/normal trio + plank-seam Voronoi (DEFERRED_BUGS Bug 2)
- `lqv/flora/photoreal.py:_append_object_from_blend` — idempotent LOD load (DEFERRED_BUGS Bug 3)
- `lqv/subscene/_cameras.py` — new `subscene_ortho_elevation/plan/section_camera/interior_camera` helpers (HOUSE_IMAGERY_SHOTLIST P1.B)
- `RENDER_VIEW` env var parallel to `RENDER_VARIANT` (HOUSE_IMAGERY_SHOTLIST §2)
- `apply_xray_override` material swap (HOUSE_IMAGERY_SHOTLIST §3)

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
| `build_scene.py` | frozen | 2026-06-10 (`85e86aa`) | byte-identity required through 2026-06-27 |
| Material registry (`lqv/materials.py`) | frozen | 2026-06-10 | three open shader bugs deferred (DEFERRED_BUGS) |
| Sub-render protocol (`lqv/subscene/`) | v1 | 2026-06-14 | `RENDER_RUN_ID` + runs/latest mirror; `RENDER_VIEW` planned post-freeze |
| Camera helpers | v0 | n/a | elevation/plan/section/interior helpers spec-only (HOUSE_IMAGERY_SHOTLIST) |
| BoQ scope filter | v1 | 2026-06-15 | `LQV_BOQ_SCOPE=escritura` ($268,685.45) vs `=full` ($288,056) |
| Wesley bundle | `20260616-1715` | 2026-06-16 | SHA-pinned, do not rebuild pre-escritura |
| Escritura deck | v6 | 2026-06-16 | 28pp, SHA-pinned in print-pack |
