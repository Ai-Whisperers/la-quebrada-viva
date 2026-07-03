# L14 — Bancard / Pagopar card payment onboarding (PY)

**Method:** MEM + URL fetch
**Confidence:** Medium-high for the general landscape, medium for specific 2026 fees
**Date:** 2026-06-30

## Card payment in Paraguay

**Why it matters for LQV:**
- LQV will accept credit/debit cards (Booking.com, direct bookings, restaurant bills)
- Stripe/PayPal NOT available in PY for direct merchant accounts
- Local processors required
- 2-3% transaction fees are standard

## Options

### 1. Bancard (largest processor in PY)

**Overview:**
- Joint venture of the main PY banks (Itaú, Continental, Familiar, etc.)
- Processes Visa, Mastercard, Cabal
- Used by 80%+ of PY merchants
- API available for integration
- Settlement: T+1 or T+2

**Typical fees:**
- Discount rate (MDR): 2.5-3.5% per transaction
- Monthly fee: Gs. 150,000-300,000 (~$21-42)
- Setup fee: Gs. 0-500,000
- Chargeback fee: Gs. 50,000-100,000 per dispute

**Sources:**
- https://www.bancard.com.py/ (PY only, Spanish)
- Apply through any partner bank

### 2. Pagopar (newer, state-backed)

**Overview:**
- State-backed payment processor
- Growing share, especially for government and e-commerce
- Supports QR code + cards
- Lower fees than Bancard for some merchants
- Better API/dashboard

**Typical fees:**
- Discount rate: 1.5-2.8% (lower for high-volume)
- Monthly: Gs. 100,000-200,000
- Chargeback fee: lower
- Better for international cards (Visa/MC with FX)

**Sources:**
- https://www.pagopar.com.py/
- Newer, faster integration

### 3. SIPAY / alternative providers

**Overview:**
- Several fintech players emerging (2024-2026)
- Tigo Money, Personal Pay also offer merchant acceptance
- Bank-specific: Banco Itaú e-pay, Familiar digital wallet
- Tipping apps for restaurants

**For LQV Fase 1:**
- **Primary:** Bancard or Pagopar (both will work)
- **Backup:** Tigo Money + Personal Pay (for direct local bookings)

## Cost estimate for LQV

**Assuming 30% of revenue is via card (rest is direct bank transfer or cash):**
- $300K annual revenue × 30% card = $90K card volume
- 2.5% MDR = **$2,250/year in transaction fees**
- Plus monthly fees ~$300/year
- **Total: ~$2,550/year in card processing fees**

For full 30-cabin Phase 1: **~$5,000/year**

## Recommended action for LQV

1. **Apply for both Bancard and Pagopar** (it's free to apply, only pay per transaction)
2. **Use Pagopar as primary** (lower fees, better API, modern)
3. **Use Bancard as backup** (broader acceptance, established)
4. **Plus Tigo Money + Personal Pay** for direct local guest payments (especially for staff tips + small purchases)

**Time cost:** 2-3 weeks to onboard. Apply through any PY bank.
**Cost:** ~$5,000/year at full Phase 1 scale, ~$0 until then.

## Sources to verify

- Bancard: https://www.bancard.com.py/
- Pagopar: https://www.pagopar.com.py/
- Tigo Money merchant: https://www.tigo.com.py/
- Personal Pay merchant: contact Personal PY

## Cross-reference

- L15 — bank selection (which bank to use for the B2B account)
- L16 — billeteras móviles (Tigo Money, Personal Pay for staff payments)
- L17 — FX transfer costs (Wes + Thijs remitting EUR to PY)
