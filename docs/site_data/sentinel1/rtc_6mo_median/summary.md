# Sentinel-1 RTC 6-month SAR median — Phase-0 §12 #7

**Source.** Microsoft Planetary Computer STAC, collection `sentinel-1-rtc` (Copernicus Sentinel-1 GRD, Radiometrically Terrain Corrected to gamma0 by Microsoft, 10 m COG).
**License.** CC-BY-4.0 (ESA Sentinel Legal Notice ≈ CC-BY-4.0).
**AOI bbox (EPSG:4326).** W-57.0450 S-25.6450 E-57.0150 N-25.6150
**Target grid (EPSG:32721, 10 m).** W495480 S7163620 E498500 N7166960  (302×334 px)
**Window.** 2025-12-28 → 2026-06-29  (~6 months).
**Pass geometry.** descending pass, relative orbit 68, IW mode, VV+VH dual-pol — pinned so every scene shares viewing geometry.
**Scenes resolved.** 14.

## Per-scene polygon-mean backscatter (dB)

| Date | Scene | Orbit | VV (dB) | VH (dB) | VV−VH (dB) |
| --- | --- | --- | ---: | ---: | ---: |
| 2025-12-29 | `S1C_IW_GRDH_1SDV_20251229T091157_20251229T091222_005664_00B4FF_rtc` | desc/68 | -7.63 | -13.43 | +5.79 |
| 2026-01-10 | `S1C_IW_GRDH_1SDV_20260110T091156_20260110T091221_005839_00BB12_rtc` | desc/68 | -7.41 | -13.01 | +5.61 |
| 2026-01-22 | `S1C_IW_GRDH_1SDV_20260122T091156_20260122T091221_006014_00C0ED_rtc` | desc/68 | -8.54 | -14.41 | +5.87 |
| 2026-02-03 | `S1C_IW_GRDH_1SDV_20260203T091155_20260203T091220_006189_00C6CA_rtc` | desc/68 | -8.41 | -14.29 | +5.88 |
| 2026-02-15 | `S1C_IW_GRDH_1SDV_20260215T091155_20260215T091220_006364_00CCD8_rtc` | desc/68 | -8.78 | -14.31 | +5.53 |
| 2026-02-27 | `S1C_IW_GRDH_1SDV_20260227T091155_20260227T091220_006539_00D2EE_rtc` | desc/68 | -8.71 | -14.27 | +5.56 |
| 2026-03-11 | `S1C_IW_GRDH_1SDV_20260311T091155_20260311T091220_006714_00D8EE_rtc` | desc/68 | -8.38 | -14.02 | +5.64 |
| 2026-03-23 | `S1C_IW_GRDH_1SDV_20260323T091155_20260323T091220_006889_00DEEC_rtc` | desc/68 | -8.31 | -13.87 | +5.55 |
| 2026-04-04 | `S1C_IW_GRDH_1SDV_20260404T091156_20260404T091221_007064_00E4D9_rtc` | desc/68 | -8.36 | -13.98 | +5.62 |
| 2026-04-16 | `S1C_IW_GRDH_1SDV_20260416T091156_20260416T091221_007239_00EABF_rtc` | desc/68 | -7.77 | -13.52 | +5.76 |
| 2026-05-22 | `S1C_IW_GRDH_1SDV_20260522T091159_20260522T091224_007764_00FC77_rtc` | desc/68 | -9.03 | -14.78 | +5.75 |
| 2026-05-23 | `S1D_IW_GRDH_1SDV_20260523T091208_20260523T091233_002909_004F90_rtc` | desc/68 | -8.47 | -14.71 | +6.24 |
| 2026-06-04 | `S1D_IW_GRDH_1SDV_20260604T091209_20260604T091234_003084_00555E_rtc` | desc/68 | -8.55 | -14.30 | +5.76 |
| 2026-06-16 | `S1D_IW_GRDH_1SDV_20260616T091210_20260616T091235_003259_005B26_rtc` | desc/68 | -8.27 | -14.39 | +6.11 |

## Summary statistics (across per-scene polygon means)

| Quantity | Min | Max | Mean |
| --- | ---: | ---: | ---: |
| VV (dB)    | -9.03   | -7.41   | -8.33   |
| VH (dB)    | -14.78   | -13.01   | -14.09   |
| VV−VH (dB) | +5.53  | +6.24  | +5.76  |

## What the polarizations measure

- **VV** (vertical send / vertical receive). Dominant scatterers: bare soil roughness, water surface (specular = very dark), urban double-bounce (very bright). Forest VV is intermediate (~−7 to −10 dB) and fairly stable.
- **VH** (vertical send / horizontal receive). Cross-pol; sensitive to volume scattering inside a canopy. Dense forest VH is typically −12 to −16 dB; bare ground/water is <−20 dB. **VH is the cleanest single-band proxy for canopy density** at C-band.
- **VV − VH (dB)** = cross-pol ratio in dB. Smooth surfaces (water, bare soil) → large ratio (>8 dB) because VV dominates. Volume scatterers (forest) → small ratio (3–6 dB) because VH catches up. Practical water-mask is VV<−15 dB AND ratio>10 dB.

## RTC = gamma0, not sigma0

Microsoft Planetary Computer's `sentinel-1-rtc` collection is **Radiometrically Terrain Corrected** to gamma0. The terrain correction divides backscatter by the local illuminated area derived from a Copernicus DEM, removing topographic distortion of brightness — so a forested slope and a forested flat give comparable values. Values stored are **gamma0 linear power**; this driver converts to dB (`10·log10(γ⁰)`) before any per-pixel comparison.

## Cross-references

- Phase-0 §12 #6 (Sentinel-2 L2A timeseries, `docs/site_data/sentinel2/timeseries_2020_2025/`) is on the **same** 302×334 EPSG:32721 10 m grid. Per-pixel S2 NDVI median (optical canopy density) and S1 VH median (radar volume scatter) can be differenced/regressed without resampling. Expect them to correlate positively across the 62 ha.
- Phase-0 §12 #10 (Hansen GFC, `docs/site_data/hansen_gfc/`) gives continuous treecover2000 / loss-year on a 30 m grid — VH median should track treecover2000 within the same parcel.
- Phase-0 §12 #12 (JRC GSW, `docs/site_data/jrc_gsw/`) gives surface-water occurrence; SAR water-mask (VV<−15 dB AND ratio>10 dB) is the high-res LQV-only counterpart. No persistent open water expected inside the 62 ha bbox — see Batch I AWEIsh result.

## Files

```
docs/site_data/sentinel1/rtc_6mo_median/
├── <SCENE_ID>/                     × N scenes
│   ├── vv.tif        (10 m, gamma0 linear power, float32)
│   ├── vh.tif
│   └── *.tif.meta.json (per-file STAC/license sidecar)
├── sar_quicklook.png    ← 3-panel VV_dB + VH_dB + RGB false-color
├── polygon_indices.csv  ← per-scene polygon means (dB)
└── summary.md           ← this file
```

## Caveats

- The window is the most recent ~6 months ending 2026-06-29; regenerate against a different window by editing `START`/`END` in the driver. Pinning to descending / relative orbit 68 forces consistent viewing geometry but caps the scene count at the ~12-day revisit cadence (≈ 15 scenes / 6 months).
- Speckle is **not** filtered here. Per-scene values include salt-and-pepper noise inherent to single-look SAR; the 6-scene `np.nanmedian` stack is the speckle suppressor. Don't read single-pixel values from the per-scene `.tif`s.
- Microsoft's RTC uses the Copernicus DEM (30 m globally; 10 m where available, which does **not** include Paraguay). Steep slope artifacts may persist near the escarpment in the SE — visual-cross-check against the Cop30 hillshade in §12 #5.
- Per-scene `.tif` files are kept on disk for re-runs but are **git-ignored** (see `.gitignore`: `docs/site_data/sentinel1/**/*.tif`). The PNG / CSV / MD outputs and the per-file `.meta.json` sidecars are tracked.
- MPC's SAS tokens expire after ~50 minutes. This driver fetches a fresh token at startup; if a run lasts longer than that across many scenes, `clip_band` may 403 mid-run — restart and the cached scenes will be skipped via `skip_if_exists`.
