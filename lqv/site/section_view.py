"""Generate a property section / cut view.

Section line: NW–SE through the central core, showing how the house typologies,
restaurant and amenities sit on the topography (ridge → terrace → stream).
Useful as an architectural drawing for the escritura presentation.

Dormant — never imported by the live builder.
"""
from __future__ import annotations

SECTION_START_XY = (-300.0, 300.0)     # NW corner ridge
SECTION_END_XY = (350.0, -350.0)       # SE corner stream lowland
SECTION_WIDTH_M = 30.0                  # extrude width for hatching


def build_section_plane(parent=None):
    """Place a planar cutter through the scene at the section line."""
    raise NotImplementedError('Pending: requires lqv.site.terrain_62ha to land first.')


def render_orthographic(camera_name: str = 'SectionCam'):
    """Render an orthographic view down the section line."""
    raise NotImplementedError('Pending: needs orthographic camera + Freestyle line work.')
