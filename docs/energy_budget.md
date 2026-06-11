# Energy Budget — La Quebrada Viva House

**Status:** living document. Sizes the PV array, LiFePO4 battery bank, micro-hydro turbine, and LPG cylinder usage so that the off-grid system meets a two-person + occasional-guest household plus a small smart-home stack.

This is the engineering basis for §6 of `docs/bom.md`.

## Design conditions

- **Latitude:** −25.4° (Paraguarí, S of the Tropic of Capricorn).
- **Site elevation:** 240–312 m a.s.l. across the property; building pad ~285 m.
- **Climate zone:** Cfa (humid subtropical, no dry season, hot summers).
- **Solar resource:** GHI 5.0 kWh/m²/day annual mean (NREL + local met data).
  - June minimum ~3.5 kWh/m²/day.
  - December peak ~6.4 kWh/m²/day.
- **Stream flow:** estimated 2–8 L/s seasonal at the upper weir (verify with bucket-and-stopwatch).
- **Hydro head:** ~12 m measured drop spring → turbine site (verify after `site_data_spike` survey).
- **Demand:** 2 residents + occasional 2 guests, cooking on tatakuá (wood) for entertaining, LPG for everyday hob.

## Daily electrical load (typical day)

| Load | Power (W) | Hours/day | Wh/day |
|---|---:|---:|---:|
| 12 V chest fridge (50 L) | 45 | 8 | 360 |
| LED lighting (12 × 6 W warm) | 72 | 4 | 288 |
| Outdoor LED sconces (4 × 4 W) | 16 | 4 | 64 |
| Ceiling fans (2 × 50 W) | 100 | 6 | 600 |
| Water pressurisation pump (40 W) | 40 | 0.5 | 20 |
| Laptop (1 × 60 W) | 60 | 5 | 300 |
| Phone + tablet charging | 20 | 4 | 80 |
| Wi-Fi router + LTE backup | 12 | 24 | 288 |
| Smart-home hub (Zigbee + Z-Wave) | 8 | 24 | 192 |
| TV (40" LED, 50 W) | 50 | 2 | 100 |
| Kitchen appliances (blender, etc.) | 600 | 0.3 | 180 |
| Composting-toilet fan | 5 | 24 | 120 |
| Rainshower pump (assist only) | 70 | 0.3 | 21 |
| **Subtotal — typical** | | | **2613** |
| Margin (15%) | | | 392 |
| **Design load** | | | **~3000 Wh/day** |

## Peak-day load (entertaining + summer)

| Add-ons | Power (W) | Hours/day | Wh/day |
|---|---:|---:|---:|
| Mini-split AC (one room, 750 W effective) | 750 | 3 | 2250 |
| Ice maker (occasional) | 120 | 2 | 240 |
| Extra fans for guests | 100 | 4 | 400 |
| **Peak-day load** | | | **~5900 Wh/day** |

## PV array sizing

- **Worst-month GHI:** 3.5 kWh/m²/day (June).
- **Derate:** 0.70 (panel orientation, dust, temperature, inverter, line loss).
- **Effective sun-hours equivalent:** 3.5 × 0.70 = 2.45 hrs.
- **PV size needed for 3 kWh/day at worst month:** 3000 / 2.45 = **1224 Wp minimum**.
- **PV size for 5.9 kWh/day at worst month:** 2408 Wp.
- **Chosen size:** **5 kWp** (8 × 625 Wp bifacial panels on a steel ground-mount frame, Rule 9).
  - Headroom for future EV charging or pool pump.
  - Average annual generation: 5 × 5.0 × 0.7 = **17.5 kWh/day** — well above demand.

## Battery sizing

- **Autonomy target:** 2 cloudy days at typical load (3 kWh/day) = 6 kWh.
- **Add 25% safety margin and 80% LiFePO4 depth-of-discharge:** 6 × 1.25 / 0.8 = 9.4 kWh.
- **Round up to off-the-shelf modules:** **10 kWh × 2 = 20 kWh** LiFePO4 bank (48 V).
  - Two modules in parallel for redundancy and easier replacement.

## Micro-hydro contribution

- **Q × head × g × η = power.**
- 4 L/s × 12 m × 9.81 × 0.55 = **259 W continuous** in wet season.
- Run continuously: 259 × 24 = **6.2 kWh/day** — nearly the entire typical load.
- Dry-season Q drops to ~1.5 L/s → power ~97 W → 2.3 kWh/day.
- **Hybrid mode:** hydro covers baseload day and night; PV tops up + charges battery for peaks.

## LPG sizing

- **Cooking hob (everyday):** 2 burners × 1.5 kW × 1 h/day = 3 kWh/day thermal.
- **LPG energy density:** 14 kWh/kg.
- **Daily consumption:** 0.21 kg/day = 6.4 kg/month.
- **Cylinder choice:** 2 × 45 kg cylinders (twin manifold + auto-changeover) → 7 months between deliveries. Wesley orders refills twice a year.

## Hot water

- **Mode 1:** PV-heated header tank with electric immersion (1 kW × 1 h/day in winter = 1 kWh).
- **Mode 2:** flat-plate solar thermal collector, 1.5 m², direct serpentine to header tank.
- **Recommended:** Mode 2 primary, electric immersion as winter backup.
- Energy budget already includes Mode 1 winter backup (folded into PV sizing).

## Cooling strategy

- **Primary:** passive — corredor shading, cross-ventilation through bedroom+kitchen E windows, thermal mass cob, sod roof.
- **Secondary:** ceiling fans (in the load list).
- **Tertiary:** one inverter mini-split in the bedroom for the 5–10 hottest nights/year.
  - Sized 9000 BTU, 0.75 kW running.
  - Expected use: ~30 night-hours/year = 22 kWh/year. Trivial.

## Heating strategy

- **Cob thermal mass** maintains 18–22 °C through winter days.
- **Tatakuá adjacent radiance** warms the corredor side on cool nights.
- **Backup:** small wood-burning rocket stove in the sala for the coldest 10 nights/year.
- No electric heating.

## Smart-home power budget

- Zigbee hub + 12 sensors + 4 smart switches = ~8 W continuous = **192 Wh/day**.
- Wi-Fi router + LTE backup = ~12 W continuous = 288 Wh/day.
- Smart-home is in the load list above. No separate budget needed.

## Outage resilience (Rule 7)

- **Primary outage source:** grid does not apply (off-grid). The risks are:
  - PV array damage (storm) → battery + hydro keep the house running 4–5 days.
  - Battery failure → PV-direct loads only; daytime-only mode.
  - Hydro stoppage (intake clog, dry season) → PV + battery sized to handle this.
  - Spring failure → 5 000 L rainwater tank gives ~10 days at 50 L / person / day.

## Smart-home automations directly relevant to energy

1. **Sun-tracking ramp on lights:** sunrise +30 min off, dusk on.
2. **Battery-aware load shedding:** AC only allowed if battery SoC > 60%.
3. **Hydro alarm:** flow drop > 30% → push notification.
4. **PV-direct boost:** heater, ice maker, large appliances scheduled for midday solar peak.
5. **Mosquito alert:** if any cistern overflow valve sticks → push notification (cross-check Rule 10).

## Cross-references

- `docs/bom.md` §6 — quantities for the equipment described here.
- `docs/build_sequence.md` Phase 7 — installation order.
- `docs/MASTER_BRIEF.md` Rule 6 (passive ≤ 35 °C), Rule 7 (outage-proof), Rule 9 (PV on steel frame), Rule 10 (mosquito mesh).
- `lqv/site/site_plan.py` — PV array site relative to building pad.
