"""Equestrian + farm zone amenity stub.

Stable for 4 horses, paddock, small kitchen-garden parcel that supplies the
restaurant. Located at the property edge to keep flies + smell away from
the guest cluster.

Dormant.
"""
from __future__ import annotations

STABLE_BAYS = 4
PADDOCK_AREA_M2 = 4000.0
KITCHEN_GARDEN_AREA_M2 = 600.0
NOTES = (
    'Stable orientation: open side NE; prevailing summer breeze cools the boxes.',
    'Manure compost bin downwind (S) of paddock; rotated monthly.',
    'No standing-water troughs (Rule 3) — automatic float-valve drinkers only.',
    'Bridle path connects to the wider 62-ha trail loop.',
)


def build(parent=None, location=(0.0, 0.0, 0.0)):
    raise NotImplementedError('Pending: see HOUSING_PARK_CONCEPT.md §amenities.')
