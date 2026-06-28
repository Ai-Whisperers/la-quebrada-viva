"""Shared amenities cluster for the housing park.

Dormant subpackage. Per ``docs/TERRAIN_PIVOT.md`` §4 the operative amenity
set is four anchor features arranged around the creek + river fronts:

- ``labrisa_lounge`` (§4.3): creek-fed open-air lounge with cascade weir;
  the central social anchor between the restaurant and the river.
- ``eco_pool`` (§4.1): regen-planting filtered eco pool, no chlorine.
- ``floating_dining`` (§4.2): low-draft platform pad off the river bank.
- ``eco_retreat_modern_oasis`` (§4.4): wellness deck — sauna + plunge tub +
  yoga.

The older HOUSING_PARK_CONCEPT amenity list (reception_shop, equestrian_zone,
parking_arrival, microhydro_centre, etc.) is now folded into the restaurant +
operations envelope and no longer lives as a standalone module.
"""
AMENITIES = (
    'labrisa_lounge',
    'eco_pool',
    'floating_dining',
    'eco_retreat_modern_oasis',
)
