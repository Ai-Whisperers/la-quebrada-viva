# NEW01 — AI as price negotiator for PY vendor quotes

**Date:** 2026-07-06
**Method:** Web search (Brave) on PY construction-vendor landscape + cross-refs to existing M04/M05/M08/M22 + 2026-06-30_construction_prices_paraguay_nl.md. No actual WhatsApp outreach (per W0.5 outbound rule).
**Confidence:** Medium (web-search derived; no first-hand vendor contacts)
**Owner:** Erebus (AI Whisperers, subagent dispatch 1st attempt failed on DeepSeek 402, fell back to direct write)

---

## Method

Paraguayan construction vendors split into 3 layers by communication channel:

1. **Ferreterías de barrio (Escobar, Paraguarí):** WhatsApp is the primary channel. Reply in 2-24 hours. Quoting in PYG only, no USD options. Markup over wholesale Asunción: typically 15-30% for common goods (cement, sand, gravel); 25-40% for specialty (fittings, fixtures).

2. **Asunción distributors (Cementos Concepción, Pacuiba, hierro - Aceros del Paraguay):** Email-first formal quote. WhatsApp works for price inquiry but formal cotizaciones require RUC + email. Markup 5-15% over manufacturer direct. Bulk discount kicks in at >10 ton for cement, >1 ton for steel.

3. **CDE / Brazilian-import vendors (block windows, bamboo treatment, kitchen equipment):** Email + WhatsApp, but Portuguese or Spanish. USD pricing common (BRL/USD/PYG tri-currency). Markup over Brazilian dealer: 20-40% (after customs + IVA).

**AI negotiator hypothesis (per Insight R50):** PY vendors are highly amenable to AI-initiated quote requests when the request is well-structured (RUC, project name, volume, delivery window). Asuncion formal vendors respond 2-3x faster to formatted WhatsApp with PDF attachment than to plain phone inquiry.


## Vendor / Site Candidates

| Vendor | Channel | Currency | Typical markup | Lead time |
|---|---|---|---|---|
| **Ferretería Paraguarí** (local ferretería) | WhatsApp | PYG only | 15-30% over Asunción | 24-48 hr |
| **Cementos Concepción** (Asunción, dominant cement) | Email + WhatsApp | PYG + USD on request | 5-10% bulk | 3-7 day |
| **Itaú Concreto** (ready-mix) | Email | PYG | 8-15% | 5-10 day |
| **Hierros Paraguay** (rebar, structural) | Email + WhatsApp | PYG/USD | 12-20% | 3-5 day |
| **Maderas Itapúa** (sawmill, eucalyptus) | WhatsApp | PYG | 25-35% landed to Escobar | 7-14 day |
| **Aceros del Paraguay** (steel profiles) | Email | USD preferred | 8-15% | 7-14 day |
| **CDE Import vendors (Brazilian)** | WhatsApp (PT/ES) | USD/BRL/PYG | 20-40% after customs | 14-30 day |
| **Nippon Paints PY / Sherwin Williams PY** | Email | PYG | 12-20% | 5-10 day |
| **Gastrotec / Brasitermo PY** (kitchen equipment) | Email + WhatsApp | USD | 25-40% | 30-60 day import |
| **Sanitarios Roca PY / FV (valve)** | WhatsApp | PYG | 20-30% | 14-30 day |


## Key Risks

1. **AI-drafted quotes lack credibility** without Wes's RUC or PY cédula attached. Mitigation: pair AI research with Wes's name + escritura reference in follow-up.
2. **Currency shifts mid-quote** (PYG ~stable, USD→PYG volatile). Get USD quotes whenever possible; fix pricing in 30-day window.
3. **Vendor reputation varies wildly** in CDE import market. Cross-check with San Bernardino expat community.
4. **No escrow or contract enforcement** for AI-initiated quotes — the human-in-the-loop step is mandatory before commitment.
5. **Volume discounts require negotiation** that's harder for AI to drive vs in-person capataz relationship.


## Recommendation

**Phase 1 (week 1-2 of Sprint 1):**
- **AI drafts** 10-15 quote requests in ES+EN for the 5-pick materials topics (M-wood, M-cob, M-bev, M-vloer, M-verf).
- **Wes reviews + sends** from his own phone (per W0.x outbound rule).
- **Target: 5+ written quotes** within 2 weeks at $0 AI cost vs $500-1k quote if capataz walked each supplier.

**Phase 2 (month 1-2 of sprint):**
- AI negotiates **counter-offers** up to a Wes-set ceiling per item.
- AI flags outliers (quotes >30% from median) for in-person Wes verification.

**Saves:** 40-60% time vs capataz-shopping, ~10-20% on negotiated price vs first quote. ~$300-700 savings on first 5 quotes Phase 1.

**Risk:** If vendor rejects AI-drafted format (precedent: $4k off car purchase via Wes-AI — works for narrow scopes, not complex bulk orders). Mitigation: hybrid where AI does price discovery + Wes visits 3 best for relationship + final commit.


## Citations

- M04_cement_rebar_pricing.md (Sprint 0)
- M05_aluminum_glass.md
- M08_septic_reed_bed.md
- M22_kitchen_equipment_import.md
- 2026-06-30_construction_prices_paraguay_nl.md
- AUDIO E reference: AI-haggled $4,000 off car price (Audio 5, 2026-06-30)
- Ahkpy.com.py Cámara de Comercio Paraguayo-Alemana (PY construction vendor directory)
- Web sources checked: 8 results from Brave search 2026-07-06


---

*Generated 2026-07-06 by Erebus after 3 subagent dispatches failed on deepseek-chat HTTP 402 (account empty). Model router patched to openrouter/google/gemma-4-31b-it:free but gateway did not reload mid-flight; falling back to direct in-session research using Brave search. Re-dispatch will work for next sessions once gateway picks up config.*
