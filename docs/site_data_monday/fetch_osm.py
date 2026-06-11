"""Pull OSM rivers, forest, buildings, paths for the Monday AOI.
Overpass API is free; we use the [out:json] endpoint.
"""
import requests, json
from AOI import BBOX

# tighter bbox for OSM
W, S, E, N = BBOX
Q = f"""
[out:json][timeout:120];
(
  way["waterway"="river"]({S},{W},{N},{E});
  way["waterway"="stream"]({S},{W},{N},{E});
  way["waterway"="rapids"]({S},{W},{N},{E});
  way["waterway"="waterfall"]({S},{W},{N},{E});
  way["natural"="water"]({S},{W},{N},{E});
  relation["natural"="water"]({S},{W},{N},{E});
  way["natural"="wood"]({S},{W},{N},{E});
  way["landuse"="forest"]({S},{W},{N},{E});
  way["landuse"="reservoir"]({S},{W},{N},{E});
  way["leisure"="park"]({S},{W},{N},{E});
  way["boundary"="protected_area"]({S},{W},{N},{E});
  way["highway"]({S},{W},{N},{E});
  way["building"]({S},{W},{N},{E});
  way["bridge"]({S},{W},{N},{E});
  way["tourism"]({S},{W},{N},{E});
);
out geom;
"""
print(f"Querying Overpass for bbox W={W:.4f} S={S:.4f} E={E:.4f} N={N:.4f}...")
r = requests.post("https://overpass-api.de/api/interpreter", data=Q.encode("utf-8"), timeout=180)
r.raise_for_status()
data = r.json()

# summary by tag
tag_counts = {}
for el in data.get("elements", []):
    tags = el.get("tags", {})
    for k in tags:
        tag_counts.setdefault(k, 0)
        tag_counts[k] += 1
print(f"Got {len(data['elements'])} elements, {len(tag_counts)} tag types")
top = sorted(tag_counts.items(), key=lambda x: -x[1])[:25]
for k, v in top:
    print(f"  {k:30s}  {v}")

with open("osm/overpass_monday.json", "w") as f:
    json.dump(data, f)
print(f"\nSaved osm/overpass_monday.json ({len(json.dumps(data))//1024} KB)")
