"""Restaurant dining hall stub.

Open-plan main hall: 48 covers indoors, expandable via folding glass walls
onto the 36-cover wooden deck. Roof: low-pitch sod overhang continuing the
LQV vocabulary (Rule 8 — cultural continuity across the housing park).

Dormant — see ``lqv.restaurant.__init__``.
"""
from __future__ import annotations

FOOTPRINT_M2 = 165.0
CEILING_HEIGHT_M = 4.2
ORIENTATION = 'long_axis_e_w'
ROOF_TYPE = 'sod_low_pitch'
NOTES = (
    'Acoustic: cork wall panels + suspended cane-mat baffles below ceiling.',
    'Flooring: lapacho strip flooring over screed; underfloor radiant cooling.',
    'Folding doors: 6-panel lift-and-slide, 4.5 m total opening.',
    'Bar against the north wall, view to the kitchen pass.',
)


def build(parent=None, location=(0.0, 0.0, 0.0)):
    raise NotImplementedError('Pending: see HOUSING_PARK_CONCEPT.md §restaurant.')
