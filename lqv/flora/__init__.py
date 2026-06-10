"""Procedural flora placeholders + populate/scatter orchestrators."""
from __future__ import annotations

import random

from .pindo import add_pindo_palm
from .lapacho import add_lapacho, scatter_lapacho_petals
from .mango import add_mango
from .fern import add_tree_fern
from .bamboo import add_bamboo_clump, scatter_grass_tufts
from .agave import add_agave
from .anthurium import scatter_anthuriums
from .fireflies import scatter_fireflies


def populate(flowering_lapacho: bool):
    """Distribute species across the site per the brief."""
    # Pindo palms — 5–6 scattered, prominent in views toward the cliff
    pindo_spots = [(-12, 8, 1.0), (-9, 18, 1.2), (14, 12, 1.1), (-15, -4, 1.0), (16, -8, 1.15)]
    for x, y, s in pindo_spots:
        add_pindo_palm(x, y, s)

    # Lapacho — 3 trees, one prominent foreground-mid for petal carpet
    lapacho_spots = [(-3, -10, 1.1), (8, -14, 1.0), (-10, 5, 1.0)]
    for x, y, s in lapacho_spots:
        add_lapacho(x, y, s, flowering=flowering_lapacho)

    # Mango canopy — surrounding the build area as dominant overstory.
    # Three north spots ((-20,20),(20,20),(-14,28)) dropped: they sat behind
    # the escarpment after Work 1 moved the cliff to y=20, so they were
    # rendering invisible mango geometry.
    mango_spots = [
        (-20, -16, 1.1), (22, -22, 1.0),
        (-18, 0, 1.0), (24, 4, 1.1),
    ]
    for x, y, s in mango_spots:
        add_mango(x, y, s)

    # Tree ferns — riparian, near stream
    for x, y in [(8.5, -7), (9.0, -11), (13.5, -16), (8.0, -19)]:
        add_tree_fern(x, y, 1.0)

    # Bamboo clumps — along stream. Far cluster (15.5, -20) was dominating the
    # hero frame; shifted east-northeast off the foreground sightline.
    for x, y in [(7.5, -4), (14.5, -3), (8.0, -14), (15.0, -10), (17.5, -16)]:
        add_bamboo_clump(x, y, n=random.randint(6, 10), scale=1.0)

    # Agave — on lower terraces, NOT designed garden
    for x, y in [(-7, -4), (-5, -5.5), (4, -6), (6, -4.5), (-8, -6)]:
        add_agave(x, y, scale=0.9)


__all__ = [
    'add_pindo_palm', 'add_lapacho', 'add_mango', 'add_tree_fern',
    'add_bamboo_clump', 'add_agave', 'populate', 'scatter_lapacho_petals',
    'scatter_grass_tufts', 'scatter_anthuriums', 'scatter_fireflies',
]
