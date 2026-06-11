"""Typology #6 — adobe courtyard house.

Traditional Paraguayan typology: adobe-block U-plan around an internal patio,
deep corredor on all sides, tatakuá oven near the patio. Most "Paraguayan-first"
of the eight typologies (Rule 8 — cultural framing).

Dormant — see ``lqv.typologies.__init__``.
"""
from __future__ import annotations

FOOTPRINT_M2 = 85.0
WALL_HEIGHT_M = 2.6
ROOF_TYPE = 'clay_tile_hipped'
ORIENTATION = 'courtyard_centred'
NOTES = (
    'Adobe blocks 30×15×10 cm, sun-dried, no fired bricks (cultural authenticity).',
    'Tatakuá in the SE corner of the patio.',
    'Corredor around all four interior sides; columns: turned lapacho.',
    'Floor: cement-stabilised earth, polished with linseed oil.',
)


def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    raise NotImplementedError('Pending: see HOUSING_PARK_CONCEPT.md typology #6.')
