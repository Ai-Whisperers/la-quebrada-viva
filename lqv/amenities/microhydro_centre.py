"""Micro-hydro visitor / interpretive centre stub.

Small open-walled pavilion at the stream tap-off. Showcases the housing-park
energy story (micro-hydro turbine, LiFePO4 bank, monitoring dashboard).
Doubles as Wesley's demo backdrop for guest tours.

Dormant.
"""
from __future__ import annotations

FOOTPRINT_M2 = 22.0
TURBINE_TYPE = 'crossflow_T15'
BATTERY_BANK_KWH = 30.0
NOTES = (
    'Live screen: production / consumption / cisterns / weather.',
    'Acoustic isolation around the turbine housing (50 dB target at 5 m).',
    'Outage indicator visible from the corredor (Rule 7 spirit — outage-proofness on display).',
    'Educational panels in 3 languages: ES / EN / DE (German community guests).',
)


def build(parent=None, location=(0.0, 0.0, 0.0)):
    raise NotImplementedError('Pending: see HOUSING_PARK_CONCEPT.md §amenities.')
