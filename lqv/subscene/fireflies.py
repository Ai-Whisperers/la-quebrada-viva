"""Sub-render: fireflies (Variant C only — night/blue-hour scatter).

Forces RENDER_VARIANT=C regardless of env, since fireflies are a
variant-C-only effect per the brief.
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

os.environ['RENDER_VARIANT'] = 'C'

from lqv.subscene import base


def _build():
    from lqv.flora import scatter_fireflies
    scatter_fireflies(n=80, variant='C')


if __name__ == '__main__':
    base.run(
        asset='fireflies',
        build_fn=_build,
        camera_target=(0.0, 0.0, 1.5),
        camera_distance=8.0,
        camera_height=2.5,
        camera_lens=35.0,
    )
