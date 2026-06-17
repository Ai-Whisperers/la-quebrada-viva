# Rollback Runbook — Escritura Bundle

> When and how to rescind a sent bundle before signing. Used only if (a) a verifiable error in the deck or evidence bundle is discovered post-send, OR (b) the escritura is postponed and the share links must be revoked.

## Tags / anchors

| Tag                              | Created   | Meaning                                                            |
|----------------------------------|-----------|--------------------------------------------------------------------|
| `escritura-frozen-T-7`           | 2026-06-20 | Last day for non-cosmetic deck edits.                              |
| `escritura-frozen-T-1`           | 2026-06-26 | Bundle SHA frozen; no further repackage allowed without re-tag.    |
| `escritura-sent-2026-06-27`      | (sent day) | Tag points at the exact commit whose deck SHA matches the sent PDF.|
| `escritura-signed-2026-06-27`    | post-event | Outcome anchor — only created if signing succeeded.                |

## Errata trigger — go / no-go

A rollback is **mandatory** if any of:
- Cl. CUARTA cifra in the deck (Gs. 2.252.700.000) does not match boleto.
- Cl. OCTAVA (ii) plazo (5 días hábiles) is misstated.
- Wesley / Thijs / sellers / Burgos name or document number is wrong.
- Parcel identification (matrícula, padrón, superficie) is wrong.
- Bundle SHA on disk ≠ SHA in INTEGRITY.md / wallet card / emails.
- Page count ≠ 28.

A rollback is **discretionary** for:
- Typos in non-cifra Spanish prose.
- Pelton appendix wording (page 27).
- English appendix wording (pages 25–26).
- Render variant swap (A/B/C re-ordering).

Discretionary errata default to "do not rollback unless ≥3 are stacked"; one isolated typo on p. 13 is not worth re-sending and re-printing.

## Procedure — mandatory rollback

1. **Within 5 min of detection:**
   - Hard-stop further sends. WhatsApp Peña / Wesley / Thijs / Burgos (in that order) with literal text: "Pausa: detecté error en el deck enviado. Reenviaré versión corregida en <ETA> min. Por favor no abrir el adjunto anterior."
   - Do NOT delete sent emails — leaves audit trail.

2. **Within 30 min:**
   - Branch from `escritura-sent-2026-06-27`: `git switch -c errata-2026-06-27`
   - Fix the specific error. No drive-by edits.
   - Re-build deck: `python scripts/build_escritura_deck.py`
   - Re-build bundle: `bash scripts/make_wesley_bundle.sh`
   - Run `dist/print_pack_2026-06-27/VERIFY.sh` — must pass 3/3.

3. **Within 60 min:**
   - Update `INTEGRITY.md` with new SHAs (errata_v6.1).
   - Update wallet-card with new SHAs.
   - Re-send emails using `docs/email_drafts/errata_template_es.md`, attaching corrected deck.
   - Re-upload bundle to Drive/WeTransfer, replace SHARE_LINKS.
   - Tag the corrected commit: `git tag escritura-sent-2026-06-27-errata-1`
   - Push tag.

4. **Print pack on the day:**
   - Reprint affected pages only (deck reprint is one-shot — replace whole booklet).
   - Burn second USB with corrected bundle, label `v6.1`.

## Procedure — discretionary rollback (rare)

Same as mandatory, but skip step 1 WhatsApp. Send corrected version with subject prefix `[fe de erratas]` referring to specific page(s) and what changed.

## Procedure — postponement

If escritura is postponed > 7 days:
1. WhatsApp all parties: postponement confirmed, new date TBC.
2. Revoke share links (Drive: remove public access; WeTransfer: expire).
3. Tag current state: `escritura-postponed-2026-06-27`.
4. Move `print_pack_2026-06-27/` to `print_pack_2026-06-27.archived/`.
5. Pause; do NOT delete bundles. Resume timeline from T-10 against new date.

## What NOT to do

- **Do not** force-push to `master` to "fix" the sent version — the tag is the historical record.
- **Do not** delete the original bundle from Drive — confused recipients will hit a dead link.
- **Do not** rotate Reply-To / From address mid-flight — confuses thread routing.
- **Do not** issue more than 2 errata; if ≥3 are needed, the answer is postponement, not patchwork.

---
Cross-refs: [[CLOSING_DAY_PREP.md]] · [[CONTINGENCIES.md]] · [[POSTMORTEM_TEMPLATE.md]] · [[DECISIONS.md]] · [[INTEGRITY.md]] · `docs/email_drafts/errata_template_es.md`
