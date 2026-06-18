#!/usr/bin/env python3
"""Exploratory liveness probe for STAC endpoints we may depend on.

NOT a pytest target — the ``test_`` prefix is for "diagnostic", invoked
by hand when ``fetch_sentinel2.py`` returns 0 scenes (often the endpoint
is down, not the AOI). Prints status code + first 2 KB of response body
per endpoint. Sibling ``conftest.py`` keeps pytest from collecting it.

Run:
    python -m scripts.satellite.test_stac

The endpoints list is exploratory: not all of them are required by the
production fetchers (only element84 + Planetary Computer are), and some
are known to be flaky or offline — see inline notes. A nonzero exit
just means none of the probed endpoints answered 2xx; it does not mean
the LQV pipeline is broken.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from datetime import UTC, datetime

from scripts.satellite._aoi import aoi_bbox

URLS = [
    # Production fetchers (fetch_sentinel2, pc_stac_quickstart, fetch_landcover,
    # fetch_climate) only depend on these two — the rest are exploratory.
    "https://earth-search.aws.element84.com/v1/search",
    "https://planetarycomputer.microsoft.com/api/stac/v1/search",
    # Exploratory / unverified. Endpoint availability and STAC API spec
    # compliance both vary. Leave probed so we notice if any ever comes back
    # online, but treat their failure as informational, not a regression.
    "https://explore.imagery.coop/stac/search",          # status: unverified
    "https://datahub.radiant.earth/stac/search",         # Radiant Earth retired its hub in 2024
    "https://catalogue.digitalearth.africa/stac/search",  # AOI is not in Africa coverage
]

_w, _s, _e, _n = aoi_bbox()
# End of probe window is "now" so the datetime range never rots.
PAYLOAD = {
    "collections": ["sentinel-2-l2a"],
    "bbox": [_w, _s, _e, _n],
    "datetime": f"2024-01-01T00:00:00Z/{datetime.now(UTC).isoformat()}",
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
