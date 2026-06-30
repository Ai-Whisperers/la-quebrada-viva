# B03: Satellite-driven optimal placement (sun, view, privacy)

**Category:** [Buyer/Investor Experience (VR + 3D + Demos)](../buyer_experience/README.md)
**Priority:** P1
**Owner:** Erebus
**Status:** `planned`
**Source:** wes_recording_2026-06-30
**Deliverable:** site-layout recommender Python tool

---

## What Wes wants

site-layout recommender Python tool

**From Wes's words:**

> _"[Action list 2026-06-30]: Taak | Wanneer | Owner | |---|---|---|---| | K1 | In gesprek met oude eigenaar over overname koeien | Week 2 | Wesley | | K2 | Inschatten waarde + gezondheid kudde | Week 3 | Wesley + dierenarts | | K3 | Afronden overname + nieuwe contract medewerker (vee + terrein) | Week 4 | Wesley + Sonja | | K4 | Terreinonderhoud-schema (weide, water, gezondheid) | Lopend | Nieuwe medewerker | --- ## §6 — FINA"_

> _"[Action list 2026-06-30]: | Prijzen-documenet (`docs/research/2026-06-30_construction_prices_paraguay_nl.md`) onderhouden + maandelijks update | Lopend | ✅ Nu live | | E3 | VR-viewer itereren — voeg typology-plaatsing + viewshed-analyse toe | Week 2-3 | 🟡 Pipeline klaar | | E4 | LQV-onderzoeks-corpus verder uitbreiden (escobar_dieren, escobar_bloemen, etc.) | Week 2 | ⚪ | | E5 | Questionnaire-skill — periodieke vragen aan Wesl"_

> _"[Dream list 2026-06-30]: llucinaties) | # | Wens | Werkelijk doel | Wie kan het | Status | |---|---|---|---|---| | D1 | **3D/VR site placement tool** — huizen verplaatsen op satelliet, 5m, andere kant, grotere veranda | Interactieve LQV-site-map met typology-plaatsing | Erebus / Hermes | ✅ Reeds lopend via `lqv-walkthrough.pages.dev` | | D2 | **VR-bril walkthrough** — investeerder/koper loopt virtueel door huis | Buyer-facing 3DG"_

> _"[Dream list 2026-06-30]: S viewer (Three.js / Cesium / UE5) | Erebus + Vast.ai pipeline | 🟡 Pipeline klaar, wacht op Wes's Luma-captures | | D3 | **Satelliet-imagerie voor optimale huis-plaatsing** — zon, uitzicht, elkaar niet zien | Auto-layout script met zonsimulatie + viewshed-analyse | Erebus | 🟢 Mogelijk met ALOS DEM + Sentinel-2 albedo, Fase 2 | | D4 | **Foto's/VB rond de site** voor visuele refere"_

## Why this matters



**Related insights from the catalog pass:**

- [Insight #3: Insurance + fire risk are coupled and urgent](../INSIGHTS.md) — _Insurance + fire risk are coupled and urgent_
- [Insight #12: Three "research_needed" items have known answers Wes can act on](../INSIGHTS.md) — _Three "research_needed" items have known answers Wes can act on_

## Full picture — context, constraints, history

**Buyer-experience stack.** These tools are the shop window for investors + future guests. Already-shipped infrastructure: lqv-walkthrough.pages.dev (live), Three.js viewer, 12 toggleable data layers, 3DGS self-host pipeline (Vast.ai + COLMAP), Cesium 3D viewer. The capture brief at [briefs/wes_capture_brief.md](../../briefs/wes_capture_brief.md) is the protocol Wes needs to follow.

## What we know already (research summary)

- **Deliverable target:** site-layout recommender Python tool
- **Source:** [Wes's brainstorm recording](../../briefs/wes_recording_2026-06-30_raw.md) (raw transcript)
- **Cleaned version:** [dream list](../../briefs/wes_recording_2026-06-30_dreamlist.md) + [action list](../../briefs/wes_recording_2026-06-30_actionlist.md)


## What needs research

- _No additional research tasks defined — see related ideas for context._

## Dependencies

**This idea depends on / is informed by:**

- [`B06`](../buyer_experience/b06_lidar_drone_survey_vs_hi-res_satellite_decision.md) — LiDAR
- [`B02`](../buyer_experience/b02_interactive_site-placement_tool_(move_houses_5m).md) — placement tool
- [`T01`](../house_typologies/t01_type_a_—_romantic_2p_(30-40_m²).md) — typology specs



## Risks & failure modes

_No specific risks identified beyond standard category risks. Add as they emerge._

## Cost / time estimate

_Estimate pending — see "What needs research" section for named cost sources._

## Done = shipped

**Acceptance criteria (measurable):**

- site-layout recommender Python tool
- Document the deliverable's location/path in this file
- Update the **Status** field above to `shipped`
- Add a 1-line entry to the Changelog below
- For research-type ideas: link the deliverable doc + note 1 key finding

## Recommended next action

1. **Wes: provide phone captures (B07) if not yet done** — this is the blocker for B01/B02/B03/B05
2. **Erebus: prototype the feature on lqv-walkthrough.pages.dev**
3. **Wes: review prototype + flip status** to `shipped` or iterate

## Priority & status meaning

**Priority:** **Needed for Phase 1 (months 1-9 post-escritura) or the first 30 days of post-escritura work.**

**Status:** Scoped and queued. Not yet started.

## Sources & references

- [Wes's brainstorm recording (raw)](../../briefs/wes_recording_2026-06-30_raw.md)
- [Wes's dream list (cleaned)](../../briefs/wes_recording_2026-06-30_dreamlist.md)
- [Wes's action list (cleaned)](../../briefs/wes_recording_2026-06-30_actionlist.md)
- [Wes's capture brief](../../briefs/wes_capture_brief.md)
- [INDEX.md](../../INDEX.md) — master catalog
- [INSIGHTS.md](../../INSIGHTS.md) — 20 patterns from reading the catalog
- [SUGGESTED.md](../../SUGGESTED.md) — 20 ideas Erebus pushed in
- Related project docs: [HOUSING_PARK_CONCEPT.md](../../HOUSING_PARK_CONCEPT.md), [EUROPEAN_TOURISM_SPEC.md](../../EUROPEAN_TOURISM_SPEC.md), [MASTER_BRIEF.md](../../MASTER_BRIEF.md), [RESEARCH_GAPS.md](../../RESEARCH_GAPS.md)

## Changelog

- 2026-06-30: Idea created from consolidated session review (initial scaffold)
- 2026-06-30: Rich content pass — What/Why/Context/Research/Dependencies/Risks/Cost/Done/Action sections populated
