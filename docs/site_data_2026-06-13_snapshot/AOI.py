"""Cataratas del Monday — AOI constants.
Center: -25.561944, -54.631389 (WGS84)
3 main drops, 40m height, 120m wide, basaltic bedrock.
AOI: 6 km × 6 km tight box (3 km radius from cascade center).
"""
import math
from pyproj import Transformer

CENTER_LAT = -25.561944
CENTER_LON = -54.631389
RADIUS_M = 3000
BBOX_W = CENTER_LON - (RADIUS_M / (111000.0 * math.cos(math.radians(abs(CENTER_LAT)))))
BBOX_E = CENTER_LON + (RADIUS_M / (111000.0 * math.cos(math.radians(abs(CENTER_LAT)))))
BBOX_S = CENTER_LAT - (RADIUS_M / 111000.0)
BBOX_N = CENTER_LAT + (RADIUS_M / 111000.0)
BBOX = (BBOX_W, BBOX_S, BBOX_E, BBOX_N)  # W,S,E,N (GeoJSON)

_t = Transformer.from_crs("EPSG:4326", "EPSG:32721", always_xy=True)
CE_UTM, CN_UTM = _t.transform(CENTER_LON, CENTER_LAT)

if __name__ == "__main__":
    print(f"Center: {CENTER_LAT}, {CENTER_LON}")
    print(f"3km AOI bbox WGS84 (W,S,E,N): {BBOX}")
    print(f"UTM 21J center: E={CE_UTM:.1f} N={CN_UTM:.1f}")
    print(f"Bbox size: {2*RADIUS_M} m × {2*RADIUS_M} m")
