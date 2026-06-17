# Contingencies — escritura 2026-06-27

Risk register and pre-decided playbook for the 10 scenarios most likely to derail the 27 Jun signing. Frozen 2026-06-17 (T-10). Re-read on 2026-06-26 (T-1).

The principle: **all engineering decisions are pre-made.** On signing day, the laptop side is a checklist, not a design exercise. Anything not covered here → defer to Wesley's call; do not improvise on the legal side.

---

## C1 — Bundle SHA verification fails on T-0 morning

**Symptom:** `bash VERIFY.sh` in `dist/print_pack_2026-06-27/` reports a mismatch on the bundle or deck.

**Pre-decided action:**

1. STOP. Do not send the existing artefact.
2. Rebuild deterministically:
   - `python3 scripts/build_escritura_deck.py`
   - `python3 scripts/build_wesley_bundle.py`
3. Re-pin `dist/print_pack_2026-06-27/INTEGRITY.md` with new SHAs.
4. Re-run `VERIFY.sh`. If still failing → roll back to commit `0081129` (last known-good deck commit) and rebuild from there.
5. Send the corrected artefact with errata note (template: `docs/email_drafts/errata_template_es.md`).
6. Do NOT delay 10:00 signing for this; the legal docs (boleto + IDs + funds receipt) are what the notary actually needs.

---

## C2 — BCP FX rate moves > 1 % overnight

**Symptom:** USD/PYG ref rate on 2026-06-27 morning is outside 7300 ± 1 % (≤ 7227 or ≥ 7373).

**Pre-decided action:**

- Update `docs/finance/fx.json` with the new ref + `as_of` date.
- Rebuild deck per Step 2 of the runbook.
- New deck → new SHA → re-pin INTEGRITY.md.
- Body of the distribution email gets one extra line: "TC del día: X PYG/USD (BCP, ref 2026-06-27). Catálogo BoQ recomputado en consecuencia."
- Contract amount (Cl. CUARTA Gs. 2.252.700.000) does NOT change — it's in PYG natively.

If BCP site is down: use yesterday's rate, note "TC T-1" in the email body, proceed.

---

## C3 — Wesley delayed / cannot attend

**Symptom:** Wesley's flight delayed, illness, can't reach the escribanía by 10:00.

**Pre-decided action:**

- Thijs (gestor de negocios ajenos per Art. 1.808 CC PY, 25 % co-buyer) can sign for Wesley's 75 % under the existing poder if one is on file with Peña. Check `docs/CLOSING_DAY_PREP.md` T-2 row for poder confirmation status.
- If no valid poder: reschedule. Cl. NOVENA penalty for buyer-side default = double the down-payment (Gs. 501,000,000). Avoid at all costs — push the new date with the seller, ideally same week.
- AI side: no rebuild needed; same deck, same bundle. Add an erratum note to the new date if rescheduled > 7 days out.

---

## C4 — Seller cannot attend (Torrasca side)

**Symptom:** Torrasca side delayed or refuses to attend.

**Pre-decided action:**

- This is a seller-side default → Cl. NOVENA in reverse (buyer can demand performance or refund + penalty). Defer to Wesley + legal counsel.
- AI side: nothing to do. Hold the bundle frozen. Do NOT re-tag anything until the new date is confirmed.
- If reschedule > 30 days: Cl. OCTAVA (ii) seller-side comprobantes window resets to new signing date.

---

## C5 — Burgos commission dispute at the table

**Symptom:** Burgos disputes the Gs. 313.000.000 split or the seña-remainder mechanics.

**Pre-decided action:**

- Wesley side: defer to the pre-agreed mechanic documented in `docs/contract_summary.md` (seña remainder Gs. 250.300.000 + direct top-up Gs. 62.700.000 = Gs. 313.000.000).
- If Burgos refuses: Wesley can pay the full Gs. 313.000.000 direct at the table to remove the friction, then claim the seña remainder back from the escribanía later. This is a Wesley decision, not an AI decision.
- AI side: nothing to rebuild. Burgos draft email (already sent T-1) is the audit trail.

---

## C6 — Notary office closed / unreachable on signing day

**Symptom:** Escribanía Peña closed on 2026-06-27 (strike, illness, building issue).

**Pre-decided action:**

- Backup escribanía: pre-identified by Wesley. Check `docs/CLOSING_DAY_PREP.md` for the second-choice notary (or ask Wesley T-2).
- If no backup: reschedule, same logic as C3/C4.
- Cl. CUARTA funds: do NOT transfer to the seller direct without notary intermediation — that breaks Cl. CUARTA's escrow assumption.

---

## C7 — Funds transfer (Gs. 2,252,700,000) blocked or delayed

**Symptom:** Wesley's transfer doesn't clear by 10:00 due to bank holiday, KYC freeze, or wire delay.

**Pre-decided action:**

- Cl. CUARTA requires comprobante de fondos at the table. A SPEI / SWIFT / IBAN screenshot showing "transfer initiated" + signed bank letter is acceptable to most Paraguayan notaries as comprobante en tránsito.
- If notary refuses provisional comprobante: 5-day extension is the standard ask; legal grounds are Cl. NOVENA buyer's good-faith carve-out (compraventa not in default while funds are demonstrably in transit).
- AI side: nothing to do. This is a Wesley + Peña conversation.

---

## C8 — Print pack physical loss (USB lost, deck print damaged)

**Symptom:** Morning of: USB missing, prints water-damaged, etc.

**Pre-decided action:**

- **Backup USB #2** lives in Wesley's car (per `docs/CLOSING_DAY_PREP.md` T-1 row). Copy is byte-identical (same SHAs — `9ce96b859620201bee7dadc7e8f164c4177613e69e7fb66e30bc14085724a53c` for the bundle, `2e4c265cd2795d7b43e88c145274bf5ea9a4c6517d337a1e2eba5c0860701137` for the deck). Verify with `bash dist/print_pack_2026-06-27/VERIFY.sh` before relying on it.
- **Print copy:** nearest copy shop in Paraguarí district — pre-identified location in `CLOSING_DAY_PREP.md` (or fall back to Asunción Centro copy shops). Print from the on-laptop PDF; verify page count = 28 (`pdfinfo escritura_deck_v6.pdf | grep Pages`) before paying.
- **Phone-cached fallback:** the deck PDF + WALLET_CARD.txt + MORNING_RUNBOOK should be cached offline in Google Drive on Wesley's + Ivan's phones (cached T-1 evening — confirm at T-2 row in `CLOSING_DAY_PREP.md`). Useful if both USBs and prints are lost simultaneously.
- **Last-resort screen-share:** notary already has the PDF in their email (T-0 07:30 send). If physical print fails entirely, screen-share from the laptop on the conference table.
- **Do not delay 10:00 for a missing print.** The notarial instrument is the boleto + IDs + funds receipt. The deck is supporting evidence; absence of the printed deck is recoverable, absence of Wesley + Thijs + the cifras is not.

---

## C9 — Email delivery failure (bounce, spam, blocked)

**Symptom:** Bounce / no-confirmation from Peña, Wesley, or Thijs after T-0 07:30 send.

**Pre-decided action:**

- **Escalation budget:** if no confirmation by **T-0 08:00** (30 min after send), assume the email did not land and switch channels. Do not wait until 09:00.
- **WhatsApp the share link directly** (`SHARE_LINKS.md` Drive folder). All four recipients have WhatsApp numbers on file (Peña Ros, Wesley, Thijs, Burgos — fill at T-1, see WALLET_CARD CONTACTOS block).
- **WhatsApp message template (ES, copy-paste ready):**
  > "Buenos días Dra. Peña — confirmo envío del pack para la escritura de hoy. Enlace: [SHARE_LINK]. SHA-256 bundle: `…724a53c` (últimos 8). Cualquier cosa, +595 [Ivan teléfono]. Gracias, Ivan."
- **Second-line fallback:** SMS the SHA-256 last-8 as fingerprint (`724a53c` bundle, `0701137` deck) + a shortened Drive link. SMS is byte-limited so omit the long explanation.
- **Verify receipt explicitly** — do not rely on WhatsApp read receipts (✓✓ blue can be a glance). Ask for a one-word reply ("recibido"). Note the confirmation in `MORNING_RUNBOOK_2026-06-27.md` log section with channel + timestamp.
- **Provider failover:** if Peña confirms by WhatsApp but the email never arrives → resend from a different email provider (Ivan has both `weissvanderpol.ivan@gmail.com` and the AI Whisperers business address). Document which channel was used in the runbook log so the audit trail is reconstructible post-signing.
- **Do not delay 10:00 for an email failure.** The notary having the bundle on their phone via WhatsApp is sufficient for the at-table reference; the email is the durable archival channel, not the working channel.

---

## C10 — At-table amendment request

**Symptom:** Peña asks for a typo fix / name correction / page-ref correction at the table.

**Pre-decided action:**

- **Typos in names / IDs / cifras:** STOP THE SIGNING. These are material. Do not sign with errata; fix the boleto-aligned data and re-sign next day.
- **Page-ref or formatting errors in the deck (not the boleto):** sign anyway. The deck is supporting evidence, not the legal instrument. Issue v-final-2 via `errata_template_es.md` within 5 hábiles.
- **Cl. CUARTA cifra mismatch:** STOP. Cifra discrepancy between boleto and escritura is a Cl. NOVENA trigger. Reconcile before signing.
- **NEVER amend Cl. OCTAVA (ii) or Cl. NOVENA wording at the table** — these are the buyer's protections; weakening them is a no-go regardless of pressure.

---

## Standing principles

1. **Don't delay 10:00 for AI-side issues.** The legal instrument is the boleto + IDs + funds. The deck and bundle are supporting evidence.
2. **Re-pin INTEGRITY.md every time anything is rebuilt.** The pin is the source of truth, not the file timestamp.
3. **Tag git on every state change.** `escritura-sent-2026-06-27`, `escritura-errata-v2-2026-06-27`, `escritura-signed-2026-06-27`, `escritura-postponed-YYYY-MM-DD`. Tags are cheap and durable.
4. **Wesley has the final call on legal-side decisions.** AI side decides only the engineering / rebuild / distribution mechanics.
