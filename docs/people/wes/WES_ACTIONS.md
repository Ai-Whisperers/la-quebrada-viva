## W0.1-W0.9 numbering (ADR 2026-07-06)

Wes-facing docs use **two coexisting numbering schemes**, resolved as follows:

**Canonical (used by `docs/wes/`, `docs/_reconciled/`, `docs/people/decisions/`):**

| # | Action | Status |
|---|---|---|
| W0.1 | NL+PY dual-tax attorney call | New numbering — see existing W0.1 below |
| W0.2 | Sonja questionnaire call | existing W0.2 |
| W0.3 | Anexo I chase to Escribana Peña | existing W0.3 |
| W0.4 | Fase 1 ownership choice | existing W0.4 |
| W0.5 | 5-of-15 materials topics pick | existing W0.5 |
| W0.6 | Project name decision | existing W0.6 |
| W0.7 | Toyota Tundra vs Presio + Anexo I follow-up | existing W0.7 |

**NEW (added 2026-07-06 by Erebus after CONSULT pack):**

| # | Action | Status |
|---|---|---|
| W0.8 | **Insurance broker outreach** | NEW — see W0.5 below (was renumbered, reverted) |
| W0.9 | **Drone LiDAR booking** | NEW — see W0.6 below (was renumbered, reverted) |

**Why the revert:** my 2026-07-06 commit `071a328` renumbered the W0.x labels in this file, which broke ~13 cross-references in `WES_INDEX`, `WES_NEXT_30_DAYS`, `WES_HOW_WE_WORK`, `WES_GLOSSARY`, `OPEN_DECISIONS`, `DECISIONS_LOG`, `CONTACTS`, and `SITE_VISIT_BRIEF`. Reverted to the canonical pre-existing scheme + added the two new actions (insurance + LiDAR) under W0.8/W0.9.

**To find the insurance broker outreach material:** see `../stakeholders/INSURANCE_BROKER_OUTREACH.md` + the W0.5 section below for shortcut.

---

# Wes's Action Checklist — the 5 things this week

**Purpose:** Single page that lists everything only Wes can do, with the action script for each.

**The 5 things this week unblock 15 of 21 P1-blockers** (per WES_TODO.md).

---

## W0.1 — Book NL+PY dual-tax attorney call

**Time:** 1-2 hours
**Cost:** €300-500
**Unblocks:** 10 P1-blockers (L01, L02, L03, L04, L05, L21, L22, L25, L28, L29)

### Steps

1. **Find an attorney** (today)
   - Ask Kiki for NL+PY dual-tax contacts in her Asunción network
   - Alternative: search LinkedIn "PY tax advisor Netherlands"
   - Alternative: AHK Paraguay (German-Argentine-International Chamber of Commerce)
   - **Need:** dual-qualified (NL + PY) OR firm with both NL and PY partners

2. **Send the brief in advance** (1-2 days before call)
   - File: `docs/people/ATTORNEY_BRIEF.md`
   - Include the 4-BV diagram, financial model, research catalogue

3. **Run the 1-2 hour call** (within 7 days)
   - Focus on Q1-Q12 in the brief
   - Capture decisions in real-time

4. **Send notes to Erebus** (same day)
   - 1-page summary of decisions
   - Any specific PY contacts (accountant, despachante, environmental engineer)

5. **Mark W0.1 ✅ in WES_TODO**

---

## W0.2 — Schedule Sonja questionnaire call

**Time:** 1-2 hours with Sonja
**Cost:** Your time
**Unblocks:** 16 P1/P2 items (W01-W19)

### Steps

1. **Schedule the call** (today)
   - Send `docs/people/SONJA_QUESTIONNAIRE.md` in advance
   - Give Sonja 2-3 days to prepare

2. **Run the call** (within 7 days)
   - Use the 16 questions in the file
   - Capture answers

3. **Send answers to Erebus** (same day)
   - Audio file if recorded, or written summary

4. **Mark W0.2 ✅ in WES_TODO**

---

## W0.3 — Pick the project name (5 minutes)

**Time:** 5 minutes decision + 1 day to check domains
**Cost:** $0
**Unblocks:** All of D14 (Cross-cutting brand/naming)

### Candidates

| Name | Source | Wes preference | Domain check |
|---|---|---|---|
| **Riverstone Valley** | Wes brainstorm (audio E) | Wes said "stolen from Yellowstone" + "boom boom boom" | BR02: check RiverstoneValley.com + .com.py |
| **Villa del Cielo** | Wes brainstorm | Spanish, "mooi" | BR03: check |
| **Cielo Azul** | Wes brainstorm | Spanish, "mooi" | BR03: check |
| **Lluvia Dorada** | Wes brainstorm | German place + plant reference | BR03: check |
| **Lluvia de Oro** | Wes brainstorm (variant) | German place + plant reference | BR03: check |
| **Riverstone Valley** | Ivan's working name | Existing brand | Check availability |
| **Eco Jungle Resort Paraguay** | Wes's working files | Descriptive | Check |

### Steps

1. **Pick one** (5 min)
2. **Tell Erebus** (1 message)
3. **Erebus checks domains** (BR02, BR03) — 1 day
4. **Update README.md** with the chosen name
5. **Mark W0.3 ✅ in WES_TODO**

---

## W0.4 — Chase Anexo I of boleto

**Time:** 1 phone call
**Cost:** $0
**Unblocks:** 1 P1-blocker (L07) + general legal completeness

### Context

The Anexo I of the boleto is the technical description of each finca (linderos, rumbos, medidas). Per the boleto, sellers' entrega was due 5 business days after 28-Apr 2026 (~5 May 2026). It's now ~2 months late.

### Steps

1. **Call Escribana Cynthia Andrea Peña Ros** (today)
   - Status of Anexo I?
   - If still missing: get written commitment date
   - If available: arrange pickup or delivery

2. **Log the call in** `docs/people/escribana_status.md`

3. **Mark W0.4 ✅ in WES_TODO**

---

## W0.5 — Insurance broker pre-qualification (NEW 2026-07-06)

> **HG-3 hard gate per `POST_ESCRITURA_NOW.md`.** 82% Atlantic Forest canopy + PY dry season = the biggest financial risk before any construction begins. **No structure goes up without binding fire+storm coverage.**

**Time:** 1-2 hours broker outreach + 4-6 weeks waiting for quotes
**Cost:** €0 (cost is in the policy later); broker outreach itself free
**Unblocks:** HG-3, Phase 1 break-ground, D15 in `OPEN_DECISIONS.md`

**Steps**
1. **Print `../stakeholders/INSURANCE_PROPERTY_DATASHEET.md` as PDF** (do not send via WhatsApp — bulky).
2. **Ask Kiki for 2-3 PY broker contacts** in her Asunción network (Mapfre PY, La Consolidada, Seguros Atlántida).
3. **Find 2-3 international broker contacts** via LinkedIn search "Marsh Brazil commercial", "Aon Argentina risk", "WTW Latin America".
4. **Send the WhatsApp outreach template** (`../stakeholders/WHATSAPP_OUTREACH_TEMPLATE_ES.md` for PY-domestic, `../stakeholders/WHATSAPP_OUTREACH_TEMPLATE_EN.md` for international).
5. **Target 3 quotes within 6 weeks** — fire, storm, general liability.
6. **Mark W0.5 ✅ in WES_TODO** when 3 quotes in hand.
7. Update `docs/research/RESULTS/W07_insurance_quotes.md` with the 3 quotes (Erebus compiles).

**Files to use (this pack):**
- `../stakeholders/INSURANCE_BROKER_OUTREACH.md` — master playbook + 5 broker targets + tiered questions
- `../stakeholders/INSURANCE_PROPERTY_DATASHEET.md` — 2-page datasheet — attach as PDF
- `../stakeholders/WHATSAPP_OUTREACH_TEMPLATE_ES.md` — ES WhatsApp for PY brokers
- `../stakeholders/WHATSAPP_OUTREACH_TEMPLATE_EN.md` — EN WhatsApp for international brokers
- `../../research/RESULTS/PRICE_GAP_MASTER.md` — 95-item price-gap inventory (~40% vendor-priced, ~45% range-only, ~15% blind). Pairs with this outreach — broker quotes fill the gaps.

**Reference:** `docs/research/RESULTS/insurance_fire_bundle.md` (Sprint 0 research, already done) + `docs/research/RESULTS/R01_fire_safety_plan.md`.

---

## W0.6 — Pick the project name (5 minutes)

> **Wes's first instinct was "Riverstone Valley" but he hasn't formally decided.** See `docs/people/wes/PROJECT_NAME_CANDIDATES.md` for 100 candidates + 3 top recommendations.

**Time:** 5 minutes decision + 1 day to check domains
**Cost:** $0
**Unblocks:** All of D14 (Cross-cutting brand/naming)

### Candidates (top 5)

| Name | Source | Wes preference | Domain check |
|---|---|---|---|
| Riverstone Valley | Audio E | Wes's first instinct | BR02: check RiverstoneValley.com + .com.py |
| **Villa del Cielo** | Audio brainstorm | Spanish, "mooi" | BR03: check |
| Cielo Azul | Audio brainstorm | Spanish, "mooi" | BR03: check |
| Lluvia Dorada | Audio brainstorm | German place + plant | BR03: check |
| Lluvia de Oro | Audio brainstorm (variant) | German place + plant | BR03: check |

### Steps

1. **Pick one** (5 min)
2. **Tell Erebus** (1 message) → domain check (BR02/BR03) → 1 day
3. **Erebus renames repo** (atomic rename commit)
4. **Mark W0.6 ✅ in WES_TODO**

---

## W0.7 — Toyota Tundra vs Presio + insurance follow-up

### Tundra vs Presio (existing AI research, finalize the pick)

**Time:** 30 min to review AH01/AH02/AH03
**Cost:** $0
**Unblocks:** Phase 1 mobility decision

**Steps**
1. Read existing research: `docs/research/RESULTS/AH01_hilux_pricing.md`, `AH02_tundra_parts.md`, `AH03_used_vs_new.md`.
2. Decide: **Toyota Hilux SRV 4x4 used** (~$30k landed, parts in PY, jungle-agile) **OR Tundra SR5** (~$50k, more capable but rare in PY).
3. Tell Erebus the choice.

### Insurance follow-up

1. Once W0.5 quotes are in hand (~6 weeks), compare 3 quotes side-by-side.
2. Bind fire + storm (~€8-15k/year) at break-ground; add liability + business interruption at Month 2.
3. Update `POST_ESCRITURA_NOW.md` HG-3 to ✅.

**Mark W0.7 ✅ in WES_TODO** when both decisions (Tundra/Presio + insurance bind) are confirmed.

---

## W0.8 (NEW 2026-07-06) — Call the NL+PY dual-tax attorney

> **HIGHEST-LEVERAGE single action in the project.** Validates the 4-BV cascade + answers 10+ P1-blockers. Use the **1-page summary** at `../stakeholders/ATTORNEY_BRIEF_1PAGE.md` as your printed handout; full 24-question brief stays in the repo.

**Time:** 1-2 hour call (prep + call + 30 min post-call notes)
**Cost:** €300-500
**Unblocks:** 10 P1 legal/tax items (L01, L02, L03, L04, L05, L21, L22, L25, L28, L29)

**Steps**
1. **Find an attorney** — message Kiki for NL+PY dual-tax contacts in her NL + Asunción network. Alternative: LinkedIn search "PY tax advisor Netherlands".
2. **Send `../stakeholders/ATTORNEY_BRIEF_1PAGE.md` + `../stakeholders/ATTORNEY_BRIEF.md` 2-3 days before call** — give attorney time to review.
3. **Run the 1-2 hour call** — lead with the 1-pager; jump to the full brief for deep dives.
4. **Mark W0.8 ✅ in WES_TODO** + send 1-page decision summary to Erebus.

**Files for this:**

| File | Purpose |
|---|---|
| `../stakeholders/ATTORNEY_BRIEF_1PAGE.md` | **Print 2 copies — one for you, one for the attorney** |
| `../stakeholders/ATTORNEY_BRIEF.md` | Full 24-question brief — digital, projector if available |

**Reference:** `docs/_reconciled/OPEN_DECISIONS.md` D1+D9, `BUSINESS_STRUCTURE.md`, `_reconciled/MASTER_BRIEF.md`.

---

## W0.9 (NEW 2026-07-06) — Sonja questionnaire call (clean re-do of old W0.2)

> Merged with old W0.2 to keep Sonja Section together. The OLD W0.2 used to be Sonja (now retired); W0.9 is the canonical name.

**Time:** 1-2 hours with Sonja
**Cost:** $0
**Unblocks:** 16 P1 worker/culture/salary items (W01-W19)

**Steps**
1. Send `docs/people/stakeholders/SONJA_QUESTIONNAIRE.md` to Sonja 2-3 days before call.
2. Schedule 1-2 hour call.
3. Capture 16 answers on the call.
4. Send answers to Erebus (audio file or written summary).
5. **Mark W0.9 ✅ in WES_TODO**.

**Reference:** `docs/people/stakeholders/SONJA_QUESTIONNAIRE.md` (existing, 16 questions).

---

## Summary

| # | Action | Time | Cost | Unblocks |
|---|---|---|---|---|
| W0.1 | Attorney call | 1-2 hr | €300-500 | 10 P1 items |
| W0.2 | (retired — was Sonja) | — | — | (see W0.9) |
| W0.3 | Name decision | 5 min | $0 | All of D14 (see W0.6) |
| W0.4 | Anexo I chase | 1 phone call | $0 | 1 P1 item |
| W0.5 | **Insurance broker outreach** | 1-2 hr + 6 wk | €0 | HG-3 hard gate |
| W0.6 | Project name pick | 5 min | $0 | D14 brand chain |
| W0.7 | Tundra/Presio + insurance follow-up | 30 min | $0 | Phase 1 mobility |
| W0.8 | Attorney call (1-pager) | 1-2 hr | €300-500 | 10 P1 items (superseded W0.1 — pick one) |
| W0.9 | Sonja questionnaire | 1-2 hr | $0 | 16 P1 items (superseded W0.2) |
| **Total** | | **~5 hours + 6 wk wait** | **~€600-1000** | **30+ items unblocked** |

**The 5 hours is still the highest-leverage work.** The 6-week wait on W0.5 (insurance quotes) runs in parallel — start that broker outreach today.

*Maintained by Erebus (AI Whisperers) for Wesley van de Camp.*
*Cross-reference key: W0.1 = W0.8 (attorney); W0.2 retired = W0.9 (Sonja); W0.3 = W0.6 (name); W0.5 split into insurance (now) + LiDAR (now W0.5-B body).*
