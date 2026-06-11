"""Parking + arrival sequence amenity stub.

Permeable-paver parking for 22 cars + 2 minibuses, intentionally separated
from the guest core by a 60 m walking path that crosses the stream on a
pedestrian-only timber bridge. Walking arrival is part of the experience.

Dormant.
"""
from __future__ import annotations

CAR_BAYS = 22
MINIBUS_BAYS = 2
ACCESSIBLE_BAYS = 2          # mandatory under PY building regs
SURFACE = 'permeable_paver_with_grass_joint'
NOTES = (
    'Slope: 2% fall to a swale planted with native iris — slows runoff into the stream.',
    'Lighting: low bollards, downlight only, 2700 K — bat-friendly.',
    'EV charge points: 2 x 11 kW Type-2; conduit pulled for 4 more.',
    'Drop-off zone covered by a steel pergola with bougainvillea climbing.',
)


def build(parent=None, location=(0.0, 0.0, 0.0)):
    raise NotImplementedError('Pending: see HOUSING_PARK_CONCEPT.md §amenities.')
