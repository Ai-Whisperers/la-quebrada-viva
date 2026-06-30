# B07: Phone capture pipeline (Luma self-host)

**Category:** [Buyer/Investor Experience (VR + 3D + Demos)](../buyer_experience/README.md)
**Priority:** P0
**Owner:** Wesley+Erebus
**Status:** `shipped_waiting_on_Wes`
**Source:** wes_capture_brief.md
**Deliverable:** splat pipeline live, waiting for Wes's Google Photos album

---

## What Wes wants

splat pipeline live, waiting for Wes's Google Photos album

**From Wes's words:**

> _"[Action list 2026-06-30]: net maandelijks updaten** | Maandelijks | Erebus | | TE2 | **Site-data updates** (weer, beelden, fauna, etc.) | Maandelijks | Erebus | | TE3 | **3DGS captures verwerken zodra Wesley levert** | Na Wesley's eerste album | Erebus | | TE4 | **UE5 / Pixel Streaming setup** voor VR-walkthrough | Maand 2-3 | Erebus | | TE5 | **VR-bril demo** voor investeerders | Maand 3 | Erebus + Wesley | --- ## §8 — EERSTE"_

> _"[Action list 2026-06-30]: **Bouw eerste huis** starten | Maand 2-3 | Wesley + team | | H5 | **Inboedel aanschaffen** voor eerste huis | Maand 4-5 | Wesley | | H6 | **Foto + VR capture** van opgeleverd huis | Maand 6 | Wesley + Erebus | | H7 | **Eerste gast boeking** (test) | Maand 7 | Wesley | --- ## §9 — PRIORITEIT VOLGORDE (komende 30 dagen) | Volgorde | Wat | Owner | |---|---|---| | 1 | Wesley's persoonlijke taken (W1-W5) |"_

> _"[Dream list 2026-06-30]: per loopt virtueel door huis | Buyer-facing 3DGS viewer (Three.js / Cesium / UE5) | Erebus + Vast.ai pipeline | 🟡 Pipeline klaar, wacht op Wes's Luma-captures | | D3 | **Satelliet-imagerie voor optimale huis-plaatsing** — zon, uitzicht, elkaar niet zien | Auto-layout script met zonsimulatie + viewshed-analyse | Erebus | 🟢 Mogelijk met ALOS DEM + Sentinel-2 albedo, Fase 2 | | D4 | **Foto's/VB rond de site"_

> _"[Dream list 2026-06-30]: er/koper loopt virtueel door huis | Buyer-facing 3DGS viewer (Three.js / Cesium / UE5) | Erebus + Vast.ai pipeline | 🟡 Pipeline klaar, wacht op Wes's Luma-captures | | D3 | **Satelliet-imagerie voor optimale huis-plaatsing** — zon, uitzicht, elkaar niet zien | Auto-layout script met zonsimulatie + viewshed-analyse | Erebus | 🟢 Mogelijk met ALOS DEM + Sentinel-2 albedo, Fase 2 | | D4 | **Foto's/VB rond"_

## Why this matters



**Related insights from the catalog pass:**

- [Insight #6: The buyer-experience tools are 80% done — just needs the captures](../INSIGHTS.md) — _The buyer-experience tools are 80% done — just needs the captures_

## Full picture — context, constraints, history

**Buyer-experience stack.** These tools are the shop window for investors + future guests. Already-shipped infrastructure: lqv-walkthrough.pages.dev (live), Three.js viewer, 12 toggleable data layers, 3DGS self-host pipeline (Vast.ai + COLMAP), Cesium 3D viewer. The capture brief at [briefs/wes_capture_brief.md](../../briefs/wes_capture_brief.md) is the protocol Wes needs to follow.

## What we know already (research summary)

- **Deliverable target:** splat pipeline live, waiting for Wes's Google Photos album
- Capture brief: [briefs/wes_capture_brief.md](../../briefs/wes_capture_brief.md)
- Self-host pipeline: Vast.ai 8xH100 rental ($0.35-0.45/hr × 25min/capture = $0.15-0.30/model)
- Luma AI archived (deprecated 2026-06-30)
- 5 walks defined: creek-line, ridge pan, cliff viewpoint, through-trees, building/skeleton

## What needs research

- **Wes's existing Google Photos library** — does he already have photos from past visits?
- **Minimum capture count** — 3 walks might suffice for proof-of-concept
- **Local videographer in PY** — if Wes won't/can't capture, hire someone
- **Capture quality preview tool** — verify before training to avoid wasted GPU time

## Dependencies

_No explicit dependencies captured yet. Likely related to other ideas in this category — review the [INDEX.md](../../INDEX.md)._

## Risks & failure modes

- **Wes never delivers** — this is the highest-risk single dependency
- **Capture quality** — poor captures = poor 3DGS = poor VR
- **Google Photos access** — Wes needs to share with AI Whisperers account
- **Vast.ai rental cost** — $0.35/hr but if training fails and needs re-runs, $5-10 total per capture

## Cost / time estimate

_Estimate pending — see "What needs research" section for named cost sources._

## Done = shipped

**Acceptance criteria (measurable):**

- splat pipeline live, waiting for Wes's Google Photos album
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

**Status:** No explanation.

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
