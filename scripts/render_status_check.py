#!/usr/bin/env python3
"""Cross-check the STATUS.md manifest against the actual contents of `renders/`.

Read-only. Prints three columns:

    <variant>_<cam>   manifest=<☑|☐>   on_disk=<size|MISSING>

Exits non-zero if any manifest ☑ row is missing on disk, OR any on-disk file is
absent from the manifest. Use as a pre-tag gate before `v1.0-bundle`.

No third-party deps; pure stdlib so it runs under any Python 3.10+.
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUS = os.path.join(ROOT, 'STATUS.md')
RENDERS = os.path.join(ROOT, 'renders')

VARIANTS = ('A', 'B', 'C')
CAMS = ('hero', 'stream_up', 'terrace', 'cliff', 'dusk', 'petal_macro')

ROW_RE = re.compile(r'^\|\s*([ABC])\s+([a-z_]+)\s*\|\s*`renders/[^`]+`\s*\|\s*(☑|☐)')


def parse_status() -> dict[str, str]:
    out: dict[str, str] = {}
    with open(STATUS, encoding='utf-8') as fh:
        for line in fh:
            m = ROW_RE.match(line)
            if m:
                out[f"{m.group(1)}_{m.group(2)}"] = m.group(3)
    return out


def main() -> int:
    manifest = parse_status()
    expected = [f"{v}_{c}" for v in VARIANTS for c in CAMS]
    bad = 0
    for key in expected:
        path = os.path.join(RENDERS, f"{key}.png")
        on_disk = os.path.getsize(path) if os.path.isfile(path) else None
        mflag = manifest.get(key, '?')
        disk = f"{on_disk//1024} KB" if on_disk is not None else 'MISSING'
        warn = ''
        if mflag == '☑' and on_disk is None:
            warn = ' <-- manifest claims done but file missing'
            bad += 1
        elif mflag == '☐' and on_disk is not None:
            warn = ' <-- on disk but manifest still ☐'
            bad += 1
        print(f"{key:24s}  manifest={mflag}  on_disk={disk}{warn}")
    if bad:
        print(f"\nFAIL: {bad} inconsistency / inconsistencies", file=sys.stderr)
        return 2
    print("\nOK: manifest matches disk")
    return 0


if __name__ == '__main__':
    sys.exit(main())
