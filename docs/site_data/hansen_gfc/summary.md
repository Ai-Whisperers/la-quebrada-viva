# Hansen Global Forest Change v1.12 (2000–2024) — Phase-0 §12.10

Centroid `-57.0355, -25.6073` — buffer 50.0 km
AOI bbox: W-57.5350 S-26.0578 E-56.5360 N-25.1568
Source tile: `20S_060W` from `https://storage.googleapis.com/earthenginepartners-hansen/GFC-2024-v1.12`

## Layers pulled

| Layer | AOI valid cells | AOI nonzero % | Polygon valid cells | Polygon nonzero % | Polygon mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| treecover2000 | 14401584 | 54.80 | 446 | 92.38 | 82.11 |
| lossyear | 14401584 | 4.94 | 446 | 1.57 | 0.08 |
| gain | 14401584 | 0.09 | 446 | 0.00 | 0.00 |
| datamask | 14401584 | 100.00 | 446 | 100.00 | 1.00 |
| loss (derived from lossyear>0) | 14401584 | 4.94 | 446 | 1.57 | 0.02 |

## Interpretation for La Quebrada Viva polygon

- **Canopy cover at 2000:** mean **82.1%**, max 100%, 412 of 446 cells with any canopy at 2000.
- **Stand-replacement loss 2001–2024:** 7 pixels (~0.63 ha at 30 m) flagged as loss.
- **Forest gain 2000–2012:** 0 pixels flagged as gain.
- **Datamask:** mean 1.00 (1=land, 2=water; polygon is all land per Hansen).

## Loss-year histogram (polygon)

| Year | Loss pixels in polygon | Loss pixels in AOI |
| ---: | ---: | ---: |
| no loss | 439 | 13690595 |
| 2001 | 1 | 11070 |
| 2002 | 0 | 14868 |
| 2003 | 4 | 22685 |
| 2004 | 0 | 25988 |
| 2005 | 0 | 23749 |
| 2006 | 0 | 21747 |
| 2007 | 1 | 20725 |
| 2008 | 0 | 25929 |
| 2009 | 0 | 17302 |
| 2010 | 0 | 15069 |
| 2011 | 0 | 24953 |
| 2012 | 0 | 36134 |
| 2013 | 0 | 20174 |
| 2014 | 1 | 28969 |
| 2015 | 0 | 20627 |
| 2016 | 0 | 38506 |
| 2017 | 0 | 58618 |
| 2018 | 0 | 27233 |
| 2019 | 0 | 23118 |
| 2020 | 0 | 44850 |
| 2021 | 0 | 46228 |
| 2022 | 0 | 47674 |
| 2023 | 0 | 46730 |
| 2024 | 0 | 48043 |

## Files

```
docs/site_data/hansen_gfc/
├── treecover2000_aoi_50km.tif  treecover2000_polygon.tif  treecover2000.png
├── loss_aoi_50km.tif           loss_polygon.tif           loss.png
├── lossyear_aoi_50km.tif       lossyear_polygon.tif       lossyear.png
├── gain_aoi_50km.tif           gain_polygon.tif           gain.png
├── datamask_aoi_50km.tif       datamask_polygon.tif       datamask.png
└── summary.md
```

## Caveats

- Hansen v1.12 covers stand-replacement loss only — sub-canopy thinning
  and selective logging are invisible. For degradation use NICFI + Mapbiomas.
- The `gain` band is a 2000–2012 product and has NOT been updated in
  later versions; treat it as historical, not contemporary.
- 1 arcsecond ≈ 30 m at the equator; at lat -25.6 the pixel is
  ~30 m N–S × ~27 m E–W (cos correction). For ha conversions we use
  the nominal 30 m × 30 m → 0.0900 ha per pixel.
- The `treecover2000` % threshold for "forest" is user-defined; UNFCCC
  Paraguay typically uses ≥10% but the BAAPA ecoregion default is ≥30%.
- For 1985–2000 history use Mapbiomas Paraguay (next §12 item).
