"""Site-data ingest tools for the 62-ha La Quebrada Viva parcel.

This package sits OUTSIDE `lqv/` on purpose — these are auxiliary ingest
scripts that pull free public satellite / climate / soil APIs and write
outputs under `docs/site_data/<dataset>/`. They never import from `lqv`
and never touch the render pipeline. Run them from the repo root.

Modules:
  - common         Shared bbox + paths + tiny HTTP retry.
  - soilgrids      ISRIC SoilGrids 250 m REST (foundation / drainage inputs).
  - nasa_power     NASA POWER daily climatology (solar / wind / thermal).
  - chirps         UCSB CHIRPS v2.0 monthly rainfall at 5 km.
  - sentinel1      ASF DAAC Sentinel-1 SAR search + HyP3 InSAR helpers.

Usage from repo root:
  python3 -m tools.site_data.soilgrids
  python3 -m tools.site_data.nasa_power
  python3 -m tools.site_data.chirps
  python3 -m tools.site_data.sentinel1 --search
"""
