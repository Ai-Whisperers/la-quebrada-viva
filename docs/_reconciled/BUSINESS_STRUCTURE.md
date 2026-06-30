# Business Structure — 4-Entity BV vs Founder-Controlled

**Sources:**
- Wes's `invesment center.docx` (founder-controlled + 3-5 passive investors)
- Ivan's LQV catalog `F01` (4-entity BV cascade)
- LQV repo: `escritura-2026-06-27` (Wesley + Thijs 75/25, legal owners)

**Date:** 2026-06-30
**Status:** OPEN — both drafts preserved, decision owed by Wes + (eventual) accountant

---

## 1. The Escritura-Fact Baseline

**Wesley + Thijs 75/25** are the **legal owners** of the 62-ha parcel as of escritura `0081129` (signed 2026-06-27, frozen at the `escritura-2026-06-27` Git tag). This is **not in dispute**. Both business structure drafts assume this as the starting point.

**What's open:** what legal structure sits **on top of** the escritura ownership for the operational Phase 1 buildout + investor capital.

---

## 2. Wes's "Founder-Controlled" Model (from `invesment center.docx`)

**Core principle:** you (founder) keep absolute decision control. 3-5 investors get capital + co-ownership but **cannot remove you or take over the company**.

**Capital strategy:**
- Raise capital at 10-11% (preferred return to investors)
- Lend at 15-30% to other projects (interest arbitrage margin = 5-15%)
- Sweet spots: real estate financing (15-20%, secured) + project loans (18-25%)

**Paraguay interest rate context (from `invesment center.docx`):**
| Sector | Rate % |
|---|---|
| Mortgage (bank) | 9-14% |
| Project development | 15-30% |
| Auto loans | 12-30% |
| Personal | 20-60% |
| Business/factoring | 18-35% |
| Agriculture/land | 10-25% |

**Warning from Wes:** "Don't lend too cheap (10% in, 12% out = bankruptcy at first problem)."

**Implied structure:**
- Single operational entity (PY S.A. or S.R.L.)
- 3-5 passive investors (NL + DE expat community + friends/family)
- Wesley + Thijs retain >50% control
- Investors get preferred return + co-ownership stake (minority)

**Pros:**
- Simple to set up
- One entity to manage
- Direct control for founder
- No cross-border tax complexity

**Cons:**
- All risk in one entity
- If Phase 1 fails, investors + founder both lose
- NL investors may be wary of single PY entity (jurisdiction risk)

---

## 3. Ivan's "4-Entity BV Cascade" (from LQV catalog F01)

**4 entities:**

1. **Land BV (PY)** — owns 62 ha parcel
   - Stays with Wesley + Thijs personally
   - Ground income (lease payments from operational entities) stays in their pocket
   - Pure land holding, no operational risk

2. **Finance BV (NL)** — interface to Dutch investors
   - PY finance is easy locally
   - NL investors need a Dutch-facing entity to wire money into
   - Tax-optimized for NL-Dutch investors (participation exemption, etc.)

3. **Phase 1 BV (PY)** — build + rent Phase 1 (first 3-6 typologies)
   - Self-liquidating
   - Receives equipment + initial capital from Finance BV
   - Returns revenue to Finance BV as debt service + dividend

4. **Phase 2 BV + Phase 3 BV (PY)** — later phases
   - **Equipment cascade:** when Phase 1 is done, sell machines to Phase 2 BV at cost-plus
   - Phase 1 investors recover their machine money first in any phase
   - Each phase BV is independent (failure of Phase 2 doesn't kill Phase 1)

**Pros:**
- Structural answer to 80% of project risk
- Equipment cascade = asset-backed operating business
- Land equity isolated from operational debt (can be re-collateralized)
- Phase independence = lower investor risk
- NL hook makes Dutch investment easier

**Cons:**
- 4 entities to manage (legal, accounting, admin)
- Cross-border tax complexity
- More expensive setup (4× legal fees)
- Equipment cascade accounting is non-trivial

---

## 4. Side-by-Side Comparison

| Aspect | Founder-controlled | 4-Entity BV |
|---|---|---|
| Number of entities | 1 | 4 |
| Setup cost | ~€500-1,500 | ~€3,000-6,000 |
| Annual accounting | 1 entity | 4 entities |
| NL tax optimization | Limited | Strong (participation exemption) |
| Founder control | Strong (single entity, majority) | Strong (land BV separate, control via shareholder agreement) |
| Investor risk | Higher (one entity) | Lower (phase isolation + land equity separate) |
| Phase independence | No | Yes |
| Equipment cascade | Manual | Natural (formal mechanism) |
| Time to first booking | 2-3 months | 4-6 months |
| Complexity for Wes | Low | Medium-high |
| Recommended advisor | PY accountant (S.A./S.R.L.) | NL+PY dual-tax accountant |

---

## 5. Hybrid Option (worth considering)

A **third option** that neither draft fully covers:

- **Land BV (PY, Wes+Thijs)** — same as Ivan's option
- **Operational S.A. (PY)** — single entity that builds + operates
- **NL holding company** — owns the operational S.A. + provides the Dutch-facing investment interface

This gives Wes the simplicity of one operational entity + the NL hook + the land equity protection. Equipment cascade becomes a **manual process** (invoice between entities at cost-plus) rather than a formal mechanism.

**Setup cost:** ~€1,500-3,000
**Annual accounting:** 2-3 entities
**NL tax optimization:** Strong
**Founder control:** Strong

**This is the Erebus recommendation** if Wes wants the BV-cascade benefits without the 4-entity complexity.

---

## 6. Decision Criteria (the questions to ask)

When Wes + the accountant sit down to decide, the binding constraints are:

1. **Who is investing?** (NL only? DE? Mixed?)
2. **How much per investor?** (€50k ticket? €200k ticket?)
3. **What's the expected hold period?** (5 years? 10? Indefinite?)
4. **Is Wes planning to do other projects?** (the `top 15 inverstering plannen.xlsx` suggests yes)
5. **What's Wes's appetite for admin overhead?** (1 entity vs 3-4)
6. **What's Thijs's preference?** (he's 25% partner; needs to sign off)
7. **Tax residency** — where does Wes spend most of his year? NL? PY? Split?
8. **Exit strategy** — is the goal long-term hold, or sell to a hotel chain in 10 years?

The answers to these 8 questions will point to one of the three options (founder-controlled, 4-entity, or hybrid).

---

## 7. Action Plan (Wes)

1. **Identify a NL+PY dual-tax accountant** — ask Kiki's network (Kiki has contacts in Asunción)
2. **Book a 1-hour intro call** — bring the financial model + this comparison doc
3. **Walk through 8 decision criteria** (above) with the accountant
4. **Get the accountant's recommendation** — they'll have seen many similar structures
5. **Document the final structure** in a new file: `BUSINESS_STRUCTURE_FINAL.md`
6. **Update the LQV catalog F01** to reflect the decision

**Cost:** €500-2,000 for the accountant intro + structure recommendation.

---

## 8. Action Plan (Erebus)

1. **Erebus drafts a 1-page summary** of the 3 options + the 8 decision criteria (Wes brings this to the accountant)
2. **Erebus updates LQV catalog F01** to reflect the 3-option framing
3. **Erebus monitors the decision** — once locked, update all related docs (FINANCIAL_MODEL, OPEN_DECISIONS, etc.)

---

## 9. Source

- **Wes's draft:** `invesment center.docx` (founder-controlled + interest arbitrage)
- **Ivan's draft:** LQV catalog `F01_4-entity_bv_cascade_(land_py_+_finance_nl_+_phase_.md` (12-section format)
- **LQV context:** `escritura-2026-06-27` tag, `0081129` commit, partnership = Wes + Thijs 75/25
- **Erebus third option:** this document (hybrid)
