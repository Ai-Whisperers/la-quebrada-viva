"""Typology #5 — straw-bale cottage.

Load-bearing wheat-straw bale walls, lime plaster, gable roof with deep eaves.
Excellent thermal mass paired with insulation; ideal for the upper plateau
where night cooling is strongest.

Dormant — see ``lqv.typologies.__init__``.
"""
from __future__ import annotations

FOOTPRINT_M2 = 55.0
WALL_HEIGHT_M = 2.7
ROOF_TYPE = 'gable_clay_tile'
WALL_THICKNESS_MM = 500       # straw bale standard
ORIENTATION = 'long_axis_n_s'
NOTES = (
    'Bales: 2-string wheat-straw, density ≥ 110 kg/m³; pinned with bamboo.',
    'Plaster: 3-coat lime, total 35 mm; NO cement (similar to Rule 2).',
    'Foundation: dry-stacked stone, 75 cm — extra elevation vs. cob (Rule 4 spirit).',
    'Roof eaves 110 cm minimum to keep rain off the lime plaster.',
)


def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    raise NotImplementedError('Pending: see HOUSING_PARK_CONCEPT.md typology #5.')
