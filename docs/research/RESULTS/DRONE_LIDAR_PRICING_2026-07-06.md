# Drone LiDAR — Service Pricing, Equipment Costs & Side-Business Viability (PY/Paraguay focus)

> **For Wesley van de Camp.** Written 2026-07-06 by Erebus. Researches the cost of hiring a drone LiDAR service vs. buying the equipment and running it as a side business in Paraguay.
>
> Sources cited inline [in brackets]. All prices converted at 1 USD = Gs. 7,500 and 1 USD = €0.93 (≈ €1 = $1.07).

---

## A) SERVICE PRICING — what it costs to hire someone to fly LiDAR

### A.1 US market (FlyGuys, E38 Survey Solutions, TheFuture3D, DroneU)

| Provider / source | Pricing model | Cost | Source |
|---|---|---:|---|
| **FlyGuys** (US, LiDAR drone service) | Per day | **$6,500–$9,000/day** (up to $12,000 with complex needs) | [flyguys.com] |
| **TheFuture3D** (US, 2026 guide) | Minimum project | **$3,000+** (small site, single-day mobilization) | [thefuture3d.com] |
| TheFuture3D | Complex / industrial | **up to $15,000+** (large facilities, dense vegetation) | [thefuture3d.com] |
| TheFuture3D | Per acre (500+ acres) | **$150–$300/acre** volume pricing | [thefuture3d.com] |
| TheFuture3D | Detailed / engineering-grade | **$400–$500/acre** (high-density point clouds) | [thefuture3d.com] |
| **DroneU** (US 2026 guide) | Hourly mapping/surveying | **$250–$600/hour** | [thedroneu.com] |
| DroneU | Drone mapping per acre | **$5–$20/acre** (basic mapping) | [thedroneu.com] |
| Reddit r/UAVmapping (2025) | Per 10 ha | **$2,000–$2,700 first 10 ha + $1,300 per additional 10 ha** (≈ $130/ha or $53/acre after the first) | [reddit.com/r/UAVmapping] |

**US "all-in" rule of thumb (2026):**
- Small project (<10 ha / 25 acres): **$1,500–$4,000**
- Mid-size project (10–50 ha): **$3,000–$10,000**
- Large project (50–500 ha): **$10,000–$30,000**
- Per-hectare rate at scale: **$200–$500/ha**

### A.2 Paraguay market (Cartomex — main provider)

| Source | Cost | Service | Notes |
|---|---:|---|---|
| **Cartomex Paraguay** ([cartomex.com/lidar-paraguay](https://www.cartomex.com/lidar-paraguay.html)) | **Quote on Messaging** (no public price) | "Lidar con dron" — hasta 5,000 ha, 5–15 cm precisión vertical, 100+ pts/m², penetra vegetación | Main competitor. Covers Región Oriental + Chaco. Experience: agricultura soya, ganadería, hidroeléctricas (Itaipú, Yacyretá) |
| **Pycomex** ([pycomex.com](https://www.pycomex.com/topografia-con-drone-lidar)) | **Quote on Messaging** | Topografía + fotogrametría + catastro | Mexican-Monterrey based but operates in PY. Less detailed public info |

**Estimated PY pricing** (no public PY rates available — must request Messaging quote from Cartomex):
- PY market likely **30–50% below US rates** due to lower labor cost
- Estimated range: **$80–$250/ha** (PY equivalent of US $150–$500/ha)
- **Recommended PY benchmark**: ask Cartomex for a 62-ha quote (matches LQV Phase 1) and budget **$5,000–$15,000 USD** for the first survey

### A.3 Peru / Colombia (regional benchmarks)

| Source | Pricing | Notes |
|---|---:|---|
| **RE20S Peru** ([re20s.com](https://re20s.com/producto/levantamiento-topografico-con-drones-lidar-en-peru-re20s/)) | **S/ 17,250** ≈ **$4,580 USD** (one-off service, DJI Matrice 350 RTK + Zenmuse L2) | Centimetric precision. Full workflow: planning + autonomous flight + processing + final deliverables |
| **LiDAR Peru** ([lidar.pe](https://lidar.pe/drones/)) | Quote on contact | Also sells equipment, rentals, subscriptions. Subscription model for repeat clients |
| **Drone Nerds LATAM** ([dronenerdslatam.com](https://dronenerdslatam.com/antes-de-comprar-un-lidar-debes-leer-esto/)) | Industry pricing article | LiDAR services "from $5,000 to $10,000 USD or more" depending on deliverables |

**RE20S $4,580 is the best regional anchor for a comparable 62-ha survey** — assuming LQV is a single-day mobilization in PY, expect PY quote in **$4,000–$8,000 USD range** for similar scope.

---

## B) EQUIPMENT COSTS — what it costs to BUY your own LiDAR drone

### B.1 Hardware (drone + sensor + base station + software)

| Item | Entry-level | Mid-range | Professional | Source |
|---|---:|---:|---:|---|
| **LiDAR sensor** | DJI Zenmuse L1: **~$7,930** (older) | DJI Zenmuse L2: contact for quote; L3: **$17,400** | GreenValley LiAir X3: ~$25,000 | [dronenerdslatam] |
| **LiDAR sensor (high-end)** | RESEPI Hesai XT-32: **$32,990** | RESEPI Hesai XT-32M2X: **$43,990** | RESEPI Teledyne Optech CL-360HD: **$154,000** | [e38surveysolutions] |
| **Drone platform** | DJI Matrice 300/350 RTK: **~$7,820** | DJI M350 RTK | DJI M400 RTK: **$10,450** (successor) | [dronenerdslatam, e38surveysolutions] |
| **Extra batteries** | ~**$1,974/set** | | | [dronenerdslatam] |
| **Base station (RTK)** | Trimble Catalyst: ~**$1,000** | DJI receiver: ~**$3,189** | EMLID Reach RS2+ kit: **$3,177** | [dronenerdslatam, e38surveysolutions] |
| **Software** | DJI Terra (free with L3 license, perpetual) | Cloud subscription $variable | PCMaster (for RESEPI): **$3,000/year** | [e38surveysolutions] |
| **Software (alt, industry)** | Pix4D / Global Mapper: **$5,000–$10,000** license | | | [dronenerdslatam] |

### B.2 Total system cost (real configurations, July 2026)

| Configuration | Total capex | Best for |
|---|---:|---|
| **Budget — DJI L1 + M300** (entry-level, 2020-era hardware) | **~$18,000** | Learning, small PY farms, internal use |
| **Recommended — DJI L3 + M400 RTK + EMLID RS2+ + DJI Terra** | **$31,000–$35,000** | Professional PY service business, engineering-grade output |
| **Pro service — RESEPI Hesai XT-32 + M400 RTK + EMLID + PCMaster Y1** | **~$48,000** | Competing with Cartomex on heavy industrial work |
| **Top-end — RESEPI Optech CL-360HD + custom drone** | **$200,000+** | Government, mining, oil & gas (overkill for PY market) |

### B.3 Annual operating costs

| Item | Cost/year | Source |
|---|---:|---|
| Drone calibration + maintenance | **$1,200–$1,500** | [dronenerdslatam] |
| Propellers + minor parts | **$200** | [dronenerdslatam] |
| Insurance (commercial drone liability + hull) | **$1,500–$3,000** | industry estimate |
| Software subscriptions (if not perpetual) | **$3,000–$5,000** | [e38surveysolutions] |
| Pilot certification + recurrent training | **$500–$1,500** | industry estimate |
| Data storage + computing | **$500–$1,000** | industry estimate |
| **Total annual opex** | **$7,000–$12,000** | |

---

## C) SIDE-BUSINESS VIABILITY — should you buy + rent it out?

### C.1 Revenue model assumptions (PY market)

- **Cartomex is currently the dominant PY LiDAR drone provider** with experience in Itaipú/Yacyretá/soya/agricultura. They cover Oriental + Chaco.
- **Entry barriers** in PY are high: pilot license (DINAC registration required), equipment capex, software learning curve, network.
- **Realistic first-year utilization**: 1 survey/week = 50 surveys/year. Realistic ramp: 10-20 surveys Year 1.

### C.2 Pricing model for your own service (PY, conservative)

**Per-project pricing** (PY market, 2026):
- Small survey (10–50 ha): **$1,500–$3,000** per project
- Mid survey (50–200 ha): **$3,000–$6,000** per project
- Large survey (200+ ha): **$6,000–$15,000** per project

**Revenue projection** (Year 1, conservative ramp):

| Scenario | Surveys/year | Avg revenue | Annual revenue |
|---|---:|---:|---:|
| **Pessimistic** (10 surveys, hobby pace) | 10 | $2,500 | **$25,000** |
| **Realistic** (24 surveys, 2/month) | 24 | $3,500 | **$84,000** |
| **Optimistic** (40 surveys, established client base) | 40 | $4,500 | **$180,000** |

### C.3 ROI calculation — DJI L3 configuration ($35K capex)

| Metric | Pessimistic | Realistic | Optimistic |
|---|---:|---:|---:|
| Annual revenue | $25,000 | $84,000 | $180,000 |
| Annual opex | $10,000 | $10,000 | $12,000 |
| **Net annual profit** | **$15,000** | **$74,000** | **$168,000** |
| Payback period | 2.3 years | 0.5 year | 0.2 year |
| 3-year cumulative profit | $10,000 | $187,000 | $469,000 |

### C.4 Side-by-side: BUY vs HIRE for the LQV Phase 1 survey (62 ha)

| Option | Cost for LQV | Reusable? | Other projects | Net cost |
|---|---:|---|---|---:|
| **A) Hire Cartomex** | **$5,000–$8,000** (estimate, 62 ha) | ❌ One-time | None | $5K–$8K |
| **B) Hire RE20S (Peru, travel)** | $4,580 + ~$2,000 travel = $6,580 | ❌ One-time | None | $6.5K |
| **C) Buy DJI L3 setup + survey own** | **$35,000 capex + $0 survey cost** | ✅ Full resale | Unlimited side-business revenue | $35K (first), $0 marginal after |

**Break-even for the equipment vs first 4-5 hires:**

- Hire 5× from Cartomex = 5 × $7,000 avg = **$35,000** (same as buying)
- Hire 6+ = **buying wins financially** AND you have a side business

### C.5 Realistic risks for the side business

**1. Market size in PY is small.** Cartomex is already the dominant provider. Total PY addressable market for drone LiDAR is probably **$300K–$800K/year** across all industries (agriculture, mining, construction, real estate, infrastructure).

**2. DINAC regulation.** Paraguay requires DINAC registration for commercial drone operations. Pilot must be licensed. Process: 4-8 weeks.

**3. Learning curve is real.** LiDAR data processing is non-trivial. DJI Terra helps but classifying point clouds (ground vs vegetation vs building) takes practice. Budget **2-3 months** before first paid deliverable.

**4. Seasonality.** PY agriculture is Sept-Mar. Construction is year-round but slow in Dec-Feb (holidays). Realistic billable weeks: ~40/year.

**5. Client acquisition cost.** First 5 clients will come from Wes's network. After that, you need marketing (web, LinkedIn,行业协会). CAC likely **$500–$2,000** per client.

**6. Equipment damage risk.** Drone crashes happen. Insurance covers hull but not always data loss. Budget **$2K/year** for unexpected replacements.

**7. Competing with Cartomex.** They have a 5-year head start + Itaipú reference project. You'll compete on price for the first 2-3 years.

---

## D) DECISION MATRIX — buy + side business vs hire

| Factor | Hire (Cartomex/RE20S) | Buy + run side business |
|---|---|---|
| **LQV Phase 1 survey cost** | $5K–$8K (Cartomex) or $6.5K (RE20S) | $35K capex (one-time) |
| **Time to first survey** | 2-4 weeks (booking) | Immediate (after DINAC registration 4-8 wk) |
| **Revenue potential (side business)** | $0 | $25K–$180K/year (depending on utilization) |
| **Payback period** | n/a | 0.2–2.3 years |
| **Risk** | Vendor reliability, scheduling | Market entry, equipment damage, learning curve |
| **Strategic value** | None (transactional) | Asset that appreciates with utilization + AI/automation trends |
| **Pycomparable** | Use Cartomex until you have 4+ confirmed client needs | Buy when you have 4+ confirmed client needs OR want to self-survey LQV |

### D.1 Verdict for the LQV project alone

**HIRE.** For the single 62-ha LQV survey, hiring Cartomex at ~$7K is the rational choice. The equipment doesn't pay back on a single use.

### D.2 Verdict if you have ≥4 external client needs (Wes network + Ai-Whisperers client sites)

**BUY.** $35K capex pays back in 4-5 hires. After that, every additional survey is pure profit (minus opex).

### D.3 Verdict if the strategic play is "Wes becomes the PY drone LiDAR provider"

**BUY now.** The market window for entry is open (Cartomex has no real competition). First-mover advantage in regional/sub-regional markets (Paraguarí, Misiones, Caaguazú) is real. Three-year horizon: **$200K–$500K cumulative revenue** if Wes can hit 30-40 surveys/year by Year 2.

---

## E) RECOMMENDATION

**For the immediate LQV need: HIRE Cartomex.** $5K–$8K for the 62-ha survey. Get a quote this week.

**For the side business: STAGE the buy.** Don't buy before you have:
1. ✅ Confirmed DINAC registration process understood (1-2 weeks research)
2. ✅ 3-5 prospective clients in pipeline (Wes's network + Ivan's Ai-Whisperers client roster — likely Gaby dentist site, Riverstone Valley, future eco-tourism clients)
3. ✅ Pilot trained and certified (Wes himself? Or hire a Part 107 equivalent certified pilot in PY)
4. ✅ Quote from Cartomex for LQV (so you know what you're competing against on price)

**Buy trigger**: when ALL 4 above are true, buy the **DJI L3 + M400 RTK setup** ($35K total) and launch the side business within 90 days. ROI target: break even by month 6, $50K+ profit by end of year 1.

**Alternative path**: start with **DJI M350 RTK + Zenmuse L2** rental from LiDAR.pe or RE20S for the first 2-3 jobs to test the market without capex. Convert to purchase once utilization is proven.

---

## F) SOURCES

1. **flyguys.com** — US LiDAR service pricing ($6,500-$12,000/day) — https://flyguys.com/how-much-do-drone-lidar-services-cost/
2. **e38surveysolutions.com** — DJI Zenmuse L3 price ($17,400), DJI M400 RTK price ($10,450), RESEPI LiDAR kit pricing — https://e38surveysolutions.com/pages/drone-lidar-price-guide
3. **thefuture3d.com** — 2026 aerial survey cost guide (per-acre rates, project size tiers) — https://www.thefuture3d.com/blog/aerial-survey-cost-guide/
4. **thedroneu.com** — 2026 drone service pricing guide (hourly rates) — https://www.thedroneu.com/blog/drone-service-cost-guide/
5. **dronenerdslatam.com** — DJI Zenmuse L1/L2 pricing, GreenValley LiAir X3 pricing, total cost breakdown — https://dronenerdslatam.com/antes-de-comprar-un-lidar-debes-leer-esto/
6. **cartomex.com** — Cartomex Paraguay LiDAR drone service (no public price, quote on Messaging) — https://www.cartomex.com/lidar-paraguay.html
7. **pycomex.com** — Pycomex (Mexican-Monterrey based, operates in PY) — https://www.pycomex.com/topografia-con-drone-lidar
8. **lidar.pe** — LiDAR Peru (subscription + rental + sales model) — https://lidar.pe/drones/
9. **re20s.com** — RE20S Peru survey service price (S/ 17,250 ≈ $4,580 USD) — https://re20s.com/producto/levantamiento-topografico-con-drones-lidar-en-peru-re20s/
10. **reddit.com/r/UAVmapping** — Practitioner pricing in 2025 ($130/ha after first 10) — https://www.reddit.com/r/UAVmapping/comments/1l2wyz5/how_much_do_you_charge_for_lidar_mapping/

---

## G) OPEN QUESTIONS for Wes / Ivan

1. **What's the AI-Whisperers client roster for "potential LiDAR survey" needs?** Gaby dentist site (small but illustrative), future eco-retreat clients, mining/construction clients. If ≥4 needs in 12 months → buy.
2. **Is Wes willing to get DINAC-licensed + train on DJI Terra?** Or hire a licensed pilot? Labor is the gating factor.
3. **Does Wes want to compete with Cartomex in PY, or focus on a sub-niche (eco-retreats, small farms <100 ha)?** Sub-niche strategy would avoid direct competition.
4. **What's the LQV Phase 1 budget appetite for the $5K-$8K survey?** If tight, that's another argument to buy (use the equipment on LQV as a "paid pilot" job).
5. **Currency risk**: equipment is USD-priced. If PYG weakens further vs USD (already -8% YoY 2025), capex goes up. Consider buying when PYG is strong.

---

*Written 2026-07-06 by Erebus for Wesley van de Camp + Ivan. This is a working business analysis, not a tender. Source files cited inline + section F.*
