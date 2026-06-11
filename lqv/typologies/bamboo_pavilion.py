"""Typology #3 — Guadua bamboo pavilion.

Open-plan pavilion: structural Guadua angustifolia bundles, palm-thatch roof,
minimal walls (curtain or movable cane panels). 60 m². Best suited to the
upper-terrace cluster where the canopy is thinnest.

Dormant — see ``lqv.typologies.__init__``.
"""
from __future__ import annotations

FOOTPRINT_M2 = 60.0
WALL_HEIGHT_M = 2.8
ROOF_TYPE = 'palm_thatch_hipped'
ORIENTATION = 'corredor_north'
SPECIES = 'guadua_angustifolia'   # NOT running bamboo
NOTES = (
    'Treat all Guadua: borax + boric acid (per cm² method).',
    'No metal-on-metal joints visible — lashings + cylindrical bolts only.',
    'Thatch: pindo palm leaves; 25 cm thick, 35° pitch to shed rain.',
    'No earthen walls — bamboo screen + glass louvres at sleeping bay.',
)


def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    raise NotImplementedError('Pending: see HOUSING_PARK_CONCEPT.md typology #3.')
