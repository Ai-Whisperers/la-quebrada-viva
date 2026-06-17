# T+1 Debrief — La Quebrada Viva escritura

> Pre-stub. Fill in the morning of 2026-06-28 (T+1) while the closing is fresh. Goal: capture what happened well, what went wrong, what surprised us, before memory decays.

**Closing date:** 2026-06-27
**Closing location:** Escribanía Cynthia Andrea Peña Ros, Asunción
**Bundle SHA (frozen):** `9ce96b859620201bee7dadc7e8f164c4177613e69e7fb66e30bc14085724a53c`
**Deck SHA (frozen):** `2e4c265cd2795d7b43e88c145274bf5ea9a4c6517d337a1e2eba5c0860701137`

---

## 1. Outcome

- [ ] Signed on time (10:00 -03)
- [ ] Signed with delay (note time: ____)
- [ ] Signed with errata (note: ____)
- [ ] Postponed (new date: ____)
- [ ] Other: ____

**Funds confirmed at table:** ☐ Yes  ☐ No  ☐ Provisional comprobante (per C7)
**All 6 padrones referenced correctly:** ☐ Yes  ☐ No (which: ____)
**Cl. OCTAVA (ii) comprobantes timing reaffirmed (5 hábiles):** ☐ Yes  ☐ No

---

## 2. What worked (engineering side)

*The pre-decided playbook items that actually fired and helped:*

- [ ] VERIFY.sh 3-check at T-0 morning
- [ ] WhatsApp fallback for share link (C9 path)
- [ ] WALLET_CARD pocket-reference at the table
- [ ] Deck v6 28-page format
- [ ] Bundle USB #1 read clean on Peña's machine
- [ ] Other: ____

---

## 3. What broke / surprised us

*The thing the pre-decided playbook did NOT cover, or covered wrong. Be specific — file paths, exact text, timestamps. This is the single most important section of this debrief: it's what makes the T+30 archive worth re-reading in 2027.*

| Surprise | What we did at the table | What we should have pre-decided |
|---|---|---|
|  |  |  |
|  |  |  |

---

## 4. CONTINGENCIES.md gaps

*Which Cn rows in `docs/CONTINGENCIES.md` were missing, wrong, or under-specified for what actually happened. File issues against this list for the T+30 archive pass.*

- C1 (bundle SHA fail): ____
- C2 (BCP FX move): ____
- C3 (Wesley delayed): ____
- C4 (seller absent): ____
- C5 (Burgos dispute): ____
- C6 (notary closed): ____
- C7 (funds delay): ____
- C8 (print pack loss): ____
- C9 (email failure): ____
- C10 (at-table amendment): ____

---

## 5. Cl. OCTAVA (ii) vendor-comprobante tracker handoff

*5-business-day deadline from signing for sellers to deliver títulos / planos / informes / impuestos comprobantes. Open `docs/OCTAVA_VENDOR_TRACKER.md` and start the clock.*

- Signing date: 2026-06-27
- 5 hábiles deadline: ____  (compute excluding weekends)
- Items confirmed in hand at signing: ____
- Items pending: ____
- Owner of chase: ☐ Wesley  ☐ Ivan  ☐ Peña

---

## 6. Cifras reconciliation

*Verify the numbers in the escritura vs the cifras in WALLET_CARD + PRINT_MANIFEST. Any drift gets logged here.*

| Line | WALLET_CARD pinned | Escritura actual | Match? |
|---|---|---|---|
| Total (Gs.) | 2.503.000.000 |  | ☐ |
| Seña (Gs.) | 250.300.000 |  | ☐ |
| Saldo Cl.CUARTA (Gs.) | 2.252.700.000 |  | ☐ |
| Burgos comisión (Gs.) | 313.000.000 |  | ☐ |
| TC ref (PYG/USD) | 7300 |  | ☐ |

---

## 7. Action items → T+30 archive

*Carry-overs to feed into `docs/ARCHIVE_RUNBOOK.md` and the post-mortem update.*

1. ____
2. ____
3. ____

---

## 8. Tag the git state

```bash
# If signed on time:
git tag -a escritura-signed-2026-06-27 -m "Escritura signed at Peña Ros, 6 padrones, 62 Ha 5737 m² 4704 cm², total Gs. 2.503.000.000"

# If postponed:
git tag -a escritura-postponed-YYYY-MM-DD -m "Postponed reason: ____"

# Push the tag:
git push origin escritura-signed-2026-06-27
```

---

## 9. Cross-references

- `docs/CONTINGENCIES.md` — playbook the day-of work was anchored on
- `docs/OCTAVA_VENDOR_TRACKER.md` — chase list for the 5-hábiles window
- `docs/ARCHIVE_RUNBOOK.md` — what to freeze, archive, and move out of working tree at T+30
- `docs/POSTMORTEM_2026-06-17.md` — pre-signing risk register (compare against actual outcome)
- `dist/print_pack_2026-06-27/MORNING_RUNBOOK_2026-06-27.md` — T-0 step-by-step (the diff between this and what actually happened goes in §3 above)
