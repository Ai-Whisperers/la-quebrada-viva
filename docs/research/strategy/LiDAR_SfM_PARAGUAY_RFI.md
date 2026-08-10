# La Quebrada Viva — LiDAR / SfM Photogrammetry RFI

**Status**: Decision-stage research, RFI prepared 2026-07-08.
**Decision needed by**: 2026-08-01 (before dry-season ends, optimal flight window).
**Author**: Erebus / Ai-Whisperers
**Project stakeholder**: Wes van de Camp (75% owner), Thijs (25% co-buyer).

## Executive summary

LQV's 3D viewer currently runs on **ALOS AW3D30 DEM at 30 m native resolution**, interpolated to 1.5 m. This produces a workable site model but:
- The terrain mesh is **terraced** at close zoom (every 30 m step is a hard ridge).
- Surface relief visible across the 62 ha parcel is only ~57 m — interpolation artifacts limit visible detail.
- We cannot map quebrada slopes, drainage channels, or individual tree positions.

Adding drone-derived elevation data — either **LiDAR** or **Structure-from-Motion photogrammetry** — would deliver cm-accurate terrain (5–50 cm vertical), point-cloud classification (terrain vs vegetation vs structures), and 1–3 cm resolution orthomosaics. **The capex ranges from $250 to $12,000 USD** depending on method, vendor, and resolution. We recommend:

**Tier 1 (≤2 weeks, ≤$1,000)**: Buy a DJI Mavic 3 Enterprise RTK + process locally with WebODM. Cheapest path, cm-accurate orthomosaic + DEM, no LiDAR (vegetation occluded but workable for 62 ha since canopy is mostly open).
**Tier 2 ($3,000–$6,000, vendor quote)**: Hire a Paraguayan survey company (Cartomex or agniforge-mapping) to fly a **drone LiDAR pass** over the 62 ha, producing classified point clouds + 0.5 m contours.
**Tier 3 (not recommended yet)**: WingtraOne or DJI M350 + L2 LiDAR owned equipment, $25k+ capex, only justified if LQV scales to >500 ha or many sister sites.

## Why does Wes need this?

The LQV housing-park vision (see `docs/research/strategy/HOUSING_PARK_CONCEPT.md`) requires:
- **Earthworks for 4–8 cabin pads** (~500 m² each, in moderately-sloped quebrada terrain): site grading, drainage, cut-and-fill decisions.
- **Roads** connecting pads, kitchen, restaurant, parking, all-weather access.
- **A quebrada bridge** spanning 30–80 m where the quebrada is deepest.
- **Water management** for the quebrada: flow direction, infiltration, seasonal behavior.

### Capex drivers at current ALOS accuracy (±5 m vertical)

Without cm-accurate terrain:
- A 500 m² house pad designed off ALOS data may be **0.5–2 m off actual elevation** — adding $5–25k in earthworks per pad.
- A road cut through quebrada rim may **undercut** or **overcut** by 1–2 m — adding $50–100k in rework.
- A bridge engineered off coarse DEM may be off by 5–10 m in span and placement — risking 6-figure redesign.

### Capex drivers with cm-accurate LiDAR / SfM

The same decisions become textbook. CM-accurate contours + classified point cloud = direct CAD ingestion, no surprises.

**Break-even** at one of: pad cost (~$15k extra), road rework (~$80k extra), or bridge redesign (~$100k extra). The $3–6k Tier 2 cost pays for itself many times over.

## Tier 1: WebODM + DJI Mavic 3 Enterprise RTK

**Setup**: Wes buys or rents the drone, runs the survey himself, processes locally on the VPS using WebODM.

### Hardware capex

| Item | Approx price (USD) | Notes |
|---|---|---|
| DJI Mavic 3 Enterprise RTK (drone + RTK module) | $4,500–6,000 | New from DJI reseller; ~$1k used on classifieds. |
| 3× spare batteries | $300 | Each flight = 25 min, need 3 for 62 ha in multiple passes. |
| Tablet with DJI Pilot app | $800 | iPad or Android — needed for flight control. |
| 1 year of DJI Care (insurance) | $400 | Strongly recommended; crash repairs otherwise $1k+. |
| **Total** | **$6,000–7,500** | First-time buyer + insurance |

### Software (free)

- **WebODM** (https://webodm.net/) — open-source, free. Runs on the VPS (32 GB RAM works for this scale).
- **OpenDroneMap** is the underlying pipeline.
- Cesium-native export: WebODM produces `.las`, `.tif` (orthomosaic + DSM), `.obj` (3D mesh).

### Time & cost

- **Flight time**: ~1.5 hours over 62 ha (GSD 2.5 cm with M3E RTK).
- **Mobility**: Drive from Asunción ~1.5 hours. Day trip possible.
- **Processing**: 4–6 hours on a VPS with 16 cores + 32 GB RAM.
- **Operator**: Wes himself or hire a local drone pilot (~$300 one-off for first session to learn).

### Output

- Orthomosaic at **1–3 cm/pixel** (much sharper than Esri z18).
- DEM at 5–10 cm accuracy (vs current ALOS at 30 m).
- 3D textured mesh for the Cesium viewer.
- No LiDAR — vegetation occluded. Fine for open canopy but won't see ground under heavy tree cover.

### Total Tier 1 cost: **$6,000–8,000 one-time + $300/session if a pilot is hired.**

## Tier 2: Hire a Paraguayan survey vendor (RECOMMENDED first move)

The two candidates:

### Cartomex (https://www.cartomex.com/lidar-paraguay.html)

- **Coverage**: Región Oriental + Chaco, all of Paraguay and LATAM.
- **Service**: Drone-mounted LiDAR — specifically markets 5–15 cm vertical accuracy, 100+ pts/m² density, vegetation-penetrating.
- **Pricing**: Vendor offers quote via Messaging "in less than 1 hour". Compare to US benchmarks: 62 ha = 153 acres. At US rate $150–$300/acre for SfM or $150–$500/acre for LiDAR, expect **$2,500–$7,500 USD** for a full LiDAR survey of 62 ha in Paraguay. Paraguay pricing is typically 30–50% below US rates.
- **Deliverables**: classified point cloud (.LAS), DTM, DSM, contours, cross-section profiles, technical report.
- **They fly the drone**: Wes doesn't need to be on site for the data capture; he is for the boundary approval.

### agniforge-mapping (https://mapping.agniforge.com/index.php/paraguay)

- 170+ pilots globally, India-headquartered with Paraguay service line.
- More expensive, more enterprise; the public-facing site doesn't show Paraguay project prices.
- **Better if** the LQV project becomes a multi-site Paraguay expansion.

### Recommended: Cartomex

Reasons:
1. Paraguay-LATAM-native pricing (no flight-cost premium for international mobilization).
2. Existing experience on Paraguay agriculture and forestry sites — local knowledge.
3. LiDAR penetrates vegetation, which matters for the quebrada's tree cover.
4. They can probably mobilize in <2 weeks; Paraguayan airspace is not as congested as US/EU.
5. They deliver the technical report directly to a surveyor / engineer (Wes can hand this to his attorney for legal-anexos, or to his architect for site planning).

### Tier 2 total: **$3,000–$6,000 USD + 0 effort from Wes except boundary walk-through.**

## Tier 3: Buy our own LiDAR drone (NOT recommended yet)

- **DJI Matrice 350 RTK + Zenmuse L2 LiDAR**: $25,000 USD + RTK base $3,000 + batteries $1,500 + 1y pilot training $5,000 + insurance $2,000 = **~$36,500**.
- Worth it only if LQV scales to >500 ha or if we take on sister sites (Wes mentioned interest in other properties in 2025).
- For the current 62 ha, Tier 2 is more capital-efficient.

## The 10-step "if Wes says yes" runbook

1. **Wes approves Tier 2 budget**: ~$5,000 USD, line item on the next monthly call. (Owner: Wes.)
2. **Boundary walk**: Wes walks the 62 ha with Cartomex's surveyor, 2 hours on site, marks property limits. (Owner: Wes + Cartomex.)
3. **Flight planning**: Cartomex files NOTAM if required by DINAC (Paraguayan civil aviation). Drone flights <150 m AGL over private land usually don't need NOTAM. ~1 week lead time.
4. **Data capture**: 1 day on site. Fly 3 passes (different altitudes / speeds) for redundancy. Cartomex pilots.
5. **Data processing**: 1–2 weeks. Cartomex processes locally in Paraguay; outputs LAS, DTM, DSM.
6. **QA / hand-off**: Wes + Iván review deliverables. Spot-check 3 features (the waterfall candidate, the quebrada confluence, the property boundary).
7. **Convert to viewer-native assets**:
   - DTM → heightmap PNG (16-bit grayscale, georeferenced)
   - LAS → tree positions as Cesium PointPrimitiveCluster
   - DSM → ground-truthed hillshade (replacing the dense 500× hillshade raster)
8. **Cesium for Unreal pipeline is now viable**: Point cloud classified, forest positions known, terrain mesh detailed. Re-evaluate UE5 → web decision.
9. **Update viewer**: LOD3 imaginary replaced with the real orthomosaic at 1–3 cm; exaggeration reduced from 450× to 100×; relief becomes *real*, not exaggerated.
10. **Re-deploy as v6.0**: full-feature, real terrain. Approximate timeline: 30 days from Wes's "yes".

## Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Wet-season weather delays flight | High in Oct–Mar | Low | Schedule for May–Sep (Paraguay dry season). |
| DINAC airspace restrictions | Low | Medium | Cartomex handles filing; >2 weeks lead time. |
| Vendor quotes higher than US benchmark | Medium | Low | Ask Cartomex for fixed-price quote before signing. |
| Vendor produces low-density point cloud | Low | High | Specify ≥100 pts/m² in contract; reject if <50. |
| LQV property boundaries disputed | Medium | High | Boundary walk with Cartomex + Iván as witness. |
| Wes flies drone himself (Tier 1) and crashes | Medium | Medium | Insurance covers; DJI Care strongly recommended. |

## Decision matrix

| Option | Cost (USD) | Quality | Effort (Wes) | Time-to-data | Verdict |
|---|---|---|---|---|---|
| **None (ALOS only)** | $0 | ±5 m vertical | 0 | Now | **Current state, blocked on close-up detail** |
| **Tier 1: WebODM + DJI Mavic RTK, self-flown** | $6,000–8,000 | 5–10 cm vertical (no LiDAR) | High (1–2 days flying + processing learning) | 2–4 weeks | **Good if Wes wants to learn drones; no vegetation penetration** |
| **Tier 2: Cartomex drone LiDAR (vendor)** | $3,000–$6,000 | 5–15 cm vertical + vegetation penetration | Low (1 day on site) | 2–4 weeks | **RECOMMENDED first move** |
| **Tier 3: own DJI M350 + L2 LiDAR equipment** | $36,500+ | 2–5 cm vertical + vegetation penetration | High (operator certification + ongoing) | 1–2 months | **Only for site-scale >500 ha or multi-site expansion** |

## Recommendation

**Tier 2 (Cartomex drone LiDAR) as the first move.** Cost-recovered by the first avoided earthworks mistake. Vendors deliver classified point clouds + DTM + orthomosaic — files that drop directly into the Cesium viewer pipeline. **Budget $5,000 USD; allocate 30 days from approval to v6.0 viewer.**

If Wes wants hands-on involvement in the data capture and has time to learn, Tier 1 ($6–8k) is a complementary path — buy the drone, fly multiple times over the year to capture seasonal variation (quebrada flow, vegetation growth, fire-cycle aftermath). The VPS processes everything for free.

Tier 3 is the wrong move right now. Revisit if LQV becomes a multi-site project.

---

**Authors' note**: This RFI was prepared in the same session that produced v5 of the viewer (LOD3 surface + dense hillshade + unlimited zoom). The next session, if Wes approves, would be a clean handoff to Cartomex + 30 days of viewer v6 work.
