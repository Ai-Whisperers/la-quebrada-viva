# Research Execution Tracker

**Date:** 2026-06-30
**Status:** Live tracker. Updates with every researched item.

## Method routing

Every research item gets routed to one of these methods. The method determines whether the work is in this turn, this week, or queued for a human.

| Method | When to use | Speed | Cost | Limitations |
|---|---|---|---|---|
| **MEM** (training data) | Fact I can answer from training | Instant | $0 | My knowledge has a Jan 2026 cutoff. PY prices and statutes may have changed |
| **FETCH** (direct URL) | Known canonical source URL (Costeo, INC, SENATUR) | 1-2 sec | $0 | Requires I know the URL |
| **SEARCH** (Brave) | General market research, current prices, vendor discovery | Throttled to 1/sec | Brave quota (2000/mo free) | Rate-limit risk — backoff on 429 |
| **HUMAN-L** (Local attorney) | NL+PY tax/legal questions | 1-2 hr call | €300-500/hr | Blocked on attorney booking |
| **HUMAN-S** (Sonja) | Cultural, worker, price questions | 1-2 hr call | Wes's time | Blocked on Sonja booking |
| **HUMAN-W** (Wes PY visit) | Site-only items (LiDAR, ANDE office, road check) | 1-2 weeks | Trip cost | Blocked on next visit |
| **HUMAN-H** (Human in PY) | Site-only items Wes can delegate | Per-visit | Per-task | Same as Wes |

## Method legend in the per-item table

- **MEM** ✅ = answered from training data, written to RESULTS/
- **FETCH** ✅ = fetched from known URL, written to RESULTS/
- **SEARCH** ✅ = Brave search succeeded, written to RESULTS/
- **HUMAN-L** ⏳ = queued for attorney
- **HUMAN-S** ⏳ = queued for Sonja
- **HUMAN-W** ⏳ = queued for Wes's next PY visit
- **HUMAN-H** ⏳ = queued for human-in-PY
- ❌ = skipped (deferred to backlog)

## Execution table

(populated below as items complete)

## Routing decisions per item

The 128 research items are routed as follows:

### Route MEM (training knowledge, ~40 items)

These are facts I can answer from training data with high confidence. Each gets a one-page RESULTS file with the answer, source, and confidence level.

- L05 — NL BV > IB threshold €70k (Belastingdienst, confirmed)
- L06 — PY S.A. vs S.R.L. vs E.A.S. (PY commercial code)
- L11 — IRE / IRP basics (PY tax)
- L12 — IMAGRO rural property tax (PY tax)
- L21 — SENATUR vacation rental regs (PY tourism law)
- L23 — IVA on platform bookings (PY tax)
- M01-M28 (most material pricing, can be cross-referenced with existing NL prices doc)
- I01-I06 (insurance types, basic PY insurance market)
- W01-W08 (typical PY worker wage bands, cross-ref with Costeo + Mercer)
- F01 — Ipoh-Karai railroad (historical knowledge)
- ... (continue routing for all 128)

### Route FETCH (direct URL, ~30 items)

These need a specific known URL. Can be fetched with urllib.

- M04 — Cement price: INC + globalcement.com
- M05 — Windows/glass: Aluar (Argentine supplier) + local ferreteria sites
- M22 — Kitchen equipment: import duty calculator, ANDE customs
- F11 — Cell coverage: Tigo/Personal/Claro coverage maps
- F12 — Starlink: starlink.com/py
- F09 — Solar sizing: PVWatts calculator + NREL data
- L14 — Bancard/Pagopar: their official sites
- L15 — Banks: Banco Itaú, Ueno, Familiar PY sites
- L16 — Tigo Money, Personal Pay: operator sites
- L17 — Wise/Revolut: their fees pages
- ... (continue)

### Route SEARCH (Brave throttled, ~25 items)

These need a search query. Throttled to 1 query/sec. Backoff on 429. Give up after 3 attempts.

- Most of D5 (site experience) — wedding venues, family venues in PY
- Most of D6 (VR) — Cesium ion, virtual tour platforms
- D8 (Auto) — current Tundra/Presio prices
- D9 (Market) — European air routes to ASU
- D10 (Food) — German chefs in PY
- D11 (Forest) — eco-certifications
- D12 (Site data) — drone LiDAR providers in PY
- D13 (Partnerships) — San Bernardino hotels, German community
- D14 (Cross-cutting) — naming/brand

### Route HUMAN-L (Local attorney, 24 items, 1 call)

One 1-2 hour call with NL+PY dual-tax attorney answers:

- L01, L02, L03, L04 (4-BV cascade + machinepark + tax)
- L05 (€70k threshold — confirm)
- L07-L13 (permits, taxes, registrations)
- L14-L17 (banking + payments) — partly confirmable by attorney
- L18-L20 (FX hedging, tax treaty, MERCOSUR)
- L21-L22 (vacation rental + insurance)
- L23-L33 (remaining legal items)

**Total: 24 items, 1 call.**

### Route HUMAN-S (Sonja, 16 items, 1 call)

One 1-2 hour call with Sonja answers:

- W01-W08 (salary bands for 7 worker roles)
- W09-W14 (aguinaldo, vacaciones, dependiente/independiente, sub-contractor registry, kopen vs huren)
- W15-W19 (hospitality training, specialist hiring, staff transport, Kuikopee forester)
- F06-F07 (ANDE-related cultural questions if Sonja knows)
- X09 (childcare norms)

**Total: 16 items, 1 call.**

### Route HUMAN-W (Wes PY visit, 7 items)

When Wes is in PY next:

- F03 (ANDE 3-phase upgrade quote)
- F05 (road conditions)
- F06 (ANDE grid capacity)
- F07 (ANDE pole + transformer)
- SD01-SD02 (drone LiDAR survey)
- PA10 (Kuikopee forester meeting)
- W17 (staff transport)

**Total: 7 items, 1 trip.**

### Route HUMAN-H (Human in PY delegated, ~10 items)

Wes's contacts in PY (Kiki, ANDE, local farmers):

- F08 (ANDE power quote)
- F13 (water well drillers)
- F14 (INAA stream permit)
- F18 (ANDE office local contacts)
- ... (some of the operational items)

## Total routing breakdown

| Method | Items | Time | This turn? |
|---|---:|---|---|
| MEM | ~40 | Instant | Yes |
| FETCH | ~30 | 1-2 min/item | Yes |
| SEARCH | ~25 | 1-10 min/item (throttled) | Yes, throttled |
| HUMAN-L | 24 | 1 call | Queued |
| HUMAN-S | 16 | 1 call | Queued |
| HUMAN-W | 7 | 1 trip | Queued |
| HUMAN-H | ~10 | varies | Queued |
| **Total** | **~152*** | — | — |

*Sum > 128 because some items can be researched multiple ways.

## Status

| Sprint | Total | MEM | FETCH | SEARCH | HUMAN | Done |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 21 | 0 | 0 | 0 | 0 | 0 |
| 1 | 35 | 0 | 0 | 0 | 0 | 0 |
| 2 | 36 | 0 | 0 | 0 | 0 | 0 |
| 3 | 36 | 0 | 0 | 0 | 0 | 0 |
| **Total** | **128** | **0** | **0** | **0** | **0** | **0** |

(Update as items complete.)
