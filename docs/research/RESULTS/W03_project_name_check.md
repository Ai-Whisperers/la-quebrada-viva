# W0.3 — Domain availability check for project name candidates

**Purpose:** Resolve the W0.3 project name decision. Wes picks one; Erebus checks domains for availability.

**Date:** 2026-06-30
**Status:** Initial research only. Wes's pick still pending.

---

## Candidates (from Wes's brainstorm audio E + Ivan's prior work)

| # | Name | Source | Wes preference signal | TLDs to check |
|---|---|---|---|---|
| 1 | **Riverstone Valley** | Wes's brainstorm (audio E) | "stolen from Yellowstone" — Wes's first mention | .com / .com.py / .io / .co |
| 2 | **Villa del Cielo** | Wes's brainstorm | Spanish, "mooi" | .com / .com.py |
| 3 | **Cielo Azul** | Wes's brainstorm | Spanish | .com / .com.py |
| 4 | **Lluvia Dorada** | Wes's brainstorm | German place + plant reference | .com / .com.py |
| 5 | **Lluvia de Oro** | Wes's brainstorm (variant) | " | .com / .com.py |
| 6 | **Riverstone Valley** | Ivan's working name | "quebrada" = stream, Spanish | .com / .com.py |
| 7 | **Eco Jungle Resort Paraguay** | Wes's working files | Descriptive, less branded | .com / .com.py |

---

## Domain availability (preliminary)

Note: I cannot do a live whois lookup from my tools. **Erebus can run a whois via local command when needed.** Below is the recommended check procedure.

```bash
# Run this from the VPS to check domain availability
for domain in \
  riverstonevalley.com riverstonevalley.com.py riverstonevalley.io riverstonevalley.co \
  villadelcielo.com villadelcielo.com.py \
  cieloazul.com cieloazul.com.py \
  lluviadorada.com lluviadorada.com.py \
  lluviadeoro.com lluviadeoro.com.py \
  quebradaviva.com quebradaviva.com.py \
  ecojungleresort.com.py; do
  echo "--- $domain ---"
  whois "$domain" 2>&1 | grep -E "^(No match|Registrar|Name Server|Status|Domain)" | head -5
  sleep 1  # rate limit
done
```

Or use web-based lookups:
- https://www.namecheap.com/domains/
- https://name.com/
- https://www.godaddy.com/domainsearch/

For .com.py (Paraguay ccTLD), check via NIC.py: https://www.nic.py/

---

## Trademark / social media check (also worth doing)

Once a name is picked, check:
- **PY trademark registry:** DINAPI (https://www.dinapi.gov.py/)
- **Argentina trademark (INPI):** https://www.argentina.gob.ar/inpi — many RV visitors will be from AR
- **US/Intl trademark:** USPTO + WIPO Madrid System
- **Social media handles:** Instagram, Facebook, TikTok — all should match
- **Domain variations** to defensively register: plural, hyphenated, common misspellings

---

## What I'm recommending to Wes

**Shortlist of 3 that match the audio preferences:**

1. **Riverstone Valley** — Wes's own first mention, sounds Anglo, matches the Eskenbach/suburbanization theme. .com might be taken; .co and .io are likely available.

2. **Villa del Cielo** — Spanish, fits the EU/Dutch-German-LATAM market. Likely available on .com.

3. **Lluvia Dorada** — Spanish + German place reference, poetic. Likely available everywhere.

**Avoid:** Riverstone Valley (Ivan's name, descriptive, less brandable). Eco Jungle Resort Paraguay (descriptive, used as Wes's working file name but not for marketing).

**Decision needed from Wes:** pick 1 (or propose another). This blocks BR02/BR03 domain check + the website/social media setup.

**Time cost:** 5 minutes for Wes to pick + 30 minutes for Erebus to verify domains + 1 day to set up social media handles if the name is clear.
