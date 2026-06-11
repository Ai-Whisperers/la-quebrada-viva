"""Groundcover patches — moss, creeping herbs, low ferns.

Currently the ground is a flat shader with displacement. Adding instanced
groundcover at corredor edges, around the stone foundation, and along the
stream bank would dramatically improve closeup believability (petal_macro
camera in particular).

Status: dormant stub.
"""
from __future__ import annotations

PATCH_TYPES = (
    'moss_sandstone',          # for stone terraces; #5F7A3D → #8AA055
    'creeping_thyme',          # for corredor margins
    'wood_sorrel',             # shade margins
    'mini_ferns',              # stream bank
)
DEFAULT_PATCH_RADIUS_M = 0.45
DEFAULT_BLADE_COUNT = 240
NOTES = (
    'No grass on the sod roof from this module — that has its own builder.',
    'Render impact: keep blade count below 300/patch to avoid blowing memory.',
)


def add_patch(patch_type: str, location, radius: float = DEFAULT_PATCH_RADIUS_M):
    """Place a groundcover patch at ``location``."""
    raise NotImplementedError('Pending: needs instance source meshes + scatter strategy.')
