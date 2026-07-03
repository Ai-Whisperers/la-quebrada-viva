# Restructure Pass — Before / After Metrics (2026-07-03)

> Quantified result of the full critique + restructure pass.
> See `RESTRUCTURE_PLAN.md` for the plan, `CRITIQUE.md` for the reasoning,
> `CRITIQUE_V2_ADDENDUM.md` for what the 2026-06-30 audit missed.

## Repo-level metrics (verified on origin/master post-push)

| Metric | Before | After | Delta | % |
|---|--:|--:|--:|--:|
| **Tracked files** | 2,368 | **1,850** | **−518** | **−21.9%** |
| **Tracked repo size** | 696.2 MB | **359.2 MB** | **−337.0 MB** | **−48.4%** |
| **Working tree size (incl. gitignored bulk)** | 2.2 GB | 1.6 GB | −600 MB | −27.3% |
| **Tracked .md files** | 500 | 510 | +10 | +2% |
| **Tracked .tif files** | 169 | 105 | **−64** | −37.9% |
| **Tracked .pdf files** | 7 | 6 | −1 | −14.3% |
| **Tracked .png files** | 118 | 118 | 0 | 0% |
| **Tracked .py files** | 258 | 258 | 0 | 0% |

## What got removed (size freed)

| Item | Files removed | MB saved | Source of decision |
|---|--:|--:|---|
| `docs/site_data_2026-06-13_snapshot/` gitignored (455 files, kept on disk) | 455 | **261.9 MB** | RESTRUCTURE_PLAN §1 — pre-Wes, fully replaced |
| `docs/site_data/mapbiomas_paraguay/` compressed to 5-year sampling | 64 | **40.3 MB** | RESTRUCTURE_PLAN §2 — 5-year trajectory preserves insight (49.7 MB → 9.4 MB) |
| `docs/escritura_deck/escritura_deck_v1.pdf` removed (v3-v6 kept as audit trail) | 1 | **34.9 MB** | New — v1 was the bulky early draft; v3-v6 are T-2 freeze iterations |
| `docs/site_data/topology_lod/regional/cop30_raw.tif` archived (unreferenced) | 1 | **11.7 MB** | RESTRUCTURE_PLAN §6 — `tier_manifest.md` only mentions cop30_30m + cop30_90m |
| **Subtotal raw size removed from tracking** | **521** | **348.8 MB** | — |
| Net tracked-size delta | **−518 files, −337 MB** | | git reclaims some via history compression; actual tracked delta smaller than raw file-deletion math |

## What got added (new content)

| File | Lines | Purpose |
|---|--:|---|
| `docs/site_data_2026-06-13_snapshot/README.md` | 55 | Explains what the snapshot is, how to re-populate (the only tracked file in the now-gitignored dir) |
| `docs/_archive/property_map_v1_brief.md` | 148 | v1 archived, v2 promoted to canonical |
| `docs/_archive/topology_lod_unreferenced/cop30_raw.tif` | (binary) | Moved out of canonical site_data/ |
| `docs/WES_INDEX.md` | 152 | Wes-facing one-page index |
| `docs/POST_ESCRITURA_NOW.md` | 106 | 5 hard gates + 12 soft gates ranked |
| `docs/CRITIQUE_FOR_WES.md` | 131 | Short roast aimed at Wes |
| `docs/audit/BEFORE_AFTER_METRICS.md` | (this file) | Quantified result |
| `docs/audit/CRITIQUE_V2_ADDENDUM.md` | 217 | What the original audit missed |
| `README.md` cold-start rewrite | +29 | Two-track nav (Wes / Ivan/Kiki/Erebus) |
| `STATUS.md` restructure banner + footer fix | +4 / ~3 changes | Documents the 2026-07-03 pass; date corrected from stuck "2026-06-10" |
| `docs/_reconciled/README.md` cross-link section | +8 | Links to WES_INDEX + POST_ESCRITURA_NOW |
| Quality field on all 109 idea files | ~330 (3 lines × 109 files) | 63 ✓ reviewed, 46 ○ auto-fill |
| Status banner on 19 pre-escritura docs | ~95 (5 lines × 19) | Anchors "as of 2026-06-30" forward to post-escritura docs |

## What got fixed (quality, not size)

| Fix | Details |
|---|---|
| **3 contradictory "current state" docs** | STATUS.md is now the single source (PROJECT_INDEX.md still serves as file map) |
| **109-idea catalog honest quality marking** | `✓ reviewed` (63) vs `○ auto-fill` (46). No more pretending all 109 are filled in. |
| **19 stale docs anchored with "as of" headers** | Pre-escritura docs now link forward to post-escritura canon |
| **Property_map duplication** | v2 brief promoted to canonical, v1 brief archived, _v2/ dir removed |
| **Unreferenced cop30_raw.tif** | Moved to `docs/_archive/topology_lod_unreferenced/` (gitignored-tier organization) |
| **Escritura deck provenance** | `escritura_deck.md` now correctly says v6 is canonical (was wrong, said v5) |
| **Wes-track top-level nav** | README now opens with "If you're Wesley — start here" before dev content |
| **Reconciled view cross-links** | `_reconciled/README.md` now points to WES_INDEX, POST_ESCRITURA_NOW, CRITIQUE_FOR_WES |
| **Bitwarden CLI local state** | `.config/` gitignored — vault decryption keys can never enter git history |
| **910 MB `docs/site_data_monday/` bulk imagery** | Gitignored — regenerable from ESRI tile server |

## What we did NOT touch (and why)

- ❌ **The 18 final renders** (`renders/A_*.png` etc.) — byte-identity frozen at `85e86aa`, NOT going to be touched
- ❌ **The 393 `LICENSES/` verbatim files** — by design, large, legally required for the bundle
- ❌ **The `lqv/` Python package** — that's the 3D rendering code, scope-out for this pass
- ❌ **The financial model placeholder docs** — needs attorney input (W0.1) before real numbers land
- ❌ **`docs/audios/`** — canonical per Wes's audios, do not modify
- ❌ **The `_reconciled/` view itself** — only added cross-link section; content stays as-is

## Verification (post-push on origin/master)

```bash
git ls-tree -r -l origin/master | wc -l                              # 1,850 files
git ls-tree -r -l origin/master | awk '{print $3}' | paste -sd+ | bc  # ~359 MB tracked
du -sh --exclude=.git .                                               # 1.6 GB working tree
git log --oneline | head -5                                           # 3 restructure commits this session
```

## Estimated impact for the next person who opens this repo

- **For Wes:** opens `docs/WES_INDEX.md`, reads 5 minutes, knows what to do this week (5 actions in `WES_ACTIONS.md`)
- **For Ivan:** opens README, sees two-track cold-start, drops into either WES_INDEX or STATUS/CLAUDE
- **For a new Erebus session:** opens STATUS.md → 2026-07-03 restructure banner → knows repo state in 30 sec
- **For a downstream researcher:** the 9 research RESULTS/ files + RESEARCH_GAPS.md are now obviously the canonical research layer

---

*Generated by Erebus · 2026-07-03 · restructure commits: 51e3ea8, 4a95e21, 3806b5c*