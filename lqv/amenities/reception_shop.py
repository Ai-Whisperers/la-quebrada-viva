"""Reception + micro-shop amenity stub.

First building guests reach after the gate. Combines check-in counter, small
shop (local produce, books, La Quebrada Viva–branded items), and the office.

Dormant.
"""
from __future__ import annotations

FOOTPRINT_M2 = 38.0
ROOF_TYPE = 'sod_low_pitch'
NOTES = (
    'Position: just inside the gate, NE corner of the central core.',
    'Cell-signal repeater installed in the ridge (for guest WiFi handoff).',
    'Lockable storage room for high-value items + petty cash safe.',
)


def build(parent=None, location=(0.0, 0.0, 0.0)):
    raise NotImplementedError('Pending: see HOUSING_PARK_CONCEPT.md §amenities.')
