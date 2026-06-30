# B06: LiDAR drone survey vs hi-res satellite decision

**Category:** [Buyer/Investor Experience (VR + 3D + Demos)](../buyer_experience/README.md)
**Priority:** P1
**Owner:** Erebus
**Status:** `research_needed`
**Source:** wes_recording_2026-06-30_v2
**Deliverable:** $200 satellite vs $1,200 LiDAR drone comparison + provider list

---

## What Wes wants

$200 satellite vs $1,200 LiDAR drone comparison + provider list

**From Wes's words:**

> _"[Dream list 2026-06-30]: llucinaties) | # | Wens | Werkelijk doel | Wie kan het | Status | |---|---|---|---|---| | D1 | **3D/VR site placement tool** — huizen verplaatsen op satelliet, 5m, andere kant, grotere veranda | Interactieve LQV-site-map met typology-plaatsing | Erebus / Hermes | ✅ Reeds lopend via `lqv-walkthrough.pages.dev` | | D2 | **VR-bril walkthrough** — investeerder/koper loopt virtueel door huis | Buyer-facing 3DG"_

> _"[Dream list 2026-06-30]: S viewer (Three.js / Cesium / UE5) | Erebus + Vast.ai pipeline | 🟡 Pipeline klaar, wacht op Wes's Luma-captures | | D3 | **Satelliet-imagerie voor optimale huis-plaatsing** — zon, uitzicht, elkaar niet zien | Auto-layout script met zonsimulatie + viewshed-analyse | Erebus | 🟢 Mogelijk met ALOS DEM + Sentinel-2 albedo, Fase 2 | | D4 | **Foto's/VB rond de site** voor visuele refere"_

> _"[Raw transcript 2026-06-30]: en. Als je ze leert hoe je het maakt." > > "Als je ze leert vissen, brengen ze je vissen. Ja. Maar prijzen en zoiets kan je zeker maken." > > "Met de satelliet-imagerie en zo. Helpen beslissen waar de huizen op optimaal zijn, zodat ze elkaar niet zien. De zon, het beste uitzicht, al die random dingen." > > "Je kunt ook zeggen, waar zou je recommenderen? Kijk eens, het ziet er goed uit. Ja. Als je het in ee"_

## Why this matters



## Full picture — context, constraints, history

**Buyer-experience stack.** These tools are the shop window for investors + future guests. Already-shipped infrastructure: lqv-walkthrough.pages.dev (live), Three.js viewer, 12 toggleable data layers, 3DGS self-host pipeline (Vast.ai + COLMAP), Cesium 3D viewer. The capture brief at [briefs/wes_capture_brief.md](../../briefs/wes_capture_brief.md) is the protocol Wes needs to follow.

## What we know already (research summary)

- **Deliverable target:** $200 satellite vs $1,200 LiDAR drone comparison + provider list
- **Source:** [Wes's brainstorm recording](../../briefs/wes_recording_2026-06-30_raw.md) (raw transcript)
- **Cleaned version:** [dream list](../../briefs/wes_recording_2026-06-30_dreamlist.md) + [action list](../../briefs/wes_recording_2026-06-30_actionlist.md)


## What needs research

- **Identify 2-3 drone pilots in PY with LiDAR (DJI L1/L2 sensors)** — source: Ivan's network, Paraguayan drone association (Asociación de Drones Paraguay)
- **Get specific quotes from 2-3 pilots** — compare against $1,200 estimate
- **Test LiDAR processing pipeline** — need GIS expertise (QGIS + PDAL or CloudCompare)
- **Validate processing time per flight** — affects overall schedule

## Dependencies

**This idea depends on / is informed by:**

- [`B03`](../buyer_experience/b03_satellite-driven_optimal_placement_(sun,_view,_pri.md) — placement
- [`C04`](../construction/c04_ground_bores_with_gps_points_(depth_to_bedrock).md) — ground bores
- [`I18`](../risk_mitigation/i18_water_security_audit_drought_and_contamination.md) — water security



## Risks & failure modes

_No specific risks identified beyond standard category risks. Add as they emerge._

## Cost / time estimate

_Estimate pending — see "What needs research" section for named cost sources._

## Done = shipped

**Acceptance criteria (measurable):**

- $200 satellite vs $1,200 LiDAR drone comparison + provider list
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

**Status:** Open question. No answer yet. Erebus to research or Wes to provide input.

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
