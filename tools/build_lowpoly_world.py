#!/usr/bin/env python3
"""LQV 3D World Builder — Blender headless asset pipeline.

Generates the low-poly Zelda-style asset pack for the LQV 3D world builder.

Output (to /root/la-quebrada-viva/docs/game_assets/lowpoly/):
  - lqv_lowpoly_terrain.glb       (50k tris, flat-shaded stepped terrain)
  - lqv_lowpoly_road.glb           (low-poly walking path overlay)
  - lqv_lowpoly_waterfall.glb      (waterfall mesh + particle placeholder)
  - lqv_lowpoly_rock_cluster.glb   (rocks for cliffs)
  - lqv_lowpoly_monte.glb          (highlighted monte/escarpment)
  - lqv_lowpoly_tree_lapacho.glb   (pink-flowering tree)
  - lqv_lowpoly_tree_palmera.glb   (palm silhouette)
  - lqv_lowpoly_tree_pino.glb      (pine / Atlantic Forest canopy)
  - lqv_lowpoly_house_cob.glb      (Zelda-style cob house, thatched roof)
  - lqv_lowpoly_typo_set.glb       (5 typology placeholders: cob, tatakua,
                                    worker housing, wigwam, glamping tent)

Style: Zelda BotW-inspired + Atlantic Forest palette.
  Grass: #7a9b4e, Earth: #8a6a3a, Rock: #6e6258,
  Cob walls: #d4a154, Thatch: #a8895a, Stone chimney: #4a4540,
  Sky/water: #5b9dd9, Lapacho: #d4956a + pink flowers.

Run:
  blender --background --python tools/build_lowpoly_world.py
"""
import bpy
import bmesh
import os
import math
import sys
import random
from mathutils import Vector

# ---------- Configuration ----------
OUT_DIR = "/root/la-quebrada-viva/docs/game_assets/lowpoly"
os.makedirs(OUT_DIR, exist_ok=True)

# Color palette (Zelda-style)
PAL = {
    "grass":     (0.478, 0.608, 0.306),  # #7a9b4e
    "grass_dk":  (0.239, 0.353, 0.165),  # #3d5a2a
    "earth":     (0.541, 0.416, 0.227),  # #8a6a3a
    "earth_lt":  (0.690, 0.561, 0.376),
    "rock":      (0.431, 0.384, 0.345),  # #6e6258
    "rock_dk":   (0.290, 0.271, 0.251),
    "water":     (0.357, 0.616, 0.851),  # #5b9dd9
    "cob":       (0.831, 0.631, 0.329),  # #d4a154
    "cob_dk":    (0.541, 0.416, 0.227),
    "thatch":    (0.659, 0.537, 0.353),  # #a8895a
    "stone":     (0.290, 0.271, 0.251),
    "wood":      (0.227, 0.180, 0.133),
    "lapacho_a": (0.831, 0.584, 0.416),  # warm pink-yellow (lapacho flowers)
    "lapacho_b": (0.659, 0.388, 0.490),  # cool pink (lapacho variant)
    "pino_dk":   (0.122, 0.220, 0.137),  # dark Atlantic Forest
    "pino_lt":   (0.290, 0.451, 0.227),
    "sky":       (0.910, 0.847, 0.690),
}

# ---------- Helpers ----------
def reset_scene():
    """Clear all objects + reset to factory."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # Disable cycles GPU requirement — we render with Eevee (or just export GLB, no render)
    try:
        bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
    except Exception:
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    # World background = warm sky
    world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (*PAL["sky"], 1.0)


def make_material(name, rgb, roughness=0.85, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    # Make it look low-poly: disable smooth shading via face attribute
    return mat


def set_flat_shading(obj):
    """Force flat shading (low-poly faceted look)."""
    for poly in obj.data.polygons:
        poly.use_smooth = False


def export_glb(filepath, objects=None):
    """Export GLB. If objects is None, export all."""
    if objects is not None:
        # Hide everything not in objects list
        all_objs = list(bpy.data.objects)
        for o in all_objs:
            o.hide_render = o not in objects
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        use_selection=False,
        export_materials='EXPORT',
        export_apply=True,
    )
    # Un-hide
    for o in bpy.data.objects:
        o.hide_render = False
    print(f"  → wrote {filepath} ({os.path.getsize(filepath)/1024:.1f} KB)")


# ============================================================
# 1. TERRAIN — flat-shaded stepped mesh from real DEM
# ============================================================
def build_terrain():
    """Read the DEM heightmap PNG, build stepped low-poly mesh.

    Source: /root/la-quebrada-viva/docs/game_assets/heightmaps/lqv_terrain_height_16bit.png
    The 16-bit PNG encodes elevation (m × 100) into [0, 65535].
    Z scale = 100 means 1m of elevation = 1 unit in Blender.
    """
    reset_scene()
    import numpy as np
    from PIL import Image

    dem_path = "/root/la-quebrada-viva/docs/game_assets/heightmaps/lqv_terrain_height_16bit.png"
    if not os.path.exists(dem_path):
        print(f"ERROR: DEM not found at {dem_path}")
        return None

    # Load 16-bit grayscale
    img = Image.open(dem_path)
    arr = np.array(img)
    print(f"  DEM shape: {arr.shape}, dtype: {arr.dtype}, min/max: {arr.min()}/{arr.max()}")

    # The terrain_height_16bit.png is 16-bit: value = elevation_m * (65535 / elev_max)
    # Convert: elev_m = value * 65.0 / 65535 ≈ value / 1008
    # But our pipeline encoded: pixel = elevation_m × 100, so elev_m = pixel / 100
    # Verify with metadata
    meta_path = "/root/la-quebrada-viva/docs/game_assets/heightmaps/lqv_terrain_metadata.json"
    if os.path.exists(meta_path):
        import json
        meta = json.loads(open(meta_path).read())
        z_scale = meta.get("z_scale_meters", 1.0)
        xy_scale = meta.get("xy_scale_meters", 1.0)
        elev_min = meta.get("elevation_min_m", 0)
        elev_max = meta.get("elevation_max_m", 400)
    else:
        z_scale = 1.0
        xy_scale = 1.0
        elev_min, elev_max = 100, 400

    # Convert: for the 16-bit PNG, pixel/65535 * (elev_max - elev_min) + elev_min
    # Read DEM metadata for the canonical decode (z_scale_meters_per_unit is what we use)
    if os.path.exists(meta_path):
        import json
        meta = json.loads(open(meta_path).read())
        z_scale = meta.get("z_scale_meters", 1.0)
        xy_scale = meta.get("xy_scale_meters", 1.0)
        elev_min_meta = meta.get("elevation_min_m", 0)
        elev_max_meta = meta.get("elevation_max_m", 400)
        # The 16-bit PNG encoded: pixel = (elevation_m - elev_min) / (elev_max - elev_min) * 65535
        # Decode:
        elev_m = arr.astype(np.float32) / 65535.0 * (elev_max_meta - elev_min_meta) + elev_min_meta
        elev_min, elev_max = elev_min_meta, elev_max_meta
    else:
        z_scale = 1.0
        xy_scale = 1.0
        elev_min, elev_max = 100, 400
        elev_m = arr.astype(np.float32)
    print(f"  Elevation: min={elev_m.min():.0f}m, max={elev_m.max():.0f}m, median={np.median(elev_m):.0f}m")

    # Downsample for low-poly look (target ~150-300x300 grid → 90k tris max but stepped)
    # Step 1: quantize to 2m elevation bands (Zelda aesthetic — visible "stairs")
    STEP_ELEV = 1.5  # metres per band
    elev_quantized = np.round(elev_m / STEP_ELEV) * STEP_ELEV

    # Step 2: decimate in XY for "blocky" low-poly
    TARGET_GRID = 160  # 160×160 = 25,600 cells = 51,200 tris
    H, W = elev_quantized.shape
    sx = max(1, W // TARGET_GRID)
    sy = max(1, H // TARGET_GRID)
    elev_small = elev_quantized[::sy, ::sx]
    print(f"  Downsampled to {elev_small.shape}, sx={sx} sy={sy}")

    # Build mesh
    h2, w2 = elev_small.shape
    verts = []
    faces = []
    for j in range(h2):
        for i in range(w2):
            x = i * 1.0  # 1 unit = 1 metre (will scale later)
            y = j * 1.0
            z = elev_small[j, i] * z_scale
            verts.append((x, y, z))
    for j in range(h2 - 1):
        for i in range(w2 - 1):
            v0 = j * w2 + i
            v1 = v0 + 1
            v2 = v0 + w2
            v3 = v2 + 1
            faces.append((v0, v1, v3, v2))

    mesh = bpy.data.meshes.new("LQV_Terrain")
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    obj = bpy.data.objects.new("LQV_Terrain", mesh)
    bpy.context.collection.objects.link(obj)

    # UVs (for satellite drape if used later)
    uv_layer = mesh.uv_layers.new(name="UVMap")
    for poly in mesh.polygons:
        for loop_idx in poly.loop_indices:
            vi = mesh.loops[loop_idx].vertex_index
            i = vi % w2
            j = vi // w2
            uv_layer.data[loop_idx].uv = (i / (w2 - 1), j / (h2 - 1))

    # FLAT SHADING — the entire point of low-poly retro
    set_flat_shading(obj)

    # Vertex colors based on elevation + slope
    # We need to compute slope too — use the quantized grid
    slp = np.zeros_like(elev_small)
    slp[:-1, :] = np.abs(np.diff(elev_small, axis=0))
    slp[:, :-1] = np.maximum(slp[:, :-1], np.abs(np.diff(elev_small, axis=1)))
    slp_max = slp.max() if slp.max() > 0 else 1.0

    vc = mesh.vertex_colors.new(name="Col")
    grass = PAL["grass"]
    earth = PAL["earth"]
    rock = PAL["rock"]
    rock_dk = PAL["rock_dk"]
    grass_dk = PAL["grass_dk"]
    water = PAL["water"]

    # Pre-compute min/max elevation for color ramp
    emin = elev_small.min()
    emax = elev_small.max()
    erange = emax - emin if emax > emin else 1.0

    for poly in mesh.polygons:
        # Average elevation of vertices in this face
        avg_e = sum(verts[mesh.loops[l].vertex_index][2] for l in poly.loop_indices) / len(poly.loop_indices)
        # Average slope (rough)
        avg_s = 0.0
        for l in poly.loop_indices:
            vi = mesh.loops[l].vertex_index
            i = vi % w2
            j = vi // w2
            if 0 < j < h2 - 1 and 0 < i < w2 - 1:
                avg_s += slp[j, i]
        avg_s /= max(1, len(poly.loop_indices))

        # Color rule: low = grass, mid = earth, high+steep = rock
        t = (avg_e - emin) / erange  # 0=low, 1=high
        if avg_s > 4.0:  # steep
            r, g, b = rock
        elif t < 0.4:
            r, g, b = grass
        elif t < 0.7:
            # Blend earth→rock based on slope
            blend = min(1.0, avg_s / 3.0)
            r = earth[0] * (1-blend) + rock[0] * blend
            g = earth[1] * (1-blend) + rock[1] * blend
            b = earth[2] * (1-blend) + rock[2] * blend
        else:
            r, g, b = earth

        for l in poly.loop_indices:
            vc.data[l].color = (r, g, b, 1.0)

    # Material with vertex colors
    mat = make_material("Terrain_VertexColor", (1, 1, 1))
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        # Add vertex color node → mix with base
        nodes = mat.node_tree.nodes
        vc_node = nodes.new("ShaderNodeVertexColor")
        vc_node.layer_name = "Col"
        vc_node.location = (-300, 200)
        # Connect: vertex color → bsdf base color
        mat.node_tree.links.new(vc_node.outputs["Color"], bsdf.inputs["Base Color"])

    obj.data.materials.append(mat)

    # Apply scale: 1 unit in Blender = 1 metre, but we want 1 unit = ~1m, terrain extends ~1km
    # Already at 1 unit = 1m. The mesh is ~160m × ~160m. That's the parcel scale.
    # For wider context we'll add a separate bigger mesh if needed.

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    print(f"  Terrain: {len(verts)} verts, {len(faces)} faces")
    return obj


# ============================================================
# 2. ARCHETYPES — trees, rocks, monte, waterfall, gate, trail
# ============================================================
def build_archetypes():
    """Build each archetype as its own GLB. Each is one mesh."""
    import random
    random.seed(42)

    arch_dir = OUT_DIR
    os.makedirs(arch_dir, exist_ok=True)

    def archetype_tree_lapacho():
        """Pink-flowering Atlantic Forest tree."""
        reset_scene()
        # Trunk: tapered cylinder, 6 segments
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=6, radius=0.18, depth=3.2, location=(0, 0, 1.6)
        )
        trunk = bpy.context.object
        trunk.name = "Lapacho_trunk"
        set_flat_shading(trunk)
        trunk.data.materials.append(make_material("Lapacho_trunk_mat", PAL["wood"], roughness=0.9))

        # 3 "blobs" for canopy (lapacho has spreading, irregular canopy)
        for dx, dy, dz, r in [(0, 0, 3.5, 1.5), (0.6, 0.3, 3.0, 1.2),
                               (-0.5, 0.4, 3.2, 1.3), (0.2, -0.5, 3.7, 1.1)]:
            bpy.ops.mesh.primitive_ico_sphere_add(
                radius=r, subdivisions=1, location=(dx, dy, dz)
            )
            blob = bpy.context.object
            blob.name = f"Lapacho_blob_{dx:.1f}"
            set_flat_shading(blob)
            # Alternate the lapacho flower color
            col = PAL["lapacho_a"] if abs(dx) > 0.3 else PAL["lapacho_b"]
            blob.data.materials.append(make_material(f"Lapacho_canopy_mat", col, roughness=0.9))
        export_glb(f"{arch_dir}/lqv_lowpoly_tree_lapacho.glb")

    def archetype_tree_palmera():
        """Palm tree — straight trunk + 7 fronds."""
        reset_scene()
        # Trunk: simple cylinder, tapered by scaling top vertices in edit mode
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=6, radius=0.22, depth=4.5, location=(0, 0, 2.25)
        )
        trunk = bpy.context.object
        trunk.name = "Palmera_trunk"
        # Taper top: edit-mode vertex scaling
        bpy.context.view_layer.objects.active = trunk
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(trunk.data)
        for v in bm.verts:
            if v.co.z > 1.5:
                v.co.x *= 0.55
                v.co.y *= 0.55
        bmesh.update_edit_mesh(trunk.data, loop_triangles=False, destructive=True)
        bpy.ops.object.mode_set(mode='OBJECT')
        set_flat_shading(trunk)
        trunk.data.materials.append(make_material("Palmera_trunk_mat", PAL["wood"], roughness=0.9))

        # Fronds: 7 elongated triangles arranged radially
        for i in range(7):
            angle = i * (2 * math.pi / 7)
            dx = math.cos(angle) * 1.8
            dy = math.sin(angle) * 1.8
            # Each frond is a flat tapered plane
            verts = [
                (0, 0, 4.5),          # base at top of trunk
                (dx * 0.6, dy * 0.6, 4.4),  # mid (slightly droop)
                (dx, dy, 3.9),         # tip (droops down)
            ]
            edges = [(0, 1), (1, 2), (2, 0)]
            faces = [(0, 1, 2)]
            mesh = bpy.data.meshes.new(f"Frond_{i}")
            mesh.from_pydata(verts, edges, faces)
            mesh.update()
            obj = bpy.data.objects.new(f"Frond_{i}", mesh)
            bpy.context.collection.objects.link(obj)
            set_flat_shading(obj)
            obj.data.materials.append(make_material(f"Frond_mat", PAL["pino_lt"], roughness=0.85))
        export_glb(f"{arch_dir}/lqv_lowpoly_tree_palmera.glb")

    def archetype_tree_pino():
        """Pine / Atlantic Forest canopy — conical, dark green."""
        reset_scene()
        # Trunk
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=6, radius=0.15, depth=2.5, location=(0, 0, 1.25)
        )
        trunk = bpy.context.object
        trunk.name = "Pino_trunk"
        set_flat_shading(trunk)
        trunk.data.materials.append(make_material("Pino_trunk_mat", PAL["wood_dk"] if "wood_dk" in PAL else PAL["wood"], roughness=0.9))

        # 3 stacked cones for layered canopy
        for i, (z, r) in enumerate([(2.8, 1.6), (4.0, 1.2), (5.0, 0.7)]):
            bpy.ops.mesh.primitive_cone_add(
                vertices=7, radius1=r, radius2=0.05, depth=1.5,
                location=(0, 0, z)
            )
            # ^^ cone_add still uses radius1/radius2/depth in Blender 4.0
            cone = bpy.context.object
            cone.name = f"Pino_cone_{i}"
            set_flat_shading(cone)
            col = PAL["pino_dk"] if i % 2 == 0 else PAL["pino_lt"]
            cone.data.materials.append(make_material(f"Pino_cone_mat_{i}", col, roughness=0.95))
        export_glb(f"{arch_dir}/lqv_lowpoly_tree_pino.glb")

    def archetype_rock_cluster():
        """5 rocks of varying sizes, clustered."""
        reset_scene()
        random.seed(13)
        for i in range(5):
            r = random.uniform(0.4, 1.2)
            bpy.ops.mesh.primitive_ico_sphere_add(
                radius=r, subdivisions=1,
                location=(random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5), r * 0.6)
            )
            rock = bpy.context.object
            # Squish slightly
            rock.scale = (1.0, 1.0, 0.7)
            rock.name = f"Rock_{i}"
            set_flat_shading(rock)
            col = PAL["rock"] if i % 2 == 0 else PAL["rock_dk"]
            rock.data.materials.append(make_material(f"Rock_mat_{i}", col, roughness=0.95))
        export_glb(f"{arch_dir}/lqv_lowpoly_rock_cluster.glb")

    def archetype_waterfall():
        """Vertical water mesh (animated UV scroll in actual game)."""
        reset_scene()
        # Back panel: rocky face
        verts = [
            (-1.5, -0.3, 5.0),  # top left
            (1.5, -0.3, 5.0),   # top right
            (1.5, -0.3, 0.0),   # bottom right
            (-1.5, -0.3, 0.0),  # bottom left
        ]
        faces = [(0, 1, 2, 3)]
        mesh = bpy.data.meshes.new("Waterfall_back")
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        back = bpy.data.objects.new("Waterfall_back", mesh)
        bpy.context.collection.objects.link(back)
        set_flat_shading(back)
        back.data.materials.append(make_material("Waterfall_rock_mat", PAL["rock_dk"]))

        # Water sheet: 3 vertical strips with different widths for "tiered" look
        for i, (top, bot, off) in enumerate([(0.6, -0.6, 0.1), (-0.3, 0.3, 0.05), (-0.6, -0.6, 0.0)]):
            verts = [
                (top - 0.6, 0.0, 5.0), (top + 0.6, 0.0, 5.0),
                (bot + 0.4, 0.0, 0.0), (bot - 0.4, 0.0, 0.0),
            ]
            faces = [(0, 1, 2, 3)]
            mesh = bpy.data.meshes.new(f"Water_sheet_{i}")
            mesh.from_pydata(verts, [], faces)
            obj = bpy.data.objects.new(f"Water_sheet_{i}", mesh)
            bpy.context.collection.objects.link(obj)
            set_flat_shading(obj)
            obj.data.materials.append(make_material(f"Water_sheet_mat_{i}", PAL["water"], roughness=0.3, metallic=0.0))
        # Splash pool at the base
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=10, radius=1.2, depth=0.15, location=(0, 0, 0.05)
        )
        pool = bpy.context.object
        pool.name = "Splash_pool"
        set_flat_shading(pool)
        pool.data.materials.append(make_material("Splash_pool_mat", PAL["water"], roughness=0.4))
        export_glb(f"{arch_dir}/lqv_lowpoly_waterfall.glb")

    def archetype_monte():
        """Stylized 'monte' / escarpment — a triangular silhouette mesh."""
        reset_scene()
        # Triangular peak with stepped facets
        verts = [
            (0, 0, 12),         # peak
            (-8, 4, 0),         # base front-left
            (8, 4, 0),          # base front-right
            (-6, -8, 0),        # base back-left
            (6, -8, 0),         # base back-right
            (0, 10, 3),         # shoulder front
        ]
        faces = [
            (0, 1, 5), (0, 5, 2),    # front faces
            (0, 2, 4), (0, 4, 3),    # back faces
            (0, 3, 1),               # left side
            (5, 1, 2),               # base front
            (4, 2, 5),               # base right
            (3, 4, 2), (2, 1, 5),    # base bottom
        ]
        mesh = bpy.data.meshes.new("Monte")
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        obj = bpy.data.objects.new("Monte", mesh)
        bpy.context.collection.objects.link(obj)
        set_flat_shading(obj)
        # Rock material with vertical gradient via vertex colors
        vc = mesh.vertex_colors.new(name="Col")
        for poly in mesh.polygons:
            avg_z = sum(verts[mesh.loops[l].vertex_index][2] for l in poly.loop_indices) / len(poly.loop_indices)
            t = avg_z / 12.0  # 0=base, 1=peak
            col = (
                PAL["rock_dk"][0] * (1-t) + PAL["rock"][0] * t,
                PAL["rock_dk"][1] * (1-t) + PAL["rock"][1] * t,
                PAL["rock_dk"][2] * (1-t) + PAL["rock"][2] * t,
                1.0,
            )
            for l in poly.loop_indices:
                vc.data[l].color = col
        mat = make_material("Monte_mat", (1, 1, 1))
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            vc_node = mat.node_tree.nodes.new("ShaderNodeVertexColor")
            vc_node.location = (-300, 200)
            mat.node_tree.links.new(vc_node.outputs["Color"], bsdf.inputs["Base Color"])
        obj.data.materials.append(mat)
        export_glb(f"{arch_dir}/lqv_lowpoly_monte.glb")

    def archetype_gate():
        """LQV gate — two stone pillars + wooden lintel with carved sign."""
        reset_scene()
        # Two pillars
        for x in (-1.0, 1.0):
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=6, radius=0.3, depth=2.4, location=(x, 0, 1.2)
            )
            p = bpy.context.object
            p.name = f"Gate_pillar_{x}"
            set_flat_shading(p)
            p.data.materials.append(make_material("Gate_pillar_mat", PAL["rock"]))
        # Lintel
        verts = [
            (-1.3, 0, 2.4), (1.3, 0, 2.4),
            (1.3, 0, 2.8), (-1.3, 0, 2.8),
        ]
        faces = [(0, 1, 2, 3), (0, 3, 2, 1)]  # double-sided
        mesh = bpy.data.meshes.new("Gate_lintel")
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        obj = bpy.data.objects.new("Gate_lintel", mesh)
        bpy.context.collection.objects.link(obj)
        set_flat_shading(obj)
        obj.data.materials.append(make_material("Gate_lintel_mat", PAL["wood"]))
        export_glb(f"{arch_dir}/lqv_lowpoly_gate.glb")

    def archetype_trail():
        """Walking path — earth-tone strip with subtle width variation."""
        reset_scene()
        # Build a 20-segment curve as flat ribbon
        random.seed(7)
        path_verts = []
        for i in range(40):
            t = i / 39
            x = -30 + 60 * t
            # meandering y
            y = math.sin(t * 6 * math.pi) * 2 + math.sin(t * 11 * math.pi) * 0.5
            # elevation rising
            z = 0.05 + t * 1.5
            path_verts.append((x, y, z))
        # Build ribbon by extruding left/right
        ribbon_verts = []
        ribbon_faces = []
        for i, (x, y, z) in enumerate(path_verts):
            if i < len(path_verts) - 1:
                dx = path_verts[i+1][0] - x
                dy = path_verts[i+1][1] - y
                # Perpendicular in XY plane
                L = math.hypot(dx, dy) or 1.0
                nx, ny = -dy / L, dx / L
            else:
                nx, ny = 0, 1
            width = 0.4 + random.uniform(-0.1, 0.1)
            ribbon_verts.append((x + nx * width, y + ny * width, z))
            ribbon_verts.append((x - nx * width, y - ny * width, z))
        for i in range(len(path_verts) - 1):
            v0 = i * 2
            ribbon_faces.append((v0, v0+1, v0+3, v0+2))
        mesh = bpy.data.meshes.new("Trail")
        mesh.from_pydata(ribbon_verts, [], ribbon_faces)
        mesh.update()
        obj = bpy.data.objects.new("Trail", mesh)
        bpy.context.collection.objects.link(obj)
        set_flat_shading(obj)
        mat = make_material("Trail_mat", PAL["earth_lt"])
        obj.data.materials.append(mat)
        export_glb(f"{arch_dir}/lqv_lowpoly_trail.glb")

    # Build all archetypes
    print("\n=== Building archetypes ===")
    archetype_tree_lapacho()
    archetype_tree_palmera()
    archetype_tree_pino()
    archetype_rock_cluster()
    archetype_waterfall()
    archetype_monte()
    archetype_gate()
    archetype_trail()


# ============================================================
# 3. TYPO SET — 5 typology placeholders for click-to-place
# ============================================================
def build_typo_set():
    """Build the 5 typologies as separate objects in ONE GLB for click-to-place UI.

    Each typology has a recognizable silhouette + signature color.
    """
    reset_scene()
    # 1. Cob house (flagship) — bigger, more detail
    # Walls (rectangular base)
    bpy.ops.mesh.primitive_cube_add(size=4, location=(0, 0, 1.5))
    walls = bpy.context.object
    walls.name = "Typo_Cob"
    walls.scale = (1.0, 0.8, 0.75)
    set_flat_shading(walls)
    walls.data.materials.append(make_material("Typo_Cob_mat", PAL["cob"]))
    # Thatched roof (triangular prism)
    verts = [
        (-2.2, -1.7, 3.0), (2.2, -1.7, 3.0), (2.2, 1.7, 3.0), (-2.2, 1.7, 3.0),
        (0, -1.7, 5.0), (0, 1.7, 5.0),
    ]
    faces = [(0, 1, 5, 4), (1, 2, 5), (2, 3, 4, 5), (3, 0, 4), (0, 3, 2, 1)]
    mesh = bpy.data.meshes.new("Typo_Cob_roof")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    roof = bpy.data.objects.new("Typo_Cob_roof", mesh)
    bpy.context.collection.objects.link(roof)
    set_flat_shading(roof)
    roof.data.materials.append(make_material("Typo_thatch_mat", PAL["thatch"]))
    # Chimney
    bpy.ops.mesh.primitive_cube_add(size=0.4, location=(1.5, -1.0, 4.2))
    chim = bpy.context.object
    chim.name = "Typo_Cob_chimney"
    set_flat_shading(chim)
    chim.data.materials.append(make_material("Typo_stone_mat", PAL["stone"]))
    # Door
    bpy.ops.mesh.primitive_cube_add(size=0.7, location=(0, 1.7, 1.0))
    door = bpy.context.object
    door.name = "Typo_Cob_door"
    door.scale = (1, 0.1, 1.4)
    set_flat_shading(door)
    door.data.materials.append(make_material("Typo_wood_mat", PAL["wood"]))
    bpy.ops.object.select_all(action='DESELECT')
    export_glb(f"{OUT_DIR}/lqv_lowpoly_house_cob.glb", objects=[walls, roof, chim, door])

    # 2. Tatakua (outdoor oven + dining)
    reset_scene()
    # Dome oven
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.8, subdivisions=2, location=(0, 0, 0.8))
    oven = bpy.context.object
    oven.name = "Typo_Tatakua_oven"
    oven.scale = (1.2, 1.0, 0.8)
    set_flat_shading(oven)
    oven.data.materials.append(make_material("Typo_Tatakua_mat", PAL["cob"]))
    # Chimney opening
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.2, depth=0.5, location=(0.4, 0, 1.2))
    ch = bpy.context.object
    ch.name = "Typo_Tatakua_chimney"
    set_flat_shading(ch)
    ch.data.materials.append(make_material("Typo_stone_mat", PAL["stone"]))
    # Dining table (low)
    bpy.ops.mesh.primitive_cube_add(size=1.8, location=(0, 2.5, 0.4))
    table = bpy.context.object
    table.scale = (1.5, 0.6, 0.15)
    set_flat_shading(table)
    table.data.materials.append(make_material("Typo_wood_mat", PAL["wood"]))
    export_glb(f"{OUT_DIR}/lqv_lowpoly_typo_tatakua.glb", objects=[oven, ch, table])

    # 3. Worker housing (long rectangle)
    reset_scene()
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
    wh = bpy.context.object
    wh.name = "Typo_Worker"
    wh.scale = (4.0, 0.8, 1.0)
    set_flat_shading(wh)
    wh.data.materials.append(make_material("Typo_Worker_mat", PAL["earth_lt"]))
    # Corrugated metal roof
    verts = [
        (-8.2, -0.9, 2.0), (8.2, -0.9, 2.0), (8.2, 0.9, 2.0), (-8.2, 0.9, 2.0),
        (0, -0.9, 2.5), (0, 0.9, 2.5),
    ]
    faces = [(0, 1, 5, 4), (1, 2, 5), (2, 3, 4, 5), (3, 0, 4)]
    mesh = bpy.data.meshes.new("Worker_roof")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    wroof = bpy.data.objects.new("Worker_roof", mesh)
    bpy.context.collection.objects.link(wroof)
    set_flat_shading(wroof)
    wroof.data.materials.append(make_material("Typo_metal_mat", PAL["rock"]))
    export_glb(f"{OUT_DIR}/lqv_lowpoly_typo_worker.glb", objects=[wh, wroof])

    # 4. Bamboo wigwam (cone hut)
    reset_scene()
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=2.0, radius2=0.1, depth=3.5, location=(0, 0, 1.75))
    wg = bpy.context.object
    wg.name = "Typo_Wigwam"
    set_flat_shading(wg)
    wg.data.materials.append(make_material("Typo_Wigwam_mat", PAL["thatch"]))
    # Door opening (small dark cube as "shadow")
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 2.0, 0.6))
    wdoor = bpy.context.object
    wdoor.scale = (0.6, 0.05, 1.4)
    set_flat_shading(wdoor)
    wdoor.data.materials.append(make_material("Typo_wood_mat", PAL["wood"]))
    export_glb(f"{OUT_DIR}/lqv_lowpoly_typo_wigwam.glb", objects=[wg, wdoor])

    # 5. Glamping tent (low triangular tent)
    reset_scene()
    # Body
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=2.2, radius2=0.1, depth=1.8, location=(0, 0, 0.9))
    tent = bpy.context.object
    tent.name = "Typo_Glamping"
    set_flat_shading(tent)
    tent.data.materials.append(make_material("Typo_Glamping_mat", PAL["thatch"]))
    # Pole on top
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.03, depth=2.2, location=(0, 0, 1.9))
    pole = bpy.context.object
    pole.name = "Typo_Glamping_pole"
    set_flat_shading(pole)
    pole.data.materials.append(make_material("Typo_wood_mat", PAL["wood"]))
    # Tiny flag at top
    bpy.ops.mesh.primitive_cube_add(size=0.15, location=(0.15, 0, 2.5))
    flag = bpy.context.object
    flag.scale = (2, 0.05, 0.6)
    set_flat_shading(flag)
    flag.data.materials.append(make_material("Typo_flag_mat", PAL["lapacho_b"]))
    export_glb(f"{OUT_DIR}/lqv_lowpoly_typo_glamping.glb", objects=[tent, pole, flag])


# ============================================================
# 4. MAIN
# ============================================================
def main():
    print("=" * 60)
    print("LQV 3D World Builder — Blender pipeline")
    print("=" * 60)
    print(f"Output dir: {OUT_DIR}")
    print()

    # 1. Terrain
    print("\n=== 1. Building low-poly terrain ===")
    obj = build_terrain()
    if obj:
        export_glb(f"{OUT_DIR}/lqv_lowpoly_terrain.glb", objects=[obj])

    # 2. Archetypes
    print("\n=== 2. Building archetypes ===")
    build_archetypes()

    # 3. Typology set
    print("\n=== 3. Building typology set ===")
    build_typo_set()

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)
    # Final inventory
    for f in sorted(os.listdir(OUT_DIR)):
        if f.endswith(".glb"):
            sz = os.path.getsize(f"{OUT_DIR}/{f}")
            print(f"  {sz/1024:>8.1f} KB  {f}")


if __name__ == "__main__":
    main()
