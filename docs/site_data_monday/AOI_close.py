"""Tight AOI: 600 m radius from the real OSM-mapped Saltos del Monday node.
Center: -25.5627515, -54.6323698 (OSM node 4218536799, height=40m, Q880046).
Sized to fit the falls + Parque Municipal + a 1-house footprint for scale.
"""
import math
from pyproj import Transformer

CENTER_LAT = -25.5627515
CENTER_LON = -54.6323698
RADIUS_M   = 600
BBOX_W = CENTER_LON - (RADIUS_M / (111000.0 * math.cos(math.radians(abs(CENTER_LAT)))))
BBOX_E = CENTER_LON + (RADIUS_M / (111000.0 * math.cos(math.radians(abs(CENTER_LAT)))))
BBOX_S = CENTER_LAT - (RADIUS_M / 111000.0)
BBOX_N = CENTER_LAT + (RADIUS_M / 111000.0)
BBOX = (BBOX_W, BBOX_S, BBOX_E, BBOX_N)

_t = Transformer.from_crs("EPSG:4326", "EPSG:32721", always_xy=True)
CE_UTM, CN_UTM = _t.transform(CENTER_LON, CENTER_LAT)

if __name__ == "__main__":
    print(f"Center (OSM node 4218536799): {CENTER_LAT}, {CENTER_LON}")
    print(f"600m AOI bbox WGS84 (W,S,E,N): {BBOX}")
    print(f"UTM 21J center: E={CE_UTM:.1f} N={CN_UTM:.1f}")
    print(f"Bbox size: {2*RADIUS_M} m × {2*RADIUS_M} m")
    print(f"  -> 1200m × 1200m (~1.44 km²)")
    print(f"  -> 4 terraces wide, 3 falls wide. 1 standard house = 8-10m footprint = 0.013% of width")
