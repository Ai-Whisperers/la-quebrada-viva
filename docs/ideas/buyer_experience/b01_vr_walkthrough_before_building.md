# B01: VR walkthrough before building

**Category:** [Buyer/Investor Experience (VR + 3D + Demos)](../buyer_experience/README.md)
**Priority:** P1
**Owner:** Erebus
**Status:** `in_progress`
**Source:** wes_recording_2026-06-30 + 2026-06-30_v2
**Deliverable:** lqv-walkthrough.pages.dev Three.js viewer

---

## What Wes wants

lqv-walkthrough.pages.dev Three.js viewer

**From Wes's words:**

> _"[Action list 2026-06-30]: WA5 | **BV/bedrijfsstructuur advies** — meerdere bv's NL vs PY, wanneer verplicht | Onderzoek belastingadvies NL + PY | Memo + contacten | | WA6 | **VR/3D interactief prototype** — site-map met verplaatsbare huizen | Bouwen op lqv-walkthrough.pages.dev | Live demo | | WA7 | **Marketing-plan voor 1e-huur-huizen** (Booking.com + Airbnb + niche) | Onderzoek + template listings | Template + strategy |"_

> _"[Action list 2026-06-30]: E2 | Prijzen-documenet (`docs/research/2026-06-30_construction_prices_paraguay_nl.md`) onderhouden + maandelijks update | Lopend | ✅ Nu live | | E3 | VR-viewer itereren — voeg typology-plaatsing + viewshed-analyse toe | Week 2-3 | 🟡 Pipeline klaar | | E4 | LQV-onderzoeks-corpus verder uitbreiden (escobar_dieren, escobar_bloemen, etc.) | Week 2 | ⚪ | | E5 | Questionnaire-skill — periodieke vragen aan"_

> _"[Action list 2026-06-30]: ley | Week 2 | ⚪ | | E8 | Research-pipeline — elke week 5 nieuwe topics onderzocht + gerapporteerd | Lopend | ⚪ | | E9 | Prijs-offertes automatisch opvragen bij leveranciers via templates | Week 3 | ⚪ | --- ## §4 — THIJS + WESLEY (eerste maanden — operationeel op de site) | # | Taak | Wanneer | Owner | |---|---|---|---| | T1 | **Locaties voor typologie-huizen bepalen** (via VR + site-visie) | Maa"_

> _"[Action list 2026-06-30]: | Erebus | | TE3 | **3DGS captures verwerken zodra Wesley levert** | Na Wesley's eerste album | Erebus | | TE4 | **UE5 / Pixel Streaming setup** voor VR-walkthrough | Maand 2-3 | Erebus | | TE5 | **VR-bril demo** voor investeerders | Maand 3 | Erebus + Wesley | --- ## §8 — EERSTE HUIS BOUW (komende 6 maanden) | # | Taak | Wanneer | Owner | |---|---|---|---| | H1 | **Bamboe-honing kleur behandelin"_

## Why this matters



**Related insights from the catalog pass:**

- [Insight #6: The buyer-experience tools are 80% done — just needs the captures](../INSIGHTS.md) — _The buyer-experience tools are 80% done — just needs the captures_
- [Insight #12: Three "research_needed" items have known answers Wes can act on](../INSIGHTS.md) — _Three "research_needed" items have known answers Wes can act on_

## Full picture — context, constraints, history

**Buyer-experience stack.** These tools are the shop window for investors + future guests. Already-shipped infrastructure: lqv-walkthrough.pages.dev (live), Three.js viewer, 12 toggleable data layers, 3DGS self-host pipeline (Vast.ai + COLMAP), Cesium 3D viewer. The capture brief at [briefs/wes_capture_brief.md](../../briefs/wes_capture_brief.md) is the protocol Wes needs to follow.

## What we know already (research summary)

- **Deliverable target:** lqv-walkthrough.pages.dev Three.js viewer
- **Source:** [Wes's brainstorm recording](../../briefs/wes_recording_2026-06-30_raw.md) (raw transcript)
- **Cleaned version:** [dream list](../../briefs/wes_recording_2026-06-30_dreamlist.md) + [action list](../../briefs/wes_recording_2026-06-30_actionlist.md)
- 3DGS self-host pipeline shipped 2026-06-30 (Vast.ai + COLMAP + gsplat)
- Three.js viewer live at lqv-walkthrough.pages.dev
- 18 Cycles final renders already ship-quality
- UE5.7 + NanoGS scaffold in [ue_project/](../../ue_project/)
- Pixel Streaming build scripts ready

## What needs research

- _No additional research tasks defined — see related ideas for context._

## Dependencies

**This idea depends on / is informed by:**

- [`B07`](../buyer_experience/b07_phone_capture_pipeline_(luma_self-host).md) — capture pipeline
- [`B04`](../buyer_experience/b04_buyer-facing_live_site_map.md) — site map
- [`I12`](../buyer_experience/i12_vr_what-if_scenarios_for_investors.md) — scenarios



## Risks & failure modes

_No specific risks identified beyond standard category risks. Add as they emerge._

## Cost / time estimate

_Estimate pending — see "What needs research" section for named cost sources._

## Done = shipped

**Acceptance criteria (measurable):**

- lqv-walkthrough.pages.dev Three.js viewer
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

**Status:** Active work in progress by Erebus or the team.

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
