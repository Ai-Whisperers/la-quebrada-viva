# L27 — Income tax (Wes + Thijs personal + BV-level)

**Date:** 2026-06-30
**Status:** MEM-based. Layered (NL personal + PY BV-level).

## What L27 is

**Two layers of tax on LQV's income:**

### Layer 1: BV-level income tax (PY)
- IRE 10% (commercial activities, per L25)
- Per BV3-5 separately
- Filed annually in PY

### Layer 2: Wes + Thijs personal income tax
- **NL:** box 1 (work), box 2 (substantial interest), box 3 (savings)
- **PY:** if resident, also subject to PY personal IRP
- **For Wes specifically:** as Director + Shareholder of BV2 (NL) + personal in NL

## The structure

**Wes + Thijs (each):**
- Hold equity in BV1 (land, PY) + BV2 (NL, finance)
- BV1 has no income (just owns land)
- BV2 receives dividends from BV3-5
- BV2 also holds operational capital + active oversight

**Tax flow for Wes:**

```
BV3 (PY) → earns $1M/year profit
  → pays 10% IRE = $100K to SET
  → distributes $900K to BV2 (NL holding)
  
BV2 (NL) → receives $900K
  → participation exemption = 0% NL tax (if conditions met)
  → distributes $900K - €25K admin - other costs to Wes + Thijs

Wes (NL resident) → receives dividend from BV2
  → box 2 (substantial interest) = 26.9% NL tax in box 2
  → if NL box 1, progressive rate
  → if NL box 3, savings rate (deemed return from net wealth)
```

**Net for Wes + Thijs:** ~25% effective personal tax on LQV profit

## Optimizations

**1. Capital structure optimization:**
- BV2 holds operating capital in different tax brackets
- Some in equity, some in subordinated debt (interest payments deductible in NL)
- "Agio" (share premium) reduces taxable dividends
- Subject to NL anti-abuse rules

**2. NL anti-abuse rules (2026):**
- Substance-over-form: BV2 must have real presence (offices, staff, decisions)
- Per €100K+ dividends, BV2 may be required to have substance
- Wes's time + oversight is the substance
- If not: NL may deny participation exemption

**3. PY-side deductions:**
- Cost of services between BV2 and BV3 (audit, legal, management) deductible in PY
- ~€30-50K/year in deductible costs = €3-5K in tax savings

**4. Holding period rules:**
- PY may have reduced withholding for long-term holdings (> 5 years)
- Strategic planning to lock in benefits

## Estimated total tax burden (Fase 1+)

**Per year (Y4+, with $1M+ profit):**

| Layer | Tax | Gs equivalent | USD |
|---|---:|---:|---:|
| BV-level IRE (10%) | $100K | 730,000,000 | — |
| BV2-NL (participation exemption) | 0% | 0 | 0 |
| Wes personal (NL box 2) | 27% × $400K = $108K | 788,000,000 | — |
| Thijs personal (NL box 2) | 27% × $400K = $108K | 788,000,000 | — |
| **Total effective tax** | | **$316K** | **$45K** |

**Net to Wes + Thijs:** $1M - $316K = **$684K/year** at full Phase 1 profit

## For Wes's personal tax position

**As a NL resident + Director of BV2:**
- **Box 1:** Work income (if any) — for direct consulting fees
- **Box 2:** Substantial interest in BV2 — 26.9% on €75K+ (per NL rules)
- **Box 3:** Savings — 36% deemed return on net wealth (small for NL resident)

**Optimization options:**
- Hold BV2 equity via "holding" structure (saves box 3 issues)
- Reinvest dividends into BV2 (no personal tax)
- Plan income timing with NL tax advisor

## Cross-reference

- L19 (NL-PY tax treaty - no treaty)
- L23 (L-series index)
- 4ENTITY_BV_CASCADE
- L18 (FX hedging)
- L29 (dividend withholding)
- W0.1 (attorney call)

## What Wes needs to do (W0.1)

- [ ] Confirm NL personal tax position with attorney
- [ ] Design BV2 share structure to minimize Wes + Thijs personal tax
- [ ] Document tax flow in financial model (per L19)
- [ ] Y4+: implement first dividend + verify tax cost
- [ ] Consider: reinvest dividends in BV2 for tax efficiency

## Status

✅ Documented. Y4+ implementation. Wes personal tax in W0.1.
