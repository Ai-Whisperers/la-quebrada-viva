# AUTONOMOUS_PLAN — post-78433a7 → escritura-close sprint

Ultrawork checkpoint, T-1 (2026-06-26). Escritura signs 2026-06-27 at Escribanía Peña.

Authorized scope: full MASTER_TODO backlog after `78433a7` polish wave shipped Bugs 1/2/3. Renderer byte-freeze at `85e86aa` is superseded for forward code work (print-pack `dist/print_pack_2026-06-27/` is SHA-pinned on disk and cannot be retroactively altered). `build_scene.py` composite path still untouched until escritura tag promotes.

## Goal

Land the post-polish backlog so that the morning after escritura signs we ship:
1. **P1.A.4** — Rule 4 stone-foundation plinth on every typology that lacks it.
2. **P1.A.5** — HDRI swap to cerrado / Atlantic-Forest-edge (CC0 / CC-BY 4.0 only).
3. **P1.B.1/2/3** — furniture stubs, `RENDER_VIEW` env + camera helpers, `apply_xray_override`.
4. **P1.C.1** — per-variant lighting differentiation (T1.6) + background-tree replacement.
5. **Cross-cutting** — CC-TOOL.1 (MCP retire/diag), CC-TOOL.5 (pyright), CC-DOC.1 (README), CC-DOC.9 (sub-render-first rule into in-repo CLAUDE.md).
6. **P0b.2 (deferred)** — promote annotated tag `escritura-2026-06-27-signed` AFTER actual signing event; write `project_state_2026_06_27_signed.md` + index pointer.

## Items (priority order)

| # | Item | Surface | Effort | Status |
|---|---|---|---|---|
| 1 | This plan + commit | `docs/AUTONOMOUS_PLAN.md` | 10 min | in_progress |
| 2 | P1.A.4 — plinth audit + helper + per-typology pass | `lqv/typologies/_plinth.py` + 13 builders | ~1.5d | pending |
| 3 | P1.A.5 — HDRI discovery (delegate to `asset-researcher`) + wire-up | `assets/hdris/` + `lqv/site/lighting.py` | 0.5d + 0.5d | pending |
| 4 | P1.B.2 — `RENDER_VIEW` env var + camera helpers | `lqv/cameras.py`, `lqv/subscene/base.py` | 4h | pending |
| 5 | P1.B.3 — `apply_xray_override` Transparent BSDF swap | `lqv/subscene/base.py` | 2h | pending |
| 6 | P1.B.1 — furniture stubs (bed/table/bench/stove/cistern) | `lqv/furniture/_stubs.py` + 16 typologies | 6h | pending |
| 7 | P1.C.1 — per-variant lighting + background-tree replacement | `lqv/site/lighting.py`, `lqv/site/canopy.py` | 1d | pending |
| 8 | CC-TOOL.1 — MCP socket diagnostic / retire | `scripts/mcp_daemon.py`, `docs/MCP_STATUS.md` | 1h | pending |
| 9 | CC-TOOL.5 — pyright pass | `pyproject.toml` + fixes | 2h | pending |
| 10 | CC-DOC.1 — README refresh | `README.md` | 1h | pending |
| 11 | CC-DOC.9 — promote sub-render-first into CLAUDE.md | `CLAUDE.md` | 30m | pending |
| 12 | P0b.2 — tag `escritura-2026-06-27-signed` after signing event | git | 10m | deferred |

Lower-priority continuation queue (P2/P3/P4 + CC-TOOL.2-4/6-9, CC-DOC.2-8, CC-SALES.1-6, CC-BUILD.1-8) is tracked in `docs/MASTER_TODO.md`; this plan only commits to the items above.

## Acceptance criteria

- **P1.A.4 done** when smoke-render of three spot-checked typologies (`bamboo_river_house`, `italian_river_house_4pax`, `eco_retreat_modern_oasis`) shows a visible 60 cm stone foundation between earthen wall and ground in variant A preview. No regression in pytest invariants (RNG seed ordering, MAT registry call-time lookup).
- **P1.A.5 done** when `assets/hdris/lqv_canopy_edge.exr` (or similar) is wired into the lighting registry and HDRI license file lands in `LICENSES/`. Three test renders at variants A/B/C show the new sky without firefly explosion.
- **P1.B.2 done** when `RENDER_VIEW=elevation|plan|section|interior PYTHONPATH=. blender -b -P lqv/subscene/<asset>.py` produces a sensible render for each view on at least one asset.
- **P1.B.3 done** when `apply_xray_override(except_materials=['lapacho_timber','adobe_render'])` swaps everything else to Transparent BSDF in a section view, exposes interior framing.
- **P1.B.1 done** when 16 typologies each have at least bed + table + cistern primitives placed via shared stubs.
- **P1.C.1 done** when variant A reads as golden hour + lapacho pink bloom, B as overcast neutral, C as blue hour + fireflies on a spot-checked subscene.
- **CC-TOOL.1 done** when `docs/MCP_STATUS.md` documents the socket-dead diagnosis and the retire-or-resurrect decision is recorded.
- **CC-TOOL.5 done** when pyright runs clean (or with a documented allowlist) on `lqv/`, `tools/`, `scripts/`.
- **CC-DOC.1 done** when README reflects current 18/18 finals + post-78433a7 state.
- **CC-DOC.9 done** when in-repo `CLAUDE.md` has explicit "sub-render-first" standing rule.
- **Pytest 16/16 invariants stay green throughout.** No commit lands while red.

## Stop conditions

- All items above complete → final report, stop.
- Item touches `dist/print_pack_2026-06-27/*` bytes → STOP and surface (print-pack is SHA-pinned).
- Item would force-push, delete branches/tags, rotate credentials, send external messages → STOP and ask.
- Same error repeats 3× across attempted fixes → document in `docs/BLOCKERS.md`, skip to next unblocked item.
- Pytest invariants go red → revert the offending commit, document, skip.
- Render parallelism breach (>1 Blender process concurrent) → kill and serialize.

## Operational notes

- Explicit-path staging only. Never `git add -A` or `git add .`.
- Always exclude: `scripts/mcp_daemon.py`, `docs/site_data/sentinel2/*.tif`, `docs/*_boleto_*.pdf`, `docs/*_escritura_*.pdf`, `docs/2026-*_*.pdf`.
- Never touch: `lqv/scatter_lapacho_petals`, `build_scene.py` composite path, `_archive/`, `wesley_bundle_20260616-1715.*`, `MONDAY_DELIVERABLE` sentinel, `render_terrain_62ha_v3/v4/v5/v5_arrowfix.sh` chain.
- Sub-renders serialize (one Blender at a time). RSS ceiling ~4.3 GB/process on 14 GB host.
- All sub-render output under `renders/sub/runs/<RENDER_RUN_ID>_<asset>[_<tag>]/<variant>.png` + `latest/` + flat back-compat path.
- Checkpoint commit every ~5 completed items. Self-critique every ~30 min wall time.
- Final report at end per ultrawork stop conditions.
