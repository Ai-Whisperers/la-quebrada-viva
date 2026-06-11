"""Sub-render: equestrian paddock + stables amenity in isolation."""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base


def _build():
    from lqv.amenities.equestrian_zone import build
    build()


if __name__ == '__main__':
    base.run(
        asset='equestrian_zone',
        build_fn=_build,
        camera_target=(0.0, 0.0, 1.0),
        camera_distance=22.0,
        camera_height=6.0,
        camera_lens=24.0,
    )
