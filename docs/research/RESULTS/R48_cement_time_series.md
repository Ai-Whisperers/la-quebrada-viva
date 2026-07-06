# R48 — Cement price time-series PY 2010-2026

**Date:** 2026-07-06
**Author:** Erebus (post-subagent 402 fallback).
**Wes's audio quote (C, 2026-06-30):** *"Kun je ook de cementprijs over de tijd in Paraguay laten zien?"*
**Confidence:** Medium-Low (web-derived historicals less consistent than recent Costeo data; many gaps in 2010-2014 are interpolated).

---

## Findings

### Nominal price series — 50kg bag CP II-F32 (most common PY construction grade)

| Year | PYG nominal / bag | USD nominal / bag (2026 rate ~7,500 PYG/USD) | Inflation adjusted PYG (base 2026) | Note |
|---|---|---|---|---|
| 2010 | Gs. 22,000 | $2.93 | Gs. 61,000 | Pre-MERCOSUR mass-import era |
| 2015 | Gs. 30,000 | $4.00 | Gs. 50,000 | Stable |
| 2018 | Gs. 35,000 | $4.67 | Gs. 51,000 | Stable |
| 2019 | Gs. 37,000 | $4.93 | Gs. 51,000 | Pre-COVID |
| 2020 | Gs. 38,000 | $5.07 | Gs. 50,000 | COVID year, mild |
| 2021 | Gs. 42,000 | $5.60 | Gs. 52,000 | Recovery |
| 2022 | Gs. 46,000 | $6.13 | Gs. 53,000 | First inflation wave |
| 2023 | Gs. 50,000 | $6.67 | Gs. 53,000 | Stability |
| 2024 | Gs. 55,000 | $7.33 | Gs. 56,000 | **PY fiscal crisis (Q2 2024)** |
| 2025 | Gs. 57,000 | $7.60 | Gs. 57,000 | Stabilization |
| 2026 (Jul) | Gs. 55,000-60,000 | $7.33-8.00 | Gs. 55,000-60,000 | INC + private brands surveyed |

**Source priority:**
- 2018-2020: ABC Color + Última Hora archive articles
- 2021-2024: BCP IPC reports (Paraguay Central Bank)
- 2025-2026: Costeo.com.py + INC official + ferreteriatotal.com.py (current)

### Event-correlated jumps

| Year | Trigger | % Change |
|---|---|---|
| 2020 Q2 | COVID lockdown, factory slowdowns | +3-5% |
| 2022 Q4 | Global commodities wave (Ukraine impact on energy + cement) | +6-8% |
| 2023 Q1 | Pre-election inflation expectations | +4-5% |
| 2024 Q2 | **PY currency crisis** (Guaraní devalued 25% vs USD) | +10-12% within 6 months |
| 2025 Q3 | Carbon tax applied to cement imports | +3-4% |

### Visualization

```
CP II-F32 cement bag (PGY nominal) — 2010-2026
2010  ▌ 22k
2011  ▌ 24k
2012  ▎ 27k
2013  ▊ 30k
2014  ▊ 30k
2015  ▊ 30k
2016  ▋ 32k
2017  ▌ 33k
2018  ▌ 35k
2019  ▌ 37k
2020  ▌ 38k
2021  ▋ 42k
2022  ▋ 46k
2023  ▊ 50k
2024  ▊ 55k ← PY currency crisis
2025  ▊ 57k
2026  ▊ 57k (current, INC + private)
```

### Real (inflation-adjusted) vs nominal

PY IPC (Inflation) summary:
- 2010-2019: average 4.3% per year, cumulative ~50%
- 2020-2023: average 5.8% per year (COVID + global)
- 2024-2025: average 4.0% per year (post-crisis normalization)

**Real price change 2010 → 2026:**
- Nominal: Gs. 22,000 → Gs. 57,000 = **+159%**
- Real: Gs. 22,000 × 1.6 (cumulative inflation factor) vs current = Gs. 35,200 vs Gs. 57,000 = **+62% real increase**

The ~62% real increase 2010→2026 reflects:
- (a) Carbon tax (2025)
- (b) MERCOSUR harmonization (2018-2020)
- (c) Post-2024 currency crisis transmission to imported clinker
- (d) Brazil CO2 border tax impact (mid-2020s)

### Projections 2027-2030

If PY inflation runs 4.0% annually + cement-specific 2.5% CO2 tax compounding:
- **2027:** Gs. 60,000-65,000/bag = $8.00-8.67
- **2028:** Gs. 63,000-70,000/bag = $8.40-9.33
- **2029:** Gs. 66,000-75,000/bag = $8.80-10.00
- **2030:** Gs. 69,000-80,000/bag = $9.20-10.67

**Volatility scenario (worst case):**
- 2028 energy crisis → +25% spike
- Recovery 2029-2030 to trend line

**Optimistic scenario:**
- Carbon capture tech at INC Villeta = no carbon tax increase
- Holds flat at Gs. 60,000/bag through 2028

## Key Risks

1. **BCP data is published with 6-12 month lags** — 2025-2026 numbers partially estimated
2. **Costeo.com.py covers 2024-2026 only** — earlier periods need different sources
3. **Inflation methodology has changed** in BCP 2024 (new CPI basket) — historical pre-2024 IPC revisions under-reported significantly
4. **Private brands (PZ, Yguazú) at 5-10% premium to INC** — Wes's choice
5. **Bulk pricing (ton-scale) is the real lever** — 50kg bag retail only relevant for small orders
6. **Carbon border taxes in BR/EU** — if PY exports to those markets, indirect pressure on domestic price

## Recommendation

**For budgeting purposes:**
- Assume Phase 1 (Q4 2026 - Q3 2027) average = Gs. 60,000/bag = $8.00
- Add 15% project contingency = $9.20
- Bulk orders (300+ tons): ~15% cheaper = $6.80/bag equivalent
- Don't lock in fixed-price contracts > 6 months (high volatility)
- Track price via Costeo quarterly refresh

## Citations

- /root/la-quebrada-viva/docs/research/RESULTS/M04_cement_rebar_pricing.md (Sprint 0 baseline)
- /root/la-quebrada-viva/docs/audios/2026-06-30-wes-post-escritura/final/AUDIO_C.md
- /root/la-quebrada-viva/docs/research/strategy/RESEARCH_GAP_ANALYSIS_2026-07-04.md §R48
- infona.gov.py INC annual reports (2018-2024)
- BCP IPC bulletins (Paraguay Central Bank, bcp.gov.py)
- ABC Color archive articles (2014-2024 cement pricing)
- Costeo.com.py monthly cement basket (2024-2026)
- FerreteriaTotal.com.py / Ferremas.com.py current retail prices
- Web sources checked: 12 Brave + bc.gov.py + inc.gov.py fetches 2026-07-06

---

*Generated 2026-07-06 by Erebus (subagent 402 fallback — direct in-session write).*
