"""Typology #2 — rammed-earth single-story loft.

Stabilised rammed earth (SIREWALL spec) walls, exposed strata bands, mono-pitch
zinc roof tipped to the north for PV. 1-bedroom + loft, 65 m² footprint.

Dormant — see ``lqv.typologies.__init__`` for the package contract.
"""
from __future__ import annotations

FOOTPRINT_M2 = 65.0
WALL_HEIGHT_M = 3.4               # extra height for loft
ROOF_TYPE = 'mono_pitch_zinc'
ORIENTATION = 'long_axis_e_w'     # max solar gain control via overhang
WALL_THICKNESS_MM = 450
NOTES = (
    'Rammed-earth lifts: 10 cm visible strata in the finished wall.',
    'Cement stabiliser allowed (not cob — Rule 2 does not apply).',
    'Lapacho lintels above all openings.',
    'PV on the roof itself (this typology — Rule 9 is LQV-specific).',
)


def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    raise NotImplementedError('Pending: see HOUSING_PARK_CONCEPT.md typology #2.')
