# Wes — Materials Picker (5 of 6)

> **Wat dit is:** Je hebt in audio D (2026-06-30) om 15 materialen-onderwerpen
> gevraagd voor Sprint 0-2 onderzoek. **8 zijn al klaar** (Sprint 0,
> ge-eindigd 2026-07-06). Er blijven **6 open voor W1.1**. Kies **5 van de 6**
> om deze 2 weken te laten onderzoeken. De 6e gaat naar Sprint 1-2.

> **How to answer:** WhatsApp voice note (je dyslexie) van 60-90 seconden:
> "Ik kies [nummers] en de reden is [kort]". Of reply in deze thread.
> The remaining item automatically slots into Sprint 1-2.

---

## The 6 remaining (Sprint 0 batch closed 8/15 on 2026-07-06)

| # | Onderwerp | Domein | Why it matters | Bron-status |
|---|---|---|---|---|
| **9** | **Bevestigingsmateriaal (fasteners)** | Bouw | Schroeven, bouten, spijkers, hoekijzers — small but **ubiquitous** (50+ kg per cabin). Verkeerde keuze = corroded joints in 2-3 jaar in PY's vochtigheid. | M09 result TBD |
| **10** | **Vloeren (flooring)** | Bouw-finish | Visible quality differentiator voor €80-150/night cabins. Must handle PY humidity + wet-mop cleaning. Hardwood? Tile? Lime-resin? | M10 result TBD |
| **11** | **Verf (paint) — weatherbestendig** | Bouw-finish | Paraguay's UV + humidity is **brutal** on exteriors. Cheap paint fades in 1-2 years. Wes mentioned a 6-year-old house with peeling paint in audio E. | M11 result TBD |
| **12** | **Pool equipment** | Wellness amenity | Voor de wellness pool (D6_HOUSING_PARK_CONCEPT §0). Variable-speed pump, sand filter, salt-chlorine-free options. IP-rated for outdoor tropical exposure. | M21 result TBD |
| **13** | **AC units for PY climate** | Klimaat | PY summers hit 38-42°C. For Fase 1 hot season, **inverter split units** sized for the cob/earthen thermal mass. Critical for guest comfort. | M23 result TBD |
| **14** | **Customs broker recommendations** | Logistiek | Welke douanebrokers zijn betrouwbaar in CDE/Ciudad del Este voor import uit BR/CN/EU? Names, contacts, fee structure, typical clearance time. | M24 result TBD |

## Erebus's recommended 5 (HIGH confidence)

**Pick 9, 10, 11, 12, 13** (skip 14 customs broker — that one is logistiek,
not a Phase 1 capex-blocker, and can wait for Sprint 2 when you actually
import the materials).

### Why these 5

- **9 — Fasteners** — invisible line item, easy to forget, but missing this
  means a 4-cabin Phase 1 build halts in week 2 because the screws rust.
  *Source-effort: 3-5 days, can do in parallel with 10/11.*
- **10 — Flooring** — **directly visible** to guests in every cabin
  photo. The €80-150/night rate is justified or broken by this choice.
  Hardwood vs tile vs lime-resin. *Source-effort: 5-7 days.*
- **11 — Paint** — **PY UV/humidity is the #1 enemy** of all exteriors.
  1-2 year fade on cheap paint = "abandoned house" perception by 2028.
  *Source-effort: 5-7 days, has the most vendor data available.*
- **12 — Pool equipment** — the wellness pool is the **single most
  differentiating amenity** vs other rural-PY lodges. Get the equipment
  spec right and the pool becomes a wellness destination, not a "rusty
  chlorine pond". *Source-effort: 5-7 days.*
- **13 — AC units** — **Phase 1 summer** is the first guest test. Without
  AC, even 28°C indoor at night kills the Booking reviews. Inverter
  splits sized for cob thermal mass = the only sane choice. *Source-effort:
  5-7 days, multiple PY vendors available.*

### Why NOT 14 (customs broker)

- The first customs clearance is **not until Sprint 1-2** (when materials
  actually start arriving from BR/CN/EU). Until then, no broker needed.
- The broker is **not capex-blocking** — you can call a broker in 1 day
  when you actually need one.
- The 5 spots are tight; defer 14 to Sprint 2 (item 15 in the 15-list).

## What you do with this

```
WhatsApp voice note (60-90 sec):
"Materialen picker. Ik kies [nummers] en de reden is [kort]."
```

Or text:
```
9, 10, 11, 12, 13 (Erebus's 5)
```

Or in Spanish (Sonja translation):
```
"Los 5 de Erebus: 9, 10, 11, 12, 13. Los fasteners + piso + pintura
+ piscina + aire acondicionado. Customs broker (14) lo dejamos para
Sprint 2 cuando realmente importemos."
```

## What happens after you pick

Each of the 5 goes to a **Sprint 1.1 AI subagent task**. Per the
operator-fallback pattern (2026-07-07), deepseek-chat is currently
HTTP 402'ing (account empty), so subagents will dispatch via
openrouter/google/gemma-3-31b-it:free as the backup model.

Each result is written to `docs/research/RESULTS/M09/M10/M11/M21/M23_*.md`,
then aggregated into `docs/research/RESULTS/CAPEX_OPTIONS.md` (your master
capex rollup).

Estimated time to deliver all 5 results: **2 weeks** (parallel agents).

## The 8 already done (FYI)

| # | Onderwerp | Result file |
|---|---|---|
| 1 | Cement + rebar pricing | `M04_cement_rebar_pricing.md` ✅ |
| 2 | Ramen/glas (windows/glass) | `M05_aluminum_glass.md` ✅ |
| 3 | Septic + reed-bed greywater | `M08_septic_reed_bed.md` ✅ |
| 4 | Kitchen equipment import | `M22_kitchen_equipment_import.md` ✅ |
| 5 | Cell coverage Tigo/Personal/Claro at site | `F11_cell_coverage.md` ✅ |
| 6 | Starlink installability | `F12_starlink.md` ✅ |
| 7 | Solar PV sizing | `F09_solar_pv.md` ✅ |
| 8 | NL BV > IB threshold €70k | `L05_NL_BV_threshold_70k.md` ✅ |

If you want to revisit any of these, the data is in
`docs/research/RESULTS/` (203 files). The 8 above are the capex-relevant
ones from Sprint 0.

---

**One more thing:** the canonical 15-list is at
[`docs/research/TOOLING/5_ONDERWERPEN_MATERIALS.md`](../TOOLING/5_ONDERWERPEN_MATERIALS.md).
The "5 of 6" framing in this doc is because Sprint 0 closed 8/15 on
2026-07-06; the 6 remaining items 9-14 are what you're picking from now.
Item 15 (customs duty calculator) is a 2-week Sprint 2 project, not a
research item.

**Aanpak:** Je hoeft alleen 5 nummers te kiezen. Erebus doet de rest.

*— Erebus, 2026-07-07*
