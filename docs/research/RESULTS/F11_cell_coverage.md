# F11: Cell coverage Tigo/Personal/Claro at LQV site (Escobar, Paraguarí)
**Method:** SEARCH (Brave) + MEM
**Confidence:** High for general operator coverage, low for specific site
**Date:** 2026-06-30

## Operator landscape in Paraguay

| Operator | Network type | Coverage profile | Market share |
|---|---|---|---|
| **Tigo** (Millicom) | 4G LTE + 3G + 2G | Strongest rural coverage in PY, especially interior | ~45% |
| **Personal** (Telecom Argentina) | 4G LTE + 3G | Strong in urban + main roads | ~30% |
| **Claro** (América Móvil) | 4G LTE + 3G | Strong in urban, decent rural | ~20% |
| **Vox** (newer) | 4G | Limited, mostly urban | <5% |

**Source:** Tigo Paraguay market position via https://www.tigo.com.py/

## Coverage map tools

| Tool | URL | Use |
|---|---|---|
| **Tigo official coverage map** | https://www.tigo.com.py/movil/cobertura | Tigo-specific, by district |
| **Claro coverage** | https://www.claro.com.py/ | Usually by city, not address-level |
| **Personal coverage** | https://www.personal.com.py/ | Same as Claro |
| **nPerf community map** | https://www.nperf.com/en/map/PY/-/-/signal | User-contributed, shows actual speeds |
| **OpenSignal** | https://www.opensignal.com/ | Same idea, real-user data |

## Escobar, Paraguarí — known coverage profile

**General reality (training data):**
- **Tigo:** Has coverage in Escobar district (town center) — 3G at minimum, 4G likely in parts
- **Personal:** Decent coverage in town, weak in rural interior
- **Claro:** Strong in Paraguarí city, weak as you go south into Escobar
- **Likely coverage gap:** If LQV is >5 km from Escobar town center, expect 3G/edge with frequent drops
- **Best option for rural site:** Multi-SIM router (Tigo + Personal) with auto-failover

**For LQV's specific location (Escobar, exact property):**
- **Wes needs to verify on-site** — physical signal test with 3 SIMs is the only reliable answer
- This is item F05 / W1.2 (PY site visit)

## Backup plan: external antenna

If signal is weak, options:
- **Yagi external antenna** (Tigo has strongest rural freq) — Gs. 350,000-800,000 installed
- **Cellular booster/repeater** — Gs. 1,500,000-3,500,000 (covers 500-1000 m²)
- **Starlink** (see F12) — better option for low-signal sites

**Recommended: combine** — Tigo primary + Personal secondary, with external Yagi if needed.

## What Wes should do next PY visit

**Bring 3 SIMs (Tigo, Personal, Claro) + a cellular signal-testing phone app** (e.g. NetMonster for Android, or Field Test Mode on iPhone).

Document signal strength at:
- [ ] Property entrance
- [ ] Proposed cabin cluster 1 (5 cabins)
- [ ] Proposed restaurant location
- [ ] Proposed reception location
- [ ] Driveway entrance (call quality matters here for guest check-in)

**Time required:** 1 hour at the property.

## Sources to verify

- Tigo official map: https://www.tigo.com.py/movil/cobertura
- nPerf: https://www.nperf.com/en/map/PY/-/-/signal
- OpenSignal PY: https://www.opensignal.com/

## Status

⚠️ Partial. Operator landscape clear, specific site coverage = needs physical test. **Item F11 routes to F05 (Wes PY site visit, W1.2).**

## Next

- Wes: bring 3 SIMs + signal test app to next PY visit
- Ivan: queue M22 (customs) + F12 (Starlink) as the backup plan if signal is poor
