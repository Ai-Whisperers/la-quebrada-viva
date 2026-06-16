# Morning runbook — escritura signing day, 27 June 2026

One-page mechanical checklist for the AI-side deliverables on signing day. Legal / contractual side is in `docs/CLOSING_DAY_PREP.md`; this file covers only what needs to happen on the laptop the morning of.

Target: PDF v-final in Wesley's and Escribana Peña's inboxes by **08:00 -03**.

---

## Pre-flight (T-1 day, evening 26 Jun)

- [ ] `git status` clean on `master`. If not, stash or commit.
- [ ] `git fetch && git log @{u}..HEAD` returns nothing (master in sync with `origin`).
- [ ] `git tag -l escritura-2026-06-27` exists and points at the v-final commit (`0081129` or successor).
- [ ] `ls renders/sub/latest/elevation_dutch_*.png | wc -l` == 68.
- [ ] `ls docs/escritura_deck/escritura_deck_v6.pdf` exists, ≥ 10 MB, 27 pages.
- [ ] Boleto PDF on disk at `docs/2026-04-28_boleto_compraventa_torrasca-vandecamp.pdf`.
- [ ] Wesley deliverable bundle on disk (see "Notary hand-off bundle" below).

If any of these fail, rebuild before going to sleep — don't fix in the morning.

---

## Notary hand-off bundle (built 2026-06-16, refresh on T-1 evening)

Single self-verifying zip for the notary table — 35 files, 271 MB. Regenerable any time via `python3 scripts/build_wesley_bundle.py` (idempotent, deterministic from disk artefacts).

- Path: `dist/wesley_bundle_20260616-1539.zip`
- SHA-256: `f8a1cc930461ab509c9de3a78a2c834dd5fb5e5e01cdc838dfcca4f676eb15dd`
- Manifest: `dist/wesley_bundle_20260616-1539.manifest.txt` (per-file sha256 + byte size)

Contents (top-level prefixes inside the zip):

| Prefix | Items |
|---|---|
| `01_brief/` | `wesley_brief_onepager.pdf` (321 KB) |
| `02_escritura_deck/` | `escritura_deck_v6.pdf` (11.2 MB, 27 pp) |
| `03_renders_finals/` | 18 finals (A/B/C × hero/cliff/dusk/petal_macro/stream_up/terrace) at `85e86aa` |
| `04_terrain_digital_twin/` | 6 T-DT v5_arrowfix renders from `renders/sub/runs/20260611_dt_run_v5_arrowfix_terrain_62ha_{birdseye,oblique}/{A,B,C}.png` |
| `05_dem_ab/` | `dem_ab_contact.png` — ALOS vs COP30 cross-check |
| `06_pelton_feasibility/` | `pelton_head_map.png` (raw greyscale), `pelton_head_map.json` (stats + DEM sha), `pelton_head_map_contact.png` (viridis + 30 m/80 m contours + histogram) |
| `07_boq/` | `boq_rollup.{csv,md,pdf}` |
| `08_provenance/` | `PROVENANCE.md`, `satdata_brief.md` |

**Pelton headline (Rule 7, critical-systems outage-proof)** — on the 62 ha parcel, with a 300 m horizontal penstock radius proxy:
- `head_max = 182.6 m`, `head_mean = 33.4 m`, `head_p95 = 108.1 m`.
- **31.2 %** of the footprint sits above the 30 m minimum head for Pelton micro-hydro; **10.7 %** sits above the 80 m "good" head.
- Computed from COP30 DEM (sha256 `10e6459cd89319176ef8218c1f644e67dd38a38b7f603061b71f41c1604fed00`, 108×108 px, ~30 m/pixel).
- Re-derivable via `python3 scripts/build_pelton_head_map.py` + `python3 scripts/contact_sheet_pelton.py`.

**Notary hand-off checklist (10:00 -03 at the escribanía):**

- [ ] USB stick or signed download link with `wesley_bundle_20260616-1539.zip` + `.sha256` (separate file).
- [ ] Print of `02_escritura_deck/escritura_deck_v6.pdf` cover, BoQ page, and English appendix p22+ (3 copies: Peña, Wesley, file).
- [ ] Pelton contact sheet `06_pelton_feasibility/pelton_head_map_contact.png` printed colour A4 — single-page evidence for Rule 7 if asked.
- [ ] Boleto `docs/2026-04-28_boleto_compraventa_torrasca-vandecamp.pdf` — paper original or notarised copy per Cl. CUARTA.
- [ ] Comprobante de fondos Gs. 2.252.700.000 ready to hand over (Cl. CUARTA).
- [ ] Verbal reminder: Cl. OCTAVA (ii) seller comprobantes due within 5 hábiles.

---

## Step 1 — FX refresh (T-0, ~07:00)

Check current BCP USD/PYG and update `docs/finance/fx.json` if drift > 1%.

```bash
# Look up BCP daily ref rate (ask side). Fallback: https://www.bcp.gov.py/cotizaciones
# Edit docs/finance/fx.json — update USD_PYG and as_of fields.
```

Acceptance: `python3 -c "from lqv.finance import get_usd_to_pyg; print(get_usd_to_pyg())"` prints the new rate.

---

## Step 2 — Rebuild PDF (~07:10)

```bash
cd /home/ai-whisperers/blender-projects/la-quebrada-viva
python3 scripts/build_escritura_deck.py
```

Acceptance: `scripts/build_escritura_deck.py` reports `27 page(s)`, file ≥ 10 MB at `docs/escritura_deck/escritura_deck_v6.pdf`.

If the BoQ rollup changed (FX delta), the catalogue-sum row will update automatically — no manual edit needed.

---

## Step 3 — Sanity check (~07:15)

```bash
# Eyeball the cover, BoQ page, and closing checklist:
xdg-open docs/escritura_deck/escritura_deck_v6.pdf
```

Spot-check (page numbers verified against v6 on 2026-06-16):
- **Cover (p1)** reads escritura date **2026-06-27** and "generated YYYY-MM-DD" of today.
- **BoQ catalogue-sum (p21)** uses today's FX (not the stale 7300). Catalogue sum should be ~USD 268,685 at 7300 (recompute if FX moved).
- **English appendix (p25)** — single page summarising key facts for Wesley.
- **Parte 4 (pp22-24)** = Spanish day-of checklist + risk register; what the escribana reads from.
- No raw `lqv/subscene/*` module names anywhere in body copy.

---

## Step 4 — Distribute (~07:30)

Send to:

- **Escribana Peña** — primary recipient. Spanish subject + body, PDF attached.
- **Wesley van de Camp** (75% owner) — CC. English subject line, point him to the English appendix.
- **Thijs** (25% co-buyer) — CC.
- **Burgos** (intermediary) — CC if previously in correspondence.

Subject (ES): `Escritura van de Camp / Torrasca — paquete técnico v-final (27/06/2026)`
Subject (EN): `La Quebrada Viva — final escritura technical pack (27 Jun 2026)`

Body essentials:
- Today's signing time + escribanía address.
- Reminder: comprobante de fondos for **Gs. 2.252.700.000** required at the table (Cl. CUARTA).
- Reminder: Cl. OCTAVA (ii) seller-side comprobantes due within 5 hábiles post-signing.

---

## Step 5 — Post-send git checkpoint (~07:40)

```bash
git tag -a escritura-sent-2026-06-27 -m "PDF v-final sent to Pena + Wesley + Thijs at 07:30 -03"
git push origin escritura-sent-2026-06-27
```

This is the durable "what we shipped" anchor.

---

## Step 6 — On-site (10:00 onward)

Hand-off to Wesley + `CLOSING_DAY_PREP.md`. AI side is done unless a last-minute number / name correction is needed; in that case branch from `escritura-sent-2026-06-27`, fix, rebuild, attach v-final-2 with a one-line errata note.

---

## Failure modes

| Symptom | Action |
|---|---|
| `build_escritura_deck.py` raises | Diff vs commit `0081129`. Revert your change, rerun. |
| PNG missing from `renders/sub/latest/` | Use the previous PDF (`git checkout 0081129 -- docs/escritura_deck/`) — do NOT delay signing to re-render. |
| BCP site down for FX | Use yesterday's rate. Note in email body that FX is T-1. |
| Email bounces | Fallback: shared Google Drive folder, links texted to recipients. |
