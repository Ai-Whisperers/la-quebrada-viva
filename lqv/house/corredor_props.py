"""Corredor props — hammock, chairs, mate gourd, lapacho table.

The corredor (the wraparound covered verandah) is the cultural heart of a
Paraguayan house (Rule 8). Today it is empty. Adding hammock + low table +
chairs + a mate gourd / bombilla would make the hero and terrace cameras
read as inhabited rather than as a sterile architectural study.

Status: dormant. No current builder pulls this in.
"""
from __future__ import annotations

DEFAULT_PROPS = (
    # (kind, count, footprint_radius_m, notes)
    ('hammock',          1, 1.20, 'lapacho posts already in mesh; rope twist 12 strand'),
    ('low_lapacho_table',1, 0.50, '40 cm tall, single slab top, four turned legs'),
    ('rocking_chair',    2, 0.55, 'caned seat + back, lapacho frame'),
    ('mate_set',         1, 0.10, 'gourd + bombilla on a small wooden tray'),
    ('throw_rug',        1, 1.40, 'woven ñandutí pattern; on the floor beside the hammock'),
    ('book_stack',       1, 0.20, 'three weathered books'),
    ('terracotta_planter',2, 0.30, 'with mburucuyá climber'),
)


def place_default_set():
    """Place ``DEFAULT_PROPS`` on the corredor."""
    raise NotImplementedError('Pending: requires corredor anchor points + collision check.')
