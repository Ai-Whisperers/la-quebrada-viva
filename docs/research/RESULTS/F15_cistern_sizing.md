# F15 — Cistern sizing for rainwater + backup (RV)

**Method:** MEM + general water engineering
**Confidence:** Medium
**Date:** 2026-06-30

## RV water demand

**Per cabin (Fase 1, 5 cabins + reception + restaurant + workers):**

| Use case | Per cabin (liters/day) | 5 cabins | Reception/office | Restaurant | Total L/day |
|---|---:|---:|---:|---:|---:|
| **Drinking + cooking** | 50L | 250 | 50 | 100 | 400 |
| **Showers (2/person × 2 people)** | 80L | 800 | 50 | 200 | 1,050 |
| **Toilets (2 flushes)** | 20L | 200 | 50 | 80 | 330 |
| **Laundry (off-site)** | 0L | 0 | 0 | 0 | 0 |
| **Cleaning** | 5L | 25 | 25 | 50 | 100 |
| **Pool top-off (evap)** | 0L | 0 | 0 | 100 | 100 |
| **Garden/landscaping (dry season)** | 50L | 250 | 50 | 100 | 400 |
| **Subtotal (occupancy @ 100%)** | | | | | **~2,400** |

**Realistic average occupancy (50-70%):** ~1,800L/day
**Peak day (100% occupancy + pool + garden):** ~3,000L/day

**Monthly demand:** 54,000L/month (avg) to 90,000L/month (peak)

## Supply sources (RV-specific)

**1. Rainwater (primary)**
- Escobar average rainfall: ~1,500-1,800 mm/year
- Wet season (Oct-Mar): ~80% of annual rainfall
- Dry season (Apr-Sep): ~20% of annual rainfall

**2. Well water (backup)**
- PY groundwater typically 50-150m deep
- Yield: 5-50 m³/hour typical
- Need: well drilling, pump, treatment

**3. Stream water (emergency)**
- RV has the existing stream per property
- Seasonal — only wet season (Nov-Mar)
- Not suitable for human consumption without treatment
- Could be used for garden/irrigation

**4. ANDE trucked water (last resort)**
- For emergencies only

## Sizing strategy

**Recommended: 3-tier water system**

### Tier 1: Rainwater harvesting (primary)
- **Roof collection** from all 5 cabins + reception
- Cabin roof: 50m² each × 5 = 250m²
- Reception roof: ~100m²
- Restaurant roof: 150m²
- **Total catchment:** ~500m²
- PY rainfall: 1,500mm/year
- Capture efficiency: 80% (gutters + first-flush diverters)
- **Annual harvest: 500m² × 1.5m × 0.8 = 600 m³/year = 1,640 L/day average**

**But uneven distribution:**
- Wet season (6 months): 4,000 L/day capture
- Dry season (6 months): 200 L/day capture
- **This is the problem — we need storage to bridge wet → dry**

### Tier 2: Cistern storage (the critical buffer)

**Sizing principle:** store 6 months of dry season deficit
- Wet season: 4,000 L/day produced, 1,800 L/day consumed → 2,200 L/day surplus
- Dry season: 200 L/day produced, 1,800 L/day consumed → 1,600 L/day deficit
- Per cabin: ~300 L/day deficit
- 5 cabins + reception + restaurant + workers: ~1,800 L/day deficit
- **6 months dry season deficit:** 1,800 × 180 = **324,000 L = 324 m³ = 324,000 L**

**Recommended cistern sizes for RV:**
- **Primary:** 4 × 50,000 L cisterns (200,000 L total) = 50 m³ each, underground
- **Backup:** 2 × 25,000 L cisterns (50,000 L total) = for fire reserves
- **Total water storage: ~250 m³** (covers ~140 days of dry season)

**Per-cabin roof + cabin-specific:** Each cabin also needs a small backup tank (5,000L) for emergency use.

### Tier 3: Well backup (drought year)
- Drill 1 well at the property (50-100m depth)
- Hand pump + electric pump for backup
- Cost: $3,000-6,000 to drill
- Operating: $50-100/month for electricity
- Yield: 5-50 m³/hour (more than enough)

## Cistern options

| Type | Capacity (L) | Cost USD | Pros | Cons |
|---|---:|---:|---|---|
| **Polyethylene (PE) tank, underground** | 5,000-50,000 | $0.20-0.50/L | Cheap, easy install | Can float if not properly anchored |
| **Fiberglass tank** | 5,000-30,000 | $0.50-0.80/L | Lighter, easier to move | UV degrades over time |
| **Concrete cistern (cast-in-place)** | any | $0.30-0.60/L | Permanent, robust, can be any size | Higher initial cost, longer install |
| **Bolted steel tank (galvanized)** | 50,000-500,000 | $0.15-0.40/L | Large volumes, fast install | Corrosion risk over time |
| **Pillow/bladder tank** | 5,000-50,000 | $0.20-0.40/L | Portable, expandable | Less durable |

**For RV recommended: PE underground tanks, 4 × 50,000L.**
- Total: 200,000L
- Cost: $40,000-100,000 (PE tanks are cheap, install is the cost)
- Alternative: 1 × 250,000L concrete cistern, $75,000-150,000 (more permanent)

**With labor + excavation + plumbing:**
- Realistic Phase 1 cost: **$50,000-80,000 for 4 × 50,000L PE tanks installed**
- Or **$80,000-120,000 for 1 × 250,000L concrete cistern installed**

## Backup well (drought-year insurance)

- 1 well at the property (50-100m depth)
- Submersible pump (1.5-2 HP)
- Pressure tank
- Treatment: sand filter + UV (same as pool)
- Cost: $5,000-10,000 installed
- Operating: $50-100/month for electricity
- **This is the "drought year" insurance** (when even the cistern runs out)

## Cost summary for RV water system (Fase 1)

| Component | Cost USD |
|---|---:|
| 4 × 50,000L PE cisterns (installed) | $50,000-80,000 |
| Roof gutters + first-flush diverters (5 cabins) | $5,000-8,000 |
| Plumbing from cistern to cabins (5 + reception) | $8,000-12,000 |
| Backup well (50-100m, pump, treatment) | $5,000-10,000 |
| 5 × 5,000L per-cabin backup tanks | $3,000-5,000 |
| **Total water system (Fase 1)** | **$71,000-115,000** |

For full Phase 1 (30 cabins): ~$200,000-300,000

## Cross-reference
- F14 (INAA water permit) — needed for well + cistern construction
- D6 (Wellness pool) — pool needs separate treatment, but cistern water can supply it
- M08 (Septic) — greywater recycling complements rainwater
- Insurance (W0.7) — fire reserves 50,000L of cistern is a feature

## Status

✅ Done. Sizing complete. Cost estimates range $71K-$115K for Fase 1 water system. Recommendation: 4 × 50,000L PE cisterns + 1 backup well.
