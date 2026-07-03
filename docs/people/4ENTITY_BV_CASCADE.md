# 4-entity BV cascade (visual diagram + final spec)

**Date:** 2026-06-30
**Status:** Per Wes's plan in audio C + Ivan's LQV draft. Awaiting W0.1 attorney call for canonical validation.

## The 4-BV structure (Wes's words, audio C)

> "vier, vakantiepark, eentje waar de grond in komt te zitten, de eigenaren van de grond, dat blijft dan in principe van ons, dan heb je er één, een financieringsmaatschappij die in verbinding staat met Nederland, van Nederlandse financierders, hier gaat dat wat makkelijker, dan hebben we één die bouwt fase 1 zeg maar, bouw en verhuur van fase 1, en dan hebben we fase, het volgende bedrijf is fase 2, en het volgende bedrijf is fase 3, en die machines koop je eigenlijk met fase 1, en als de fase 1 af is, verkoop je die machines weer naar fase 2, en een eentje erbij, en zo schuift dat mooi op, de eerste investeerders hebben hun geld ook weer van de machines terug"

**Translation:**
- BV1 (Land): Wes + Thijs, long-term hold, equity
- BV2 (Finance): NL, interface for Dutch investors
- BV3 (Fase 1): Build + rent Fase 1
- BV4+ (Fase 2/3): Independent phases, equipment cascade

## The visual diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                      WESLEY + THIJS                               │
│                    (Personal ownership)                            │
└────────────────────────────────────────────────────────────────────┘
                                 │
                                 │ (50-100% ownership)
                                 ▼
        ┌──────────────────────────────────────────────┐
        │   BV1 — LAND (PY — S.A. or E.A.S.)         │
        │   Holds 62 ha parcel                         │
        │   Long-term land equity                      │
        │   Wes + Thijs (personal)                     │
        │   Leases land to BV3, BV4, BV5              │
        └──────────────────────────────────────────────┘
                                 │
                                 │ (Lease payments)
                                 ▼
        ┌──────────────────────────────────────────────┐
        │   BV2 — FINANCE (NL — Besloten             │
        │   Vennootschap)                              │
        │   Holds equity in BV3, BV4, BV5             │
        │   NL investors' interface                    │
        │   Receives dividends from operating BVs       │
        │   Repays NL investors via BV3-5 distributions│
        └──────────────────────────────────────────────┘
                                 │
                                 │ (Equity + shareholder loans)
                                 ▼
        ┌──────────────────────────────────────────────┐
        │   BV3 — FASE 1 BV (PY — E.A.S.)             │
        │   Builds 5 cabins + reception + restaurant  │
        │   Operates Fase 1                           │
        │   Owns Fase 1 equipment (truck, AC, pool)  │
        │   Self-liquidating (10-yr exit)             │
        │   When stable: sells equipment to BV4       │
        └──────────────────────────────────────────────┘
                                 │
                                 │ (Equipment cascade)
                                 ▼
        ┌──────────────────────────────────────────────┐
        │   BV4 — FASE 2 BV (PY — E.A.S.)             │
        │   Builds 10 more cabins                     │
        │   Operates Fase 2                           │
        │   Buys equipment from BV3 at cost-plus      │
        │   (BV3 investors recover machine money)      │
        │   Adds +5 new machines                       │
        └──────────────────────────────────────────────┘
                                 │
                                 │ (Equipment cascade)
                                 ▼
        ┌──────────────────────────────────────────────┐
        │   BV5 — FASE 3 BV (PY — E.A.S.)             │
        │   Builds 15 more cabins                     │
        │   Full amenities (wellness, events)         │
        │   Sonja's 60th weekend preparation         │
        │   Final state at 30 cabins                  │
        └──────────────────────────────────────────────┘
```

## How it works in practice (Wes's "machinepark rouleert")

**Y1 (BV3):**
- BV3 buys equipment for Fase 1 (truck, AC units, pool pump, etc.) = $50K
- BV3 starts operating, generates revenue
- BV3 needs to repay NL investors (via BV2) → distributions
- After 2-3 years, BV3 is stable

**Y2 (BV4 starts):**
- BV4 needs equipment → buys from BV3 at cost-plus ($55K for same equipment)
- BV3 distributes the $55K to BV2 → BV2 distributes to NL investors
- **NL investors recover their machine money first** (key feature)
- BV3 still has its remaining capital + cabin revenue stream

**Y3 (BV5 starts):**
- BV5 buys equipment from BV4 at cost-plus
- BV4 distributes to investors
- All 3 phases stable

**Y4+ (2030 Sonja's 60th):**
- All 3 BVs operational + profitable
- LQV as a brand
- New investors can buy into BV2 (additional capital raise)
- Or BV3-5 can be merged into a single holding for an exit event

## What this means for the money flow

**For NL investors:**
- Invest €X into BV2
- BV2 invests in BV3 (Fase 1)
- BV3 operates, generates profit
- BV2 receives dividends, distributes to NL investors
- When BV4 starts, BV2 receives equipment sale proceeds
- **NL investors recover their machine money within 4-5 years**
- **After that, they're in a profit-only position**

**For Wes + Thijs:**
- Long-term land equity (BV1)
- Active management role (BV3, BV5)
- NL network access (BV2)
- Risk contained per phase

**For the project:**
- Each phase is independently fundable
- Each phase failure doesn't kill the project
- Land equity (BV1) protected from operational debt
- Multiple options for exit (sale of BV3, BV4, BV5 to a hotel chain)

## Why this is structurally better than a single PY entity

**Single PY entity structure (BAD):**
- If Fase 1 fails, investors + founder both lose everything
- Land equity mixed with operational debt
- No clear exit for early investors
- Hard to bring in NL investors (PY entity less familiar)

**4-BV cascade (GOOD):**
- Each phase is independently fundable
- Equipment cascade gives early investors machine money back
- Land equity protected from operational debt
- NL holding makes Dutch investment natural
- Failure contained to one phase

## Cost comparison

| Approach | One-time setup | Annual admin |
|---|---:|---:|
| Single PY S.A. | $400-500 | $200-300 |
| 4-BV cascade (1 S.A. + 1 NL BV + 2 E.A.S.) | $2,500-3,000 (initial) | $500-700 |
| 4-BV cascade (1 S.A. + 1 NL BV + 2 E.A.S. ongoing) | — | $600-800/year |

**$2,000-2,500 extra upfront** for the structural protection of the cascade structure. Pays for itself in the first avoided mistake.

## What needs to happen next (attorney call)

1. ✅ W0.1 attorney call (this week)
2. Confirm 4-BV structure is correct
3. Get 3 quotes for setup costs
4. Decide on the actual entity types (S.A. vs E.A.S.)
5. Set up the shareholder structure (Wes + Thijs + early investors)
6. Establish the equipment-cascade legal mechanism (sale-leaseback vs asset transfer)
7. Coordinate with NL tax advisor for BV2 setup

## Cross-reference
- L01 (4-BV cascade research) — covered
- L02 (NL vs PY holding) — covered
- L03 (5e holding) — covered
- L04 (machinepark legal) — covered
- L06 (PY entity types) — done
- L08 (RUC setup) — done
- L15 (banking) — done
- F-series (build equipment) — informs equipment cascade

## Status

⚠️ Awaiting W0.1 attorney call. Diagram + spec ready. Implementation requires attorney's blessing + Wes's confirmation.
