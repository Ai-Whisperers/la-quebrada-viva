"""Bridge to Blender's bundled Sapling Tree generator.

Sapling produces parametric trees with branching variation that is far more
species-accurate than our procedural cylinder-and-curve lapacho. This module
will wrap the Sapling operator and emit a deterministic tree given a species
preset + seed, so the headless build path remains byte-identical between runs.

Status: dormant. Sapling is the built-in add-on (``add_curve_sapling``); we
have not yet enabled it in ``addon_setup.py``. See
``docs/lapacho_quality_upgrade.md`` for the proposed cutover.
"""
from __future__ import annotations

ADDON_MODULE_NAME = 'add_curve_sapling'

# Per-species presets; tuned for the Cerro Patiño microclimate.
PRESETS = {
    'lapacho_winter': {
        'shape': '4',         # tend-flame
        'levels': 3,
        'length': (1.0, 0.6, 0.6),
        'branches': (0, 22, 28, 32),
        'leaves': 0,           # bare in winter
        'leaf_type': '0',
    },
    'lapacho_bloom': {
        'shape': '4',
        'levels': 3,
        'length': (1.0, 0.6, 0.6),
        'branches': (0, 22, 28, 32),
        'leaves': 0,           # blossoms added as a separate particle pass
        'leaf_type': '0',
    },
    'mango': {
        'shape': '0',          # dense round
        'levels': 3,
        'length': (1.2, 0.55, 0.55),
        'branches': (0, 30, 36, 40),
        'leaves': 60,
        'leaf_type': '2',
    },
}


def is_addon_enabled() -> bool:
    """True iff ``add_curve_sapling`` is currently enabled in Blender."""
    raise NotImplementedError('Pending: needs bpy.utils.module loop in active session.')


def grow_tree(species: str, seed: int):
    """Run the Sapling operator with the species preset + seed, return the curve object."""
    raise NotImplementedError('Pending: implement once Sapling is enabled in addon_setup.')
