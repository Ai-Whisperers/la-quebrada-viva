"""Tight 2km AOI centered on the real OSM Saltos del Monday node.
Center: -25.5627515, -54.6323698 (OSM node 4218536799, height 40m, Q880046).
Box: 2 km × 2 km (1 km radius) — covers the falls + Parque Municipal + the 120m cliff face
in detail, with a small buffer for the urban edge.
"""
import math
from pyproj import Transformer

CENTER_LAT = -25.5627515
CENTER_LON = -54.6323698
RADIUS_M   = 1000  # 2 km × 2 km box
BBOX_W = CENTER_LON - (RADIUS_M / (111000.0 * math.cos(math.radians(abs(CENTER_LAT)))))
BBOX_E = CENTER_LON + (RADIUS_M / (111000.0 * math.cos(math.radians(abs(CENTER_LAT)))))
BBOX_S = CENTER_LAT - (RADIUS_M / 111000.0)
BBOX_N = CENTER_LAT + (RADIUS_M / 111000.0)
BBOX = (BBOX_W, BBOX_S, BBOX_E, BBOX_N)

_t = Transformer.from_crs("EPSG:4326", "EPSG:32721", always_xy=True)
CE_UTM, CN_UTM = _t.transform(CENTER_LON, CENTER_LAT)

# Real OSM IDs for traceability
OSM_WATERFALL_NODE = 4218536799
OSM_CLIFF_WAY      = 543393748
OSM_HEIGHT_M       = 40
OSM_WIKIDATA       = "Q880046"

if __name__ == "__main__":
    print(f"Center (OSM node {OSM_WATERFALL_NODE}): {CENTER_LAT}, {CENTER_LON}")
    print(f"  height={OSM_HEIGHT_M}m  wikidata={OSM_WIKIDATA}")
    print(f"  cliff way: {OSM_CLIFF_WAY}")
    print(f"2km AOI bbox WGS84 (W,S,E,N): {BBOX}")
    print(f"UTM 21J center: E={CE_UTM:.1f} N={CN_UTM:.1f}")
    print(f"Bbox size: {2*RADIUS_M} m × {2*RADIUS_M} m (~{4*RADIUS_M*RADIUS_M/1e6:.2f} km²)")
    print(f"Cliff is at ~ 25.5620-25.5629S, 54.6320-54.6324W = 100m x 50m, all inside the AOI")
