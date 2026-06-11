"""Sub-render: canopy volume scatter — Cycles volume cube above the field."""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base


def _build():
    from lqv.lighting import build_canopy_volume
    build_canopy_volume(skip=False)


if __name__ == '__main__':
    base.run(
        asset='canopy_volume',
        build_fn=_build,
        camera_target=(0.0, 0.0, 4.0),
        camera_distance=12.0,
        camera_height=5.0,
        camera_lens=35.0,
    )
