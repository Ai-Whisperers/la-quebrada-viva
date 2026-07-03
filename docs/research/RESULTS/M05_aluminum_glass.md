# M05: Ramen/glas — import vs local fabrication
**Method:** MEM + SEARCH (limited PY-specific data online)
**Confidence:** Medium for ranges, low for specific 2026 prices
**Date:** 2026-06-30

## Current state of the PY aluminum/glass market

**Domestic fabrication:**
- **Aluminum profiles (perfiles):** Largely IMPORTED as raw stock from Brazil (Alcoa) and Argentina (Aluar). Local workshops (herrería de aluminio) cut, machine, assemble.
- **Glass (vidrio):** Single-pane float glass mostly imported from Brazil (CeBRACE) or Argentina (VASA). Laminated + tempered = imported or specialty suppliers.
- **Double-glazing (DVH - doble vidriado hermético):** Available in Asunción, supplied by 5-8 local workshops. Premium = imported.

**Top PY suppliers (training data):**
- **Aluar (Argentina) + Alcoa (Brazil)** — raw aluminum profiles, imported via Ciudad del Este
- **Vidrio plano (float):** from CeBRACE (Brazil) or VASA (Argentina)
- **Local workshop chain:** ~20 mid-size carpinterías de aluminio in Asunción + 2-3 in Ciudad del Este + 1-2 in Encarnación
- **Top brands assembled in PY:** Alear (Asunción), Genebre (Spanish parent), FV (Feria de la Vivienda distribution)
- **Cross-border reality:** Many "PY" fabricators actually import finished frames from Brazil/AR and just install

## Estimated prices (2026 ranges, training data)

| Item | Unit | Price range (Gs) | USD equivalent |
|---|---|---:|---:|
| Aluminum window 1.20 × 1.00 m, single-pane | unit | 280,000 - 450,000 | $39-63 |
| Aluminum window 1.20 × 1.00 m, double-pane (DVH) | unit | 450,000 - 750,000 | $63-105 |
| Sliding glass door 2.00 × 2.10 m, single-pane | unit | 850,000 - 1,400,000 | $119-196 |
| Sliding glass door 2.00 × 2.10 m, DVH | unit | 1,400,000 - 2,200,000 | $196-308 |
| Fixed glass wall 3.00 × 2.50 m, single-pane | m² | 380,000 - 550,000 | $53-77 |
| Fixed glass wall, DVH | m² | 580,000 - 850,000 | $81-119 |
| Aluminum frame per lineal meter (incl installation) | ml | 85,000 - 140,000 | $12-20 |
| 6mm single-pane glass | m² | 95,000 - 130,000 | $13-18 |
| 6mm laminated glass | m² | 180,000 - 280,000 | $25-39 |
| DVH (4+12+4mm) | m² | 280,000 - 420,000 | $39-59 |

**Source basis:** Typical PY market 2024-2026 range estimates. **Needs Wes to verify with 2-3 local carpintería quotes.**

## Decision framework: import vs local

**Import (full pre-assembled from BR/AR):**
- Pros: Known quality, faster installation, factory warranty
- Cons: 4-6 week shipping, customs duties (~10-15% CIF), breakage risk in transit, limited local after-sales
- Best for: Premium cabins (Type A Luxe Spa tier) where quality matters

**Local fabricate (PY workshop):**
- Pros: 1-2 week lead time, lower cost (~15-25% less), local warranty, supports PY economy
- Cons: Quality varies, smaller workshops have capacity limits, finish quality lower than factory
- Best for: All other typologies (Type A Basic, Type B, Type C)

**Recommended split for LQV:**
- Type A Luxe Spa (7 units): Import premium frames from Brazil (Aluar) or Spain (Genebre) — focus on finish quality for the premium price
- All other types (23 units): Local Asunción workshops — Alear, FV distributors
- Special: Kitchen + restaurant windows — local (frequent replacement expected)

## Cost estimate for LQV Phase 1 (5 cabins)

- 5 cabins × 8 windows avg × Gs. 350,000 = **Gs. 14M (~ $2,000 USD)** for typical windows
- 5 cabins × 1 sliding door × Gs. 1,000,000 = **Gs. 5M (~ $700 USD)** for sliding doors
- **Total windows + doors Phase 1: ~Gs. 19M ≈ $2,650 USD**

For full 30-cabin Phase 1: **~$16,000 USD** for windows/doors (5.5% of cabin build cost €3.6M ≈ $4M).

## Sources to verify (Wes action)

- **BuscoInfo PY directory:** https://www.buscoinfo.com.py/buscar/aberturas-aluminio/asuncion
- **MercadoLibre PY:** https://listado.mercadolibre.com.py/aberturas-aluminio
- **Direct quotes (Wes):** Get 2-3 quotes from Asunción workshops: Alear, FV (Feria de la Vivienda), Genebre-PY
- **Cross-check:** Aluar Argentina direct quote for premium frames

## Status

⚠️ Partial. Ranges provided, but specific 2026 prices need Wes to get 2-3 local quotes. Item flagged for Sprint 1 verification (W1.1 batch).

## Next

- Wes: visit 1-2 carpinterías in Asunción next PY trip, get written quotes
- Erebus: queue import duty calculator (M22) which covers customs on aluminum/glass imports
