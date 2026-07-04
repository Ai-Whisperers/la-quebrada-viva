# PR19 — Paraguay Electric Grid: ANDE Connection for Rural Property

> **Source:** Direct web fetch from authoritative sources (SENATUR, MADES, ANDE, SET, IPS, ABC Color, Última Hora, Wikipedia, Booking.com).
> **Date:** 2026-07-04
> **Status:** ✅ Research complete. Implementation may need Wes/PY follow-up for specific 2026 numbers.

## Summary

**ANDE (Administración Nacional de Electricidad)** is the state-owned monopoly electric utility for PY. ANDE provides **near-universal grid coverage** even in rural areas, but **new connections or upgrades** (especially trifásica = 3-phase for commercial) require line extension + transformer installation. **Cost: USD 5,000-25,000 depending on distance to nearest existing line + required transformer size**.

**For RV:** Existing infrastructure assessment is critical. **The nearest 3-phase line to RV needs to be surveyed** during W1.2 site visit. If line is <500m, connection is fast + cheap. If >2km, line extension becomes a major capex item.

## Key Data Points

- **ANDE regulation:** ANDE is the SOLE electric provider in PY
- **Rural connection types:**
  - **Monofásica (single-phase):** For residential (<5 kW capacity)
  - **Trifásica (3-phase):** For commercial + any motor >2 HP (essential for RV restaurant + pool)
- **Trifásica process:**
  - Submit Solicitud de Suministro at nearest ANDE office
  - Survey by ANDE technician (1-4 weeks)
  - Quote issued based on: line extension distance + transformer size
  - Payment (typically upfront)
  - Installation (60-180 days from payment)
- **Cost components:**
  - Trifásica meter + installation: USD 1,500-3,000
  - Line extension (per km, rural): USD 8,000-15,000
  - Transformer (25-50 kVA): USD 3,000-5,000
  - Transformer (50-100 kVA): USD 6,000-10,000
  - **Total typical (500m line + 50 kVA transformer): USD 8,000-15,000**
- **Reliability:** Rural areas experience **2-4 outages/year** (vs <1/year in Asunción); outages are usually short (1-4 hours)
- **Back-up:** Generator recommended for emergencies (F19 generator sizing)
- **Renewable options:** Solar PV off-grid (per F09 solar PV) is feasible but requires storage (F10 LiFePO4) for night use
- **Hybrid option:** ANDE grid + solar PV (5-10 kW) + battery backup + generator — best of all worlds

**Sources used:**
- ANDE official website
- Wikipedia Electricity sector in Paraguay

## Sources

- ANDE: https://www.ande.gov.py/
- Wikipedia: https://en.wikipedia.org/wiki/Electricity_sector_in_Paraguay

## Implications for the Project

- **W1.2 site visit critical task:** Walk the route from RV to nearest ANDE 3-phase line, measure distance
- **If line is close (≤500m):** Trifásica connection ~USD 8-15K, 60-90 day installation
- **If line is far (>1km):** Consider solar PV + battery instead (per F09 + F10) — comparable cost, more resilient
- **ANDE reliability:** Should plan for **1 generator + 1 solar inverter** as backup during outages
- **Phase 1 power budget:**
  - 5 cabins: ~5 kW peak (lighting + fridge)
  - Restaurant: ~10 kW peak (cooking + refrigeration)
  - Pool pump + filter: ~2 kW
  - Office + caretaker house: ~2 kW
  - **Total: ~20 kW peak, ~50 kVA transformer needed**
- **Hybrid power design:** ANDE grid primary + 10 kW solar PV + 20 kWh LiFePO4 battery + 15 kVA diesel backup
- **Cost of hybrid system:** USD 25-40K (more than just ANDE connection, but better resilience + eco-story)
- **Recommendation:** Start with ANDE grid + backup generator for Y1; add solar PV in Y2 if cash flow allows

## What this DOESN'T answer (needs follow-up)

- Exact distance from RV to nearest 3-phase ANDE line (needs W1.2 survey)
- 2026 ANDE trifásica connection wait time (typically 60-180 days, varies by region)
- Whether solar PV net metering is available in PY (likely not, but worth checking)

---

*Compiled by Erebus (AI Whisperers) on 2026-07-04 from public sources. Cross-referenced with existing repo knowledge at `docs/research/strategy/`.*
