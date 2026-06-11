"""ERA5 reanalysis climate baseline for the LQV site.

Free via CDS. Pulls 1990-2025 monthly mean temperature, total precipitation,
10m wind, and surface solar radiation for the 3.3 km x 3.3 km search bbox.

CDS is request-based: submits the request, returns a job ID, polls until ready.
First request is fast (small file). Full 35-year pulls are larger.

Outputs:
  - docs/site_data/climate_era5/era5_2m_tavg_1990_2025.nc
  - docs/site_data/climate_era5/era5_total_precip_1990_2025.nc
  - docs/site_data/climate_era5/era5_10m_wind_1990_2025.nc
  - docs/site_data/climate_era5/era5_solar_rad_1990_2025.nc
  - docs/site_data/climate_era5/climate_summary.txt
  - docs/site_data/climate_era5/climate_brochure.md
"""
import sys
from pathlib import Path

import cdsapi

HERE = Path('/home/ai-whisperers/blender-projects/house-field')
OUT_DIR = HERE / 'docs' / 'site_data' / 'climate_era5'
OUT_DIR.mkdir(parents=True, exist_ok=True)

# CDS sub-region must be at least 1 ERA5 grid cell (0.25 deg) and 1 ERA5-Land cell (0.1 deg).
# Our 3.3 km x 3.3 km property bbox is smaller than either grid. Expanding to 1.0 deg x 1.0 deg
# (approx 110 km x 110 km) captures the property plus many grid points for spatial context.
AREA_STATS = {'north': -25.0, 'south': -26.2, 'west': -57.5, 'east': -56.5}
YEARS = list(range(1990, 2026))
MONTHS = [f'{m:02d}' for m in range(1, 13)]

DATASETS = {
    '2m_temperature': {
        'dataset': 'reanalysis-era5-single-levels-monthly-means',
        'request': {
            'product_type': 'monthly_averaged_reanalysis',
            'variable': '2m_temperature',
            'year': [str(y) for y in YEARS],
            'month': MONTHS,
            'time': '00:00',
            'area': [-25.0, -57.5, -26.2, -56.5],
            'format': 'netcdf',
        },
        'output': 'era5_2m_tavg_1990_2025.nc',
    },
    'total_precipitation': {
        'dataset': 'reanalysis-era5-single-levels-monthly-means',
        'request': {
            'product_type': 'monthly_averaged_reanalysis',
            'variable': 'total_precipitation',
            'year': [str(y) for y in YEARS],
            'month': MONTHS,
            'time': '00:00',
            'area': [-25.0, -57.5, -26.2, -56.5],
            'format': 'netcdf',
        },
        'output': 'era5_total_precip_1990_2025.nc',
    },
    '10m_wind': {
        'dataset': 'reanalysis-era5-single-levels-monthly-means',
        'request': {
            'product_type': 'monthly_averaged_reanalysis',
            'variable': ['10m_u_component_of_wind', '10m_v_component_of_wind'],
            'year': [str(y) for y in YEARS],
            'month': MONTHS,
            'time': '00:00',
            'area': [-25.0, -57.5, -26.2, -56.5],
            'format': 'netcdf',
        },
        'output': 'era5_10m_wind_1990_2025.nc',
    },
    'solar_radiation': {
        'dataset': 'reanalysis-era5-single-levels-monthly-means',
        'request': {
            'product_type': 'monthly_averaged_reanalysis',
            'variable': 'surface_solar_radiation_downwards',
            'year': [str(y) for y in YEARS],
            'month': MONTHS,
            'time': '00:00',
            'area': [-25.0, -57.5, -26.2, -56.5],
            'format': 'netcdf',
        },
        'output': 'era5_solar_rad_1990_2025.nc',
    },
}


def fetch_one(c, name, cfg):
    out = OUT_DIR / cfg['output']
    if out.exists() and out.stat().st_size > 1_000_000:
        print(f'  [{name}] cached: {out.name} ({out.stat().st_size//1024//1024} MB)')
        return out
    print(f'  [{name}] submitting CDS request (35 years x 12 months)...', flush=True)
    import time
    t0 = time.time()
    try:
        result = c.retrieve(cfg['dataset'], cfg['request'])
        print(f'  [{name}] job accepted, downloading to {out.name}...', flush=True)
        result.download(str(out))
        elapsed = time.time() - t0
        print(f'  [{name}] OK: {out.stat().st_size//1024//1024} MB in {elapsed:.0f}s')
        return out
    except Exception as e:
        elapsed = time.time() - t0
        print(f'  [{name}] FAILED after {elapsed:.0f}s: {type(e).__name__}: {str(e)[:200]}')
        return None


def main():
    print('=' * 70)
    print('ERA5 climate baseline — Escobar / Mbopicuá, PY')
    print(f'Bbox: N={AREA_STATS["north"]} S={AREA_STATS["south"]} W={AREA_STATS["west"]} E={AREA_STATS["east"]}')
    print(f'Years: {YEARS[0]}-{YEARS[-1]} ({len(YEARS)} years x 12 months)')
    print('=' * 70)

    c = cdsapi.Client()
    print(f'CDS client: {c.url}')
    print(f'UID: {c.key}')

    fetched = {}
    for name, cfg in DATASETS.items():
        f = fetch_one(c, name, cfg)
        if f:
            fetched[name] = f

    print(f'\nDONE. {len(fetched)}/{len(DATASETS)} files fetched.')
    return 0 if len(fetched) == len(DATASETS) else 1


if __name__ == '__main__':
    sys.exit(main())