"""62-ha housing-park master site plan.

Dormant module. Once promoted, this is the single entry point that places
every typology, the restaurant, the amenities, and the trail loop on the
larger 62-ha terrain. It will call ``lqv.typologies.*.build``,
``lqv.restaurant.*.build``, ``lqv.amenities.*.build``,
``lqv.site.terrain_62ha.build_terrain`` and ``lqv.site.section_view.build``.

Not imported by the current build path.

Layout coordinates (placeholders; final values come from the surveyor's plan):

    central_core:        ( 0, 0)     # restaurant + reception + parking arrival
    typology_lqv:        (-30, -20)  # existing LQV scene
    typology_2_loft:     (50, 40)
    typology_3_bamboo:   (130, -10)
    typology_4_container:(-70, 90)
    typology_5_straw:    (170, 110)
    typology_6_adobe:    (60, -120)
    typology_7_treecabin:(-150, 20)
    typology_8_dome:     (220, -60)
    pool_wellness:       (40, 50)
    event_lawn:          (-20, 80)
    microhydro_centre:   (-200, -50)
    equestrian_zone:     (300, 200)
    parking_arrival:     (-280, 280)

Distances are metres, origin at the central restaurant pad.
"""
from __future__ import annotations

PROPERTY_AREA_HA = 62.0
PROPERTY_PERIMETER_M = 3550.0     # approx, surveyor TBD
ELEVATION_MIN_M = 240.0           # near stream
ELEVATION_MAX_M = 312.0           # ridge
TRAIL_LOOP_LENGTH_M = 2400.0


def build(parent=None):
    raise NotImplementedError('Pending — wait for surveyor topo + Wesley sign-off on layout.')
