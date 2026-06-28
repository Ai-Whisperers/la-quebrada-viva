# LICENSES/ — verbatim license texts for offline bundle

Mirrored Creative Commons legal code for every license used by assets in this
repository. Required so the redistribution bundle is offline-complete and so
auditors can verify CC text against the canonical source without a network
fetch.

| File | Covers | Source | Mirrored |
|---|---|---|---|
| `CC0-1.0.txt` | Poly Haven HDRIs + PBR textures; one Sketchfab CC0 prop (plaggy plant pot, planned) | <https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt> | verbatim |
| `CC-BY-4.0.txt` | All Sketchfab CC-BY models (Phases 1–5 already in-scene; Phase 8 props planned) + Hyper3D-derived assets that attach a CC-BY notice | <https://creativecommons.org/licenses/by/4.0/legalcode.txt> | verbatim |

Vendor-specific terms (Poly Haven distribution policy, Sketchfab Standard
Terms, Hyper3D Rodin generator output policy) are **intentionally not
mirrored** here — those terms evolve faster than a repo mirror would track.
The canonical URLs are authoritative; see `LICENSE_BUNDLE.md` §7 for the
full pointer table.

If a future bundle freeze needs snapshotted vendor terms, fetch at tag time
and stamp the fetched date inside each file header so readers know what
revision of the terms applied at bundle creation.

## Cross-references

- `../LICENSE_BUNDLE.md` — per-license summary, bundle-readiness checklist, §7 mirror-status table.
- `../CREDITS.md` — per-asset attribution lines.
- `../docs/license_obligations.md` — narrative explanation of obligations at publication time.
- `../LICENSE` — MIT license for the code at repo root (`lqv/`, `build_scene.py`, `scripts/`, `docs/`). Does NOT cover `assets/` or `renders/`.

### Extended back-pointers (additive 2026-06-10)

Closing the asymmetry: many docs reference this directory forward (LICENSE_BUNDLE §7 mirror-status table, CREDITS §Sketchfab + §Hyper3D headers, asset_plan §G, wesley_deliverable_bundle Tier-2) but the reverse pointers were never collected here. Listed below with *why* each back-link matters; the four core pointers above are unchanged.

- `../STATUS.md` §1 — render manifest is the trigger. The CC0-1.0.txt + CC-BY-4.0.txt mirror files landed on 2026-06-10 as a precondition for the 18/18 ☑ flip and the subsequent v1.0-bundle tag; when STATUS.md §1 flips to 18/18 ☑, LICENSE_BUNDLE.md §6 readiness gates flip, and **the verbatim mirrors in this directory** are what those gates actually check against. STATUS.md is the trigger; LICENSE_BUNDLE is the checklist; this directory is the deliverable.
- `../docs/SESSION_LOG.md` — narrative log of the 2026-06-10 mega-session including the exact tick where `CC0-1.0.txt` (121 lines) and `CC-BY-4.0.txt` (396 lines) were captured verbatim from the canonical CC `legalcode.txt` URLs. SESSION_LOG is the audit trail proving the mirrors were not editorialised; this README is the receipt for the audit.
- `../ARCHITECTURE.md` §"Variant C additions (2026-06-10)" — the procedural Variant C additions (`lqv/lighting.py` Variant C branch, `lqv/house/cob.py:build_window_emission`, `lqv/flora/fireflies.py`) add ZERO new third-party-asset rows, therefore ZERO new license-text additions are needed here. ARCHITECTURE.md's Variant C block is the reciprocal source-of-truth for that "no new license texts needed for Variant C" claim.
- `../CLAUDE.md` §"Document map" + §"Things to refuse / push back on" — CLAUDE.md names this directory as one of the three documents (CREDITS.md, LICENSE_BUNDLE.md, **this directory's README + mirrored legal-code files**) that together satisfy CC-BY 4.0 attribution at distribution time. Without the verbatim legal-code mirrors, the Tier-2 USB bundle cannot satisfy CC-BY §6.a redistribution obligations offline.
- `../docs/asset_plan.md` §G — the Phase 1-8 import plan; every CC-BY 4.0 asset row in §B/§C eventually requires `CC-BY-4.0.txt` to ship in the redistribution bundle. asset_plan §G is the forward plan, this directory is the downstream artefact.
- `../docs/external_assets.md` §Cross-references — the download log + `[USED]`/`[PLANNED]` ledger. Every `[USED]` row that points at CC0 or CC-BY 4.0 license terms expects this directory's verbatim mirrors to cover its redistribution obligation. external_assets.md is the per-asset register; this directory is the legal-text backing-store.
- `../docs/wesley_deliverable_bundle.md` §Tier 2 — the USB / cloud bundle includes `CREDITS.md`, `LICENSE_BUNDLE.md`, **and the contents of this `LICENSES/` directory** as the offline-complete legal corpus. wesley_deliverable_bundle.md is the packaging spec; this directory is the payload.
- `../docs/photographic_references.md` — separate license framework for **reference photography** in `assets/references/` (photographs are NOT embedded in renders but are subject to their own per-photo attribution). photographic_references.md is the parallel framework; this directory mirrors only the asset-license texts, not the reference-photo terms.
