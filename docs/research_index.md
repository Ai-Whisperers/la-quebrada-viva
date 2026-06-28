# Research Index — Meta-Pointer to Every Research Doc in the Project

**Status:** living document. The single entry point that links every research document in `docs/` so that a newcomer (Wesley, Thijs, a future Claude session, a new collaborator) can navigate without grepping the directory.

Use this file as the **starting point** when joining the project.

## By document type

### Research narratives

- **`docs/paraguay_clay_house_research.md`** — Paraguay-specific cob/adobe research: climate data for Paraguarí, soil characteristics, lapacho timber availability, mosquito/insect pressure, local construction labour rates.
- **`docs/HOUSING_PARK_CONCEPT.md`** — The 8-typology housing-park concept: market positioning, target guest profile, 25 open questions for Wesley.
- **`docs/EUROPEAN_TOURISM_SPEC.md`** — Europe-source travellers' preferences, average daily rate elasticity, booking funnel.
- **`docs/cultural_notes.md`** — Paraguayan cultural design constraints; what to use vs avoid (Rule 8 backing).

### Engineering specs

- **`docs/MASTER_BRIEF.md`** — The 10 design rules. Authoritative source.
- **`docs/floor_plan.md`** — Room-by-room program.
- **`docs/build_sequence.md`** — Construction phase order.
- **`docs/section_view.md`** — NW-SE section drawing description.
- **`docs/energy_budget.md`** — PV, battery, hydro, LPG sizing.
- **`docs/bom.md`** — Bill of materials, total USD ~56k.

### Project ops & roadmap

- **`docs/master_plan.md`** — Top-level overview (the entry-point doc most older Claude sessions read first).
- **`docs/housing_park_phasing.md`** — 5-year build-out plan with money cadence.
- **`docs/wesley_deliverable_bundle.md`** — Escritura-day shipping manifest.
- **`docs/wesley_brief_onepager.md`** — One-pager for Wesley's escritura meeting.
- **`docs/CLOSING_DAY_PREP.md`** — Printable T-7 / T-5 / T-2 / signing-day / T+30 escritura checklist + risk register.
- **`docs/contract_summary.md`** — Parcel ID + ownership facts. Wesley keeps current.

### Asset pipeline

- **`docs/asset_plan.md`** — What assets we want, where they live, how we source them.
- **`docs/external_assets.md`** — Download log, license, modifications.
- **`CREDITS.md`** (repo root) — Attribution list (CC-BY 4.0 obligation).
- **`LICENSE_BUNDLE.md`** (repo root) — License texts.
- **`docs/license_obligations.md`** — How we satisfy each license.
- **`docs/site_data_spike.md`** — DEM / topo data acquisition spike.
- **`docs/photographic_references.md`** — Photo reference index.

### Gap analysis & forward-looking

- **`docs/RESEARCH_GAPS.md`** — What we don't yet know. Updated when we hit unknowns.

### Code & state docs (additive 2026-06-10 — previously orphaned from this index)

These are not research narratives, but a newcomer joining the project hits them within the first 10 minutes and needs the pointer somewhere central. Added here as a satellite section so the index is complete without rewriting the categories above.

- **`CLAUDE.md`** (repo root) — operating instructions for any future Claude session: doc map, 10 rules, code invariants, samples policy, variants A/B/C status. Authoritative for "what is true right now".
- **`STATUS.md`** (repo root) — render manifest (current: A/B 12/12 ☑, C 2/6 ☑ + 4 in flight), open tasks, decisions log, critical dates. Updated at session end.
- **`ARCHITECTURE.md`** (repo root) — `lqv/` package code map: module-by-module table, RNG-ordering invariants, positional coupling web, Variant C additions block (2026-06-10).
- **`docs/SESSION_LOG.md`** — narrative log of the 2026-06-10 mega-session; tick-by-tick continuation arc with rationale for every additive doc edit. Read after a break to re-orient.
- **`LICENSES/README.md`** — verbatim CC0 + CC-BY 4.0 legal-code mirror; vendor-terms pointer table. Reciprocal to `CREDITS.md` §"Cross-references".
- **`docs/claude_code_blender_best_practices.md`** — generic tooling reference (already listed in `CLAUDE.md`'s doc map but worth a pointer here for completeness).

## By topic

### Climate & geography

- `paraguay_clay_house_research.md` §climate, §soil.
- `energy_budget.md` §design-conditions.
- `cultural_notes.md` §plant-language.
- `site_data_spike.md` §coordinate-system-notes.

### Materials & construction

- `MASTER_BRIEF.md` Rules 1–5.
- `build_sequence.md` Phases 1–6.
- `bom.md` §1–§5.
- `floor_plan.md` §compliance.
- `cultural_notes.md` §materials.

### Energy & water systems

- `MASTER_BRIEF.md` Rules 7, 9, 10.
- `energy_budget.md` (entire).
- `build_sequence.md` Phase 7.
- `bom.md` §6.

### Off-grid resilience

- `MASTER_BRIEF.md` Rule 7.
- `energy_budget.md` §outage-resilience.
- `housing_park_phasing.md` §risks.

### Cultural authenticity

- `MASTER_BRIEF.md` Rule 8.
- `cultural_notes.md` (entire).
- `floor_plan.md` §adjacencies.
- `HOUSING_PARK_CONCEPT.md` §brand-positioning.

### Tourism & monetisation

- `EUROPEAN_TOURISM_SPEC.md` (entire).
- `HOUSING_PARK_CONCEPT.md` §market-positioning.
- `housing_park_phasing.md` §money-cadence.
- `wesley_deliverable_bundle.md` §tier-1.

### Asset licensing

- `license_obligations.md` (entire).
- `CREDITS.md`.
- `LICENSE_BUNDLE.md`.
- `asset_plan.md` §licenses.

### Site survey & DEM

- `site_data_spike.md` (entire).
- `section_view.md` §section-line.
- `housing_park_phasing.md` §risks.

## By stakeholder

### Wesley (client, 75% owner)

Reads first:
1. `wesley_brief_onepager.md`
2. `master_plan.md`
3. `housing_park_phasing.md`
4. `bom.md`
5. `energy_budget.md`

Periodically:
- `MASTER_BRIEF.md`
- `HOUSING_PARK_CONCEPT.md` (especially the 25 open questions for him)

### Thijs (25% owner, brother)

Reads first:
1. `master_plan.md`
2. `housing_park_phasing.md` (focus money cadence + risks)
3. `EUROPEAN_TOURISM_SPEC.md` (booking funnel, ADR)

### Future Claude session

Reads first:
1. `CLAUDE.md` (repo root)
2. `STATUS.md`
3. This file (`research_index.md`)
4. `MASTER_BRIEF.md`
5. `RESEARCH_GAPS.md`

### A new collaborator (visiting arquitecto, photographer, marketer)

Reads first:
1. `master_plan.md`
2. `cultural_notes.md`
3. The 18 final renders
4. `MASTER_BRIEF.md`

## Dependency arrows

```
contract_summary ─┐
                  ├─→ master_plan ─→ wesley_brief_onepager ─→ wesley_deliverable_bundle
MASTER_BRIEF ─────┤                  ↓
paraguay_research ┤              HOUSING_PARK_CONCEPT ─→ housing_park_phasing
cultural_notes ───┘                  ↓                           ↓
                                EUROPEAN_TOURISM_SPEC      bom + energy_budget
                                                                 ↓
                                                          build_sequence
                                                                 ↓
                                                          floor_plan + section_view
                                                                 ↓
                                                          asset_plan ──→ external_assets
                                                                 ↓             ↓
                                                          license_obligations ─ CREDITS + LICENSE_BUNDLE
                                                                 ↓
                                                          site_data_spike ──→ photographic_references
                                                                 ↓
                                                          RESEARCH_GAPS (updated whenever we hit unknowns)
```

Escritura-day side-chain (Phase 0 driver — closes 2026-06-27):

```
contract_summary ──┐
                   ├─→ CLOSING_DAY_PREP ←── wesley_brief_onepager
wesley_deliverable_bundle ─────┘                ↑
                                                housing_park_phasing (Phase 0 begins post-signing)
```

## Cross-references (additive 2026-06-10 — closes reverse-discoverability gap)

This index has always been *referenced forward* by adjacent docs (asset_plan §G second-pass, master_plan §Phase 7.5, wesley_deliverable_bundle Extended back-pointers, CLAUDE.md Supplementary docs sub-section) but the reverse pointers were never collected here. Listed below with *why* each back-link matters; the dependency arrows graph above is unchanged.

- `CLAUDE.md` §"Supplementary docs (Tier 2 — 2026-06-10 mega-session)" — entry-point doc names this index as the canonical pointer to the ~80-repo Phase 7.5 survey. Any cold-start session begins research discovery here.
- `docs/master_plan.md` §Phase 7.5 — master_plan names this index as the deliverable artefact of Phase 7.5 (the research-survey phase that ratified the Phase 1-8 asset-procurement order). Master_plan is upstream; this index is downstream of Phase 7.5.
- `docs/asset_plan.md` §G + §G second-pass — asset_plan §C.3 Sketchfab shortlist + §C.4 Hyper3D prompt archive draw directly from this index. asset_plan is the curated downstream shortlist; this index is the upstream survey.
- `docs/wesley_deliverable_bundle.md` §"Extended back-pointers (additive 2026-06-10)" — the Tier-2 USB bundle's asset choices ultimately derive from this index. wesley_deliverable_bundle is the packaging spec; this index is the upstream research feed.
- `docs/external_assets.md` Cross-references — external_assets is the per-asset `[USED]`/`[PLANNED]` ledger; every `[USED]` row's selection rationale traces back to a research_index entry. external_assets is the live download log; this index is the candidate pool from which `[USED]` rows were selected.
- `docs/photographic_references.md` — parallel framework for reference photography. Where this index catalogues *3D-asset repositories*, photographic_references catalogues *reference-photo sources*; both feed Phase 7.5 evaluation. The two indexes are complementary.
- `docs/RESEARCH_GAPS.md` — the gaps doc enumerates *what we don't yet know how to procure*; this index enumerates *what we surveyed*. RESEARCH_GAPS is the negative-space companion to this positive-space catalogue.
- `docs/SESSION_LOG.md` — narrative log of the 2026-06-10 mega-session including the Phase 7.5 research execution that produced this index. SESSION_LOG is the audit trail; this index is the survey result.

## Maintenance rule

When a new `docs/*.md` is added: edit THIS file to list it. Otherwise it's orphaned and future sessions won't find it.

When a doc is renamed: search-and-replace here too.

When a doc is deleted: remove the entry here; consider whether the content lives somewhere else.
