"""Decompose imported 3rd-party meshes into editable subcomponents.

Some assets we want to download (chairs, hammocks, kitchen tools) arrive as a
single welded mesh or a single FBX with baked materials. To re-use them in the
LQV build we need to break them into named subcomponents whose materials can
be swapped to the project's `MAT` registry, and whose pivots can be reset for
deterministic placement.

Status: dormant. The current builder uses pure-procedural props.
"""
from __future__ import annotations

DECOMPOSE_STRATEGIES = (
    'by_material',             # split by material slot
    'by_loose_parts',          # bmesh.separate_loose
    'by_naming_convention',    # _XX suffix groups
)


def decompose(imported_obj_name: str, strategy: str = 'by_loose_parts'):
    """Return a list of sub-object names after decomposition."""
    raise NotImplementedError('Pending: needs bpy.ops.mesh.separate + naming pass.')


def remap_materials_to_mat_registry(sub_objs, slot_to_mat_key: dict[str, str]):
    """Remap material slots on each sub-object to keys in ``lqv.materials.MAT``."""
    raise NotImplementedError('Pending: implement once decompose() lands.')
