#!/usr/bin/env python3
"""LQV viewer orchestrator. Rebuilds all data layers from source rasters
and OSM Overpass in the correct order.

Usage:
  python3 scripts/make.py             # full rebuild
  python3 scripts/make.py --quick      # skip OSM pull, hillshade, contours
  python3 scripts/make.py --deploy     # build + wrangler deploy

Order:
  1. fetch_osm_10km.py           (~60s, Overpass API)
  2. build_10km_layers.py        (~4 min, Sentinel-2 + Copernicus DEM)
  3. build_hillshade.py          (~30s, hillshade raster)
  4. build_dem_contours.py        (~30s, 50 m contours)
  5. build_10km_fullcover.py      (~60s, MapBiomas + Hansen)
  6. build_woodland_merged.py     (~30s, 4-source fusion)
  7. build_client_gps_layers.py   (~5s, Wes's GPS data)
  8. audit_wetlands_10km.py       (~30s, OSM × JRC × DEM audit)
  9. audit_jrc_waterbodies.py     (~5s, JRC waterbodies)
  10. build_combined_waterway.py  (~5s, combined water)
  11. build_hand.py               (~30s, HAND floodplain)
  12. build_local_quebrada.py     (~5s, GPS-derived quebrada)
  13. build_ndvi_backdrop.py      (~30s, NDVI continuous raster)
  14. build_elevation_grid.py     (~10s, cursor HUD grid)
  15. build_forest_timeline.py    (~30s, MapBiomas 1985→2023)
  16. add_area_ha.py              (~5s, accurate WGS84 area)
  17. clean_geometries.py         (~10s, validation + clip)
  18. smoke_test.py               (~10s, validation report)
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path("/root/la-quebrada-viva")
SCRIPTS = ROOT / "scripts"

STEPS = [
    ("fetch_osm_10km.py",           60,  "Pull OSM Overpass"),
    ("build_10km_layers.py",        240, "DEM streams + NDVI canopy + flow arrows"),
    ("build_hillshade.py",          30,  "Hillshade raster"),
    ("build_topology_hillshade.py", 5,   "Parcel-scale 5m hillshade"),
    ("build_parcel_contours_5m.py", 30,  "Parcel-scale 5m contours (topology tier-1)"),
    ("build_dem_contours.py",       30,  "DEM contours + colour-relief"),
    ("build_10km_fullcover.py",     60,  "MapBiomas + Hansen loss/gain"),
    ("build_woodland_merged.py",    30,  "Woodland merged (4 sources)"),
    ("build_client_gps_layers.py",  5,   "Client GPS layers"),
    ("audit_wetlands_10km.py",      30,  "Wetland audit"),
    ("audit_jrc_waterbodies.py",    5,   "JRC waterbodies"),
    ("build_combined_waterway.py",  5,   "Combined water"),
    ("build_hand.py",               30,  "HAND floodplain"),
    ("build_local_quebrada.py",     5,   "Local Quebrada from GPS"),
    ("build_ndvi_backdrop.py",      30,  "NDVI backdrop raster"),
    ("build_elevation_grid.py",    10,  "Cursor HUD grid"),
    ("build_forest_timeline.py",    30,  "Forest change timeline"),
    ("add_area_ha.py",              5,   "Add WGS84 area_ha"),
    ("clean_geometries.py",         10,  "Validate + clip"),
    ("smoke_test.py",               10,  "Smoke test"),
]

QUICK_SKIP = {
    "fetch_osm_10km.py",
    "build_hillshade.py",
    "build_dem_contours.py",
}


def run(name, timeout):
    print(f"\n{'='*60}\n>>> {name}\n{'='*60}", flush=True)
    t0 = time.time()
    try:
        result = subprocess.run(
            ["python3", "-u", str(SCRIPTS / name)],
            cwd=ROOT, timeout=timeout, capture_output=False,
        )
        dt = time.time() - t0
        if result.returncode != 0:
            print(f"  ✗ {name} failed (rc={result.returncode}, {dt:.0f}s)")
            return False
        print(f"  ✓ {name} done ({dt:.0f}s)")
        return True
    except subprocess.TimeoutExpired:
        print(f"  ✗ {name} TIMEOUT after {timeout}s")
        return False


def deploy():
    import os
    deploy_dir = ROOT / "splats/exports/web"
    env_file = Path("/root/.cloudflare-env")
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("CLOUDFLARE_API_TOKEN="):
                tok = line.split("=", 1)[1].strip().strip('"').strip("'")
                os.environ["CF_API_TOKEN"] = tok
                os.environ["CLOUDFLARE_API_TOKEN"] = tok
                break
    os.environ["CLOUDFLARE_ACCOUNT_ID"] = "9eb1832f3e42a1dbd6ba854f8d6a1cb2"
    print(f"\n{'='*60}\n>>> Deploying to Cloudflare Pages\n{'='*60}")
    subprocess.run([
        "wrangler", "pages", "deploy", str(deploy_dir),
        "--project-name", "lqv-walkthrough", "--branch", "main",
        "--commit-dirty=true",
    ], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="Skip OSM + hillshade + contours")
    ap.add_argument("--deploy", action="store_true", help="Deploy after build")
    ap.add_argument("--only", help="Run only this script (substring match)")
    args = ap.parse_args()

    failures = []
    for name, timeout, desc in STEPS:
        if args.quick and name in QUICK_SKIP:
            print(f"  ⊘ {name} skipped (--quick)")
            continue
        if args.only and args.only not in name:
            continue
        print(f"\n  [{desc}]")
        if not run(name, timeout):
            failures.append(name)

    if failures:
        print(f"\n✗ {len(failures)} failures: {failures}")
        sys.exit(1)

    if args.deploy:
        deploy()
    else:
        print("\n✓ All builds complete. Deploy with --deploy or:")
        print("  cd splats/exports/web && wrangler pages deploy . \\")
        print("    --project-name lqv-walkthrough --branch main")


if __name__ == "__main__":
    main()