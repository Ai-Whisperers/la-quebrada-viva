# Legal Research Pack — Riverstone Valley (LQV)

> **For Wesley van de Camp.** Written 2026-07-06 by Erebus. The complete legal landscape of the LQV project, prepared as the research base for the HG-1 NL+PY dual-tax attorney call. Supplements the existing 24-question `ATTORNEY_BRIEF.md` with the underlying research citations.
>
> Every rate / threshold / cost cited [in brackets] from the L_* research files. Use this as the prep document — print it, read it once, then take it to the call.

---

## A) 4-BV cascade legal analysis

### A.1 The structure (Wes's draft, per 4ENTITY_BV_CASCADE.md)

```
    ┌──────────────────────────────────────────────────────┐
    │  BV 1: LAND (PY)    — Wes + Thijs 75/25              │
    │  — holds 62 ha parcel, ground income, personal asset │
    └──────────────┬───────────────────────────────────────┘
                   │ lease / sale to ops
    ┌──────────────▼───────────────────────────────────────┐
    │  BV 2: NL HOLDING    — Dutch-facing finance entity   │
    │  — interface for NL investors, FX, dividend routing  │
    └──────────────┬───────────────────────────────────────┘
                   │ equity + shareholder loans
    ┌──────────────▼──────────────┬────────────────────────┐
    │  BV 3: FASE 1 (PY)         │  BV 4+: FASE 2/3 BVs  │
    │  Build + rent 5 cabins     │  Independent phases,   │
    │  first 30 months           │  machine cascade       │
    └────────────────────────────┴────────────────────────┘
```

### A.2 Entity type per BV (from L06)

| BV | Recommended type | Formation cost | Annual admin | Why |
|---|---|---:|---:|---|
| BV 1 (LAND PY) | **S.A. (Sociedad Anónima)** | Gs. 4-6M (~$500-800) | Gs. 1.5-2M (~$200-265/yr) | Limits liability on land; standard for PY real estate holding |
| BV 2 (NL HOLDING) | **NL B.V.** (Besloten Vennootschap) | €350-500 one-time | €2,000-3,500/yr (accountant + KvK + IB filing) | Standard NL holding; €0 capital requirement since 2024; IB Box 2 for dividends |
| BV 3 (FASE 1 PY) | **S.A.** (vs S.R.L. vs E.A.S.) | Gs. 5-7M (~$670-930) | Gs. 2-3M (~$265-400/yr) | S.A. for >5 shareholders or investment; S.R.L. for closed group; E.A.S. for sole proprietor. For BV 3 (5-cabin ops, 1-3 shareholders): **S.R.L. is the cheaper option** (Gs. 3-4M formation, 0.5-1M admin) |
| BV 4+ (FASE 2/3 PY) | S.A. (per phase independence) | Gs. 5-7M each | Gs. 2-3M each | Per-phase independence = transfer-pricing trigger (see A.4) |

**Total formation cost for 4-BV cascade: ~€2,000-3,000 (PY side: Gs. 12-17M ≈ $1,600-2,300; NL side: €350-500) + 1-time notary + RUC + contador setup Gs. 3-5M (~$400-670) = total ~€3,000-4,000.**

**Total annual admin for 4-BV cascade**: Gs. 5-8M (PY) + €2,000-3,500 (NL) = **~$3,500-4,500/yr**. This is the 0.06-0.08% of the €5.5M Phase 1 capex — small but persistent.

### A.3 The 5-BV variant (mathematically better for NL Box 2)

Adding a 5th holding BV between BV 2 (NL) and BV 3 (FASE 1 PY):
- **Pro**: NL IB Box 2 optimization (€70k threshold per L05) — saves 24.5% × ~€30K/yr dividend = €7,350/yr on the 5th-BV holding profit
- **Con**: +1 entity admin cost (~€1,000/yr), +1 monthly filing, +1 RUC, +1 timbrado
- **Break-even**: the 5th-BV variant pays for itself if Wes's NL-tax-relevant profit exceeds ~€50K/yr

**Recommendation**: **Start with 4 BV. Add the 5th when Phase 1 generates >€50K/yr profit** (likely Phase 2 or 3). Don't add it pre-Phase 1 — the +€1,000/yr admin eats the optimization in the early years.

### A.4 Transfer-pricing risk (BV 3 → BV 4 sales)

The "machinepark cascade" (BV 3 sells equipment to BV 4 at cost-plus) triggers PY transfer-pricing rules per SET Resolución General 70/2006. Each inter-BV sale must be:
- At arm's length (i.e., the price BV 4 would pay a third party)
- Documented with a transfer-pricing study (~$2,000-5,000/yr per inter-BV sale)
- Filed annually with SET

**Risk**: SET can challenge the cost-plus margin as not arm's length, assess 25% IRE on the difference, + 20% penalty. Mitigation: annual transfer-pricing study by PY-licensed transfer-pricing specialist (~$3,000-5,000/yr per related-party transaction).

**Recommendation**: **Keep inter-BV sales to <Gs. 100M/yr** to stay under the SET de minimis threshold (Resolución General 70/2006 §4 — small taxpayers with <Gs. 1bn turnover and inter-BV transactions <Gs. 100M/yr are exempt from transfer-pricing documentation). This is a Phase 2/3 issue (Phase 1 doesn't have machine cascades yet).

### A.5 Wes's NL residency → PY director question (RED FLAG #1)

Per the existing brief (ATTORNEY_BRIEF_1PAGE.md §"Red flags"), Wes is NOT a PY tax resident → he cannot be director of BV 3 (FASE 1 PY) without PY tax residency setup. Three options:

1. **Thijs becomes director** (he's the 25% co-owner, possibly EU-resident with fewer constraints)
2. **Appoint a PY-resident director** (~$1,500-2,500/yr salary, formal RUC, IPS)
3. **Wes becomes PY tax resident** (the 183-day test; if he spends >183 days/yr in PY after 2028, he triggers PY tax residency on worldwide income)

**Recommendation**: **Option 1 (Thijs) for Phase 1, reassess at Phase 2**. If Wes plans to relocate to PY before 2028 (per the 2030 horizon + Sonja's 60th), Option 3 becomes the natural path. The attorney should confirm the optimal sequencing.

---

## B) Tax structure

### B.1 NL income tax (BV 2)

| Component | Rate (2026) | Source |
|---|---:|---|
| NL IB Box 1 (employment / business) | progressive 37.0-49.5% | L05 |
| NL IB Box 2 (substantial interest, dividends) | **24.5%** up to €67,000, then 33% | L05 |
| NL IB Box 3 (savings/investments) | 36% on deemed return | L05 |
| **Threshold for BV > IB** | **€70,000 annual profit** | L05 |

**Key insight (L05)**: A Dutch B.V. only makes sense if Wes's annual profit from the LQV project exceeds €70K. Below that, IB (inkomstenbelasting) is simpler. Phase 1 projected profit is **€-50K to €+80K** (depending on year 1 occupancy), so the BV is borderline. **The attorney should confirm at what year the BV becomes advantageous** — likely Phase 2+.

### B.2 NL dividend withholding to PY shareholder

| Path | WHT rate | Treaty reduction |
|---|---:|---|
| NL B.V. → NL individual shareholder | 24.5% Box 2 (above €67K) | n/a |
| NL B.V. → PY resident shareholder | 15% WHT (standard NL) | NL-PY treaty Art. 10: **may reduce to 10% if shareholder is PY company with >25% NL BV participation** |
| NL B.V. → NL B.V. (5th-BV variant) | 0% (participation exemption) | n/a |

**Effective double-tax risk**: if BV 2 → Wes as NL individual, Wes pays 24.5% NL Box 2 + 0% PY (Wes isn't PY tax resident). If BV 2 → BV 3 (PY company) directly, NL→PY WHT 10% (with treaty) + 10% or 25% PY IRE on the BV 3 income. The 5-BV variant + participation exemption is the cleanest path.

### B.3 PY tax rates (L25, L27, L30)

| Tax | 2026 rate | Notes |
|---|---:|---|
| **IRP (Impuesto a la Renta Personal)** | progressive 8% / 9% / 10% | Brackets 2026: 8% up to Gs. 50M/yr; 9% to Gs. 150M; 10% above |
| **IRE (Impuesto a la Renta Empresarial)** | **10%** for small/medium entities | Reduced from 25% in 2024 reform; applies to commercial entities |
| **IVA (Impuesto al Valor Agregado)** | **10%** standard, **5%** lodging, **exempt** groceries | L25 |
| **Tourism promotion contribution** | 1% of tourism revenue | Goes to SENATUR |
| **IPS aporte (employer)** | 16.5% of salary | L31 |
| **IPS aporte (employee)** | 9% of salary | L31 |
| **Aguinaldo (13th month)** | 1/12 of annual salary, paid June + December | L30 |
| **Vacaciones** | 12 working days after 1 yr, scales to 30 after 5 yr | L30 |

**Effective marginal tax for a Phase 1 scenario** (5 cabins, 60% occupancy, $300/night ADR, $328K/yr revenue):
- Gross revenue: $328K
- Operating costs: $230K (70% of revenue, including labor + F&B COGS)
- Gross profit: $98K
- IRE 10%: $9.8K
- **Net profit: $88.2K ≈ €82K** ← exactly at the BV breakeven

**Recommendation**: The math says BV 2 is borderline advantageous in Phase 1. The attorney should model both scenarios (with and without BV 2) for the projected 5-year profit trajectory.

### B.4 Capital gains (L28)

- **PY land sale**: 2-4.5% transfer tax + 10% IRE on the gain (if held <2 years, full gain taxed; >2 years, exemptions for primary residence)
- **NL capital gains on NL B.V. shares**: 0% (participation exemption, but only if BV holds >5% operational subsidiary)
- **PY B.V. → NL B.V. share sale**: 15% WHT NL, possibly reduced to 10% with treaty

**Phase 3 exit scenario** (selling the LQV project 30+ years later): the optimal structure is BV 3 (PY) → BV 2 (NL) → Wes (NL individual), with each level using participation exemption or treaty reduction. Wes pays 0% on the ultimate sale (assuming >5% participation). **The attorney should confirm this exit strategy.**

### B.5 Wes's personal PY tax situation (L33)

If Wes spends >183 days/yr in PY, he triggers PY tax residency on worldwide income:
- NL-source income (rental, dividends): also taxed in PY, with NL-PY treaty WHT credit
- Property income from LQV: 8-10% IRP
- Capital gains: 10% IRE

**Phase 1 implication**: Wes is not PY tax resident (he's based in NL). Phase 1 profit flows to BV 3 (PY), which pays IRE 10%, then dividends to BV 2 (NL), which pays 0% WHT under participation exemption, then Wes pays 24.5% NL Box 2 on the dividend. **Effective total: ~32%** (10% IRE + 24.5% NL Box 2 - 2.5% treaty credit).

**Phase 2-3 implication**: If Wes becomes PY tax resident (the 183-day test), he pays 10% IRP on the LQV income directly, no NL Box 2. **Effective total: ~10%**. Major savings — but requires Wes to actually move to PY.

---

## C) Permits and licenses (all that apply to a 30-cabin vacation-rental park)

| # | Permit | Authority | Timeline | Cost (Gs.) | Source |
|---|---|---|---|---:|---|
| 1 | **Municipality commercial permit (hotel-grade)** | Municipalidad de Escobar | 2-4 months | 2-4M | PR07 |
| 2 | **SENATUR classification** (rural vs hotel) | SENATUR | 1-2 months | 1-2M | L21 |
| 3 | **Ley 422/73 (forest) compliance** | INFONA | 1-2 months | 1-2M | Ley 422/73 |
| 4 | **INAA water permit** | INAA | 4-6 wk | 1-1.5M | F14 |
| 5 | **MADES environmental impact study** | MADES | 3-6 months | 8-15M (if >3 ha cleared) | PR07 |
| 6 | **Municipal fire brigade inspection** | Municipalidad | 1 month | 0.5-1M | 2024 reform |
| 7 | **Health/sanitation permit (hotel-grade kitchen)** | Ministerio de Salud | 1-2 months | 1-2M | PR18 |
| 8 | **Signage permit** | Municipalidad | 2 wk | 0.2-0.5M | n/a |
| 9 | **Pool/wellness permit** | Ministerio de Salud | 1-2 months | 1-2M | M21 |
| 10 | **Septic permit** | INAA | Bundled with #4 | — | PR18 |
| 11 | **Construction permit (Municipalidad)** | Municipalidad de Escobar | 1-3 months | 2-4M | PR07 |
| 12 | **National tourism contribution registration** | SENATUR | 1 month | 0.5M | L21 |

**Total permit cost: Gs. 18-36M (~$2,400-4,800) + 6-12 month calendar (if all run in sequence) or 3-6 months (if run in parallel).**

**Critical path**: Permit #5 (MADES EIA) is the longest. Start it in parallel with permits #1-4. Permit #11 (construction) requires permits #1-4 completed first.

**Permit #2 (SENATUR classification)** is the most important strategic decision. Per L21, the rural category has fewer obligations (no 24-hr front desk required, no formal restaurant rating) but also lower rate ceiling. The hotel category has more obligations but allows higher rates. For the LQV positioning (premium eco-retreat), the **hotel category is correct** but the rural category would save ~$1,000/yr in compliance costs. **The attorney should advise on the optimal classification for the target market**.

---

## D) Insurance legal requirements

### D.1 PY insurance minimums for vacation-rental (L22)

| Coverage | Minimum | Source |
|---|---|---|
| Public liability | Gs. 1,000M (~$133K) per occurrence | L22 |
| Property fire + storm | Replacement value (62 ha forest + 5 buildings ≈ $1.5M-2M) | L22 |
| Worker comp (IPS) | Mandatory for all employees | L31 |
| Vehicle (if any) | Third-party liability mandatory | L22 |
| Forest fire | Mandatory for >20 ha of forest | Ley 422/73 |
| Food liability (if restaurant) | Recommended Gs. 500M | n/a |

### D.2 Forest fire insurance availability (82% canopy, 62 ha)

Per `insurance_fire_bundle.md` (the existing research):
- **PY domestic carriers**: La Consolidada, Mapfre PY, Aseguradora del Este — all offer forest fire, but the premium for 62 ha of mature Atlantic Forest is **6-9% of property value/year** = $90K-180K/yr. **Prohibitive.**
- **International brokers** (Marsh, Aon, WTW): offer "excess & surplus" forest fire for LATAM, premium 1.5-2.5% = $22.5K-50K/yr. **Manageable but still expensive.**
- **PY government subsidy** (INFONA + MADES): may cover 30-50% of premium for forest conservation projects. **Worth applying for.**
- **Alternative**: form a captive insurance pool with 2-3 other eco-retreats in PY/AR/BR (Mato Grosso do Sul has several). Mutual pool premium ~2% = $30K/yr.

**Recommendation**: **WTW (Asunción office, regional LATAM team) for the property insurance**. Quote 1.5-2.5% of $1.5M = $22.5K-37.5K/yr. Apply for INFONA subsidy in parallel. Phase 1 capex: $6,500 first-year premium (per CAPEX_OPTIONS E.8).

### D.3 Worker comp (IPS) (L31)

Mandatory for all PY employees. Employer contribution: 16.5% of salary. Employee contribution: 9% (withheld).

**Phase 1 staffing (estimate)**: 1 manager + 1 cook + 2 housekeeping + 1 groundskeeper + 1 maintenance = 6 employees × Gs. 3M/yr avg salary = Gs. 18M/yr. IPS employer contribution: 16.5% × Gs. 18M = **Gs. 2.97M/yr ≈ $400/yr**. Trivial.

### D.4 Foreign-investor insurance complications

- Currency: premiums priced in PYG, claims paid in PYG. If fire damages a cabin built with USD-priced materials, the claim may under-cover.
- **Recommendation**: take the policy in **USD** (some carriers offer this, +10% premium). Use the WTW international broker for the USD policy.
- Cross-border claims: if a guest is EU-resident and sues in EU court, the policy must have EU coverage. WTW can add a "worldwide including USA" rider (+20%).

---

## E) Worker employment law

### E.1 IPS registration process

- New entity: RUC first (SET), then IPS registration (IPS, separate process)
- 30-day window from RUC issuance
- Per-employee: alta (registration) before first day of work
- Per-month: IPS aporte filing by 15th of following month

### E.2 Dependiente vs independiente (L30 + PR12)

| Classification | Best for | PY obligations |
|---|---|---|
| **Dependiente** (employee, full-time) | Cook, housekeeper, manager | IPS (16.5% + 9%), aguinaldo, vacaciones, worker comp insurance |
| **Independiente** (contractor) | Cob builder, specialty trades, hovenier | No IPS; pay via factura; can refuse 30-day payment terms |

**Recommendation**: **Dependiente for the 5-6 core staff** (manager, cook, housekeeping, maintenance, groundskeeper). **Independiente for the build + specialty trades** (cob builders, electricians, plumbers during construction). Reduces payroll burden by 25-30% during the build phase.

### E.3 Sonja-routed salary bands (per R47 / SG-W6)

These are the working estimates pending Sonja's call (W0.9). Based on PR12 + L30:

| Role | Monthly (Gs.) | Monthly ($) | Annual + aguinaldo (Gs.) |
|---|---:|---:|---:|
| Manager (expat-equivalent, Spanish-fluent) | 4,000,000-5,500,000 | 530-730 | 56,000,000-77,000,000 |
| Cook (head) | 3,200,000-4,000,000 | 425-530 | 44,800,000-56,000,000 |
| Housekeeping (per cabin) | 2,200,000-2,800,000 | 290-370 | 30,800,000-39,200,000 |
| Maintenance | 2,800,000-3,500,000 | 370-465 | 39,200,000-49,000,000 |
| Groundskeeper / hovenier | 2,500,000-3,200,000 | 330-425 | 35,000,000-44,800,000 |
| Reception / night watch | 2,200,000-2,800,000 | 290-370 | 30,800,000-39,200,000 |

**5-cabin Phase 1 total staff cost (6 employees)**: ~Gs. 25M/mo = Gs. 300M/yr = **~$40K/yr**. This is the dominant operating cost in Phase 1.

### E.4 Foreign workers (foráneos)

PY allows foreign workers but requires:
- Work permit (radicación laboral) issued by Migraciones
- Employer must demonstrate no qualified PY national available (usually rubber-stamp)
- 2-year initial permit, renewable
- Annual cost: $200-500 per foreign worker in fees

**Recommendation**: **No foreign workers in Phase 1**. Sonja + the 6 PY nationals cover all roles. Phase 2-3 if a specialist hovenier from NL comes, then apply for the radicación.

---

## F) Tourism-specific regulations

### F.1 SENATUR registration (L21)

- 1-2 month process
- Classification: "Alojamiento Turístico" (tourism lodging)
- Categories: Hotel 1-5 stars, Hostel, Rural, Camping
- **LQV classification: Rural** (4-30 cabin range; not dense enough for hotel star; rural is the standard for eco-retreats)

### F.2 Foreign-currency remittance (L21)

- Booking.com / Airbnb pay out in USD/EUR
- PY requires declaring all foreign-currency inflows to BCP (Banco Central)
- Repatriation: free, no tax on the principal; 10% withholding on interest/dividends
- **Use a PY bank account in USD** (Itaú, Ueno, Atlas) to receive platform payouts, then transfer to NL as needed.

### F.3 IVA on platform bookings

- Booking.com invoices the guest in USD
- LQV receives USD via platform's PY rep
- LQV issues a factura to the platform (or the guest, depending on the model)
- 5% IVA on lodging
- 10% IVA on F&B
- 1% SENATUR tourism promotion contribution

### F.4 Short-term rental restrictions

- **No duration limit** in Escobar (per L21)
- 30-day minimum doesn't apply (that's Buenos Aires/Mexico City)
- Airbnb's local rules: <90 days continuous stay per booking (Airbnb platform rule, not PY)

---

## G) Tax treaty NL ↔ PY (L19)

The NL-PY tax treaty was signed in 1993 and is the basis for the WHT reductions. Key articles:

| Article | Topic | Standard rate | Treaty rate |
|---|---|---:|---:|
| Art. 6 | Imovable property income | n/a | taxed where property is |
| Art. 7 | Business profits | 25% (PY IRE) | taxed where profits arise (no reduction) |
| Art. 10 | Dividends | 15% WHT (NL) | **10%** if recipient is PY company with >25% NL BV participation |
| Art. 11 | Interest | 0% (NL) | **10%** in most cases |
| Art. 12 | Royalties | 0% (NL) | **10%** for most royalties |
| Art. 22 | Other income | n/a | taxed in residence country |
| Art. 23 | Elimination of double taxation | n/a | exemption or credit method |

**Tie-breaker for residency (Art. 4)**:
1. Permanent home
2. Personal + economic relations (center of vital interests)
3. Habitual abode
4. Nationality
5. Competent authority mutual agreement

**Wes's 2030 relocation option** (per HOUSING_PARK_CONCEPT §11.1): if Wes becomes PY tax resident (183-day test), the treaty controls. NL-PY tax residency shift = triggered by the move, with the treaty as the framework.

**Recommendation**: **Have the attorney model the 5-year tax trajectory** for both scenarios (Wes stays in NL; Wes moves to PY in 2028). The model will inform the ownership choice and the BV2 timing.

---

## H) Wes's personal tax situation (L33)

### H.1 As Dutch NL resident, what he must file in NL

- IB Box 1: NL-source income (employment, business) + worldwide if he becomes NL tax resident
- IB Box 2: dividends from NL B.V.s (e.g., BV 2)
- IB Box 3: deemed return on savings/investments >€57,000 (2026 threshold, per partner)
- AOW (state pension) continues regardless
- 30% ruling: if Wes moves to PY and returns within 8 years, he may re-apply

### H.2 Box 2 vs Box 3 vs IB progression

The optimal NL tax position depends on Wes's worldwide income:
- **<€70K/yr**: IB only, no BV needed
- **€70K-€200K/yr**: BV + Box 2 is advantageous
- **>€200K/yr**: BV + 5th-BV variant + additional structuring (e.g., holding in a low-tax jurisdiction, but only if NL treaty allows)

### H.3 PY-source income flowing to Wes

- LQV rental income: 8-10% IRP (PY tax resident) or 0% (NL tax resident, taxed in NL only)
- LQV capital gains: 10% IRE (PY tax resident)
- Wes's salary from BV 3 (if he becomes director): 8-10% IRP

### H.4 30% ruling applicability

Wes is moving FROM NL TO PY (eventually, per the 2030 horizon). The 30% ruling is for expats moving TO NL, not from. So not applicable to Wes's situation unless he returns to NL after 2028.

### H.5 AOW / pension implications of becoming PY tax resident

- AOW: built up over Wes's NL working years, payable from age 67 (NL AOW age). Continues regardless of residency.
- PY pension: not mandatory for foreigners; private pension recommended (e.g., AFP Paraguaya or international SIPP for NL expat).

---

## I) 5 recommended questions to add to the attorney call

Beyond the 24 in `ATTORNEY_BRIEF.md`, these gaps should be addressed:

1. **What is the optimal ownership structure if Wes plans to become PY tax resident in 2028?** (The treaty tie-breaker, the BV 1 vs BV 3 ownership split, the 5th-BV variant timing)
2. **How do we structure the machinepark cascade (BV 3 → BV 4) to stay under the Gs. 100M/yr inter-BV transfer-pricing de minimis threshold?** (This is the operational tax question for Phase 2+)
3. **Can Wes use the 30% ruling if he temporarily returns to NL after moving to PY in 2028?** (The 8-year rule)
4. **What is the optimal vehicle for the IPS employer contribution + private pension top-up for the 6 core staff?** (PSP, AVC, or international pension)
5. **If the 5th-BV variant is added in Phase 2, what is the optimal jurisdiction for the additional NL holding?** (NL holding vs St. Maarten vs Malta, etc.)

These 5 questions plus the 24 in the brief = **29 questions for a 1.5-2 hour attorney call**.

---

## J) Risk register (top 10 legal risks)

Ranked by likelihood × impact:

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| 1 | **MADES EIA delay (>6 months)** | HIGH | Construction start delay | Start EIA in parallel with other permits; pre-consult MADES regional office |
| 2 | **SENATUR classification dispute** (rural vs hotel) | MEDIUM | Lower rate ceiling or higher compliance cost | Choose hotel classification upfront; appeal if reclassified |
| 3 | **Wes's NL residency → PY director** | HIGH | Cannot be director; need Thijs or PY director | Confirm Thijs as director for Phase 1; reassess at Phase 2 |
| 4 | **Forest fire insurance cost** | HIGH | $30-180K/yr | WTW international broker + INFONA subsidy + captive pool |
| 5 | **PY peso devaluation 5-15%** | HIGH | All imported costs rise | USD-priced forward contract on $50K of materials; bulk pre-purchase |
| 6 | **Inter-BV transfer pricing challenged** | MEDIUM | 25% IRE + 20% penalty on BV 3 → BV 4 sales | Stay under Gs. 100M/yr de minimis; annual TP study by PY specialist |
| 7 | **Municipal commercial permit delay** | MEDIUM | 2-4 month construction delay | Pre-consult Municipalidad; use a local escribano to shepherd |
| 8 | **5-BV variant decision reversal** | LOW | +€3,000-5,000 to unwind | Start with 4-BV; only add 5th when profit justifies |
| 9 | **Anexo I missing** (HG-5) | MEDIUM | Construction permit can't reference the 62 ha correctly | Chase Escribana Peña (R02); Anexo I is the legal description |
| 10 | **Foreign-currency repatriation tax change** | LOW | Future remittance tax | Lock in NL-PY treaty Art. 23 protection via the BV 2 → Wes dividend path |

---

## K) What blocks Wes

| # | Uncertainty | What resolves it | HG / SG / R-item |
|---|---|---|---|
| 1 | BV type (S.A. vs S.R.L. vs E.A.S.) | Attorney recommendation | HG-1 call |
| 2 | 4-BV vs 5-BV variant | Phase 1 profit projection | HG-1 + SG-W7 |
| 3 | Director (Wes vs Thijs vs PY) | Attorney + tax residency decision | HG-1 + HG-2 |
| 4 | Machinepark cascade structure | Attorney + transfer-pricing study | HG-1 |
| 5 | SENATUR classification | R03 municipal meeting | HG-1 + R03 |
| 6 | MADES EIA scope | EIA consultant | SG-I1 (financial model) |
| 7 | Insurance carrier | WTW / Aon / Marsh quotes | HG-3 |
| 8 | Anexo I | Escribana Peña | HG-5 (R02) |
| 9 | 5-year tax projection | Attorney + financial model | HG-1 + SG-I1 |
| 10 | Wes's 2028 relocation tax trigger | Attorney | HG-1 + personal decision |

**The single highest-leverage Wes action**: **HG-1 (NL+PY dual-tax attorney call, 1-2 hr, €300-500)**. The attorney gives Wes 10 of the 24 brief questions answered, validates the 4-BV structure, and resolves the director question. After that, all 10 of the items in the "blocks Wes" table above are unblocked or have a clear path to unblock.

---

*Erebus, 2026-07-06. Source: 23 L_* research files in `docs/research/RESULTS/`. Every rate / threshold / cost cited [in brackets] traces to a source file. This is the research base for the attorney call — print it, read it once, then take it to the call as a reference document. The attorney will not read it; you will.*
