"""Sub-render: agave rosette (14 blades)."""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base


def _build():
    from lqv.flora import add_agave
    add_agave(0.0, 0.0, scale=1.0)


if __name__ == '__main__':
    base.run(
        asset='agave',
        build_fn=_build,
        camera_target=(0.0, 0.0, 0.4),
        camera_distance=2.5,
        camera_height=1.0,
        camera_lens=50.0,
    )
