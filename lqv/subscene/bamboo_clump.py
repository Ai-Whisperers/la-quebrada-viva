"""Sub-render: Guadua bamboo clump (n=20 culms)."""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base


def _build():
    from lqv.flora import add_bamboo_clump
    add_bamboo_clump(0.0, 0.0, n=20, scale=1.0)


if __name__ == '__main__':
    base.run(
        asset='bamboo_clump',
        build_fn=_build,
        camera_target=(0.0, 0.0, 5.5),
        camera_distance=14.0,
        camera_height=4.0,
        camera_lens=50.0,
    )
