"""Restaurant garden + deck stub.

Lapacho deck off the dining hall + a planted "kitchen garden" parcel that
doubles as scenery and as a herb source. Strict rule: NO standing-water
features (Rule 3 applies across the whole housing park).

Dormant — see ``lqv.restaurant.__init__``.
"""
from __future__ import annotations

DECK_AREA_M2 = 95.0           # ~36 covers at 2.6 m²/cover
GARDEN_AREA_M2 = 240.0
NOTES = (
    'Deck: lapacho 21x140 mm, hidden fixings, 5° fall to drain into French drain.',
    'Pergola: bamboo rafters, climbing passionfruit (mburucuyá) — afternoon shade.',
    'Garden: raised beds 80 cm high, drip irrigation, automatic timer.',
    'Lighting: low-glare bollards along the deck edge, warm 2700 K.',
)


def build(parent=None, location=(0.0, 0.0, 0.0)):
    raise NotImplementedError('Pending: see HOUSING_PARK_CONCEPT.md §restaurant.')
