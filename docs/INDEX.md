# docs/ — index

Single navigation entrypoint into the doc-mesh. Maintained additively; section ordering reflects what a cold-start session should read first.

## Tier 0 — escritura-critical (read first if today is 2026-06-2X)

- [`MASTER_BRIEF.md`](./MASTER_BRIEF.md) — project North Star, scope boundaries, owner.
- [`CLIENT.md`](./CLIENT.md) — Wesley van de Camp (75 %) + Thijs (25 %). Decision-maker, communication preferences.
- [`contract_summary.md`](./contract_summary.md) — boleto 2026-04-28 quick-reference + glossary. Companion to the boleto PDF.
- [`CLOSING_DAY_PREP.md`](./CLOSING_DAY_PREP.md) — T-7 / T-5 / T-2 / signing-day / T+30 actionable checklist (legal side).
- [`MORNING_RUNBOOK_2026-06-27.md`](./MORNING_RUNBOOK_2026-06-27.md) — signing-day mechanical runbook (laptop side, 07:00 → 10:00 -03).
- [`CONTINGENCIES.md`](./CONTINGENCIES.md) — C1–C10 risk register, pre-decided playbook, standing principles.
- [`ROLLBACK_RUNBOOK.md`](./ROLLBACK_RUNBOOK.md) — errata trigger / mandatory-vs-discretionary procedure / postponement protocol.
- [`../dist/print_pack_2026-06-27/INTEGRITY.md`](../dist/print_pack_2026-06-27/INTEGRITY.md) — canonical artefact pins (deck SHA, bundle SHA, 28 pp, source commit).
- [`../dist/print_pack_2026-06-27/audit_log.txt`](../dist/print_pack_2026-06-27/audit_log.txt) — stale-token sweep log.
- [`../dist/print_pack_2026-06-27/WALLET_CARD.txt`](../dist/print_pack_2026-06-27/WALLET_CARD.txt) — pocket-size SHA + cifras + logística card (print on entry).
- [`../dist/print_pack_2026-06-27/BUNDLE_README.txt`](../dist/print_pack_2026-06-27/BUNDLE_README.txt) — bundle integrity / verification commands / contents map (ships with USB).

## Tier 1 — supporting deliverables

- [`wesley_brief_onepager.md`](./wesley_brief_onepager.md) — one-page brief.
- [`wesley_deliverable_bundle.md`](./wesley_deliverable_bundle.md) — what ships to Wesley + structure.
- [`escritura_deck/escritura_deck.md`](./escritura_deck/escritura_deck.md) — escritura deck source (PDF: `docs/escritura_deck/escritura_deck_v6.pdf`).
- [`boq/boq_rollup.md`](./boq/boq_rollup.md) — Bill of Quantities rollup, 175 items, USD primary + PYG @ TC 7300.
- [`finance/fx.json`](./finance/fx.json) — BCP USD/PYG ref rate + `as_of` date (refresh on T-0 ~07:00).

## Tier 2 — email drafts + distribution

- [`email_drafts/pena_es.md`](./email_drafts/pena_es.md) — Escribana Peña, primary recipient.
- [`email_drafts/wesley_en.md`](./email_drafts/wesley_en.md) — Wesley, English.
- [`email_drafts/thijs_es.md`](./email_drafts/thijs_es.md) — Thijs, Spanish.
- [`email_drafts/burgos_es.md`](./email_drafts/burgos_es.md) — Burgos, Spanish.
- [`email_drafts/SHARE_LINKS.md`](./email_drafts/SHARE_LINKS.md) — Drive primary + WeTransfer + USB fallbacks + pinned hashes.
- [`email_drafts/errata_template_es.md`](./email_drafts/errata_template_es.md) — last-minute v-final-2 errata draft.
- [`email_drafts/sent_archive/.gitkeep`](./email_drafts/sent_archive/.gitkeep) — naming convention for actually-delivered emails.

## Tier 3 — engineering + research provenance

- [`ARCHITECTURE.md`](./ARCHITECTURE.md) — `lqv/` module layout + RNG order invariant + sub-render-first standing rule.
- [`asset_plan.md`](./asset_plan.md) — per-asset / per-typology / per-amenity plan.
- [`sub_render_strategy.md`](./sub_render_strategy.md) — 31-target sub-render queue + driver template + RNG derivation.
- [`_archive/MANIFEST.md`](./_archive/MANIFEST.md) — index of archived critiques + tiered fix-plans (Tier-0 landed; carry-forward items live in `DEFERRED_BUGS.md` + TaskList #34–#50).
- [`PROVENANCE.md`](./PROVENANCE.md) — license + URL + SHA-256 + bbox + retrieval date for ALOS / COP30 / Sentinel-2 / GEDI / OSM / SRTM / NASADEM.
- [`site_data/satdata_brief.md`](./site_data/satdata_brief.md) — S1–S4 satellite render-pipeline reader.
- [`research/README.md`](./research/README.md) — research synthesis (5 sub-reports, ~80 repos).
- [`RESEARCH_GAPS.md`](./RESEARCH_GAPS.md) — open research gaps + tiered close plan.
- [`cultural_notes.md`](./cultural_notes.md) — Paraguayan cultural authenticity sweep.

## Tier 4 — license + credits

- [`../LICENSE_BUNDLE.md`](../LICENSE_BUNDLE.md) — bundled-asset license summary (CC0 + CC-BY 4.0 only gate).
- [`../LICENSES/README.md`](../LICENSES/README.md) — per-asset license file index.
- [`../CREDITS.md`](../CREDITS.md) — per-asset credits.
- [`license_obligations.md`](./license_obligations.md) — what must be attributed where.

## Tier 5 — session + status

- [`../STATUS.md`](../STATUS.md) — canonical state document. §11 is the T-10 sweep block.
- [`SESSION_LOG.md`](./SESSION_LOG.md) — continuation-arc tick log.
- [`DECISIONS.md`](./DECISIONS.md) — append-only durable-judgement log (boleto Cl. NOVENA, render parallelism, sub-render-first, etc).
- [`POSTMORTEM_TEMPLATE.md`](./POSTMORTEM_TEMPLATE.md) — escritura postmortem skeleton (fill T+1).
- [`../MEMORY.md`](../MEMORY.md) — auto-memory index (machine-local; not on origin).

## Tier 6 — house + landscape spec (research-tier; load when working subscene drivers)

- [`floor_plan.md`](./floor_plan.md), [`section_view.md`](./section_view.md), [`build_sequence.md`](./build_sequence.md), [`bom.md`](./bom.md), [`energy_budget.md`](./energy_budget.md), [`housing_park_phasing.md`](./housing_park_phasing.md), [`photographic_references.md`](./photographic_references.md), [`external_assets.md`](./external_assets.md), [`site_data_spike.md`](./site_data_spike.md).

---

**Reading order on cold start, T-10 → T-0**: MASTER_BRIEF → CLIENT → contract_summary → CLOSING_DAY_PREP → MORNING_RUNBOOK → CONTINGENCIES → INTEGRITY.md → audit_log.txt → SHARE_LINKS → 4 email drafts. That's the escritura-critical chain in priority order.

*Maintained by Ivan / AI Whisperers. Last updated 2026-06-17 (T-10 to escritura).*
