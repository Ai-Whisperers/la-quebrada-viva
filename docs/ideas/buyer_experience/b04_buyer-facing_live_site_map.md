# B04: Buyer-facing live site map

**Category:** [Buyer/Investor Experience (VR + 3D + Demos)](../buyer_experience/README.md)
**Priority:** P0
**Owner:** Erebus
**Status:** `shipped`
**Source:** prior session
**Deliverable:** https://lqv-walkthrough.pages.dev (12 layers, 3DGS viewer)

---

## What Wes wants

https://lqv-walkthrough.pages.dev (12 layers, 3DGS viewer)

**From Wes's words:**

> _"[Action list 2026-06-30]: vies NL + PY | Memo + contacten | | WA6 | **VR/3D interactief prototype** — site-map met verplaatsbare huizen | Bouwen op lqv-walkthrough.pages.dev | Live demo | | WA7 | **Marketing-plan voor 1e-huur-huizen** (Booking.com + Airbnb + niche) | Onderzoek + template listings | Template + strategy | | WA8 | **Google One upgrade uitvoeren** | Handleiding Wesley | Wesley doet credit-card-actie | --- ## §3"_

> _"[Action list 2026-06-30]: eek 1 | ⚪ | | E2 | Prijzen-documenet (`docs/research/2026-06-30_construction_prices_paraguay_nl.md`) onderhouden + maandelijks update | Lopend | ✅ Nu live | | E3 | VR-viewer itereren — voeg typology-plaatsing + viewshed-analyse toe | Week 2-3 | 🟡 Pipeline klaar | | E4 | LQV-onderzoeks-corpus verder uitbreiden (escobar_dieren, escobar_bloemen, etc.) | Week 2 | ⚪ | | E5 | Questionnaire-skill — periodiek"_

> _"[Action list 2026-06-30]: icht | Onderzoek belastingadvies NL + PY | Memo + contacten | | WA6 | **VR/3D interactief prototype** — site-map met verplaatsbare huizen | Bouwen op lqv-walkthrough.pages.dev | Live demo | | WA7 | **Marketing-plan voor 1e-huur-huizen** (Booking.com + Airbnb + niche) | Onderzoek + template listings | Template + strategy | | WA8 | **Google One upgrade uitvoeren** | Handleiding Wesley | Wesley doet credit-card-act"_

> _"[Action list 2026-06-30]: belastingadvies NL + PY | Memo + contacten | | WA6 | **VR/3D interactief prototype** — site-map met verplaatsbare huizen | Bouwen op lqv-walkthrough.pages.dev | Live demo | | WA7 | **Marketing-plan voor 1e-huur-huizen** (Booking.com + Airbnb + niche) | Onderzoek + template listings | Template + strategy | | WA8 | **Google One upgrade uitvoeren** | Handleiding Wesley | Wesley doet credit-card-actie | ---"_

## Why this matters



**Related insights from the catalog pass:**

- [Insight #6: The buyer-experience tools are 80% done — just needs the captures](../INSIGHTS.md) — _The buyer-experience tools are 80% done — just needs the captures_

## Full picture — context, constraints, history

**Buyer-experience stack.** These tools are the shop window for investors + future guests. Already-shipped infrastructure: lqv-walkthrough.pages.dev (live), Three.js viewer, 12 toggleable data layers, 3DGS self-host pipeline (Vast.ai + COLMAP), Cesium 3D viewer. The capture brief at [briefs/wes_capture_brief.md](../../briefs/wes_capture_brief.md) is the protocol Wes needs to follow.

## What we know already (research summary)

- **Deliverable target:** https://lqv-walkthrough.pages.dev (12 layers, 3DGS viewer)
- Live URL: https://lqv-walkthrough.pages.dev (HTTP 200, deployed 2026-06-30)
- 12 vector layers + 3 basemaps + Cesium 3D
- 926 renders tracked in docs/render_catalogue/
- Custom domain lqv.paragu-ai.com: CNAME not set yet (60-sec fix)

## What needs research

- _No additional research tasks defined — see related ideas for context._

## Dependencies

**This idea depends on / is informed by:**

- [`I01`](../operations/i01_reservation_widget_and_whatsapp_handoff.md) — booking widget
- [`I02`](../operations/i02_operations_dashboard_multi-calendar_view.md) — operations dashboard



## Risks & failure modes

_No specific risks identified beyond standard category risks. Add as they emerge._

## Cost / time estimate

_Estimate pending — see "What needs research" section for named cost sources._

## Done = shipped

**Acceptance criteria (measurable):**

- https://lqv-walkthrough.pages.dev (12 layers, 3DGS viewer)
- Document the deliverable's location/path in this file
- Update the **Status** field above to `shipped`
- Add a 1-line entry to the Changelog below
- For research-type ideas: link the deliverable doc + note 1 key finding

## Recommended next action

1. **Wes: provide phone captures (B07) if not yet done** — this is the blocker for B01/B02/B03/B05
2. **Erebus: prototype the feature on lqv-walkthrough.pages.dev**
3. **Wes: review prototype + flip status** to `shipped` or iterate

**Priority note:** This is P0 — should ship within 2 weeks.

## Priority & status meaning

**Priority:** **Critical for the next sprint or the immediate escritura follow-up.** Blocks downstream work.

**Status:** This idea has been delivered. The artefact is on disk or live. See deliverable above for location.

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
