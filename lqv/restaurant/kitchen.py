"""Restaurant production kitchen stub.

Hot line + cold prep + pastry section, separated from the dining hall by a
glass pass. SET / municipal HACCP compliance: stainless surfaces, sealed
floor coving, three-bay sink. See ``docs/EUROPEAN_TOURISM_SPEC.md`` for
regulatory dependencies (SENATUR + municipal habilitación).

Dormant — see ``lqv.restaurant.__init__``.
"""
from __future__ import annotations

FOOTPRINT_M2 = 42.0
CEILING_HEIGHT_M = 3.2
EXTRACTION = 'twin_500mm_canopy_with_makeup_air'
GAS_BOTTLES = '2x_45kg_LPG_external_cage'
NOTES = (
    'Cold storage 8 m² + walk-in chiller against the north (cooler) wall.',
    'Tatakuá oven OUTSIDE the kitchen — in the patio next to the deck (cultural feature).',
    'No open drains in food zone — covered linear strip drains only.',
    'Grease trap external; service-yard access for monthly pump-out.',
)


def build(parent=None, location=(0.0, 0.0, 0.0)):
    raise NotImplementedError('Pending: see HOUSING_PARK_CONCEPT.md §restaurant.')
