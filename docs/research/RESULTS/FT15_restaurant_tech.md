# FT15 — Restaurant tech stack: POS, reservations, online ordering (W1.1 item)

**Method:** MEM + training data
**Confidence:** Medium
**Date:** 2026-06-30

## What RV needs (Fase 1 restaurant)

**5 systems:**
1. **POS (point of sale)** — order taking, payment processing
2. **Reservations** — booking management
3. **Online ordering** — if RV does delivery (probably not for Fase 1)
4. **Inventory** — track food + beverage
5. **Staff scheduling** — for 7 restaurant staff

## Comparison options

| System | POS | Reservations | Inventory | Pricing | Notes |
|---|---|---|---|---|---|
| **Square (US, available in PY)** | ✅ | partial | basic | Free + $60-150/mo for advanced | Simple, good for small restaurants |
| **Toast (US, US-focused)** | ✅ | ❌ | basic | $165-200/mo | Not in PY |
| **Lightspeed (US, CA-focused)** | ✅ | partial | good | $69-200/mo | Good for hotels + restaurants |
| **Cloudbeds (US, strong in LATAM)** | partial | ✅ | basic | $20-30/mo | **Best for the RV hotel + restaurant** |
| **Mews (CZ, newer, growing)** | ❌ | ✅ | ❌ | $50-100/mo | Property management focus |
| **Cloudbeds + Lightspeed combo** | ✅ | ✅ | good | ~$200-300/mo | **Recommended for RV** |
| **Lodgify** (Spain) | partial | ✅ | basic | $20-30/mo | Vacation rental focus |
| **Loca01 / ProSoftware** (PY local) | ✅ | ❌ | basic | $30-50/mo | PY-local, but limited features |

## Recommended stack for RV

**Primary: Cloudbeds + Lightspeed combo**

**Cloudbeds (for the hotel/booking system):**
- Strong in LATAM
- Built for vacation rentals
- Channel manager (Booking.com, Airbnb)
- Revenue management
- $20-30/month starter plan
- Scales to full Phase 1

**Lightspeed (for the restaurant POS):**
- Strong inventory
- Integrates with Cloudbeds
- Restaurant-focused
- $69-200/month

**Total monthly cost: ~$100-230/month for the combined system**

## Alternative: Cloudbeds only

If RV wants simplicity (1 system for hotel + restaurant), Cloudbeds does have basic POS. For Fase 1 with limited restaurant volume (25-40 covers/day), Cloudbeds' POS is sufficient.

**Total monthly cost: $20-30/month**

## Recommendation: Cloudbeds + Lightspeed

For RV (Fase 1 expanding into Fase 2/3):
- **Cloudbeds** for the hotel/booking system (RV's 30 cabins)
- **Lightspeed** for the restaurant POS (when restaurant volume justifies)

**Add later:**
- **Square** for the wellness center + gift shop
- **Messaging Business API** for guest communication
- **Google Workspace** for team email + documents

## What Wes needs to do

- [ ] Set up Cloudbeds account (1 day)
- [ ] Set up Lightspeed when restaurant is ready (1 week)
- [ ] Connect to Booking.com channel manager
- [ ] Set up staff training on both systems
- [ ] Budget $200-300/month initially

## Sources
- Cloudbeds: https://www.cloudbeds.com/
- Lightspeed: https://www.lightspeedhq.com/
- Square: https://squareup.com/

## Cross-reference
- M01 (Booking.com setup) — covered by Cloudbeds channel manager
- D14 (brand) — restaurant tech is part of the brand experience
- W0.2 Sonja call — chef opinion on restaurant tech
- Restaurant operations (Fase 1 ops) — informed by these

## Status

✅ Done. Recommend Cloudbeds + Lightspeed for RV. ~$200-300/month initially.
