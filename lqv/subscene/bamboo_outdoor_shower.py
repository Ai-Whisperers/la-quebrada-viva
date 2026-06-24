"""Sub-render: bamboo outdoor shower amenity in isolation.

House-scale amenity (~1.6 × 1.6 × 2.4 m). Standard ``base.run()`` with a
close camera to read the duckboard, river-stone drain, and steel showerhead.
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base

ASSET = 'bamboo_outdoor_shower'


def main():
    from lqv.typologies.bamboo_outdoor_shower import build_bamboo_outdoor_shower

    return base.run(
        ASSET,
        build_fn=lambda: build_bamboo_outdoor_shower(origin=(0.0, 0.0, 0.0)),
        camera_target=(0.0, 0.0, 1.2),
        camera_distance=4.5,
        camera_height=1.8,
        camera_lens=35.0,
        ground_material='laterite',
        context_flora_count=10,
    )


if __name__ == '__main__':
    main()
