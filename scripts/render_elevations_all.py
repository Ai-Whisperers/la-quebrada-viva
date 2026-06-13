"""Orchestrator: 4 Dutch elevations for every typology + amenity -> 72 PNGs total.

Loops the 14 typologies declared in `lqv.typologies.TYPOLOGIES` plus the 4
amenities in `lqv.amenities.AMENITIES`, dispatches each to
`lqv.subscene.elevation_dutch.render_typology`, and prints a final summary.
Per-typology failures do not abort the run — the deck builder will fall back
to placeholders if a tile is missing.

Output (per typology):
    renders/sub/runs/<RENDER_RUN_ID>_elevation_dutch_<slug>/{front,back,left,right}.png
    renders/sub/latest/elevation_dutch_<slug>_{front,back,left,right}.png

Usage (headless Blender):
    RENDER_RUN_ID=20260613_elev RENDER_VARIANT=A RENDER_SAMPLES=64 \\
        RENDER_RES=preview blender -b -P scripts/render_elevations_all.py

To restrict the run to a subset (e.g. for debugging):
    ELEVATION_TYPOLOGIES=hobbit_house,bamboo_beton_28 \\
        blender -b -P scripts/render_elevations_all.py
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.typologies import TYPOLOGIES
from lqv.amenities import AMENITIES
from lqv.subscene import elevation_dutch


def main():
    all_targets = list(TYPOLOGIES) + list(AMENITIES)
    filt = os.environ.get('ELEVATION_TYPOLOGIES', '').strip()
    if filt:
        wanted = {s.strip() for s in filt.split(',') if s.strip()}
        targets = [t for t in all_targets if t in wanted]
        missing = wanted - set(targets)
        if missing:
            print(f"[elev-all] WARN unknown slugs in ELEVATION_TYPOLOGIES: {sorted(missing)}")
    else:
        targets = all_targets

    total_typ = len(targets)
    total_elev = total_typ * 4
    print(f"[elev-all] rendering {total_typ} typologies x 4 elevations = {total_elev} PNGs")

    summary = []  # list of (typology, ok_list, fail_dict)
    for i, typology in enumerate(targets, start=1):
        print(f"\n[elev-all] ({i}/{total_typ}) {typology}")
        try:
            result = elevation_dutch.render_typology(typology)
            summary.append((typology, result['ok'], result['fail']))
        except Exception as e:
            print(f"[elev-all] FATAL {typology}: {e}")
            import traceback
            traceback.print_exc()
            summary.append((typology, [], {'_setup': str(e)}))

    # Final tally.
    total_ok = sum(len(ok) for _, ok, _ in summary)
    total_fail = sum(len(fail) for _, _, fail in summary)
    print(f"\n[elev-all] done — {total_ok}/{total_elev} elevations rendered")
    for typology, ok, fail in summary:
        status = 'OK ' if not fail else ('PART' if ok else 'FAIL')
        print(f"  [{status}] {typology:<40} ok={ok} fail={list(fail.keys())}")

    if total_fail:
        print(f"\n[elev-all] {total_fail} elevation(s) failed — deck builder will use placeholders")


if __name__ == '__main__':
    main()
