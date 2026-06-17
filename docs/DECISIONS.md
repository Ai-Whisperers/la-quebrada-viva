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

---
Cross-refs: [[CLOSING_DAY_PREP.md]] · [[CONTINGENCIES.md]] · [[ROLLBACK_RUNBOOK.md]] · [[POSTMORTEM_TEMPLATE.md]] · [[INDEX.md]]
