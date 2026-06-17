"""Satellite / GIS data acquisition for the 62-ha La Quebrada Viva AOI.

All scripts here read the canonical AOI bbox from
``docs/site_data/aoi_62ha.geojson`` (W -57.045, S -25.645, E -57.015, N -25.615)
and write outputs under ``docs/site_data/<dataset>/``. Each module is a
standalone CLI; nothing imports anything from this package at runtime —
the ``__init__`` exists so pyright/ruff treat the dir as a package and so
``python -m scripts.satellite.<name>`` resolves.

Tiers (see ``docs/site_data/DATA_INVENTORY.md`` §11):
  T1 — high impact, low effort: PC STAC quickstart (S1+S2+WorldCover+JRC),
       GEE quickstart, NICFI Planet basemaps, Sentinel-1 SAR, multi-temporal
       NDVI/NDWI.
  T2 — medium impact: Copernicus GLO-30 (already pulled), CHIRPS rainfall,
       TerraClimate, Hansen Forest Change, HLS harmonized Landsat-Sentinel.
  T3 — drone/lidar/commercial sub-meter (deferred — needs paid licensing).
  T4 — niche: GEDI L4A AGB, MODIS LST, VIIRS, OSM, Sentinel-5P trace gas.
"""
