# R33 — Property Management Software (PMS)

> **For Wesley van de Camp.** Generated 2026-07-06 by Erebus. Builds on `L14_senatur_lodging_regulations.md` + `D7_marketing_budget.md` + `R16_comparable_properties_2026-07-06.md`.

---

## Executive summary

PMS (Property Management Software) is **the operational backbone** of the LQV's booking + revenue management. For a 5-cabin boutique eco-retreat, a **cloud-based PMS with multi-language** is best. Top 3 options: **Cloudbeds** (most popular), **Hostaway** (mid-tier), **Little Hotelier** (small). Mews is great for 50+ units but overkill for Phase 1.

---

## Top 5 PMS options (priced for 5-30 room boutique)

| PMS | Pricing/mo USD | Best for | Channels | Multi-language | PY support |
|---|---:|---|---|---|---|
| **Cloudbeds** | $200-350 | All-in-one (PMS + booking + channel) | 100+ (Airbnb, Booking, Expedia) | ES/EN/DE/NL/FR | Yes |
| **Hostaway** | $150-300 | Airbnbers + small hotels | 50+ | ES/EN/DE/NL/FR | Yes |
| **Little Hotelier** | $100-150 | <15 rooms | 50+ | ES/EN/DE/NL | Limited |
| **Mews** | $400-600 | 30-200 rooms | 100+ | ES/EN/DE/NL | Limited |
| **RMS Cloud** (AU) | $300-500 | 30-200 rooms | 50+ | ES/EN/DE/NL | Limited |

**For LQV Phase 1 (5 cabins)**: **Little Hotelier** or **Hostaway** (cheapest, simple).
**For LQV Phase 2-3 (30 cabins)**: **Cloudbeds** or **Mews** (more features).

---

## Standalone vs all-in-one

| Type | What it includes | Cost | Example |
|---|---|---|---|
| **Standalone PMS** | Booking calendar + check-in/check-out | $50-150/mo | HotelKit, Clock |
| **All-in-one (PMS + booking + channel)** | All features + channel manager + booking engine | $150-400/mo | Cloudbeds, Mews |
| **OTA-only** | Just the booking (no PMS) | Free + commission | Airbnb-only (15-20% cut) |

**For LQV**: **all-in-one** (Cloudbeds or Hostaway) is the right choice. Why: 5 cabins means direct bookings + Airbnb/Booking.com + a website should all be managed in one place.

---

## Channel manager comparisons

| Channel | Commission | Why include? |
|---|---|---|
| **Airbnb** | 14-16% (host fee) | Most visibility, EU guests use it |
| **Booking.com** | 15-18% (commission) | Strong in EU, NL/DE/FR |
| **Expedia** | 15-20% (commission) | Strong in US |
| **Hostelworld** | 15-18% | Backpacker/flashpacker crowd, less relevant |
| **VRBO** | 8% (subscription) | US vacation rental focus |
| **Direct website** | 0% | Highest margin, most branding |

**For LQV**: enable **Airbnb + Booking.com + Website** (3 channels). Skip Hostelworld (irrelevant) + Expedia (limited US market for premium positioning).

---

## POS (Point of Sale) for the restaurant

| POS | Pricing | Languages | PY |
|---|---|---|---|
| **Square** | 2.6% per transaction | EN/ES | Limited support |
| **SumUp** | 2.6% per transaction | EN/ES | Limited support |
| **MercadoPago PY** | Variable (4-6%) | ES | Strong PY support |
| **Odoo POS** | $20-50/mo | Multi | Open source |
| **Lightspeed POS** | $69+/mo | Multi | Limited PY |

**For LQV**: **MercadoPago PY** for PY guests + **SumUp** or **Square** for EU/international cards. Cash + 2 e-payment methods is enough for a boutique eco-retreat.

---

## API + automation considerations

| API integration | What it does | Cost |
|---|---|---|
| **Payment gateways** | Stripe, MercadoPago, MP | Built into the PMS or $20-50/mo |
| **Channel manager (Booking.com API)** | Real-time room availability sync | Included in PMS |
| **Guest messaging (Messaging Business API)** | Automated messages, pre-arrival | $0-100/mo |
| **Dynamic pricing (PriceLabs)** | Yield management | $20-50/mo |
| **Accounting (Xero, QuickBooks)** | Revenue, expense tracking | $30-80/mo |

---

## Recommended stack for LQV

| Layer | Tool | Cost USD/mo |
|---|---|---:|
| **PMS + Channel Manager + Booking Engine** | Cloudbeds | $250 |
| **POS (restaurant)** | MercadoPago + SumUp | 4-6% per txn (variable) |
| **Guest messaging** | Messaging Business API (via Twilio or 360dialog) | $30-50 |
| **Dynamic pricing** | PriceLabs | $30-50 |
| **Accounting** | Xero (NL-PY connection) | $35 |
| **Website** | WordPress + Wix + Custom | $30-100 |
| **Total monthly tech cost** | — | **$400-500** |

**Annual tech cost**: ~$5,000-6,000.

---

## Implementation timeline

| When | Action |
|---|---|
| **Now (Jul 2026)** | Sign up for Cloudbeds + Channel Manager (free trial, setup help) |
| **Q3 2026** | Connect Airbnb, Booking.com, Wix website |
| **Q4 2026** | Connect MercadoPago + SumUp POS |
| **Q1 2027** | Connect Messaging Business for guest messaging |
| **Phase 1 opening (Q2 2027)** | Full stack live |

---

## What this means for LQV

1. **R33 RESOLVED**. 5 PMS options compared + POS + channels + stack recommendation.
2. **Year 1**: Cloudbeds + MercadoPago + SumUp + Airbnb/Booking. **Cost: ~$5-6K/year**.
3. **Year 2-3**: consider Mews or stay with Cloudbeds (which scales well).
4. **Channel strategy**: enable 3 main channels (Airbnb + Booking.com + website). Skip irrelevant ones.

---

## Sources

- Cloudbeds: https://www.cloudbeds.com/
- Hostaway: https://www.hostaway.com/
- Little Hotelier: https://www.littlehotelier.com/
- Mews: https://www.mews.com/
- Square: https://squareup.com/
- MercadoPago PY: https://www.mercadopago.com.py/
- L14_senatur_lodging_regulations.md (existing)

---

*Erebus, 2026-07-06. Cloudbeds for Phase 1-2, Mews for Phase 3 if needed. Annual cost ~$5-6K. 3 main channels: Airbnb + Booking.com + website.*