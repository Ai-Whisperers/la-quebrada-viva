"""Yard props — firewood stack, drying rack, tools, compost bin.

Outdoor working details that signal a lived-in property: a cut firewood
stack near the tatakuá, a wooden drying rack for herbs, hand tools leaned
against the wall, a wire compost bin discreetly placed away from the
corredor.

Status: dormant.
"""
from __future__ import annotations

DEFAULT_PROPS = (
    # (kind, count, anchor_zone, notes)
    ('firewood_stack',  1, 'south_of_tatakua',   '0.8 m³ split urunday + lapacho offcuts'),
    ('herb_drying_rack',1, 'east_corredor_end',  '4 horizontal lapacho rails, removable'),
    ('garden_tools',    1, 'service_wall',       'shovel + hoe + machete on hooks'),
    ('wheelbarrow',     1, 'service_yard',       'painted metal body, wood handles'),
    ('compost_bin',     1, 'service_yard',       '1 m³ wood-slat 3-bay, lid covered'),
    ('axe_in_block',    1, 'firewood_stack',     'detail prop next to the stack'),
)
NOTES = (
    'No standing water (Rule 3) — wheelbarrow stored upturned during the rainy season.',
    'Compost lidded — keeps rats + flies down, helps habilitación inspections.',
)


def place_default_set():
    """Place ``DEFAULT_PROPS`` in the yard."""
    raise NotImplementedError('Pending: requires yard anchor zones + collision check.')
