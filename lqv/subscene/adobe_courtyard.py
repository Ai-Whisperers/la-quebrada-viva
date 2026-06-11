"""Sub-render: adobe courtyard typology in isolation."""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base


def _build():
    from lqv.typologies.adobe_courtyard import build
    build()


if __name__ == '__main__':
    base.run(
        asset='adobe_courtyard',
        build_fn=_build,
        camera_target=(0.0, 0.0, 1.8),
        camera_distance=15.0,
        camera_height=5.0,
        camera_lens=28.0,
    )
