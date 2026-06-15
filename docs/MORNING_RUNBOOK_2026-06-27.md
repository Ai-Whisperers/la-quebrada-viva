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

If any of these fail, rebuild before going to sleep — don't fix in the morning.

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

Spot-check:
- Cover page date reads **27 de junio de 2026**.
- BoQ catalogue-sum row uses today's FX (not the stale 7300).
- English appendix begins around page 22 (Wesley's section).
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
