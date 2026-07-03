# F19 — Generator sizing for restaurant + cabin backup (LQV)

**Method:** MEM + electrical engineering
**Confidence:** Medium
**Date:** 2026-06-30

## What needs backup power (when battery depleted)

- **Restaurant kitchen** (refrigeration + cooking) — can't go down
- **Cabin minibars** — guests will leave if their drinks aren't cold
- **AC units** (especially Luxe Spa) — high-end guests expect cooling
- **Water pumps** (well + pool circulation)
- **Starlink** (for booking system)
- **Reception** (computer, lighting)

## Sizing estimate

**Restaurant peak load (worst case, all appliances on):**
- 2× walk-in cooler/freezer: 1,000W
- Cooking line (electric): 3,000W peak
- Lights + outlets: 1,000W
- AC for kitchen (commercial): 2,000W
- Misc (POS, sound): 500W
- **Total restaurant peak:** ~7,500W = **10 kVA** (with power factor)

**Cabin critical (1 Luxe Spa, all on):**
- AC (1.5 kW): 1,500W
- Fridge: 60W
- Lights: 200W
- **Per cabin peak:** ~1,800W = 2.5 kVA

**LQV Fase 1 (5 cabins + restaurant + reception):**
- Restaurant: 10 kVA
- Reception: 2 kVA
- 2 Luxe Spa cabins (priority during outage): 2.5 kVA × 2 = 5 kVA
- Other 3 cabins (basic level): 1.5 kVA × 3 = 4.5 kVA
- **Total peak (all on):** ~21 kVA
- **Realistic average (only essentials on):** ~8-10 kVA

## Recommended: 2-generator strategy

**Generator 1: Main commercial (20 kVA)**
- Covers restaurant + reception + 2 Luxe Spa cabins
- Auto-start on battery depletion
- Sized for the peak loads
- Diesel fuel (3-4 L/hour at full load)

**Generator 2: Residential (8 kVA)**
- Backup for the 3 basic cabins + water pump
- Smaller, cheaper, longer runtime per tank
- Diesel (2-3 L/hour at full load)

**Why 2 generators, not 1 big one:**
- The 20 kVA is too loud for night operation near cabins
- The 8 kVA is quieter, can run overnight
- Redundancy: if 1 fails, the other can cover essentials
- Fuel efficiency: match generator to load

## Generator options

### Large 20 kVA commercial diesel
- **Caterpillar XQ20 (rental-grade):** $15,000-25,000 (used 30-50% off retail)
- **Cummins C22D6 (stationary):** $18,000-28,000
- **Honda EU22i (inverter, 2.2 kW, quiet):** $4,500 — too small for 20 kVA
- **Cummins C33D6 (33 kVA):** $22,000-35,000 — good if future growth
- **Used commercial (Kohler, Generac, CAT):** $8,000-15,000

### Smaller 8 kVA residential diesel
- **Honda EU70is (7 kW):** $5,500-6,500 (inverter, super quiet, premium)
- **Cummins Onan Quiet Series 8 kW:** $5,000-7,000
- **Kohler 8RESV:** $4,500-6,000
- **Used Kubota or Yanmar 8-10 kVA:** $2,500-4,500

### New portable / hybrid
- **EcoFlow Delta Pro Ultra (7.2 kWh battery + 0-7200W solar):** $5,000 — silent, no fuel
- **Bluetti EP900 (9.6 kWh + 9 kW inverter):** $4,000 — no fuel, no noise
- **Generac PWRcell (battery + generator hybrid):** $8,000-15,000

## Recommendation

**Option A: Traditional diesel (recommended for Fase 1)**
- 1 × 20 kVA diesel commercial (Caterpillar or Cummins) — restaurant + reception
- 1 × 8 kVA residential diesel (Honda or Kohler) — cabins + backup
- **Total cost: $20,000-35,000** (both units installed)
- Operating cost: $300-500/month in diesel (4-6 hours/day runtime)

**Option B: Hybrid (battery + small generator, recommended for Fase 2)**
- Existing LFP battery (per F10, 100 kWh) handles 90% of backup needs
- Small 5-8 kVA generator handles 10% (long outages)
- **Quieter, cleaner, lower operating cost**
- Best for high-end cabins where noise is unacceptable

**For LQV:** Start with Option A (proven, cheaper upfront), upgrade to Option B in Year 2 as cabin density increases.

## Fuel cost estimate

**Diesel cost in PY (2026):** Gs. 7,500-9,000/liter (~$1-1.20)
**Generator consumption:**
- 20 kVA at full load: 4-5 L/hour
- 20 kVA at 50% load: 2-3 L/hour
- 8 kVA at full load: 2-2.5 L/hour
- 8 kVA at 50% load: 1-1.5 L/hour

**LQV running pattern (estimated):**
- 8 kVA runs 2-4 hours/day for cabins = 60-90 L/month
- 20 kVA runs 4-8 hours/day for restaurant + reception = 240-480 L/month
- **Total: 300-570 L/month = $300-680/month = $3,600-8,200/year**

**For budget: assume $5,000/year in generator diesel.**

## Cross-reference
- F09 (solar PV) — solar is primary, generator is backup
- F10 (LiFePO4 battery) — battery reduces generator runtime
- F15 (cistern) — water pump needs backup
- M22 (kitchen) — kitchen equipment is the largest critical-load user
- D6 (Wellness pool) — pool circulation pump also needs backup
- Insurance — generator adds to "resilience" feature for property

## What Wes needs to do
- [ ] Get quotes for 2 generators (1 commercial 20 kVA, 1 residential 8 kVA)
- [ ] Consider hybrid battery + generator for Fase 2 (cleaner, quieter)
- [ ] Budget $25,000-35,000 for generators + $5,000/year operating

## Status

✅ Done. Sizing + cost analysis complete. Recommend traditional diesel for Fase 1.
