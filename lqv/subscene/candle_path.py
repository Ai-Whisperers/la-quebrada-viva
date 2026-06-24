"""Sub-render: candle path amenity in isolation.

Strip-shaped asset (~6 m × 0.9 m × ~1 m). Standard ``base.run()`` with a low,
along-path camera angle so lantern glow and firefly sprites read against the
dusk/night sky. C-variant blue-hour exposure will read best for this one.
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base

ASSET = 'candle_path'


def main():
    from lqv.typologies.candle_path import build_candle_path

    # Centre the path so the camera (looking along -Y from +Y) frames it well.
    return base.run(
        ASSET,
        build_fn=lambda: build_candle_path(origin=(0.0, -3.0, 0.0)),
        camera_target=(0.0, 0.0, 0.4),
        camera_distance=8.0,
        camera_height=1.4,
        camera_lens=35.0,
        ground_material='laterite',
        context_flora_count=18,
    )


if __name__ == '__main__':
    main()
