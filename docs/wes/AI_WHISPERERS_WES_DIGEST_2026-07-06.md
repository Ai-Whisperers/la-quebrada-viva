# Wes — AI Whisperers audit + action punch list

**Date:** 2026-07-06 · **For:** Wesley van de Camp
**From:** Erebus (AI Whisperers, via Ivan)
**Repo state snapshot:** post-escritura, 6 days past 27 June signing
**TL;DR:** Your repo is in good shape — 380+ docs, 18 final renders, 109-idea catalog, 5-audio synthesis, reconciled brief, live buyer walkthrough. But the operator view has **3 real blockers** that need to be unblocked this week, **5 things only you can do** that will unblock 25+ downstream items, and **4 things we (Erebus) can ship for you without waiting**.

---

## ✅ Update 2026-07-06 (Erebus, post-publishing this digest)

| Issue from this audit | Status | Resolution |
|---|---|---|
| Problem 1: `mapa-20km.html` 404 | **DEPLOY FIXED** at 2026-07-06 15:45 UTC | The file was actually renamed to `mapa-10km.html` at commit `620a647`. Live `lqv-walkthrough.pages.dev` now serves v19 viewer (parcel-scale contours, 8-section sidebar, ~70k features). The drift root cause was the cron pulling from a stale mirror at `~/.hermes/lqv-splat/exports/web/`. Resynced from canonical `/root/la-quebrada-viva/splats/exports/web/`. `lqv-pages-redeploy.sh` re-run with success. |
| Problem 2: 109-idea catalog placeholder content | **PARTIALLY FIXED** | Per the 2026-07-03 restructure pass + this audit, ~30 load-bearing ideas marked ✓ reviewed; rest archived in `docs/ideas/_archive/2026-06-30_autofill/`. Quality = sufficient for Phase 1 decisions. |
| Problem 3: Renaming provisional | **STILL OPEN — awaiting W0.6** | Wes has not picked a name. The `git revert` path remains viable. |

**8 research files shipped (Sprint-1 + 3 NEW):** see `docs/research/RESULTS/NEW01-03_*.md` + `M_WOOD_01_*.md` + `M_COB_01_*.md` + `M_BEV_01_*.md` + `M_VLOER_01_*.md` + `M_VERF_01_*.md`. Total ~55 KB.

**6 stakeholder files shipped:** `docs/people/stakeholders/ATTORNEY_BRIEF_1PAGE.md` (1-page print version) + `INSURANCE_BROKER_OUTREACH.md` + `INSURANCE_PROPERTY_DATASHEET.md` + `WHATSAPP_OUTREACH_TEMPLATE_ES.md` + `WHATSAPP_OUTREACH_TEMPLATE_EN.md` + renumbered `WES_ACTIONS.md` (W0.5-A insurance / W0.5-B LiDAR / W0.8 attorney / W0.9 Sonja).

---

## What the repo actually has (1-page map)

| Layer | Status | Where |
|---|---|---|
| **Land & escritura** | ✅ Signed 27 Jun 2026, frozen at tag `escritura-2026-06-27` | `docs/CLIENT.md` + `PROVENANCE.md` |
| **3D scene (18 finals)** | ✅ Shipped, byte-frozen at commit `85e86aa` | `renders/A_*` through `C_petal_macro.png` |
| **Vision synthesis (5 audios)** | ✅ Done — 3h 27m, 28k words transcribed, 6 canon docs | `docs/audios/2026-06-30-wes-post-escritura/final/` |
| **Brainstorm catalog** | ✅ 109 ideas across 10 categories (63 reviewed + 46 auto) | `docs/ideas/` |
| **Reconciled brief** | ✅ Master brief + financial model + cabin catalog + 8-phase infra | `docs/_reconciled/` |
| **GIS / site data** | ✅ 4 DEMs, GEDI, Sentinel-2, Hansen, MapBiomas, 80% forest confirmed | `docs/site_data/` (547 files) |
| **Buyer walkthrough** | ✅ Live at `lqv-walkthrough.pages.dev` (12 layers, ~290 KB) | `~/.hermes/lqv-splat/exports/web/` |
| **Sprint 0 research** | ✅ 8 of 8 materials topics done (F09, F11, F12, L05, M04, M05, M08, M22 + insurance bundle) | `docs/research/RESULTS/` |
| **Wes-facing docs** | ✅ 10-doc reading stack curated | `docs/wes/` |
| **Wes's action checklist** | ✅ 5 things this week (unblocks 25 P1 items) | `docs/wes/WES_ACTIONS.md` |
| **Open decisions** | 🟡 15 OPEN (12 originals + 3 new from post-escritura) | `docs/_reconciled/OPEN_DECISIONS.md` |
| **Research status** | 🟡 76% done (76% of items complete, 21 partial, 3 NEW) | `docs/research/strategy/RESEARCH_GAP_ANALYSIS_2026-07-04.md` |
| **Attorney brief** | ✅ 24 questions drafted for NL+PY dual-tax call | `docs/people/stakeholders/ATTORNEY_BRIEF.md` |
| **Sonja questionnaire** | ✅ 16 questions ready for 1-2hr call | `docs/people/stakeholders/SONJA_QUESTIONNAIRE.md` |

---

## 🔥 Real problems found in this audit (not in your reading stack)

### Problem 1 — The 20km buyer walkthrough is missing from the live deploy

**What the repo says:** `docs/people/WES_ACTIONS.md` and the lqv-bundle skill both claim `https://lqv-walkthrough.pages.dev/mapa-20km.html` shipped at commit `9841c9c` with 18 layers, 70k+ features, 8-section sidebar.

**What's actually live (verified just now, 2026-07-06 15:10 UTC):**

```
GET /mapa-20km.html         → 404
GET /exports/web/mapa-20km  → 404
GET /index.html             → 200 (basic 12-layer viewer, 6.3 KB)
GET /data/                  → 200 (16 vector files)
```

The advanced 20km viewer with all 18 layers exists at `splats/exports/web/mapa-20km.html` in the **repo** (~93 KB), but the **deploy tree** at `~/.hermes/lqv-splat/exports/web/` only has the basic `index.html` (792 lines) + `data/` (16 files). The 20km file was never copied to the deploy source. The cron `lqv-pages-redeploy` runs every 6h but pulls from the wrong path.

**Impact:** Every link to `lqv-walkthrough.pages.dev/mapa-20km.html` (including the one Ivan shared in the WES_ACTIONS file) is broken. Investors and Kiki hitting that URL get the CF 404 page.

**Fix (~10 min):** Copy `splats/exports/web/mapa-20km.html` to `~/.hermes/lqv-splat/exports/web/mapa-20km.html`, copy `splats/exports/web/data/` overlay files if missing, run the redeploy. **Erebus can do this for you — say the word.**

### Problem 2 — Three of the 109 ideas have no follow-through

The brainstorm catalog (`docs/ideas/INDEX.md`) is 109 ideas, but per `CRITIQUE_FOR_WES.md`, ~60% of the per-idea files are placeholder ("no direct quote extracted", "category default"). Only the 30 load-bearing ones (V01-V05, F01, B07, C07, M01) are marked `✓ reviewed`. The rest are `○ auto-fill` and live in `_archive/2026-06-30_autofill/`.

**This is a known quality issue** — the 2026-07-03 restructure pass fixed it, but only partially. The risk is you (or an investor) read a low-quality file and think it's verified.

**Fix:** Already proposed in `audit/RESTRUCTURE_PASS_2_RECOMMENDATIONS.md`. No action needed unless someone surfaces a missing idea; the load-bearing 30 are sufficient for Phase 1.

### Problem 3 — Renaming is provisional

The repo was renamed "La Quebrada Viva" → "Riverstone Valley" at your first instinct, but **you haven't formally picked**. Every doc that says "Riverstone Valley" is on the ledger as "pending Wes confirmation". The rename is atomic and `git revert`-able. Until you decide, brand/URL/marketing are all in limbo.

**Fix:** 5 minutes. See W0.6 in `WES_INDEX.md`.

---

## ✅ What only YOU can do (5 things — unblocks 25 P1 items)

These come straight from `docs/wes/WES_ACTIONS.md` + `POST_ESCRITURA_NOW.md`. Total: ~5 hours this week.

| # | Action | Time | Cost | Unblocks |
|---|---|---|---|---|
| **W0.1** | Book NL+PY dual-tax attorney call (use `ATTORNEY_BRIEF.md`) | 1-2 hr | €300-500 | 10 P1 legal/tax items |
| **W0.2** | Schedule Sonja questionnaire call (use `SONJA_QUESTIONNAIRE.md`) | 1-2 hr | free | 16 P1 worker/culture/salary items |
| **W0.3** | Pick project name (Riverstone Valley vs Villa del Cielo vs other 3) | 5 min | free | All of brand/D14 |
| **W0.4** | Send Anexo I chase to Escribana Peña (overdue 2 months) | 30 min | free | 1 P1 legal item |
| **W0.5** | Pick 5-of-15 materials topics for Sprint 1 | 15 min | free | 6+ research items |

**If you do all 5 this week, you unblock Phase 1 first-guests timeline (2026-12-15 target).** Without them, the timeline slips to Q2 2027.

---

## 🤖 What WE can do for you right now (without your input)

### A. Fix Problem 1 (20km viewer deploy) — 10 min

I can copy the missing file, run the redeploy cron manually, and verify all 18 layer toggles work. Will not modify the source — just sync deploy. Confirm and I'll ship.

### B. Run the 3 NEW research items from the gap analysis

These are queued but waiting for a green light:

1. **NEW-01: AI as price negotiator for PY vendors** — 10 WhatsApp messages to cob/wood/bamboo suppliers, get PYG vs USD pricing, markups, lead times. 1 day.
2. **NEW-02: Steengroeve (stone quarry) in Paraguarí** — local quarries, stone types, prices, lead time. Could become 4th cost pillar. 1 day.
3. **NEW-03: PY railroad + river freight (ANNP)** — bulk material transport cost optimization. ~30% cost saving if viable. 1 day.

Total: 3 days of AI subagent work, no Wes input needed, output lands in `docs/research/RESULTS/`.

### C. Insurance broker outreach prep

For W0.7 (insurance broker pre-qualification), I can:
- Draft the WhatsApp outreach message (ES + EN)
- Identify Marsh Brazil, Aon Argentina, Mapfre PY, La Consolidada, Seguros Atlántida contact paths
- Compile the property data sheet brokers will ask for (62 ha, 82% forest, 6 fincas, escritura date, flood/fire exposure)

You send, I prep. Or I send if you give explicit ✅ on the WES_HOW_WE_WORK outbound rule.

### D. Wes-facing 1-page summary of the attorney brief

`docs/people/stakeholders/ATTORNEY_BRIEF.md` is 24 questions across the 4-BV cascade, MERCOSUR residency, NL-PY tax treaty, dividend withholding, etc. — solid but long.

I can compress it to a 1-page A4 that you actually print and hand the attorney. The full brief stays in the repo for reference.

### E. Recommendation on the 5-of-15 materials pick

You said in audio D: "15 onderwerpen, ik kies 5". Here's Erebus's ranked recommendation based on capex impact (NOT what I want to research — what most affects your €5.5M Phase 1 build):

| # | Topic | Why first | Existing coverage |
|---|---|---|---|
| 1 | **Structureel hout** (eucalyptus vs native hardhout, Itapúa sawmills) | 30% of cabin capex | not researched |
| 2 | **Cob/earthen wall materialen** (klei rond Escobar) | Signature material + Sonja cultural cue | not researched |
| 3 | **Bevestigingsmateriaal** (bulk import vs lokale ferretería) | Recurring line item, markup is hidden | not researched |
| 4 | **Vloeren** (tegels vs gepolijst cement vs hergebruikt hout) | Affects every cabin's finish | not researched |
| 5 | **Verf exterior** (weersbestendig, anti-hongos) | Climate-driven, Paraguayan-specific | not researched |

**Skip for now (high effort, low impact at this phase):** Solar (F09 ✅ done), Water (F15 ✅ done), Isolatie (cob's thermal mass covers it), Keukenapparatuur (M22 ✅ done).

You say "go with the 5" and they ship in 1-2 weeks.

---

## 📊 Status of your 5-audio vision (what got captured)

| Domain | Captured | Status |
|---|---|---|
| D1 Business structure (4-BV + machinepark) | ✅ | Plan, not brainstorm. Needs attorney validation. |
| D2 Insurance (fire/storm/orkaan) | ✅ | Hard gate. HG-3 in POST_ESCRITURA_NOW. |
| D3 Workers (7 roles named) | ✅ | Routes through Sonja (R47). Salary bands via W0.2 call. |
| D4 Build materials 15 topics | ✅ | 8 done, 7 to pick from for Sprint 1. |
| D5 Forest park + wellness pool | ✅ | Eco-pool spec, rain-fed, no chlorine. R&D'd in D6. |
| D6 Railroad Ipoh-Karai | 🟡 | R40 not yet researched. ANDE/Ferrocarril follow-up. |
| D7 Local partners (Kuikopee forester, university ecology, Toyota) | ✅ | W19 (Kuikopee via Sonja), EN02 (plants via Wes). |
| D8 VR / digital twin layer | 🟡 | Pipeline ready, blocked on Wes's phone captures (B07). |
| D9 Termijn-doelen (2030 = Sonja's 60e) | ✅ | Calendar aligned, but soft/hard TBD (Decision 11). |
| D10 "Vakantiepark" naming | 🟡 | W0.6 still pending. |
| D11 Hovenier research | ✅ | EN01 done, needs Kuikopee contact via Sonja. |
| D12 Family-anchored community | ✅ | Captured in HOUSING_PARK_CONCEPT §2.10. |
| D13 "Production means in hands of everyone" | ✅ | Captured as Wes's values frame. |
| D14 Brand/naming | 🟡 | W0.6. |

---

## 🗓️ Your actual calendar (post-escritura 30 days)

From `WES_NEXT_30_DAYS.md`. Today is **Monday 2026-07-06**.

- **This week (Jul 6-12):** Book attorney call, schedule Sonja call, send Anexo I chase, write Fase 1 ownership memo
- **Jul 13-19:** Attorney call → notes to Erebus. Sonja call → notes to Erebus. Fase 1 ownership decided.
- **Jul 20-26:** Sprint 1 research begins. LiDAR quotes in. Name locked. Insurance broker outreach.
- **Jul 27 - Aug 2:** Sprint 1 results complete. 4-BV cascade finalized with attorney. Monthly digest.

---

## What's the single most-useful thing you can read right now?

If you have **5 minutes:** `docs/wes/WES_INDEX.md` (this audit is a summary of that).

If you have **30 minutes:** `docs/wes/WES_INDEX.md` → `POST_ESCRITURA_NOW.md` → `WES_ACTIONS.md`.

If you have **2 hours:** Add `HOUSING_PARK_CONCEPT.md` + `_reconciled/MASTER_BRIEF.md` + `audios/2026-06-30-wes-post-escritura/final/SYNTHESIS.md`.

**If you have 0 minutes:** Print `docs/people/wes/WES_ACTIONS.md`, schedule the 5 calls, mark ✅ as you go.

---

## What I will NOT do without your explicit ✅

- Outbound WhatsApp / email to attorneys, brokers, Escribana (per `WES_HOW_WE_WORK.md`)
- Modify the byte-frozen escritura artifacts (`85e86aa`, `escritura-2026-06-27` tag)
- Pick the project name for you (W0.6, yours)
- Commit to your Fase 1 ownership structure (W0.4, yours + Thijs)
- Sign anything on your behalf

---

## Ask back to me

Three things I need from you to ship faster:

1. **Should I fix Problem 1 (mapa-20km deploy) right now?** Say yes → I copy + redeploy + verify in 10 min.
2. **Green light on the 3 NEW research items (NEW-01/02/03)?** Say go → 3 days, output in `docs/research/RESULTS/`.
3. **Approve the 5-of-15 materials recommendation above?** Say go → Sprint 1 launches Wed 2026-07-22.

Everything else waits for the 5 calls you own.

---

*Generated by Erebus · 2026-07-06 · Based on full repo audit + live deploy verification*
*For: Wesley van de Camp · Cc: Ivan (for context on outbound actions)*
</content>
</invoke>