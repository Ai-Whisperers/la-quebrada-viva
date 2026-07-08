# PROJECT_INDEX — Riverstone Valley

Full-repo navigation. Auto-generated structural sweep (`git ls-files`, `wc -l`, `du -sh`).

This file is the cold-start map: tells a reader what the repo holds, where the load-bearing code lives, what the docs are, and what to be careful about. For Wes-facing nav, read [`WES_INDEX.md`](docs/wes/WES_INDEX.md). For escritura-day operational order, read [`docs/INDEX.md`](docs/INDEX.md). For module architecture, read [`ARCHITECTURE.md`](ARCHITECTURE.md). For build invariants, read [`CLAUDE.md`](CLAUDE.md).

## 1. What this project is

A Blender-driven photoreal model of a 62-ha parcel in Escobar/Paraguarí, Paraguay, owned 75/25 by **Wesley van de Camp** and **Thijs**. Post-escritura (signed 2026-06-27), the project is now **dual-scope**:

1. **Riverstone Valley cob house** — first example building typology on site. 18 photoreal Cycles finals (A/B/C × 6 cameras) shipped at byte-frozen commit `85e86aa`.
2. **Escobar Housing Park ("Riverstone Valley")** — Wes's expanded vision: housing park + restaurant + wellness pool + ceremonies + family-anchored community. 15 vacation-rental typologies + 4 amenities. 4-BV corporate structure. 2030 horizon (Sonja's 60th birthday).

## 2. Top-level layout

`git ls-files | wc -l` → **1861 tracked files**. Top-level layout (file counts):

| Path | Files | Purpose |
|---|--:|---|
| `LICENSES/` | 393 | 0.1 MB — Verbatim CC0-1.0 + CC-BY-4.0 legal-text mirror (offline redistribution corpus) |
| `assets/` | 10 | 1.1 MB — Tracked source assets (terrain heightmaps + NDVI; heavy .blend/.exr/.jpg are gitignored) |
| `docs/` | 1100 | 132.1 MB — The doc layer — Wes-facing briefs, research, audio synth, post-escritura canon |
| `lqv/` | 148 | 0.8 MB — Python package — Blender scene generation, materials, flora, typologies |
| `renders/` | 21 | 221.4 MB — Final PNGs (18 finals tracked; previews + sub-runs gitignored) |
| `scripts/` | 101 | 0.9 MB — Build orchestration + render entry points + tooling |
| `splats/` | 44 | 2.6 MB — Gaussian Splatting exports + tooling |
| `tests/` | 4 | 0.0 MB — pytest invariants (boq, render catalogue, RNG, typology contract) |
| `tools/` | 8 | 0.0 MB — Cross-cutting utilities (license checker, etc.) |
| `.claude/`, `.github/`, `.githooks/` | 10 | AI session config (skills, agents, hooks) + CI workflows + git hooks |

## 3. Top-level files

| File | Size | Purpose |
|---|--:|---|
| `ARCHITECTURE.md` | 9.0 KB | lqv/ package map + fragility / positional-coupling notes. |
| `CLAUDE.md` | 21.0 KB | AI session operating instructions. Document map, 10 design rules, code invariants. |
| `CREDITS.md` | 7.5 KB | Per-asset attribution lines (CC-BY 4.0 required). |
| `LICENSE` | 1.7 KB | MIT license for code. |
| `LICENSE_BUNDLE.md` | 9.4 KB | Per-license summary + bundle-readiness checklist. |
| `Makefile` | 3.1 KB | Build orchestration (boq, deck, sub, render, etc.). |
| `PROJECT_INDEX.md` | ~ | This file — full repo structural map. |
| `PROVENANCE.md` | 11.1 KB | Asset license + URL + SHA-256 manifest for all upstream data. |
| `README.md` | 5.4 KB | Cold-start entry point. Two-track nav (Wes / dev). |
| `STATUS.md` | 29.7 KB | Canonical current state (render manifest, decisions log, critical dates). |
| `build_scene.py` | 4.2 KB | 93-line entry point that wires lqv/ modules. |
| `pyproject.toml` | 2.0 KB | Python project metadata + tooling config. |
| `pyrightconfig.json` | 0.1 KB | Pyright type-checker config. |

> **Last regenerated:** 2026-07-04 (post-restructure, 1875 tracked files).

## 4. LOC summary

| Language | Files | LOC |
|---|--:|--:|
| Python (`lqv/`, `scripts/`, `tools/`) | 257 | 48,751 |
| Markdown (`docs/`) | 1100 | 67,543 |
| Shell (`scripts/*.sh`) | 17 | — |

## 5. Critical caveats

- **Renderer byte-freeze at `85e86aa`**: do not modify `lqv/` modules that affect the 18 final PNGs without an unwritten-renderer pass.
- **`MASTER_BRIEF.md` §14** is the source-of-truth for the 10 design rules (mirrored in `CLAUDE.md`).
- **The 109-idea catalog** was quality-marked in 2026-07-03. 63 ✓ reviewed files in `docs/ideas/`, 46 ○ auto-fill files in `docs/ideas/_archive/2026-06-30_autofill/`.
- **Wes-facing nav** = `docs/wes/WES_INDEX.md` (5-min read). **Post-escritura priorities** = `docs/state/POST_ESCRITURA_NOW.md` (5 hard gates). **Honest critique** = `docs/wes/CRITIQUE_FOR_WES.md`.

## 6. Where to start (cold-start reading order)

1. **`README.md`** — entry point + Wes-track vs dev-track nav
2. **`STATUS.md`** — current state (last updated 2026-07-03)
3. **`CLAUDE.md`** — operating playbook for AI sessions
4. **`ARCHITECTURE.md`** — only if you're editing `lqv/`
5. **`docs/wes/WES_INDEX.md`** — only if your stakeholder is Wes
6. **`docs/_reconciled/README.md`** — the merged Wes-files + RV view
7. **`docs/audit/BEFORE_AFTER_METRICS.md`** — only if you want repo restructure history

---

*Generated 2026-07-03 from disk state. 1861 tracked files. Top-level layout auto-derived from `git ls-files`.*
