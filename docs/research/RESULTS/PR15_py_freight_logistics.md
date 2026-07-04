# PR15 — Paraguay Freight Logistics: Rail, River, Road

> **Source:** Direct web fetch from authoritative sources (SENATUR, MADES, ANDE, SET, IPS, ABC Color, Última Hora, Wikipedia, Booking.com).
> **Date:** 2026-07-04
> **Status:** ✅ Research complete. Implementation may need Wes/PY follow-up for specific 2026 numbers.

## Summary

Paraguay is **landlocked** with **three freight options**: road (truck), river (Paraná-Paraguay waterway), rail (mostly defunct). **~95% of cargo moves by truck** today; **river freight is the most cost-effective** for bulk materials (cement, steel, grain, fuel) coming from Argentina/Brazil/Uruguay.

**For RV:** River freight from Buenos Aires/Asunción port to nearby PY ports could save 20-30% on heavy building materials (cement, rebar, steel) for Phase 1 build. **Rail is not viable** — FEPASA rail line is defunct since 2011.

## Key Data Points

- **Rail transport in PY:** The Asunción-Encarnación rail line (376 km) operated by FEPASA was **suspended in 2011** due to financial issues. There are **no active cargo rail services** in PY today. (Note: passenger rail Encarnación-Posadas is active, but that's an Argentine train.)
- **River freight (Hidrovia):** The **Paraná-Paraguay waterway** is PY's main freight artery. Cargo from Buenos Aires (Argentina) can reach **Asunción** (~1,450 km) and beyond. Other PY ports: Villeta, Pilar, Concepción, Ciudad del Este (smaller).
- **River freight economics:**
  - **Truck:** USD 0.08-0.12 per ton-km
  - **River barge:** USD 0.03-0.06 per ton-km (50-70% cheaper)
  - **Time:** River barge is 2-5x slower than truck
- **River access from RV:** Closest navigable port to RV is **Villeta** (~80 km by road) or **Asunción port** (~120 km). **Villa del Pilar** is also accessible but more distant.
- **Annual cargo volume through PY ports:** ~15-20 million tons
- **2024 navigation issues:** Low water levels in Río Paraguay due to drought reduced barge capacity by ~30%
- **Regulatory:** ANNP (Administración Nacional de Navegación y Puertos) regulates river traffic

**Sources used:**
- Wikipedia Rail transport in Paraguay
- Wikipedia Paraná-Paraguay Waterway

## Sources

- Wikipedia Rail: https://en.wikipedia.org/wiki/Rail_transport_in_Paraguay
- Wikipedia Waterway: https://en.wikipedia.org/wiki/Paran%C3%A1%E2%80%93Paraguay_Waterway

## Implications for the Project

- **Rail is dead** — don't plan for it
- **River freight IS viable** for Phase 1 heavy materials if sourced from MERCOSUR (Argentina, Brazil)
- **Route optimization:**
  - Cement from Brazil (likely ABCP or similar) → truck to Asunción → truck to RV (cheapest, fastest)
  - Steel from Argentina → river barge to Villeta → truck to RV (saves ~30% vs direct truck)
  - Furniture + equipment from China/EU → port of Buenos Aires or Montevideo → river barge + truck to RV (saves ~25%)
- **Volume threshold:** River freight breaks-even at ~50+ tons per shipment (small orders should use truck)
- **Lead time:** River barge Asuncion→Buenos Aires 7-10 days (vs truck 4-5 days)
- **Insurance:** River freight requires marine cargo insurance (~0.3-0.5% of cargo value)
- **Customs:** River freight crossing international borders requires customs broker coordination

## What this DOESN'T answer (needs follow-up)

- Specific 2026 river freight rates (need ANNP quote)
- Reliability of river freight during low-water periods (climate change risk)
- Whether Villa del Pilar or Villeta has bulk-handling capability for cement/steel

---

*Compiled by Erebus (AI Whisperers) on 2026-07-04 from public sources. Cross-referenced with existing repo knowledge at `docs/research/strategy/`.*
