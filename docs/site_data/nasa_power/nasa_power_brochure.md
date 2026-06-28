# NASA POWER daily climatology — La Quebrada Viva parcel

Source: NASA POWER (https://power.larc.nasa.gov), US public domain  
Point: lon=-57.03000, lat=-25.63000 (nearest grid cell ~½°)  
Window: 19900101–20251231  
Pulled: 2026-06-18T18:12:42Z

## Long-term means (engineering-deck headline)

| Variable | Mean | Min | Max | N days |
| --- | ---:| ---:| ---:| ---:|
| ALLSKY_SFC_SW_DWN | 4.899 | 0.19 | 9.331 | 13149 |
| ALLSKY_KT | 0.539 | 0.03 | 0.79 | 9130 |
| T2M | 22.625 | 4.16 | 36.24 | 13149 |
| T2M_MAX | 28.556 | 7.91 | 43.57 | 13149 |
| T2M_MIN | 17.45 | -1.76 | 29.81 | 13149 |
| RH2M | 73.472 | 21.11 | 98.6 | 13149 |
| WS2M | 0.379 | 0.12 | 1.02 | 13149 |
| WS10M | 1.501 | 0.51 | 4.36 | 13149 |
| WS50M | 3.346 | 0.93 | 9.84 | 13149 |
| PRECTOTCORR | 4.12 | 0.0 | 184.23 | 13149 |

## Monthly mean solar (ALLSKY_SFC_SW_DWN, kWh/m²/day) — PV sizing

| Month | kWh/m²/day |
| --- | ---:|
| Jan | 6.76 |
| Feb | 6.164 |
| Mar | 5.369 |
| Apr | 4.354 |
| May | 3.373 |
| Jun | 2.809 |
| Jul | 3.204 |
| Aug | 3.825 |
| Sep | 4.525 |
| Oct | 5.352 |
| Nov | 6.393 |
| Dec | 6.728 |

## Interpretation hooks

- Worst-month solar: Jun at 2.809 kWh/m²/day → size PV array against this.
- Best-month solar:  Jan at 6.76 kWh/m²/day.
- T2M_MAX mean above 32 °C → passive cooling design (Rule 6) is non-optional.
- WS50M mean below 4 m/s → small wind is unlikely to beat PV economically.
- Cross-check PRECTOTCORR against CHIRPS (5 km) before tank sizing.

Raw daily series: `nasa_power_daily.csv` (one row per day).