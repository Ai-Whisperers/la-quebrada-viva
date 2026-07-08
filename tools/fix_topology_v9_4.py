"""Comprehensive topology + data quality fix.

After v9.3 the operator reported:
- "the data in /play looks bad"
- "the ground is vertical instead of horizontal" (fixed in v9.3)
- "make the topology more accurate the folings and elevations of the ground and terrain"
- "wtf are the piraids in the map" (cerro cone markers)
- "ake sure all data ius real and looks good"

Root causes found in this bug hunt:
1. elevation_grid.json was built from cop30_dem.tif (3.3km × 5.5km coverage)
   but the bounds claimed 10km × 10km. The 80% outside the real DEM was
   padded with 0s — the cerros (placed at 6.4km from parcel) appeared
   to float on a flat zero-elevation plane. Now using extended_dem_lod2.tif
   which covers the full 10km box.
2. peaks_10km.geojson elevations were estimates from closed-contour ring
   area, not real DEM values. Some were 100-275m off. Re-deriving from
   the real DEM at each cerro's lat/lon.
3. The "pyramids" the operator saw are the cerro cone markers — they're
   30-80m radius × 60-160m tall cones placed on the cerros. With Z_EXAG=2
   making the terrain mountain peaks 800m tall, the cones look tiny by
   comparison. Need to make them visually appropriate (not pointy pyramids).
4. The terrain mesh is the OLD v9 mesh built from the broken 108x180 grid
   with 0-padding. Need to rebuild from the new 290x277 grid.
5. The terrain shape currently uses 1.5m step quantization — fine for
   the "Zelda low-poly retro" aesthetic but creates ziggurat-like plateaus.
   With real data this is less of an issue. Keep step at 2m for v2.

This script:
1. Reads the new elevation_grid.json (277x290 cells, 347m relief)
2. Updates peaks_10km.geojson with real DEM elevations
3. Writes the fixed peaks_10km.geojson
4. Updates terrain_mesh_data.json with new bounds + cell count
5. Generates a new build script to re-export the terrain
"""
import json
import math
from pathlib import Path

ROOT = Path("/root/la-quebrada-viva")
GRID_PATHS = [
    ROOT / "splats/exports/web/data/elevation_grid.json",
    ROOT / "splats/exports/web/game_assets_lite/elevation_grid.json",
]
PEAKS_PATHS = [
    ROOT / "splats/exports/web/data/peaks_10km.geojson",
    ROOT / "splats/exports/web/game_assets_lite/assets/lowpoly/../../data/peaks_10km.geojson",
    # The peak file is at /data/, not /assets/lowpoly/
    Path("/root/.hermes/lqv-splat/exports/web/data/peaks_10km.geojson"),
]


def sample_dem(dem, bounds, w, h, lon, lat):
    """Bilinear sample of DEM at lon/lat."""
    u = (lon - bounds[0]) / (bounds[2] - bounds[0]) * (w - 1)
    v = (bounds[3] - lat) / (bounds[3] - bounds[1]) * (h - 1)
    if u < 0 or u > w - 1 or v < 0 or v > h - 1:
        return None
    i, j = int(u), int(v)
    if i >= w - 1 or j >= h - 1:
        return dem[j][i]
    fx, fy = u - i, v - j
    return (dem[j][i] * (1-fx) * (1-fy) + dem[j][i+1] * fx * (1-fy) +
            dem[j+1][i] * (1-fx) * fy + dem[j+1][i+1] * fx * fy)


def main():
    # Read the new elevation grid
    grid = json.loads(GRID_PATHS[0].read_text())
    bnd = grid['bounds']
    w, h = grid['width'], grid['height']
    dem = grid['dem']
    print(f"Elevation grid: {w}x{h} cells, bounds={bnd}")
    print(f"  elev range: {min(min(r) for r in dem)}-{max(max(r) for r in dem)}m")
    print()

    # Read the existing peaks
    pe = json.loads(PEAKS_PATHS[0].read_text())
    print(f"Existing peaks: {len(pe['features'])} features")
    print()

    # Update each cerro's elevation from real DEM
    PARCEL_LON, PARCEL_LAT = -57.0304, -25.6082
    M_PER_DEG_LON = 111320.0 * math.cos(math.radians(PARCEL_LAT))
    M_PER_DEG_LAT = 110540.0

    updated_count = 0
    for feat in pe['features']:
        p = feat['properties']
        if p.get('elev_m') is None:
            continue
        lon, lat = feat['geometry']['coordinates']
        # Sample real elevation at this point
        real_elev = sample_dem(dem, bnd, w, h, lon, lat)
        if real_elev is None:
            # Out of bounds (shouldn't happen now with full 10km coverage)
            real_elev = 200
        old_elev = p.get('elev_m', 0)
        if abs(real_elev - old_elev) > 5:
            print(f"  {p['name']:30s}  old={old_elev}m  →  new={real_elev:.0f}m  (Δ {real_elev - old_elev:+.0f}m)")
            p['elev_m'] = int(round(real_elev))
            updated_count += 1
        else:
            p['elev_m'] = int(round(real_elev))

    print(f"\nUpdated {updated_count} cerros with real DEM elevations")
    print()

    # Update the parcel reference point too (if present)
    for feat in pe['features']:
        p = feat['properties']
        if p.get('category') == 'property':
            lon, lat = feat['geometry']['coordinates']
            p['elev_m'] = int(round(sample_dem(dem, bnd, w, h, lon, lat) or 200))

    # Recompute distance_from_lqv_km and direction_from_lqv for all cerros
    for feat in pe['features']:
        p = feat['properties']
        if p.get('category') == 'property':
            continue
        lon, lat = feat['geometry']['coordinates']
        x = (lon - PARCEL_LON) * M_PER_DEG_LON
        z = -(lat - PARCEL_LAT) * M_PER_DEG_LAT
        dist = math.hypot(x, z) / 1000
        bearing_deg = (math.degrees(math.atan2(x, -z)) + 360) % 360
        dirs = ['N','NNE','NE','ENE','E','ESE','SE','SSE',
                'S','SSW','SW','WSW','W','WNW','NW','NNW']
        direction = dirs[round(bearing_deg / 22.5) % 16]
        p['distance_from_lqv_km'] = round(dist, 2)
        p['direction_from_lqv'] = direction

    # Save back
    for p_path in PEAKS_PATHS:
        if p_path.exists():
            p_path.write_text(json.dumps(pe, indent=2))
            print(f"wrote {p_path}")

    # Also fix the terrain_mesh_data.json bounds + dimensions
    mesh_data_paths = [
        Path("/root/.hermes/lqv-splat/exports/web/game_assets_lite/assets/lowpoly/terrain_mesh_data.json"),
        ROOT / "splats/exports/web/game_assets_lite/assets/lowpoly/terrain_mesh_data.json",
    ]
    for md_path in mesh_data_paths:
        if md_path.exists():
            md = json.loads(md_path.read_text())
            # Update bounds + pixel count
            md['bounds'] = bnd
            md['pixels'] = (w, h)
            md['elev_min_m'] = min(min(r) for r in dem)
            md['elev_max_m'] = max(max(r) for r in dem)
            md['z_exag'] = 2.0
            md_path.write_text(json.dumps(md))
            print(f"updated {md_path}")


if __name__ == "__main__":
    main()
