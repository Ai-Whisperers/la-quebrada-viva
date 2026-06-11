"""Typology #7 — elevated lapacho-post tree cabin.

Light timber cabin lifted 3-4 m above grade on lapacho posts, no concrete
footing in canopy zones, accessed by a sloping gangway. Sits within the
Atlantic-forest fragment, minimum impact on roots.

Dormant — see ``lqv.typologies.__init__``.
"""
from __future__ import annotations

FOOTPRINT_M2 = 40.0
WALL_HEIGHT_M = 2.4
ROOF_TYPE = 'shed_zinc'
ELEVATION_M = 3.5
ORIENTATION = 'aligned_to_slope'
NOTES = (
    'Posts: lapacho heartwood, 25 cm diameter, pier blocks not pour-in-place.',
    'No concrete pads within 5 m of significant trees.',
    'Walls: tongue-and-groove lapacho exterior, sheep-wool insulation.',
    'Roof: standing-seam zinc, slope 8°, drips to a rainwater chain at gangway head.',
)


def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    raise NotImplementedError('Pending: see HOUSING_PARK_CONCEPT.md typology #7.')
