# Reconciled Docs — Read Me

**Date:** 2026-06-30
**Status:** First-pass reconciliation. Both source sets preserved unchanged.

## What this directory is

This is the **merged view** of two overlapping but non-identical project state sets:

1. **Wes's working files** (the Excel/DOCX set Ivan pasted in) — canonical for financial, cabin, infra, equipment, activities, F&B, materials, business structure
2. **Ivan's LQV repo + working dir** (`Ai-Whisperers/la-quebrada-viva` + `/root/.hermes/lqv-splat/`) — canonical for escritura milestone, land details, 3DGS pipeline, Sonja's 2030 deadline, partnership structure, render-pipeline typology concept art

This directory does **not** modify or replace either source. Both stay intact:
- Wes's files live on his local machine
- LQV repo lives on GitHub (commit `1d4c855` + the new commit from this PR)

The reconciled docs here are the **bridge** — what Wes, Ivan, Kiki, Erebus read together to understand the project as it stands now.

## What to read first

**If you only have 5 minutes:** read `MASTER_BRIEF.md`

**If you have 30 minutes:** read `MASTER_BRIEF.md` + `OPEN_DECISIONS.md`

**If you have 2 hours:** read everything below + cross-reference to `docs/ideas/INDEX.md` for the 109-idea catalog

## The documents

| Doc | Purpose | Source of truth for |
|---|---|---|
| `MASTER_BRIEF.md` | Single-page overview of everything | Project identity, big numbers, key dates |
| `FINANCIAL_MODEL.md` | €5.5M Phase 1 + 3 scenarios | All financial figures (capex, revenue, staff, fixed costs) |
| `CABIN_CATALOG.md` | 30 cabins, 10 types | Per-type build cost, night price, guest count |
| `INFRASTRUCTURE_8_PHASES.md` | Survey → materials → water → sewer → electric → internet → roads → irrigation | Phase ordering, deliverables, costs |
| `EQUIPMENT_STRATEGY.md` | Heavy equipment import 2nd hand NL, standard buy PY | Equipment buy/rent decisions |
| `ACTIVITIES_25_PLUS.md` | 25+ activities catalogued | Activity list, pricing, cross-ref to LQV amenities |
| `MATERIALS_PRICE_TEMPLATE.md` | 17-category priority list + 14-sheet master | What materials to source, in what order |
| `BUSINESS_STRUCTURE.md` | Founder vs 4-entity BV vs hybrid | Legal structure decision |
| `LAND_PARCEL.md` | 62 ha Escobar + escritura + 3DGS | Land details, what's confirmed, what's open |
| `OPEN_DECISIONS.md` | 12 decisions owed by Wes | What's blocking, who's deciding, what to do |

## Cross-references

Each doc links to:
- **Source files** (Wes's local files, LQV repo, written transcripts)
- **LQV catalog** (109 ideas in `docs/ideas/`, INSIGHTS, SUGGESTED)
- **LQV render pipeline** (where it intersects)

## Maintenance

This directory is updated by Erebus as decisions get made. When a decision in `OPEN_DECISIONS.md` resolves:
1. Update the relevant doc (e.g. `BUSINESS_STRUCTURE.md` if Decision 1 closes)
2. Update the LQV catalog idea file (e.g. `F01_4-entity_bv_cascade...md`)
3. Update `OPEN_DECISIONS.md` to reflect the new state
4. Commit to LQV repo (preserves history)

## What this is NOT

- This is **not** a replacement for either source set. Both stay intact.
- This is **not** an executable plan. The actionable items are in `OPEN_DECISIONS.md`.
- This is **not** a Wes-side deliverable. The Wes-facing artefacts are:
  - **Investor pitch deck** (Phase 2 deliverable, pending F01 decision)
  - **Buyers' site walkthrough** (live at lqv-walkthrough.pages.dev)
  - **Materials quote package** (Phase 1, pending D5)
  - **Insurance pre-qualification** (URGENT, pending D6)
  - **Construction playbook** (Phase 1, pending T01-T03 specs)
- This is **not** the escritura-frozen record. The escritura-frozen artefacts are at `docs/escritura_deck/`, `docs/boq/`, and the `escritura-2026-06-27` tag.

## Source

**Created by:** Erebus (AI Whisperers)
**Date:** 2026-06-30
**For:** Wesley van de Camp + Ivan + Kiki
**Trigger:** Ivan's prior work was based on a partial share from Wes. The full working set became available 2026-06-30, prompting this reconciliation.
