"""62-ha terrain model.

Imports a DEM (digital elevation model) for the Escobar / Paraguarí parcel
and rebuilds it as a meshed plane with vertex colours per soil-type zone.
Inputs (when available, all under ``assets/site_data/``):

* ``escobar_dem_5m.tif`` — SRTM-derived 5m DEM (USGS Earth Explorer; CC0).
* ``escobar_soil_zones.geojson`` — surveyor's soil-type polygons.
* ``escobar_streams.geojson`` — hydrology layer.

Until those land, the module is dormant. See ``docs/site_data_spike.md`` for
the acquisition checklist.
"""
from __future__ import annotations

import os

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'assets', 'site_data')


def is_available() -> bool:
    """True iff the DEM is on disk."""
    return os.path.exists(os.path.join(ASSETS, 'escobar_dem_5m.tif'))


def build_terrain(parent=None, exaggeration: float = 1.0):
    """Mesh the DEM into a Blender plane with subdivision matching the DEM grid."""
    raise NotImplementedError(
        'Pending: DEM not on disk yet. See docs/site_data_spike.md for the acquisition checklist.'
    )
