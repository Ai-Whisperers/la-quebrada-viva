"""Event lawn amenity stub.

Flat lawn surrounded by stone-bench amphitheatre seating, sized for ~80
guests at a wedding or workshop. Power + water sleeves under the lawn for
event hookups.

Dormant.
"""
from __future__ import annotations

LAWN_AREA_M2 = 480.0
NOTES = (
    'Slope: 1% fall NW for drainage, invisible to the eye.',
    'Power sleeves: 4 x 50 mm conduit + 2 x 100 mm, all to a stage box at the south edge.',
    'Water hose-bib pair: north + south.',
    'Backup generator silenced in service yard 80 m away (regulatory + courtesy).',
)


def build(parent=None, location=(0.0, 0.0, 0.0)):
    raise NotImplementedError('Pending: see HOUSING_PARK_CONCEPT.md §amenities.')
