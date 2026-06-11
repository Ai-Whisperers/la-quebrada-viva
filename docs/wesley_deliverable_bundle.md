# Wesley Deliverable Bundle — 2026-06-27 Escritura Package

**Status:** living document. Defines exactly what Wesley van de Camp walks into the escritura traslativa meeting with on 2026-06-27. This is the master shipping manifest for the AI Whisperers engagement Phase 1.

## Why this bundle matters

The escritura is the final ownership transfer of the 62-ha property in Escobar, Paraguarí, from the current owners to Wesley (75%) + Thijs (25%). At that meeting:

- The notary verifies parcel ID, area, encumbrances, and seller authority.
- The buyer presents their intended use (helpful, not mandatory).
- Funds clear.
- The escritura is signed and presented to the registro de inmuebles for inscription.

Wesley benefits from showing up with a **vision document** so the notary and any seller-side advisor see that this is a long-term productive plan, not speculation. That tone matters in small-town Paraguay legal culture.

## Deliverables

### Tier 1 — physical bundle Wesley brings to the meeting

A single labeled folder ("La Quebrada Viva — Wesley van de Camp — 27/06/2026") containing:

1. **One-pager brief** (`docs/wesley_brief_onepager.md` exported to A4 PDF, color, single sheet).
2. **18-render contact sheet** (A3 landscape, all 18 hero shots at thumbnail size + key callouts).
3. **5 large prints** of selected finals: A_dusk, B_terrace, C_hero, B_stream_up, A_petal_macro at A3 color.
4. **Floor plan + section view** (A2 print of each, from `docs/floor_plan.md` and `docs/section_view.md` rendered as drawings).
5. **Site plan** (A2 print of the 62 ha with 8 typology pads marked, from `lqv/site/site_plan.py` + topo overlay).
6. **5-year phasing chart** (A4, condensed from `docs/housing_park_phasing.md`).
7. **Construction cost estimate summary** (A4, top-line from `docs/bom.md`, total USD 56k for the LQV house).
8. **Energy + water systems schematic** (A4 diagram from `docs/energy_budget.md`).
9. **Day-by-day closing checklist** (A4 print of [`docs/CLOSING_DAY_PREP.md`](./CLOSING_DAY_PREP.md) — T-7 / T-5 / T-2 / signing-day / T+30 sequence + risk register; for Wesley's own use, not handed to notary).

Print quality: 300 dpi minimum. Color profile: Adobe RGB → print profile of the chosen Asunción print shop (verify ICC).

### Tier 2 — digital bundle (USB key + cloud link)

A USB drive (and a parallel Google Drive link) containing:

1. **All 18 final renders** at native 2560×1440 (hero) and 1920×1080 (others), PNG + JPEG copies.
2. **`docs/master_plan.md` + housing-park concept + tourism spec** (PDFs).
3. **`docs/floor_plan.md` + `docs/build_sequence.md` + `docs/bom.md`** (PDFs).
4. **`docs/energy_budget.md` + `docs/license_obligations.md`** (PDFs).
5. **`docs/cultural_notes.md`** (PDF) — to back the cultural authenticity claim.
6. **Source `.blend`** files for the 18 renders (zipped).
7. **`lqv/*` Python package** as a zipped reference.
8. **`CREDITS.md` + `LICENSE_BUNDLE.md`** (both at repo root).

### Tier 3 — escritura-specific paperwork (Wesley provides — NOT us)

- Boleto privado de compraventa, signed.
- Boleto pago + comprobantes de pago.
- Wesley's cédula + Thijs's pasaporte (or apoderado document).
- Sellers' titles, RUC, cédula.
- Mensura by the colegiado surveyor.
- Certificado de no gravamen del inmueble (registro de inmuebles).

We do NOT touch these. They are between Wesley, the notary, and the seller.

## Presentation logic for the meeting (1-page narrative we hand the notary)

The brief opens with:

> "Mi señor escribano, esta propiedad va a ser desarrollada como un parque residencial de bajo impacto, con la primera vivienda de barro y vidrio reciclado ya diseñada y aprobada en anteproyecto. Adjuntamos el plano, la sección, el plan de construcción y la estimación de costos para su archivo."

Then the bundle is laid out in the order: vision (renders) → plan (drawings) → schedule (phasing) → numbers (BOM) → systems (energy) → cultural backing (notes).

The notary doesn't have to engage with all of it; the **presence** of the bundle changes the meeting's tone.

## Production pipeline (what AI Whisperers does, 2026-06-09 → 2026-06-25)

| Date | Output |
|---|---|
| 2026-06-09 | A and B render batches shipped (12 of 18 done). |
| 2026-06-10–12 | C render batch finishes (6 of 18). |
| 2026-06-13 | All 18 renders re-tagged, named, COA'd. |
| 2026-06-14 | `docs/wesley_brief_onepager.md` polished + reviewed by Wesley. |
| 2026-06-15 | PDFs generated for all docs. |
| 2026-06-16 | Asunción print shop selected; ICC profile coordinated. |
| 2026-06-17–20 | Prints produced + collected. |
| 2026-06-21 | Wesley pickup in Asunción. |
| 2026-06-22–25 | Wesley reviews, prepares mental script. |
| 2026-06-27 | Escritura meeting. |

## Risk register

1. **C render fails to finish.** Mitigation: A + B alone (12 renders) is publishable; C can wait a week.
2. **Print shop ICC mismatch.** Mitigation: send a test print of A_dusk + check color before bulk run.
3. **Wesley travel delay.** Mitigation: cloud bundle + Asunción notary office hands-off pickup.
4. **Wesley changes the design** between now and 2026-06-27. Mitigation: documentation flagged "living doc"; any change ripples through `floor_plan` + `bom` + `phasing` + render queue.

## Post-escritura follow-up

1. **2026-07-15**: Wesley confirms inscription at registro de inmuebles. We archive a copy of the título escritura in `docs/contract_summary.md`.
2. **2026-07-30**: Phase 1 (LQV house construction) kicks off; AI Whisperers shifts to construction-supervision tooling (cost tracker, photo journal generator).
3. **2026-09**: Soft launch of `quebrada-viva.com` (placeholder TBD).

## Variant C delivery satellite (additive 2026-06-10, in-session)

Pipeline-table row "2026-06-10–12 | C render batch finishes" is **already in motion as of 2026-06-10 17:25 local**. Recorded here so the manifest above stays frozen until atomic end-of-batch update:

- **C_hero** ☑ on disk (19.9 MB, 2560×1440 hero res).
- **C_stream_up** ☑ on disk (11.2 MB, 1920×1080).
- **C_terrace** ⏳ rendering, ~2 min ETA at write-time.
- **C_cliff / C_dusk / C_petal_macro** pending (per-cam Blender process loop, prevents OOM accumulation).
- **Disk total**: 14/18 finals.

**Variant C visual signatures** are procedural code recipes (no third-party asset, no extra CC-BY obligation): `lqv/flora/fireflies.py` (~80 emission spheres), `lqv/house/cob.py:build_window_emission` (warm window glow planes inside hidden `WindowCut_*` outlines), `lqv/lighting.py` Variant C branch (cool moonlight + reduced Nishita sky strength). The Tier-2 USB / cloud bundle therefore needs no additional license artefact beyond the same `CREDITS.md` + `LICENSE_BUNDLE.md` + `LICENSES/README.md` triple that already covers A and B.

**Risk-register #1 update**: "C render fails to finish" mitigation is now *partially executed* — per-cam relaunch loop has already delivered 2/6 C-cams cleanly; A+B still publishable on its own if the remaining 4 fail. No action needed unless render loop SIGKILLs.

## Cross-references

- `docs/wesley_brief_onepager.md` — the one-pager itself.
- `docs/master_plan.md` — full plan.
- `docs/HOUSING_PARK_CONCEPT.md` — typology designs.
- `docs/floor_plan.md` — interior plan.
- `docs/section_view.md` — section drawing.
- `docs/build_sequence.md` — construction order.
- `docs/bom.md` — cost estimate.
- `docs/energy_budget.md` — systems sizing.
- `docs/housing_park_phasing.md` — 5-year roadmap.
- `docs/license_obligations.md` — attribution + IP framework.
- `docs/cultural_notes.md` — authenticity backing.
- `docs/contract_summary.md` — parcel + ownership facts (Wesley to keep current).
- `LICENSES/README.md` (repo root) — verbatim CC0 + CC-BY 4.0 legal-code mirror; required in Tier-2 USB/cloud bundle alongside `LICENSE_BUNDLE.md` (added 2026-06-10).
- `STATUS.md` (repo root) — current render manifest + open-task ledger; the source of truth for "what's actually on disk right now" vs the production-pipeline schedule above.
- `docs/SESSION_LOG.md` — narrative log of the 2026-06-10 mega-session including Variant C implementation + the per-cam render-loop architecture decision that produced the C batch.
- `ARCHITECTURE.md` (repo root) — `lqv/` package code map including "Variant C additions" block (the procedural recipes referenced in the delivery satellite above).

### Extended back-pointers (additive 2026-06-10)

Closing the reciprocal-pointer gap: docs that name this deliverable spec forward (CLAUDE.md "Document map" + new "Supplementary docs" sub-section, LICENSES/README.md "Extended back-pointers", LICENSE_BUNDLE.md §8, CREDITS.md §Cross-references, asset_plan.md §G, external_assets.md, research_index.md root, photographic_references.md) had no inbound listing here. Listed below with *why* each matters:

- `CLAUDE.md` §"Document map" + §"Supplementary docs (Tier 2 — 2026-06-10 mega-session)" — CLAUDE.md is the entry-point doc every new Claude session reads first; its Document map + new Tier-2 sub-section both name this file as the canonical packaging-spec for the Wesley deliverable. Any cold-start session begins discovery of this bundle's Tier-1/2/3 split there.
- `CREDITS.md` §Cross-references — CREDITS.md is the Tier-2 bundle payload (per-asset attribution lines); this file is the spec saying *what* CREDITS.md ships in. CREDITS.md's reciprocal pointer back to this file documents that contract from the attribution side.
- `LICENSE_BUNDLE.md` §8 + §6 readiness gates — LICENSE_BUNDLE.md is the other Tier-2 bundle payload (per-license summary + readiness checklist); §6 gates explicitly require the Tier-2 USB bundle to ship the LICENSE_BUNDLE.md alongside CREDITS.md and the LICENSES/ directory. This file is where that requirement is specified end-to-end.
- `LICENSES/README.md` §"Extended back-pointers" — LICENSES/README.md is the legal-text backing-store of the Tier-2 bundle; its tick-14 reverse pointers explicitly name this file because Tier-2 §packaging includes `LICENSES/` directory contents as the offline-complete legal corpus. This file is the packaging spec; LICENSES/ is the payload.
- `docs/asset_plan.md` §G — asset_plan §G is the Phase 1-8 forward plan; every asset row eventually feeds into the Tier-2 bundle. The asset planning surface and the deliverable spec are complementary: §G says *what to import*, this file says *how to package*.
- `docs/external_assets.md` §Cross-references — external_assets.md is the per-asset `[USED]`/`[PLANNED]` ledger; the Tier-2 bundle packaging cannot be finalised until every row is `[USED]` or explicitly excluded. This file consumes external_assets.md as a precondition for the final bundle freeze.
- `docs/research_index.md` (root note) — research_index catalogues the ~80 repos surveyed during Phase 7.5; downstream Phase 8+ imports referenced in the production pipeline above derive from that survey. The research index is upstream of the import plan, which is upstream of this packaging spec.
- `docs/photographic_references.md` — separate license framework for reference photography in `assets/references/` (NOT embedded in renders, so NOT in Tier 1 renders, but Tier 2 USB COULD include photo references with their own per-photo attribution). This file's Tier-2 scope decision (asset-license-mirrors-only vs include-photo-references) maps to that doc's parallel framework.
