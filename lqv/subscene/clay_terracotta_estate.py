"""Sub-render: clay-terracotta two-storey estate in isolation.

House-scale asset (~10 × 8 × 7 m). Standard ``base.run()`` with
HOUSE_CLIP_END_M. Camera framed slightly elevated and offset so the second
storey, eave overhang, and latticed screen all read.
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base

ASSET = 'clay_terracotta_estate'


def main():
    from lqv.typologies.clay_terracotta_estate import build_clay_terracotta_estate

    return base.run(
        ASSET,
        build_fn=lambda: build_clay_terracotta_estate(origin=(0.0, 0.0, 0.0)),
        camera_target=(0.0, 0.0, 3.0),
        camera_distance=18.0,
        camera_height=5.5,
        camera_lens=35.0,
        ground_material='laterite',
        context_flora_count=18,
    )


if __name__ == '__main__':
    main()
