# docs/ — index

> **Single navigation entrypoint.** What every `docs/` subdir contains,
> organized by who reads it.
>
> **Last updated:** 2026-07-06 (Erebus post-audit update — see §delta below)

---

## 2026-07-06 delta (Erebus)

What changed in this directory in this session:

- `docs/wes/AI_WHISPERERS_WES_DIGEST_2026-07-06.md` — new operator-facing audit + action punch list (~12 KB)
- `docs/people/stakeholders/ATTORNEY_BRIEF_1PAGE.md` — print-ready A4 attorney brief (replaces some 24-Q-folder-only references)
- `docs/people/stakeholders/INSURANCE_BROKER_OUTREACH.md` — broker outreach playbook
- `docs/people/stakeholders/INSURANCE_PROPERTY_DATASHEET.md` — PHI-safe broker datasheet
- `docs/people/stakeholders/WHATSAPP_OUTREACH_TEMPLATE_ES.md` + `..._EN.md` — outreach templates
- `docs/people/wes/WES_ACTIONS.md` — renumbered to W0.5-A/W0.5-B/W0.8/W0.9 (preserves original W0.1-W0.7 alongside)
- `docs/research/RESULTS/NEW01-03_*.md` (3) — NEW-tier research: AI negotiator, steengroeve, river freight
- `docs/research/RESULTS/M_WOOD/COB/BEV/VLOER/VERF_01_*.md` (5) — Sprint-1 materials
- `docs/research/RESULTS/PRICE_GAP_MASTER.md` — 95-item price-gap inventory
- `docs/research/RESULTS/PRICE_INTELLIGENCE_MASTER.md` — scaffold for 6-category deep scrape (sections 1-6 placeholders, awaiting next-batch dispatch with delegation routing fix)

Net change in this session: +11 files (~57 KB markdown), 0 deletes, 1 doc rewrite (M_VERF_01 v1 → v2 with verified ASTM citations + PR06 climate anchor). No broken cross-references after the W0.x reconcile at `d4fc5e2`.

---

## Top-level rules

- **No more than 10 files at any single level.** Subdirs grouped by
  purpose (see below).
- **`_underscore` prefix** = internal/historical (don't read unless you're
  auditing or researching the past).
- **Data dirs** (raster tiles, satellite imagery) get a more permissive
  10-file rule because each raster is a discrete dataset — not a doc.

---

## Read this first (cold-start order)

1. [`README.md`](../README.md) — repo root, 5-min Wes-friendly nav
2. [`WES_INDEX.md`](./wes/WES_INDEX.md) — the 10-doc Wes reading stack
3. [`POST_ESCRITURA_NOW.md`](./state/POST_ESCRITURA_NOW.md) — what blocks
   Fase 1 right now (5 hard gates + 12 soft gates)
4. [`STATUS.md`](../STATUS.md) — canonical current state

---

## Who reads what (the 24 subdirs)

### Wes-facing (read first if you're Wes)

| Subdir | What's in it | Files |
|---|---|---|
| [`wes/`](./wes/) | The 10-doc Wes reading stack: WES_INDEX, WES_FAQ, WES_GLOSSARY, WES_WARNINGS, WES_HOW_WE_WORK, WES_NEXT_30_DAYS, CRITIQUE_FOR_WES, + bundle/inventory | 10 |
| [`people/`](./people/) | All stakeholder briefs, split by who (now includes 5 insurance + 1 attorney-pack files in stakeholders/ as of 2026-07-06) | 17 (in 3 subdirs) |
| [`legal/`](./legal/) | CLIENT.md, CLOSING_DAY_PREP.md, contract_summary.md | 3 |

### Project state (read for situational awareness)

| Subdir | What's in it | Files |
|---|---|---|
| [`state/`](./state/) | The canonical "where are we" docs: TIMELINE, MASTER_BRIEF, DECISIONS, POST_ESCRITURA_NOW, SESSION_LOG, MCP_STATUS, master_plan, etc. | 10 |
| [`research/`](./research/) | Strategy + research synthesis (split into strategy/ paraguay_context/ satellite_research/ + 4 existing subdirs) | 141 |
| [`audit/`](./audit/) | Repo health audits, before/after metrics, restructure playbooks | 9 |
| [`_reconciled/`](./_reconciled/) | The post-Wes-share merged view (split into business/ buildings/ land/) | 11 |

### Operations (runbooks, procedures)

| Subdir | What's in it | Files |
|---|---|---|
| [`operations/`](./operations/) | ARCHIVE_RUNBOOK, ROLLBACK_RUNBOOK, MORNING_RUNBOOK, CONTINGENCIES, POSTMORTEM_TEMPLATE, DEFERRED_BUGS | 6 |

### Technical specs (how things work)

| Subdir | What's in it | Files |
|---|---|---|
| [`specs/`](./specs/) | Render pipeline (8 files), house/cob specs (5), tourism spec (1), assets + license (2) | 16 (in 4 subdirs) |
| [`reference/`](./reference/) | AIW brand style, photographic references, terrain pivot, etc. | 7 |

### Comms + outreach (external-facing)

| Subdir | What's in it | Files |
|---|---|---|
| [`comms/`](./comms/) | Outreach (OCTAVA_VENDOR_TRACKER), guides (api_access), prompt templates | 5 |
| [`email_drafts/`](./email_drafts/) | Sent + draft emails | 7 |
| [`escritura_deck/`](./escritura_deck/) | The escritura deck PDFs (v6 is canonical) | 6 |
| [`boq/`](./boq/) | Bill of quantities | 3 |
| [`finance/`](./finance/) | Financial tracking | 1 |
| [`satellite/`](./satellite/) | Satellite data overview | 1 |

### Assets + render artefacts (large binaries)

| Subdir | What's in it | Files |
|---|---|---|
| [`audios/`](./audios/) | 5 audio transcripts (Wes recordings) + drafts + final | 27 |
| [`ideas/`](./ideas/) | 109 idea brainstorm catalog (63 ✓ reviewed + 46 in _archive) | 123 |
| [`render_catalogue/`](./render_catalogue/) | 18 final PNGs + by_asset/ + contact_sheets/ | 108 |
| [`references/`](./references/) | Wes's original WhatsApp photos (2026-06-11) | 41 |

### Data + GIS (technical, mostly machine-readable)

| Subdir | What's in it | Files |
|---|---|---|
| [`site_data/`](./site_data/) | GIS / satellite / climate / biodiversity data, 30+ subdirs each by data type | 547 |
| [`site_data_2026-06-13_snapshot/`](./site_data_2026-06-13_snapshot/) | Frozen pre-Wes-share data snapshot (gitignored) | 455 (local only) |
| [`site_data_monday/`](./site_data_monday/) | Frozen 2026-06-13 Monday deliverable (gitignored) | 266 (local only) |

### Historical (don't read unless auditing)

| Subdir | What's in it | Files |
|---|---|---|
| [`_archive/`](./_archive/) | All closed-session + superseded docs, split by date | 33 |

---

## Reorg history (2026-07-04)

This reorg pass:
- **66 → 2 files at docs/ root** (CHANGELOG.md + INDEX.md only)
- **Created 8 new subdirs** at docs/ level (wes, state, operations, specs, research, legal, comms, reference)
- **Split 6 over-10 dirs** into sub-subdirs: specs/, research/, _archive/, _reconciled/, people/, ideas/
- **Reorganized 8 site_data/ subdirs** (chelsa, mod16, hansen_gfc, jrc_gsw, mapbiomas, extended_aoi, flora, soilgrids) by data type/year
- **17 subdirs that previously violated the 10-file rule** → all comply now

See git log for the specific commits (this was a single atomic
reorg + content-fix pass on 2026-07-04).

---

*Maintained by Erebus (AI Whisperers). Updated 2026-07-04.*