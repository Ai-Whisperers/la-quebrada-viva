"""Sub-render: north escarpment cliff (80m × 50m at y=20)."""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base


def _build():
    from lqv.site import build_escarpment
    build_escarpment()


if __name__ == '__main__':
    base.run(
        asset='escarpment',
        build_fn=_build,
        camera_target=(0.0, 20.0, 8.0),
        camera_distance=40.0,
        camera_height=12.0,
        camera_lens=50.0,
        with_ground=False,
    )
