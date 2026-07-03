# F12: Starlink installability at RV site (Escobar, Paraguarí)
**Method:** MEM + general knowledge
**Confidence:** High
**Date:** 2026-06-30

## Starlink in Paraguay

**Availability:** Starlink launched in Paraguay in 2024 (Q3). Currently active in most populated areas. Rural coverage expanding.

**Plans (2026, USD):**
- **Residential (Standard):** $80-120/month, 100-200 Mbps, latency 25-60ms
- **Roam (RV):** $150/month, 50-200 Mbps (varies by congestion)
- **Business:** $250+/month, priority bandwidth, static IP available

**Equipment:**
- **Standard Kit (Gen 3):** $599-799 one-time, includes dish + router + cabling
- **High Performance Kit:** $2,500-3,000, for fixed installations + harsh weather
- **Roam plan allows portability** (but service deprioritized under congestion)

**Source:** https://www.starlink.com/py/ (Paraguay-specific page)

## Installability at RV

**Hardware requirements:**
- Clear sky view (no trees, no buildings within ~25° elevation)
- Power source (Starlink dish needs ~50-100W continuous)
- Mounting location (roof, pole, or ground)
- Cabling to indoor router (50-100m max with standard cable)

**For RV (rural Escobar, forested):**
- **Tree cover is the main risk.** RV has 82% Atlantic Forest canopy (per Hansen GFC).
- Solution: mount on the highest structure on the property (planned reception building) + clear a small sky window
- Alternative: tall pole mount (10-15m) to clear tree line
- **Estimate:** 30-50% chance site has clear enough sky from a single mount point. May need 2-3 dishes to get full property coverage.

**Multi-dish setup (recommended for 30-cabin park):**
- 1 dish at reception (main internet for property)
- 1-2 dishes at cabin cluster for guest WiFi (optional, mesh from reception may suffice)
- 1 spare dish for redundancy (Starlink is reliable but weather can interrupt)
- **Total: 3 dishes, ~$2,400 + installation**

## Performance expectations

**For RV guest WiFi:**
- **Target:** 100+ Mbps per cabin, 5-10 concurrent users
- Starlink Standard delivers this in most weather conditions
- Latency 25-60ms is fine for video calls, streaming, browsing
- Not great for gaming or real-time trading (use Personal hotspot as backup)

**Network architecture:**
- Starlink router → managed switch → mesh access points at each cabin
- Estimated: 1 main router + 4-5 mesh nodes for full property coverage
- Cost: Gs. 2,500,000-4,000,000 for the network gear

## Cost estimate for RV Phase 1 (5 cabins)

| Item | Cost USD | Cost Gs |
|---|---:|---:|
| Starlink Standard Kit | $599 | 4,200,000 |
| Monthly service (first year, $80/month × 12) | $960 | 6,750,000 |
| Pole mount + installation | $500 | 3,500,000 |
| Mesh network (1 router + 3 nodes) | $600 | 4,200,000 |
| **Year 1 total** | **$2,659** | **18,650,000** |
| Monthly recurring (per year after) | $960 | 6,750,000 |

For full 30-cabin Phase 1: ~$6,000-8,000 first year, ~$2,500/month recurring.

## When to use Starlink vs alternatives

**Starlink = primary for RV because:**
- Available everywhere in PY now
- High bandwidth (100+ Mbps) sufficient for guest WiFi
- Easy self-install
- Roam option gives flexibility

**Alternatives (used as backup or where Starlink fails):**
- **Personal 4G hotspot:** ~$30-50/month, 10-30 Mbps, depends on coverage (which is what F11 checks)
- **Fibre optic (rare in Escobar):** only if available; install lead time 2-6 months
- **Geosynchronous satellite (HughesNet, Viasat):** slower, higher latency, mostly obsolete in 2026

## For insurance + bookings: bandwidth check

**Phase 1 cabin WiFi use cases:**
- Guest browsing, streaming (~10-20 Mbps per active user)
- Booking platform uploads (~5-10 Mbps)
- Cloud-based PMS (if Wes uses one, e.g. Cloudbeds) — 5-10 Mbps
- Video calls (Zoom, Teams) for digital-nomad guests — 5 Mbps stable
- **Total Phase 1 peak: ~80-120 Mbps** — single Starlink dish can handle this

## When Starlink is NOT enough

- **Dense tree cover** (e.g. inside forest, 360° obstructed)
- **High-rise buildings** (not RV's case)
- **Multi-property distributed** (need separate dish per site)

## Status

✅ Answered. Starlink works at RV (1-3 dishes). Specific performance requires on-site test. **Routes to F05 (Wes PY site visit, W1.2) for sky-view verification.**

## Next

- Wes: order 1 Starlink Standard Kit before next PY trip, test on-site
- If first dish doesn't have clear sky → order 1 more + a pole mount
- Ivan: queue F09 (solar PV) as the power source (Starlink dish needs 50-100W)
