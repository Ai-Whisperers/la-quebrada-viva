# Final Gallery — La Quebrada Viva (production composites @ 85e86aa)

**18 hero composites** at full Cycles render (parcel-scale, 62 ha digital twin + flora photoreal + Wesley typologies placed).
Three lighting variants (**A** dawn / interior · **B** neutral mid-day · **C** golden hero) × six cameras (**cliff · dusk · hero · petal_macro · stream_up · terrace**).
Frozen at commit `85e86aa` (renderer byte-identity preserved this sprint).

Companion to [HOUSES_REVIEW_2026-06-14.md](HOUSES_REVIEW_2026-06-14.md) — that doc covers per-asset sub-renders; this one covers full-scene composites.

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
- Re-render trigger: the deferred T1.6 (per-variant lighting differentiation) + Step 8 (final composite re-render of all 18) supersede this set when shipped; until then, `85e86aa` is canonical.
