"""Geometry-Nodes scatter helpers for flora.

Today the flora builders use Python-side ``random`` scatter (deterministic with
seed, but expensive). A Geometry-Nodes scatter graph would be faster, viewport-
visible, and would let the artist tweak density without a rebuild. This module
will hold the GN-node-graph builders; current procedural scatter stays the
authoritative path until parity is proven.

Status: dormant. No imports from ``lqv/*`` yet — adding it now does not affect
byte-identity of the in-flight render.
"""
from __future__ import annotations

DEFAULT_DENSITY = {
    'petal_carpet': 25.0,       # per m² under the lapacho
    'agave_terrace': 0.6,
    'fern_riparian': 1.4,
    'groundcover_moss': 12.0,
}


def build_scatter_modifier(target_mesh_name: str, source_collection_name: str, density: float):
    """Attach a Geometry-Nodes scatter modifier to ``target_mesh_name``.

    The graph should:
        1. Distribute Points on Faces (seed from RNG_SEED env).
        2. Instance on Points from the source collection.
        3. Rotate Z by random in [0, 2π]; tilt small.
        4. Scale by random in [0.85, 1.15].

    Determinism: seed must be threaded through from build_scene.py so reruns
    match. Do NOT pull from ``random.random()`` inside the node-tree builder.
    """
    raise NotImplementedError(
        'Pending: needs node-tree builder + parity test vs procedural scatter.',
    )
