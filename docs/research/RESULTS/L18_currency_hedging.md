# L18 — Currency hedging for PYG/USD/EUR exposure (W1.1 item)

**Method:** MEM + training data
**Confidence:** Medium
**Date:** 2026-06-30

## LQV's currency exposure

**Three currencies:**
- **EUR** (Wes + Thijs personal, NL investors via BV2)
- **USD** (international OTA payments, Booking.com/Airbnb)
- **PYG** (PY operational costs, suppliers, payroll)

**Exposure flows:**
- **EUR/PYG** (Wes + Thijs to BV1/BV2 + operating BVs) — Wes's main transfer
- **USD/PYG** (OTA revenue to PY) — recurring
- **EUR/USD** (NL investors → BV2, then BV2 → operating BVs) — initial capital
- **PYG/USD** (operational: equipment, materials) — recurring

**Risk:** PYG devaluation against EUR/USD. PY inflation 4-6%/year typically, but PYG can move 10-20% in crisis years.

## Hedging options for LQV

### Option 1: Keep PYG (no hedge, accept risk)
- **Pro:** Simple, no fees
- **Con:** Capital erosion if PYG devalues
- **Best for:** Operations only (e.g. €5K/month payroll)

### Option 2: Hold USD/EUR as buffer (Wes + BV2)
- **Pro:** Easy, no formal hedge
- **Con:** Idle cash loses to inflation
- **Best for:** Operational buffer + capex

### Option 3: Banco Itaú's FX hedging products (PY local)
- Itaú offers currency-linked deposits (CDB in USD or EUR)
- 3-12 month terms
- Yield tied to currency performance
- **Pro:** Local, no cross-border complexity
- **Con:** Limited flexibility

### Option 4: Cross-border hedging (NL brokers)
- Dutch brokers offer FX forward contracts
- BNP Paribas, ING, Rabobank
- **Pro:** Professional, can lock in rates
- **Con:** Min contract size €100K+ (too big for LQV Fase 1)

### Option 5: Natural hedge via operating decisions
- Charge guests in USD/EUR (most European OTA clients are EUR-priced)
- Hold capital in multiple currencies
- Reduces single-currency exposure
- **Pro:** Free, no fees
- **Con:** Requires operational discipline

## Recommendation for LQV

**Fase 1:** Option 5 (natural hedge)
- Price everything in USD/EUR (Booking.com is in these currencies)
- Hold cash in multiple currencies
- Keep 3-6 months operating buffer in USD or EUR
- No formal hedge needed (too small for forwards)

**Fase 2-3:** Consider Option 3 (Itaú CDB) when capital is larger
- More dollars to hedge
- Local instruments
- Maybe 30-50% of net worth in USD CDB

**Y2030+:** If project is wildly successful, full FX hedging needed
- Cross-border forwards
- NL broker partnership
- Currency diversification

## How to mitigate the PYG risk in practice (Fase 1)

1. **Wes transfers EUR → BVs via Wise (per L17)**
2. **BVs hold in mixed currency account:** 50% PYG (operational), 30% USD (buffer), 20% EUR (NL interface)
3. **Guest bookings in EUR/USD via Booking.com (per M01)**
4. **Suppliers paid in PYG** at fair market rate
5. **Quarterly FX review** with the accountant
6. **Capex purchased in USD or EUR** (imported equipment from BR/EU)
7. **Operating expenses in PYG** (local labor, services)

## Cost of NOT hedging

- PYG devaluation 10%/year (bad year) = 10% of operating capital eroded
- LQV has $50-200K in operating capital typically
- Risk: $5-20K/year in lost purchasing power
- **Total over 5 years (compounded):** $30-100K of lost value
- **vs cost of natural hedge (free):** save $30-100K

## What Wes needs to do

- [ ] Discuss with W0.1 attorney call (do they have FX expertise?)
- [ ] Set up mixed-currency account with Banco Itaú (operational BV)
- [ ] Document the FX policy in OPEN_DECISIONS
- [ ] Quarterly FX review with accountant

## Sources
- Banco Itaú FX products: https://www.itau.com.py/
- Wise hedging info: https://wise.com/help/
- Dutch brokers: search "FX hedging Paraguay" or "USD/EUR forward"

## Cross-reference
- L17 (FX transfer costs) — done
- L02 (NL vs PY holding) — affects where to hold EUR vs PYG
- F-series (operational costs) — informed by FX policy
- L15 (banking) — done

## Status

✅ Done. Recommendation: natural hedge (Option 5) for Fase 1. Formal hedging in Fase 2-3.
