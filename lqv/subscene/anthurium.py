"""Sub-render: Anthurium plowmanii rosettes — bird's-nest epiphytes.

Default scatter mounts on riparian trunks; for the isolation render we
substitute a centered ring of explicit spots so the rosettes read against
neutral ground without requiring host trunks in the scene.
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base


def _build():
    from lqv.flora import scatter_anthuriums
    spots = [
        (-0.8, -0.6, 0.30, 1.10),
        (0.9, -0.5, 0.32, 1.05),
        (-0.5, 0.7, 0.34, 1.00),
        (0.6, 0.8, 0.31, 1.05),
    ]
    scatter_anthuriums(spots=spots)


if __name__ == '__main__':
    base.run(
        asset='anthurium',
        build_fn=_build,
        camera_target=(0.0, 0.0, 0.4),
        camera_distance=2.5,
        camera_height=1.2,
        camera_lens=50.0,
    )
