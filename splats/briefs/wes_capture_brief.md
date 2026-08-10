# Wes — Camera Capture Brief voor La Quebrada Viva

**Doel**: hoognauwkeurige 3D Gaussian Splats van het perceel + wandelpaden,
getraind op Vast.ai (~$0.15 per wandeling). Eén goede wandeling = één splat.

---

## Wat film je

| Opname | Wat | Hoelang | Waarom |
|---|---|---|---|
| **Hoofdwandeling** | het volledige perceel, elke stap | 3–6 min, langzaam | de splat zelf |
| **Quebrada-detail** | de beek + bomen, van dichtbij | 30–60 s | textuur + beekbedding |
| **Cerros rondom** | 1–2 uitzichtpunten, langzaam pannen | 30 s elk | bergcontext |
| **Look-ups / look-downs** | op elk endpoint: omhoog naar bladerdek, omlaag naar grond | 5–10 s elk | sluit de splat |

Eén wandeling = één continue clip als het kan. Liever 3 min aaneengesloten
dan 3 losse fragmenten — sequentiële matching werkt beter.

## Hoe je filmt

- **Resolutie**: 4K (of de hoogste die je telefoon kan, ≥1080p).
- **Codec**: H.264 of HEVC, in `.mp4` of `.mov`.
- **Beweging**: loop alsof je een oudere met filmt — niet rennen, niet
  pauzeren, niet achterom kijken. Eén tempo, ~1 stap/seconde.
- **Belichting**: gouden uur (ochtend 7-9, late middag 16-18) > middag.
  Bewolkt is prima. Geen tegenlicht in de lens.
- **Kader**: houd de telefoon **diagonaal of verticaal** (niet perfect
  waterpas), zodat opeenvolgende frames genoeg overlap hebben.

## Wat je NIET filmt

- Andere mensen, huisdieren, voertuigen — die verschijnen als ghosts in
  de splat.
- Rennen of snel pannen — dat geeft motion blur + sparse puntenwolk.
- Close-ups van je schoen / hand / het pad direct onder de camera.
- Het interieur van huizen — we doen het exterieur eerst.

## Voor de meet (deze week)

1. **Download** je Google Photos album (Photos → album → ⋯ → Download).
   Kies "Original quality" als dat aangeboden wordt — anders
   "High quality" is OK.
2. **Zip of map** in `~/Downloads/` met naam `takeout-2026MMDD.zip`
   (MMDD = datum).
3. Stuur de link / het bestand door naar Ivan.

## Na de meet

De agent draait:

```bash
python3 splats/tools/ingest_album.py \
    --input ~/Downloads/takeout-2026MMDD.zip \
    --source wes \
    --date 2026-MM-DD \
    --split-safety        # splits langere clips in <60s stukken
```

Resultaat: `splats/captures/2026-MM-DD_wes/` met de geaccepteerde clips
+ `_ingest_check.json` (welke video's zijn doorgekomen, welke niet, en
waarom). Afgekeurde clips (te kort, te stil, verkeerde codec) worden
apart gelogd zodat we kunnen beslissen of ze toch bruikbaar zijn.

## Checks die de agent doet

| Check | Drempel | Waarom |
|---|---|---|
| Duur | ≥ 10 s | korte clips matchen niet met COLMAP |
| Beweging | mean\|ΔY\| ≥ 0.30 | stilstaande telefoon = geen 3D |
| Container | mp4/mov/webm/m4v | splat-trainers verwachten deze |
| Split | > 60 s → knippen in stukken | back-up tegen crash mid-train |

## Vragen?

Stuur ze via Messaging in het NL — Ivan leest het snelst terug in het NL.
Of spreek ze in op een voice-note in de projectchat, dan transcribeert
de agent ze en zet ze in `WES_ACTIONS.md`.

---

*Bron: lqv-bundle/capture/SKILL.md + kanban task t_b2ef974f (2026-07-28)*
*Update deze brief als de drempels veranderen na de eerste splat.*