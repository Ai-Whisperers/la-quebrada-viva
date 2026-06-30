# Cabin Catalog — 30 Cabins, 10 Types

**Source:** Wes's working files (Eco_Resort_Paraguay_Fase1_Financieel_Model.xlsx, Sheet 3 "Units & Build")
**Date:** 2026-06-30
**Status:** Canonical, extracted from Wes's data

---

## Summary

| Metric | Value |
|---|---|
| Total cabins | 30 |
| Type variants | 10 |
| Total build cost | €3,629,050 |
| Average build cost per cabin | €120,968 |
| Average build cost per m² (weighted) | €1,096 |
| Nightly rate range | €75-€420 |
| Average guests per cabin | 3.2 |

---

## Per-Type Detail

### 2p Basic × 3
- **m²:** 40
- **Build cost per unit:** €35,000 (€875/m²)
- **Total for 3 units:** €105,000
- **Night price:** €75
- **Avg guests:** 2
- **Use case:** Entry-level, solo travelers, budget couples

### 2p Boomhut (Treehouse) × 3
- **m²:** 42
- **Build cost per unit:** €53,600 (€1,276/m²)
- **Total for 3 units:** €160,800
- **Night price:** €135
- **Avg guests:** 2
- **Use case:** Novelty-luxury, Instagram-driven bookings

### 2p Beekhuisje (Creek-side) × 2
- **m²:** 60
- **Build cost per unit:** €68,000 (€1,133/m²)
- **Total for 2 units:** €136,000
- **Night price:** €145
- **Avg guests:** 2
- **Use case:** Honeymooners, premium couples (creek-front premium)

### 2p Luxe Spa × 7
- **m²:** 90
- **Build cost per unit:** €136,500 (€1,517/m²)
- **Total for 7 units:** €955,500
- **Night price:** €220
- **Avg guests:** 2
- **Use case:** Top-tier romantic stays, anniversary bookings

### 4p Basic × 2
- **m²:** 90
- **Build cost per unit:** €77,000 (€856/m²)
- **Total for 2 units:** €154,000
- **Night price:** €130
- **Avg guests:** 4
- **Use case:** Small families, friends sharing

### 4p Boomhut × 2
- **m²:** 95
- **Build cost per unit:** €111,750 (€1,176/m²)
- **Total for 2 units:** €223,500
- **Night price:** €190
- **Avg guests:** 4
- **Use case:** Family adventure stays

### 4p Beekhuisje × 2
- **m²:** 105
- **Build cost per unit:** €118,000 (€1,124/m²)
- **Total for 2 units:** €236,000
- **Night price:** €210
- **Avg guests:** 4
- **Use case:** Family creek-stay, premium

### 4p Luxe Spa × 3
- **m²:** 115
- **Build cost per unit:** €171,250 (€1,484/m²)
- **Total for 3 units:** €513,750
- **Night price:** €290
- **Avg guests:** 4
- **Use case:** Top-tier family vacation

### Family Basic Creek × 3
- **m²:** 145
- **Build cost per unit:** €144,500 (€998/m²)
- **Total for 3 units:** €433,500
- **Night price:** €240
- **Avg guests:** 5.5
- **Use case:** Multi-generational families, week-long stays

### Family Luxe Spa × 3
- **m²:** 160
- **Build cost per unit:** €237,000 (€1,481/m²)
- **Total for 3 units:** €711,000
- **Night price:** €420
- **Avg guests:** 5.5
- **Use case:** Top-tier family + special occasions

---

## Build Cost Analysis

### Cost-per-m² Tier

| Tier | Cost/m² € | Cabins | Total cost € |
|---|---|---|---|
| Basic (€875-€998) | under 1,000 | 8 | €692,500 |
| Boomhut/Beekhuisje (€1,124-€1,276) | 1,000-1,300 | 10 | €756,300 |
| Luxe Spa (€1,481-€1,517) | 1,400-1,600 | 12 | €2,180,250 |

**Insight:** Luxe Spa tier is 60% of total cabin build cost, but only 40% of cabin count (12/30). This is **the highest-margin segment** — the 2p Luxe Spa at €220/night × 7 units alone could generate €562K/year at 100% occupancy (impossible in practice, but illustrative).

---

## Inventory Mix Decision Logic

Wes's plan has 6 different styles across 30 cabins. This is intentional:
- Allows repeat guests to return for "new" experience
- Distributes risk across price points
- Matches the LQV rule: "Don't be a single-typology property"

**Mix summary:**
- 2p units: 15 (50% of count)
- 4p units: 9 (30%)
- Family units: 6 (20%)
- Basic style: 8 (27%)
- Boomhut/Beekhuisje: 10 (33%)
- Luxe Spa: 12 (40%)

---

## Construction Approach

Per Wes: "Start with concrete + bamboo, use Paraguayan construction workers (no Balinese needed initially), build in batches of 5 with 6 different styles so guests can return for new experiences."

**Materials strategy (per cabin batch):**
- Foundation: concrete (locally sourced, see materials price doc)
- Walls: concrete + bamboo (hybrid)
- Roof: per Wes's 17-category list (trusses, sheets, insulation, gutters)
- Interior: per Wes's 6 interior finishing categories
- Furniture: per Wes's 8 furniture category (compare PY vs Brazil vs NL auctions)

**See:** `MATERIALS_PRICE_TEMPLATE.md` for the 14-sheet master materials list.

---

## Ivan's LQV Render Pipeline Cross-Reference

The LQV render pipeline (`/root/la-quebrada-viva/lqv/typologies/`) has 13 typology build files created during the 18-final-render sprint (2026-05-2026). These are **concept art**, not a build commitment. Some overlap with Wes's 10-type plan:

| LQV Render File | Overlap with Wes's Plan |
|---|---|
| `bamboo_beton_28.py` | Partial (concrete + bamboo typology) |
| `bamboo_beton_30.py` | Partial |
| `bamboo_boomhut_treehouse.py` | **Matches 2p/4p Boomhut** |
| `bamboo_river_house.py` | **Partial match with Beekhuisje (creek-side)** |
| `bamboo_wigwam_lodge.py` | No direct match |
| `bamboo_curved_roof_villa.py` | Partial match with Luxe Spa |
| `bamboo_container_4pax.py` | No direct match (container not in Wes's 10) |
| `cob.py` | No direct match (cob not in Wes's 10) |
| `bottle_wall.py` | No direct match |
| `clay_terracotta_estate.py` | No direct match |
| `hobbit_house.py` | No direct match |
| `italian_stone_small_v1/v2.py` | No direct match |
| `candle_path.py` | Not a cabin (path amenity) |

**Decision needed:** keep Ivan's render files as concept art (no build commitment) or retire? See `OPEN_DECISIONS.md` §3.

---

## Construction Pricing Cross-Reference

Ivan's NL prices doc has material prices for many of the inputs that go into these cabins:
- Cement (INC CP II-F32 at €0.60/kg ≈ Gs. 4,400)
- Sand (€8.77/m³ delivered)
- Gravel/crushed stone (€17-18.50/tonne)
- Bricks (€62-205/millar)
- Iron rebar (€1.23-1.44/kg)
- Cob house cost benchmark: €120-225/m² (depending on approach)

The 10-type plan costs (€856-€1,517/m²) are **higher** than Ivan's cob benchmark because they include:
- Luxury finishes (Luxe Spa tier)
- Full bathroom/kitchen
- Furniture (sometimes included in the cost/m² figure)
- Site infrastructure allocation (roads, water, electric)

**See:** `docs/research/2026-06-30_construction_prices_paraguay_nl.md` for the full NL pricing reference.

---

## Source

- **File:** `Eco_Resort_Paraguay_Fase1_Financieel_Model.xlsx` Sheet 3 "Units & Build"
- **Caveat:** all build costs are estimates. Actual costs depend on:
  - Final supplier quotes (Ivan's 17-category price research is the input here)
  - FX at time of import (heavy equipment 2nd hand from NL)
  - Weather/disruption overruns (5-15% buffer recommended)
  - Bali craftsmen availability (3 men × 18 months is the plan)
