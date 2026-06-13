#!/usr/bin/env python3
import json,sys,urllib.request,urllib.error
from datetime import datetime

URLS=[
  "https://earth-search.aws.element84.com/v1/search",
  "https://explore.imagery.coop/stac/search",
  "https://datahub.radiant.earth/stac/search",
  "https://catalogue.digitalearth.africa/stac/search",
]
PAYLOAD={"collections":["sentinel-2-l2a"],"bbox":[-57.045,-25.645,-57.015,-25.615],"datetime":"2024-01-01T00:00:00Z/2026-06-11T23:59:59Z","limit":3}

def probe(url):
    body=json.dumps(PAYLOAD).encode()
    req=urllib.request.Request(url,data=body,
        headers={"Content-Type":"application/json","User-Agent":"house-field/test_stac.py"},
        method="POST")
    try:
        with urllib.request.urlopen(req,timeout=30) as r: return r.status, r.read(2048).decode(errors="replace")
    except urllib.error.HTTPError as e: return e.code, e.read(1024).decode(errors="replace")
    except urllib.error.URLError as e: return 0, str(e.reason)

def main():
    print("STAC Endpoint Diagnosis")
    working=[]
    for url in URLS:
        print(f"Testing: {url}")
        s,b=probe(url); print(f"  Status: {s}"); print(f"  Body: {b[:300]!r}")
        if 200<=s<300: working.append(url)
    print(f"Working: {working if working else 'none'}")
    if not working: sys.exit(1)

if __name__=="__main__": main()
