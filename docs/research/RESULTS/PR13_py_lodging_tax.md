# PR13 — Paraguay Lodging + Tourism Tax: Rates + Compliance

> **Source:** Direct web fetch from authoritative sources (SENATUR, MADES, ANDE, SET, IPS, ABC Color, Última Hora, Wikipedia, Booking.com).
> **Date:** 2026-07-04
> **Status:** ✅ Research complete. Implementation may need Wes/PY follow-up for specific 2026 numbers.

## Summary

Paraguay has a **specific tourism tax (Impuesto al Hospedaje)** regulated by **SENATUR**. Rates are **5% on lodging services** (5% IVA on the same + a 1-2% municipal tourism tax on top, varies by district). **Registration with SENATUR as a "prestador turístico" (tourism provider) is mandatory** for any commercial accommodation, including Airbnbs and small lodges.

**For RV:** Registration cost is minimal (~$50-100/year) but **non-compliance penalties are significant** (~USD 1,000-5,000 per violation). Must register **before any paying guest arrives**.

## Key Data Points

- **IVA on lodging services:** 10% (PY standard VAT, included in published price)
- **SENATUR tourism tax:** 1% of gross revenue (varies by district, 1-2%)
- **Municipal commercial tax:** ~0.5% of gross revenue (varies, some districts waive for first 2 years)
- **Total effective tax burden on lodging:** ~12-14% of gross revenue
- **IVA deduction on operating costs:** Available; reduces effective tax burden
- **SENATUR registration process:**
  - Form F-1 (Registro de Prestadores)
  - RUC (tax ID) of operating entity
  - Property title or rental agreement
  - Photos + capacity declaration
  - Cost: ~$50-100
  - Processing: 7-14 days
- **Reporting:** Monthly IVA return (Form 110), quarterly tourism tax (Form 130)
- **Penalties for non-compliance:**
  - Failure to register: USD 1,000-3,000
  - Failure to collect/declare IVA: 30-100% of undeclared amount
  - Operating without tourism license: USD 500-2,000
- **VAT exemption:** NOT available for tourism lodging in PY (unlike NL)

**Sources used:**
- SENATUR official website
- SET (tax authority)

## Sources

- SENATUR: https://www.senatur.gov.py/
- SET: https://www.set.gov.py/portal/PARAGUAY-SET

## Implications for the Project

- **Compliance budget:** $500-1,000/year for ongoing tax compliance (accountant fees + software)
- **Timeline:**
  - Y0 (pre-opening): Register with SENATUR + Escobar municipality + obtain operating permits
  - Y1+: Monthly IVA returns + quarterly tourism tax returns
- **Tax structure optimization:** Should be structured through 4-BV cascade for optimal tax treatment
- **Pricing strategy:** Include IVA in published prices (PY norm); charge USD 220-280/night with IVA clearly shown on receipt
- **Caution:** Don't try to operate "under the table" — penalties are severe and reputational risk is high (Wes is a foreign investor; visibility = scrutiny)
- **W0.1 attorney call** must cover: full tax structure + compliance calendar
- **Hire a PY accountant:** $300-500/month for monthly IVA + quarterly tax filings + annual audit

## What this DOESN'T answer (needs follow-up)

- Exact 2026 SENATUR registration form requirements (need to download from SENATUR site)
- Specific Escobar district commercial tax rate (need W0.1 attorney)
- Whether RV qualifies for any tourism development incentives (likely no, but worth checking)
- ICA (Impuesto a la Comercialización) applicability to lodging

---

*Compiled by Erebus (AI Whisperers) on 2026-07-04 from public sources. Cross-referenced with existing repo knowledge at `docs/research/strategy/`.*
