"""Sub-render: bamboo curved-roof villa in isolation.

House-scale signature pavilion (~6 × 9 × 4.2 m). Standard ``base.run()`` with
a camera framed slightly off the open south facade to read the rib arches
against the palm-thatch skin.
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base

ASSET = 'bamboo_curved_roof_villa'


def main():
    from lqv.typologies.bamboo_curved_roof_villa import build_bamboo_curved_roof_villa

    return base.run(
        ASSET,
        build_fn=lambda: build_bamboo_curved_roof_villa(origin=(0.0, 0.0, 0.0)),
        camera_target=(0.0, 0.0, 2.4),
        camera_distance=14.0,
        camera_height=4.0,
        camera_lens=35.0,
        ground_material='laterite',
        context_flora_count=20,
    )


if __name__ == '__main__':
    main()
