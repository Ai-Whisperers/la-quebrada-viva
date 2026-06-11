"""Sub-render: sandstone retaining terraces (3 stepped walls)."""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base


def _build():
    from lqv.site import build_terraces
    build_terraces()


if __name__ == '__main__':
    base.run(
        asset='terraces',
        build_fn=_build,
        camera_target=(0.0, -6.0, 0.5),
        camera_distance=14.0,
        camera_height=5.0,
        camera_lens=35.0,
    )
