# Decisions Log — La Quebrada Viva

> Append-only. One entry per durable judgement call. Newest at bottom.
> Format: ISO date · short title · decision · why · alternatives considered · revisit when.

---

## 2026-06-04 · Boleto Cl. NOVENA — no renegotiate

**Decision:** Acceptance of double-down-payment penalty (Gs. 500.6 M asymmetric exposure on buyer side) without renegotiation.
**Why:** Boleto was signed 2026-04-28; renegotiating Cl. NOVENA at T-50 would have telegraphed weakness to sellers, who already gave on price. Mitigation: bring full funds physically certified day-of, eliminate non-payment as a failure mode.
**Alternatives:** Insertion of escrow buffer clause (rejected — adds 2 more parties); cash deposit in Peña's hands at T-15 (rejected — escribana fees).
**Revisit:** Never, for this deal. Pattern: in next deal, push for Cl. NOVENA symmetry pre-boleto.

## 2026-06-10 · GitHub remote — private, Ai-Whisperers org

**Decision:** Pushed to `Ai-Whisperers/la-quebrada-viva`, private, no public mirror.
**Why:** Site-specific data (parcel coordinates, BoQ at supplier-level, escritura draft contents) is not for public mirror until post-signing + scrub. Org account ≠ personal account keeps wallet IDs out of public commit metadata.
**Alternatives:** Personal account (rejected — leaks identity to suppliers reading the repo); GitLab (rejected — Wesley already on GitHub).
**Revisit:** T+30 (consider read-only public mirror of the non-sensitive `lqv/` library + `docs/site_data` schemas, keeping evidence bundle private).

## 2026-06-11 · 62-ha digital twin shipped before Pelton siting closed

**Decision:** Shipped T-DT (digital twin) at `4409dba` despite Pelton siting still being open (P1/P2/P3 candidates not yet ground-truthed).
**Why:** T-DT is a deliverable in its own right (boleto-stage evidence); blocking it on Pelton ground-truthing meant slipping the T-15 internal checkpoint. Pelton honesty flag (penstock 300 m rule) shipped as separate appendix at p. 27 of deck.
**Alternatives:** Hold T-DT for Pelton ground-truth (rejected — ground-truth needs site visit not feasible pre-escritura).
**Revisit:** T+30, after site visit, re-rank P1/P2/P3 with ground photographs.

## 2026-06-15 · Render parallelism ceiling = 1

**Decision:** All Blender sub-renders serialize on the 14 GB host (no `-j N` parallelism).
**Why:** Measured ~4.3 GB RSS peak per Blender process; ×3 OOMs the host (kernel kill at sample 192/256). One render at a time, batches via Bash for loops over variant arrays.
**Alternatives:** Cloud render farm (rejected — license check on Hyper3D-generated assets not bullet-proof for CC0+CC-BY 4.0 gate); ×2 with swap (rejected — swap thrash made wall-time worse than serial).
**Revisit:** When host RAM upgrades or render volume materially increases.

## 2026-06-17 · T-10 sweep — five artefacts gate

**Decision:** T-10 readiness defined as five artefacts present on disk: `CONTINGENCIES.md`, `SHARE_LINKS.md`, `errata_template_es.md`, `INTEGRITY.md`, `audit_log.txt`.
**Why:** Gives a single deterministic check (`ls -la docs/{,email_drafts/,print_pack…}…`) that the dossier is operationally ready. Anything missing = block escritura departure.
**Alternatives:** Hash-based gate (rejected — file content is hand-edited up to T-1, so SHAs churn).
**Revisit:** T+1 postmortem — were any of the five never opened on the day? If yes, drop from next deal's T-10 gate.

## 2026-06-17 · Email Reply-To explicit despite From = Reply-To

**Decision:** Inserted `Reply-To: weissvanderpol.ivan@gmail.com` header in all 4 escritura drafts (Peña, Wesley, Thijs, Burgos), even though `From:` already routes to the same address.
**Why:** Mobile clients (especially the one Peña uses) occasionally collapse `From:` into a display-name only and route replies to the org address. Explicit `Reply-To:` blocks that edge case and signals intent. Cost: 1 line per draft. Risk: zero.
**Alternatives:** Trust `From:` alone (rejected — too many moving clients on the recipient side); use `Sender:` header (rejected — semantically wrong for this).
**Revisit:** Never; standing pattern for future deal-day drafts.

## 2026-06-17 · Sub-render-first workflow ratified

**Decision:** Any new asset / typology / amenity requires its own `lqv/subscene/<asset>.py` driver before any composite (`build_scene.py`) touch. Reaffirmed.
**Why:** Sub-render gives a 30 s loop on a 4 GB peak; composite gives a 7+ min loop on a 4.3 GB peak. Catching bugs in sub-render saves an order of magnitude on iteration cost. Also: `build_scene.py` is byte-frozen at `85e86aa` until post-escritura — zero edits allowed.
**Alternatives:** Build directly in composite (rejected — locks the byte-frozen state).
**Revisit:** Post-escritura, when `build_scene.py` thaws.

## 2026-06-27 · Escritura pública signed — deal closed

**Decision:** Closing executed at Escribana Peña Ros's office on 2026-06-27 (T0). 60 días corridos clock from boleto 2026-04-28 closed cleanly; no Cl. NOVENA invocation by either side. Land is legally Wesley + Thijs's.
**Why:** Boleto-locked date. The T-10 → T-1 dossier sequence (CONTINGENCIES, SHARE_LINKS, errata, INTEGRITY, audit_log) held; Reply-To explicit headers held; frozen bundle SHA-256 `9ce96b859620201bee7dadc7e8f164c4177613e69e7fb66e30bc14085724a53c` shipped untouched.
**Alternatives:** None — date was contractually fixed.
**Revisit:** Never. Carry-forward to the next deal's pattern library lives in `docs/wesley_deliverable_bundle.md` + `docs/POSTMORTEM.md`. The 5-artefact T-10 gate (see 2026-06-17 entry) survives the postmortem — all five were opened on the day.

## 2026-06-28 (T+1) · Polygon scope-lock — 30.9 ha buildable as canonical AOI

**Decision:** Wesley's 30.9 ha hand-drawn polygon (`docs/site_data/escobar_property_polygon.geojson`, northern Mbopicua cluster, ≈3 of the 6 fincas) becomes the canonical AOI for **all GIS, render, siting, and concept-art work** going forward. The 62.57 ha legal footprint stays canonical only for **finance, contract, and escritura artifacts** (BoQ totals, padrón triples, capital allocation).
**Why:** Wesley's mental model of the parcel boundary is a deliberate subset of the legal total; the remaining ~32 ha read as forest reserve, not near-term build zone. Acting on the full 62 ha for siting work would overstate the buildable surface area and risk vendor quotes priced against geometry the client never intended to develop. Anchors: `c06c1db` (analysis pack), `b6ebd25` (R37/R38 drafts), `docs/post_escritura_site_knowledge.md`.
**Alternatives:** Keep 62.57 ha as single canonical AOI (rejected — conflates legal and buildable, telegraphs we're siting on land Wesley doesn't see as the build zone); ship both AOIs in parallel without a canonical (rejected — duplicates work and creates ambiguity downstream).
**Revisit:** T+30, after Anexo I from Escribana Peña Ros confirms the padrón triple (currently 30.35 ha ≈ candidate A or B, deferred), or when Wesley's photos re-anchor stream position, internal road, and canopy mix.

## 2026-06-28 (T+1) · Outreach pause — no external send until photos arrive

**Decision:** Zero outbound contact to any third party (Awasi, San Bernardino hotels/clubs/AHK PY, architects, drone operators, vendors, DMCs) until Wesley's on-site photos drop and we re-anchor satellite-derived assumptions. All drafts closing R-status promises live local-only in the repo with explicit "DO NOT SEND" headers: R01 (`docs/comms/2026-06-28_wesley_thijs_draft.md`), R37 (`docs/comms/awasi_outreach_draft.md`), R38 (`docs/research/r38_san_bernardino_targets.md`).
**Why:** Wesley flagged in-person photos forthcoming. Satellite-derived claims (stream position, internal road, canopy species mix, existing structures) will likely re-anchor on photo arrival. Pitching Awasi against the wrong R&C exclusivity assumption, or commissioning architect quotes against geometry the photos may redefine, burns relationships and capital. Standing posture per Ivan's directive: "dont send the emails etc just do the work on everythinh" — AI Whisperers drafts, Wesley sends.
**Alternatives:** Send the Wesley/Thijs partner draft immediately (rejected — partner courtesy: Wesley sets tone with Thijs as 75% owner, our role is supplying the analysis pack, not narrating to Thijs); contact Awasi commercial team in parallel with photo-wait (rejected — R&C exclusivity verification in `docs/comms/awasi_outreach_draft.md` §5 not yet performed; cold-pitching the wrong manager is worse than waiting).
**Revisit:** When photos arrive and the §6 gap matrix in `docs/post_escritura_site_knowledge.md` collapses; or at T+30 if photos still haven't landed (re-evaluate whether to push Wesley for a deadline).

---
Cross-refs: [[CLOSING_DAY_PREP.md]] · [[CONTINGENCIES.md]] · [[ROLLBACK_RUNBOOK.md]] · [[POSTMORTEM_TEMPLATE.md]] · [[INDEX.md]]
