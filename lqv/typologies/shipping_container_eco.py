"""Typology #4 — eco-retrofitted shipping containers.

Two 40-ft high-cube containers in L-configuration, white roof, deep overhangs,
internal sheep-wool insulation, lapacho deck linking them. Showcase rapid-build
typology for visitors who like industrial aesthetics.

Dormant — see ``lqv.typologies.__init__``.
"""
from __future__ import annotations

CONTAINERS = 2
CONTAINER_TYPE = '40HC'
FOOTPRINT_M2 = 60.0           # ~30 m² per container, less openings overlap
WALL_HEIGHT_M = 2.9
ROOF_TYPE = 'flat_white_with_pergola_overhang'
ORIENTATION = 'l_facing_ne'   # NE-facing inner corner
NOTES = (
    'White cool-roof coating REQUIRED — raw container roof would cook in PY summer.',
    'Sheep-wool internal insulation 100 mm; no spray foam.',
    'Cut openings: 2 large panoramic + 4 standard; remaining walls solid.',
    'Connecting deck: lapacho boards on galvanised steel sub-frame.',
)


def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    raise NotImplementedError('Pending: see HOUSING_PARK_CONCEPT.md typology #4.')
