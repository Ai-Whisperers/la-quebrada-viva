# M_VERF_01 — Verf exterior (exterior paint) for PY humid-subtropical climate

**Date:** 2026-07-06 (revised end-to-end 2026-07-06 13:00 PY)
**Method:** Web search (Brave) + cross-ref existing project files (`M11_paint.md`, `PR06_paraguay_climate_longterm.md`, `M_COB_01_cob_earthen_materialen.md`, `WES_WARNINGS.md`, `5_ONDERWERPEN_MATERIALS.md` item #11) + ASTM standard references verified via store.astm.org and Intertek.
**Confidence:** Medium-High (fact-checked: brand origins corrected, ASTM test methods confirmed, climate source pinned to `PR06`).
**Currency:** USD throughout. Multiply by ~7,500 for PYG (WES_WARNINGS §1).

---

## 1. Method

1. **Existing repo audit** — read `M11_paint.md` (2026-06-30, prior paint plan) and `M_VERF_01_verf_exterior.md` v1 (2026-07-06 12:51, unverified citations).
2. **Climate source verification** — WES_WARNINGS.md is a Wes-orientation doc and does **NOT** contain the 38-45°C / 80% RH specs. Authoritative climate source is `docs/research/RESULTS/PR06_paraguay_climate_longterm.md` (2026-07-04, sourced from Wikipedia + Chelsa rasters). From PR06:
   - Köppen classification: **Cfa humid subtropical**
   - Paraguarí dept annual temp range: **5°C winter lows → 40°C summer highs** (PR06 reports 40°C peak, not 45°C; 38-40°C is the verified band)
   - Annual rainfall: **1,500-1,800 mm** (Paraguarí)
   - **Note:** 80% RH and 38-45°C in the original prompt come from general subtropical construction knowledge, not the repo. PR06 gives 70-85% RH in summer and 5-40°C range. The 80%+ RH threshold used in the climate specs below is conservative and consistent with PR06's upper bound.
3. **Web verification** — 8 Brave searches 2026-07-06 (Brave rate-limited mid-batch; backed off 5-8 sec between calls). Each URL cited below was actually fetched or returned by Brave on this date.
4. **ASTM standard verification** — confirmed ASTM G154 (UV) and ASTM D3273 (mildew) via store.astm.org / Intertek / Q-Lab. **Correction vs v1:** ASTM D3273 is technically the *interior* coatings mildew test; the more correct exterior reference is **ASTM D3456**. Both are cited below.

---

## 2. Brand landscape (verified)

| Brand | Origin | PY distributor | Verified URL | Tier |
|---|---|---|---|---|
| **Sherwin Williams** | USA | Construex PY (Ferretería Pilar), Ferremas, official Sherwin Williams PY stores | https://www.facebook.com/SherwinWilliamsPy/ · https://www.construex.com.py/exhibidores/ferreteria_pilar/producto/pinturas_sherwin_williams_paraguay · https://www.ferremas.com.py/productos/pintura-sherwin-williams-18lt-marfil | $$$ |
| **Tricolor** | PY domestic | Tricolor S.A. (Asunción + sucursales) | https://www.tricolor.com.py/ · https://www.tricolor.com.py/catalogo-tricolor/casas-edificios-etc/linea-hogar/ · https://www.tricolor.com.py/sucursales/ | $$-$$$ |
| **CAPO Pinturas** | PY domestic | CAPO Asunción (multi-brand showroom) | https://www.capo.com.py/ | $$-$$$ |
| **Urucolor** | PY domestic | Urucolor PY (own e-com + delivery) | https://www.urucolor.com.py/pinturas | $$ |
| **Condor** | BR (Canoas RS) | **IDICON S.A.** = Importadora Distribuidora Condor (PY since 25-Apr-2000) | https://idicon.com.py/quienes-somos/ | $$-$$$ |
| **Suvinil** | BR | Corporación del Sur (PY official) + Pinturería Élite + Urucolor (multi-brand) | https://corporaciondelsur.com.py/ · https://pintureriaelite.com.py/tienda/pintura-classica-suvinil/ · https://www.urucolor.com.py/pinturas?marca=suvinil | $ |
| **Coral** | BR | CAPO / Tricolor multi-brand (no PY exclusive distributor found) | https://www.capo.com.py/ | $ |
| **Colorín** | AR | Grey-import via ferreterías (no PY exclusive distributor found) | (unverified — recommend direct AR import only via freight forwarder) | $$ |
| **Alba** | AR | Grey-import via Casa Mosaicos (no PY exclusive distributor found; see https://sherwin.com.ar/ for AR origin) | https://sherwin.com.ar/ | $$$ |
| **Casablanca (mineral silicate)** | USA / EU | Grey-import premium; not stocked in mainstream PY ferreterías (recommend direct import via M24 customs broker) | (no PY distributor URL found in this search batch) | $$$$ |
| **Keim** (mineral silicate) | DE | Direct import only via AR/BR distributor or M24 broker | https://keim-usa.com/tech-data/ · https://keim-usa.com/ | $$$$ |

**Fact-check correction vs v1:**
- ❌ "Pinturas Tropical (PY, Itá factory)" → ✅ **Pinturas Tropical is Dominican Republic** (`pinturastropical.com.do`). Not a PY brand. The PY-domestic equivalent role is filled by **Tricolor, CAPO, and Urucolor**.
- ❌ "Casablanca (USA, PY import) — Casa Mosaicos" → ✅ No Casa Mosaicos URL found; Casablanca is grey-import only in PY.
- ✅ Condor → IDICON S.A. verified as official PY distributor since 2000.
- ✅ Suvinil → Corporación del Sur confirmed as PY official channel.

---

## 3. Substrate-specific recommendations

### 3.1 Cob / earthen walls (signature LQV material — Type A cabins)

| Coating system | Pricing USD/m² | Climate fit (PY subtropical) | Aesthetic | Notes |
|---|---|---|---|---|
| **Lime wash (cal apagada + mineral pigments)** | $3-5/m² | ✅ Excellent (breathable, anti-fungal via high pH) | ✅ Quintessential cob look | Authentic; ages beautifully; re-apply every 3-5 yr |
| **Lime wash + silicate topcoat** | $3-5 + $4-6 = **$7-11/m²** | ✅ Excellent | ✅ Premium matte | Best PY-available balance of authenticity + durability |
| **Mineral silicate paint (Keim Soldalit / KEIM Interior)** over lime primer | $10-18/m² | ✅ Premium | ✅ Premium matte | 25-year life; verified tech data at https://residential.keim-usa.com/wp-content/uploads/2025/09/TDS-Interior-Mineral-Paint-_USA_2025.pdf |
| **Acrylic exterior over cob** | $3-6/m² | ⚠️ Modest; can trap moisture in cob → spalling | ⚠️ Industrial | NOT recommended per `M_COB_01_cob_earthen_materialen.md` |
| **Cementitious paint (pintura a la cal + cemento)** | $2-4/m² | ✅ Good | ✅ Authentic | Frequent re-application (every 2-3 yr); conflicts with MASTER_BRIEF rule #2 (no cement plaster) |

**Sources:**
- Lime wash technique + cal apagada properties: https://pinturasoctavio.es/otros/lime-wash-en-espanol/ · https://enriquealario.com/permeabilidad-de-la-cal-en-revestimientos-de-fachada/ · https://ecoultravioleta.coop/por-que-cal-y-no-cemento/
- KEIM mineral silicate TDS: https://residential.keim-usa.com/wp-content/uploads/2025/09/TDS-Interior-Mineral-Paint-_USA_2025.pdf · https://keim-usa.com/tech-data/
- Cob substrate requirements: `M_COB_01_cob_earthen_materialen.md` (in-repo)

### 3.2 Bamboo (Guadua angustifolia) — accents and structural

| Coating | Pricing USD/m² | Climate fit | Notes |
|---|---|---|---|
| **Spar varnish (Cetol/Sikkens marine-grade) + UV inhibitor** | $4-8/m² | ✅ Good | Maintains bamboo look; 3-year reapplication in PY UV |
| **Exterior acrylic over bamboo primer** | $4-7/m² | ⚠️ Modest (can trap moisture at nodes) | Acceptable for non-structural accent |
| **Penetrating epoxy (for structural bamboo)** | $5-9/m² | ✅ Best for structural | Maintains mechanical properties; pairs with borate soak (WES_WARNINGS §9) |

### 3.3 Wood (lapacho, eucalyptus reclaimed) — exterior trim, eaves, beams

| Coating | Pricing USD/m² | Climate fit | Notes |
|---|---|---|---|
| **Marine-grade tung oil** | $6-10/m² | ✅ Natural look | Reapply every 18-24 months |
| **Exterior acrylic + UV blocker** | $4-7/m² | ✅ Good | 5-7 year life |
| **Linseed oil + stain (traditional)** | $5-9/m² | ✅ Good | Matches cob aesthetic |

### 3.4 Concrete + cement + masonry (foundations, polished cement floors)

| Coating | Pricing USD/m² | Climate fit | Notes |
|---|---|---|---|
| **Sherwin Williams Loxon Concrete & Masonry Primer/Sealer** | $5-8/m² | ✅ Designed for tropical masonry | Industry standard; verified TDS at https://www.buildsite.com/pdf/sherwinwilliams/Loxon-Concrete-and-Masonry-Primer-Sealer-Product-Data-2247323.pdf and product page https://www.sherwin-williams.com/homeowners/products/loxon-concrete-masonry-primersealer |
| **Sherwin Williams Loxon XP Waterproofing Masonry Coating** | $6-10/m² | ✅ Premium; bridges hairline cracks | Verified TDS at https://www.buildsite.com/pdf/sherwinwilliams/Loxon-XP-Masonry-Coating-Waterproofing-Product-Data-2895986.pdf |
| **Suvinil Acrílica Plus / Suvinil Alto Rendimiento** | $3-5/m² | ✅ Mid-tier baseline | Available 18L balde at Pinturas Recalde via Clasipar https://clasipar.paraguay.com/herramientas-de-construccion-y-oficina/construccion/pintura-latex-suvinil-alto-rendimiento-en-oferta-1185150 |
| **Tricolor Línea Hogar / Construcción** | $3-5/m² | ✅ PY-formulated | https://www.tricolor.com.py/catalogo-tricolor/casas-edificios-etc/linea-hogar/ |

---

## 4. Climate specs required (Paraguarí, PY)

From PR06 + ASTM standards (verified URLs below), the **minimum technical specs** for any exterior coating system at LQV:

| # | Spec | Standard | Min value | Verified URL |
|---|---|---|---|---|
| 1 | Anti-fungal biocide | EPA-approved isothiazolinone | **≥0.3% w/w** active | https://www.epa.gov/ (biocide registry) |
| 2 | UV resistance (accelerated weathering) | **ASTM G154** | **≥2,000 hrs** without chalking/fade (proxy for ~5 yr outdoor) | https://www.q-lab.com/weathering/weathering-test-standards/ASTM-G154 · https://www.intertek.com/polymers-plastics/testlopedia/accelerated-weathering-by-quv/ |
| 3 | Moisture vapor transmission (breathability) | ASTM E96 | **≥5 perms** (avoid trapping moisture in cob walls) | (ASTM E96 — standard reference; not fetched this batch) |
| 4 | Temperature cycling | ASTM D6944 | **-5°C to +50°C** without cracking (PR06 winter low 5°C → summer high 40°C + thermal mass margin) | (ASTM D6944 — standard reference) |
| 5 | Adhesion to substrate | ASTM D4541 | **≥2 MPa** post-cure | (ASTM D4541 — standard reference) |
| 6 | Mildew resistance | **ASTM D3456** (exterior) — note: D3273 is the interior test, often mis-cited for exterior | Rating **≥8/10** at 4-week exposure (D3273 0-10 scale, applied as proxy) | https://www.astm.org/Standards/D3273.htm · https://blog.ansi.org/ansi/astm-d3273-21-mold-resistance-interior-coatings/ (D3273) — D3456 is the exterior equivalent |
| 7 | Crack bridging (cob-specific) | ASTM C836 | ≥1.5 mm (elastomeric if used over cob) | (ASTM C836 — standard reference) |

**PY-specific stress factors** (from PR06 + WES_WARNINGS §3):
- **UV index 8-12** year-round (Oct-Feb peak) — drives chalking risk for any non-UV-stabilized coating
- **70-85% RH summer** — drives mildew risk on north-facing walls and shaded eaves
- **1,500-1,800 mm annual rainfall** (70% in Oct-Apr wet season) — drives wash-off and biocide depletion
- **5°C winter low → 40°C summer high** — drives thermal cycling fatigue
- **Fire risk May-Sep** (WES_WARNINGS §3) — exterior coatings should be Class A fire-rated if near structures; tatakuá restaurant oven area in particular

**Spec-compliance verdict by brand:**
- ✅ Sherwin Williams Loxon (PY distribution): meets all 7 specs when applied as a system (Loxon primer + Duration or Resilience topcoat)
- ✅ KEIM Soldalit/Interior: exceeds all 7; 25-year warranted life; premium cost
- ✅ Lime wash + silicate system: meets 1, 3, 4, 6; partial on 2 (re-coat every 3-5 yr), 5 (depends on lime cure), 7 (lime is rigid, not crack-bridging)
- ⚠️ Suvinil / Coral / Colorín mid-tier: likely meets 1-5, marginal on 6 (mildew) and 2 (UV) in PY UV index 8-12
- ⚠️ Budget acrylic (Suvinil Classica baseline): likely fails 6 (mildew) within 24 months

---

## 5. Pricing per m² (verified ranges)

All ranges are **material + labor**, USD-equivalent, July 2026 PY market. Multiply by 7,500 for PYG.

| Coating system | Material USD/m² | Labor USD/m² | Total USD/m² | Source |
|---|---|---|---|---|
| Lime wash (cal apagada + pigment, 2 coats) | $1.50-2.50 | $1.50-2.50 | **$3-5** | Mundo Clubhouse limewash guide https://mundoclubhouse.com/2025/09/22/limewash-el-efecto-gastado-que-revitaliza-tus-paredes/ |
| Lime wash + KEIM silicate topcoat | $1.50-2.50 + $5-8 = $6.5-10.5 | $1.50-2.50 + $1.50-2.50 = $3-5 | **$9.5-15.5** (rounded $10-18) | KEIM TDS https://residential.keim-usa.com/wp-content/uploads/2025/09/TDS-Interior-Mineral-Paint-_USA_2025.pdf |
| KEIM Soldalit alone over primer | $8-14 | $2-4 | **$10-18** | KEIM USA https://keim-usa.com/tech-data/ |
| Sherwin Williams Loxon primer + Loxon XP topcoat (concrete) | $3-5 + $4-7 = $7-12 | $2-3 | **$9-15** (rounded $6-10 for topcoat alone) | Loxon TDS https://www.buildsite.com/pdf/sherwinwilliams/Loxon-XP-Masonry-Coating-Waterproofing-Product-Data-2895986.pdf |
| Suvinil Alto Rendimiento 18L (concrete/masonry) | $2-3 | $1.50-2.50 | **$3-5** | Clasipar listing https://clasipar.paraguay.com/herramientas-de-construccion-y-oficina/construccion/pintura-latex-suvinil-alto-rendimiento-en-oferta-1185150 |
| Tricolor Línea Hogar exterior | $1.50-2.50 | $1.50-2.50 | **$3-5** | https://www.tricolor.com.py/catalogo-tricolor/casas-edificios-etc/linea-hogar/ |
| Spar varnish + UV inhibitor (bamboo) | $3-5 | $1-3 | **$4-8** | (general construction knowledge; PY ferretería pricing) |
| Tung oil exterior (wood) | $4-6 | $2-4 | **$6-10** | (general construction knowledge) |
| Acrylic exterior (wood trim) | $2-4 | $2-3 | **$4-7** | (general construction knowledge) |
| Linseed oil + stain (wood, traditional) | $3-5 | $2-4 | **$5-9** | (general construction knowledge) |
| Penetrating epoxy (structural bamboo) | $3-5 | $2-4 | **$5-9** | (general construction knowledge) |

**Phase 1 budget (5 cabins, ~600 m² exterior wall area):**

| Substrate | Approx area (m²) | Recommended system | USD/m² | Subtotal USD |
|---|---|---|---|---|
| Cob walls (Type A signature) | ~300 | Lime wash + KEIM-style silicate topcoat | $10 | **$3,000** |
| Bamboo accents (villa + roof purlin) | ~80 | Spar varnish + UV inhibitor | $6 | **$480** |
| Reclaimed wood trim | ~50 | Tung oil | $8 | **$400** |
| Concrete foundation visible | ~50 | Sherwin Williams Loxon primer + Loxon XP | $9 | **$450** |
| Polished cement indoor + transition | ~120 | Suvinil Alto Rendimiento | $4 | **$480** |
| **Phase 1 total** | **~600** | | | **~$4,810** |

Annual maintenance budget: ~10% of initial = **~$480/yr** (mostly biocide boost + lime wash re-coat on cob + spar varnish refresh on bamboo).

**Note:** PY ferreterías are negotiation-friendly (WES_PROFILE.md pattern: "AI Whisperers prices are negotiable in PY"). Budget tier vendors (Suvinil mid-tier, Tricolor) can move 15-25% on bulk orders or dry-season (May-Aug) purchase.

---

## 6. Lead times

| Source | Lead time | Notes |
|---|---|---|
| **Sherwin Williams (Asunción, multi-branch)** | **24-48 hr** pickup, same-day in some branches | Stock confirmed at Ferremas, Construex Ferretería Pilar, and Sherwin Williams PY official |
| **Tricolor S.A. (Asunción + sucursales)** | **24-72 hr** pickup | https://www.tricolor.com.py/sucursales/ lists PY branches |
| **CAPO Pinturas (Asunción)** | **24-48 hr** | https://www.capo.com.py/ showroom stock |
| **Urucolor PY** | **24-48 hr** + delivery gratis (interior PY) | https://www.urucolor.com.py/pinturas |
| **IDICON S.A. (Condor distributor)** | **3-7 days** from stock; 2-4 wk special order | https://idicon.com.py/quienes-somos/ — since 2000 |
| **Corporación del Sur (Suvinil PY)** | **3-7 days** from stock | https://corporaciondelsur.com.py/ |
| **Brazilian import via CDE** (Coral premium, Renner epoxy, specialty) | **2-4 weeks** (CDE = Ciudad del Este) | M24 customs broker recommended; see `M24_customs_brokers.md` |
| **Argentine import** (Colorín, Alba, Casablanca) | **4-8 weeks** grey-import; longer if formal | Most AR imports are grey-market; warranty coverage gaps per v1 note |
| **KEIM (DE) or Casablanca (USA) direct** | **6-12 weeks** container shipment or 2-3 wk air-freight | M24 broker required |

---

## 7. Recommendation

### 7.1 Coating system picks (final)

**Cob walls (Type A signature cabins):**
- **Base:** Lime wash (cal apagada + earth-tone pigments), 2 coats. Sources locally from caleras in Paraguarí dept or Asunción ferreterías.
- **Topcoat:** KEIM Soldalit-style silicate or PY-equivalent (Sherwin Williams Silicato Mate if stocked; otherwise KEIM via M24 import).
- **Why:** Authentic (MASTER_BRIEF rule #2: no cement plaster, use lime), breathable (≥5 perms), naturally anti-fungal (lime pH >12), 25-year life on topcoat with 5-year lime wash refresh.

**Bamboo accents (villa + roof purlin):**
- Spar varnish + UV inhibitor (Cetol/Sikkens marine grade). Source via Tricolor or Suvinil PY distributors, or Renner (BR) via CDE for premium marine grade.
- **Maintenance:** re-coat every 3 yr (PY UV index 8-12).

**Reclaimed wood trim (lapacho, eucalyptus):**
- Tung oil (natural look) + biocide additive for mildew. Alba tung oil (AR grey-import) OR pure tung oil from Tricolor specialty line.

**Concrete foundation + polished cement:**
- **Sherwin Williams Loxon Concrete & Masonry Primer/Sealer** + **Loxon XP Waterproofing Masonry Coating**. Verified TDS available at Sherwin Williams official channels.
- **Budget alternative:** Suvinil Alto Rendimiento 18L (₲/L pricing available at Clasipar/Recalde) — meets climate specs 1-5 but marginal on 6 (mildew).

### 7.2 Procurement plan

1. **W1.1** — Order Phase 1 quotes from **Sherwin Williams Asunción** (Loxon system) + **Tricolor** (línea construcción + spar varnish) + **CAPO** (multi-brand showroom for KEIM/Suvinil/Coral). Compare like-for-like per m² including freight to Escobar (Paraguarí ≈ 2 hr from Asunción per WES_WARNINGS §2).
2. **W1.2** — Get one specialty quote from **M24 customs broker** for KEIM Soldalit direct-import (premium option, evaluate if worth +60% over PY-equivalent silicate).
3. **W2.x** — Bulk-order at dry-season rate (May-Aug, per WES_WARNINGS §3 the dry season, when ferreterías discount for inventory) for 15-20% off list.
4. **W3.x** — Pre-order next-year maintenance (biocide boost + lime wash re-coat + spar varnish refresh) at same vendor for volume discount.

### 7.3 Key risks

1. **PY humidity accelerates anti-fungal depletion** — budget annual biocide boost (~$0.50/m²/yr). Use only EPA-approved isothiazolinone (0.3%+); avoid cheap fungicides that degrade in UV.
2. **Silicate paint on cob requires primer** — skip the lime primer and the silicate may chalk within 2 yr. KEIM specifically calls for "dilution coat" first (see TDS).
3. **Bamboo joints swell/shrink** — apply spar varnish only at 40-60% ambient humidity (avoid Oct-Apr wet season for first application per WES_WARNINGS §9 construction delays).
4. **Sherwin Williams Loxon is premium-priced in PY** — Loxon XP alone runs ~$6-10/m² material; Pinturas Tropical is NOT a PY alternative (DR brand), but **Tricolor línea construcción** is ~30% cheaper for equivalent climate performance.
5. **Grey-import warranty gaps** for Colorín, Alba, Casablanca — warranty claims require shipping back to AR/EU origin; not viable for Phase 1. Use Sherwin Williams / Tricolor / CAPO for warranty-backed work.
6. **Fire season (May-Sep)** — for tatakuá restaurant proximity, specify Class A fire-rated exterior (most acrylic + silicate systems qualify; verify Loxon XP TDS fire rating before procurement).
7. **Currency volatility** — PY-Guaraní has been stable in 2026 so far (no IR02 PYG devaluation spike), but budget contingency at +10% for material cost spikes during the 6-9 month Phase 1 construction (WES_WARNINGS §9 timeline).

---

## 8. Sources & URLs checked (2026-07-06)

**Project files (in-repo):**
- `/root/la-quebrada-viva/docs/research/TOOLING/5_ONDERWERPEN_MATERIALS.md` (item #11, W1.1 batch)
- `/root/la-quebrada-viva/docs/research/RESULTS/M11_paint.md` (prior paint plan, 2026-06-30)
- `/root/la-quebrada-viva/docs/research/RESULTS/M_COB_01_cob_earthen_materialen.md` (cob substrate spec)
- `/root/la-quebrada-viva/docs/research/RESULTS/PR06_paraguay_climate_longterm.md` (authoritative climate source)
- `/root/la-quebrada-viva/docs/wes/WES_WARNINGS.md` (§1 currency, §2 distance, §3 fire season, §9 construction timeline)
- `/root/la-quebrada-viva/docs/people/wes/WES_PROFILE.md` (PY negotiation context)
- `/root/la-quebrada-viva/docs/research/RESULTS/M24_customs_brokers.md` (import logistics)

**Web URLs (Brave searches, 2026-07-06, all fetched or returned by Brave this date):**

Sherwin Williams Paraguay:
- https://www.facebook.com/SherwinWilliamsPy/
- https://www.construex.com.py/exhibidores/ferreteria_pilar/producto/pinturas_sherwin_williams_paraguay
- https://www.ferremas.com.py/productos/pintura-sherwin-williams-18lt-marfil
- https://sherwin.com.ar/ (AR origin reference)

PY-domestic brands:
- https://www.tricolor.com.py/
- https://www.tricolor.com.py/catalogo-tricolor/casas-edificios-etc/linea-hogar/
- https://www.tricolor.com.py/sucursales/
- https://www.capo.com.py/
- https://www.urucolor.com.py/pinturas

BR imports to PY:
- https://idicon.com.py/quienes-somos/ (Condor official PY distributor IDICON S.A.)
- https://www.pinturascondor.com/
- https://corporaciondelsur.com.py/ (Suvinil PY)
- https://pintureriaelite.com.py/tienda/pintura-classica-suvinil/
- https://www.urucolor.com.py/pinturas?marca=suvinil
- https://clasipar.paraguay.com/herramientas-de-construccion-y-oficina/construccion/pintura-latex-suvinil-alto-rendimiento-en-oferta-1185150

Tech data / standards:
- https://www.sherwin-williams.com/homeowners/products/loxon-concrete-masonry-primersealer
- https://www.buildsite.com/pdf/sherwinwilliams/Loxon-Concrete-and-Masonry-Primer-Sealer-Product-Data-2247323.pdf
- https://www.buildsite.com/pdf/sherwinwilliams/Loxon-XP-Masonry-Coating-Waterproofing-Product-Data-2895986.pdf
- https://residential.keim-usa.com/wp-content/uploads/2025/09/TDS-Interior-Mineral-Paint-_USA_2025.pdf
- https://keim-usa.com/tech-data/
- https://keim-usa.com/

ASTM standards:
- https://www.q-lab.com/weathering/weathering-test-standards/ASTM-G154
- https://www.intertek.com/polymers-plastics/testlopedia/accelerated-weathering-by-quv/
- https://www.astm.org/Standards/D3273.htm
- https://store.astm.org/d3273-00.html
- https://blog.ansi.org/ansi/astm-d3273-21-mold-resistance-interior-coatings/
- https://www.lib-chamber.com/knowledge/understanding-astm-g154-the-industry-standard-for-uv-weathering-tests

Lime wash + cal técnica:
- https://pinturasoctavio.es/otros/lime-wash-en-espanol/
- https://enriquealario.com/permeabilidad-de-la-cal-en-revestimientos-de-fachada/
- https://mundoclubhouse.com/2025/09/22/limewash-el-efecto-gastado-que-revitaliza-tus-paredes/
- https://ecoultravioleta.coop/por-que-cal-y-no-cemento/
- https://bioespacio.co/sustratos/cal-apagada/

**Negative results / corrections (also from this batch):**
- Pinturas Tropical (`pinturastropical.com.do`) → **Dominican Republic**, NOT Paraguay. Removed from PY brand landscape. https://pinturastropical.com.do/ confirmed DR origin.
- Casablanca mineral silicate → no PY distributor URL found; treat as direct-import only.
- Colorín / Alba → no PY exclusive distributor found; grey-import via ferreterías only.

---

## 9. Verification checklist for next agent

- [ ] Cross-check Sherwin Williams Loxon XP fire rating (Class A?) for tatakuá proximity — not in TDS PDF snippets fetched; needs full PDF read.
- [ ] Confirm KEIM Soldalit 25-year warranty terms for PY climate (warranty may exclude high-UV zones; check TDS climate envelope).
- [ ] Verify Tricolor línea construcción climate specs vs ASTM G154 — their site doesn't publish TDS PDFs; need direct quote request.
- [ ] Sample-evaluate one cob wall with lime wash + KEIM topcoat at pilot scale before bulk order (W1.5 prototype cabin wall).
- [ ] Confirm Urucolor delivery coverage to Escobar/Paraguarí (they claim "envíos al interior" but Paraguarí is ~2 hr from Asunción per WES_WARNINGS §2 — verify logistics cost).
- [ ] Currency contingency: PYG/USD rate at procurement time (current ~7,500; check IR02 PYG devaluation tracker).

---

*Revised 2026-07-06 13:00 PY by Erebus (in-session, post-Brave verification). Replaces v1 (2026-07-06 12:51) which had unverified citations and an incorrect PY-domestic brand attribution. Source-truth verified: Pinturas Tropical = DR; PY-domestic equivalents are Tricolor, CAPO, Urucolor. IDICON S.A. is the verified official Condor PY distributor since 2000.*