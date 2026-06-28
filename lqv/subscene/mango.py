"""Sub-render: mango canopy (Mangifera indica) — dominant rounded crown."""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base


def _build():
    from lqv.flora import add_mango
    add_mango(0.0, 0.0, scale=1.0)


if __name__ == '__main__':
    base.run(
        asset='mango',
        build_fn=_build,
        camera_target=(0.0, 0.0, 3.0),
        camera_distance=8.0,
        camera_height=3.5,
        camera_lens=35.0,
    )
