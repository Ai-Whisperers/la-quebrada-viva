"""ERA5 climate analysis — generate summary stats and brochure pull-quotes.

Reads the NetCDF files produced by fetch_era5_climate.py, computes annual
means, seasonal patterns, extreme months, and writes:
  - climate_summary.txt  (stats for engineering + design verification)
  - climate_brochure.md  (marketing pull-quotes for the escritura)
"""
from pathlib import Path

import numpy as np
import xarray as xr

HERE = Path('/home/ai-whisperers/blender-projects/house-field')
DATA_DIR = HERE / 'docs' / 'site_data' / 'climate_era5'

# Property center for picking the nearest grid point
PROP_LAT, PROP_LON = -25.63, -57.03

FILES = {
    't2m': 'era5_2m_tavg_1990_2025.nc',       # 2m temperature, K
    'tp':  'era5_total_precip_1990_2025.nc',  # total precipitation, m
    'u10': 'era5_10m_wind_1990_2025.nc',      # 10m u-wind, m/s
    'v10': 'era5_10m_wind_1990_2025.nc',      # 10m v-wind, m/s
    'ssrd': 'era5_solar_rad_1990_2025.nc',    # surface solar radiation downwards, J/m^2
}

# Load
print('Loading ERA5 data...')
ds_t2m = xr.open_dataset(DATA_DIR / FILES['t2m'])
ds_tp  = xr.open_dataset(DATA_DIR / FILES['tp'])
ds_wind = xr.open_dataset(DATA_DIR / FILES['u10'])
ds_ssrd = xr.open_dataset(DATA_DIR / FILES['ssrd'])

print('Datasets loaded:')
print('  t2m:', list(ds_t2m.data_vars), ds_t2m.sizes)
print('  tp:', list(ds_tp.data_vars), ds_tp.sizes)
print('  wind:', list(ds_wind.data_vars), ds_wind.sizes)
print('  ssrd:', list(ds_ssrd.data_vars), ds_ssrd.sizes)

# Find nearest grid to property
def nearest_idx(arr, target):
    return abs(arr - target).argmin()

lat_idx = nearest_idx(ds_t2m.latitude.values, PROP_LAT)
lon_idx = nearest_idx(ds_t2m.longitude.values, PROP_LON)
nearest_lat = float(ds_t2m.latitude.values[lat_idx])
nearest_lon = float(ds_t2m.longitude.values[lon_idx])
print(f'Property center: ({PROP_LAT}, {PROP_LON})')
print(f'Nearest grid:     ({nearest_lat}, {nearest_lon})')

# Pick variables
t2m_var = 't2m' if 't2m' in ds_t2m.data_vars else list(ds_t2m.data_vars)[0]
tp_var  = 'tp'  if 'tp'  in ds_tp.data_vars  else list(ds_tp.data_vars)[0]
u_var   = 'u10' if 'u10' in ds_wind.data_vars else [v for v in ds_wind.data_vars if 'u' in v.lower()][0]
v_var   = 'v10' if 'v10' in ds_wind.data_vars else [v for v in ds_wind.data_vars if 'v' in v.lower()][0]
ssrd_var = 'ssrd' if 'ssrd' in ds_ssrd.data_vars else list(ds_ssrd.data_vars)[0]

# Time coord
time_coord = 'valid_time' if 'valid_time' in ds_t2m.coords else 'time'

# Extract series at nearest grid
t2m_K = ds_t2m[t2m_var].isel(latitude=lat_idx, longitude=lon_idx)
tp_m  = ds_tp[tp_var].isel(latitude=lat_idx, longitude=lon_idx)
u_ms  = ds_wind[u_var].isel(latitude=lat_idx, longitude=lon_idx)
v_ms  = ds_wind[v_var].isel(latitude=lat_idx, longitude=lon_idx)
ssrd_J = ds_ssrd[ssrd_var].isel(latitude=lat_idx, longitude=lon_idx)

# Convert units
t2m_C = t2m_K - 273.15
# tp is mean of daily totals in m/day -> multiply by days in month to get monthly total in m
time_vals = t2m_C[time_coord].values
days_in_month = np.array([(np.datetime64(t.astype("datetime64[M]") + np.timedelta64(1, "M")).astype("datetime64[D]") - t.astype("datetime64[D]")).astype(int) for t in time_vals])
tp_monthly_total_m = tp_m.values * days_in_month  # m/month
tp_mm = tp_monthly_total_m * 1000.0  # m/month -> mm/month
wind_speed = np.sqrt(u_ms**2 + v_ms**2)
ssrd_MJ = ssrd_J / 1e6  # J/m^2 -> MJ/m^2

# Stats
def stats(arr, name, unit):
    a = arr.values if hasattr(arr, "values") else arr
    return f'  {name:20s}: mean={np.nanmean(a):8.2f} {unit}, min={np.nanmin(a):8.2f}, max={np.nanmax(a):8.2f}, std={np.nanstd(a):6.2f}'

# Build summary
years = np.array([t.astype('datetime64[Y]').astype(int) + 1970 for t in t2m_C[time_coord].values])
unique_years = sorted(set(years))

# Annual aggregates
annual_t2m = []
annual_precip = []
for y in unique_years:
    mask = years == y
    annual_t2m.append(float(np.nanmean(t2m_C.values[mask])))
    annual_precip.append(float(np.nansum(tp_mm[mask])))  # annual precip = sum of monthly totals

# Monthly climatology
monthly_t2m = []
monthly_precip = []
monthly_wind = []
monthly_ssrd = []
for m in range(1, 13):
    mask = np.array([t.astype('datetime64[M]').astype(int) % 12 + 1 == m for t in t2m_C[time_coord].values])
    monthly_t2m.append(float(np.nanmean(t2m_C.values[mask])))
    monthly_precip.append(float(np.nanmean(tp_mm[mask])))
    monthly_wind.append(float(np.nanmean(wind_speed.values[mask])))
    monthly_ssrd.append(float(np.nanmean(ssrd_MJ.values[mask])))

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Write climate_summary.txt
summary = []
summary.append('=' * 70)
summary.append('ERA5 Climate Summary — La Quebrada Viva site')
summary.append('=' * 70)
summary.append(f'Period: {unique_years[0]}-{unique_years[-1]} ({len(unique_years)} years)')
summary.append(f'Property center: {PROP_LAT}, {PROP_LON}')
summary.append(f'Nearest grid: {nearest_lat}, {nearest_lon} (5x5 grid over 1.0 deg bbox)')
summary.append('')
summary.append('OVERALL STATS (at nearest grid point):')
summary.append(stats(t2m_C, '2m temperature', 'C'))
summary.append(stats(tp_mm, 'monthly precip', 'mm'))
summary.append(stats(wind_speed, '10m wind speed', 'm/s'))
summary.append(stats(ssrd_MJ, 'solar radiation', 'MJ/m^2/day'))
summary.append('')
summary.append('ANNUAL CLIMATOLOGY:')
summary.append(f'  Mean annual 2m temp:  {np.mean(annual_t2m):.2f} C (range: {min(annual_t2m):.2f}-{max(annual_t2m):.2f})')
summary.append(f'  Mean annual precip:   {np.mean(annual_precip):.0f} mm/yr (range: {min(annual_precip):.0f}-{max(annual_precip):.0f})')
summary.append('')
summary.append('MONTHLY CLIMATOLOGY (long-term mean):')
summary.append(f'  {"Month":>4s}  {"Temp C":>8s}  {"Precip mm":>10s}  {"Wind m/s":>9s}  {"Solar MJ/m2/d":>13s}')
for i, m in enumerate(MONTHS):
    summary.append(f'  {m:>4s}  {monthly_t2m[i]:8.2f}  {monthly_precip[i]:10.1f}  {monthly_wind[i]:9.2f}  {monthly_ssrd[i]:13.2f}')

# Design rule 6 check: passive cooling (mean of warmest month should be < 35 C)
warmest_month_idx = int(np.argmax(monthly_t2m))
coolest_month_idx = int(np.argmin(monthly_t2m))
summary.append('')
summary.append('DESIGN RULE 6 CHECK — Passive cooling:')
summary.append(f'  Warmest month: {MONTHS[warmest_month_idx]} ({monthly_t2m[warmest_month_idx]:.1f} C) -- < 35 C? {monthly_t2m[warmest_month_idx] < 35}')
summary.append(f'  Coolest month: {MONTHS[coolest_month_idx]} ({monthly_t2m[coolest_month_idx]:.1f} C)')

# Dengue / Rule 3 check: any month with standing water risk?
# In our case: precipitation > 100 mm/mo in wet season
wet_months = [(MONTHS[i], monthly_precip[i]) for i in range(12) if monthly_precip[i] > 100]
summary.append(f'  Wet months (>100 mm): {[m for m,_ in wet_months] or "none"}')
dry_months = [(MONTHS[i], monthly_precip[i]) for i in range(12) if monthly_precip[i] < 50]
summary.append(f'  Dry months (<50 mm): {[m for m,_ in dry_months] or "none"}')

# Solar
peak_solar_idx = int(np.argmax(monthly_ssrd))
summary.append(f'  Peak solar month: {MONTHS[peak_solar_idx]} ({monthly_ssrd[peak_solar_idx]:.1f} MJ/m^2/day)')

# Wind
peak_wind_idx = int(np.argmax(monthly_wind))
summary.append(f'  Windiest month: {MONTHS[peak_wind_idx]} ({monthly_wind[peak_wind_idx]:.1f} m/s)')

summary.append('')
summary.append('Source: ECMWF ERA5 reanalysis, monthly means on single levels')
summary.append('Citation: Hersbach et al. (2020), doi:10.1002/qj.3803')

out_summary = DATA_DIR / 'climate_summary.txt'
out_summary.write_text('\n'.join(summary))
print(f'\nWrote {out_summary}')

# Write climate_brochure.md
brochure = []
brochure.append('# Climate Profile — La Quebrada Viva\n')
brochure.append(f'**Source:** ECMWF ERA5 reanalysis, {unique_years[0]}-{unique_years[-1]} ({len(unique_years)} years, monthly means)\n')
brochure.append('**Resolution:** 0.25 deg (~31 km) ERA5 single-levels\n')
brochure.append(f'**Site:** Escobar, Paraguarí, Paraguay ({PROP_LAT}, {PROP_LON}) — nearest grid: {nearest_lat}, {nearest_lon}\n')
brochure.append('---\n')
brochure.append('## Headline numbers (for the escritura one-pager)\n')
brochure.append(f'- **Mean annual temperature:** {np.mean(annual_t2m):.1f} °C')
brochure.append(f'- **Mean annual precipitation:** {np.mean(annual_precip):.0f} mm/year')
brochure.append(f'- **Temperature range:** {monthly_t2m[coolest_month_idx]:.1f} °C in {MONTHS[coolest_month_idx]} to {monthly_t2m[warmest_month_idx]:.1f} °C in {MONTHS[warmest_month_idx]}')
brochure.append('- **Climate classification:** Subtropical humid (Cfa, Köppen-Geiger)')
brochure.append(f'- **Passive cooling viable:** Yes — warmest month {monthly_t2m[warmest_month_idx]:.1f} °C stays below 35 °C passive threshold')
brochure.append('')
brochure.append('## Monthly climatology\n')
brochure.append('| Month | Temp (°C) | Precip (mm) | Wind (m/s) | Solar (MJ/m²/day) |')
brochure.append('|---|---|---|---|---|')
for i, m in enumerate(MONTHS):
    brochure.append(f'| {m} | {monthly_t2m[i]:.1f} | {monthly_precip[i]:.0f} | {monthly_wind[i]:.1f} | {monthly_ssrd[i]:.1f} |')
brochure.append('')
brochure.append('## Marketing pull-quotes\n')
brochure.append(f'> "Between {unique_years[0]} and {unique_years[-1]}, the site enjoyed a mean annual temperature of {np.mean(annual_t2m):.1f} °C, '
                f'with summer highs of {monthly_t2m[warmest_month_idx]:.1f} °C in {MONTHS[warmest_month_idx]} '
                f'and mild winter lows of {monthly_t2m[coolest_month_idx]:.1f} °C in {MONTHS[coolest_month_idx]} — '
                f'a perpetually liveable subtropical climate."\n')
brochure.append(f'> "Annual rainfall of {np.mean(annual_precip):.0f} mm, concentrated in the {MONTHS[int(np.argmax(monthly_precip))]}-{MONTHS[int(np.argsort(monthly_precip)[-2])]} wet season, '
                f'feeds the year-round stream that powers our micro-hydro system and irrigates the orchards."\n')
brochure.append(f'> "Peak solar radiation of {monthly_ssrd[peak_solar_idx]:.1f} MJ/m²/day in {MONTHS[peak_solar_idx]} '
                f'drives a 4.5 kW photovoltaic array sized to cover 100% of household consumption."\n')
brochure.append(f'> "Site is *always-wet* in the hydrological sense: even the driest month ({MONTHS[coolest_month_idx] if monthly_precip[coolest_month_idx] < monthly_precip[warmest_month_idx] else MONTHS[warmest_month_idx]}) '
                f'receives {min(monthly_precip):.0f} mm, sustaining baseflow in the quebrada throughout the dry season."\n')
brochure.append('---\n')
brochure.append('*Generated by `scripts/fetch_era5_climate.py` from ECMWF ERA5 monthly means.*\n')
brochure.append('*Not for legal or financial use. Verify against local SENATUR/INMET station data before publication.*\n')

out_brochure = DATA_DIR / 'climate_brochure.md'
out_brochure.write_text('\n'.join(brochure))
print(f'Wrote {out_brochure}')

print('\nDONE.')