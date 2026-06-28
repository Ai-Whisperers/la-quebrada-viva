# Final Gallery — La Quebrada Viva (production composites @ `85e86aa`)

**18 hero composites** at full Cycles render (parcel-scale, 62 ha digital twin + flora photoreal + Wesley typologies placed).
Three lighting variants (**A** dawn / interior · **B** neutral mid-day · **C** golden hero) × six cameras (**cliff · dusk · hero · petal_macro · stream_up · terrace**).
Frozen at commit `85e86aa` (renderer byte-identity preserved this sprint).

## Canonical lineage

| Asset | SHA / tag | Status | Notes |
|---|---|---|---|
| Renderer composite path | `85e86aa` | byte-frozen | composite path byte-identity preserved through 2026-06-27 |
| Print-pack bundle (`dist/print_pack_2026-06-27/`) | `0081129` (tag `escritura-2026-06-27`) | SHA-pinned | rebuild target; see `BUNDLE_README.txt` |
| Bundle ZIP | `wesley_bundle_20260616-1715.zip` | 266 MB / 37 files | SHA-256 `9ce96b859620201bee7dadc7e8f164c4177613e69e7fb66e30bc14085724a53c` |
| Escritura deck v6 | `02_deck/escritura_deck_v6.pdf` | 28 pp / 10.8 MB | SHA-256 `2e4c265cd2795d7b43e88c145274bf5ea9a4c6517d337a1e2eba5c0860701137` |
| 18 finals on disk | `renders/A‖B‖C_{cliff,dusk,hero,petal_macro,stream_up,terrace}.png` | shipped at `85e86aa` | mirrored into bundle `03_renders/` |
| Post-`85e86aa` polish wave (material registry v2 / HDRI swap / xray override) | `78433a7` (+ subsequent CC-* commits) | OFF print-pack | did NOT retroactively change shipped bytes — see `docs/CHANGELOG.md` `[Unreleased]` freeze note |

Companions:

- per-asset gallery — `docs/render_catalogue/INDEX.md` (926 renders / 53 assets, regenerated with the protocol-v2 `view` axis per CC-DOC.6)
- multi-view shotlist (`RENDER_VIEW={hero3q,elevation,plan,section,interior,xray}`) — `docs/RESULTS_GUIDE.md` §5 and `docs/HOUSE_IMAGERY_SHOTLIST.md` §5.1
- archived per-house critique — [`_archive/2026-06-1X/HOUSES_REVIEW_2026-06-14.md`](_archive/2026-06-1X/HOUSES_REVIEW_2026-06-14.md)

---

## Cliff camera — south escarpment overlook

| A — dawn | B — mid-day | C — golden hero |
|---|---|---|
| <a href="../renders/A_cliff.png"><img src="../renders/A_cliff.png" width="320"></a> | <a href="../renders/B_cliff.png"><img src="../renders/B_cliff.png" width="320"></a> | <a href="../renders/C_cliff.png"><img src="../renders/C_cliff.png" width="320"></a> |

## Dusk camera — long-shadow valley sweep

| A — dawn | B — mid-day | C — golden hero |
|---|---|---|
| <a href="../renders/A_dusk.png"><img src="../renders/A_dusk.png" width="320"></a> | <a href="../renders/B_dusk.png"><img src="../renders/B_dusk.png" width="320"></a> | <a href="../renders/C_dusk.png"><img src="../renders/C_dusk.png" width="320"></a> |

## Hero camera — main establishing shot (escritura cover candidate)

| A — dawn | B — mid-day | C — golden hero |
|---|---|---|
| <a href="../renders/A_hero.png"><img src="../renders/A_hero.png" width="320"></a> | <a href="../renders/B_hero.png"><img src="../renders/B_hero.png" width="320"></a> | <a href="../renders/C_hero.png"><img src="../renders/C_hero.png" width="320"></a> |

## Petal-macro camera — lapacho petal carpet detail

| A — dawn | B — mid-day | C — golden hero |
|---|---|---|
| <a href="../renders/A_petal_macro.png"><img src="../renders/A_petal_macro.png" width="320"></a> | <a href="../renders/B_petal_macro.png"><img src="../renders/B_petal_macro.png" width="320"></a> | <a href="../renders/C_petal_macro.png"><img src="../renders/C_petal_macro.png" width="320"></a> |

## Stream-up camera — looking upstream along the creek

| A — dawn | B — mid-day | C — golden hero |
|---|---|---|
| <a href="../renders/A_stream_up.png"><img src="../renders/A_stream_up.png" width="320"></a> | <a href="../renders/B_stream_up.png"><img src="../renders/B_stream_up.png" width="320"></a> | <a href="../renders/C_stream_up.png"><img src="../renders/C_stream_up.png" width="320"></a> |

## Terrace camera — guest-side terrace looking out

| A — dawn | B — mid-day | C — golden hero |
|---|---|---|
| <a href="../renders/A_terrace.png"><img src="../renders/A_terrace.png" width="320"></a> | <a href="../renders/B_terrace.png"><img src="../renders/B_terrace.png" width="320"></a> | <a href="../renders/C_terrace.png"><img src="../renders/C_terrace.png" width="320"></a> |

---

## Notes

- File sizes ~10–21 MB (full-res 4K composites — healthy PNGs, no HDRI-only silent-failure fallbacks).
- Variant profiles are the same A/B/C the sub-renders use: see `lqv/subscene/base.py:VARIANT_PROFILES`.
- For deck use: **A_hero** is the current escritura-deck cover; **C_hero** and **C_terrace** are the cinematic alternates.
- Provenance: every PNG written after CC-TOOL.8 (commit `4be4ac4`, 2026-06-15) embeds the git SHA + RNG seed + relevant env vars (`LQV_HDRI_BIOME`, `LQV_BOQ_SCOPE`, `RENDER_VIEW`) into the PNG metadata. The 18 shipped finals here predate that harness — provenance for them is fixed by the `85e86aa` byte-freeze.
- Re-render trigger: the deferred T1.6 (per-variant lighting differentiation, MASTER_TODO task #23) supersedes this set when shipped; until then, `85e86aa` is canonical and the print-pack bundle at `dist/print_pack_2026-06-27/` is the authoritative delivery artefact.
