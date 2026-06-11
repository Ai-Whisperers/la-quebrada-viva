"""Typology #8 — earthbag dome with partial earth berm.

Dome of polypropylene earthbags filled with stabilised earth, lime plaster
inside and out, north face open with a glazed apse, the other three sides
bermed into the upper terrace. Excellent summer thermal performance.

Dormant — see ``lqv.typologies.__init__``.
"""
from __future__ import annotations

FOOTPRINT_M2 = 50.0
WALL_HEIGHT_M = 3.0          # dome apex
ROOF_TYPE = 'integrated_dome'
ORIENTATION = 'open_face_n'
BERM_DEPTH_M = 1.8
NOTES = (
    'Bags: 50 cm wide woven PP, UV-resistant; barbed wire between courses.',
    'Plaster: lime inside; outside: lime under-coat + earth + drainage sand layer + sod.',
    'Sky-tube oculus at apex; tornado-rated polycarbonate cap.',
    'Drainage: French drain ring at berm intersection — critical, do NOT cut.',
)


def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    raise NotImplementedError('Pending: see HOUSING_PARK_CONCEPT.md typology #8.')
