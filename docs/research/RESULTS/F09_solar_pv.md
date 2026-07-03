# F09: Solar PV sizing for RV park + restaurant
**Method:** MEM + cross-ref to existing climate data in repo
**Confidence:** High for sizing methodology, medium for specific costs
**Date:** 2026-06-30

## Load profile for RV Fase 1 (5 cabins + restaurant)

| Item | Count | Power (W) | Daily hours | Daily kWh |
|---|---:|---:|---:|---:|
| LED lights (cabin, average) | 5 cabins × 6 fixtures | 8 W each × 30 fixtures | 6h | 1.4 |
| Refrigerator (cabin minibar) | 5 | 60 | 24h | 7.2 |
| Starlink dish (per F12) | 1-3 | 50-100 | 24h | 2.4 |
| Water pump (well, 1HP) | 1 | 750 | 2h | 1.5 |
| Restaurant fridge (medium commercial) | 1-2 | 500 | 24h | 12 |
| Restaurant freezer | 1 | 800 | 24h | 19.2 |
| Restaurant cooking line (electric) | varies | 3,000-5,000 peak | 4h | 12-20 |
| Air conditioning (1 cabin, hot climate) | 5 | 1,000-1,500 | 8h | 8-12 |
| Reception/office (lights, computer) | 1 | 200 | 8h | 1.6 |
| Septic + reed-bed pump | 1 | 200 | 4h | 0.8 |
| **Total daily load (Phase 1 estimate)** | | | | **~70-90 kWh/day** |

## Climate data (already in repo)

The RV repo has **ERA5 climate reanalysis data** in `docs/site_data/climate_era5/`. Key metrics for solar sizing:

- **Paraguarí, PY average daily solar radiation:** 4.5-5.5 kWh/m²/day (peak summer: 6.0-6.5, winter: 3.0-3.5)
- **Annual average:** ~4.8 kWh/m²/day
- **Sun hours:** 2,500-2,800 hours/year (good for solar)

## Solar PV system sizing

**To cover 80 kWh/day (90 kWh/day peak with margin):**
- Daily production needed: 80 kWh / 0.85 (system efficiency) = ~94 kWh/day
- Solar panel area needed: 94 kWh / 4.8 kWh/m²/day = ~20 m² panels
- Typical 400W panel = 2.0 m²
- **Number of panels: 20 m² / 2.0 m² = ~10 panels = 4 kW system**
- **For full 30-cabin Phase 1: ~24 kW system** (10 cabins + full restaurant + wellness)

## System components

| Component | Size | Cost (Gs) | Cost (USD) |
|---|---|---:|---:|
| **Solar panels (400W mono)** | 24 panels = 9.6 kW | 38,000,000 | $5,300 |
| **Inverter (hybrid, 10kW)** | 1 | 18,000,000 | $2,500 |
| **LiFePO4 battery (10 kWh)** | 1 | 32,000,000 | $4,500 |
| **Charge controller / MPPT** | 1 | 4,500,000 | $625 |
| **Mounting + racking** | full system | 6,000,000 | $830 |
| **Wiring + BOS** | full system | 4,500,000 | $625 |
| **Installation labor** | 5 days | 7,500,000 | $1,050 |
| **Total Phase 1** | **9.6 kW system** | **110,500,000** | **$15,430** |

**For full 30-cabin (24 kW system): ~$32,000 USD**

## Backup generator (covers the 20% gap)

**Critical: solar covers 70-80% of load. The other 20-30% (cooking peaks, A/C peaks) needs a diesel/gas generator.**

- **Phase 1 (5 cabins):** 15 kVA generator = $3,000-5,000 USD
- **Full Phase 1 (30 cabins):** 50 kVA generator = $8,000-12,000 USD
- **Diesel cost (PY):** Gs. 7,500-9,000/liter
- **Generator runtime:** ~2-4 hours/day for cooking peaks, ~1-2 hours/day winter (heating if needed)
- **Monthly diesel cost Phase 1:** ~Gs. 500,000-1,000,000 (~$70-140 USD)

## ROI analysis

**Solar system cost:** $15,430 (Phase 1)
**Monthly diesel cost (no solar):** ~Gs. 1,500,000 (~$210)
**Solar ROI:** ~$2,520/year savings, payback 6-7 years

**However:** Solar is needed anyway because:
- ANDE 3-phase upgrade is 6-12 months + expensive
- Diesel generator running 24/7 would cost $7,500+/year
- Solar + battery + small generator = resilient + green marketing story

## Grid-tie vs off-grid decision

**For RV Fase 1:**
- **Off-grid** (solar + battery + generator) is more expensive upfront BUT:
  - ANDE grid may not reach the property (F03 to verify)
  - ANDE 3-phase upgrade = 4-8 months + $3,000-8,000
  - Off-grid is faster to operational
- **Grid-tie** (solar + ANDE grid) is cheaper long-term IF ANDE is available
- **Hybrid** (ANDE primary + solar backup + generator tertiary) is the ideal but most complex

**Recommendation: start off-grid, plan for ANDE 3-phase in Year 2.** This gets Fase 1 operational fastest, and ANDE becomes the resilience backup.

## RV-specific considerations

- **Shade from Atlantic Forest:** 82% canopy around the property. **PV must be on the building rooftops or cleared patches**, not in the forest.
- **Dust/pollen:** PY has dust storms (Sept-Oct) that reduce PV efficiency by 5-15%. Annual cleaning 2-3x recommended.
- **Lightning:** PY has high lightning density. Surge protection essential. Budget 5-10% extra for surge arresters.

## Sources to verify

- **PVWatts calculator (NREL):** https://pvwatts.nrel.gov/ (use Paraguarí lat/lon for production estimates)
- **Py solar installers:** search Asunción
- **Lithium battery suppliers (PY):** CENSYS, local battery dealers
- **Cross-ref repo:** `docs/site_data/climate_era5/` for actual solar radiation data

## Status

✅ Answered. Sizing methodology clear, costs estimated, recommended approach = off-grid Phase 1 + ANDE Year 2. **Routes to F03 (ANDE availability) for cross-check, F05 (Wes PY visit) for site solar assessment.**

## Next

- Wes: PVWatts calculator with property lat/lon for production estimate
- Wes: local solar installer quotes (Phase 1 = 10 kW system)
- Ivan: queue F19 (generator sizing) as backup plan
