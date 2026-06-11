# License Bundle — La Quebrada Viva

> Per-license summary of every third-party asset that ships in this repository's renders. Companion to `CREDITS.md` (which lists per-asset attribution); this file is the answer to "if I redistribute the `assets/` directory or a render bundle, what propagates?".
>
> Authoritative pointers: `CREDITS.md` for attribution lines, `docs/external_assets.md` for the planning catalog, `docs/master_plan.md` §5 for the licensing strategy.

Last updated: 2026-06-10.

---

## 1. Tiered summary

| License | Attribution required | Share-alike propagates | Commercial use | Count (in-scene) | Count (planned) |
|---|---|---|---|---|---|
| **CC0 1.0** (Poly Haven HDRIs + textures) | No (listed for traceability) | No | Yes | 3 HDRIs + 17 PBR sets | — |
| **CC0 1.0** (Sketchfab) | No (listed for traceability) | No | Yes | 0 | 1 (plant pot) |
| **CC-BY 4.0** (Sketchfab + Hyper3D-derived) | Yes — author + title + UID + license URL in `CREDITS.md` | No | Yes | 11 (Phases 1–5) | 5 (Phase 8 props) |
| **CC-BY-SA 4.0** | Yes + derivative bundle must also be CC-BY-SA | **YES — contaminating** | Yes | 0 | 0 (intentionally excluded) |
| **Hyper3D / Hunyuan3D generated** | Per generator ToS (record per asset) | Per generator ToS | Per generator ToS | 0 | 2 (lapacho_A, lapacho_B) |

---

## 2. What "redistribute" means here

The repo currently tracks three categories of output:

- `renders/*.png` — final raster output. Derivatives of every asset in the scene at render time. Distributing these requires honouring every asset's terms (attribution for CC-BY; share-alike would apply if any CC-BY-SA asset were used, but **none are**).
- `assets/sketchfab/<uid>/`, `assets/hdris/`, `assets/textures/` — raw third-party files. Distributing these is a direct redistribution of the original asset; original license terms apply unchanged.
- `lqv/`, `build_scene.py`, `scripts/` — our own code. MIT-licensed by default (declare at repo root if not already). No third-party-license entanglement.

If only `renders/` is published and the `assets/` directory is kept private, attribution is still required for every CC-BY asset that contributed to the render, because the rendered PNG is a derivative.

---

## 3. Hard exclusions — assets we intentionally do NOT use

| Asset | UID | License | Reason for exclusion |
|---|---|---|---|
| Hammock (paraguayan, 1-3D.com) | `b5b2e42309144dafaf2efe9b71a491c8` | CC-BY-SA 4.0 | Share-alike would force the entire bundle (and all derivative renders) to CC-BY-SA. Replaced with Andrey3Ds CC-BY hammock UID `c5fd4cef873f44f5a31db1fc6a04c572`. |

Any future CC-BY-SA candidate must be approved by the user before import. The default is exclude.

---

## 4. Reproducibility notes

- **Poly Haven** assets are pulled by slug from `polyhaven.com`. Slugs in `CREDITS.md` map to the canonical URL `https://polyhaven.com/a/<slug>` for HDRIs/models and `https://polyhaven.com/a/<slug>` for textures.
- **Sketchfab** assets are pulled by UID. Canonical URL: `https://sketchfab.com/3d-models/<slug>-<uid>` (slug optional). UIDs in `CREDITS.md` are stable identifiers — they outlive author renames.
- **Hyper3D / Hunyuan3D** assets are generated from text prompts archived in `docs/asset_plan.md` §C.4 (when that section lands). Each generated asset records its prompt + generator + seed in `CREDITS.md` so the output is reproducible.

---

## 5. Per-asset license map

For per-asset attribution lines see `CREDITS.md`. The current in-scene composition (12 Variant A + B finals already shipped) draws on:

- 3 Poly Haven HDRIs (CC0)
- 17 Poly Haven PBR texture sets (CC0)
- 11 Sketchfab models under CC-BY 4.0 (Phases 1–5; all attributed in `CREDITS.md`)

The Phase 7 (Variant C) additions are fully procedural (window glow emission planes, firefly UV-spheres, qwantani_dusk_2 HDRI already counted above) — zero new third-party assets.

Phase 8+ additions (per shortlist in `docs/external_assets.md`):

- 5 Sketchfab models under CC-BY 4.0 (hammock, mate diorama, chicken coop, firewood, bonfire)
- 1 Sketchfab model under CC0 (plant pot)
- 2 Hyper3D-generated lapacho meshes (license recorded at generation time)

---

## 6. Bundle-readiness checklist

Before tagging `v1.0-bundle`:

- [ ] Every asset in `assets/` has a matching line in `CREDITS.md`.
- [ ] No `[PLANNED]` entry survives in `CREDITS.md` — either delivered as `[USED]` or removed.
- [ ] No CC-BY-SA asset appears in `assets/` or in any render's contribution list.
- [ ] Each Hyper3D-generated asset has its prompt + seed + generator recorded.
- [ ] `STATUS.md` manifest shows 18/18 finals ☑.
- [ ] This file (`LICENSE_BUNDLE.md`) updated to flip counts from the "planned" column to the "in-scene" column.
- [ ] Repo root has an explicit code license (MIT or chosen alternative).

---

## 7. License texts — upstream pointers

We do not inline the full legalcode for every license referenced (would add ~5000 lines and rot when CC issues errata). Instead, the upstream canonical URLs below are authoritative. The `LICENSES/` sibling directory at repo root mirrors the Creative Commons texts so the redistribution bundle is offline-complete.

| License | Canonical URL | Mirror path | Mirror status |
|---|---|---|---|
| CC0 1.0 Universal — Public Domain Dedication | <https://creativecommons.org/publicdomain/zero/1.0/legalcode> | `LICENSES/CC0-1.0.txt` | ☑ landed 2026-06-10 (121 lines, verbatim from `legalcode.txt`) |
| CC-BY 4.0 — Attribution International | <https://creativecommons.org/licenses/by/4.0/legalcode> | `LICENSES/CC-BY-4.0.txt` | ☑ landed 2026-06-10 (396 lines, verbatim from `legalcode.txt`) |
| Poly Haven distribution terms (CC0 wrapper) | <https://polyhaven.com/license> | `LICENSES/PolyHaven-terms.txt` | ☐ NOT mirrored — vendor terms change; URL is authoritative |
| Sketchfab Standard Terms (governs all UID downloads regardless of CC license) | <https://sketchfab.com/tos> | `LICENSES/Sketchfab-tos.txt` | ☐ NOT mirrored — vendor ToS, URL is authoritative |
| Hyper3D Rodin generator output terms | <https://hyper3d.ai/terms> | `LICENSES/Hyper3D-terms.txt` | ☐ NOT mirrored — verify at generation time |

The two CC licenses (CC0, CC-BY 4.0) cover every asset in `assets/` today; vendor-terms files are intentionally URL-only because they evolve faster than a repo mirror would track. If a future bundle needs frozen vendor-terms snapshots, fetch at tag time and stamp the fetched date inside the file header.

---

## 8. Cross-references

- `CREDITS.md` (repo root) — per-asset attribution lines; each Sketchfab/Hyper3D entry here has a matching row there.
- `docs/license_obligations.md` — narrative explanation of how each license obligation is satisfied at render-distribution time + at repo-distribution time.
- `docs/photographic_references.md` — separate license framework for **reference photography** in `assets/references/` (not embedded in renders, but subject to its own attribution rules).
- `docs/external_assets.md` — download log and current `[USED]` / `[PLANNED]` state per asset.
- `docs/asset_plan.md` §§5, C.4 — licensing strategy + Hyper3D prompt archive.
- `docs/wesley_deliverable_bundle.md` — Tier 2 USB/cloud bundle includes both `CREDITS.md` and this file.
- `LICENSES/README.md` — verbatim CC0-1.0 + CC-BY-4.0 legal-code mirror + vendor-terms pointer table; the row "☐ NOT mirrored — verify at generation time" for Sketchfab/Hyper3D vendor terms in §7 above points readers to that file's URL-only policy rationale. Added 2026-06-10 to close the back-pointer asymmetry.
- `STATUS.md` — render manifest; the §6 readiness gates ("☐ NOT mirrored", "☐ ZIP creation script", etc.) above flip to ☑ only when a `STATUS.md` manifest cell flips to ☑ on the same bundle release. STATUS.md is the trigger; this file is the checklist.
- `ARCHITECTURE.md` §"Variant C additions (2026-06-10)" — the procedural-recipe additions for Variant C (`lqv/lighting.py` Variant C branch, `lqv/house/cob.py:build_window_emission`, `lqv/flora/fireflies.py`) add ZERO new third-party-asset rows to this file's §§3-5 tables; ARCHITECTURE.md's §"Variant C additions" block is the reciprocal source-of-truth for that "zero new license exposure" claim.
- `docs/SESSION_LOG.md` — narrative log of the 2026-06-10 mega-session including license posture decisions (CC-BY-SA exclusion in §3, Hyper3D vendor-terms URL-only policy in §7); each per-license decision recorded above maps to a tick in SESSION_LOG.
- `CLAUDE.md` §"Things to refuse / push back on" + §"Document map" — CLAUDE.md names this file as one of the three documents (CREDITS.md, this file, LICENSES/README.md) that together satisfy the bundle's CC-BY 4.0 attribution requirement at distribution time. The two files are contract: CLAUDE.md says *why* the bundle pattern exists; this file says *how* §6 readiness gates implement it.
