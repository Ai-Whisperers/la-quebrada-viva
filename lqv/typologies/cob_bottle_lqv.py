"""Typology #1 — La Quebrada Viva (cob + bottle walls).

This module is a *pointer* to the live builder in ``lqv.house.cob`` /
``lqv.house.roof`` / etc.  Promoting LQV to a typology in the housing-park
master plan does NOT mean we rewrite it — we expose the same builders here
behind a uniform interface so the future ``lqv.site.site_plan`` can place
all 8 typologies through one call signature.

Dormant. Never imported by the current build path.
"""
from __future__ import annotations

FOOTPRINT_M2 = 95.0       # interior, see docs/MASTER_BRIEF §3
WALL_HEIGHT_M = 2.6
ROOF_TYPE = 'sod_low_pitch'
ORIENTATION = 'corredor_north'   # corredor faces north (south hemisphere)
NOTES = (
    'Foundation: 60 cm dry-stacked sandstone (Rule 4).',
    'Walls: cob + recycled bottle ends (luminous wall on west elevation).',
    'Plaster: lime only — never cement (Rule 2).',
    'Roof: sod over EPDM on lapacho rafters, low pitch.',
    'Solar: separate steel frame, NOT on sod roof (Rule 9).',
)


def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    """Delegate to the existing LQV builders.

    Implementation deferred: call sites currently invoke the LQV builders
    directly from ``build_scene.py``. When ``lqv.site.site_plan`` lands this
    function will dispatch to ``lqv.house.cob.build_house`` with offset.
    """
    raise NotImplementedError(
        'cob_bottle_lqv.build is a forward-declaration; call lqv.house.cob.build_house directly for now.'
    )
