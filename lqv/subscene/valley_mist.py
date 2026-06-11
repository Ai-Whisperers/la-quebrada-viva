"""Sub-render: valley mist volume (variant-driven density / colour)."""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base


def _build(variant: str):
    from lqv.lighting import build_valley_mist
    build_valley_mist(variant, skip=False)


if __name__ == '__main__':
    _variant = os.environ.get('RENDER_VARIANT', 'A')

    def _wrapped():
        _build(_variant)

    base.run(
        asset='valley_mist',
        build_fn=_wrapped,
        camera_target=(0.0, 10.0, 2.0),
        camera_distance=20.0,
        camera_height=4.0,
        camera_lens=35.0,
    )
