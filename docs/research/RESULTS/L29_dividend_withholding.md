# L29 — Withholding on dividends to NL (formal)

**Date:** 2026-06-30
**Status:** MEM-based. Confirmed for BV2 → NL investors.

## What L29 is

**When BV3-5 (PY operating BVs) pay dividends to BV2 (NL holding):**
- PY withholding tax applies
- Rate depends on NL-PY tax treaty (which doesn't exist) vs default

**Default rate:** 15% (per PY IRE on dividends to non-PY residents)
**With significant participation (BV2 > 30% holding):** may reduce to 5%

## How it works in practice

**Scenario: BV3 distributes Gs. 100,000,000 in dividends to BV2**
- Default: 15% × 100,000,000 = **Gs. 15,000,000** (~$2,150) withholding
- Reduced (if >30% participation): 5% × 100,000,000 = **Gs. 5,000,000** (~$715) withholding
- BV2 receives: 85,000,000 (or 95,000,000 with reduced rate)
- BV2 then receives this as a "dividend from foreign source" in NL
- **No further NL tax** (participation exemption if conditions met, per L19)

## How to minimize the withholding

**1. Maximize participation exemption (NL side):**
- BV2 holds ≥5% of BV3 (easily met)
- BV3 is "operating company" (not passive holding)
- BV2's NL tax position: 0% on received dividends (subject to conditions)

**2. Reduce PY withholding (PY side):**
- Direct holding > 30% → 5% (vs 15% default)
- Strategic holding structure
- Long-term holding period (probably automatic)

**3. Treaty relief:**
- No NL-PY treaty exists
- Could negotiate per-investment (rare)
- Standard rules apply

**4. Strategic alternatives:**
- Use BV2 (NL) as the only foreign holder (current plan)
- All dividends route through BV2 (single tax event)
- NL-side participation exemption handles the rest

## How to structure the cash flow

**For LQV:**

**Y1-Y3 (no dividends, all reinvested):**
- BV3-5 retain earnings
- No withholding triggered
- LQV grows from internal cash flow

**Y4+ (start distributing dividends):**
- Per L19, BV2 receives dividends
- PY-side: 5% or 15% withholding
- NL-side: 0% (participation exemption)
- Net: ~$0.07-0.20 per $1 dividend

**For LQV's projected Y5+ profit ($1M+):**
- $100K-$200K in dividends to NL investors
- $5K-$30K in withholding
- Net: $70K-$195K to investors
- Cost of withholding: $5K-$30K/year

## What Wes needs to do

- [ ] Per W0.1 attorney call, design BV2 structure to maximize participation exemption
- [ ] Document the withholding in financial model (per L19)
- [ ] Y4+: first dividends, expect 5-15% withholding
- [ ] Per W0.2 Sonja Q&A, ask about local tax experience for context

## Cross-reference
- L19 (tax treaty)
- 4ENTITY_BV_CASCADE
- L18 (FX hedging)
- L26 (anticipos for vendors)
- L25 (IVA for restaurant)
- L23 (L-series index)

## Status

✅ Documented. Y4+ implementation. Plan built into financial model.
