"""Window light cones — debug visualization for Variant C night render.

For night-render fault diagnosis (does the warm interior light actually reach
the corredor?) we sometimes want to visualize each window's outgoing light
cone as a translucent volume. This module would emit cone primitives at each
``WindowCut_*`` position, pointing along the wall normal.

Status: dormant. Production renders must NEVER include the cones; they are a
diagnostic-only tool.
"""
from __future__ import annotations

CONE_LENGTH_M = 4.0
CONE_HALF_ANGLE_DEG = 35.0     # ~ 70° cone, matching real diffuse interior glow
DEBUG_COLLECTION_NAME = '_DEBUG_WindowCones'


def show_cones(visible: bool = True):
    """Toggle the debug collection."""
    raise NotImplementedError('Pending: needs lookup of WindowCut_* objects in scene.')


def assert_not_in_production_render():
    """Sanity check called by ``lqv.util.ten_rules_check`` (future Rule 11)."""
    raise NotImplementedError('Pending: integrate into ten_rules_check once that path is live.')
