"""Fetch Wikimedia Commons close-up photos of Saltos del Monday for Blender reference."""
import os, requests
from urllib.parse import unquote

# 1) Find all files in the category
cat_url = "https://commons.wikimedia.org/w/api.php"
files = []
cmcontinue = None
while True:
    p = {
        "action": "query", "list": "categorymembers", "cmtitle": "Category:Saltos del Monday",
        "cmtype": "file", "cmlimit": 50, "format": "json",
    }
    if cmcontinue: p["cmcontinue"] = cmcontinue
    r = requests.get(cat_url, params=p, timeout=30, headers={"User-Agent": "ai-whisperers/1.0"})
    d = r.json()
    files.extend(m["title"] for m in d.get("query", {}).get("categorymembers", []))
    if "continue" not in d: break
    cmcontinue = d["continue"]["cmcontinue"]
print(f"Category 'Saltos del Monday' has {len(files)} files:")
for f in files: print(f"  {f}")

# Also do a search for "Cataratas del Monday" (alt name)
for srch in ["Cataratas del Monday", "Monday Falls", "Saltos Monday", "Tape Aviru Monday"]:
    p = {"action":"query","list":"search","srsearch":f'"{srch}" filetype:bitmap','srnamespace':6, 'srlimit':20, "format":"json"}
    r = requests.get(cat_url, params=p, timeout=30, headers={"User-Agent":"ai-whisperers/1.0"})
    d = r.json()
    for hit in d.get("query",{}).get("search",[]):
        if hit["title"] not in files:
            files.append(hit["title"])
            print(f"  + search[{srch}]: {hit['title']}")

# 2) Get image URLs for each file
for f in files:
    p = {
        "action": "query", "titles": f, "prop": "imageinfo", "iiprop": "url|size|mime",
        "format": "json",
    }
    r = requests.get(cat_url, params=p, timeout=30, headers={"User-Agent": "ai-whisperers/1.0"})
    d = r.json()
    for pg in d.get("query",{}).get("pages",{}).values():
        for info in pg.get("imageinfo",[]):
            url = info["url"]
            mime = info.get("mime", "")
            w = info.get("width", 0)
            h = info.get("height", 0)
            if not (mime.startswith("image/")): continue
            safe = unquote(f.replace("File:", "")).replace("/", "_")
            out = f"references/photos/{safe}"
            if not os.path.exists(out):
                print(f"  downloading {f}  {w}x{h}  {url[:80]}...")
                try:
                    img = requests.get(url, timeout=60, headers={"User-Agent":"ai-whisperers/1.0"})
                    if img.status_code == 200 and len(img.content) > 1000:
                        with open(out, "wb") as fh: fh.write(img.content)
                        sz = os.path.getsize(out)
                        print(f"    -> {out}  {sz//1024} KB")
                except Exception as e:
                    print(f"    FAIL: {e}")
            else:
                print(f"  cached {f}")

# 3) Also pull the dedicated page
for url in ["https://commons.wikimedia.org/wiki/Saltos_del_Monday"]:
    try:
        r = requests.get(url, timeout=30, headers={"User-Agent":"ai-whisperers/1.0"})
        with open("references/commons_saltos_del_monday_page.html","w") as f: f.write(r.text)
        print(f"saved {url}")
    except Exception as e: print(f"FAIL {url}: {e}")
