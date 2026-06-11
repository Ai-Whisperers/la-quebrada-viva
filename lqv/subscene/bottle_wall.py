"""Sub-render: bottle wall cluster, embedded in the east arm wall."""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base


def _build():
    # Bottle wall is meaningless without its host wall — bring cob_house too
    # so the bottles read embedded rather than floating in space.
    from lqv.house import build_cob_house, build_bottle_wall
    build_cob_house()
    build_bottle_wall()


if __name__ == '__main__':
    base.run(
        asset='bottle_wall',
        build_fn=_build,
        camera_target=(6.0, 2.0, 1.8),
        camera_distance=4.5,
        camera_height=2.0,
        camera_lens=50.0,
    )
