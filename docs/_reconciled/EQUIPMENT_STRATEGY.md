# Equipment Strategy

**Source:** Wes's working files (`Machines_Masterplan_NL_aangepast_import.xlsx`)
**Date:** 2026-06-30
**Status:** Strategy canonical, prices being filled per-item

---

## Decision Framework

| Equipment Type | Strategy | Rationale |
|---|---|---|
| **Heavy equipment** (excavators, cranes, loaders) | **Import 2nd hand from NL** | 50-70% savings vs new |
| **Agricultural equipment** (tractors, dump trucks) | **Buy new in PY** | PY market competitive, no import advantage |
| **Standard power tools** | **Mix: rent locally for short bursts, buy for long-term** | Optimize cash flow |
| **Specialty tools** (3D scanners, LiDAR, drone) | **Buy or rent depending on use frequency** | Higher unit cost, lower volume |
| **Vehicles** (site trucks, buggies, quads) | **Mix: buy used 2nd hand + rent for peak** | Avoid over-capitalizing |
| **Office equipment** (computers, network) | **Buy new, standard models** | Long-tail, no import advantage |

---

## Heavy Equipment (Import 2nd hand NL) — Pricing Comparison

| Machine | 2nd hand NL import € | New NL € | New PY € (est) | Savings vs new |
|---|---|---|---|---|
| Mini excavator 1.5t | **16,000** | 30,000 | ~40,000 | 47-60% |
| Mini excavator 3t | **18,000** | 55,000 | ~70,000 | 67-74% |
| Crawler crane 8t | **35,000** | 135,000 | n/a | 74% |
| Crawler crane 20t | **60,000** | 260,000 | n/a | 77% |
| Mobile crane 12t | **45,000** | 200,000 | n/a | 78% |
| Wheel loader 3-5t | **20,000** | 70,000 | ~85,000 | 71-76% |

**Recommendation:** Heavy equipment → import 2nd hand from NL.

**Logistics:**
- Source: used equipment dealers in NL (e.g. ebay-kleinanzeigen, machinery trader sites)
- Transport: container shipping Rotterdam → Buenos Aires → land transport to PY
- Import tax: ~30-40% (depends on age, condition, type)
- Lead time: 6-10 weeks (door to door)
- Customs broker: needed in PY (€1-3k fee)

**See:** `Machines_Masterplan_NL_aangepast_import.xlsx` for the full comparison tool with all 10 categories.

---

## Agricultural Equipment (Buy new in PY)

| Item | Why buy in PY | Est. cost € |
|---|---|---|
| Tractor 80-120hp | PY market is competitive; parts available locally | 35,000-50,000 |
| Dump truck | Standard model, PY dealers competitive | 30,000-50,000 |
| Flatbed trailer | PY-built common | 18,000-25,000 |
| Water tanker (truck-mounted) | PY-built for agricultural use | 15,000-25,000 |
| Concrete mixer (truck) | Local rental available, buy only if heavy use | 25,000-40,000 |

**Suppliers:** John Deere PY, AGROFÉRTIL, Grupo Guerrero, Ciabay (Asunción)

---

## Specialty Tools (3DGS + Drone + LiDAR)

This is where Ivan's existing pipeline intersects with Wes's equipment plan:

| Tool | Use | Source | Cost € |
|---|---|---|---|
| DJI Mavic 3 Pro drone | Aerial photography, 4K video for 3DGS | Ivan's existing | owned |
| DJI L1/L2 LiDAR (optional) | Sub-meter terrain accuracy for infra planning | Buy or rent | 8,000-15,000 buy, 1,200-2,000 rent |
| COLMAP (open source) | 3D reconstruction from photos | Free | 0 |
| gsplat (open source) | 3DGS training | Free | 0 |
| Vast.ai GPU rental | 3DGS training compute | Ivan's account | 0.35-0.45/hour |
| R2 storage (Cloudflare) | 3DGS models + renders | Ivan's account | 0.023/GB/mo |

**See:** Ivan's LQV catalog idea `B06_lidar_drone_survey_vs_hi-res_satellite_decision.md` for the satellite ($200) vs LiDAR ($1,200) decision.

---

## Small Machines (Power Tools)

| Category | Strategy | Est. range € |
|---|---|---|
| Power drills, saws, sanders | Buy (mid-range, not Bosch Pro) | 1,000-3,000 set |
| Concrete mixer (portable) | Rent for first build, buy if doing 3+ | 500-1,500 buy, 50-100/day rent |
| Generators (portable) | Buy 2 (backup redundancy) | 1,500-3,000 each |
| Air compressors | Buy 1 | 500-1,500 |
| Pressure washers | Buy 1-2 | 200-500 each |
| Welding equipment | Buy (mig + stick) | 1,000-2,500 |

**See:** `Machines_Masterplan_NL_aangepast_import.xlsx` for the full 10-category breakdown with rental rates per day/week/month.

---

## Hand Tools

Per Wes's 17-category list (category 16):
- Buy in PY (locally available, no import advantage)
- Sourcing: easy, walk into any Ferreteria
- Budget: €2,000-5,000 for the full Phase 1 site

---

## Rental vs Buy Decision (for short-term need)

If equipment is needed for less than 3 months, **rent**. If more than 6 months, **buy**. Between, compare specific quotes.

| Equipment | Daily rent € | Weekly € | Monthly € | Buy new € | Buy 2nd hand € | Break-even (months) |
|---|---|---|---|---|---|---|
| Mini excavator 3t | 80-150 | 400-700 | 1,200-2,500 | 55,000 | 18,000 | 7-15 |
| Concrete mixer (portable) | 30-50 | 100-200 | 300-500 | 1,000 | 400 | 1-2 |
| Generator 5kVA | 25-40 | 100-150 | 250-400 | 1,500 | 600 | 2-3 |
| Welder (industrial) | 30-50 | 120-200 | 300-500 | 2,000 | 800 | 2-3 |

**For Phase 1 first year (5 cabins):** rent most equipment. Buy only the 2-3 items used daily.

---

## Source

- **File:** `Machines_Masterplan_NL_aangepast_import.xlsx` (10 categories: F9 heavy equipment, F10-F18 lighter categories)
- **Companion file:** `Maquinaria_Proyecto_ES.xlsx` (Spanish version, same structure)
- **PDF versions:** `Machines_Masterplan_NL (1).pdf`
- **Decision flow:** see Wes's `hooft lijstr van prijzen uitzoeken.docx` (17-category priority list)

**Status:** Strategy locked. Per-item prices need to be filled (some done, some pending).
