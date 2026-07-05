"""Combine the 4 sources of water/creek/stream/river/etc data into
one GeoJSON the viewer can show as a single toggle.

Sources (each uniquely tagged for traceability):
  1. OSM waterways (LineString)  — verified mapper ground-truth
  2. DEM quebrada streams (LineString) — model-derived D8 + flow-accum
  3. JRC GSW polygons — satellite-detected standing water bodies
  4. OSM water polygons — audited into 11 categories

Output:
  splats/exports/web/data/water_combined_20km.geojson
    - Every feature carries properties.source = one of the above
    - Every feature carries properties.category = ... clean taxonomy
    - Polygons + LineStrings in the same file (the viewer styles them
      differently based on geometry type + class)
"""
from __future__ import annotations

import json
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone

ROOT = Path("/root/la-quebrada-viva")
OUT = ROOT / "splats/exports/web/data"
OUT.mkdir(parents=True, exist_ok=True)

# Master class taxonomy — used by viewer styles AND displayed in sidebar
# legend. Single source of truth shared across both polygon + line layers.
WATER_FAMILY = {
    # LineString classes
    "main_river":        {"kind": "line",   "color": "#0c4a6e", "width": 3.5,
                          "label": "Main river (≥ 25 km² catchment, DEM)",
                          "priority": 0},
    "river":             {"kind": "line",   "color": "#1d4ed8", "width": 3,
                          "label": "River (OSM waterway=river)",
                          "priority": 1},
    "tributary":         {"kind": "line",   "color": "#3b82f6", "width": 2.2,
                          "label": "Tributary (5–25 km², DEM)",
                          "priority": 2},
    "creek":             {"kind": "line",   "color": "#60a5fa", "width": 1.6,
                          "label": "Creek (1–5 km², DEM)",
                          "priority": 3},
    "rill":              {"kind": "line",   "color": "#93c5fd", "width": 1,
                          "label": "Rill (< 1 km², DEM)",
                          "priority": 4},
    "stream":            {"kind": "line",   "color": "#7dd3fc", "width": 1.4,
                          "label": "Stream (OSM waterway=stream)",
                          "priority": 4},
    "tidal_channel":     {"kind": "line",   "color": "#a3e635", "width": 1.4,
                          "label": "Tidal channel (OSM)",
                          "priority": 6},
    "canal":             {"kind": "line",   "color": "#2563eb", "width": 1.4,
                          "label": "Canal (OSM)",
                          "priority": 5},
    "ditch":             {"kind": "line",   "color": "#fb923c", "width": 0.8,
                          "label": "Ditch / drain (OSM)",
                          "priority": 7},
    "dam":               {"kind": "line",   "color": "#94a3b8", "width": 1,
                          "label": "Dam (OSM)",
                          "priority": 8},

    # Polygon classes
    "verified_lake":            {"kind": "poly", "color": "#0ea5e9", "fill_opacity": 0.75,
                                "label": "Verified lake (JRC ≥ 50%)", "priority": 0},
    "verified_wetland":         {"kind": "poly", "color": "#0369a1", "fill_opacity": 0.7,
                                "label": "Verified wetland (JRC 20–50%)", "priority": 1},
    "seasonal_wetland":         {"kind": "poly", "color": "#67e8f9", "fill_opacity": 0.5,
                                "label": "Seasonal wetland (JRC 10–20%)", "priority": 2},
    "stream_riparian_pool":     {"kind": "poly", "color": "#7dd3fc", "fill_opacity": 0.55,
                                "label": "Stream riparian pool (within 200 m of a stream)",
                                "priority": 3},
    "river_corridor_polygon":   {"kind": "poly", "color": "#1d4ed8", "fill_opacity": 0.5,
                                "label": "River corridor polygon (OSM natural=water water=river)",
                                "priority": 4},
    "reservoir_polygon":        {"kind": "poly", "color": "#1e40af", "fill_opacity": 0.55,
                                "label": "Reservoir / farm dam (OSM)",
                                "priority": 5},
    "pond_polygon_depiction":   {"kind": "poly", "color": "#c4b5fd", "fill_opacity": 0.45,
                                "label": "Pond / basin (OSM, not JRC-verified)",
                                "priority": 6},
    "stream_polygon_depiction": {"kind": "poly", "color": "#a78bfa", "fill_opacity": 0.35,
                                "label": "Stream centreline as polygon (OSM water=stream)",
                                "priority": 7},
    "dry_depression":           {"kind": "poly", "color": "#fbbf24", "fill_opacity": 0.35,
                                "label": "Dry depression (OSM wetland, flat, no water)",
                                "priority": 8},
    "likely_mis-tagged":        {"kind": "poly", "color": "#f87171", "fill_opacity": 0.4,
                                "label": "Likely mis-tagged (steep + JRC < 5%)",
                                "priority": 9},
    "unclassified":             {"kind": "poly", "color": "#94a3b8", "fill_opacity": 0.25,
                                "label": "Unclassified OSM water polygon",
                                "priority": 99},
}


def _audit_class_to_category(audit_class: str) -> str:
    """Map audit classification → shared category taxonomy key."""
    return audit_class   # already shared


def main():
    print("Combining 4 water-data sources into single GeoJSON...")
    features = []
    sources = Counter()

    # 1. OSM waterways (LineString)
    audit = json.load(open(OUT / "surface_water_20km.geojson"))
    for f in audit["features"]:
        g = f["geometry"]
        if g["type"] not in ("LineString", "MultiLineString"):
            continue
        cls = f["properties"].get("audit_class", "ditch")
        meta = WATER_FAMILY.get(cls, WATER_FAMILY["ditch"])
        # OSM drainage class has same priority as creek/tributary
        new_props = dict(f["properties"])
        new_props["category"] = cls
        new_props["source"] = "osm_waterway"
        new_props["class_label"] = meta["label"]
        new_props["color"] = meta["color"]
        new_props["width"] = meta["width"]
        new_props["draw_priority"] = meta["priority"]
        features.append({
            "type": "Feature",
            "properties": new_props,
            "geometry": g,
        })
        sources["osm_waterway"] += 1

    # 2. DEM quebrada streams (LineString)
    dem_streams = json.load(open(OUT / "dem_streams_20km.geojson"))
    for f in dem_streams["features"]:
        g = f["geometry"]
        if g["type"] != "LineString":
            continue
        cls = f["properties"]["class"]
        # Translate internal cls → shared categories
        cls_map = {"main": "main_river", "tributary": "tributary",
                   "headwater": "creek"}  # legacy "headwater" → "creek"
        shared = cls_map.get(cls, cls)
        meta = WATER_FAMILY[shared]
        new_props = dict(f["properties"])
        new_props["category"] = shared
        new_props["source"] = "dem_streams"
        new_props["class_label"] = meta["label"]
        new_props["color"] = meta["color"]
        new_props["width"] = meta["width"]
        new_props["draw_priority"] = meta["priority"]
        features.append({
            "type": "Feature",
            "properties": new_props,
            "geometry": g,
        })
        sources["dem_streams"] += 1

    # 3. JRC GSW water bodies (Polygon)
    jrc = json.load(open(OUT / "lqv_jrc_waterbodies_20km.geojson"))
    for f in jrc["features"]:
        new_props = dict(f["properties"])
        audit_class = new_props.get("audit_class", "seasonal")
        # Map JRC's own classes
        cls_map = {
            "persistent": "verified_lake",
            "seasonal":   "verified_wetland",
            "rare":       "seasonal_wetland",
        }
        shared = cls_map.get(audit_class, "verified_wetland")
        meta = WATER_FAMILY[shared]
        new_props["category"] = shared
        new_props["source"] = "jrc_gsw"
        new_props["class_label"] = meta["label"]
        new_props["color"] = meta["color"]
        new_props["fill_opacity"] = meta["fill_opacity"]
        new_props["draw_priority"] = meta["priority"]
        features.append({
            "type": "Feature",
            "properties": new_props,
            "geometry": f["geometry"],
        })
        sources["jrc_gsw"] += 1

    # 4. OSM audited water polygons (Polygon)
    for f in audit["features"]:
        if f["geometry"]["type"] != "Polygon":
            continue
        cls = f["properties"].get("audit_class", "unclassified")
        meta = WATER_FAMILY.get(cls, WATER_FAMILY["unclassified"])
        new_props = dict(f["properties"])
        new_props["category"] = cls
        new_props["source"] = "osm_polygon"
        new_props["class_label"] = meta["label"]
        new_props["color"] = meta["color"]
        new_props["fill_opacity"] = meta["fill_opacity"]
        new_props["draw_priority"] = meta["priority"]
        features.append({
            "type": "Feature",
            "properties": new_props,
            "geometry": f["geometry"],
        })
        sources["osm_polygon"] += 1

    # Sort: low priority (more important) first, then lines before polys
    # so draw call order is: rivers under polygons
    def sort_key(f):
        p = f["properties"]
        return (
            # main rivers at the bottom underneath so lakes overlay nicely
            p.get("draw_priority", 99),
            0 if f["geometry"]["type"] == "LineString" else 1,
        )
    features.sort(key=sort_key)

    # Assign stable feature IDs
    for i, f in enumerate(features):
        f.setdefault("properties", {})["feature_id"] = f"lqv-wat-{i:05d}"

    fc = {
        "type": "FeatureCollection",
        "name": "water_combined_20km",
        "metadata": {
            "schema_version": 1,
            "bbox": list(audit["metadata"]["bbox"]),
            "family_taxonomy": WATER_FAMILY,
            "source_counts": dict(sources),
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "feature_count": len(features),
        },
        "features": features,
    }
    out_path = OUT / "water_combined_20km.geojson"
    out_path.write_text(json.dumps(fc, separators=(",", ":")))
    print(f"wrote {out_path}")
    print(f"  total: {len(features):,} features")
    for k, v in sources.items():
        print(f"  {v:>5}  from {k}")


if __name__ == "__main__":
    main()
