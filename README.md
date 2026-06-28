# La Quebrada Viva

62-hectare parcel in Escobar District, Paraguarí, Paraguay (~26°36'S 56°51'W). Owned 75/25 by **Wesley van de Camp** + Thijs. Escritura signing: **2026-06-27**.

Dual scope:

1. **La Quebrada Viva cob house** — first example building typology on site. 18 photoreal Cycles finals (A/B/C × 6 cameras) shipped at byte-frozen commit `85e86aa`.
2. **Escobar Housing Park** — Wesley's expanded vision: 15 vacation-rental typologies + 4 amenities for European / 1st-world travelers. Driven via the sub-render-first pipeline (`lqv/subscene/<asset>.py` → `renders/sub/runs/<RUN_ID>_<asset>/<variant>.png`).

## Deliverables (priority order)

| # | Deliverable | State |
|---|---|---|
| 1 | 18 cob-house finals (A/B/C × hero / stream_up / terrace / cliff / dusk / petal_macro) | **shipped** — `85e86aa` |
| 2 | 62-ha photoreal digital twin (ALOS DEM + Sentinel-2 albedo + GEDI canopy) | **shipped** — `4409dba` |
| 3 | Escritura technical pack (deck v6 PDF + Wesley bundle ZIP) | **frozen** — tag `escritura-2026-06-27` @ `0081129` |
| 4 | Housing-park master plan (15 typologies + 4 amenities, sub-render matrix) | **in progress** — driven by MASTER_TODO P1.A / P1.B / P1.C |

## Cold-start docs

Open in this order when picking up the project from scratch:

- [`PROJECT_INDEX.md`](PROJECT_INDEX.md) — full file map (1,186 tracked files, top-level layout, deliverable index)
- [`STATUS.md`](STATUS.md) — canonical current state (render manifest, decisions log, critical dates)
- [`CLAUDE.md`](CLAUDE.md) — operating instructions for AI sessions (document map, 10 design rules, code invariants)
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — `lqv/` package map + fragility / positional-coupling notes
- [`docs/INDEX.md`](docs/INDEX.md) — `docs/` directory navigator
- [`docs/MASTER_TODO.md`](docs/MASTER_TODO.md) — multi-phase TODO across P0–P4 + cross-cutting tracks
- [`docs/DEFERRED_BUGS.md`](docs/DEFERRED_BUGS.md) — known-but-deferred issues with reproducers

## Quick run

```bash
scripts/smoke_test.sh                  # build only, no render — run after any code edit
scripts/render_preview.sh A hero       # 1280×720 preview  → renders/_preview_A_hero.png
scripts/render_final.sh   A hero       # full-res final     → renders/A_hero.png
scripts/render_all_finals.sh           # all 18 finals (A/B/C × 6 cams)
```

Env vars: `RENDER_VARIANT=A|B|C` · `RENDER_CAM=hero|stream_up|terrace|cliff|dusk|petal_macro` · `RENDER_RES=preview|final|hero` · `RENDER_SAMPLES=<int>` · `RENDER_SKIP=1`.

Sub-render pipeline (housing-park typologies + amenities):

```bash
make sub                               # full sub-render matrix → renders/sub/runs/<RUN_ID>_<asset>/<variant>.png
make boq                               # BoQ rollup (escritura scope) → docs/boq/boq_rollup.{csv,md}
make deck                              # escritura deck PDF → docs/escritura_deck/escritura_deck_vN.pdf
```

## Variants

- **A** — dry-season warm sunrise (HDRI `bryanston_park_sunrise_4k`, strength 0.8)
- **B** — overcast wet-season midday with valley mist (HDRI `xanderklinge_4k`, strength 1.4)
- **C** — civil-twilight blue hour, fireflies + moonlight stand-in (HDRI `kloppenheim_07_4k`, strength 0.5)

Dispatcher at `lqv/lighting.py:19-23`.

## Constraints

- Blender 4.2.3 LTS, Cycles, AgX Punchy, OptiX + OIDN.
- 14 GB host — Blender sub-renders **must serialize** (one process at a time; ~4.3 GB RSS peak, ×3 OOMs).
- AMD-only host; HIP failing → CPU via `LQV_ALLOW_CPU_FALLBACK=1`.
- `build_scene.py` byte-frozen at `85e86aa`; do NOT modify without supersession plan.
- Renderer is **already Cycles** (`lqv/engine.py:15`). No EEVEE for finals. No box-modeled cob walls. No solar on living roof. No Tuscan / Bali / Earthship framing.

## Licensing

- Code (`lqv/`, `build_scene.py`, `scripts/`, `docs/`): MIT — see [`LICENSE`](LICENSE).
- Assets + renders: per-asset licenses, all CC0 1.0 or CC-BY 4.0. See [`LICENSE_BUNDLE.md`](LICENSE_BUNDLE.md), [`CREDITS.md`](CREDITS.md), [`PROVENANCE.md`](PROVENANCE.md), and [`LICENSES/`](LICENSES/) for verbatim legal text.
- CC-BY-SA assets explicitly **excluded** (incompatible with bundle redistribution).

## Repo

`Ai-Whisperers/la-quebrada-viva` (private). Push on commit; do not let the working tree become the sole copy.
