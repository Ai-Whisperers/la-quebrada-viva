#!/usr/bin/env python3
"""Liveness probe for STAC endpoints we depend on.

Useful when ``fetch_sentinel2.py`` returns 0 scenes — often the endpoint
is down rather than the AOI being wrong. Prints status code + first
2 KB of response body per endpoint.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

from scripts.satellite._aoi import aoi_bbox

URLS = [
    "https://earth-search.aws.element84.com/v1/search",
    "https://planetarycomputer.microsoft.com/api/stac/v1/search",
    "https://explore.imagery.coop/stac/search",
    "https://datahub.radiant.earth/stac/search",
    "https://catalogue.digitalearth.africa/stac/search",
]

_w, _s, _e, _n = aoi_bbox()
PAYLOAD = {
    "collections": ["sentinel-2-l2a"],
    "bbox": [_w, _s, _e, _n],
    "datetime": "2024-01-01T00:00:00Z/2026-06-17T23:59:59Z",
    "limit": 3,
}


def probe(url):
    body = json.dumps(PAYLOAD).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json",
                 "User-Agent": "lqv/scripts.satellite.test_stac"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read(2048).decode(errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(1024).decode(errors="replace")
    except urllib.error.URLError as e:
        return 0, str(e.reason)


def main():
    print("STAC Endpoint Diagnosis")
    print(f"  AOI bbox: ({_w}, {_s}, {_e}, {_n})")
    working = []
    for url in URLS:
        print(f"Testing: {url}")
        s, b = probe(url)
        print(f"  Status: {s}")
        print(f"  Body: {b[:300]!r}")
        if 200 <= s < 300:
            working.append(url)
    print(f"Working: {working if working else 'none'}")
    if not working:
        sys.exit(1)


if __name__ == "__main__":
    main()
