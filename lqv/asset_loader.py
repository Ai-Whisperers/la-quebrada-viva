"""External-asset import helpers (Sketchfab / Poly Haven models / BlenderKit).

Standalone module — intentionally NOT imported by any other lqv/* module yet.
Phase 8 builders (corredor_props, yard_props, etc.) will import this once the
asset files land under ``assets/<source>/<id>/``. Until then this is dormant
and cannot affect render byte-identity for the in-flight A/B/C batch.

Design contract:

* Each importer reads from a content-addressable on-disk path. No MCP, no
  network. The MCP socket may be dead at any moment; the loader doesn't care.
* If the asset directory is missing OR the import fails, the function logs a
  warning and returns ``None``. Callers must treat ``None`` as "fall back to
  procedural builder" and never raise.
* Every successful import is parented to a fresh ``Empty`` named
  ``Asset_<source>_<id>`` so the caller has a single transform handle and the
  scene outliner stays tidy.
* Scale is applied to the parent Empty (not the imported geometry) so a later
  caller can rescale without re-walking the hierarchy.
* No material edits, no modifier stacking — leave the asset's shipped look
  untouched; per-prop tweaks belong in the Phase-8 builders.

Env flag ``USE_EXTERNAL_FLORA=1`` (read by :mod:`lqv.config` once that lands)
gates whether flora builders try this loader at all. When unset, procedural
builders run as before — zero behavior change.
"""
from __future__ import annotations

import os

import bpy

from .config import PROJECT_DIR

ASSETS_ROOT = os.path.join(PROJECT_DIR, 'assets')

Vec3 = tuple[float, float, float]


def _make_parent(name: str, location: Vec3, rotation: Vec3, scale: float) -> bpy.types.Object:
    empty = bpy.data.objects.new(name, None)
    empty.empty_display_type = 'PLAIN_AXES'
    empty.empty_display_size = 0.3
    empty.location = location
    empty.rotation_euler = rotation
    empty.scale = (scale, scale, scale)
    bpy.context.collection.objects.link(empty)
    return empty


def _adopt_imported(parent: bpy.types.Object, before: set) -> int:
    """Reparent every object created since the import call to `parent`.

    Returns the count of adopted objects. Uses set diff on bpy.data.objects
    because importers vary in what they return (gltf2 returns None, append
    returns a list, etc.).
    """
    after = {o.name for o in bpy.data.objects}
    new_names = after - before
    adopted = 0
    for name in new_names:
        obj = bpy.data.objects.get(name)
        if obj is None or obj is parent:
            continue
        if obj.parent is None:
            obj.parent = parent
            adopted += 1
    return adopted


def _log_skip(reason: str, path: str) -> None:
    print(f"[asset_loader] SKIP {reason}: {path}")


def import_sketchfab(
    uid: str,
    location: Vec3,
    rotation: Vec3 = (0.0, 0.0, 0.0),
    scale: float = 1.0,
) -> bpy.types.Object | None:
    """Load ``assets/sketchfab/<uid>/scene.gltf`` and return the root Empty.

    Returns None if the asset folder, scene.gltf, or gltf2 import operator is
    missing — caller should fall through to a procedural builder.
    """
    asset_dir = os.path.join(ASSETS_ROOT, 'sketchfab', uid)
    gltf_path = os.path.join(asset_dir, 'scene.gltf')
    if not os.path.isfile(gltf_path):
        _log_skip('sketchfab asset not on disk', gltf_path)
        return None

    parent = _make_parent(f"Asset_sketchfab_{uid[:8]}", location, rotation, scale)
    before = {o.name for o in bpy.data.objects}
    try:
        bpy.ops.import_scene.gltf(filepath=gltf_path)
    except Exception as exc:
        print(f"[asset_loader] gltf import failed for {uid}: {exc!r}")
        bpy.data.objects.remove(parent, do_unlink=True)
        return None
    adopted = _adopt_imported(parent, before)
    print(f"[asset_loader] sketchfab {uid[:8]}: adopted {adopted} objects @ {location}")
    return parent


def import_blenderkit(
    asset_id: str,
    location: Vec3,
    rotation: Vec3 = (0.0, 0.0, 0.0),
    scale: float = 1.0,
) -> bpy.types.Object | None:
    """Append every object from ``assets/blenderkit/<asset_id>.blend``.

    Uses ``wm.append`` with link=False so the asset becomes part of the .blend
    on save. Returns None if the file is missing or no objects were appended.
    """
    blend_path = os.path.join(ASSETS_ROOT, 'blenderkit', f"{asset_id}.blend")
    if not os.path.isfile(blend_path):
        _log_skip('blenderkit asset not on disk', blend_path)
        return None

    parent = _make_parent(f"Asset_blenderkit_{asset_id[:8]}", location, rotation, scale)
    before = {o.name for o in bpy.data.objects}
    try:
        with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
            data_to.objects = list(data_from.objects)
    except Exception as exc:
        print(f"[asset_loader] blenderkit load failed for {asset_id}: {exc!r}")
        bpy.data.objects.remove(parent, do_unlink=True)
        return None

    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)

    adopted = _adopt_imported(parent, before)
    if adopted == 0:
        print(f"[asset_loader] blenderkit {asset_id}: no objects in .blend, removing empty")
        bpy.data.objects.remove(parent, do_unlink=True)
        return None
    print(f"[asset_loader] blenderkit {asset_id[:8]}: adopted {adopted} objects @ {location}")
    return parent


def import_polyhaven_model(
    slug: str,
    location: Vec3,
    rotation: Vec3 = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    res: str = '4k',
) -> bpy.types.Object | None:
    """Append from ``assets/polyhaven/models/<slug>/<slug>_<res>.blend``."""
    model_dir = os.path.join(ASSETS_ROOT, 'polyhaven', 'models', slug)
    blend_path = os.path.join(model_dir, f"{slug}_{res}.blend")
    if not os.path.isfile(blend_path):
        _log_skip('polyhaven model not on disk', blend_path)
        return None

    parent = _make_parent(f"Asset_polyhaven_{slug}", location, rotation, scale)
    before = {o.name for o in bpy.data.objects}
    try:
        with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
            data_to.objects = list(data_from.objects)
    except Exception as exc:
        print(f"[asset_loader] polyhaven load failed for {slug}: {exc!r}")
        bpy.data.objects.remove(parent, do_unlink=True)
        return None
    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)
    adopted = _adopt_imported(parent, before)
    if adopted == 0:
        bpy.data.objects.remove(parent, do_unlink=True)
        return None
    print(f"[asset_loader] polyhaven {slug}: adopted {adopted} objects @ {location}")
    return parent


def is_available(source: str, identifier: str) -> bool:
    """Cheap existence probe used by flora builders before they call import_*.

    ``source`` ∈ {'sketchfab', 'blenderkit', 'polyhaven'}.
    """
    if source == 'sketchfab':
        return os.path.isfile(os.path.join(ASSETS_ROOT, 'sketchfab', identifier, 'scene.gltf'))
    if source == 'blenderkit':
        return os.path.isfile(os.path.join(ASSETS_ROOT, 'blenderkit', f"{identifier}.blend"))
    if source == 'polyhaven':
        return any(
            fname.endswith('.blend')
            for fname in os.listdir(os.path.join(ASSETS_ROOT, 'polyhaven', 'models', identifier))
        ) if os.path.isdir(os.path.join(ASSETS_ROOT, 'polyhaven', 'models', identifier)) else False
    return False
