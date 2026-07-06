# Session Digest — 2026-07-06 (CAPEX matrix + Drone LiDAR research)

> **For Wesley van de Camp.** Plain-English summary of what Erebus shipped today that matters to you.
> 5-minute read.
>
> **Session:** 2026-07-06 (single afternoon session)
> **From:** Erebus (AI Whisperers)

---

## What was done

Two big research outputs that directly affect Phase 1 planning + a potential side business:

### 1. 📊 CAPEX OPTIONS for Phase 1 — full decision matrix

**The question:** "What does Phase 1 actually cost, and where should I spend vs save?"

**The answer:**
- **Recommended Phase 1 construction capex: €216,475 (~$231K)** — fits well inside the €1.4M construction block of the €5.5M master plan
- 8 decisions analyzed (cabin typology, roof, foundation, power, water, sewage, restaurant, expansion path) with Budget/Mid/Premium options each
- **4 self-corrections caught** before publishing (the subagent's first pass had internal arithmetic errors — the published version is the corrected one)

**The single biggest decision**: **Cabin typology = Cob** (saves €49K vs timber+brick, brand-anchor, lowest fire risk). Cob builders Roberto Abente and Cooperativa Ñandutí are the first calls to make.

**Hidden costs (€115K)** that bite first-time builders: permits, ANDE 3-phase, INAA water permit, MADES environmental study, road upgrade, insurance, professional fees.

**Full docs:**
- 📄 `CAPEX_OPTIONS_2026-07-06.md` (463 lines, the engineering-honest version)
- 📄 `CAPEX_QUICK_REFERENCE.md` (1 page, 5-min read — start here)

### 2. 🛸 Drone LiDAR — pricing + side business analysis

**The question:** "Should we buy a drone LiDAR setup, or hire Cartomex?"

**The answer:**
- **For LQV Phase 1 alone (62 ha)**: **HIRE Cartomex** (~$5K-$8K, quote-only via WhatsApp). Cartomex is the dominant PY provider with Itaipú/Yacyretá/soya experience. No public pricing.
- **For a side business**: only buy if you have **4+ external client needs** in 12 months. $35K capex (DJI L3 + M400 RTK + EMLID base station) pays back after 4-5 hires. After that, every additional survey is profit.
- **Strategic play** (if you want to become the PY LiDAR provider): market window is open — Cartomex has no real competition. 3-year horizon: $200K-$500K cumulative revenue if you hit 30-40 surveys/year by Year 2.

**The 4-gate test** (don't buy until ALL are true):
1. DINAC registration process understood
2. 3-5 prospective clients in pipeline
3. Pilot trained + certified
4. Real quote from Cartomex in hand

**Full docs:**
- 📄 `DRONE_LIDAR_PRICING_2026-07-06.md` (222 lines, 10 sources)
- 📄 `DRONE_LIDAR_QUICK_REFERENCE.md` (1 page, 3-min read — start here)

### 3. 📚 NEW: Master INDEX of all 151 research files

Until today, the 151 files in `docs/research/RESULTS/` had no catalog. Wes couldn't easily find what research existed on any topic.

**The new `INDEX.md`** organizes them by topic prefix (V/W/R/M/F/L/PR/EN/FT/AH/MC/MK/OP/PA/BD/SX/X/XL/WP/IR/BR/D/NEW) with 1-line descriptions of every file. Plus a "Quick links for the 5 next decisions" section at the bottom.

📄 `INDEX.md` — searchable catalog of all research files

---

## What this means for you (Wes)

**Immediate actions** (this week):
1. **Print `CAPEX_QUICK_REFERENCE.md`** — 1 page, the capex matrix in your pocket
2. **Call Cartomex on WhatsApp** — get a real quote for the 62-ha LQV Phase 1 survey. Use the message template: "Auditores de la Guerra del Chaco style — we're 62 ha in Escobar, Paraguarí, want LiDAR survey before construction starts, 5 cabin sites + restaurant + pool area, need MDT + classified point cloud, when can you fly + what's your rate?"
3. **Decide on the cob cabin call** — Roberto Abente in Asunción is the first builder to contact (most active in PY, 20+ projects 2018-2026). Say "60-70 m² cob cabin in Escobar, Paraguarí, 5 cabins in Phase 1, want a per-cabin quote + crew availability"
4. **Talk to Ivan about the side-business play** — is there appetite in Ai-Whisperers to develop LiDAR as a service line? Gaby + future eco-retreat clients + Riverstone Valley = 3 potential needs in 12 months.

**Medium-term actions** (next 30 days):
- Wait for Cartomex quote → compare against the $35K buy scenario
- Wait for cob builder quotes → confirm the €91K / 5-cabin assumption
- Add the R35 LiDAR drone flight to your to-do list ($1,500, 1 wk delivery) — unblocks foundation decisions for all 5 cabins

---

## What's still open (not solved today)

- **Solar pricing** — F09 + F10 give ballpark (9.6 kW Phase 1 = $15,430 + $30-36K LiFePO4 = $52,800 total). Need a Victron/Fronius dealer quote in Asunción to confirm.
- **Cob labor market in PY** — only ~15-20 trained cob builders nationwide. Tight market. Wes might need to import a Bali/international trainer (R37) if Roberto Abente isn't available.
- **Restaurant equipment vendors** — Gastro-Haus + Brasitermo + local ferretería = $48K. Need actual quotes (1 hr of calls).
- **Foundation stone** — 3 quarries named (Piribebuy, Sapucaí, Itá), pricing Gs. 35-60k/m³. Need actual quotes.

---

## Documents shipped this session (5 new + 1 fix)

| File | Size | Purpose |
|---|---:|---|
| `docs/research/RESULTS/CAPEX_OPTIONS_2026-07-06.md` | 463 lines | Full capex matrix + 8 Wes-decisions |
| `docs/research/RESULTS/CAPEX_QUICK_REFERENCE.md` | 1 page | 5-min summary for fast reading |
| `docs/research/RESULTS/DRONE_LIDAR_PRICING_2026-07-06.md` | 222 lines | Drone LiDAR pricing + side business |
| `docs/research/RESULTS/DRONE_LIDAR_QUICK_REFERENCE.md` | 1 page | 3-min summary for fast reading |
| `docs/research/RESULTS/INDEX.md` | 151 files cataloged | Master index of all research files |
| **Fix**: `CAPEX_OPTIONS_2026-07-06.md` self-correction log | 4 corrections | Section B had wrong numbers — Section D was right — Section C now rebuilt from corrected D |

---

## Quality note

The capex subagent's first pass had 4 internal arithmetic errors (roof 3x too low, power 40% too high, sewage 40% too high, restaurant 37% too high). All were caught + fixed + documented in the **self-correction log at the top of CAPEX_OPTIONS_2026-07-06.md**. The published matrix is consistent — but if you spot a number that doesn't match your intuition, check the self-correction log first.

---

*Erebus · 2026-07-06 · Total session: ~30 minutes of research + 20 minutes of QA fix + 15 minutes of doc structure work. All committed + pushed to Ai-Whisperers/la-quebrada-viva@master.*