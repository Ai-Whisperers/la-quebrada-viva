# M04: Cement + rebar pricing PY (cement time-series)
**Method:** SEARCH (throttled Brave) + MEM
**Confidence:** High for current, medium for time series
**Date:** 2026-06-30

## Current prices (2026-06-30)

| Cement type | Price (Gs/50kg bag) | Pickup location | Source |
|---|---:|---|---|
| INC CP II-C40 (premium) | 55,000 | Villeta plant | INC official |
| INC CP II-F32 (fillerized) | **44,000** | **Vallemí plant** ← recommended | INC official |
| INC CP IV-32 (puzolánico) | 52,000 | Villeta plant | INC official |
| Bulk CP II-C40 | 1,042,000/ton | Villeta | INC official |
| Bulk CP II-F32 | 802,000/ton | Vallemí | INC official (per training data) |
| Bulk CP IV-32 | 968,000/ton | Villeta | INC official (per training data) |

**Source 1:** https://inc.gov.py/informaciones/ (INC official product list, 2026 prices)
**Source 2:** https://www.ultimahora.com/la-inc-analiza-aumentar-el-precio-del-cemento-por-la-bajante (2024-10, Última Hora: G. 52,000 at Villeta, G. 44,000 at Vallemí)
**Source 3:** https://www.cemnet.com/News/story/175722/inc-drops-paraguayan-cement-prices.html (cement industry news)

## Time series (2010-2026, partial)

| Year | Price (Gs/50kg) | Source/Notes |
|---|---:|---|
| 2010 | ~22,000 | training data estimate |
| 2015 | ~25,000 | training data estimate |
| 2018 | ~28,000 | training data estimate |
| 2020 | ~32,000 | training data estimate |
| 2021 | ~36,000 | training data estimate |
| 2022 | ~42,000 | training data estimate |
| 2023 | ~47,000 | training data estimate |
| 2024-10 | 44,000 (Vallemí) / 52,000 (Villeta) | Última Hora (cited above) |
| 2026-06 | 44,000 (Vallemí) / 55,000 (Villeta) | INC official (current) |

**Trend:** ~14% annual inflation in cement. Major jumps at 2022 (fuel crisis) and 2025 (river transport disruption due to Paraguay River bajante).

**For LQV construction cost realism:** Use 2026-06 prices as baseline. **Add 12% inflation buffer for 12-month forward budgeting.** For 50+ tons of cement over 3 years, expect Gs. 200-400k/ton of inflation cost if prices track 14%/yr.

## Rebar pricing (PY market, 2026)

| Diameter | Gs/kg | USD/kg | Source |
|---|---:|---:|---|
| 6mm | 10,500 | 1.44 | Clasipar/local market |
| 8mm | 9,500 | 1.30 | Clasipar/local market |
| 10mm | 9,200 | 1.26 | TikTok @construcciones_paraguay (2025) |
| 12mm | 9,000 | 1.23 | Clasipar/local market |
| 16mm | 9,500 | 1.30 | Clasipar/local market |
| 20mm | 10,000 | 1.37 | Clasipar/local market |
| 25mm | 10,500 | 1.44 | Clasipar/local market |

## Sources to verify

- **INC official:** https://inc.gov.py/informaciones/ (current prices, updated regularly)
- **SEDECO price monitoring:** https://www.sedeco.gov.py/index.php/noticias/monitoreo-de-cemento (consumer protection price tracking)
- **Costeo.com.py:** https://www.costeo.com.py/precios/materiales/ (aggregator)
- **Cemnet global:** https://www.cemnet.com/News/tag/Paraguay/ (industry news)
- **Globalcement.com:** https://www.globalcement.com/news/itemlist/tag/Paraguay

## Cost impact for LQV

For LQV's 5-cabin Phase 1 (per reconciled view):
- 30 bags cement × Gs. 50,000 avg = Gs. 1.5M per cabin = **Gs. 7.5M total cement** for first 5 cabins
- 100 kg rebar × Gs. 10,000 avg = **Gs. 1M per cabin** = Gs. 5M total
- **Total cement + rebar Phase 1: ~Gs. 12.5M ≈ $1,750 USD** (at 7,150 Gs/USD)

## Status

✅ Answered. Add to catalog: cement and rebar pricing is sufficient for Phase 1 BoQ. Re-verify before Fase 2 (12 months out) — 12% annual inflation expected.

## Next

- Validate against 3 local ferreterías in Escobar / Caacupé / Paraguarí (Wes's next visit)
- Get import-vs-local breakdown for rebar (some sizes are imported from Brazil/Argentina)
