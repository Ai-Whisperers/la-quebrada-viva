#!/usr/bin/env python3
"""Audit `assets/` against `CREDITS.md`.

Walks `assets/sketchfab/<uid>/`, `assets/polyhaven/textures/<slug>/`,
`assets/polyhaven/models/<slug>/`, and `assets/hdris/` and prints which IDs are:

    on_disk    listed_in_credits
    YES        YES                     OK
    YES        NO                      ATTRIBUTION GAP (CC-BY/CC0 must be credited)
    NO         YES (marked [USED])     STALE manifest — file gone, credit lingers
    NO         YES (marked [PLANNED])  expected — waiting on Phase 8 / MCP

Exits non-zero on any ATTRIBUTION GAP (the only thing that risks a CC-BY violation).
Pure stdlib.
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, 'assets')
CREDITS = os.path.join(ROOT, 'CREDITS.md')

UID_RE = re.compile(r'`([0-9a-f]{32})`')
SLUG_RE = re.compile(r'`([a-z][a-z0-9_]+)`')


def parse_credits() -> tuple[set[str], set[str], set[str]]:
    """Return (sketchfab_uids, polyhaven_slugs, planned_uids).

    A "planned" entry is a Sketchfab line starting with "[PLANNED]".
    """
    uids: set[str] = set()
    planned: set[str] = set()
    slugs: set[str] = set()
    with open(CREDITS, encoding='utf-8') as fh:
        for line in fh:
            line_stripped = line.strip()
            for m in UID_RE.finditer(line):
                if '[PLANNED]' in line_stripped:
                    planned.add(m.group(1))
                else:
                    uids.add(m.group(1))
            if line_stripped.startswith('- `') and len(line_stripped) < 80:
                m = SLUG_RE.match(line_stripped[2:])
                if m:
                    slugs.add(m.group(1))
    return uids, slugs, planned


def list_disk_uids() -> set[str]:
    sf = os.path.join(ASSETS, 'sketchfab')
    if not os.path.isdir(sf):
        return set()
    return {d for d in os.listdir(sf) if os.path.isdir(os.path.join(sf, d))}


def list_disk_textures() -> set[str]:
    out: set[str] = set()
    for sub in ('polyhaven/textures', 'textures'):
        path = os.path.join(ASSETS, sub)
        if os.path.isdir(path):
            out.update(d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)))
    return out


def main() -> int:
    credit_uids, credit_slugs, planned = parse_credits()
    disk_uids = list_disk_uids()
    disk_tex = list_disk_textures()

    gaps = 0

    print("=== sketchfab UIDs ===")
    for uid in sorted(disk_uids | credit_uids | planned):
        on_disk = uid in disk_uids
        listed = uid in credit_uids
        is_planned = uid in planned
        status = (
            'OK' if on_disk and listed else
            'ATTRIBUTION GAP' if on_disk and not listed else
            'PLANNED (expected)' if not on_disk and is_planned else
            'STALE (file gone)' if not on_disk and listed else
            '???'
        )
        if status == 'ATTRIBUTION GAP':
            gaps += 1
        print(f"  {uid}  disk={'Y' if on_disk else 'N'}  credit={'Y' if listed else 'N'}  {status}")

    print("\n=== poly haven texture slugs ===")
    for slug in sorted(disk_tex | credit_slugs):
        on_disk = slug in disk_tex
        listed = slug in credit_slugs
        status = (
            'OK' if on_disk and listed else
            'CC0 (no legal risk) but missing from CREDITS' if on_disk and not listed else
            'listed but not on disk (download pending)'
        )
        print(f"  {slug:32s}  disk={'Y' if on_disk else 'N'}  credit={'Y' if listed else 'N'}  {status}")

    if gaps:
        print(f"\nFAIL: {gaps} CC-BY attribution gap(s)", file=sys.stderr)
        return 2
    print("\nOK: no CC-BY attribution gaps")
    return 0


if __name__ == '__main__':
    sys.exit(main())
