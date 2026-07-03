# IR02 — PY macro devaluation scenario

**Date:** 2026-06-30
**Status:** MEM-based. Risk scenario for operational planning.

## What IR02 is

**The risk:** What if PY guaraní devalues significantly against EUR/USD?

**Per L18 (FX hedging) + L19 (no treaty):**
- LQV's operational costs are in PYG
- NL investors receive dividends in EUR via BV2
- 10-30% PYG devaluation in a year would significantly impact LQV

## Scenarios

### Scenario 1: Stable PYG (-2% to +2% per year)
- Status quo, no significant impact
- LQV operations smooth
- Dividends in EUR (BV2 holds) are unaffected
- **Most likely scenario (5-year probability ~50%)**

### Scenario 2: Mild devaluation (5-15% per year)
- Operational costs go up 5-15% in EUR
- Revenue (in PYG) also up
- Net margin compressed by 5-10%
- Investors see lower dividend growth
- **Probability (~20-30%)**

### Scenario 3: Major devaluation (20-40% per year)
- Operational costs spike (PY hyperinflation)
- Revenue also spikes (in PYG) but lags
- Operating margin squeezed
- LQV can't easily pass through to guests (booking lags)
- **Probability (~10-20%) — PY history shows episodic instability**

### Scenario 4: PYG crashes (50%+ per year)
- Hyperinflation scenario
- LQV needs to operate in USD/EUR
- Insurance + regulatory issues
- **Probability (~5-10%) — would force structural change**

## LQV's natural hedges

**1. NL holding structure (per 4ENTITY_BV_CASCADE):**
- BV2 (NL) holds operational capital
- NL investors receive dividends in EUR
- **PY devaluation doesn't affect BV2 or NL investors directly**

**2. PYG/USD balance:**
- LQV's PYG costs (operational) vs PYG revenue (guests)
- If PYG devalues, both go up equally
- Net effect: near zero (assuming same-currency balance)

**3. EUR booking (V04 + M01):**
- 50%+ of bookings can be priced in EUR (European market)
- Reduces PYG dependency for revenue
- **Operational PYG still dominant, but revenue partly EUR**

**4. Inflation-passable to guests:**
- Higher prices each year (matching inflation)
- Guest expectations: 5-10% price increase is normal

**5. Asset diversification:**
- BV1 land value (PY): PYG-denominated, but real value is independent of currency
- BV2 holdings (NL): EUR-denominated, insulated from PYG
- LQV equipment: EUR import values

**6. Operational cost real-time adjustments:**
- Prices updated every 6 months in Cloudbeds
- Wages reviewed annually (with PY inflation)

## What LQV does (if scenarios 2-3 happen)

**1. Per L18: hold 3-6 months operating buffer in USD/EUR:**
- Acts as natural hedge
- Cash not exposed to PYG devaluation during that period
- **Already in plan**

**2. Increase EUR-denominated bookings:**
- Direct EUR pricing for European customers
- Reduces PYG revenue dependency
- **Per V04 + M01: in plan**

**3. Hedge insurance + large expenses in USD/EUR:**
- 3-month buffer for major payments
- Reduces PYG exposure on big-ticket items
- **Already done in W0.7 + W1.2 planning**

**4. Forward contracts (if needed):**
- PY banks + international banks offer FX forward contracts
- 6-12 month horizons
- Cost: 1-3% of contract value
- **Per L18: only if scenarios 2-3 unfold**

**5. Operational restructuring (if scenario 4):**
- Move to USD pricing for everything
- Pay staff in USD
- Operate as foreign-owned hotel
- **Last resort**

## LQV's resilience to devaluation

**Net assessment:**
- LQV's NL holding structure (per 4BV) is the strongest hedge
- Operational PYG/USD balance is partial natural hedge
- Asset real value (land, building) is independent of currency
- Major devaluation would compress margins but not destroy value
- **LQV is more resilient than pure PY operators**

## Probability × impact

| Scenario | Probability | Impact on LQV | Recommended action |
|---|---:|---|---|
| Stable PYG | 50% | None | Continue plan |
| Mild (5-15%/yr) | 25% | 5-10% margin compression | Hold 3-6 month USD buffer |
| Major (20-40%) | 15% | 15-25% margin squeeze | Active FX hedging + EUR pricing |
| Crash (50%+) | 10% | 30-50% margin erosion | Operational restructuring |
| Combined risk | weighted avg: | ~10% impact/year | Multi-layer hedge |

**Annual PYG risk budget for LQV:** $5-10K/year (FX buffer cost)
**This is the cost of insurance against the scenario**

## What Wes needs to do

- [ ] Per L18, hold 3-6 month operating buffer in USD/EUR
- [ ] Per W0.2 Sonja Q, ask about historical PYG experience
- [ ] Per W1.2, test direct EUR pricing with 1-2 European guests
- [ ] Per W0.1, attorney confirms BV2 structure as natural hedge
- [ ] Y2-3: active FX hedging if needed

## Cross-reference
- L18 (FX hedging) - main risk tool
- L19 (no NL-PY tax treaty) - related
- 4ENTITY_BV_CASCADE - structural hedge
- V04 (European market) - EUR revenue source
- LQV's overall resilience

## Status

✅ Risk plan documented. L18 + 4BV structure is the main mitigation.
