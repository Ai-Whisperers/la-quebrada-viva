# Credits — La Quebrada Viva

Attribution for third-party assets used in the render pipeline. Update this file as assets land in `assets/models/`; remove entries when assets are removed from the scene.

CC0 assets (Poly Haven HDRIs and PBR textures) do not legally require attribution but are listed here for traceability.

## Sketchfab — CC-BY 4.0 (attribution required)

License terms: <https://creativecommons.org/licenses/by/4.0/>

Each entry below corresponds to an asset planned in `docs/asset_plan.md`. Mark `[USED]` once the asset is committed in `assets/models/`; entries without `[USED]` are planned but not yet imported.

- **Pindo palm tree** — Sketchfab UID `1fba8da266bc428ebfe8fe8a4f4df987` — CC-BY-4.0 — drooping fronds, riparian foreground (Cam_Cliff)
- **Tropical mango trees (5-pack)** — Jagobo — Sketchfab UID `6997814540f14929bf13cf3828b5dc90` — CC-BY-4.0 — dominant canopy backdrop
- **Tree fern** — b_nealie — Sketchfab UID `c6bc31d122c043a19346c90f5cbde40e` — CC-BY-4.0 — riparian shade understory
- **Bamboo (Guadua)** — local.yany — Sketchfab UID `3c13dc82ffb54d079a71fb8160d0cf90` — CC-BY-4.0 — clumping along stream (decimated from 1.5M to ~50k tris)
- **Agave americana** — LucaDubs — Sketchfab UID `efe126efa459471c81cfc3132357b1b6` — CC-BY-4.0 — lower-terrace colonisers (decimated from 1M to ~50k tris)
- **Anthurium plowmanii** — Lassi Kaukonen — Sketchfab UID `e6a92c1ddb8941e9b8aa92dc1f0f3c18` — CC-BY-4.0 — trunk epiphytes (species verification pending)
- **Solar PV panel** — 3DJeff — Sketchfab UID `71f959c15448419e98be183871b7ed19` — CC-BY-4.0 — Rule 9, mounted on procedural steel frame (NOT on sod roof)
- **Pelton wheel runner** — Filipe.Canto — Sketchfab UID `de3a9ddc430740eaac82fd43b06b7394` — CC-BY-4.0 — micro-hydro visible at stream weir (Rule 7)
- **Water tank (5000L)** — Maggadog — Sketchfab UID `7cd2b87c332a4cce8f881e3b0b4faa40` — CC-BY-4.0 — cistern with procedural 0.5mm stainless mesh (Rule 10)
- **Tatakuá oven** — knockcg — Sketchfab UID `d98456e4673943feb277dab8b45e5db6` — CC-BY-4.0 — courtyard cultural marker (Rule 8)
- **Glass bottles** — FrodoUndead — Sketchfab UID `334377879cb4475d9a4720a2f7c4cf55` — CC-BY-4.0 — instanced inside procedural cob bottle-wall panel (Rule 8)

### Phase 8 — Paraguayan detail props (PLANNED, not yet imported)

Shortlist sourced from `docs/external_assets.md`. Each entry stays `[PLANNED]` until `lqv/asset_loader.py` lands and the asset is committed under `assets/sketchfab/<uid>/`.

- **[PLANNED] Hammock** — Andrey3Ds — Sketchfab UID `c5fd4cef873f44f5a31db1fc6a04c572` — CC-BY-4.0 — Phase 8 cultural prop, strung between two corredor posts (Rule 8). REPLACES the rejected CC-BY-SA hammock UID `b5b2e42309144dafaf2efe9b71a491c8` (share-alike contamination risk for bundled redistribution).
- **[PLANNED] Mate / tereré diorama** — Szymon — Sketchfab UID `f9c34aac9f594e8ca176e96cb0155259` — CC-BY-4.0 — mate cup + bombilla + termo, placed on a small lapacho table on the corredor (Rule 8)
- **[PLANNED] Chicken coop** — BRNDL — Sketchfab UID `cbe1217c25804ffab1213b138db7ec76` — CC-BY-4.0 — wire-mesh coop near the east-yard cistern (Rule 8, foodway sell on `terrace` cam)
- **[PLANNED] Firewood pile** — Seth7Santos — Sketchfab UID `24694d04c1704aa1838ac775e1013f07` — CC-BY-4.0 — replaces/augments procedural firewood beside the tatakuá
- **[PLANNED] Bonfire / fire pit** — merlinammm — Sketchfab UID `ae5b6e5fcf9340f9bfe487404d547604` — CC-BY-4.0 — ember emission inside the tatakuá; pairs with Variant C window glow

## Sketchfab — CC0 1.0 (no attribution required; listed for traceability)

License terms: <https://creativecommons.org/publicdomain/zero/1.0/>

- **[PLANNED] Plant pot / cántaro substitute** — plaggy — Sketchfab UID `52bd62403b2e4b1db4e4641ebfd4f241` — CC0 — earthenware pot on corredor floor (Rule 8)

## Poly Haven — CC0 (no attribution required; listed for traceability)

License terms: <https://polyhaven.com/license>

HDRIs:
- `kiara_1_dawn` — Variant A golden hour skydome
- `misty_pines` — Variant B overcast skydome
- `qwantani_dusk_2` — dusk camera skydome

PBR textures:
- `aerial_mud_1` — laterite ground primary
- `brown_mud_03`, `clay_floor_001` — laterite alternates
- `aerial_grass_rock` — moss/sandstone terraces primary
- `dry_riverbed_rock`, `coast_sand_rocks_02`, `forest_ground_04` — rock detail
- `clay_block_wall` — raw cob base
- `clay_plaster` — lime plaster overlay
- `rough_plaster_brick`, `damaged_plaster` — wall wear detail
- `dark_wood` — milled lapacho timber
- `wood_floor_deck` — footbridge deck
- `weathered_brown_planks`, `rough_wood` — other timber detail
- `tree_bark_03` — lapacho bark
- `palm_tree_bark` — pindo bark
- `bark_platanus` — mango bark
- `fern_02` — understory ground cover

## Hyper3D / Hunyuan3D generated assets

These are generated procedurally from text prompts; no third-party attribution required. Listed for reproducibility — prompts archived in `docs/asset_plan.md` §C.4. Each generated asset must record `generator`, `prompt`, and `seed` at generation time so the output can be regenerated bit-for-bit (or close to it, given upstream model drift).

- **[PLANNED]** `lapacho_A.blend` — Handroanthus impetiginosus, bare + pink bloom
  - generator: Hyper3D Rodin
  - prompt: see `docs/asset_plan.md` §C.4 — "Lapacho A"
  - seed: TBD-at-generation (record back here once the job lands)
- **[PLANNED]** `lapacho_B.blend` — Handroanthus impetiginosus, fully leafed
  - generator: Hyper3D Rodin
  - prompt: see `docs/asset_plan.md` §C.4 — "Lapacho B"
  - seed: TBD-at-generation (record back here once the job lands)

### Cross-references

- `LICENSE_BUNDLE.md` (repo root) — per-license summary and bundle-readiness checklist.
- `LICENSES/README.md` — verbatim CC0 + CC-BY 4.0 legal-code mirror, with vendor-terms pointer table.
- `docs/license_obligations.md` — how each license is satisfied at publication time.
- `docs/asset_plan.md` §C.4 — full prompt archive (Lapacho A / B / Thatch + procedural-recipe notes for Variant C emission elements).
- `docs/external_assets.md` — download log and `[USED]` / `[PLANNED]` status for every Sketchfab + Poly Haven asset listed above.
- `docs/wesley_deliverable_bundle.md` §Tier 2 — this file ships in the Tier-2 USB / cloud bundle alongside `LICENSE_BUNDLE.md` and `LICENSES/README.md`; the triple together satisfies CC-BY 4.0 attribution at distribution time. Added 2026-06-10 to close the back-pointer asymmetry.
- `STATUS.md` — render manifest + open-task ledger; the source of truth for which `[PLANNED]` Sketchfab/Hyper3D entries above actually got wired into the build vs deferred behind the MCP-socket block.
- `ARCHITECTURE.md` §"Variant C additions (2026-06-10)" — code-side index of the three procedural recipes (fireflies, window-glow emission planes, Variant C lighting branch) that explain why this file gains *zero* new third-party rows for Variant C.
- `docs/SESSION_LOG.md` — narrative log of the 2026-06-10 mega-session including Variant C implementation + per-cam render-loop architecture decision; each `[USED]` entry in this file maps to an asset-import action recorded there.
- `CLAUDE.md` §"Material color references" + §"Plant species — critical accuracy notes" — the photographic constants this file's `[PLANNED]` reference rows must respect; e.g., pindo plumose-droop is mandated, so any Sketchfab pindo model added here must be visually verified against that spec before its row flips from `[PLANNED]` to `[USED]`.
