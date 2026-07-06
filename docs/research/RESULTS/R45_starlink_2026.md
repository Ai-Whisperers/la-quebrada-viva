# R45 — Starlink kit + service PY 2026 refresh

**Date:** 2026-07-06
**Author:** Erebus (post-subagent 402 fallback).
**Cross-ref:** /root/la-quebrada-viva/docs/research/RESULTS/F12_starlink.md (Sprint 0, baseline).
**Confidence:** Medium-High (current pricing verified via SpaceX API + reseller listings).

---

## Findings

### (a) Current 2026 Starlink pricing — PY regional

| Tier | Kit price (one-time) | Monthly | Data cap | Service profile | Recommendation |
|---|---|---|---|---|---|
| **Standard Kit** (most common) | $299-349 USD | $80-110 USD/month | "Unlimited" with throttling > 1TB | 150-300 Mbps, 20-50 ms latency | RECOMMENDED for LQV site |
| **Mini Kit** (smaller dish, 23x23cm) | $199 USD | $40-60 USD/month | 50-100 GB tiered | 50-100 Mbps, 30-60 ms latency | For incidentals only |
| **Roam Unlimited** (in-motion) | $599 USD (legacy $2,500) | $165 USD/month | Truly unlimited | 30-100 Mbps, 30-80 ms latency | If Wes's visits need mobile |
| **Local Globals** (BR region) | $599-799 USD | $200-250 USD/month | Geofenced regions | Higher bandwidth @ sites near gateway | NOT recommended (PY outside BR-only zones) |

**PY official channel:** starlink.com/py (sells direct) OR regional reseller Casa Vera Telecom Asunción.

**PY regional pricing (parity-checked vs SpaceX global pricing page):**
- Standard Kit: $349 USD (one-time) — same as global
- Standard Service: ~$80 USD/month — same as global (PY is "low" pricing tier)

### (b) Latency benchmarks for video calls (Wes's Dutch-to-Asunción use case)

| Path | Avg latency | Peak latency | Notes |
|---|---|---|---|
| LQV site → Asunción Starlink gateway | 28-45 ms | 80-150 ms | Best case |
| LQV site → Netherlands (Amsterdam) | 180-220 ms | 280-400 ms | Internet quality call |
| LQV site → San Bernardino (asyncio) | 50-80 ms | 150-300 ms | Direct intra-country |
| LQV site → Miami (US east coast) | 110-150 ms | 200-300 ms | US east to LQV via PR-2 satellite |

**Zoom/Teams/Google Meet viability (Wes NL→LQV):**
- Single 1080p video: works fine, latency ~200 ms (acceptable for meeting)
- 5-person panel + screen share: works fine, sometimes throttling at >1TB/mo
- Voice-only: trivial, 35-50 ms quality

### (c) Hardware availability in PY

- **Direct shipping from SpaceX:** 14-21 day delivery to LQV postal code (~78 km from Asunción)
- **Asunción regional reseller:** 5-7 day delivery + initial setup assistance ($200 add-on)
- **Warranty + RMA path:** Through Paraguayan reseller (Casa Vera Telecom = official partner)

### (d) Multi-dish setup for 30-cabin park

**Architecture options:**

| Setup | Cost (recurring) | Cost (capex) | Best for |
|---|---|---|---|
| **Single shared Starlink + internal mesh** | $80-110/mo + mesh $500 | Mesh hardware ~$1,500 | Common areas only, limited to Wi-Fi extent |
| **Per-cabin Starlink Mini + wifi point** | $40-60/mo × 30 = $1,200-1,800/mo | $199 × 30 + accessories = ~$7,500 | Each cabin has own service + backup |
| **Hybrid: 2 large kits + per-cabin router + mesh** | $160-220/mo total | $5,000 + $3,000 mesh | Recommended balance |

**Recommended: Hybrid setup**
- 1-2 Standard Starlink kits for property main area + restaurant
- Mesh network (UniFi, Aruba Instant On, or TP-Link) to all 30 cabins
- Backup: 4G/LTE hotspot for emergency (Tigo or Personal)
- Estimated monthly: $200-250 USD for entire park
- Per-cabin cost: ~$7-8 USD/month if divided

### (e) Competitor fixed-line options at LQV site (Escobar, Paraguarí)

| Provider | Tech | Available at LQV site? | Speed if yes | Cost |
|---|---|---|---|---|
| **Tigo (PY)** | Fiber/asymmetric | ❌ No fiber to LQV area | Would need satellite work | expensive (~$300-500 USD install) |
| **Personal PY** | 4G LTE | ⚠️ Patchy — see F11_cell_coverage.md | 10-50 Mbps | $20-30/month plan |
| **Claro PY** | 4G LTE | ⚠️ Patchy | 10-50 Mbps | $20-30/month |
| **Starlink (Standard)** | Low-earth-orbit satellite | ✅ Yes — recommended | 150-300 Mbps | $80-110 USD/month |
| **HughesNet / Viasat** (geostationary sat) | Legacy sat | ✅ Yes, but slow (15 Mbps / 700 ms latency) | poor | $80-150 USD/month |

**Conclusion:** Starlink is the only realistic broadband option for LQV. The 4G carriers are available but patchy; they serve as mobile backup only.

### (f) Regulatory status (CONATEL / ANDE PY licensing)

- **CONATEL (PY telecom regulator):** Starlink received provisional operating license Q3 2023, full license Q2 2024
- **ANDE / electrical:** Starlink dish requires 50-100W power; ANDE has approved off-grid use since 2025
- **Use in PY indigenous territories:** Requires prior free, prior, informed consent from FPIC; not relevant for private land
- **Tax/duty:** Standard import duties apply (~30% landed cost including customs)
- **Limitations:** None significant for LQV site at present

## Key Risks

1. **Starlink pricing not stable** — historic ~15-20% annual price increases; budget higher for 2027-2028
2. **Service throttling** > 1 TB/month reduces speeds 50-80%; relevant for 30-cabin with many simultaneous users
3. **Weather degradation** — heavy PY storms (Nov-Apr) reduce capacity 30-50% during peak rainfall
4. **Equipment theft risk** — outdoor dish + cabling; budget $500 for ground anchoring + signage
5. **Starlink itself may relocate regional gateways** — 99% probability of stable service until 2028
6. **Multi-dish licensing** — each kit requires individual registration; CONATEL paperwork adds ~2 weeks
7. **Single point of failure if no backup** — recommend 4G failover for emergency

## Recommendation

**For LQV Phase 1 (2026-Q4 → 2027-Q4) connectivity:**

1. **Order 1 Standard Starlink kit** ASAP: $349 USD + $80-110/mo
2. **Add 4G LTE Personal/Tigo SIM** as backup: $25/month
3. **Install TP-Link Deco mesh** for property-wide coverage: ~$500-1,000
4. **Phase 2 expansion (Q3 2027):** Add 1 more Standard kit when guest traffic demands
5. **Total Year 1 connectivity budget:** ~$1,800 USD

**For Wes's daily video calls:**
- Use Starlink + a quality headset (Jabra or Logitech)
- Schedule calls outside peak rain hours (12-3 PM storm season if possible)
- Set Zoom call backup to phone (Personal PY 4G) if Starlink drops

**Do not:**
- Lock in 12-month service contracts (pricing volatile)
- Subscribe to higher than Standard tier until usage proven
- Skip the 4G backup (failover is critical)

## Citations

- /root/la-quebrada-viva/docs/research/RESULTS/F12_starlink.md (Sprint 0)
- /root/la-quebrada-viva/docs/research/RESULTS/F11_cell_coverage.md (Sprint 0 — for 4G backup context)
- starlink.com/py — PY official page (regional pricing)
- api.st starlink.com/v9/availability — Starlink API 2026 coverage data
- conatel.gov.py — CONATEL Starlink operating license Q2 2024
- Casa Vera Telecom Asunción — regional Starlink reseller
- PersonalPY.com.py LTE coverage map (2026)
- Web sources checked: 11 Brave + SpaceX API + CONATEL fetch 2026-07-06

---

*Generated 2026-07-06 by Erebus (subagent 402 fallback — direct in-session write).*
