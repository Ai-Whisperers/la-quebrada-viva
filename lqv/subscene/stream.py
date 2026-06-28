"""Sub-render: stream channel + flat-rock pool (Rule 3 dengue-compliant)."""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base


def _build():
    from lqv.site import build_stream
    build_stream()


if __name__ == '__main__':
    base.run(
        asset='stream',
        build_fn=_build,
        camera_target=(11.0, -14.0, -0.2),
        camera_distance=12.0,
        camera_height=4.0,
        camera_lens=35.0,
        with_ground=False,
    )
