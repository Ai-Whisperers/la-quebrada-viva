"""Pool + wellness amenity stub.

Lap-style pool (15×4 m), sauna-cabin, outdoor shower. Pool: biological /
natural-pool design (regen-zone planted filter) to avoid chlorine on the
site's water table. Standing water concern (Rule 3) is dengue specifically:
fast-circulating pool water with biological filter is permitted.

Dormant.
"""
from __future__ import annotations

POOL_LENGTH_M = 15.0
POOL_WIDTH_M = 4.0
POOL_DEPTH_M = 1.6
POOL_TYPE = 'natural_swim_regen_zone'
NOTES = (
    'Regen-zone footprint = swim-zone footprint (1:1) per natural-pool spec.',
    'Skimmer + slow-current pump: full turnover every 4 h max.',
    'Sauna cabin: cedar, wood-fired, separate paved pad.',
    'NO open standing water in the regen-zone surface — gravel cap + biofilm.',
)


def build(parent=None, location=(0.0, 0.0, 0.0)):
    raise NotImplementedError('Pending: see HOUSING_PARK_CONCEPT.md §amenities.')
