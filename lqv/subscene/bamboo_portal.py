"""Sub-render: bamboo entry portal in isolation.

House-scale asset (footprint ~3.2 × 0.8 m, height 3.5 m). Standard ``base.run()``
entry point with HOUSE_CLIP_END_M; framed slightly off-axis so the slat pergola
reads against the sky.
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base

ASSET = 'bamboo_portal'


def main():
    from lqv.typologies.bamboo_portal import build_bamboo_portal

    return base.run(
        ASSET,
        build_fn=lambda: build_bamboo_portal(origin=(0.0, 0.0, 0.0)),
        camera_target=(0.0, 0.0, 1.6),
        camera_distance=7.5,
        camera_height=2.2,
        camera_lens=35.0,
        ground_material='laterite',
        context_flora_count=12,
    )


if __name__ == '__main__':
    main()
