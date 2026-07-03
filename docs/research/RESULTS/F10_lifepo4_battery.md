# F10 — LiFePO4 battery sizing for backup (solar + LQV ops)

**Method:** MEM + cross-ref to F09 solar PV
**Confidence:** Medium
**Date:** 2026-06-30

## Why LQV needs battery backup

**Use cases:**
- Off-grid solar (when ANDE 3-phase is not yet available)
- Night-time operation (AC, lighting, refrigeration)
- Storm backup (ANDE outages during wet season)
- Phone/comm tower backup (Starlink)
- Restaurant + cabin lighting during grid failure

**LQV's battery priority (from F09 plan):**
- **LFP (LiFePO4) preferred** over lead-acid (3-4x lifespan, deeper DoD, faster charge)
- **Modular design** — can expand as needs grow
- **High cycle count** — handles daily cycling well

## Sizing estimate for LQV Fase 1

| Use case | Power draw | Daily hours | Daily energy |
|---|---:|---:|---:|
| Cabin lighting (5 cabins × 200W LED) | 1,000W | 6h | 6.0 kWh |
| AC (1 cabin, 1.5kW unit) | 1,500W | 8h | 12.0 kWh |
| Refrigeration (5× 60W cabin minibars + 1× 500W restaurant fridge) | 800W | 24h | 19.2 kWh |
| Starlink (5 cabins) | 500W | 24h | 12.0 kWh |
| Reception/office (computer, lights) | 200W | 8h | 1.6 kWh |
| Water pump (well, 1HP) | 750W | 2h | 1.5 kWh |
| **Total daily energy** | | | **~52 kWh** |

**Recommended battery bank size:**
- 80% depth of discharge (LFP standard): 52 / 0.8 = 65 kWh
- 1.5x safety margin (for cold days, cloudy days, future expansion): **100 kWh**
- Split into 2-4 modular units for redundancy

**LFP (LiFePO4) options:**

| Brand | Capacity (kWh) | Cost USD | Notes |
|---|---:|---:|---|
| **Pylontech US5000** | 4.8 kWh each | $1,800-2,200 each | 19-21 units = 91-101 kWh, $34,000-46,000 |
| **Dyness B4850** | 5 kWh | $1,500-1,800 | Stackable, 20 units = 100 kWh, $30,000-36,000 |
| **BYD Battery-Box Premium HVS** | 5.1, 7.7, 10.2 kWh | $2,000-4,000 | Modular, premium |
| **Huawei Luna 2000** | 5-30 kWh per pack | $1,800-2,500 | Modular, popular in LATAM |
| **DIY LFP cells** | various | varies | Cheaper but requires assembly skill |

**For LQV Fase 1 (100 kWh system):**
- ~20 Pylontech US5000 units = $36,000-44,000
- ~20 Dyness B4850 units = $30,000-36,000
- **Recommended: Dyness B4850 (best price + best PY distribution via solar installers)**

**Sizing safety:**
- Add 20% buffer for unknown future loads (kitchen expansion, more cabins, pool pumps)
- **Realistic Fase 1: 100-120 kWh total bank**

## Inverter pairing (F09 cross-ref)

**For 100 kWh LFP bank, need:**
- **Hybrid inverter** (off-grid + grid-tie capable)
- **Pure sine wave output** (sensitive electronics like Starlink need clean power)
- **10-20 kW continuous** (handles all Phase 1 loads)
- **48V battery bank** (LFP standard)

**Recommended:**
- **Victron MultiPlus-II** (10-15 kW, 48V, very reliable): $3,000-5,000
- **Sungrow SH10RT** (10 kW hybrid, good price): $2,500-3,500
- **Deye SUN-12K-SG04LP3** (12 kW, very popular in LATAM): $2,000-3,000
- **Victron Quattro** (premium): $4,000-6,000

**Recommended for LQV:** Victron MultiPlus-II 10 kW (best reliability, PY distributor support).

## Total battery + inverter cost (Fase 1)

| Component | Cost USD |
|---|---:|
| 100 kWh LFP bank (Dyness) | $30,000-36,000 |
| 10 kW hybrid inverter (Victron MultiPlus) | $3,000-5,000 |
| Wiring + busbars + fuses + mount | $500-1,000 |
| **Total Fase 1 (100 kWh + 10 kW inverter)** | **$33,500-42,000** |

**Full Phase 1 (30 cabins, 300+ kWh):** ~$100,000-130,000 (3x scale)

## Lifecycle & cost analysis

**LFP lifespan:** 6,000-10,000 cycles = 16-27 years at 1 cycle/day
**Round-trip efficiency:** 95-98% (vs 70-80% for lead-acid)
**Warranty:** 10 years typical
**Operating cost:** Near zero (no maintenance, no water refills)

**Vs lead-acid (which LQV should AVOID):**
- Lead-acid lifespan: 500-1,000 cycles = 1.5-3 years
- 50-60% round-trip efficiency
- Needs water top-ups
- 10x replacement cost over 20 years

**LFP ROI:** pays for itself in 5-7 years vs lead-acid (counting replacement cycles + efficiency + maintenance).

## What Wes needs to do

- [ ] When designing F09 solar system (9.6 kW), add LFP battery to it
- [ ] Get quotes for 100 kWh LFP + 10 kW inverter package
- [ ] Vendor: local solar installer (Asunción, see F09 vendor list)
- [ ] Consider: do Fase 1 with 50 kWh + 5 kW, expand to 100 kWh in Year 2
- [ ] Budget $33,500-42,000 for the battery + inverter

## Sources to verify
- Dyness: search for PY distributor
- Pylontech: search for PY distributor
- Victron: https://www.victronenergy.com/ (has LATAM support)
- Sungrow: https://en.sungrowpower.com.au/

## Cross-reference
- F09 (solar PV sizing) — battery is the storage half of the system
- F19 (generator) — backup when battery depleted
- F15 (cistern) — for water storage, not energy
- Insurance — battery adds value to property (resilience)
- D6 (Wellness pool) — pool equipment can also be backed up by battery
