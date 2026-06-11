"""WorldClim 2.1 — climate baseline for the Escobar / Paraguarí site.

Free, no auth. Pulls the 30s-arc (~1 km) resolution bioclimate + temperature +
precipitation variables, crops to the 3.3 km search bbox, saves as GeoTIFF.

WorldClim 2.1 monthly temperature + precipitation:
  - tavg, tmin, tmax, prec, srad, wind, vap (12 months each = 84 rasters)
  - bioclimate (19 derived rasters: annual mean temp, max temp warmest month,
    annual precip, precip seasonality, etc.)

Outputs (per variable):
  - docs/site_data/worldclim/wc2.1_30s_tavg_*.tif (12 months)
  - docs/site_data/worldclim/wc2.1_30s_bio_*.tif (19 bioclim vars)
  - docs/site_data/worldclim/worldclim_summary.txt

Use: cross-validate the climate section in docs/MASTER_BRIEF.md against
real WorldClim values for this exact site. Useful for the brochure and
for the "always-wet" GIS layer in the site analysis.
"""
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

HERE = Path('/home/ai-whisperers/blender-projects/house-field')
load_dotenv(dotenv_path=HERE / '.env.local')

OUT_DIR = HERE / 'docs' / 'site_data' / 'worldclim'
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Bbox for the site (same as GEDI + DEM)
BBOX = {'south': -25.645, 'north': -25.615, 'west': -57.045, 'east': -57.015}
# 30s-arc tile names that cover this bbox. WorldClim uses 5° tiles: S25W060,
# S25W055, S30W060, S30W055. Bbox at 25.6 S, 57.0 W sits on the S25W060 tile.
# We'll download the larger S25_W060 tile and crop.

# WorldClim 2.1 variables
MONTHLY_VARS = ['tavg', 'tmin', 'tmax', 'prec', 'srad', 'wind', 'vap']
BIOCLIM_VARS = [f'bio_{i}' for i in range(1, 20)]

BASE_URL = 'https://geodata.ucdavis.edu/climate/worldclim/2_1/30s/'
TILE = 's25_w060'  # -25 to -20 lat, -60 to -55 lon

# Download with retry
def download(url: str, out: Path, attempts: int = 3):
    for i in range(attempts):
        try:
            with requests.get(url, stream=True, timeout=180) as r:
                r.raise_for_status()
                with open(out, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 64):
                        f.write(chunk)
            return out.stat().st_size
        except Exception:
            if i == attempts - 1:
                raise
            time.sleep(2 * (i + 1))
    return 0


def crop_to_bbox(in_path: Path, out_path: Path):
    """Crop the tile to the site bbox using rasterio."""
    import rasterio
    from rasterio.windows import from_bounds
    with rasterio.open(in_path) as src:
        win = from_bounds(BBOX['west'], BBOX['south'], BBOX['east'], BBOX['north'], src.transform)
        win = win.intersection(rasterio.windows.Window(0, 0, src.width, src.height))
        data = src.read(window=win)
        new_transform = src.window_transform(win)
        profile = src.profile.copy()
        profile.update({
            'height': data.shape[1], 'width': data.shape[2],
            'transform': new_transform, 'driver': 'GTiff',
            'count': data.shape[0], 'dtype': data.dtype,
        })
        with rasterio.open(out_path, 'w', **profile) as dst:
            dst.write(data)


def main():
    print("=" * 70)
    print("WorldClim 2.1 — Escobar / Mbopicuá, PY (30s-arc ~1 km)")
    print(f"Bbox: W={BBOX['west']} S={BBOX['south']} E={BBOX['east']} N={BBOX['north']}")
    print("=" * 70)
    summary = []
    raw_dir = OUT_DIR / '_raw'
    raw_dir.mkdir(exist_ok=True)
    for var in MONTHLY_VARS + BIOCLIM_VARS:
        for suffix in ([f'_{i+1:02d}' for i in range(12)] if var in MONTHLY_VARS else ['']):
            fname = f"wc2.1_cruts4.06_30s_{var}{suffix}.tif"
            url = f"{BASE_URL}{var}/{TILE}_{var}{suffix}.tif"
            raw = raw_dir / fname
            out = OUT_DIR / fname
            print(f"  {var}{suffix}: downloading…", end=' ', flush=True)
            try:
                if not raw.exists():
                    size = download(url, raw)
                else:
                    size = raw.stat().st_size
                crop_to_bbox(raw, out)
                print(f"OK  {size//1024} KB  →  {out.relative_to(HERE)}")
                summary.append(f"{var}{suffix}: {size//1024} KB")
            except Exception as e:
                print(f"FAILED: {type(e).__name__}: {str(e)[:80]}")
                summary.append(f"{var}{suffix}: FAILED")
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for s in summary:
        print(f"  {s}")
    with open(OUT_DIR / 'worldclim_summary.txt', 'w') as f:
        f.write('\n'.join(summary) + '\n')


if __name__ == '__main__':
    main()
