# Infrastructure Plan — 8 Phases

**Source:** Wes's working files (`Paraguay_Infra_Masterplan_Uitgebreid_NL.xlsx` / `Infra_Masterplan_Compleet_ES.xlsx`)
**Date:** 2026-06-30
**Status:** Scope canonical from Wes, prices NOT YET filled in source template

---

## 8 Phases Overview

| # | Phase | Priority | Est. duration | Critical for Phase 1? |
|---|---|---|---|---|
| 1 | Terrain survey & base | 🔴 | 2-4 weeks | **YES** (before any design) |
| 2 | Raw materials | 🔴 | ongoing | **YES** (batched across build) |
| 3 | Water supply | 🔴 | 4-8 weeks | **YES** (before cabins) |
| 4 | Sewer & water treatment | 🟠 | 4-8 weeks | **YES** (parallel with water) |
| 5 | Electricity | 🔴 | 6-12 weeks | **YES** (ANDE 3-phase upgrade) |
| 6 | Internet | 🟡 | 1-2 weeks | **YES** (Starlink = fast) |
| 7 | Roads & paving | 🟠 | 8-16 weeks | **YES** (access + construction traffic) |
| 8 | Irrigation | 🟢 | 4-8 weeks | Phase 2 (after landscaping) |

**Total Phase 1 infra budget:** ~€405,000 (per `FINANCIAL_MODEL.md` §1 line items for roads/parking/earthworks + water/septic/sewer + electric/internet/camera + landscaping/jungle/paths)

---

## Phase 1 — Terrain Survey & Base

**Tasks:**
- Georeferencing (full property + boundaries)
- Elevation maps (drone or LiDAR)
- **3D terrain model** ← relevant to Ivan's 3DGS pipeline
- Water features mapping (existing streams, ponds, wet zones)
- Groundwater assessment (test wells)
- Soil testing (load-bearing capacity, drainage, contamination)
- Rock layer depth (for foundation design + well drilling)
- Road/utility location planning

**Deliverable:** 3D terrain model + 2D CAD overlays + soil report + water report

**Ivan's 3DGS pipeline relevance:** If Wes captures 5 phone videos + Ivan runs them through the COLMAP/gsplat pipeline, the 3D terrain model from phase 1 can be the **first real artefact** produced by the buyer-experience stack (B01, B04). This kills two birds: validates the 3DGS pipeline + produces the engineering base map.

**Status:** Not yet started. Need:
- Geodesist (PY: 1-2 quotes needed, ~$2-5k)
- Soil lab (PY: SENACSA or similar)
- 3DGS pipeline ready (Ivan)

---

## Phase 2 — Raw Materials (batched across build)

**Tasks:**
- Tierra roja (red soil) sourcing — for cob, foundations, paths
- Fill sand (large volumes for site grading)
- Topsoil (for landscaping)
- River sand (for concrete + plaster)
- Crushed stone (graded 4e/5e/6e)
- Cement (INC CP II-F32 Vallemí = €0.60/kg)
- Concrete (ready-mix vs on-site)
- Rebar (6-25mm)

**Decision:** Per Wes's NL prices doc, ready-mix concrete is €98/m³ vs in-situ (hand-mixed) at €38-48/m³. Break-even ~3 m³ (below = in-situ, above = ready-mix). LQV total foundations ~6 m³ → recommended: in-situ with hired mixer.

**Suppliers to contact:** Inc. cement (INC Vallemí), Mennonite colony bamboo (Loma Plata), local quarry (Caacupé area), aggregate suppliers (Sumerlabs + Clasipar-listed).

**Status:** Pricing partially captured in Ivan's NL prices doc. Need to fill `Paraguay_Infra_Masterplan_Uitgebreid_NL.xlsx` per-line.

---

## Phase 3 — Water Supply

**Tasks:**
- Well drilling (3 depths: 50m / 100m / 150m)
- Pumps (submersible + surface backup)
- Filters (sand / carbon / UV)
- Water storage tanks (5K to 100K liters, multiple units)
- HDPE pipes (distribution network)
- Pressure system + backup

**Water source decision:**
- **Well (drilled):** reliable, controllable, but PY has variable groundwater quality + depth (typically 50-150m)
- **Stream (creek):** free, abundant in wet season, but unreliable in dry + contamination risk
- **Rainwater:** backup only in PY (insufficient as primary)

**Recommendation per Wes's brief:** well primary, creek secondary, rainwater tertiary.

**Cost range:**
- Well drilling 50m: $1,500-3,000
- Well drilling 100m: $3,000-6,000
- Well drilling 150m: $5,000-10,000
- Pump + filtration: $1,500-3,000
- Storage tank 5K L: $400-600
- Storage tank 50K L: $2,000-3,000

**Status:** Critical. Need well driller quotes + hydrogeological survey.

---

## Phase 4 — Sewer & Water Treatment

**Tasks:**
- Pipe network (PVC + beton)
- Inspection pits
- Pumping stations (if gravity insufficient)
- Biodigester (anaerobic)
- Biological treatment (aerobic)
- Wetland / reed field (polishing)
- Water reuse for irrigation (closes the loop)

**Critical design constraint (Wes's "no standing water"):**
- Avoid dengue mosquito habitat
- No open cisterns (per MASTER_BRIEF Rule 10)
- Sewer water must flow continuously to treatment
- Treatment wetland is the safe endpoint

**Cost estimate:** €60,000 (per `FINANCIAL_MODEL.md` §1)

**Status:** Self-executed. Need civil engineer design + permesso ambiental.

---

## Phase 5 — Electricity

**Tasks:**
- ANDE grid connection (3-phase upgrade)
- Transformers (100-400 kVA)
- Backup generator (100-250 kVA diesel)
- Cables (underground or overhead)
- Distribution boards (per cabin + per amenity)
- Lightning protection

**ANDE 3-phase upgrade process:**
- 6-12 weeks to install
- ~$3,000-8,000 depending on distance from existing grid
- Application at local ANDE office (Paraguarí)

**Backup generator:** mandatory for high-end guests (Luxe Spa tier). Power outages in rural PY are common.

**Cost estimate:** €75,000 (per `FINANCIAL_MODEL.md` §1)

**Status:** Critical. Visit ANDE office in Paraguarí + get quote.

---

## Phase 6 — Internet

**Options:**
- **Starlink** (SpaceX): €60/month + €500 equipment. Fast, reliable, 50-200 Mbps. **Best for rural PY.**
- Fiber optic (Tigo/Claro/Personal): only if infrastructure passes the property (rare in rural)
- Local 4G/5G (Tigo/Claro/Personal): variable, ~€30-50/month, often 5-20 Mbps

**Recommendation:** Starlink primary + 4G backup + WiFi mesh across property.

**Status:** Easy. Order Starlink, set up in 1-2 weeks.

---

## Phase 7 — Roads & Paving

**Tasks:**
- Main road (entry → reception)
- Internal roads (cabin to cabin, cabin to amenities)
- Service/maintenance road (for construction, then daily ops)
- Parking (20 cars Phase 1 → 60 ultimate)
- Drainage (culverts, wadis, rainwater basins)
- Paving options:
  - Asphalt (most expensive, most durable)
  - Poured concrete (mid-cost, very durable)
  - Concrete bricks (mid-cost, replaceable)
  - Grass concrete tiles (eco-friendly, less durable)
  - Gravel mats (cheapest, needs maintenance)

**Recommended:** concrete bricks for main + service roads, gravel for back paths. Balance durability, cost, eco-aesthetic.

**Cost estimate:** €80,000 (per `FINANCIAL_MODEL.md` §1) for 8-16 weeks of work

**Status:** Critical for construction access. Must complete before Year-2 build phase.

---

## Phase 8 — Irrigation

**Tasks:**
- Water source (reuse treated wastewater)
- Buffer basin
- HDPE pipes (distribution)
- Drip lines (for plant beds)
- Sprinklers (pop-up for lawn, rotor for large areas, micro for shrubs)
- Pumps
- Automation computer (irrigation controller)
- Sensors (soil moisture, rain shutoff)
- Treated water reuse pipeline (from Phase 4)

**Status:** Phase 2. Can be added Year 2-3 after landscaping is in.

---

## Cross-Reference: Ivan's 3DGS Pipeline + LQV Ideas

Ivan's render pipeline can contribute to multiple phases:
- Phase 1 (terrain model) — from 5 phone videos + ALOS DEM + Sentinel-2
- Phase 2 (visualization of materials placement)
- Phase 3-4 (water + sewer design visualization)
- Buyer/investor experience (VR walkthrough of the planned build)

**LQV idea files that intersect:**
- B01: VR walkthrough before building
- B02: Interactive site-placement tool
- B03: Satellite-driven optimal placement
- B06: LiDAR drone survey vs hi-res satellite
- C04: Ground bores with GPS points (water source planning)
- C05: Water purification (concrete-chemical vs natural wetland)
- C06: Pressurized sewer with pump stations
- I18: Water security audit (drought + contamination)

**See:** `docs/ideas/INDEX.md` for the full catalog.

---

## Open Items for Phase 1 Infra

1. **Get well driller quotes** (3 depths: 50/100/150m) — requires hydro assessment first
2. **Visit ANDE office Paraguarí** — get 3-phase upgrade quote
3. **Civil engineer** — for sewer + water + road design
4. **Soil testing** — load bearing for foundation design
5. **Topographic survey** — drone or geode (Ivan's 3DGS could substitute if Wes captures)
6. **Environmental permit (MADES)** — required for water extraction + wastewater discharge
7. **Municipal permits (Municipalidad de Escobar)** — for any construction
8. **Starlink order** — 1-week delivery
9. **Backup generator quote** — Honda EU22i or industrial diesel
10. **Insurance broker (3 quotes)** — for the completed infrastructure (per Insight #3)
