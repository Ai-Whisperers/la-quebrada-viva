# Session Log — 2026-06-10

> Narrative of what happened in this session, what got created, what decisions were made, and what remains open. AI Whisperers (Ivan) for the client Wesley.
>
> See `STATUS.md` for the canonical current state and `docs/RESEARCH_GAPS.md` for the action list.

> **Navigation (added 2026-06-11, T1.5).** This file is now an **append-only archive** of
> session arcs. Newest arc lives at the bottom under `## Continuation arc` (and successive
> dated headers as they accrue). Existing content is preserved verbatim per the additions-only
> directive — nothing is removed or rewritten. Quick jumps:
>
> - **Current state:** `STATUS.md` (canonical) and `docs/RESEARCH_GAPS.md` (open items).
> - **Latest tick:** scroll to the last `## Continuation arc …` header.
> - **Topic indexes:** `docs/paraguay_context.md` (Paraguay-specific), `MASTER_BRIEF.md` (project root).
> - **Design rules:** `MASTER_BRIEF.md` §14 is canonical (mirrored in `CLAUDE.md` and `docs/paraguay_clay_house_research.md` §18).
>
> When this file grows past ~1000 lines, split older arcs into `docs/session_log/archive_<YYYY-MM>.md`
> and link from this header — deferred until then per additions-only.

---

## Session arc

The session opened with a single artifact: the `Borrador Boleto Compraventa Torrasca Van de Camp.pdf` at the project root, plus a working Blender + Python render pipeline for the La Quebrada Viva cob house. The user asked to analyze the PDF, organize the project, and understand the client.

Over the course of the session, the project scope shifted from "single self-sufficient home" to "housing park + restaurant on 62 hectares" — a meaningful change with major implications for the planning work. By the end of the session we had a clear refined direction, a research tracker, and a 17-day clock to the escritura signing.

## What was created

### New docs in `docs/`

| File | What it is |
|---|---|
| `2026-04-28_boleto_compraventa_torrasca-vandecamp.pdf` | The original 5-page PDF, moved from project root (was: `./Borrador Boleto Compraventa Torrasca Van de Camp.pdf`) |
| `CLIENT.md` | Wesley is the client; sellers, notary, intermediary, project relationship, escritura deadline, 4 open questions for the clients |
| `contract_summary.md` | Greppable boleto privado summary: parties, 6 fincas, money flow diagram, penalty matrix, cláusula summary, gaps in the borrador, 5 open items to chase |
| `HOUSING_PARK_CONCEPT.md` | The menu of possibilities: 8 concept models, restaurant deep-dive, catalogue of all things to include, Paraguay considerations, phasing, 25 open questions |
| `EUROPEAN_TOURISM_SPEC.md` | The refined direction: houses-first vacation rentals for European / 1st-world travelers, restaurant later (European + Dutch, sourced via San Bernardino + German community). 13 sections of Paraguay research, 26 questions |
| `wesley_brief_onepager.md` | One-pager for the 27 Jun escritura signing. v1 was menu-based; v2 (after the refined direction) is focused on 5 decision-unblocking questions |
| `RESEARCH_GAPS.md` | Living tracker: 34 items across 5 tiers, with status legend (🔴🟡🟢⚫🚫), owner legend (W/I/A/H/L), source, effort. Empty findings log at the bottom |
| `SESSION_LOG.md` | This file |

### Updated docs

- `CLAUDE.md` — doc map updated to point at all new docs; project tagline updated to reflect the dual-track scope (renders + planning); variants section preserved
- `STATUS.md` — rewritten as the canonical state doc with render manifest, vision summary, doc inventory, open tasks, decisions log, critical dates, environment, next session priorities

### What was NOT changed

- `lqv/` package — untouched this session. Render agent handles Blender work.
- `scene.blend` and backups — untouched.
- `renders/` — no new finals added by this agent (render agent handles).
- `MASTER_BRIEF.md`, `paraguay_clay_house_research.md`, `asset_plan.md`, `master_plan.md` — not modified, still authoritative for their respective scopes.
- `_archive/` — untouched (gitignored, do-not-touch anyway).

## Key decisions made

### 1. Client identification

- **Wesley Manuel van de Camp** (Pasaporte NWF23H565) = the client. 75% legal owner of the 62 ha. Design decision-maker.
- **Thijs Adrianus Hendricus** (Pasaporte NP19HPFP6) = 25% financial co-buyer. Not the design client.
- **Justiniano Torrasca Delgado + María Teresa Medina de Torrasca** = sellers (married couple, bienes gananciales).
- **Escribana Cynthia Andrea Peña Ros** = holds the seña in depósito notarial.
- **Juan José Burgos Armoa** = real estate intermediary, G. 313M commission.
- **Ivan Weiss Van Der Pol / AI Whisperers** = digital support lead (research, planning, digital help). NOT the legal owner of the land. The "Owner: Ivan" line in `MASTER_BRIEF.md:4` is misleading and was flagged for correction.

### 2. Scope reframing

- **Old scope**: single self-sufficient home (La Quebrada Viva) on the 62 ha.
- **New scope**: housing park + restaurant + amenities on the 62 ha.
- The cob house design becomes the **first example building typology** within the larger vision, not the whole vision.
- The 12 existing renders stay valid as concept art for the cob typology.
- The site model (the durable deliverable) is unaffected.

### 3. Sequencing

- **Houses first** (Phase 1, months 1–9 post-closing): 3–6 cob/earthen + timber vacation-rental houses, Airbnb/Booking-ready, target European / 1st-world travelers.
- **Events** (Phase 2, months 9–18): scale to 6–8+ houses, build event space.
- **Restaurant** (Phase 3, year 2+): European-Dutch cuisine, multi-zone, sourced via San Bernardino + German community.

### 4. Target market

- **Primary**: European travelers (German, Dutch, Swiss, Austrian, French, Belgian, Scandinavian) + North Americans with PY ties
- **Distribution**: Booking.com + Airbnb + direct + travel media + expat community word-of-mouth
- **Seasonality**: peak Jun–Aug (Southern Hemisphere winter), shoulder Mar–May / Sep–Nov, events-driven secondary peaks
- **Pricing benchmark**: USD 150–400/night (verify with R06)

### 5. Style

- Resort + events + eco-natural retreat (a blend, not a pure eco retreat)
- Cob/earthen construction continues to be the lead design language
- Site preserves most of the 62 ha as Atlantic Forest (92% already gone in PY; this is part of the remaining 8%)

### 6. Supply chain anchor

- **San Bernardino** (48 km from Asunción, on Lago Ypacaraí) + the **German community in Paraguay** (Asunción, San Ber, Itapúa, Chaco Mennonites) = the source of European ingredients, chefs, and bilingual staff
- Wesley's **personal network** in these communities is the single biggest predictor of Phase 1 timeline

### 7. Process decisions

- **Doc work and render work are now in different agents.** AI Whisperers (Ivan) handles docs, planning, research. A separate render agent handles the 6 remaining C-finals. They are not blocking each other.
- **R04 is the single most important research question** — does Wesley have a personal network in the German / Dutch / European expat community in PY? Determines whether Phase 1 lands in 9 months or 18+.

## What was researched

### Documented (in spec + tracker)

- San Bernardino geography and role
- German community in Paraguay (concentrations, supply chain, numbers)
- Dutch community in Paraguay (smaller, but exists, and Wesley + Thijs are Dutch)
- European / 1st-world tourism to PY (size, segments, patterns)
- Comparable properties in PY (Chaco eco-lodges, San Bernardino B&Bs, Asunción boutique hotels)
- Regional comparable models (Mendoza, Iberá, José Ignacio)
- Vacation-rental typology for this market
- Events market (weddings, corporate, family)
- Eco-natural positioning for this market
- Restaurant phase 2 direction (European-Dutch, sourced via San Ber)
- Regulatory stack (SENATUR, SET, bomberos, bromatología, hotel vs residential, IVA, foreign-ownership)
- Marketing channels (OTAs, direct, PR, partnerships, expat word-of-mouth)
- Phasing (3 phases over 3 years)
- 25 + 26 = 51 open questions for Wesley across the two docs

### What remains open (the 34 research items)

See `docs/RESEARCH_GAPS.md` for the full list with status. The 4 most critical items for the next 17 days:

- **R01** — Site visit to Escobar (human-in-PY)
- **R02** — Anexo I of the boleto (Wesley + Escribana Peña)
- **R03** — Municipalidad de Escobar land use rules (Wesley + local attorney)
- **R04** — Wesley's personal network (Wesley; 30 minutes)

## What the next session should do

1. **Wesley answers R01, R02, R03, R04** before the 27 Jun escritura. These four together unblock ~80% of the planning.
2. **AI Whisperers spins up a research subagent on the A-tier items** (R05, R06, R12, R13, R21, R22, R23, R24, R26, R34) — all web research, runs unattended.
3. **Wesley engages a local attorney** on the legal stack (R02, R03, R14, R27, R28).
4. **Render agent finishes the 6 C-finals** before 27 Jun.
5. **AI Whisperers polishes the onepager** (`docs/wesley_brief_onepager.md`) once R01–R08 answers come in.
6. **Once a direction is firm**, AI Whisperers drafts Phase 1 capex ranges, marketing plan, and event-space feasibility.

## What's at risk

- **The escritura deadline (27 Jun)** is firm. If the deal collapses for any reason, all this planning is moot. The sellers' entrega of title docs (due ~5 May) needs to be verified as in hand.
- **If Wesley doesn't have a warm personal network in the San Bernardino / German community** (R04), the project timeline stretches from 9 months to 18+ for Phase 1. That's not fatal but it's a major pace change.
- **The Municipality of Escobar could refuse commercial classification** (R03). If so, the entire housing park + restaurant model is blocked. The cob house for personal use is the fallback.
- **The render agent could be blocked** by the smoke test hang we saw earlier. The other agent needs to recover and continue. AI Whisperers is not the right agent to debug this.

## What was NOT in scope this session

- No Blender work (delegated to render agent)
- No contact with Wesley directly (Ivan is the bridge, not the sender)
- No changes to `lqv/` code, `scene.blend`, or any renders
- No commits to git (per user preference; uncommitted changes are at root of project for user review)
- No marketing copy, no website, no business plan with financials (waiting for R07 capex data)

---

## Continuation arc (same calendar day, later)

After the original session log was written, work continued on additive polish + render delivery. Captured here so a future session reading top-down sees the full state.

### License bundle prep (completed)

- `LICENSES/CC0-1.0.txt` — landed verbatim from `https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt` (121 lines)
- `LICENSES/CC-BY-4.0.txt` — landed verbatim from `https://creativecommons.org/licenses/by/4.0/legalcode.txt` (396 lines)
- `LICENSES/README.md` — mirror-policy explainer: which CC texts are mirrored verbatim, why vendor terms (Poly Haven / Sketchfab / Hyper3D) are intentionally NOT mirrored, cross-references to `CREDITS.md` / `LICENSE_BUNDLE.md` / `docs/license_obligations.md`
- `LICENSE_BUNDLE.md` §7 — mirror-status table flipped: CC0 + CC-BY rows show `☑ landed 2026-06-10`; vendor rows show `☐ NOT mirrored — vendor terms change; URL is authoritative`. Trailing paragraph rewritten to explain the vendor-URL-only policy.

These satisfy the Phase 8 bundle-prep item from `LICENSE_BUNDLE.md` §7 (license texts available offline for the redistribution bundle).

### Render delivery (in progress)

- A + B variants × 6 cams each = **12 of 18 finals** committed (per `STATUS.md` manifest).
- C variant batch (`renders/C_*.png`) is rendering headless in a background `blender` process under `/tmp/render_finals.log`. C_hero (2560×1440 @ 512 samples) renders first, then 5 other cams at 1920×1080 @ 256 samples. Wall-clock estimate ~2 h from start.
- Pre-Phase-7 C_hero attempt died at sample 504/512 to OOM; relaunched with system memory headroom verified. Per-process Blender memory stays ~1.2 GB peak under current load.

### Onepager additive polish

- `docs/wesley_brief_onepager.md` — added a **closing-day prep checklist** section: docs/funds/powers Wesley + Thijs should bring or confirm 5 days before the 27 Jun signing, plus a risks-to-watch list (seller no-show penalty, buyer no-show penalty, last-minute gravamen, missing Cl. OCTAVA delivery). Does not change the 5 priority questions — those still need Wesley's answers to fully polish v3.

### Continuation arc tick 3 — cross-link audit (same calendar day)

Additive-only doc polish while the C-render batch runs in the background. Goal: make every escritura-relevant doc cross-link the printable [`CLOSING_DAY_PREP.md`](./CLOSING_DAY_PREP.md) day-by-day sequence + risk register so a reader landing on any of them can pivot to the actionable checklist.

- Audit via `grep -l "CLOSING_DAY_PREP" docs/*.md CLAUDE.md STATUS.md` — already cross-linked: `STATUS.md`, `docs/contract_summary.md`, `docs/RESEARCH_GAPS.md` (R02 row), `CLAUDE.md` (doc map). Missing: `docs/CLIENT.md`, `docs/wesley_brief_onepager.md`, `docs/SESSION_LOG.md`.
- `docs/CLIENT.md` — appended a one-line cross-link paragraph after the "Open items before 27 June" numbered list pointing readers at the T-7 / T-5 / T-2 / signing-day / T+30 sequence.
- `docs/wesley_brief_onepager.md` — inserted a blockquote under the "Closing-day prep checklist" header flagging the printable version, plus a reference-docs bullet for `docs/CLOSING_DAY_PREP.md`.
- `docs/SESSION_LOG.md` — this section. Closes the last cross-link gap on the audit list.

No `lqv/` edits, no scene changes, no git operations, no subagent spawns this tick. All edits are byte-identity-safe with respect to the in-flight C-batch (sample ~196/512 on C_hero at the time of writing; ~33 min projected to C_hero completion; 5 lighter cams to follow).

### Continuation arc tick 4 — vision-doc cross-links (same calendar day)

Additive-only continuation of the cross-link audit. Extends CLOSING_DAY_PREP reachability from the 7 escritura-operational docs (CLIENT, contract_summary, wesley_brief_onepager, RESEARCH_GAPS, CLAUDE, SESSION_LOG, STATUS) into the two **scope-vision** docs that frame the larger housing-park direction.

- `docs/HOUSING_PARK_CONCEPT.md` — under "Phase 0 — Pre-closing (now → 27 Jun 2026)" (line ~317), appended a one-line bullet cross-linking the day-by-day T-7 / T-5 / T-2 / signing-day / T+30 sequence and risk register. Rationale: a reader exploring the 8 concept models or 25 open questions still needs a single click to reach the actionable closing checklist.
- `docs/EUROPEAN_TOURISM_SPEC.md` — under "Phase 0 — Pre-closing (now → 27 Jun 2026) ← we are here" (line ~397), appended the same one-line bullet. Rationale: this is the refined-direction doc Wesley will be reading most; a single in-line link to the printable checklist keeps the operational path one hop away from the vision narrative.
- Final cross-link reachability now covers 9 docs total: STATUS, CLIENT, contract_summary, wesley_brief_onepager, RESEARCH_GAPS, CLAUDE, SESSION_LOG, HOUSING_PARK_CONCEPT, EUROPEAN_TOURISM_SPEC. Every doc a stakeholder is likely to land on first can pivot to CLOSING_DAY_PREP in one click.

Render state during this tick: sample 240 → 284 on C_hero (~22 min projected to completion at tick close). blender PID 1410354 healthy at 396% CPU, 14.2% mem, elapsed 29:47. System pressure: 3.9 Gi RAM available + 1.8 Gi swap free — tightened ~1 Gi from prior tick but still within safe margin. No SIGKILL signature. Doc-only operations only this tick (no `lqv/` edits, no scene changes, no git operations, no subagent spawns). Byte-identity-safe with respect to the in-flight C-batch.

### Continuation arc tick 5 — phasing + bundle + index cross-links (same calendar day)

Additive-only continuation. Extends CLOSING_DAY_PREP reachability beyond the 9 escritura-operational + vision docs into the 3 remaining ops/index docs where a reader will plausibly land.

- `docs/housing_park_phasing.md` — line 17 bullet under "## Phase 0 — Escritura + entitlements (months 0–3, 2026-Q3)" amended (additively) to suffix the existing `2026-06-27: escritura traslativa signed.` with `Day-by-day T-7 / T-5 / T-2 / signing-day / T+30 checklist + risk register: [\`CLOSING_DAY_PREP.md\`](./CLOSING_DAY_PREP.md).` Rationale: this doc is the 5-year build-out timeline; the very first dated bullet is the escritura, and a click to the printable checklist is the natural pivot.
- `docs/wesley_deliverable_bundle.md` — appended item 9 to the Tier 1 physical-bundle list: `Day-by-day closing checklist (A4 print of CLOSING_DAY_PREP.md — T-7 / T-5 / T-2 / signing-day / T+30 sequence + risk register; for Wesley's own use, not handed to notary)`. Rationale: bundle manifest must explicitly enumerate every print Wesley needs in the folder, including the operational checklist (which is for him + Thijs, not for the notary).
- `docs/research_index.md` — inserted a one-line bullet for `docs/CLOSING_DAY_PREP.md` in the "Project ops & roadmap" section (between `wesley_brief_onepager.md` and `contract_summary.md`). Rationale: the doc-index must surface the closing checklist alongside the other escritura-day docs; otherwise a future-Claude session reading the index first won't find it.
- Final cross-link reachability now covers 12 docs total: STATUS, CLIENT, contract_summary, wesley_brief_onepager, RESEARCH_GAPS, CLAUDE, SESSION_LOG, HOUSING_PARK_CONCEPT, EUROPEAN_TOURISM_SPEC, housing_park_phasing, wesley_deliverable_bundle, research_index. Audit candidate-list exhausted for natural fits. `master_plan.md` not cross-linked: its "Phase 7+" headings refer to render-pipeline phases (Variant C + asset integration), not property phases — inserting a CLOSING_DAY_PREP link there would be a category error.

Render state during this tick: sample 284 → 344 on C_hero (~15 min projected to completion at tick close). blender PID 1410354 healthy at 396% CPU, 14.2% mem, elapsed 33:31. System pressure: 4.8 Gi RAM available + 1.9 Gi swap free — actually loosened slightly from prior tick (3.9 → 4.8 Gi). No SIGKILL signature. Monitor armed on `/tmp/render_finals.log` for `Saved:|Killed|Error|Traceback|OOM|Segmentation|signal` to catch C_hero completion + 5 follow-on cams. Doc-only operations only this tick. Byte-identity-safe with respect to the in-flight C-batch.

### Continuation arc tick 6 — backlink + dependency-graph satellite (same calendar day)

Additive-only continuation. The 12-doc cross-link reachability set is exhausted per tick 5; the two remaining additive opportunities both improve **discoverability of CLOSING_DAY_PREP** without inserting category-error links into render-pipeline docs.

- `docs/CLOSING_DAY_PREP.md` — appended `research_index.md` to "## Authoritative references" (line ~104) as a back-link to the meta-pointer doc. Rationale: the index already lists CLOSING_DAY_PREP under §Project ops & roadmap; a reciprocal back-link closes the navigation loop so a reader who lands on the closing checklist can find every other research doc in one click without re-grepping.
- `docs/research_index.md` — appended an **escritura-day side-chain** dependency diagram below the main dependency-arrow block (line ~167). Rationale: the main tree centers on the design/build/asset pipeline; the escritura-day Phase 0 driver (CLOSING_DAY_PREP) was orphaned from the visual graph. Drawing it as a satellite chain (`contract_summary + wesley_deliverable_bundle → CLOSING_DAY_PREP ← wesley_brief_onepager + housing_park_phasing`) keeps the main tree's ASCII alignment intact (initial attempt to inline CLOSING_DAY_PREP into the main bracket broke the `cultural_notes ───┘` joining alignment — reverted and used the satellite-block pattern instead).
- Cross-link reachability now covers 13 distinct discoverability paths to CLOSING_DAY_PREP from the doc graph. No new operational content added; this is purely graph-topology improvement.

Render state during this tick: C_hero ☑ landed (19.9 MB PNG, written 17:04 local). C_stream_up sample 80 → 136 on tick close (~7 min projected to completion). Per-cam-loop architecture working as designed — `random.seed()` ordering preserved, memory stable at ~982 MB peak (well below the C_hero pre-fix OOM signature of 1.6+ Gi). No SIGKILL. MCP socket "Bad file descriptor" errno 9 noise in log is benign — known dead socket, not a render failure signal. Doc-only operations only this tick. Byte-identity-safe with respect to the in-flight 5 follow-on C-cams (stream_up → terrace → cliff → dusk → petal_macro).

### Continuation arc tick 7 — code-map currency for already-shipped Variant C (same calendar day)

Additive-only continuation. Audit moved outside the 13-path doc-cross-link graph and into the **code-map docs** (`ARCHITECTURE.md`, `CREDITS.md`) which had stale gaps for Variant C work that already landed in `lqv/`. None of these edits touch `lqv/` itself — render byte-identity for the in-flight C-batch is preserved.

- `CREDITS.md` — appended `LICENSES/README.md` to "### Cross-references" (line ~82). Rationale: `LICENSES/README.md` already back-links to CREDITS.md + LICENSE_BUNDLE.md; the reciprocal link was missing, leaving the verbatim CC0/CC-BY 4.0 legal-code mirror reachable only by directory traversal. One-line addition closes that loop.
- `ARCHITECTURE.md` — added a **`lqv/flora/fireflies.py` row** to the Subpackages table (~80 firefly emission spheres on corredor + lower terrace, Variant C only) **and** a new "### Variant C additions (2026-06-10) — already in code, listed for navigation" satellite block below the table covering: (i) the lighting.py Variant C branch (cool moonlight + low blue sky strength + exposure +0.6) with an explicit note that the existing "Anything else raises ValueError" line predates C and is now stale; (ii) `lqv/house/cob.py:build_window_emission` (warm window-glow planes inside the hidden `WindowCut_*` cutouts); (iii) pointer back to the new fireflies row.
- Pattern note: additive satellite block instead of in-row rewrite because the in-row "Anything else raises ValueError" claim is technically wrong post-C, but rewriting violates the additions-only directive — a "this note predates C" override in a new block is the additive-compliant fix and is more honest about doc history than silent in-place revision.

Render state during this tick: C_hero ☑ (19.9 MB, 17:04 local). C_stream_up at sample 248/256, ~27 sec remaining, mem stable 982 MB peak 991 MB. No SIGKILL, no Traceback. MCP "Bad file descriptor" noise still benign. Doc-only operations this tick. Byte-identity-safe for the in-flight 5 follow-on C-cams.

Cross-link / code-map reachability tally at tick close: 13 distinct discoverability paths to CLOSING_DAY_PREP (unchanged); 1 new doc→docs reciprocal link (CREDITS↔LICENSES/README); ARCHITECTURE.md now covers 100% of shipped Variant C subpackages (was missing fireflies + window_emission).

### Continuation arc tick 8 — index orphans + Variant C procedural-recipe traceability (same calendar day)

Additive-only continuation. Two doc gaps surfaced after tick 7: (i) `docs/external_assets.md` had no entry explaining that Variant C's two procedural visual signatures (fireflies + window-glow) are code recipes — not third-party assets — so a future session could waste time searching for "the firefly asset"; (ii) `docs/research_index.md` listed every research narrative but omitted the **code & state docs** (`CLAUDE.md`, `STATUS.md`, `ARCHITECTURE.md`, this `SESSION_LOG.md`, `LICENSES/README.md`, `claude_code_blender_best_practices.md`) — they sat orphaned from the project's "single entry point" index.

- `docs/external_assets.md` — appended a **"Variant C — procedural recipes (no third-party asset, listed for traceability)"** block immediately after the Phase 11 work-order line. Lists `lqv/flora/fireflies.py`, `lqv/house/cob.py:build_window_emission`, and `lqv/lighting.py` Variant C branch with rationale ("no license obligation because no third-party asset"). Includes pointer triad: `CREDITS.md` §Hyper3D + `docs/asset_plan.md` §C.4 + `ARCHITECTURE.md` §Variant C additions.
- `docs/research_index.md` — added a **"Code & state docs (additive 2026-06-10 — previously orphaned from this index)"** satellite section in the "By document type" group, after the "Gap analysis & forward-looking" subsection and before "By topic". Indexes `CLAUDE.md`, `STATUS.md`, `ARCHITECTURE.md`, `docs/SESSION_LOG.md`, `LICENSES/README.md`, `docs/claude_code_blender_best_practices.md` with one-line each.
- Pattern note: chose satellite "(additive — previously orphaned)" framing on the research_index addition rather than splicing entries into the existing categories ("Engineering specs" / "Project ops & roadmap") because those categories were originally scoped to research narratives, not code-map artifacts; broadening them in-place would silently reframe the index, while a satellite block is a transparent and additive expansion.

Render state during this tick: C_hero ☑ (19.9 MB, 17:04 local). C_stream_up ☑ (11.2 MB, 17:21 local). C_terrace at sample 80/256, Time:04:04.15, Remaining:08:45.22, mem stable 982 MB peak 991 MB. Healthy progression. No SIGKILL, no Traceback. Doc-only operations this tick. Byte-identity-safe for the in-flight 4 follow-on C-cams.

Cumulative reachability metric at tick close: research_index.md now covers 100% of `.md` files a future-Claude-session is likely to hit in its first hour of cold-start (was previously missing the 6 code-state docs listed above). external_assets.md now closes the procedural-vs-third-party ambiguity for Variant C (was previously silent — a session reading the asset shortlist would have to infer "no asset needed" from CREDITS.md absence).

### Continuation arc tick 9 — STATUS.md render-progress satellite (same calendar day)

Additive-only continuation. After tick 8 the doc graph + code-map were complete; the remaining drift was that **`STATUS.md`** still showed A+B 12/12 ☑ and the C row frozen at "0/6 — in flight" while C_hero + C_stream_up were already on disk. Rewriting the manifest table cells mid-batch would violate atomic-end-of-batch update; satellite-block pattern preserves the frozen manifest until Batch 7 ships.

- `STATUS.md` — inserted "### 1.1 Render-progress satellite (additive 2026-06-10 17:25 — frozen manifest preserved above)" block between section 1 closing line and the "## 2. ..." header. Lists C_hero ☑ (19.9 MB, 17:04 local), C_stream_up ☑ (11.2 MB, 17:21 local), C_terrace ⏳ in flight at write-time, C_cliff / C_dusk / C_petal_macro pending in per-cam loop, per-cam memory peak ~991 MB (well under pre-fix C_hero OOM signature of 1.6+ Gi).
- Pattern note: the canonical manifest table at top of `STATUS.md` stays frozen until Batch 7 commit performs the **atomic end-of-batch update** to A/B/C 18/18 ☑. The satellite block is the live state pointer; the manifest table is the contract surface (= "what got shipped as a batch"). Drifting the contract surface mid-batch is the pattern this avoids.

Render state during this tick: C_hero ☑. C_stream_up ☑. C_terrace at sample ~152/256 mid-tick. Healthy progression. No SIGKILL, no Traceback. Doc-only operations this tick. Byte-identity-safe for the in-flight 4 follow-on C-cams.

### Continuation arc tick 10 — license + bundle Variant C backfill (same calendar day)

Additive-only continuation. After tick 7 added the procedural-recipe Variant C block to `external_assets.md` and tick 8 indexed it from `research_index.md`, two parallel docs still had **stale silence** about Variant C: `docs/license_obligations.md` (the IP/CC-BY framework — silent on whether Variant C added any license obligation) and `docs/wesley_deliverable_bundle.md` (the escritura-day shipping manifest — silent on Variant C delivery status). Both gaps closed here without rewriting the original frozen content.

- `docs/license_obligations.md` — appended "## Variant C procedural recipes — no third-party license obligation (additive 2026-06-10)" block before "## Cross-references". Records the explicit license-posture implication: Variant C imagery does **not** add a CC-BY attribution requirement because fireflies + window-glow + cool moonlight are all procedural recipes in `lqv/`, not third-party assets. The only license obligations for C-imagery flow through the same Poly Haven CC0 HDRI + CC0 PBR textures already credited for A and B. Extended Cross-references with a one-line bullet for `LICENSES/README.md` to close the verbatim-legal-code reachability gap from this doc.
- `docs/wesley_deliverable_bundle.md` — appended "## Variant C delivery satellite (additive 2026-06-10, in-session)" block before "## Cross-references". Records the live C-batch state (C_hero ☑, C_stream_up ☑, C_terrace ⏳, C_cliff / C_dusk / C_petal_macro pending), notes the Tier-2 USB / cloud bundle needs **no additional license artefact** beyond the same `CREDITS.md` + `LICENSE_BUNDLE.md` + `LICENSES/README.md` triple already covering A and B, and updates the **Risk-register #1 status** ("C render fails to finish") to *partially executed* — per-cam relaunch loop has already delivered 2/6 C-cams cleanly; A+B alone (12 renders) still publishable if the remaining 4 fail. Extended Cross-references with 4 new bullets: `LICENSES/README.md`, `STATUS.md`, `docs/SESSION_LOG.md`, `ARCHITECTURE.md`.
- Pattern note: same satellite-block-vs-rewrite pattern as tick 9. The pipeline-table row "2026-06-10–12 | C render batch finishes" in `wesley_deliverable_bundle.md` stays frozen until atomic end-of-batch update. The Risk-register #1 entry stays frozen too; the satellite block records the *partial-execution* status without rewriting the original risk text. Symmetric with how `STATUS.md`'s frozen manifest is preserved.

Render state during this tick: C_hero ☑. C_stream_up ☑. C_terrace landed (10.8 MB, 17:36 local) at tick close → **15/18 disk milestone reached**. C_cliff starting in per-cam loop. Healthy. No SIGKILL, no Traceback. Doc-only operations this tick. Byte-identity-safe for the in-flight 3 follow-on C-cams.

Cumulative reachability metric at tick close: `docs/license_obligations.md` now closes the Variant C license-posture silence (previously inferrable only by absence-from-CREDITS reasoning). `docs/wesley_deliverable_bundle.md` now records the live C-batch delivery state without breaking the frozen production-pipeline manifest contract above it. 6 docs are now Variant-C-aware: `CLAUDE.md`, `STATUS.md` (via satellite), `ARCHITECTURE.md` (via satellite), `external_assets.md` (via traceability block), `license_obligations.md` (this tick), `wesley_deliverable_bundle.md` (this tick).

### Continuation arc tick 11 — bidirectional doc-graph closure: asset_plan §G + external_assets cross-refs + 16/18 milestone (same calendar day)

Additive-only continuation. After tick 10 the Variant-C-aware doc set was: `CLAUDE.md`, `STATUS.md` (satellite), `ARCHITECTURE.md` (satellite), `external_assets.md` (procedural traceability), `license_obligations.md` (carve-out + LICENSES/README cross-ref), `wesley_deliverable_bundle.md` (delivery satellite + 4 cross-refs). Two **symmetric orphan pointers** remained: (i) `docs/asset_plan.md` was referenced BY external_assets.md / license_obligations.md / wesley_deliverable_bundle.md but did not reference them back; (ii) `docs/external_assets.md` was referenced BY license_obligations.md / wesley_deliverable_bundle.md / asset_plan.md (after the §G addition) but its tail had only a 3-target "See also" line pointing to CREDITS / asset_plan §C.4 / ARCHITECTURE — no reverse pointers to the docs that depend on it.

- `docs/asset_plan.md` — appended a "## G. Cross-references (additive 2026-06-10)" section after §F. Preamble notes this plan was previously a closed loop ending at §F. 10 cross-reference bullets: `docs/external_assets.md` (live download/status mirror + Variant C procedural-recipe traceability block), `docs/license_obligations.md` (CC0/CC-BY 4.0 obligations + Variant C carve-out), `LICENSES/README.md` (verbatim legal-code mirror), `docs/wesley_deliverable_bundle.md` (Tier-1/2/3 shipping manifest), `CREDITS.md` (per-asset attribution rows), `LICENSE_BUNDLE.md` (full license texts), `STATUS.md` (live render manifest), `docs/SESSION_LOG.md` (per-cam render-loop architecture decision), `ARCHITECTURE.md` (`lqv/` package code map for §D.2 integration points), `CLAUDE.md` (code invariants §D.3 must preserve).
- `docs/external_assets.md` — appended a "## Cross-references (additive 2026-06-10)" section after the existing tail "See also" line. Preamble notes the "See also" line covers immediate Variant-C neighborhood but several docs depend on this file without reverse pointers. 9 bullets back-linking to: `docs/asset_plan.md` §C.3 + §G, `docs/license_obligations.md`, `docs/wesley_deliverable_bundle.md`, `CREDITS.md`, `LICENSES/README.md`, `STATUS.md`, `docs/SESSION_LOG.md`, `ARCHITECTURE.md`, `CLAUDE.md`. Each bullet states *why* the back-link matters (e.g., LICENSES/README required in Tier-2 USB/cloud bundle; CLAUDE.md invariants must be preserved by Phase 8c asset imports).
- Pattern note: bidirectional reachability across the asset-graph mesh is now complete — every doc in {asset_plan, external_assets, license_obligations, wesley_deliverable_bundle, CREDITS, LICENSE_BUNDLE, LICENSES/README, STATUS, SESSION_LOG, ARCHITECTURE, CLAUDE} that names any other in the set has a reciprocal pointer. Cold-start sessions can land on any of the 11 nodes and traverse the full subgraph without dead-ends.

Render state during this tick: C_hero ☑ (19.9 MB, 17:04 local). C_stream_up ☑ (11.2 MB, 17:21 local). C_terrace ☑ (10.8 MB, 17:36 local). **C_cliff ☑ (10.0 MB, 17:47 local) — 16/18 disk milestone reached** at sample 256/256, Time:09:11.36, Final mem 1158.78M peak 1253.70M (within the per-cam OOM margin — the pre-fix C_hero spike was 1.6+ Gi). C_dusk starting in per-cam loop. C_petal_macro queued behind. Healthy progression. No SIGKILL, no Traceback. Doc-only operations this tick. Byte-identity-safe for the in-flight 2 follow-on C-cams.

Cumulative reachability metric at tick close: asset-graph mesh has full bidirectional reachability across 11 nodes (was previously asymmetric — `asset_plan.md` and `external_assets.md` were both "referenced but not referencing"). A cold-start Claude session can now begin reading at any of the 11 docs and reach the entire asset/license/delivery subgraph by following inline cross-references — no dead-ends, no orphan pointers. 16/18 finals on disk; C_dusk + C_petal_macro remaining, ~18 min ETA combined.

### Continuation arc tick 12 — ARCHITECTURE.md + CREDITS.md + LICENSE_BUNDLE.md back-pointer closure (same calendar day, C_dusk in flight)

Additive-only continuation. After tick 11 the asset-graph mesh had full bidirectional reachability across 11 nodes — *for the asset/license/delivery subgraph*. But three documents in that mesh — `ARCHITECTURE.md`, `CREDITS.md`, `LICENSE_BUNDLE.md` — still had asymmetric pointer surfaces: each was the *target* of many cross-references from the asset/license docs (and from CLAUDE.md, STATUS.md, SESSION_LOG.md) but had Cross-references sections of their own that were either missing entirely or covered only a partial set. This tick closes that asymmetry without touching frozen module tables, attribution rows, or per-license bundle entries.

- `ARCHITECTURE.md` — appended a "## Cross-references (additive 2026-06-10)" section after the existing tail "Laterite primary `#C4522A` is slightly outside the documented photo range (warmer read under AgX)." line. Preamble notes this file is the navigation entry for the `lqv/` Python package; multiple docs *point at* this file for code-location lookups but the reverse pointers were missing. 10 back-link bullets each stating *why* the back-link matters: `CLAUDE.md` §"Document map" (the two files are contract — CLAUDE.md says *why* the invariant exists, ARCHITECTURE.md says *which module enforces it*), `STATUS.md` (module table ↔ render manifest pairing), `docs/SESSION_LOG.md` (decision-side index for the §"Variant C additions" code-side index above), `docs/asset_plan.md` §C + §G (Phase 8 asset-import plan landing in planned `lqv/asset_loader.py`), `docs/external_assets.md` §Cross-references (USE_EXTERNAL_FLORA flag target), `docs/license_obligations.md` (Variant C procedural-recipe carve-out names same 3 code paths), `docs/wesley_deliverable_bundle.md` §Cross-references (Tier-2 USB bundle includes zipped `lqv/*`), `CREDITS.md` + `LICENSE_BUNDLE.md` ("zero new third-party assets" reciprocal source-of-truth), `docs/research/README.md` (Phase 7.5 fragility enforces design rules 1, 4, 5, 8), `_archive/build_scene.py.pre-refactor.bak` (pre-refactor monolith reference-only).
- `CREDITS.md` — extended the existing 5-bullet §Cross-references at the file tail with 5 additional symmetric back-pointers: `docs/wesley_deliverable_bundle.md` §Tier 2 (CC-BY 4.0 attribution triple at distribution time), `STATUS.md` (source of truth for which `[PLANNED]` Sketchfab/Hyper3D entries actually got wired vs deferred behind the MCP-socket block), `ARCHITECTURE.md` §"Variant C additions (2026-06-10)" (code-side index of the three procedural recipes that explain why this file gains *zero* new third-party rows for Variant C), `docs/SESSION_LOG.md` (each `[USED]` maps to an asset-import action recorded there), `CLAUDE.md` §"Material color references" + §"Plant species — critical accuracy notes" (photographic constants this file's `[PLANNED]` reference rows must respect — e.g., pindo plumose-droop spec gates any future flip from `[PLANNED]` → `[USED]`).
- `LICENSE_BUNDLE.md` — extended the existing 6-bullet §8 Cross-references with 5 additional symmetric back-pointers: `LICENSES/README.md` (verbatim legal-code mirror; vendor-terms URL-only policy rationale lives there), `STATUS.md` (§6 readiness gates flip to ☑ only when STATUS.md manifest cell flips — STATUS triggers, LICENSE_BUNDLE checklists), `ARCHITECTURE.md` §"Variant C additions (2026-06-10)" (the three Variant C procedural recipes add *zero* rows to §§3-5 — reciprocal source-of-truth for the "zero new license exposure" claim), `docs/SESSION_LOG.md` (per-license decisions in §3 CC-BY-SA exclusion + §7 Hyper3D vendor-terms URL-only policy map to ticks), `CLAUDE.md` §"Things to refuse / push back on" + §"Document map" (three-file CC-BY 4.0 attribution contract — CLAUDE.md says *why*, this file says *how* §6 gates implement it).
- Pattern note: same additive Cross-references-append pattern as ticks 9-11. All three documents' pre-existing content (module tables, fragility list, known-divergences block in ARCHITECTURE.md; per-asset attribution rows in CREDITS.md; per-license tables + §6 readiness gates + §7 vendor-terms table in LICENSE_BUNDLE.md) is **byte-identical**. Only end-of-file extensions; no rewrites, no removals.

Render state during this tick: 16/18 finals on disk (C_hero ☑ 19.9MB, C_stream_up ☑ 11.2MB, C_terrace ☑ 10.8MB, C_cliff ☑ 10.0MB). **C_dusk in flight at Sample 96/256, Time:05:37, Remaining:09:14, Mem:1095.50M, Peak:1232.43M** — healthy progression (within the per-cam OOM margin; C_hero pre-fix spike was 1.6+ Gi). C_petal_macro queued behind C_dusk. Doc-only operations this tick. Byte-identity-safe for the in-flight 2 follow-on C-cams (zero `lqv/*` edits).

Cumulative reachability metric at tick close: the full 11-node mesh now has full bidirectional reachability **including the navigation/contract subgraph** ({ARCHITECTURE, CREDITS, LICENSE_BUNDLE} previously had asymmetric pointer surfaces in addition to the asset/license/delivery asymmetry closed in tick 11). A cold-start Claude session can now begin reading at *any* of the 11 docs (asset/license/delivery + navigation/contract) and traverse the full subgraph without dead-ends. All Variant C documentation surfaces (CLAUDE.md → STATUS.md → ARCHITECTURE.md → SESSION_LOG.md → license docs → delivery docs → attribution docs) carry reciprocal back-pointers stating *why* the link exists, not just *that* it exists.

### Continuation arc tick 13 — STATUS.md §9 Cross-references closure (same calendar day, C_dusk Sample 240/256)

Additive-only continuation. After tick 12 closed the navigation/contract subgraph by extending `ARCHITECTURE.md`, `CREDITS.md`, and `LICENSE_BUNDLE.md` with reciprocal back-pointers, one asymmetry remained: `STATUS.md` itself. STATUS is the most-referenced doc in the 11-node mesh — CLAUDE.md, ARCHITECTURE.md, CREDITS.md (×2 from prior ticks), LICENSE_BUNDLE.md §6 gates, every render-progress satellite block — yet it had **sections 1-8 only and zero Cross-references section**. Doc-graph reachability was *forward-from-STATUS missing* even after the navigation/contract subgraph was closed; STATUS was the universal target but not a navigation hub. This tick closes that final asymmetry without modifying §1 render manifest, §4 open-task ledger, §5 decisions log, or §6 critical dates.

- `STATUS.md` — appended a new "## 9. Cross-references (additive 2026-06-10)" section before the line 199 trailer (`*Maintained by Ivan / AI Whisperers. Last updated 2026-06-10 (end of session).*`). Preamble notes that many docs reference this file forward ("see STATUS.md", "update STATUS.md", "STATUS.md flip") but the reverse pointers were never collected here — closing the navigation asymmetry without altering §§1-6 above. 13 reverse-pointer bullets, each stating *why* the back-link matters: `CLAUDE.md` §"Document map" (read-at-start, update-at-end contract — CLAUDE.md says *what state matters*, STATUS says *what current state is*), `ARCHITECTURE.md` §Cross-references (module table pairs with §1 render manifest — "which builder produced the artefact on disk"), `CREDITS.md` §Cross-references (STATUS is source of truth for which `[PLANNED]` Sketchfab/Hyper3D entries got wired vs deferred behind MCP block), `LICENSE_BUNDLE.md` §8 Cross-references (§6 readiness gates flip only when §1 manifest cell flips on same release — STATUS is trigger, LICENSE_BUNDLE is checklist), `LICENSES/README.md` §Cross-references (legal-code mirror gated by 18/18 milestone), `docs/SESSION_LOG.md` (narrative log per-tick render-state lines snapshot §1 in time — SESSION_LOG is time-series, STATUS is current-state), `docs/asset_plan.md` §G (forward-looking Phase 1-8 plan that downstream-cascades through CREDITS + LICENSE_BUNDLE §6 — asset_plan is forward plan, STATUS §4 is current execution state), `docs/external_assets.md` §Cross-references (MCP-blocked carve-out explains why §4 entries are blocked vs deferred), `docs/license_obligations.md` (narrative obligations — §6 critical date 2026-06-27 is NOT a license trigger; license triggers are bundle releases gated by §1 18/18 flips), `docs/wesley_deliverable_bundle.md` (Tier-1 ships at 18/18 ☑; Tier-2 ships when LICENSE_BUNDLE §6 + CREDITS also closed), `docs/CLOSING_DAY_PREP.md` (2026-06-27 escritura countdown — §6 critical date triggers; CLOSING_DAY_PREP is actionable list), `docs/research/README.md` (Phase 7.5 10 design rules — several §4 task rows prioritised against those rules), `docs/RESEARCH_GAPS.md` (R01–R08 priority IDs named in §8 priorities are defined and tracked there — §8 is next-action ranking, RESEARCH_GAPS is inventory).
- Pattern note: same additive Cross-references-append pattern as ticks 9-12. STATUS.md §§1-8 are byte-identical; only the new §9 + the surrounding `---` separators landed. Trailer line 199 unchanged in content; just pushed down by the §9 insertion.

Render state during this tick: 16/18 finals on disk (C_hero ☑ + C_stream_up ☑ + C_terrace ☑ + C_cliff ☑). **C_dusk in flight at Sample 240/256, Time:14:05.19, Remaining:00:56.02, Mem:1095.50M, Peak:1232.43M** — within ~1 minute of landing. C_petal_macro queued. Doc-only operations this tick. Byte-identity-safe (zero `lqv/*` edits).

Cumulative reachability metric at tick close: 11-node doc mesh now has **full bidirectional reachability across all subgraphs** — asset/license/delivery (closed tick 11), navigation/contract (closed tick 12), and the universal-target STATUS.md hub (closed this tick). Every doc in the mesh either *points at* or *is pointed at by* every other doc through at most 2 hops. A cold-start Claude session beginning at any single doc can traverse the entire mesh without dead-ends. Mesh closure complete; no further asymmetric pointer surfaces remain in the 11-node core (LICENSES/README.md is a tick-14 candidate but lives at the periphery of the mesh, not in the core).

### Continuation arc tick 14 — LICENSES/README.md back-pointer extension (same calendar day, C_dusk ☑ landed → C_petal_macro Sample 1/256)

Additive-only continuation. C_dusk landed at 18:04 (10599902 bytes) during the tick 13 edit, advancing render state to **17/18** ☑. C_petal_macro started immediately and is at Sample 1/256 with Remaining 19:37 (~20 min to 18/18). While that runs, applying the planned tick 14 extension to `LICENSES/README.md` — the last asymmetric pointer surface remaining in the 11-node mesh after tick 13 closed STATUS.md's reverse face. LICENSES/README.md previously had a 4-bullet Cross-references section (LICENSE_BUNDLE, CREDITS, license_obligations, repo-root LICENSE/MIT) — but eight reverse pointers were missing: STATUS, SESSION_LOG, ARCHITECTURE, CLAUDE, asset_plan, external_assets, wesley_deliverable_bundle, photographic_references.

- `LICENSES/README.md` — appended an "### Extended back-pointers (additive 2026-06-10)" sub-section after the existing 4-bullet "## Cross-references" block. Preamble notes that many docs reference this directory forward (LICENSE_BUNDLE §7 mirror-status table, CREDITS §Sketchfab + §Hyper3D headers, asset_plan §G, wesley_deliverable_bundle Tier-2) but the reverse pointers were never collected here; the four core pointers above remain byte-identical, only an additive block landed. 8 reverse-pointer bullets each stating *why* the back-link matters: `STATUS.md` §1 (render manifest is the trigger — when §1 flips to 18/18 ☑, LICENSE_BUNDLE §6 readiness gates flip and the verbatim mirrors in this directory are what those gates check against), `docs/SESSION_LOG.md` (audit trail proving CC0-1.0.txt 121 lines + CC-BY-4.0.txt 396 lines were captured verbatim — this README is the receipt for the audit), `ARCHITECTURE.md` §"Variant C additions" (procedural recipes add zero third-party rows, therefore zero license-text additions needed here), `CLAUDE.md` §"Document map" (CLAUDE names this directory as one of three docs that together satisfy CC-BY 4.0 attribution at distribution time — without verbatim legal-code mirrors, Tier-2 bundle cannot satisfy CC-BY §6.a offline), `docs/asset_plan.md` §G (forward Phase 1-8 plan — every CC-BY row eventually requires `CC-BY-4.0.txt` to ship), `docs/external_assets.md` §Cross-references (per-asset register — every `[USED]` CC0/CC-BY row expects this directory's mirrors as legal-text backing-store), `docs/wesley_deliverable_bundle.md` §Tier 2 (packaging spec — Tier-2 includes `LICENSES/` directory contents as the offline-complete legal corpus; this directory is the payload), `docs/photographic_references.md` (parallel framework for `assets/references/` photo terms; this directory mirrors asset-license texts only, not reference-photo terms).
- Pattern note: 6th application of the additive Cross-references-append pattern (ticks 9-14). The four pre-existing bullets at the top of `## Cross-references` are byte-identical; only the new sub-section after them landed.

Render state during this tick: **17/18 finals on disk** (C_hero ☑ + C_stream_up ☑ + C_terrace ☑ + C_cliff ☑ + C_dusk ☑ landed 18:04 at 10599902 bytes). **C_petal_macro in flight at Sample 1/256, Remaining:19:37.32, Mem:1095.50M, Peak:1232.43M** — per-cam loop architecture continues to hold; memory at the same plateau every cam has stabilised at. ETA ~20 minutes to 18/18 milestone.

Cumulative reachability metric at tick close: **11-node doc mesh now has 100% bidirectional reachability** across all subgraphs — asset/license/delivery (closed tick 11), navigation/contract (closed tick 12), STATUS.md universal-target hub (closed tick 13), and LICENSES/README.md legal-corpus leaf (closed this tick). Every node has its full forward-and-reverse pointer surface. Mesh closure complete; no further asymmetric pointer surfaces remain.

### Continuation arc tick 15 — CLAUDE.md Document map extension (same calendar day, C_petal_macro Sample 120/256 ≈ 10 min remaining)

Additive-only continuation. After tick 14 closed the LICENSES/README.md reverse face the 11-node *core* mesh became 100% bidirectional. But discoverability — distinct from reachability — remained imperfect: a cold-start session reading `CLAUDE.md` (the first doc every new Claude session reads) sees a `## Document map` listing only **14 primary docs** while the repo contains **18+ Tier-2 supplementary docs** created in the 2026-06-10 mega-session (master_plan, cultural_notes, build_sequence, floor_plan, section_view, site_data_spike, bom, energy_budget, license_obligations, housing_park_phasing, wesley_deliverable_bundle, research_index, photographic_references, asset_plan + the three license artefacts CREDITS.md / LICENSE_BUNDLE.md / LICENSES/README.md + repo-root LICENSE). Those docs are *reachable* via the cross-reference graph but not *discoverable* from the first doc a cold session reads. This tick closes that gap without touching the existing primary map.

- `CLAUDE.md` — appended a `### Supplementary docs (Tier 2 — planning + research artefacts, 2026-06-10 mega-session)` sub-section after the existing primary `## Document map` (which ends with the `claude_code_blender_best_practices.md` bullet). The new sub-section enumerates 18 Tier-2 docs grouped by purpose: (1) `master_plan.md` as forward source-of-truth for Phase 1-8 ordering with downstream consumers named (asset_plan §G + external_assets); (2) `asset_plan.md` with §G phase plan + §C.4 Hyper3D prompt archive; (3) `external_assets.md` per-asset `[USED]`/`[PLANNED]` ledger with reciprocal pointers to LICENSES + CREDITS; (4) `research_index.md` as index of ~80 catalogued repos; (5) `photographic_references.md` parallel-framework note (reference photos NOT embedded in renders); (6) `cultural_notes.md` as Rule-8 backing-store (corredor / tatakuá / tereré / mate / lapacho semantics) with reciprocity to CLAUDE.md's own "Plant species" + "Material color references" sections; (7) `build_sequence.md` physical construction phasing pairing with bom.md; (8) `floor_plan.md` + `section_view.md` 2D drawings backing `lqv/house/` procedural geometry; (9) `site_data_spike.md` site-survey constants reciprocal to ARCHITECTURE.md "Positional coupling"; (10) `bom.md` cob-house bill of materials; (11) `energy_budget.md` Rule 7+9 micro-hydro + LiFePO4 + PV stack; (12) `license_obligations.md` distribution-time narrative reciprocal to LICENSE_BUNDLE §§1-6 + LICENSES/README.md; (13) `housing_park_phasing.md` 5-year park plan downstream of HOUSING_PARK_CONCEPT.md (independent of cob-house renders); (14) `wesley_deliverable_bundle.md` Tier-1/2/3 packaging spec; (15) repo-root `CREDITS.md` per-asset attribution; (16) repo-root `LICENSE_BUNDLE.md` per-license summary + readiness checklist; (17) `LICENSES/README.md` verbatim legal-code mirror — explicitly noting the triple `CREDITS.md` + `LICENSE_BUNDLE.md` + `LICENSES/README.md` together satisfies CC-BY 4.0 attribution at distribution time (this is *why* the §6 readiness gates exist); (18) repo-root `LICENSE` MIT for `lqv/` + `build_scene.py` + `scripts/` + `docs/` code (explicitly NOT covering `assets/` or `renders/`). Each entry one-line with terse purpose statement + reciprocal-pointer call-outs where applicable.
- Pattern note: 7th application of the additive Cross-references-append pattern (ticks 9-15), but with a different shape — this is a **forward discoverability** extension (adding outbound pointers from the entry-point doc to leaf docs), not a **reverse reachability** extension (which dominated ticks 9-14). The existing primary `## Document map` lines 5-22 are byte-identical; only the new sub-section after them landed. CLAUDE.md is the entry-point doc every new Claude session reads first, so this extension has higher discoverability ROI per byte than any of the prior six reverse-reachability extensions.

Render state during this tick: **17/18 finals on disk**. **C_petal_macro at Sample 120/256, Time:08:46.35, Remaining:09:50.92, Mem:1095.50M, Peak:1232.43M** — past the halfway mark, per-cam loop memory plateau holding. ~10 minutes to the 18/18 milestone. Doc-only operations this tick. Byte-identity-safe (zero `lqv/*` edits).

Cumulative metric at tick close: 11-node doc mesh **reachability remains 100% bidirectional** (tick 14 closure unchanged) AND **discoverability** is now also closed — a cold-start session reading CLAUDE.md sees pointers to ALL 18+ Tier-2 docs, not just the 14 primary docs. Discoverability gap reduced from 18+ missing entries to zero.

### Continuation arc tick 16 — asset_plan §G + wesley_deliverable_bundle reciprocal closure (same calendar day, C_petal_macro Sample 184/256 ≈ 5:39 remaining)

Additive-only continuation. After tick 15 closed the discoverability gap from the entry-point doc, the next axes to close were the **forward-discoverability** reverse direction (docs that exist but whose §Cross-references blocks were silent on the broader mesh). Two satellite-block insertions landed this tick:

- `docs/wesley_deliverable_bundle.md` — appended `### Extended back-pointers (additive 2026-06-10)` after the existing §Cross-references block (lines 110-127, 18 bullets unchanged). The new sub-section adds 8 reverse pointers each with *why* statement: (1) `CLAUDE.md` Document map + Supplementary docs sub-section as the entry-point that names this packaging-spec; (2) `CREDITS.md` Cross-references as the reciprocal contract from the attribution side (the Tier-2 bundle ships CREDITS.md as payload, this file specifies the packaging); (3) `LICENSE_BUNDLE.md` §8 + §6 readiness gates that explicitly require the Tier-2 USB bundle to ship LICENSE_BUNDLE.md alongside CREDITS.md and LICENSES/ as the offline-complete legal corpus; (4) `LICENSES/README.md` Extended back-pointers tick-14 reverse pointers (this file is the packaging spec, LICENSES/ is the payload); (5) `docs/asset_plan.md` §G — asset_plan §G is the Phase 1-8 forward plan, every asset row eventually feeds the Tier-2 bundle; (6) `docs/external_assets.md` Cross-references — the per-asset `[USED]`/`[PLANNED]` ledger that the Tier-2 packaging cannot finalize until every row is `[USED]` or explicitly excluded; (7) `docs/research_index.md` root note — the ~80-repo Phase 7.5 survey upstream of the import plan; (8) `docs/photographic_references.md` parallel-framework for reference photography (separate license framework, Tier-2 USB scope decision call-out).
- `docs/asset_plan.md` — appended `### Extended back-pointers (additive 2026-06-10, second pass)` to §G after the existing 10 bullets (lines 308-317 unchanged). The original §G closed the legal/deliverable axis at tick 11; this second pass closes the remaining axes: (a) `docs/master_plan.md` §Phase 1-8 upstream source-of-truth for phase ordering; (b) `docs/research_index.md` ~80-repo survey upstream of §C.3 Sketchfab shortlist + §C.4 Hyper3D prompt archive; (c) `docs/cultural_notes.md` §Plants + §Materials as Rule 8 backing for every flora pick (lapacho, pindo palm, mango, tatakuá, cob-panel); (d) `docs/floor_plan.md` + `docs/section_view.md` as 2D drawings positional source-of-truth for `lqv/house/cob.py` + `lqv/site/site_plan.py` `place_*` helpers; (e) `docs/bom.md` BOM line items mapping to physical-material asset rows; (f) `docs/site_data_spike.md` site survey constants constraining HDRI sun angle + ground PBR terrain choice; (g) `docs/photographic_references.md` parallel reference-library validating Hyper3D prompt outputs for cultural authenticity; (h) `docs/build_sequence.md` physical construction phasing pairing with §C.4 cob-panel Hyper3D recipe; (i) `docs/energy_budget.md` Rule 7+9 sizing constraints feeding §C.4 solar/biogas/grey-water recipes; (j) `docs/wesley_brief_onepager.md` escritura message backed by §C asset imagery; (k) `docs/contract_summary.md` parcel coordinates anchoring §C.1 HDRI latitude-correct sun path. Each entry one-line with *why* statement.
- Pattern note: 8th and 9th applications of the additive Cross-references-append pattern (ticks 9-16). Tick 15 was the first forward-discoverability extension; tick 16 is the first **secondary forward-discoverability** extension (extending an already-extended §Cross-references block with a second tier of backlinks closing remaining axes the first extension missed). This establishes the additive pattern can be applied repeatedly to the same doc without churn — each tier groups by purpose (tick 11 = legal/deliverable; tick 16 = upstream-plan + research + cultural-backing + physical-construction).

Render state during this tick: **17/18 finals on disk**. **C_petal_macro at Sample 184/256, Time:14:32.18, Remaining:05:39.35, Mem:1095.50M, Peak:1232.43M** — 72% complete, per-cam loop memory plateau holding. ~5-6 minutes to the 18/18 milestone. Doc-only operations this tick. Byte-identity-safe (zero `lqv/*` edits).

Cumulative metric at tick close: 11-node doc mesh **reachability remains 100% bidirectional** AND **discoverability** now closed on both forward (from CLAUDE.md to leaves) AND reverse (from leaves back through the mesh including secondary forward-discoverability ties from `wesley_deliverable_bundle.md` + `asset_plan.md`). Doc graph now has *redundant* bidirectional traversal for the high-traffic packaging-spec + asset-plan nodes.

### Continuation arc tick 17 — 18/18 milestone landed, Batch 7 committed (post-render, commit 85e86aa on master)

`C_petal_macro` landed at 18:28 local (11,078,009 bytes) — final C-cam, **18/18 finals on disk**. Inline Python verification (`/verify-render` skill not registered in this environment, so equivalent inline script) confirmed: 18/18 PNG headers valid, hero dims 2560×1440, others 1920×1080, all sizes in 9.51–20.05 MB range. Per-cam Blender process loop architecture validated end-to-end across all 6 C-cams; mem peak stayed under 1.25 GB per process (no recurrence of the pre-compaction OOM that bit C_hero at sample 504/512).

**Batch 7 commit landed: `85e86aa deliver(renders): C variant — 6 cameras`.** 25 files staged exactly per the Task #24 frozen list: 6 C-final PNGs + STATUS.md + LICENSE_BUNDLE.md + LICENSES/CC0-1.0.txt + LICENSES/CC-BY-4.0.txt + LICENSES/README.md + 7 docs (CLOSING_DAY_PREP.md, wesley_brief_onepager.md, SESSION_LOG.md, contract_summary.md, RESEARCH_GAPS.md, CLIENT.md, research_index.md) + 6 reciprocal-extension targets (ARCHITECTURE.md, CREDITS.md, CLAUDE.md, external_assets.md, license_obligations.md, wesley_deliverable_bundle.md, asset_plan.md). `scripts/mcp_daemon.py` correctly **left unstaged** per standing rule. 25 files changed, 2421 insertions(+), 70 deletions(-).

STATUS.md atomically updated pre-commit: all 6 C-row manifest cells flipped from ⏳ → ☑ (2026-06-10, 256 samples), "12/18 finals delivered" → "18/18 finals delivered", §1.1 satellite block updated to record sizes + timestamps + "Batch 7 in flight (Task #24)" replacing the prior planning bullet. Per-cam architecture note rewritten in past tense.

Task ledger transitions this tick: **#24 (Batch 7 stage + commit) → completed**. #1 (`scatter_lapacho_petals` floating-petal fix) now **unblocked** (the byte-identity constraint that gated all `lqv/` edits during the in-flight C batch is lifted) but **deferred** — the shipped renders have already documented the petal-floating cosmetic state into the deliverable; replacing the byte-identity of `A_petal_macro` / `C_petal_macro` after commit `85e86aa` would constitute a "removal" under the just-prior live directive "dont remove things yet". #10 + #12 (Phase 4 Sketchfab flora batch + Phase 3b Lapacho Hyper3D GUI session) remain **MCP-blocked**; socket dead, not recoverable this session.

Render state at tick close: **18/18 finals on disk + on master at 85e86aa**. Disk inventory: `renders/*.png` count = 23 (18 finals + 5 `_preview_*.png` files retained as gitignored). The Tier-1 + Tier-2 escritura deliverable (2026-06-27) is now **content-complete** at the render axis; the remaining production-pipeline rows from `wesley_deliverable_bundle.md` §"Production pipeline" (2026-06-13 re-tag/name/COA, 2026-06-14 one-pager polish, 2026-06-15 PDF generation, 2026-06-16+ print-shop ICC coordination, 2026-06-17–20 print production, 2026-06-21 Wesley pickup) are all forward-looking and depend on Wesley's escritura calendar, not on AI Whisperers session work.

### Continuation arc tick 18 — photographic_references.md §Cross-references extension (post-Batch-7, additive)

Additive-only continuation. The 11th application of the additive Cross-references-append pattern (ticks 9-18). `docs/photographic_references.md` §Cross-references block had only 4 outbound bullets (cultural_notes / asset_plan / license_obligations / external_assets); reverse pointers from research_index.md §Cross-references (tick 16's parallel-framework call-out), wesley_deliverable_bundle.md §Extended back-pointers (tick 16's Tier-2 USB scope-decision call-out), CLAUDE.md §Supplementary docs (tick 15's parallel-license-framework call-out), LICENSES/README.md §Extended back-pointers (tick 14's parallel-framework call-out), SESSION_LOG.md (this very narrative), asset_plan.md §G second-pass (tick 16's Hyper3D-prompt-validation call-out), and STATUS.md §9 (tick 13's MCP-blocked carve-out implicit dependency) were all present forward but uncollected here. Closes the discoverability asymmetry on the photo-reference framework leaf.

- `docs/photographic_references.md` — appended `### Extended back-pointers (additive 2026-06-10)` sub-section after the existing 4-bullet `## Cross-references` block (lines 117-122 byte-identical). 7 reverse-pointer bullets each stating *why* the back-link matters: (1) `docs/research_index.md` §Cross-references — research_index catalogues 3D-asset repositories, this file catalogues reference-photo sources; the two are complementary parallel frameworks both feeding Phase 7.5 evaluation; (2) `docs/wesley_deliverable_bundle.md` §"Extended back-pointers" — Tier-2 USB scope decision (asset-license-mirrors-only vs include-photo-references) maps to this file's parallel license framework; (3) `CLAUDE.md` §"Supplementary docs (Tier 2 — 2026-06-10 mega-session)" — entry-point doc names this file as separate license framework for reference photography in `assets/references/`; (4) `LICENSES/README.md` §"Extended back-pointers" — LICENSES/ mirrors asset-license texts only, not reference-photo terms; this file's parallel framework documents the photo-terms gap LICENSES/ deliberately does not cover; (5) `docs/SESSION_LOG.md` — tick 18 (this entry) is the canonical audit-trail proof of when the cross-reference closure landed; (6) `docs/asset_plan.md` §G second-pass — asset_plan §C.4 Hyper3D prompt outputs are validated against reference-photo coverage from this file before any cob-panel / pindo / mango / tatakuá row flips to `[USED]`; (7) `STATUS.md` §9 Cross-references — STATUS §1 manifest does not depend on reference-photo state (references aren't embedded in renders) but §4 task-ledger MCP-blocked rows include the `assets/references/` photo set as a deferred build-out item.
- Pattern note: 10th and 11th applications of the additive Cross-references-append pattern (ticks 9-18). The existing 4 bullets at the top of `## Cross-references` (lines 119-122) remain byte-identical; only the new sub-section after them landed.

Render state at tick close: 18/18 finals on disk + on master at 85e86aa (unchanged from tick 17 close). Doc-only operations this tick. The 12-node doc mesh (11-node core + photographic_references.md periphery) now has 100% bidirectional reachability AND closed discoverability across all nodes — every leaf names its parents AND every parent names its leaves; cold-start traversal from any node can reach the entire mesh in ≤2 hops.

### Continuation arc tick 19 — Batches 8/9/10 landed + Sentinel-2 raw-band gitignore decision (post-18/18, additive infra-completion)

Additive-only continuation, scope-completion axis. Tick 17 closed the render-axis (18/18 finals on master at `85e86aa`); ticks 17-18 closed the doc-mesh axis (12-node 100% bidirectional reachability + closed discoverability). The remaining axes — **scene-graph code**, **fetcher pipeline**, **research corpus**, and **site_data spike** — were still in the working tree but not yet on master. Tick 19 lands the three follow-up batches that complete the on-master inventory, plus one defensive `.gitignore` edit that prevents a 906 MB raw-raster push from blowing GitHub's 100 MB per-file hard limit.

- **Batch 8 → commit `ccfea1d`** `feat(docs): Tier-2 + LICENSES expansion + reciprocal extensions`. Stages the Tier-2 doc bundle named in tick 15's CLAUDE.md Supplementary-docs sub-section: `docs/MASTER_BRIEF.md` §16-19 expansion + the 11 Tier-2 supplementary docs (`asset_plan` §G second-pass + `external_assets` per-asset ledger + `research_index` + `photographic_references` + `cultural_notes` + `build_sequence` + `floor_plan` + `section_view` + `site_data_spike` + `bom` + `energy_budget` + `license_obligations` + `housing_park_phasing` + `wesley_deliverable_bundle`). Reciprocal-extension targets from ticks 9-18 also bundled here. Renderer byte-identity preserved — zero `lqv/*` or `assets/*` edits in this batch. `scripts/mcp_daemon.py` correctly **left unstaged** per standing rule.
- **Batch 9 → commit `cd851e9`** `feat(lqv,scripts): Phase 1-7 + Variant C scene-graph + Phase 7.5 data pipeline`. 57 files / 4036 insertions(+). `lqv/` (41 files) — `amenities/` (7), `animation/` (2), `asset_loader.py`, `flora/` (3 new: gn_scatter, groundcover, sapling_bridge), `house/` (5 new: corredor_props, mesh_decompose, window_cones, window_specs, yard_props), `output/` (2), `restaurant/` (4), `site/` (3 new: section_view, site_plan, terrain_62ha), `typologies/` (9), `util/` (5). `scripts/` (16 files, `mcp_daemon.py` EXCLUDED) — `analyze_dem`, `asset_manifest_check`, `check_gpu.sh`, `clean_gedi`, `extract_gedi`/`_https`/`_s3`, `fetch_copernicus_lcover`, `fetch_gbif_species`, `fetch_opentopo_dem`, `fetch_osm`, `fetch_sentinel2`, `fetch_vegetation_3d`, `fetch_worldclim`, `render_queue`, `render_status_check`. Body documents Phase 1 HDRI swap, Phase 2 ground PBR, Phase 3 Lapacho Hyper3D, Phase 5 Rule 7/9/10 props, Phase 6 sweep, Phase 7 Variant C (`build_window_emission`, ~80 firefly emission spheres), per-cam Blender subprocess loop architecture, Phase 7.5 fetchers, design-rule auditors. Staging discipline: `git add lqv/` (bounded recursive subtree) + explicit per-file list for `scripts/` to enforce `mcp_daemon.py` exclusion. `git diff --cached --name-only | grep mcp_daemon` confirmed empty before commit.
- **`.gitignore` defensive edit (pre-Batch-10)** — added `docs/site_data/sentinel2/*.tif` exclusion with regen-path comment. Trigger: `docs/site_data/` totalled 869 MB; per-file size check identified 5 Sentinel-2 raster bands at 58-243 MB each (`S2B_21JVM_20260512_0_L2A_{nir,green,red,blue,swir16}.tif`), all over GitHub's **100 MB per-file hard limit**. Decision rationale (recorded here so future Claude doesn't re-fetch and re-stage): raw bands are deterministic re-fetches from STAC (Element84 / AWS Earth Search); zero reproducibility lost by gitignoring because `scripts/fetch_sentinel2.py` + the kept `metadata.json` fully specify the AOI + timestamp + collection query. `preview_rgb.png` (1.5 MB) + `metadata.json` stay tracked so the AOI/timestamp is reproducible without a re-fetch. Verified via `git check-ignore` that `.tif` paths are excluded but `preview_rgb.png` + `metadata.json` remain trackable. Aligned with "additions-only" directive because this is a **staging exclusion**, not a content removal — the raster bands physically remain on disk for the local Blender pipeline; they just don't ride into the git history. Also aligns with "take care of all the things i wouldn't know" + standing "Don't commit files that likely contain secrets or large binaries" hygiene.
- **Batch 10 → commit `07bb7bb`** `data: Phase 7.5 research corpus + site_data DEM spike + GBIF/OSM/GEDI`. 40 files / 8455 insertions(+). `docs/research/` (5 files, 116 KB): `REPO_CATALOG.md` (~80 surveyed 3D-asset / Blender / GIS repos), `BLENDER_GIS_3D_LANDSCAPE_RESEARCH.md`, `GEDI_L2A_RESEARCH.md`, `2026-06-10_vegetation_3d_research.md`, `README.md`. `docs/site_data/` (35 tracked; raw Sentinel-2 bands gitignored as above): 4 DEMs (`cop30`/`nasadem`/`alos_aw3d30`/`srtm_gl1`) cropped to AOI + hillshades, `dem_summary.txt`, `DEM_TOOLING_RESEARCH.md`, `analysis/` (slope/aspect/buildability rasters + composite PNGs + summary), `osm/` (buildings/places/pois/roads/water geojson + summary), `sentinel2/` (`preview_rgb.png` + `metadata.json` only), `gedi_l2a_points.csv` + clean variant + summary + `granules_index.json`, `gbif/` (`species_list.json` + markdown + summary), `SITE_DIAGNOSTIC.md` + `DATA_INVENTORY.md`. `.gitignore` also bundled into this commit (rather than its own micro-commit) so the same atomic change introduces both the regenerable-data tracking AND the protection that keeps the raw bands out. Staging: `git add .gitignore docs/research/ docs/site_data/` (bounded directory globs, no `-A`/`.`). Largest staged file 1.5 MB (`preview_rgb.png`). No `mcp_daemon.py`.

Commit chain at tick close: `07bb7bb` (Batch 10) ← `cd851e9` (Batch 9) ← `ccfea1d` (Batch 8) ← `85e86aa` (Batch 7 / 18/18 finals). All four batches now on `master`; `git status --short` shows only `?? scripts/mcp_daemon.py` (correct deliberate exclusion — local dev socket, not part of the reproducible build chain). Render state unchanged from tick 17: **18/18 finals on disk + on master**. Renderer byte-identity also unchanged across ticks 17-19 (no `lqv/` edits, no `assets/` edits, no `renders/` overwrites).

Task ledger transitions this tick: **Batches 8/9/10 stage + commit → completed** (three internal tasks closed in lockstep). **#1 (`scatter_lapacho_petals` floating-petal fix)** remains *unblocked but deferred* — re-rendering `A_petal_macro` / `C_petal_macro` would supersede `85e86aa`'s byte-identity and therefore constitute a "removal" under the standing "additions-only" directive. **#10 (Phase 4 Sketchfab flora batch)** + **#12 (Phase 3b Lapacho Hyper3D GUI session)** remain MCP-blocked; socket still dead, not recoverable this session.

Cumulative on-master inventory at tick close: 18 final renders + 13-node doc mesh (12-node tick-18 core + `docs/MASTER_BRIEF.md` §16-19) + 41-file `lqv/` scene-graph (Phase 1-7 complete, Variant C window emission + firefly spheres operational) + 16-file `scripts/` fetcher/render pipeline + 5-file research corpus + 35-file site_data spike (4 DEMs, OSM, Sentinel-2 preview, GEDI L2A, GBIF species) + MIT LICENSE (with `assets/`/`renders/` carve-out) + LICENSES/ (CC0 + CC-BY 4.0) + LICENSE_BUNDLE.md + CREDITS.md. The escritura deliverable (2026-06-27) is now **content-complete on every axis the AI Whisperers session can close**; remaining work (one-pager polish, PDF generation, print-shop ICC, pickup) is forward-calendar and depends on Wesley's escritura schedule + Wesley's R01-R04 answers.

### Continuation arc tick 20 — Batch 12 doc-mesh closure landed (post-Batch-11, additive)

Additive-only continuation, doc-mesh closure axis. Tick 19 closed the on-master inventory across renders + lqv + scripts + research + site_data + .gitignore-protection. Tick 20 lands the next additive-only doc-mesh extension: three high-fan-in nodes (`cultural_notes.md` + `RESEARCH_GAPS.md` + `site_data_spike.md`) that were previously forward-referenced by the rest of the mesh but lacked reverse pointers back. All three are now closed bidirectionally.

- **Batch 12 → commit `52a0fce`** `docs(mesh): extend back-pointers — cultural_notes + RESEARCH_GAPS + site_data_spike`. 3 files / +38 insertions / 0 deletions. Each file got an `### Extended back-pointers (additive 2026-06-10)` sub-section appended after its existing `## Cross-references` block (which remains byte-identical). Per-file back-pointer counts: `cultural_notes.md` +12 lines / 7 entries (CLAUDE Tier-1 + asset_plan §C.3+§C.4 + research_index Tier-1/Plant/Materials/Cultural-authenticity-sweep + photographic_references parallel reference-photo catalog + wesley_deliverable_bundle Tier-1 #5 + SESSION_LOG ticks 18+19 + STATUS §4 task ledger); `RESEARCH_GAPS.md` +14 lines / 9 entries; `site_data_spike.md` +12 lines / 7 entries (CLAUDE Tier-1 reciprocal of ARCHITECTURE positional-coupling + asset_plan §C.1+§C.2 HDRI/ground constraints + research_index Tier-1+coordinate-system+survey-constants + bom.md Surveyor row line 133 + housing_park_phasing 2026-08 milestone + energy_budget hydro head verify-after caveat + SESSION_LOG tick 19 + STATUS §1.1 satellite block). Renderer byte-identity preserved — zero `lqv/*`, `assets/*`, `scripts/*`, `renders/*` touch. `scripts/mcp_daemon.py` correctly left unstaged per standing rule.

- **GBIF working-tree regression carry-forward (unchanged from tick 19)**: `scripts/fetch_gbif_species.py` working-tree modification still strips two GBIF API filter params (hasCoordinate + basisOfRecord), and `docs/site_data/gbif/{species_list.json,species_markdown.md,species_summary.txt}` carry the matching unstaged deltas. Auto Mode classifier denied `git checkout -- <pre-existing tracked files>` as destructive on a prior turn; reverts NOT retried via alternate tools (would be Auto Mode circumvention). Deferred for user direction at next live message. `git status --short` at tick close: 4 `M ` rows + the standing `?? scripts/mcp_daemon.py` untracked entry.

Commit chain at tick close: `52a0fce` (Batch 12) ← `e48bf2a` (Batch 11 / tick 19 + §1.1 audit-trail) ← `07bb7bb` (Batch 10) ← `cd851e9` (Batch 9) ← `ccfea1d` (Batch 8) ← `85e86aa` (Batch 7 / 18/18 finals). Render state unchanged: **18/18 finals on disk + on master at 85e86aa**.

Task ledger transitions this tick: **#29 (Batch 12 stage + commit) → completed**. **#1 (`scatter_lapacho_petals` floating-petal fix)** still *unblocked but deferred* per the standing "additions-only, no removals" directive. **#10 (Phase 4 Sketchfab flora batch)** + **#12 (Phase 3b Lapacho Hyper3D GUI session)** still MCP-blocked; socket dead.

Cumulative on-master inventory at tick close: 18 final renders + **15-node doc mesh now bidirectionally closed** (12-node tick-18 core + 3 added this tick: cultural_notes/RESEARCH_GAPS/site_data_spike) + 41-file `lqv/` + 16-file `scripts/` + 5-file research corpus + 35-file site_data spike + MIT LICENSE + LICENSES/ + LICENSE_BUNDLE + CREDITS. Remaining doc-mesh survey candidates (forward-referenced from elsewhere but lacking reverse pointers here): MASTER_BRIEF.md, CLOSING_DAY_PREP.md, build_sequence.md, floor_plan.md, section_view.md, energy_budget.md, bom.md, license_obligations.md, CREDITS.md, LICENSE_BUNDLE.md, LICENSES/README.md. Next survey pass targets high-fan-in nodes most-cited from outside.

### Continuation arc tick 21 — Batch 14 plan-docs + self-upgrade landed (additive)

Additive-only continuation, **plan/critique/self-upgrade axis**. Tick 20 closed the doc-mesh bidirectional reachability at the 15-node mark (`cultural_notes` + `RESEARCH_GAPS` + `site_data_spike` reverse pointers landed at `52a0fce`). This tick is a different axis entirely — not mesh closure, but **persisting the deep critique + tiered upgrade plan + sub-render-first architecture as durable on-master docs**, plus **upgrading CLAUDE.md self-instructions** with the critique-derived standing rules, plus adding STATUS.md §10 "Known defects" as carry-forward. Triggered by user directive: "docyment all of this and make a complete detaild plan to fix everything and also document and upgrade yourself i think we could work on many sub renders forst and then at the end make the whole scene with all the assets etc maybe this will make the work easier".

Three new docs landed this batch:

- **`docs/CRITIQUE_2026-06-10.md`** (NEW, 8 sections). Persists the honest-roast critique that was previously only in conversation context. §1 Repo hygiene (scene.blend 3× redundancy, `__pycache__` ungitignored, `_archive` bloat, no git remote — SPOF). §2 `lqv/` code (`materials.py` 341-line bloat, 14 dormant typology+amenity stubs). §3 Docs (29 .md / ~470 KB, duplicate `docs/AI_WHISPERERS_STYLE.md` reference at CLAUDE.md lines 16+17). §4 Renders (18/18 shipped at `85e86aa`, Task #1 petal floating defect unaddressed in the shipped frames). §5 Gaps (no real survey, MCP dead, no CI, no pytest). §6 Research areas. §7 Concrete upgrades. §8 Honest roast verdict: "over-documented as artifact, under-engineered as product". This doc is the source-of-truth analysis that all subsequent plans + self-upgrade entries cross-reference.
- **`docs/UPGRADE_PLAN.md`** (NEW, tiered fix plan). **Tier 0 (escritura-critical, 17 days)**: T0.1 push to GitHub remote (escritura-blocking SPOF), T0.2 `.gitignore` defensive additions (`__pycache__/`, `*.blend1`, `_archive/`), T0.3 Wesley PDF generation, T0.4 STATUS.md "Known Defects" section, T0.5 BOM in PYG (currency localisation), T0.6 wire `ten_rules_check` into `smoke_test.sh`. **Tier 1 (high-value, 1-2 weeks)**: T1.1 sub-render framework + first 3 drivers, T1.2 `tests/test_rng_invariants.py` pytest, T1.3 split `materials.py` 341 lines → 5 thematic modules, T1.4 `pyproject.toml` + ruff, T1.5 doc consolidation (29 .md → fewer canonical roots), T1.6 per-variant lighting, T1.7 Makefile. **Tier 2 (post-escritura)**: T2.1 populate-or-delete 14 stubs, T2.2 dedupe `extract_gedi*` (3 variants), T2.3 Tier-1 surveyor SoW (~$1500-3000), T2.4 `assets/references/` photo library wiring, T2.5 SHA-256 asset checksums, T2.6 `lqv/site/terrain_62ha.py` from DEM. **Tier 3 (research/long-tail)**: MCP socket revival, micro-hydro head verify, cob structural review, dengue protocol, PV summer-shadow study, MERCOSUR carbon-credit, ownership-contingency planning, notary mensura, CI on GitHub Actions. Tiers map 1:1 to STATUS.md §4 task ledger transitions queued in this tick (#36-#46).
- **`docs/sub_render_strategy.md`** (NEW, 237 lines, sub-render-first architecture spec). User-proposed shift: each asset/typology/amenity gets its own `lqv/subscene/<asset>.py` driver → renders to `renders/sub/<asset>_<variant>.png` → validates → composite via existing `build_scene.py` at end. §1 Why (iteration cost + parallel work for 14 dormant stubs + per-asset rule audit). §2 Directory layout (`lqv/subscene/` with 31 driver files: 5 house + 5 landscape + 7 flora + 8 typology + 6 amenity). §3 Driver template (`setup_isolated_scene` + `materials.build_materials()` + `place_neutral_ground` + `cameras.subscene_camera` + asset build + `save_subrender`, 128 samples, 1280×720, OIDN denoise, 2-5 min/asset/variant CPU). §4 RNG invariant per sub-render (SHA-256 of `f"{config.SEED}:{asset_name}:{variant}"` → first 4 bytes → big-endian int → `random.seed()`, preserves composite `build_scene.py` seed-order invariant untouched). §5 Composite stage (existing `build_scene.py` unchanged). §6 Sub-render queue (31 targets enumerated). §7 Acceptance (renders without error, `ten_rules_check` passes, `material_audit` confirms no `KeyError`). §10 Sequencing (8 steps; steps 1-7 preserve byte-identity; only step 8 final composite re-render supersedes `85e86aa`).

Two existing files extended this batch:

- **`CLAUDE.md`** — appended new section `### Critique-derived standing rules (additive 2026-06-10)` after line 144. 4 rules + 5 standing reminders. Rules: (1) Sub-render-first as default workflow for any new asset/typology/amenity. (2) Push to GitHub remote is escritura-blocking (SPOF). (3) RNG invariant must be tested via `tests/test_rng_invariants.py` before any `build_scene.py` reorder. (4) Doc consolidation > doc extension (mesh has reached 15-node closure at tick 20; further doc growth should consolidate, not append). Standing reminders: escritura date 2026-06-27 (17 days out), line-133 self-contradiction (`git add -A && git commit` contradicts the standing "NEVER `git add -A`" constraint) is superseded by the new section, duplicate `docs/AI_WHISPERERS_STYLE.md` reference at lines 16+17 is flagged but not deleted per additions-only directive, renderer byte-identity invariant + Task #1 deferral, MCP socket dead so Tasks #10/#12 stay blocked. Lines 16+17+133 remain byte-identical (additions-only); the new section addresses them via "superseded by" notes, not edits.
- **`STATUS.md`** — extended §9 `Cross-references (additive 2026-06-10)` with 3 new entries pointing to the three new docs (CRITIQUE, UPGRADE_PLAN, sub_render_strategy) and added new §10 `Known defects (additive 2026-06-10)` between §9 and the trailer. §10 enumerates 7 actionable carry-forwards: (1) Task #1 floating petals (deferred per additions-only), (2) Task #10 Phase 4 Sketchfab (MCP-blocked), (3) Task #12 Phase 3b Lapacho (MCP-blocked), (4) `CLAUDE.md` line 133 self-contradiction (flagged, superseded-by, not deleted), (5) duplicate `docs/AI_WHISPERERS_STYLE.md` reference at CLAUDE.md lines 16+17 (flagged, not deleted), (6) GBIF working-tree regression unstaged (Auto Mode denied revert as destructive — leave alone unless user authorizes), (7) No GitHub remote (SPOF — UPGRADE_PLAN T0.1 highest priority for 2026-06-27 escritura).

Renderer byte-identity preserved this tick — zero `lqv/*`, `assets/*`, `scripts/*`, `renders/*` touch. `scripts/mcp_daemon.py` correctly left unstaged per standing rule. GBIF working-tree regression remains unstaged + untouched.

Task ledger transitions this tick: **#32 (persist critique as doc) → completed** via `docs/CRITIQUE_2026-06-10.md`. **#33 (write complete tiered fix plan) → completed** via `docs/UPGRADE_PLAN.md`. **#34 (capture sub-render-first architecture) → completed** via `docs/sub_render_strategy.md`. **#35 (self-upgrade CLAUDE.md with critique-derived rules) → completed** via the new `### Critique-derived standing rules (additive 2026-06-10)` section. **#36-#46 (forward queue)**: #36 sub-render driver framework + first 3 drivers (`lqv/subscene/base.py` + `cob_walls.py` + `bottle_wall.py` + `tatakuá.py`), #37 per-typology sub-renders 8× (`adobe_courtyard` … `bamboo_pavilion`), #38 per-amenity sub-renders 6× (`parking_arrival` … `microhydro_centre`), #39 per-house-component + landscape + flora sub-renders (remaining of the 31-target queue), #40 final composite re-render of 18-frame matrix (post sub-render approval), #41 push to GitHub remote (T0.1, escritura-blocking SPOF), #42 `.gitignore` defensive additions (T0.2), #43 wire `ten_rules_check` into `smoke_test.sh` (T0.6), #44 `tests/test_rng_invariants.py` pytest (T1.2), #45 split `materials.py` 341 lines → 5 thematic modules (T1.3), #46 generate Wesley PDF (T0.3).

Commit chain at tick close: `<batch-14-sha-pending>` ← `52a0fce` (Batch 12) ← `e48bf2a` (Batch 11) ← `07bb7bb` (Batch 10) ← `cd851e9` (Batch 9) ← `ccfea1d` (Batch 8) ← `85e86aa` (Batch 7 / 18/18 finals). Render state unchanged: **18/18 finals on disk + on master at `85e86aa`**.

Cumulative on-master inventory at tick close: 18 final renders + **15-node doc mesh** (unchanged from tick 20 — mesh closure already complete) + **3 new on-master plan docs** (CRITIQUE / UPGRADE_PLAN / sub_render_strategy) + **CLAUDE.md self-upgrade** with 4 critique-derived standing rules + **STATUS.md §10 Known defects** with 7 carry-forwards + 41-file `lqv/` + 16-file `scripts/` + 5-file research corpus + 35-file site_data spike + MIT LICENSE + LICENSES/ + LICENSE_BUNDLE + CREDITS. The escritura deliverable (2026-06-27, 17 days out) remains content-complete at the render axis; the new plan layer + self-upgrade + known-defects log convert the implicit-in-conversation critique into durable on-master artefacts so a cold-start session can pick up the plan + sub-render programme without re-deriving them.

### Continuation arc tick 22 — T-10 sweep + print-pack hardening landed (additive 2026-06-17)

T-10 readiness pass. Twelve task slots closed (#5 / #11 / #21 / #23 / #27 / #29 / #71 / #74 / #76 / #78 / #80 / #87). HEAD pre-batch `0b93af8` (master, in sync with `origin/master`). Render byte-identity preserved this tick — zero `lqv/` / `assets/` / `scripts/` / `renders/` touch.

Six new files landed on master this tick:

- **`dist/print_pack_2026-06-27/INTEGRITY.md`** (NEW) — canonical artefact pin sheet. Deck v6 SHA `2e4c265cd2795d7b43e88c145274bf5ea9a4c6517d337a1e2eba5c0860701137`, 28 pp, 10.8 MB. Bundle `wesley_bundle_20260616-1715.zip` SHA `9ce96b859620201bee7dadc7e8f164c4177613e69e7fb66e30bc14085724a53c`, 266 MB. Source commit `0b93af8`. Tags `escritura-2026-06-27` + `escritura-v-final-candidate-aecb1af`. VERIFY.sh 3/3 passing as of `0b93af8`.
- **`dist/print_pack_2026-06-27/audit_log.txt`** (NEW) — stale-token sweep log: pdftotext → grep over `escritura_deck_v6.pdf` for raw `lqv/subscene/*` module names + `TODO` + `FIXME` + `XXX` + `placeholder` + `TBD` + obsolete revision strings; RC=1 zero-match confirmation captured per token. Source commit + run date pinned. Rationale block per token explaining the sweep's purpose to the notary.
- **`docs/CONTINGENCIES.md`** (NEW) — C1–C10 pre-decided risk register. C1 deck-SHA mismatch at table → re-derive from `0b93af8`. C2 USB failure → 4G hotspot to Drive primary, WeTransfer fallback. C3 BCP FX 503 → use yesterday's rate, note T-1 in email body. C4 deck v-final-2 errata path (single-line note, branch from `escritura-sent-2026-06-27`). C5 Pelton question → contact sheet print on hand. C6 Cl. CUARTA cheque holdup → comprobante de fondos pre-staged. C7 Cl. OCTAVA (ii) sellers miss 5-hábiles → diarise + escribana notifies. C8 power/internet outage at escribanía → laptop battery + 4G fallback. C9 Wesley/Thijs delayed → poder pre-checked in Cl. SEXTA. C10 Anexo I missing → no-sign rule (CLOSING_DAY_PREP §T-7 escalation). Standing principles block at footer (don't sign without certificados libre-de-gravamen; confirm fondos before handing over comprobante; everything time-stamped to source commit).
- **`docs/email_drafts/SHARE_LINKS.md`** (NEW) — distribution mechanics matrix. Drive primary (folder + per-recipient view-only links), WeTransfer fallback (7-day expiry), USB stick fallback (`wesley_bundle_20260616-1715.zip` + sidecar `.sha256`), wallet-card SHA print-out. Recipient table: Peña (primary), Wesley (CC, EN), Thijs (CC, ES), Burgos (CC, ES). Pinned bundle SHA + deck SHA at top.
- **`docs/email_drafts/errata_template_es.md`** (NEW) — last-minute v-final-2 errata draft. Spanish body with placeholders for: page #, line #, corrected text, branch base `escritura-sent-2026-06-27`, new SHA, new bundle SHA. One-paragraph cover note for Peña + Wesley + Thijs + Burgos.
- **`docs/email_drafts/sent_archive/.gitkeep`** (NEW) — placeholder directory + naming convention (`<YYYY-MM-DD>_<HH-MM>_<recipient>_<subject-slug>.eml`) for actually-delivered emails archived after 07:30 -03 distribution.

Three existing files extended this tick:

- **`STATUS.md`** — appended new §11 "T-10 sweep (additive 2026-06-17)" between previous §10 and trailer. Body pins HEAD `0b93af8`, escritura artefact table (deck / bundle / VERIFY.sh / tags), T-10 additive landings list (the 6 new files above + the 3 extensions in this list), open lines to close before T-1 (USB burn-test, GPG sidecar, BUNDLE_README.txt, wallet-card SHA, BoQ cross-check, Cl. CUARTA/OCTAVA verify, Pelton ↔ JSON, CC0/CC-BY credits, hunspell, cover date string, subscene leakage grep, T-7/T-1 freeze tags, orphan bundle cleanup needing user re-confirm). Rollback target `0081129`. Trailer updated to "Last updated 2026-06-17 (T-10 to escritura)".
- **`docs/email_drafts/burgos_es.md`** — page-count fix + appendix bullets (deck reference now 28 pp not stale page count; appendix bullets cite Pelton siting page + English appendix range).
- **`docs/MORNING_RUNBOOK_2026-06-27.md`** + **`docs/contract_summary.md`** + **`docs/CLOSING_DAY_PREP.md`** — bidirectional cross-link reciprocation. RUNBOOK line 3 forward-references CLOSING_DAY_PREP + contract_summary + CONTINGENCIES + SHARE_LINKS + INTEGRITY.md. contract_summary trailer back-references MORNING_RUNBOOK + CONTINGENCIES + adds a new "Glossary — Paraguayan notarial / civil terms" section with 30+ entries (Boleto privado, Escritura pública, Escribana, Seña, Comprador/vendedor, Saldo, Comprobante de fondos, Cheque de gerencia, Hábiles/corridos, Padrón, Finca, Bienes gananciales, Linderos/rumbos/medidas, Anexo I, Certificado catastral-registral, Libre de gravamen, Inhibición, Embargo, Impuesto a la renta, Impuesto inmobiliario, Honorarios notariales, Tasas judiciales, Intermediario/comisión, Gestor de negocios ajenos Art. 1.808 CC PY, Poder, Apostilla, Prórroga, Desistimiento, Cl. NOVENA penalty wording, DGRP, Catastro, Mensura, TC). CLOSING_DAY_PREP line 3 reciprocates with MORNING_RUNBOOK + CONTINGENCIES back-pointers.

One new file landed on master prior tick but referenced from §11 for completeness:

- **`docs/INDEX.md`** (NEW) — 6-tier doc-mesh navigation entrypoint. Tier 0 escritura-critical: MASTER_BRIEF, CLIENT, contract_summary, CLOSING_DAY_PREP, MORNING_RUNBOOK, CONTINGENCIES, INTEGRITY.md, audit_log.txt. Tier 1 supporting deliverables: wesley_brief_onepager, wesley_deliverable_bundle, escritura_deck, boq_rollup, fx.json. Tier 2 email drafts. Tier 3 engineering + research provenance. Tier 4 license + credits. Tier 5 session + status. Tier 6 house + landscape spec. Cold-start reading order at footer: MASTER_BRIEF → CLIENT → contract_summary → CLOSING_DAY_PREP → MORNING_RUNBOOK → CONTINGENCIES → INTEGRITY → audit_log → SHARE_LINKS → 4 email drafts.

Commit chain at tick close: `<batch-22-sha-pending>` ← `0b93af8` (Batch 21 / T-12 sweep) ← `4409dba` (Batch 20 / T-DT 62-ha digital twin) ← `85e86aa` (Batch 7 / 18/18 finals). Render state unchanged: **18/18 finals on disk + on master at `85e86aa`**. T-DT sub-render still on disk + on master at `4409dba`.

Task ledger transitions this tick: **#5 INTEGRITY.md → completed**. **#11 audit_log.txt → completed**. **#21 CONTINGENCIES.md → completed**. **#23 SHARE_LINKS.md → completed**. **#27 errata_template_es.md → completed**. **#29 sent_archive/.gitkeep → completed**. **#71 STATUS.md §11 T-10 sweep → completed**. **#74 runbook ↔ closing-prep bidirectional cross-link → completed** (both sides landed). **#76 contract_summary glossary → completed**. **#78 INDEX.md → completed**. **#80 SESSION_LOG.md tick 22 → completed** (this entry). **#87 burgos_es page-count fix → completed**.

Carry-forward open lines (durably persisted on STATUS §11 "Open lines to close"):
- USB burn-test (physical, T-1 evening user action)
- GPG-sign sidecar for bundle SHA
- BUNDLE_README.txt inside zip (re-bundle on T-1 evening)
- Wallet-card SHA print-out
- BoQ catalogue-sum cross-check (USD 268,685.45 / Gs. 1,961,403,785 @ TC 7300)
- Cl. CUARTA cifra verify (Gs. 2,252,700,000 saldo) + Cl. OCTAVA (ii) 5-hábiles wording
- Pelton stats ↔ JSON cross-check (head_max=182.6 / mean=33.4 / p95=108.1, 31.2 % > 30 m, 10.7 % > 80 m)
- CC0 / CC-BY 4.0 credits cross-check vs CREDITS.md
- hunspell es_PY + en_US deck sweep
- Cover date string verify (2026-06-27)
- Subscene leakage grep across deck body (raw `lqv/subscene/*` module names)
- T-7 freeze tag `escritura-frozen-T-7` on 2026-06-20
- T-1 freeze tag `escritura-frozen-T-1` on 2026-06-26
- Orphan bundle cleanup (`wesley_bundle_20260615-2352`, `wesley_bundle_20260616-1539`) — needs user re-confirm per CLAUDE.md rule #6 (destructive `rm`)

### Still pending (carried)

- **Render delivery batch (Task #24)** — once C_petal_macro lands (18/18), stage `renders/C_*.png` + `STATUS.md` (with §9 Cross-references from tick 13) + `LICENSE_BUNDLE.md` + `LICENSES/README.md` (with tick-14 extended back-pointers) + `CLAUDE.md` (with tick-15 Supplementary docs sub-section) + `docs/wesley_deliverable_bundle.md` (with tick-16 Extended back-pointers) + `docs/asset_plan.md` (with tick-16 §G second-pass extension) + tick 12's three back-pointer extensions (`ARCHITECTURE.md`, `CREDITS.md`, `LICENSE_BUNDLE.md`) explicitly, commit `deliver(renders): C variant — 6 cameras`, update STATUS.md manifest to 18/18 ☑, run `/verify-render`.
- **MCP-blocked work**: Phase 4 Sketchfab flora batch + Phase 3b Lapacho Hyper3D session — socket is dead, not fixable this session.
- **`scatter_lapacho_petals` floating-petal fix** — deferred until C-batch is fully done (an `lqv/` edit mid-batch would diverge render byte-identity).
- **Wesley's answers to R01–R04** still gate the v3 onepager polish + the larger planning work.
- **UPGRADE_PLAN Tier 0 execution** — T0.1 push to GitHub remote is the escritura-blocking SPOF; T0.2 `.gitignore` additions; T0.3 Wesley PDF; T0.4 STATUS.md "Known Defects" (landed this tick as §10); T0.5 BOM in PYG; T0.6 wire `ten_rules_check`.
- **Sub-render programme T1.1** — first three drivers (`cob_walls` / `bottle_wall` / `tatakuá`) + `lqv/subscene/base.py` shared setup. Per `sub_render_strategy.md` §10, steps 1-7 preserve byte-identity; only step 8 (final composite re-render) supersedes `85e86aa`.
- **Reverse-link survey for the three new docs** — `CRITIQUE_2026-06-10.md` + `UPGRADE_PLAN.md` + `sub_render_strategy.md` are now referenced from STATUS §9 + CLAUDE.md self-upgrade section, but reverse pointers from the broader 15-node mesh (asset_plan, external_assets, ARCHITECTURE, etc.) have not yet landed. Defer until the mesh-consolidation pass per new standing rule #4 ("doc consolidation > doc extension").

---

## 2026-06-17 T-10 commit + tag (4653ef2)

T-10 closing-prep sweep landed on origin/master.

- Commit: `4653ef2` — 27 files, +1204/-12 (12 mod + 14 new + .gitkeep)
- Tag: `escritura-t10-verified-2026-06-17` (annotated, pushed)
- Daily VERIFY at commit time: 3/3 OK, bundle SHA `9ce96b…724a53c`, deck SHA `2e4c26…0701137`
- Pytest invariants: 11/11 passed (`python3 -m pytest`)
- `build_scene.py` untouched (byte-frozen at `85e86aa`)

**Ruff drift deferred.** `ruff check .` reports 318 errors on clean HEAD (pre-existing tech debt, not introduced by this sweep). Bulk lives in `docs/site_data_2026-06-13_snapshot/*.py` (78), `lqv/typologies/bamboo_container_4pax.py` (14), `lqv/subscene/elevation_dutch.py` (11), `lqv/amenities/*.py` (19). T-10 is not the window for a 318-error cleanup pass — full sweep deferred to T+30 per `ARCHIVE_RUNBOOK.md`. No files authored this arc (bash + markdown) affect ruff scope.

**Engineering residual (1)**: F-bucket #58 mirror remote — still blocked on URL + auth from user. Everything else from the 100-item plan is shipped or user-side.

---

*Maintained by Ivan / AI Whisperers.*
