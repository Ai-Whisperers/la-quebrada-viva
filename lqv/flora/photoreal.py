"""Photoreal flora importers — Poly Haven CC0 .blend appenders.

These replace the procedural builders in the gallery and any future scene that
opts into `RENDER_FLORA_PHOTOREAL=1`. Pattern mirrors
`lqv.subscene.terrain_62ha_photoreal._append_object_from_blend`: load all
objects, pick the largest mesh by polygon count, drop everything else, return
the hero.

Mapping (procedural → photoreal):

| Procedural builder    | Photoreal source (Poly Haven CC0, 4k) |
| --------------------- | ------------------------------------- |
| add_lapacho           | jacaranda_tree (foliage re-tinted pink when flowering) |
| add_mango             | pachira_aquatica_01 (broad tropical canopy proxy) |
| add_tree_fern         | fern_02 |
| scatter_anthuriums    | anthurium_botany_01 (exact match) |

Pindo palm and bamboo clump remain procedural — neither species (nor a close
visual proxy) exists in the Poly Haven catalog and the Sketchfab CC-BY path is
blocked while the MCP socket is dead.
"""
from __future__ import annotations

import os

import bpy
from mathutils import Vector

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_DIR = os.path.join(_PROJECT_ROOT, "assets", "models")

JACARANDA_BLEND = os.path.join(MODEL_DIR, "jacaranda_tree", "jacaranda_tree_4k.blend")
PACHIRA_BLEND = os.path.join(MODEL_DIR, "pachira_aquatica_01", "pachira_aquatica_01_4k.blend")
FERN_BLEND = os.path.join(MODEL_DIR, "fern_02", "fern_02_4k.blend")
ANTHURIUM_BLEND = os.path.join(MODEL_DIR, "anthurium_botany_01", "anthurium_botany_01_4k.blend")

# Bug 3 fix: re-appending the same .blend auto-suffixes objects (`.001`, `.002`,
# …) and the suffixed orphans break later unlink-by-name lookups. We append
# once per blend, cache the hero, and deep-copy on subsequent calls.
_LOADED_HEROES: dict[str, bpy.types.Object] = {}


def _safe_unlink_from_active(obj: bpy.types.Object) -> None:
    coll = bpy.context.collection
    if obj.name in coll.objects:
        try:
            coll.objects.unlink(obj)
        except RuntimeError:
            pass


def _append_object_from_blend(blend_path: str) -> bpy.types.Object:
    """Append every object from `blend_path`, link the largest mesh, return it.

    Idempotent across repeat calls: first call appends + caches the hero;
    subsequent calls deep-copy from the cache so the underlying Blender
    library never re-loads (avoiding the `.001`/`.002` suffix collision).
    """
    cached = _LOADED_HEROES.get(blend_path)
    if cached is not None and cached.name in bpy.data.objects:
        dup = cached.copy()
        if cached.data is not None:
            dup.data = cached.data.copy()
        bpy.context.collection.objects.link(dup)
        return dup

    if not os.path.exists(blend_path):
        raise SystemExit(f"missing asset blend: {blend_path}")
    before = set(bpy.data.objects.keys())
    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        data_to.objects = list(data_from.objects)
    new_objs = [bpy.data.objects[n] for n in bpy.data.objects.keys() if n not in before]
    mesh_objs = [o for o in new_objs if o.type == "MESH" and o.data is not None]
    if not mesh_objs:
        raise SystemExit(f"no mesh objects found in {blend_path}")
    mesh_objs.sort(key=lambda o: len(o.data.polygons), reverse=True)
    hero = mesh_objs[0]
    for o in new_objs:
        _safe_unlink_from_active(o)
    bpy.context.collection.objects.link(hero)
    _LOADED_HEROES[blend_path] = hero
    return hero


def _place(obj: bpy.types.Object, x: float, y: float, z: float, scale: float, rot_z: float = 0.0):
    obj.location = (x, y, z)
    obj.scale = (scale, scale, scale)
    obj.rotation_euler = (0.0, 0.0, rot_z)


def _scale_to_height(obj: bpy.types.Object, target_height_m: float):
    """Uniformly scale obj so its world-space Z extent matches target_height_m, then
    translate vertically so its base sits at z=0."""
    bpy.context.view_layer.update()
    bbox = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    zs = [v.z for v in bbox]
    cur_h = max(zs) - min(zs)
    if cur_h <= 1e-6:
        return
    factor = target_height_m / cur_h
    obj.scale = tuple(s * factor for s in obj.scale)
    bpy.context.view_layer.update()
    bbox2 = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    min_z = min(v.z for v in bbox2)
    obj.location = (obj.location.x, obj.location.y, obj.location.z - min_z)


def _classify_material(mat) -> str:
    """Inspect Image Texture nodes feeding the Principled BSDF and classify the
    material as 'structural' (bark/trunk/branches/wood), 'foliage' (leaves/flowers),
    or 'unknown'. Decision is by image filename, not material name — Poly Haven
    materials are often named after the asset, not the slot purpose."""
    if mat is None or not mat.use_nodes:
        return "unknown"
    structural_tags = ("trunk", "bark", "branch", "wood", "stem")
    foliage_tags = ("leaves", "leaf", "foliage", "flower", "petal", "frond")
    files = []
    for node in mat.node_tree.nodes:
        if node.type == "TEX_IMAGE" and node.image is not None:
            files.append((node.image.filepath or node.image.name or "").lower())
    if any(any(tag in f for tag in structural_tags) for f in files):
        return "structural"
    if any(any(tag in f for tag in foliage_tags) for f in files):
        return "foliage"
    return "unknown"


def _tint_foliage_pink(obj: bpy.types.Object):
    """Push lapacho-pink onto leaf materials only. Skips structural materials by
    Image-Texture filename inspection. Preserves the leaf diffuse texture by
    blending pink through a MixRGB (Color blend) node rather than clobbering
    the Base Color input."""
    pink = (0.95, 0.45, 0.65, 1.0)
    for slot in obj.material_slots:
        mat = slot.material
        kind = _classify_material(mat)
        if kind == "structural":
            continue
        if kind == "unknown":
            continue
        bsdf = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if bsdf is None:
            continue
        base = bsdf.inputs["Base Color"]
        if base.is_linked:
            link = base.links[0]
            src_socket = link.from_socket
            mat.node_tree.links.remove(link)
            mix = mat.node_tree.nodes.new("ShaderNodeMixRGB")
            mix.blend_type = "COLOR"
            mix.inputs["Fac"].default_value = 0.7
            mix.inputs["Color2"].default_value = pink
            mat.node_tree.links.new(src_socket, mix.inputs["Color1"])
            mat.node_tree.links.new(mix.outputs["Color"], base)
        else:
            base.default_value = pink


TARGET_HEIGHTS = {
    "lapacho": 8.0,
    "mango": 5.0,
    "tree_fern": 2.0,
    "anthurium": 0.5,
}


def add_lapacho_photoreal(x: float = 0.0, y: float = 0.0, scale: float = 1.0, *, flowering: bool = True) -> bpy.types.Object:
    """Photoreal lapacho via jacaranda_tree_4k. Foliage tinted pink when flowering."""
    hero = _append_object_from_blend(JACARANDA_BLEND)
    _place(hero, x, y, 0.0, scale)
    _scale_to_height(hero, TARGET_HEIGHTS["lapacho"])
    if flowering:
        _tint_foliage_pink(hero)
    return hero


def add_mango_photoreal(x: float = 0.0, y: float = 0.0, scale: float = 1.0) -> bpy.types.Object:
    """Photoreal mango proxy via pachira_aquatica_01 (broad tropical canopy)."""
    hero = _append_object_from_blend(PACHIRA_BLEND)
    _place(hero, x, y, 0.0, scale)
    _scale_to_height(hero, TARGET_HEIGHTS["mango"])
    return hero


def add_tree_fern_photoreal(x: float = 0.0, y: float = 0.0, scale: float = 1.0) -> bpy.types.Object:
    """Photoreal tree fern via fern_02."""
    hero = _append_object_from_blend(FERN_BLEND)
    _place(hero, x, y, 0.0, scale)
    _scale_to_height(hero, TARGET_HEIGHTS["tree_fern"])
    return hero


def add_anthurium_photoreal(x: float = 0.0, y: float = 0.0, scale: float = 1.0) -> bpy.types.Object:
    """Photoreal anthurium via anthurium_botany_01 (exact species match)."""
    hero = _append_object_from_blend(ANTHURIUM_BLEND)
    _place(hero, x, y, 0.0, scale)
    _scale_to_height(hero, TARGET_HEIGHTS["anthurium"])
    return hero


__all__ = [
    "add_lapacho_photoreal",
    "add_mango_photoreal",
    "add_tree_fern_photoreal",
    "add_anthurium_photoreal",
]
