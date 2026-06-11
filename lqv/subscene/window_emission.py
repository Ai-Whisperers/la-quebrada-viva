"""Sub-render: window emission planes (variant-driven warm interior glow).

Pairs cob house + window_emission so the emission planes register against
the actual WindowCut_* Boolean cutters rather than floating squares.
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base


def _build(variant: str):
    from lqv.house import build_cob_house, build_window_emission
    build_cob_house()
    build_window_emission(variant)


if __name__ == '__main__':
    import os as _os
    _variant = _os.environ.get('RENDER_VARIANT', 'A')

    def _wrapped():
        _build(_variant)

    base.run(
        asset='window_emission',
        build_fn=_wrapped,
        camera_target=(0.0, 0.0, 1.5),
        camera_distance=8.0,
        camera_height=2.4,
        camera_lens=35.0,
    )
