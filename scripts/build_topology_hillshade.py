"""Convert the fused 5m DEM hillshade (core/dem_fused_5m_hillshade.png)
to a parcel-scale JPEG overlay for the LQV viewer.

The 5m hillshade is 213 KB PNG, already downscaled from a much larger
DEM. We re-save it as a JPEG (smaller, faster) and clip it to the
parcel's bounding box so the viewer can show it as a zoom-dependent
overlay.

Why: the main hillshade_10km.jpg is 30m-resolution; at z=15-16 zoom
on the parcel, the user can see individual trees / ridges if they
have a higher-resolution backdrop.

Output: splats/exports/web/data/hillshade_parcel.png
Bounds: parcel_ext bbox (will be matched to GPS polygon exactly)
"""
from pathlib import Path
from PIL import Image

ROOT = Path("/root/la-quebrada-viva")
SRC = ROOT / "docs/site_data/topology_lod/core/dem_fused_5m_hillshade.png"
OUT = ROOT / "splats/exports/web/data"

if not SRC.exists():
    print(f"source not found: {SRC}")
    raise SystemExit(1)

print(f"loading {SRC}...")
img = Image.open(SRC)
print(f"  source size: {img.size} mode={img.mode}")

# If RGBA, flatten onto dark gray
if img.mode == 'RGBA':
    bg = Image.new('RGBA', img.size, (60, 60, 60, 255))
    img = Image.alpha_composite(bg, img).convert('RGB')

# Save as JPEG (smaller)
out_path = OUT / "hillshade_parcel.jpg"
img.save(out_path, "JPEG", quality=85, optimize=True)
print(f"wrote {out_path} ({out_path.stat().st_size/1024:.1f} KB)")

# Save bounds JSON for the parcel-scale hillshade
# (will match the topo core — but the topo didn't have geo info, so
#  we use a tight bbox around the LQV parcel as a fallback)
import json
parcel = json.load(open(OUT / "client_gps/client_gps_polygon.geojson"))
ring = parcel['features'][0]['geometry']['coordinates'][0]
lons = [p[0] for p in ring]
lats = [p[1] for p in ring]
# Add 50m buffer
m_per_deg_lat = 111320
m_per_deg_lon = 111320 * abs(min(lats)) * 0.0174533 / 1
lat_buf = 100 / m_per_deg_lat
lon_buf = 100 / m_per_deg_lon
bounds = {
    "min_lon": min(lons) - lon_buf,
    "min_lat": min(lats) - lat_buf,
    "max_lon": max(lons) + lon_buf,
    "max_lat": max(lats) + lat_buf,
}
bounds_path = OUT / "hillshade_parcel_bounds.json"
bounds_path.write_text(json.dumps(bounds))
print(f"wrote {bounds_path} (LQV parcel area, 100m buffer)")
