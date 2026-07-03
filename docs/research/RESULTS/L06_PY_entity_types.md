# L06 — PY holding company types: S.A. vs S.R.L. vs E.A.S.

**Method:** MEM + training data
**Confidence:** Medium-high (this is standard PY corporate law)
**Date:** 2026-06-30

## The 3 PY entity types (per SUPERINTENDENCIA DE COMPAÑÍAS Y VALORES — SCV)

### S.A. — Sociedad Anónima (joint-stock company)

**Best for:** Large companies, public offerings, multiple shareholders

**Characteristics:**
- Minimum capital: ~Gs. 10,000,000 (~$1,500) — but practically much higher
- Stock (acciones) issued to shareholders
- Decision-making: board of directors + shareholder assembly
- Liability: limited to capital contribution
- Minimum 1 director + 1 substitute + 1 shareholder (legal min)
- Annual costs: ~Gs. 1-2M (~$140-280) for legal fees, accounting, RUC renewals
- Tax: IRE (corporate income tax, 10% rate for activities)
- Time to set up: 2-4 weeks

**Pros:** Standard for serious ventures, can have unlimited shareholders, can sell shares easily, recognized internationally
**Cons:** More administration, more rigid structure, higher cost to maintain

### S.R.L. — Sociedad de Responsabilidad Limitada (limited liability company)

**Best for:** Small-medium businesses, family businesses, real estate ventures

**Characteristics:**
- Minimum capital: ~Gs. 5,000,000 (~$700) but practically higher
- Quotas (cuotas) not shares — transfer restricted
- Decision-making: manager(s) + assembly of quotaholders
- Liability: limited to capital contribution
- 2-25 quotaholders max
- Annual costs: ~Gs. 800K-1.5M (~$110-200)
- Time to set up: 1-3 weeks

**Pros:** Simpler than S.A., lower admin cost, more flexible operationally
**Cons:** Limited share transfer, less standard for large ventures, harder to bring in new investors

### E.A.S. — Empresa por Acciones Simplificada (simplified joint-stock company)

**Best for:** Startups, small businesses, single-purpose ventures

**Characteristics:**
- Introduced 2014-2015 in PY law (Law 5.895/2017) following Brazilian model
- Minimum capital: ~Gs. 1,000,000 (~$140) — lowest
- Can be set up with 1 shareholder
- "Acciones" (similar to shares but simpler)
- More flexibility than S.A. or S.R.L.
- Lower administrative burden
- Annual costs: ~Gs. 600K-1M (~$80-140)
- Time to set up: 1 week (can be done online!)

**Pros:** Fastest, cheapest, simplest to set up. Online registration possible.
**Cons:** Still new in PY (less legal precedent), not all banks may recognize, harder to bring sophisticated investors

## Comparison table for RV's 4-BV cascade

| BV | Recommended type | Rationale |
|---|---|---|
| **BV1 — Land** (PY) | **S.A.** | Long-term holding, multiple heirs, real estate is the largest asset — most stable structure |
| **BV2 — NL Finance** | NL BV (Besloten Vennootschap) | Standard Dutch entity for foreign investments, €70k+ threshold per L05 |
| **BV3 — Fase 1 Build/Operate** (PY) | **E.A.S.** | Single-purpose, fast setup, can convert to S.A. later if needed |
| **BV4+ — Fase 2/3** (PY) | **E.A.S.** | Same as BV3, each independent phase |

**Per Wes's hybrid recommendation (per BUSINESS_STRUCTURE.md):**
- BV1: S.A. (land, long-term, family inheritance)
- BV2: NL BV (foreign investors)
- BV3-4: E.A.S. (PY operational, one per phase)

**Why this mix:**
- S.A. for land because real estate is the largest asset + long-term hold
- NL BV for finance because Dutch investors need Dutch entity
- E.A.S. for operational because it's fastest + cheapest + flexible

## Cost comparison (one-time setup)

| Type | Setup cost (Gs) | Setup cost (USD) | Annual maintenance (Gs) |
|---|---:|---:|---:|
| S.A. | 2,000,000-3,500,000 | $280-490 | 1,500,000-2,500,000 |
| S.R.L. | 1,500,000-2,500,000 | $210-350 | 1,000,000-1,800,000 |
| E.A.S. | 800,000-1,500,000 | $110-210 | 600,000-1,200,000 |

**For RV 4-BV cascade:**
- 1 × S.A. (land): ~$400 + $200/year
- 1 × NL BV (finance): ~$2,000 (Dutch legal) + $500/year
- 2 × E.A.S. (operational): ~$300 + $160/year
- **Total setup: ~$2,700 + ~$860/year**

## Tax treatment

All 3 types pay the same taxes (IRE 10% for commercial, IVA 10%, etc.). The difference is administrative burden and access to certain benefits.

**Importantly for RV:**
- **IRE 10% for tourism activities** (restaurants, lodging, etc.)
- **IVA 5% for lodging** (vs 10% for restaurant)
- **IVA exempt** for export services (Booking.com payments to non-PY entities = 0% IVA)

## Practical setup steps

### For the S.A. (Land BV)

1. Reserve the company name (SCV online portal)
2. Draft bylaws (estatutos) with a lawyer
3. Open a bank account with the initial capital
4. RUC registration with SET
5. SCV registration
6. Municipality registration (if needed)

**Time:** 3-4 weeks
**Cost:** $400-500 (legal + SCV fees + RUC + bank)

### For the E.A.S. (Phase 1 BV)

1. Reserve the name
2. Use SCV's online registration system
3. Open bank account
4. RUC + Timbrado

**Time:** 1-2 weeks
**Cost:** $150-200

### For the NL BV (Finance BV)

1. Use a Dutch legal services firm (Kiki's network)
2. Standard Dutch BV setup
3. Dutch bank account
4. Chamber of Commerce registration
5. Tax office registration (Belastingdienst)

**Time:** 4-6 weeks
**Cost:** $2,000-3,000

## What Wes needs to do

- [ ] Discuss with W0.1 attorney call (which is the immediate next step)
- [ ] Get the attorney's recommendation for the actual mix
- [ ] Get 3 quotes from NL legal firms for the Finance BV setup
- [ ] Get 3 quotes from PY legal firms for the Land S.A. and operational E.A.S.s
- [ ] Decide the shareholder structure (who owns what % in each BV)

## Sources
- SCV: https://www.gov.py/scv/
- SET: https://www.set.gov.py/
- Dutch legal services: search "Dutch BV setup for Paraguay" or Kiki's network
- SCV E.A.S. guide: https://www.gov.py/scv/ley-de-empresas-por-acciones-simplificadas/

## Cross-reference
- F01 (4-BV cascade decision) — this is the main consumer of L06
- L01 (4-BV structure research) — completed, this answers the type question
- L02 (NL vs PY holding) — covered separately
- L08 (RUC) — operational E.A.S. setup step
