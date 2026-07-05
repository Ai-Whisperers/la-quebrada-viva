"""Add accurate WGS84 area_ha to GeoJSON polygons using pyproj.Geod."""
import json
import sys
from pathlib import Path
from shapely.geometry import shape
from pyproj import Geod

geod = Geod(ellps="WGS84")


def add_area(path):
    d = json.load(open(path))
    n = 0
    for f in d['features']:
        g = shape(f['geometry'])
        try:
            area_m2, _ = geod.geometry_area_perimeter(g)
            f['properties']['area_ha'] = round(abs(area_m2) / 10000, 2)
            n += 1
        except Exception:
            f['properties']['area_ha'] = 0
    Path(path).write_text(json.dumps(d, separators=(',', ':')))
    print(f"  {path}: {n} polygons updated")


if __name__ == "__main__":
    files = sys.argv[1:] or [
        'splats/exports/web/data/mapbiomas_2023_10km.geojson',
        'splats/exports/web/data/woodland_merged_10km.geojson',
        'splats/exports/web/data/surface_water_10km.geojson',
    ]
    for f in files:
        if Path(f).exists():
            add_area(f)