"""Post-process the GEDI CSV to (a) drop the elev_lowestmode outliers (some beams
return scaled values when the receive-channel mis-calibrates) and (b) join the
DEM elevations from the ALOS GeoTIFF to each shot so we have a single
canonical (ground elevation) value per shot.

Outputs:
  - docs/site_data/gedi_l2a_points_clean.csv  (filtered + DEM-joined)
  - docs/site_data/gedi_l2a_clean_summary.txt

Heuristics:
  - Keep shots with 100 < ground_elevation_m < 500 m AMSL (Paraguari elevation
    band — covers stream pool at ~120m to escarpment top at ~380m per the DEM).
    Drops the elev >1000 m outliers seen in the raw GEDI output.
  - For shots that pass the filter, prefer DEM elevation at the shot XY (more
    reliable than the beam's elev_lowestmode). Add `dem_elev_m` column.
  - Recompute canopy as elev_highestreturn - dem_elev_m where the canopy
    value looks reasonable, else keep the original GEDI canopy.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from dotenv import load_dotenv
from rasterio.transform import rowcol

HERE = Path('/home/ai-whisperers/blender-projects/la-quebrada-viva')
load_dotenv(dotenv_path=HERE / '.env.local')

IN_CSV = HERE / 'docs' / 'site_data' / 'gedi_l2a_points.csv'
DEM_PATH = HERE / 'docs' / 'site_data' / 'alos_aw3d30_dem.tif'
OUT_CSV = HERE / 'docs' / 'site_data' / 'gedi_l2a_points_clean.csv'
OUT_SUMMARY = HERE / 'docs' / 'site_data' / 'gedi_l2a_clean_summary.txt'

ELEV_MIN_M = 100.0
ELEV_MAX_M = 500.0

print("=" * 70)
print("GEDI L2A post-processing — clean outliers + DEM-join")
print("=" * 70)

df = pd.read_csv(IN_CSV)
print(f"\nLoaded {len(df)} raw shots from {IN_CSV.name}")
print(f"  ground_elevation_m: min {df['ground_elevation_m'].min():.1f}, "
      f"max {df['ground_elevation_m'].max():.1f}, "
      f"median {df['ground_elevation_m'].median():.1f}")
print(f"  canopy_height_m:    min {df['canopy_height_m'].min():.1f}, "
      f"max {df['canopy_height_m'].max():.1f}, "
      f"median {df['canopy_height_m'].median():.1f}")

# 1) Drop elev outliers
before = len(df)
df = df[(df['ground_elevation_m'] >= ELEV_MIN_M) & (df['ground_elevation_m'] <= ELEV_MAX_M)].copy()
print(f"\n[1/3] Elev outlier filter: kept {len(df)}/{before} (dropped {before - len(df)})")
print(f"  range after filter: {df['ground_elevation_m'].min():.1f} - {df['ground_elevation_m'].max():.1f} m AMSL")

# 2) Join DEM elevation at each shot XY
print(f"\n[2/3] Joining DEM elevations from {DEM_PATH.name}...")
with rasterio.open(DEM_PATH) as src:
    dem = src.read(1).astype(float)
    dem_nodata = src.nodata
    if dem_nodata is not None:
        dem = np.where(dem == dem_nodata, np.nan, dem)
    transform = src.transform
    rows, cols = [], []
    for _, shot in df.iterrows():
        try:
            r, c = rowcol(transform, shot['longitude'], shot['latitude'])
            rows.append(int(r))
            cols.append(int(c))
        except Exception:
            rows.append(-1)
            cols.append(-1)
    df['_row'] = rows
    df['_col'] = cols
    def _dem_elev(r, c):
        if 0 <= r < dem.shape[0] and 0 <= c < dem.shape[1]:
            v = dem[r, c]
            return float(v) if not np.isnan(v) else np.nan
        return np.nan
    df['dem_elev_m'] = [_dem_elev(r, c) for r, c in zip(df['_row'], df['_col'])]
    df.drop(columns=['_row', '_col'], inplace=True)
print(f"  dem_elev_m: min {df['dem_elev_m'].min():.1f}, "
      f"max {df['dem_elev_m'].max():.1f}, "
      f"median {df['dem_elev_m'].median():.1f}")

# 3) Recompute canopy as elev_highestreturn - dem_elev_m
print("\n[3/3] Recomputing canopy with DEM-anchored base...")
df['elev_highestreturn_m'] = df['ground_elevation_m'] + df['canopy_height_m']
df['canopy_from_dem_m'] = (df['elev_highestreturn_m'] - df['dem_elev_m']).clip(lower=0, upper=80)
df['canopy_height_m_final'] = df['canopy_from_dem_m']

# 4) Save
df.to_csv(OUT_CSV, index=False)
print(f"\nWrote {len(df)} clean shots to {OUT_CSV.name}")

print("\nClean ground_elevation_m (GEDI, after outlier filter):")
print(df['ground_elevation_m'].describe().to_string())
print("\ndem_elev_m (ALOS AW3D30 30m, more reliable):")
print(df['dem_elev_m'].describe().to_string())
print("\ncanopy_height_m_final (anchored to DEM):")
print(df['canopy_height_m_final'].describe().to_string())
print("\nBeam distribution (cleaned):")
print(df['beam'].value_counts().to_string())

with open(OUT_SUMMARY, 'w') as f:
    f.write(f"GEDI L2A cleaned — {pd.Timestamp.now().isoformat()}\n")
    f.write(f"Source CSV: {IN_CSV} ({len(pd.read_csv(IN_CSV))} rows)\n")
    f.write(f"After elev outlier filter ({ELEV_MIN_M}-{ELEV_MAX_M} m): {len(df)} rows\n")
    f.write(f"DEM source for elevation join: {DEM_PATH.name}\n\n")
    f.write("Clean ground_elevation_m (GEDI):\n")
    f.write(df['ground_elevation_m'].describe().to_string() + "\n\n")
    f.write("dem_elev_m (ALOS AW3D30):\n")
    f.write(df['dem_elev_m'].describe().to_string() + "\n\n")
    f.write("canopy_height_m_final:\n")
    f.write(df['canopy_height_m_final'].describe().to_string() + "\n\n")
    f.write("Beam distribution:\n")
    f.write(df['beam'].value_counts().to_string() + "\n\n")
    f.write("Lat range: {:.5f} to {:.5f}\n".format(df['latitude'].min(), df['latitude'].max()))
    f.write("Lon range: {:.5f} to {:.5f}\n".format(df['longitude'].min(), df['longitude'].max()))

print(f"\nSummary written to {OUT_SUMMARY.name}")
print("DONE.")
