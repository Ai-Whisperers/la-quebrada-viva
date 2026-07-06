# Riverstone Valley

> **⚠️ NAME STATUS — provisional pending Wes's W0.6 decision**
> The repo content has been renamed from "La Quebrada Viva" → "Riverstone Valley"
> as Wes's **first instinct** (audio E: "Stolen from Yellowstone, it's Riverstone Valley. Boom. Boom. Boom.").
> However, Wes has **not formally decided** yet — see [`docs/people/wes/PROJECT_NAME_CANDIDATES.md`](docs/people/wes/PROJECT_NAME_CANDIDATES.md)
> for 100 candidates and 3 top recommendations (Erebus's pick: **Villa del Cielo**).
>
> **What's safe to use "Riverstone Valley" for:** internal repo, marketing copy, email, code comments.
> **What's NOT changed:** repo URL (`github.com/Ai-Whisperers/la-quebrada-viva`), the legal name on the escritura
> (which says "La Quebrada Viva"), the `lqv/` Python package name, the 18 final render filenames, scripts/.
>
> **To revert:** `git revert` this commit. The rename is one atomic commit for clean rollback.

62-hectare parcel in Escobar District, Paraguarí, Paraguay (~26°36'S 56°51'W). Owned 75/25 by **Wesley van de Camp** + Thijs. Escritura signed **2026-06-27**. Vision locked **2026-06-30** (5 audio recordings, 3h 19m, 28K words).

## 👋 If you're Wesley — start here

Open **[`docs/wes/WES_INDEX.md`](docs/wes/WES_INDEX.md)** — it's the one page
built for you. 5-min read.

**👉 NEW (2026-07-06): For the 1-page map of all 9 working files (capex, supply chain, legal, archaeology, BOQ, financial model), see [`docs/research/RESULTS/CHEATSHEET.md`](docs/research/RESULTS/CHEATSHEET.md). It's the fastest way to navigate the project.**

Then read in this order:

1. [`docs/wes/WES_FAQ.md`](docs/wes/WES_FAQ.md) — common questions (10 min)
2. [`docs/wes/WES_GLOSSARY.md`](docs/wes/WES_GLOSSARY.md) — vocabulary, NL/ES/EN
3. [`docs/wes/WES_NEXT_30_DAYS.md`](docs/wes/WES_NEXT_30_DAYS.md) — your calendar
4. [`docs/wes/WES_WARNINGS.md`](docs/wes/WES_WARNINGS.md) — things that might surprise you
5. [`docs/wes/WES_HOW_WE_WORK.md`](docs/wes/WES_HOW_WE_WORK.md) — how AI Whisperers + Wes collaborate

Then the 5 things-only-you-can-do this week in **[`docs/people/wes/WES_ACTIONS.md`](docs/people/wes/WES_ACTIONS.md)**.

If you want to know what's blocking Phase 1 right now: **[`docs/state/POST_ESCRITURA_NOW.md`](docs/state/POST_ESCRITURA_NOW.md)**.

## 👋 If you're Ivan / Kiki / Erebus — start here

Cold-start docs (open in this order):

- [`docs/state/POST_ESCRITURA_NOW.md`](docs/state/POST_ESCRITURA_NOW.md) — what's blocking Phase 1, post-escritura
- [`STATUS.md`](STATUS.md) — canonical current state
- [`CLAUDE.md`](CLAUDE.md) — operating instructions for AI sessions
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — `lqv/` package map + fragility notes
- [`docs/_reconciled/README.md`](docs/_reconciled/README.md) — Wes-files + Ivan-RV merged view
- [`docs/audit/CRITIQUE.md`](docs/audit/CRITIQUE.md) + [`RESTRUCTURE_PLAN.md`](docs/audit/RESTRUCTURE_PLAN.md) — repo health

## Project scope

Dual scope (post-escritura):

1. **Riverstone Valley cob house** — first example building typology on site. 18 photoreal Cycles finals (A/B/C × 6 cameras) shipped at byte-frozen commit `85e86aa`.
2. **Escobar Housing Park** ("Riverstone Valley") — Wesley's expanded vision: housing park + restaurant + wellness pool + ceremonies + family-anchored community. 15 vacation-rental typologies + 4 amenities. 4-BV corporate structure (machinepark principle). 2030 horizon (Sonja's 60th birthday).

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
- [`docs/state/MASTER_TODO.md`](docs/state/MASTER_TODO.md) — multi-phase TODO across P0–P4 + cross-cutting tracks
- [`docs/operations/DEFERRED_BUGS.md`](docs/operations/DEFERRED_BUGS.md) — known-but-deferred issues with reproducers

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
