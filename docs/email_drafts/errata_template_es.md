To: Escribana Cynthia Andrea Peña Ros <email>
From: Ivan Weiss Van Der Pol <weissvanderpol.ivan@gmail.com>
CC: Wesley van de Camp <email>; Thijs Adrianus Hendricus <email>
Subject: Escritura van de Camp / Torrasca — errata v-final-2 (27/06/2026)

Estimada Escribana Peña,

Detectamos una corrección menor en el paquete técnico v-final enviado anteriormente. Adjunto la versión actualizada **v-final-2** del deck y el sidecar SHA-256 correspondiente.

**Cambio puntual:**

- [FOJA / PÁGINA AFECTADA]: [DESCRIPCIÓN BREVE DE LA CORRECCIÓN — p. ej. "Cómputo BoQ pág. 21 actualizado por refresco TC BCP", "Apéndice inglés pág. 25 — corrección tipográfica en nombre de comprador"].
- Ningún dato contractual cambia (cifras Cl. CUARTA, identificación de partes, fechas).

**Artefactos v-final-2:**

- `escritura_deck_v6_2.pdf` ([NUEVO TAMAÑO] MB, 28 páginas).
- SHA-256 deck v-final-2: `[HASH NUEVO]`.
- Bundle: sin cambios — sigue siendo `wesley_bundle_20260616-1715.zip` (SHA-256 `9ce96b859620201bee7dadc7e8f164c4177613e69e7fb66e30bc14085724a53c`) — la corrección es solo en el deck.

**Acción solicitada:**

- Sustituir el adjunto previo por `escritura_deck_v6_2.pdf` en su archivo digital.
- En la mesa: utilizar la copia impresa nueva (la traigo físicamente). La copia previa puede destruirse o conservarse marcada como "superada".

Quedo a disposición por WhatsApp para confirmar recepción.

Saludos cordiales,

Ivan Weiss Van Der Pol
Ai-Whisperers — soporte técnico del Sr. van de Camp
weissvanderpol.ivan@gmail.com

---
**Adjunto:** `escritura_deck_v6_2.pdf`
**Tag git:** `escritura-errata-v2-2026-06-27` (commit a confirmar en el momento de la corrección).

---
## INSTRUCCIONES DE USO (no enviar en el correo real)

Plantilla para una corrección de último momento si el deck cambia entre el envío inicial (T-0 07:30) y la firma (10:00).

1. Hacer el fix en `scripts/build_escritura_deck.py` o en el dato fuente.
2. Rebuild: `python3 scripts/build_escritura_deck.py`.
3. Verificar 28 páginas, ≥ 10 MB.
4. Calcular SHA-256 nuevo: `sha256sum docs/escritura_deck/escritura_deck_v6.pdf`.
5. Renombrar a `escritura_deck_v6_2.pdf` y mover a `dist/print_pack_2026-06-27/`.
6. Reemplazar `[FOJA / PÁGINA AFECTADA]`, `[DESCRIPCIÓN]`, `[NUEVO TAMAÑO]`, `[HASH NUEVO]` en este draft.
7. Crear tag git: `git tag -a escritura-errata-v2-2026-06-27 -m "Errata v-final-2: <descripción>"`.
8. Enviar a Peña + Wesley + Thijs. CC Burgos solo si el cambio afecta su comisión.
9. Imprimir nueva copia (1 ejemplar para la mesa) y reemplazar el ejemplar de Peña.
10. Actualizar `dist/print_pack_2026-06-27/INTEGRITY.md` con el nuevo SHA + nota de errata.
