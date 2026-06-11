"""Sub-render: tatakuá domed clay oven (Rule 8 cultural detail)."""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base


def _build():
    from lqv.house import build_tatakua
    build_tatakua()


if __name__ == '__main__':
    base.run(
        asset='tatakua',
        build_fn=_build,
        camera_target=(-5.5, -4.5, 0.7),
        camera_distance=3.5,
        camera_height=1.6,
        camera_lens=50.0,
    )
