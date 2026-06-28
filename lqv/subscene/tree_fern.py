"""Sub-render: tree fern (Dicksonia/Cyathea) — 2.8m trunk + arching fronds."""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base


def _build():
    from lqv.flora import add_tree_fern
    add_tree_fern(0.0, 0.0, scale=1.0)


if __name__ == '__main__':
    base.run(
        asset='tree_fern',
        build_fn=_build,
        camera_target=(0.0, 0.0, 1.6),
        camera_distance=4.5,
        camera_height=2.0,
        camera_lens=50.0,
    )
