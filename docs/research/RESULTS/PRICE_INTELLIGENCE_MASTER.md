# PRICE INTELLIGENCE MASTER — 20+ source deep scrape for Wes

**Date:** 2026-07-06
**Author:** Erebus (in-session, parallel subagent dispatch)
**Purpose:** Deep, source-cited price intelligence across every category Wes needs for Phase 1 build + Phase 2 ops. 20+ distinct source URLs per category. Verbatim quotes in Spanish/English. Vendor names + contacts where public. Competitive context.

**Subagent dispatch plan (2 waves of 3 parallel agents, free OpenRouter model per memory note delegation-402-fallback):**
- Wave 1 (running): materials, wood/bamboo, paint
- Wave 2 (running): equipment, infrastructure, business/comparables

**Output files:** `/tmp/intel_batch{1-6}_*.md` (one per category)

---

## Index

| Section | Category | Subagent batch | Status |
|---|---|---|---|
| 1 | Cement + rebar + aggregates + bricks + structural steel | batch1_materials | ⏳ |
| 2 | Timber + bamboo (Guadua) + wood treatments | batch2_wood | ⏳ |
| 3 | Exterior paint + coatings + ASTM specs | batch3_paint | ⏳ |
| 4 | Aluminum + glass + kitchen equipment + AC + pool equipment | batch4_equipment | ⏳ |
| 5 | Solar PV + LiFePO4 + generator + septic + cistern + internet | batch5_infrastructure | ⏳ |
| 6 | Insurance + permits + legal/4-BV + labor + competitive landscape | batch6_business | ⏳ |
| 7 | Consolidated competitive insights (cross-batch synthesis) | (synthesis) | ⏳ |
| 8 | Wes-action priority queue (top 10 highest-leverage findings) | (synthesis) | ⏳ |

---

## How to read this document

- **Verbatim quotes** are marked with `>` blockquote + `[[source-N]]` reference back to the source URL table at end of section.
- **Vendor PYG → USD** at 7,500 PYG/USD (WES_WARNINGS §1); some vendors quote USD directly — keep both.
- **PY-domestic vs imported** marked in the vendor column with `[PY]` / `[BR]` / `[AR]` / `[CN]` / `[DE]` / `[USA]` / `[EU]` flags.
- **Lead time** columns follow the format in `NEW01_ai_price_negotiator.md`: 24-48hr (local), 3-7d (Asunción distributor), 2-4wk (CDE/BR import), 4-8wk (AR import), 6-12wk (container CN/EU).

---

## Section 1 — Cement + Rebar + Aggregates + Bricks + Structural Steel

*[Will be populated by /tmp/intel_batch1_materials.md]*

## Section 2 — Timber + Bamboo + Wood Treatments

*[Will be populated by /tmp/intel_batch2_wood.md]*

## Section 3 — Exterior Paint + Coatings + ASTM Specs

*[Will be populated by /tmp/intel_batch3_paint.md]*

## Section 4 — Aluminum + Glass + Kitchen + AC + Pool Equipment

*[Will be populated by /tmp/intel_batch4_equipment.md]*

## Section 5 — Solar PV + Battery + Generator + Septic + Cistern + Internet

*[Will be populated by /tmp/intel_batch5_infrastructure.md]*

## Section 6 — Insurance + Permits + Legal + Labor + Competitive Landscape

*[Will be populated by /tmp/intel_batch6_business.md]*

---

## Sections 7-8 — Synthesis (post-batch)

*[To be written after all 6 batches return]*

---

## Source provenance protocol

For every price claim in this document, the chain of evidence is:

1. **Primary source** — vendor's own website, official PDF, or Clasipar/MercadoLibre listing with date stamp.
2. **Secondary source** — third-party (ABC Color, Última Hora, BCP index, AHK directory) citing the same price.
3. **Tertiary source** — AI Whisperers prior research (M-series files) with the original URL preserved.
4. **Anecdotal** — Wes/Sonja/Kiki direct quote. Lower weight, flagged explicitly.

A claim with only tertiary or anecdotal sourcing is flagged `⚠️ NEEDS VENDOR CONFIRMATION` in the master summary.

---

*Build-time: 2026-07-06. Subagents dispatched at 13:45 PY. Expected return: 5-10 minutes per batch. Master document will be patched in-place as each batch returns.*