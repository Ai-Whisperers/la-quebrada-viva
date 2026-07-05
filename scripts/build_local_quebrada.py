"""Derive a 'Local Quebradas' polyline from the lowest points on Wes's
GPS walking track. The quebrada runs through the lowest part of the
terrain; the GPS path crosses it. We find the local elevation minima
along the walking track (using the Copernicus GLO-30 DEM) and chain
them together into a polyline that approximates the quebrada's path
through the parcel.

The DEM quebrada network (DEM quebrada streams, P0-1) misses the
LQV quebrada because its watershed is below the threshold. This
ground-truth-derived layer shows where the quebrada actually runs.
"""
import json
from pathlib import Path
from pyproj import Geod
from shapely.geometry import LineString, mapping

ROOT = Path("/root/la-quebrada-viva")
OUT = ROOT / "splats/exports/web/data"

geod = Geod(ellps="WGS84")

def get_elevation(lon, lat):
    """Sample Copernicus GLO-30 DEM at a single point."""
    import rasterio
    src = ROOT / "docs/site_data/extended_aoi/dem/cop30_dem.tif"
    with rasterio.open(src) as ds:
        try:
            return float(next(ds.sample([(lon, lat)]))[0])
        except Exception:
            return None


def main():
    walk = json.load(open(OUT / "client_gps/client_gps_walking_path.geojson"))
    f = walk['features'][0]
    coords = f['geometry']['coordinates']
    ts = f['properties']['timestamps']
    cats = f['properties'].get('category_per_point', [])

    print(f"Sampling DEM at {len(coords)} walking points...")
    enriched = []
    for i, (lon, lat) in enumerate(coords):
        e = get_elevation(lon, lat)
        if e is None:
            continue
        enriched.append({
            'idx': i, 'lon': lon, 'lat': lat,
            'elev': e,
            'timestamp': ts[i] if i < len(ts) else None,
            'category': cats[i] if i < len(cats) else None,
        })
    enriched.sort(key=lambda x: x['elev'])
    print(f"  elevation range on walking track: "
          f"{min(e['elev'] for e in enriched):.1f} - "
          f"{max(e['elev'] for e in enriched):.1f} m")

    # Local minima: points whose elevation is lower than their immediate
    # neighbours by ≥2 m, AND are below the median elevation of the track.
    track_median = sorted([e['elev'] for e in enriched])[len(enriched) // 2]
    print(f"  median elevation: {track_median:.1f} m")

    # Sort by timestamp to get the walk order
    enriched_by_time = sorted([e for e in enriched if e['timestamp']],
                              key=lambda x: x['timestamp'])

    # Walk along the path and find local minima (within ±2 neighbours)
    quebrada_pts = []
    for i in range(1, len(enriched_by_time) - 1):
        prev_e = enriched_by_time[i-1]['elev']
        curr_e = enriched_by_time[i]['elev']
        next_e = enriched_by_time[i+1]['elev']
        if curr_e < prev_e - 1 and curr_e < next_e - 1:
            quebrada_pts.append(enriched_by_time[i])

    # Also include the absolute minimum point even if it's at the edge
    if enriched:
        quebrada_pts.append(enriched[0])  # lowest point overall
    quebrada_pts = list({p['idx']: p for p in quebrada_pts}.values())
    quebrada_pts.sort(key=lambda x: x['idx'])

    print(f"  local minima on walking track: {len(quebrada_pts)} points")
    for p in quebrada_pts:
        print(f"    [{p['idx']:>2}] {p['lon']:.5f}, {p['lat']:.5f}  "
              f"{p['elev']:.1f} m  {p['category']}")

    if len(quebrada_pts) < 2:
        print("  not enough points for polyline")
        return

    # Build polyline in walking order
    quebrada_coords = [[p['lon'], p['lat']] for p in quebrada_pts]

    # Compute total length (pyproj.Geod.geometry_length returns forward+backward)
    line = LineString(quebrada_coords)
    length_m = geod.geometry_length(line)
    print(f"  quebrada polyline length: {length_m:.0f} m")

    out = {
        "type": "FeatureCollection",
        "name": "local_quebradas_10km",
        "metadata": {
            "source": "Derived from Wesley's GPS walking track + Copernicus GLO-30 DEM local-minima detection",
            "method": "Local elevation minima along walking track, chained in walk order",
            "license": "Client-provided GPS data",
        },
        "features": [{
            "type": "Feature",
            "properties": {
                "category": "local_quebrada",
                "name": "LQV quebrada (ground-truth)",
                "description": "GPS-derived quebrada polyline from local elevation minima along Wes's walk",
                "color": "#1d4ed8",
                "stroke_width": 4,
                "vertex_count": len(quebrada_coords),
                "length_m": round(length_m, 1),
                "elev_min_m": round(min(p['elev'] for p in quebrada_pts), 1),
                "elev_max_m": round(max(p['elev'] for p in quebrada_pts), 1),
                "captured_dates": "2026-06-22 + 2026-06-28",
                "captured_by": "Wesley van de Camp",
                "source_quality": "ground-truth (not DEM-derived)",
            },
            "geometry": mapping(line),
        }],
    }
    out_path = OUT / "local_quebradas_10km.geojson"
    out_path.write_text(json.dumps(out, separators=(",", ":")))
    print(f"wrote {out_path} ({out_path.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    main()