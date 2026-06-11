"""Sub-render: Rule 7+9+10 service stack — weir + Pelton + solar frame + tank + tatakuá.

Services are placed relative to the cob house, so we build the cob house
first to give them context and correct Z-offsets (solar frame sits on a
steel A-frame anchored to the wall plate, not floating in space).
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from lqv.subscene import base


def _build():
    from lqv.house import build_cob_house, build_services
    build_cob_house()
    build_services()


if __name__ == '__main__':
    base.run(
        asset='services',
        build_fn=_build,
        camera_target=(0.0, 0.0, 2.2),
        camera_distance=10.0,
        camera_height=4.0,
        camera_lens=35.0,
    )
