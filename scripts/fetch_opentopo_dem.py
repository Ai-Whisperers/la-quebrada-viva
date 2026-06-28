"""OpenTopography global DEM fetcher for the Escobar / Mbopicuá bbox.

Loads OPENTOPOGRAPHY_API_KEY from .env.local, requests several DEMs, saves
the GeoTIFFs + a hillshade PNG for each, writes a summary.

Output:
  - docs/site_data/alos_aw3d30_dem.tif + _hillshade.png
  - docs/site_data/cop30_dem.tif + _hillshade.png
  - docs/site_data/srtm_gl1_dem.tif + _hillshade.png
  - docs/site_data/nasadem_dem.tif + _hillshade.png
  - docs/site_data/dem_summary.txt
"""
import os
import sys
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import requests
from dotenv import load_dotenv

HERE = Path(__file__).parent.parent
load_dotenv(dotenv_path=HERE / ".env.local")
OT_KEY = os.environ.get("OPENTOPOGRAPHY_API_KEY")
if not OT_KEY:
    print("ERROR: OPENTOPOGRAPHY_API_KEY not in .env.local", file=sys.stderr)
    sys.exit(1)

BBOX = {"south": -25.645, "north": -25.615, "west": -57.045, "east": -57.015}
OT_API = "https://portal.opentopography.org/API/globaldem"
OUT_DIR = HERE / "docs" / "site_data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# (demtype, friendly name, output prefix)
DATASETS = [
    ("AW3D30",   "ALOS World 3D 30m (JAXA)",         "alos_aw3d30"),
    ("COP30",    "Copernicus DEM 30m (GLO-30)",      "cop30"),
    ("SRTMGL1",  "SRTM v3 GL1 30m (NASA / USGS)",     "srtm_gl1"),
    ("NASADEM",  "NASADEM 30m (NASA)",                "nasadem"),
]

def fetch_dem(demtype: str) -> bytes:
    params = {
        "demtype": demtype,
        "west": BBOX["west"],
        "south": BBOX["south"],
        "east": BBOX["east"],
        "north": BBOX["north"],
        "outputFormat": "GTiff",
        "API_Key": OT_KEY,
    }
    r = requests.get(OT_API, params=params, timeout=180)
    if r.status_code != 200:
        print(f"      HTTP {r.status_code} — body: {r.text[:200]}")
        return None
    if r.content[:4] != b"II*\x00":  # TIFF magic bytes
        print(f"      not a TIFF, body preview: {r.content[:120]!r}")
        return None
    return r.content


def make_hillshade(tif_path: Path, out_png: Path, label: str):
    with rasterio.open(tif_path) as src:
        arr = src.read(1).astype(float)
        nodata = src.nodata
        if nodata is not None:
            arr = np.where(arr == nodata, np.nan, arr)
        valid_mask = ~np.isnan(arr)
        if not valid_mask.any():
            print(f"      (no valid pixels for {tif_path.name})")
            return None, None
        bounds = src.bounds
        res = src.res
        stats = {
            "min_m": float(np.nanmin(arr)),
            "max_m": float(np.nanmax(arr)),
            "mean_m": float(np.nanmean(arr)),
            "median_m": float(np.nanmedian(arr)),
            "p10_m": float(np.nanpercentile(arr, 10)),
            "p90_m": float(np.nanpercentile(arr, 90)),
            "range_m": float(np.nanmax(arr) - np.nanmin(arr)),
            "pixel_res_m": float(res[0]),
        }

        # Hillshade (az 315° NW, alt 45°)
        az_rad = np.deg2rad(90.0 - 315.0)
        alt_rad = np.deg2rad(45.0)
        x, y = np.gradient(arr, res[0], res[0])
        slope = np.pi / 2.0 - np.arctan(np.sqrt(x * x + y * y))
        aspect = np.arctan2(-x, y)
        shaded = np.sin(alt_rad) * np.sin(slope) + np.cos(alt_rad) * np.cos(slope) * np.cos(az_rad - aspect)
        shaded = np.clip(np.where(np.isnan(shaded), 0, shaded), 0, 1)

    fig, ax = plt.subplots(figsize=(10, 10), dpi=120)
    im = ax.imshow(
        shaded, cmap="gray",
        extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
        origin="upper",
    )
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(
        f"{label}\nHillshade (az 315°, alt 45°) — elev "
        f"{stats['min_m']:.0f}–{stats['max_m']:.0f} m AMSL ({stats['range_m']:.0f} m range)"
    )
    plt.colorbar(im, ax=ax, label="hillshade intensity")
    plt.tight_layout()
    plt.savefig(out_png, dpi=120, bbox_inches="tight")
    plt.close()
    return shaded, stats


def main():
    print("=" * 70)
    print("OpenTopography Global DEMs — Escobar / Mbopicuá, Paraguarí, PY")
    print("=" * 70)
    print(f"Bbox: W={BBOX['west']} S={BBOX['south']} E={BBOX['east']} N={BBOX['north']}")
    print()

    summary_lines = [f"OpenTopography global DEMs — {datetime.utcnow().isoformat()}Z",
                     f"Bbox: W={BBOX['west']} S={BBOX['south']} E={BBOX['east']} N={BBOX['north']}",
                     ""]

    for demtype, label, prefix in DATASETS:
        print(f"\n[{demtype}] fetching {label}…")
        content = fetch_dem(demtype)
        if content is None:
            print("      FAILED, skipping")
            summary_lines.append(f"{demtype}: FAILED")
            continue
        tif = OUT_DIR / f"{prefix}_dem.tif"
        tif.write_bytes(content)
        print(f"      wrote {tif}  ({len(content):,} bytes)")

        print("      computing hillshade + stats…")
        hs, stats = make_hillshade(tif, OUT_DIR / f"{prefix}_hillshade.png", label)
        if stats is None:
            continue
        print(f"      elev {stats['min_m']:.1f}–{stats['max_m']:.1f} m AMSL  "
              f"(range {stats['range_m']:.1f} m, mean {stats['mean_m']:.1f} m, median {stats['median_m']:.1f} m)")
        print(f"      pixel {stats['pixel_res_m']:.0f} m  hillshade: {prefix}_hillshade.png")
        summary_lines.append(
            f"{demtype}: {label}  |  elev {stats['min_m']:.0f}–{stats['max_m']:.0f} m "
            f"(range {stats['range_m']:.0f} m, mean {stats['mean_m']:.0f} m)  |  "
            f"pixel {stats['pixel_res_m']:.0f} m"
        )

    with open(OUT_DIR / "dem_summary.txt", "w") as f:
        f.write("\n".join(summary_lines) + "\n")
    print(f"\nSummary written to {OUT_DIR / 'dem_summary.txt'}")
    print("DONE.")


if __name__ == "__main__":
    main()
