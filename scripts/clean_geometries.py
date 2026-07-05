"""Clean up LineString/MultiLineString geometries in the deployed GeoJSON
files. The dem_streams_20km.geojson had 537 invalid geometries because
the streaming tracing produced paths with the same start and end point
(no movement), which shapely rejects.

Drop any geometry component with fewer than 2 points; emit as a clean
LineString if exactly one valid component remains, otherwise a
MultiLineString. Also clip to the 20 km box.
"""
import json
from pathlib import Path
import sys
from shapely.geometry import shape, mapping, LineString, MultiLineString
from shapely.validation import make_valid
from shapely.ops import unary_union

BBOX = box_wsen = (-57.231502, -25.787336, -56.839502, -25.427336)  # W, S, E, N
from shapely.geometry import box
BBOX_BOX = box(*BBOX)

FILES = [
    "dem_streams_20km.geojson",
    "dem_streams_arrows_20km.geojson",
    "dem_contours_20km.geojson",
    "water_combined_20km.geojson",
    "surface_water_20km.geojson",
    "osm_20km/pois.geojson",
    "osm_20km/trees.geojson",
    "osm_20km/buildings.geojson",
    "osm_20km/places.geojson",
    "osm_20km/water.geojson",
    "osm_20km/waterways.geojson",
    "osm_20km/landuse.geojson",
    "osm_20km/roads.geojson",
]

ROOT = Path("/root/la-quebrada-viva/splats/exports/web/data")


def clean_geom(g, allow_points=False):
    """Repair and clean geometry. Returns (cleaned_geom, kept_in_bbox_bool).
    Set allow_points=True for arrow/POI files where Point geometries are valid."""
    if not g.is_valid:
        g = make_valid(g)
    if g.is_empty:
        return None, False
    # Clip to 20 km box
    try:
        clipped = g.intersection(BBOX_BOX)
    except Exception:
        clipped = g
    if clipped.is_empty:
        return None, False
    # Extract only desired components
    components = []
    gtype = clipped.geom_type
    if gtype == "LineString":
        if len(clipped.coords) >= 2:
            components = [clipped]
    elif gtype == "MultiLineString":
        components = [c for c in clipped.geoms if c.geom_type == "LineString"
                      and len(c.coords) >= 2]
    elif gtype == "Point" and allow_points:
        components = [clipped]
    elif gtype == "MultiPoint" and allow_points:
        components = [c for c in clipped.geoms]
    elif gtype == "Polygon" and allow_points:
        components = [clipped]
    elif gtype == "MultiPolygon" and allow_points:
        components = [c for c in clipped.geoms if c.geom_type == "Polygon"
                      and c.area > 0]
    elif gtype == "GeometryCollection":
        for c in clipped.geoms:
            if c.geom_type == "LineString" and len(c.coords) >= 2:
                components.append(c)
            elif allow_points and c.geom_type in ("Point", "Polygon"):
                components.append(c)
    if not components:
        return None, False
    if len(components) == 1:
        return components[0], True
    if all(c.geom_type == "LineString" for c in components):
        return MultiLineString(components), True
    # Mixed types — return first valid
    return components[0], True


def clean_file(path, allow_points=False):
    print(f"=== {path.name} ===")
    d = json.load(open(path))
    feats = d['features']
    before_invalid = 0
    before_oob = 0
    after_invalid = 0
    after_oob = 0
    kept = []
    for f in feats:
        g = shape(f['geometry'])
        if not g.is_valid:
            before_invalid += 1
        if not g.intersects(BBOX_BOX):
            before_oob += 1
        cleaned, in_box = clean_geom(g, allow_points=allow_points)
        if cleaned is None or not in_box:
            after_oob += 1
            continue
        if not cleaned.is_valid:
            after_invalid += 1
            continue
        f['geometry'] = mapping(cleaned)
        kept.append(f)
    d['features'] = kept
    out = path
    out.write_text(json.dumps(d, separators=(",", ":")))
    print(f"  before: invalid={before_invalid}  oob={before_oob}")
    print(f"  after:  invalid={after_invalid}  oob={after_oob}")
    print(f"  kept:   {len(kept)}/{len(feats)}")
    print(f"  size:   {out.stat().st_size/1024/1024:.2f} MB")


def main():
    # Line-only files (no Points)
    for name in [
        "dem_streams_20km.geojson",
        "dem_contours_20km.geojson",
        "water_combined_20km.geojson",
        "osm_20km/waterways.geojson",
        "osm_20km/roads.geojson",
    ]:
        p = ROOT / name
        if p.exists():
            clean_file(p, allow_points=False)
        else:
            print(f"  ! {p} not found")
    # Mixed files (Points allowed for arrows, POIs, etc.)
    for name in [
        "dem_streams_arrows_20km.geojson",
        "surface_water_20km.geojson",
        "osm_20km/pois.geojson",
        "osm_20km/trees.geojson",
        "osm_20km/buildings.geojson",
        "osm_20km/places.geojson",
        "osm_20km/water.geojson",
        "osm_20km/landuse.geojson",
    ]:
        p = ROOT / name
        if p.exists():
            clean_file(p, allow_points=True)
        else:
            print(f"  ! {p} not found")


if __name__ == "__main__":
    main()