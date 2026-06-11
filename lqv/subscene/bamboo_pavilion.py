"""Sub-render: open-air bamboo pavilion typology in isolation."""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base


def _build():
    from lqv.typologies.bamboo_pavilion import build
    build()


if __name__ == '__main__':
    base.run(
        asset='bamboo_pavilion',
        build_fn=_build,
        camera_target=(0.0, 0.0, 2.0),
        camera_distance=12.0,
        camera_height=4.0,
        camera_lens=28.0,
    )
