"""Pull cloud-free Sentinel-2 L2A RGB + NIR composites for the Monday AOI.
Free via Element84 Earth Search STAC (no auth).
We'll grab the lowest-cloud scene from the last 12 months.
"""
import os, sys, json
import pystac_client
import requests
from AOI import BBOX

CAT = "https://earth-search.aws.element84.com/v1"
cat = pystac_client.Client.open(CAT)

print("Searching Sentinel-2 L2A for Monday AOI 2025-06 to 2026-06...")
search = cat.search(
    collections=["sentinel-2-l2a"],
    bbox=list(BBOX),
    datetime="2025-06-11/2026-06-11",
    query={"eo:cloud_cover": {"lt": 10}, "platform": {"eq": "Sentinel-2A"}},
    max_items=20,
)
items = sorted(search.items(), key=lambda x: x.properties.get("eo:cloud_cover", 100))
print(f"Found {len(items)} scenes")
for it in items[:5]:
    cc = it.properties.get("eo:cloud_cover", "?")
    dt = it.properties.get("datetime", "?")
    print(f"  {dt[:10]}  cloud {cc:>4}%  {it.id}")

if not items:
    sys.exit("no scenes")

best = items[0]
print(f"\nUsing scene: {best.id} (cc {best.properties.get('eo:cloud_cover')}%)")

bands = ["red", "green", "blue", "nir", "scl"]
asset_urls = {b: best.assets[b].href for b in bands}
for b, u in asset_urls.items():
    print(f"  {b}: {u[:80]}...")

# download 10m RGB + 20m NIR + SCL
os.makedirs("sentinel2", exist_ok=True)
for b in ["red", "green", "blue", "nir", "scl"]:
    u = asset_urls[b]
    out = f"sentinel2/{best.id}_{b}.tif"
    if not os.path.exists(out):
        print(f"  downloading {b}...")
        with requests.get(u, stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(out, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
    print(f"  -> {out} ({os.path.getsize(out)//1024} KB)")

# save the scene metadata
with open(f"sentinel2/{best.id}_metadata.json", "w") as f:
    json.dump(dict(best.properties), f, indent=2)
print(f"\nScene: {best.id}  date: {best.properties.get('datetime')}  cloud: {best.properties.get('eo:cloud_cover')}%")
