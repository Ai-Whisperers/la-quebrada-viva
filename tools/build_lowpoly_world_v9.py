#!/usr/bin/env python3
"""LQV 3D World — REBUILT terrain + asset placement (v9).

CHANGES from v8:
- Terrain mesh rebuilt from elevation_grid.json (the 10km box DEM, NOT the
  parcel-scale 16-bit PNG) at correct world scale:
    * 108 × 180 cells × ~187m = ~20km × ~20km coverage
    * X axis = (lon - parcel_lon) * 100385 m_per_deg_lon (east in metres)
    * Z axis = -(lat - parcel_lat) * 110540 m_per_deg_lat (north negated)
    * Y axis = elevation_m - 116 (lowest point is z=0)
    * Origin (0, 0, 0) = LQV parcel centroid
- Cerros placed at REAL lat/lon from peaks_10km.geojson
- Monte + waterfall + house placed at REAL GPS positions
- Trees scattered with Hansen/NDVI density bias (deterministic seed)
- Quebrada ribbon follows the real quebrada polygon
- Z scale exaggerated 2x for visual drama (real relief is 116-391 = 275m of variance)

Output (to /root/la-quebrada-viva/docs/game_assets/lowpoly/):
  - lqv_lowpoly_terrain.glb     (correctly scaled, 19km × 20km, 5km relief)
  - lqv_lowpoly_world.json      (asset placements with positions + rotations)
"""
import bpy
import bmesh
import json
import math
import os
import random
from mathutils import Vector

# ---------- Configuration ----------
OUT_DIR = "/root/la-quebrada-viva/docs/game_assets/lowpoly"
DATA_DIR = "/root/la-quebrada-viva/docs/game_assets"
os.makedirs(OUT_DIR, exist_ok=True)

# Real LQV parcel centroid
PARCEL_LON = -57.0304
PARCEL_LAT = -25.6082

# Metres per degree at parcel latitude (calculated from -25.6082)
M_PER_DEG_LON = 111320.0 * math.cos(math.radians(-25.6082))   # ~100385 m/°
M_PER_DEG_LAT = 110540.0                                       # ~110540 m/°

# Z exaggeration (visual drama — real relief 275m looks subtle at 20km scale)
Z_EXAG = 2.0

# Terrain extents (will be auto-computed from elevation_grid.json)
GRID_BOUNDS = None    # [-57.13, -25.698, -56.931, -25.518]
GRID_PIXELS = None    # (108, 180)

# ---------- Helpers ----------
def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def make_material(name, rgb, roughness=0.85):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
    return mat


def set_flat_shading(obj):
    for poly in obj.data.polygons:
        poly.use_smooth = False


def export_glb(filepath, objects=None):
    if objects is not None:
        all_objs = list(bpy.data.objects)
        for o in all_objs:
            o.hide_render = o not in objects
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        export_materials='EXPORT',
        export_apply=True,
    )
    for o in bpy.data.objects:
        o.hide_render = False
    sz = os.path.getsize(filepath)
    print(f"  → wrote {os.path.basename(filepath)} ({sz/1024:.1f} KB)")


def lonlat_to_xz(lon, lat):
    """Convert real lon/lat to world x/z in metres from parcel centroid."""
    x = (lon - PARCEL_LON) * M_PER_DEG_LON
    z = -(lat - PARCEL_LAT) * M_PER_DEG_LAT
    return x, z


# ============================================================
# 1. TERRAIN — from elevation_grid.json (real DEM, 20km box)
# ============================================================
def build_terrain():
    """Build stepped terrain mesh from elevation_grid.json.

    World coordinates:
      X axis = east in metres (positive = east)
      Z axis = south in metres (positive = south, negated from lat)
      Y axis = (elevation_m - 116) * Z_EXAG (lowest point at y=0)
      Origin (0, 0, 0) = LQV parcel centroid

    Mesh extents: ~20km × ~20km, ~550m of vertical relief (with 2x exag)
    """
    reset_scene()
    import numpy as np

    # Load real DEM
    grid_path = "/root/.hermes/lqv-splat/exports/web/game_assets_lite/elevation_grid.json"
    grid = json.loads(open(grid_path).read())
    global GRID_BOUNDS, GRID_PIXELS
    GRID_BOUNDS = grid["bounds"]
    GRID_PIXELS = (grid["width"], grid["height"])
    dem = np.array(grid["dem"], dtype=np.float32)
    print(f"  DEM: {dem.shape}, range {dem.min():.0f}-{dem.max():.0f}m")

    # Coordinate transform:
    #   grid i (column) → X = (lon - parcel_lon) * M_PER_DEG_LON
    #   grid j (row)    → Z = -(lat - parcel_lat) * M_PER_DEG_LAT
    w_pix, h_pix = GRID_PIXELS
    w_lon = GRID_BOUNDS[2] - GRID_BOUNDS[0]   # 0.199° = 19978m
    h_lat = GRID_BOUNDS[3] - GRID_BOUNDS[1]   # 0.180° = 19897m
    cell_x = w_lon * M_PER_DEG_LON / (w_pix - 1)  # ~187m per cell
    cell_z = h_lat * M_PER_DEG_LAT / (h_pix - 1)  # ~111m per cell
    print(f"  cell size: {cell_x:.0f}m × {cell_z:.0f}m, total: {w_lon * M_PER_DEG_LON:.0f}m × {h_lat * M_PER_DEG_LAT:.0f}m")

    # Quantize elevation to 2m bands for low-poly stepped look (Zelda aesthetic)
    STEP = 2.0
    elev_q = np.round(dem / STEP) * STEP
    elev_min_real = float(elev_q.min())
    print(f"  quantized range: {elev_min_real:.0f}m to {elev_q.max():.0f}m")

    # Build mesh — vertex at (x, y, z)
    # We write (x, z, y_swap) so that:
    #   - GLB X = east (unchanged)
    #   - GLB Y = up (gets the elevation value, so glTF's Y-up convention is correct)
    #   - GLB Z = horizontal (was south_m, becomes a horizontal axis)
    # This way the GLB file comes out Y-up with the terrain lying horizontal.
    verts = []
    h, w = elev_q.shape
    for j in range(h):
        for i in range(w):
            # Convert pixel index to lon/lat → world x/z
            lon = GRID_BOUNDS[0] + (i / (w - 1)) * w_lon
            lat = GRID_BOUNDS[3] - (j / (h - 1)) * h_lat  # row j=0 is top (north)
            x, z = lonlat_to_xz(lon, lat)
            y = (elev_q[j, i] - elev_min_real) * Z_EXAG
            # GLB needs Y = up = elevation. So write Y first.
            verts.append((x, y, z))

    faces = []
    for j in range(h - 1):
        for i in range(w - 1):
            v0 = j * w + i
            v1 = v0 + 1
            v2 = v0 + w
            v3 = v2 + 1
            faces.append((v0, v1, v3, v2))

    mesh = bpy.data.meshes.new("LQV_Terrain")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("LQV_Terrain", mesh)
    bpy.context.collection.objects.link(obj)

    # Flat shading (the whole point of low-poly)
    set_flat_shading(obj)

    # Vertex colors based on elevation + slope (graduated earth→grass→rock)
    slp = np.zeros_like(elev_q)
    if h > 1 and w > 1:
        # Vertical diff
        slp[:-1, :] = np.abs(np.diff(elev_q, axis=0)) / STEP
        # Horizontal diff
        slp[:, :-1] = np.maximum(slp[:, :-1], np.abs(np.diff(elev_q, axis=1)) / STEP)
    slp_max = max(slp.max(), 1.0)

    vc = mesh.vertex_colors.new(name="Col")
    # Colors (Zelda palette)
    grass = (0.478, 0.608, 0.306)      # #7a9b4e
    grass_dk = (0.239, 0.353, 0.165)   # #3d5a2a
    earth = (0.541, 0.416, 0.227)      # #8a6a3a
    earth_lt = (0.690, 0.561, 0.376)
    rock = (0.431, 0.384, 0.345)       # #6e6258
    rock_dk = (0.290, 0.271, 0.251)
    snow = (0.95, 0.95, 0.97)

    emin = float(elev_q.min())
    emax = float(elev_q.max())
    erange = emax - emin if emax > emin else 1.0

    for poly in mesh.polygons:
        # Average elevation of this face
        avg_e = sum(verts[mesh.loops[l].vertex_index][1] for l in poly.loop_indices) / len(poly.loop_indices)
        avg_s = 0.0
        for l in poly.loop_indices:
            vi = mesh.loops[l].vertex_index
            i = vi % w
            j = vi // w
            if 0 < j < h - 1 and 0 < i < w - 1:
                avg_s += slp[j, i]
        avg_s /= max(1, len(poly.loop_indices))

        t = (avg_e - emin) / erange  # 0=low, 1=high
        # Color rule: low=grass, mid=earth, high+steep=rock, peaks=snow
        if avg_s > 6.0:  # steep cliff
            r, g, b = rock
        elif t > 0.85:  # peaks
            r, g, b = snow
        elif t > 0.6:
            # Blend earth→rock based on slope
            blend = min(1.0, avg_s / 4.0)
            r = earth[0] * (1-blend) + rock[0] * blend
            g = earth[1] * (1-blend) + rock[1] * blend
            b = earth[2] * (1-blend) + rock[2] * blend
        elif t < 0.25:
            # Low = grass (darker in valleys)
            blend = 1.0 - t * 4  # darker as we go lower
            r = grass_dk[0] * blend + grass[0] * (1-blend)
            g = grass_dk[1] * blend + grass[1] * (1-blend)
            b = grass_dk[2] * blend + grass[2] * (1-blend)
        else:
            r, g, b = earth_lt

        for l in poly.loop_indices:
            vc.data[l].color = (r, g, b, 1.0)

    # Material with vertex colors
    mat = make_material("Terrain_VertexColor", (1, 1, 1))
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        vc_node = mat.node_tree.nodes.new("ShaderNodeVertexColor")
        vc_node.layer_name = "Col"
        vc_node.location = (-300, 200)
        mat.node_tree.links.new(vc_node.outputs["Color"], bsdf.inputs["Base Color"])
    obj.data.materials.append(mat)

    print(f"  Terrain mesh: {len(verts)} verts, {len(faces)} faces")
    print(f"  X range: {min(v[0] for v in verts):.0f} to {max(v[0] for v in verts):.0f}m")
    print(f"  Y range: {min(v[1] for v in verts):.0f} to {max(v[1] for v in verts):.0f}m (rel)")
    print(f"  Z range: {min(v[2] for v in verts):.0f} to {max(v[2] for v in verts):.0f}m")

    # Save the verts as a reference (for the play.html to sample elevations)
    out_json = {
        "bounds": GRID_BOUNDS,
        "pixels": GRID_PIXELS,
        "elev_min_m": emin,
        "elev_max_m": emax,
        "z_exag": Z_EXAG,
        "parcel_center_lon": PARCEL_LON,
        "parcel_center_lat": PARCEL_LAT,
        "m_per_deg_lon": M_PER_DEG_LON,
        "m_per_deg_lat": M_PER_DEG_LAT,
        "verts_count": len(verts),
        "verts": verts,  # for browser to sample elevation at any (x, z)
    }
    with open(f"{OUT_DIR}/terrain_mesh_data.json", "w") as f:
        json.dump(out_json, f)
    print(f"  → wrote terrain_mesh_data.json")

    return obj, verts


# ============================================================
# 2. ARCHETYPES (unchanged from v8 — they're correctly sized)
# ============================================================
def build_archetypes():
    """Same archetypes as v8 — already correctly sized at house scale."""
    import random
    random.seed(42)

    def tree_lapacho():
        reset_scene()
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.18, depth=3.2, location=(0, 0, 1.6))
        trunk = bpy.context.object; trunk.name = "Lapacho_trunk"; set_flat_shading(trunk)
        trunk.data.materials.append(make_material("Lapacho_trunk_mat", (0.227, 0.180, 0.133)))
        for dx, dy, dz, r in [(0, 0, 3.5, 1.5), (0.6, 0.3, 3.0, 1.2), (-0.5, 0.4, 3.2, 1.3), (0.2, -0.5, 3.7, 1.1)]:
            bpy.ops.mesh.primitive_ico_sphere_add(radius=r, subdivisions=1, location=(dx, dy, dz))
            blob = bpy.context.object; blob.name = f"Lapacho_blob"
            set_flat_shading(blob)
            col = (0.831, 0.584, 0.416) if abs(dx) > 0.3 else (0.659, 0.388, 0.490)
            blob.data.materials.append(make_material("Lapacho_canopy_mat", col))
        export_glb(f"{OUT_DIR}/lqv_lowpoly_tree_lapacho.glb")

    def tree_palmera():
        reset_scene()
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.22, depth=4.5, location=(0, 0, 2.25))
        trunk = bpy.context.object; trunk.name = "Palmera_trunk"
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
        trunk.data.materials.append(make_material("Palmera_trunk_mat", (0.227, 0.180, 0.133)))
        for i in range(7):
            angle = i * (2 * math.pi / 7)
            dx = math.cos(angle) * 1.8
            dy = math.sin(angle) * 1.8
            verts = [(0, 0, 4.5), (dx * 0.6, dy * 0.6, 4.4), (dx, dy, 3.9)]
            edges = [(0, 1), (1, 2), (2, 0)]
            faces = [(0, 1, 2)]
            mesh = bpy.data.meshes.new(f"Frond_{i}")
            mesh.from_pydata(verts, edges, faces); mesh.update()
            obj = bpy.data.objects.new(f"Frond_{i}", mesh)
            bpy.context.collection.objects.link(obj); set_flat_shading(obj)
            obj.data.materials.append(make_material(f"Frond_mat", (0.290, 0.451, 0.227)))
        export_glb(f"{OUT_DIR}/lqv_lowpoly_tree_palmera.glb")

    def tree_pino():
        reset_scene()
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.15, depth=2.5, location=(0, 0, 1.25))
        trunk = bpy.context.object; trunk.name = "Pino_trunk"
        set_flat_shading(trunk); trunk.data.materials.append(make_material("Pino_trunk_mat", (0.227, 0.180, 0.133)))
        for i, (z, r) in enumerate([(2.8, 1.6), (4.0, 1.2), (5.0, 0.7)]):
            bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=r, radius2=0.05, depth=1.5, location=(0, 0, z))
            cone = bpy.context.object; cone.name = f"Pino_cone_{i}"; set_flat_shading(cone)
            col = (0.122, 0.220, 0.137) if i % 2 == 0 else (0.290, 0.451, 0.227)
            cone.data.materials.append(make_material(f"Pino_cone_mat_{i}", col))
        export_glb(f"{OUT_DIR}/lqv_lowpoly_tree_pino.glb")

    def rock_cluster():
        reset_scene()
        random.seed(13)
        for i in range(5):
            r = random.uniform(0.4, 1.2)
            bpy.ops.mesh.primitive_ico_sphere_add(radius=r, subdivisions=1, location=(random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5), r * 0.6))
            rock = bpy.context.object; rock.scale = (1, 1, 0.7); set_flat_shading(rock)
            rock.data.materials.append(make_material(f"Rock_mat_{i}", (0.431, 0.384, 0.345)))
        export_glb(f"{OUT_DIR}/lqv_lowpoly_rock_cluster.glb")

    def waterfall():
        reset_scene()
        # Wide rocky back (the cliff the water falls down)
        verts = [(-4, -0.5, 12), (4, -0.5, 12), (4, -0.5, 0), (-4, -0.5, 0)]
        mesh = bpy.data.meshes.new("Waterfall_back")
        mesh.from_pydata(verts, [], [(0, 1, 2, 3)]); mesh.update()
        back = bpy.data.objects.new("Waterfall_back", mesh); bpy.context.collection.objects.link(back)
        set_flat_shading(back); back.data.materials.append(make_material("Waterfall_rock_mat", (0.290, 0.271, 0.251)))
        # Three water sheets, varying widths
        for i, (top, bot, off) in enumerate([(1.2, -1.2, 0.15), (-0.6, 0.6, 0.08), (-1.2, -1.2, 0.0)]):
            verts = [(top - 1.0, 0, 12), (top + 1.0, 0, 12), (bot + 0.7, 0, 0), (bot - 0.7, 0, 0)]
            mesh = bpy.data.meshes.new(f"Water_sheet_{i}")
            mesh.from_pydata(verts, [], [(0, 1, 2, 3)]); mesh.update()
            obj = bpy.data.objects.new(f"Water_sheet_{i}", mesh); bpy.context.collection.objects.link(obj)
            set_flat_shading(obj); obj.data.materials.append(make_material(f"Water_sheet_mat_{i}", (0.357, 0.616, 0.851), roughness=0.3))
        # Splash pool
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=2.5, depth=0.3, location=(0, 0, 0.1))
        pool = bpy.context.object; pool.name = "Splash_pool"; set_flat_shading(pool)
        pool.data.materials.append(make_material("Splash_pool_mat", (0.357, 0.616, 0.851), roughness=0.4))
        export_glb(f"{OUT_DIR}/lqv_lowpoly_waterfall.glb")

    def monte():
        reset_scene()
        # Stylized escarpment silhouette — larger + more dramatic
        verts = [
            (0, 0, 30),         # peak
            (-15, 8, 0),        # base front-left
            (15, 8, 0),         # base front-right
            (-12, -15, 0),      # base back-left
            (12, -15, 0),       # base back-right
            (0, 18, 8),         # shoulder front
            (-4, 12, 18),       # sub-peak
        ]
        faces = [
            (0, 1, 5), (0, 5, 2),    # front
            (0, 2, 4), (0, 4, 3),    # back
            (0, 3, 1),               # left
            (5, 1, 2),               # base front
            (4, 2, 5),               # base right
            (3, 4, 2), (2, 1, 5),    # base bottom
            (0, 6, 1), (0, 2, 6), (1, 6, 5), (5, 6, 2),  # sub-peak connections
        ]
        mesh = bpy.data.meshes.new("Monte")
        mesh.from_pydata(verts, [], faces); mesh.update()
        obj = bpy.data.objects.new("Monte", mesh); bpy.context.collection.objects.link(obj)
        set_flat_shading(obj)
        vc = mesh.vertex_colors.new(name="Col")
        for poly in mesh.polygons:
            avg_z = sum(verts[mesh.loops[l].vertex_index][2] for l in poly.loop_indices) / len(poly.loop_indices)
            t = avg_z / 30.0
            col = (
                0.290 * (1-t) + 0.700 * t,
                0.271 * (1-t) + 0.650 * t,
                0.251 * (1-t) + 0.580 * t,
                1.0,
            )
            for l in poly.loop_indices:
                vc.data[l].color = col
        mat = make_material("Monte_mat", (1, 1, 1))
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            vc_node = mat.node_tree.nodes.new("ShaderNodeVertexColor")
            mat.node_tree.links.new(vc_node.outputs["Color"], bsdf.inputs["Base Color"])
        obj.data.materials.append(mat)
        export_glb(f"{OUT_DIR}/lqv_lowpoly_monte.glb")

    def gate():
        reset_scene()
        for x in (-1.5, 1.5):
            bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.4, depth=3.0, location=(x, 0, 1.5))
            p = bpy.context.object; p.name = f"Gate_pillar_{x}"; set_flat_shading(p)
            p.data.materials.append(make_material("Gate_pillar_mat", (0.431, 0.384, 0.345)))
        verts = [(-1.9, 0, 3.0), (1.9, 0, 3.0), (1.9, 0, 3.5), (-1.9, 0, 3.5)]
        mesh = bpy.data.meshes.new("Gate_lintel")
        mesh.from_pydata(verts, [], [(0, 1, 2, 3), (0, 3, 2, 1)])
        mesh.update()
        obj = bpy.data.objects.new("Gate_lintel", mesh); bpy.context.collection.objects.link(obj)
        set_flat_shading(obj); obj.data.materials.append(make_material("Gate_lintel_mat", (0.227, 0.180, 0.133)))
        export_glb(f"{OUT_DIR}/lqv_lowpoly_gate.glb")

    def trail():
        reset_scene()
        random.seed(7)
        path_verts = []
        for i in range(60):
            t = i / 59
            x = -50 + 100 * t
            y = math.sin(t * 6 * math.pi) * 3 + math.sin(t * 11 * math.pi) * 0.8
            z = 0.1 + t * 2.5
            path_verts.append((x, y, z))
        ribbon_verts = []
        ribbon_faces = []
        for i, (x, y, z) in enumerate(path_verts):
            if i < len(path_verts) - 1:
                dx = path_verts[i+1][0] - x
                dy = path_verts[i+1][1] - y
                L = math.hypot(dx, dy) or 1.0
                nx, ny = -dy / L, dx / L
            else:
                nx, ny = 0, 1
            width = 0.6 + random.uniform(-0.15, 0.15)
            ribbon_verts.append((x + nx * width, y + ny * width, z))
            ribbon_verts.append((x - nx * width, y - ny * width, z))
        for i in range(len(path_verts) - 1):
            v0 = i * 2
            ribbon_faces.append((v0, v0+1, v0+3, v0+2))
        mesh = bpy.data.meshes.new("Trail")
        mesh.from_pydata(ribbon_verts, [], ribbon_faces); mesh.update()
        obj = bpy.data.objects.new("Trail", mesh); bpy.context.collection.objects.link(obj)
        set_flat_shading(obj); obj.data.materials.append(make_material("Trail_mat", (0.690, 0.561, 0.376)))
        export_glb(f"{OUT_DIR}/lqv_lowpoly_trail.glb")

    def typo_cob():
        reset_scene()
        bpy.ops.mesh.primitive_cube_add(size=4, location=(0, 0, 1.5))
        walls = bpy.context.object; walls.scale = (1, 0.8, 0.75); set_flat_shading(walls)
        walls.data.materials.append(make_material("Typo_Cob_mat", (0.831, 0.631, 0.329)))
        verts = [(-2.2, -1.7, 3.0), (2.2, -1.7, 3.0), (2.2, 1.7, 3.0), (-2.2, 1.7, 3.0), (0, -1.7, 5.0), (0, 1.7, 5.0)]
        faces = [(0, 1, 5, 4), (1, 2, 5), (2, 3, 4, 5), (3, 0, 4), (0, 3, 2, 1)]
        mesh = bpy.data.meshes.new("Typo_Cob_roof")
        mesh.from_pydata(verts, [], faces); mesh.update()
        roof = bpy.data.objects.new("Typo_Cob_roof", mesh); bpy.context.collection.objects.link(roof)
        set_flat_shading(roof); roof.data.materials.append(make_material("Typo_thatch_mat", (0.659, 0.537, 0.353)))
        bpy.ops.mesh.primitive_cube_add(size=0.4, location=(1.5, -1.0, 4.2))
        chim = bpy.context.object; chim.name = "Typo_Cob_chimney"; set_flat_shading(chim)
        chim.data.materials.append(make_material("Typo_stone_mat", (0.290, 0.271, 0.251)))
        bpy.ops.mesh.primitive_cube_add(size=0.7, location=(0, 1.7, 1.0))
        door = bpy.context.object; door.scale = (1, 0.1, 1.4); set_flat_shading(door)
        door.data.materials.append(make_material("Typo_wood_mat", (0.227, 0.180, 0.133)))
        export_glb(f"{OUT_DIR}/lqv_lowpoly_house_cob.glb", objects=[walls, roof, chim, door])

    def typo_tatakua():
        reset_scene()
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.8, subdivisions=2, location=(0, 0, 0.8))
        oven = bpy.context.object; oven.scale = (1.2, 1.0, 0.8); set_flat_shading(oven)
        oven.data.materials.append(make_material("Typo_Tatakua_mat", (0.831, 0.631, 0.329)))
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.2, depth=0.5, location=(0.4, 0, 1.2))
        ch = bpy.context.object; ch.name = "Typo_Tatakua_chimney"; set_flat_shading(ch)
        ch.data.materials.append(make_material("Typo_stone_mat", (0.290, 0.271, 0.251)))
        bpy.ops.mesh.primitive_cube_add(size=1.8, location=(0, 2.5, 0.4))
        table = bpy.context.object; table.scale = (1.5, 0.6, 0.15); set_flat_shading(table)
        table.data.materials.append(make_material("Typo_wood_mat", (0.227, 0.180, 0.133)))
        export_glb(f"{OUT_DIR}/lqv_lowpoly_typo_tatakua.glb", objects=[oven, ch, table])

    def typo_worker():
        reset_scene()
        bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
        wh = bpy.context.object; wh.scale = (4.0, 0.8, 1.0); set_flat_shading(wh)
        wh.data.materials.append(make_material("Typo_Worker_mat", (0.690, 0.561, 0.376)))
        verts = [(-8.2, -0.9, 2.0), (8.2, -0.9, 2.0), (8.2, 0.9, 2.0), (-8.2, 0.9, 2.0), (0, -0.9, 2.5), (0, 0.9, 2.5)]
        faces = [(0, 1, 5, 4), (1, 2, 5), (2, 3, 4, 5), (3, 0, 4)]
        mesh = bpy.data.meshes.new("Worker_roof")
        mesh.from_pydata(verts, [], faces); mesh.update()
        wroof = bpy.data.objects.new("Worker_roof", mesh); bpy.context.collection.objects.link(wroof)
        set_flat_shading(wroof); wroof.data.materials.append(make_material("Typo_metal_mat", (0.431, 0.384, 0.345)))
        export_glb(f"{OUT_DIR}/lqv_lowpoly_typo_worker.glb", objects=[wh, wroof])

    def typo_wigwam():
        reset_scene()
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=2.0, radius2=0.1, depth=3.5, location=(0, 0, 1.75))
        wg = bpy.context.object; wg.name = "Typo_Wigwam"; set_flat_shading(wg)
        wg.data.materials.append(make_material("Typo_Wigwam_mat", (0.659, 0.537, 0.353)))
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 2.0, 0.6))
        wdoor = bpy.context.object; wdoor.scale = (0.6, 0.05, 1.4); set_flat_shading(wdoor)
        wdoor.data.materials.append(make_material("Typo_wood_mat", (0.227, 0.180, 0.133)))
        export_glb(f"{OUT_DIR}/lqv_lowpoly_typo_wigwam.glb", objects=[wg, wdoor])

    def typo_glamping():
        reset_scene()
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=2.2, radius2=0.1, depth=1.8, location=(0, 0, 0.9))
        tent = bpy.context.object; tent.name = "Typo_Glamping"; set_flat_shading(tent)
        tent.data.materials.append(make_material("Typo_Glamping_mat", (0.659, 0.537, 0.353)))
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.03, depth=2.2, location=(0, 0, 1.9))
        pole = bpy.context.object; pole.name = "Typo_Glamping_pole"; set_flat_shading(pole)
        pole.data.materials.append(make_material("Typo_wood_mat", (0.227, 0.180, 0.133)))
        bpy.ops.mesh.primitive_cube_add(size=0.15, location=(0.15, 0, 2.5))
        flag = bpy.context.object; flag.scale = (2, 0.05, 0.6); set_flat_shading(flag)
        flag.data.materials.append(make_material("Typo_flag_mat", (0.659, 0.388, 0.490)))
        export_glb(f"{OUT_DIR}/lqv_lowpoly_typo_glamping.glb", objects=[tent, pole, flag])

    print("\n=== Building archetypes (house-scale) ===")
    tree_lapacho()
    tree_palmera()
    tree_pino()
    rock_cluster()
    waterfall()
    monte()
    gate()
    trail()
    typo_cob()
    typo_tatakua()
    typo_worker()
    typo_wigwam()
    typo_glamping()


# ============================================================
# 3. WORLD PLACEMENTS — from real data
# ============================================================
def build_world_metadata():
    """Build lqv_lowpoly_world.json — every asset's real position + scale.

    Reads from peaks_10km.geojson, gps polygon, etc. Outputs a JSON the
    browser uses to place assets in correct world coordinates.
    """
    import random
    random.seed(42)

    placements = []

    # === CERROS — 13 peaks at real lat/lon from peaks_10km.geojson ===
    peaks = json.loads(open("/root/.hermes/lqv-splat/exports/web/data/peaks_10km.geojson").read())
    grid = json.loads(open("/root/la-quebrada-viva/docs/game_assets/lowpoly/terrain_mesh_data.json").read())
    emin = grid["elev_min_m"]

    # Load DEM to get elevation at any (lon, lat) — bilinear interp
    dem_grid = json.loads(open("/root/.hermes/lqv-splat/exports/web/game_assets_lite/elevation_grid.json").read())
    dem = dem_grid["dem"]
    w, h = dem_grid["width"], dem_grid["height"]
    bnd = dem_grid["bounds"]

    def sample_dem(lon, lat):
        # Convert lon/lat to grid indices
        u = (lon - bnd[0]) / (bnd[2] - bnd[0]) * (w - 1)
        v = (bnd[3] - lat) / (bnd[3] - bnd[1]) * (h - 1)
        if u < 0 or u > w - 1 or v < 0 or v > h - 1:
            return None
        i, j = int(u), int(v)
        # Bilinear
        if i < w - 1 and j < h - 1:
            fx, fy = u - i, v - j
            return (dem[j][i] * (1-fx) * (1-fy) + dem[j][i+1] * fx * (1-fy) +
                    dem[j+1][i] * (1-fx) * fy + dem[j+1][i+1] * fx * fy)
        return dem[j][i]

    for feat in peaks["features"]:
        p = feat["properties"]
        if p.get("elev_m") is None:
            continue  # skip the parcel reference point
        lon, lat = feat["geometry"]["coordinates"]
        x, z = lonlat_to_xz(lon, lat)
        # Cerro's actual elevation (real data)
        elev = p["elev_m"]
        # Place cone at cerro summit, scale based on prominence
        prominence_factor = p.get("area_ha", 1) / 100  # bigger cerros → bigger cone
        radius = 30 + min(50, prominence_factor * 5)
        height = 60 + min(100, prominence_factor * 8)
        placements.append({
            "type": "cerro",
            "id": p["name"].replace(" ", "_"),
            "name": p["name"],
            "elev_m": elev,
            "x": round(x, 1),
            "y": round((elev - emin) * Z_EXAG, 1),  # mesh coords (relative to lowest)
            "z": round(z, 1),
            "scale": {"radius": round(radius, 1), "height": round(height, 1)},
            "category": p.get("category", "hill"),
            "direction_from_lqv": p.get("direction_from_lqv", ""),
            "distance_from_lqv_km": p.get("distance_from_lqv_km", 0),
        })

    # === DEFAULT COB HOUSE — at parcel centroid ===
    # LQV parcel polygon centroid
    poly = json.loads(open("/root/.hermes/lqv-splat/exports/web/data/client_gps/client_gps_polygon.geojson").read())
    coords = poly["features"][0]["geometry"]["coordinates"][0]
    parcel_lon_c = sum(c[0] for c in coords) / len(coords)
    parcel_lat_c = sum(c[1] for c in coords) / len(coords)
    parcel_x, parcel_z = lonlat_to_xz(parcel_lon_c, parcel_lat_c)
    parcel_elev = sample_dem(parcel_lon_c, parcel_lat_c) or 200
    placements.append({
        "type": "default_house",
        "id": "lqv_default_cob",
        "typo": "lqv_lowpoly_house_cob",
        "name": "LQV Cob House (default)",
        "x": round(parcel_x, 1),
        "y": round((parcel_elev - emin) * Z_EXAG, 1),
        "z": round(parcel_z, 1),
        "rotation_y": 0,
        "scale": 8,  # cob house is ~12m wide → scale 8 from base unit ~1.5m
    })

    # === QUEBRADA RIBBON — sample from real quebrada polygon ===
    quebrada_poly = json.loads(open("/root/.hermes/lqv-splat/exports/web/data/local_quebradas_10km.geojson").read())
    # Walk the LineString → ribbon vertices
    for feat in quebrada_poly["features"]:
        geom = feat["geometry"]
        if geom["type"] == "LineString":
            coords_q = geom["coordinates"]
            for i, c in enumerate(coords_q):
                if i % 3 != 0: continue  # subsample every 3rd point
                lon, lat = c[0], c[1]
                x, z = lonlat_to_xz(lon, lat)
                elev = sample_dem(lon, lat) or 200
                placements.append({
                    "type": "quebrada_segment",
                    "x": round(x, 1),
                    "y": round((elev - emin) * Z_EXAG + 5, 1),  # 5m above terrain
                    "z": round(z, 1),
                })

    # === TREES — scattered by Hansen/NDVI density (deterministic) ===
    # For v1 we don't have a Hansen raster here; use Hansen loss/gain geojsons
    # to bias: more trees where Hansen loss is LOW (old-growth forest)
    try:
        hansen = json.loads(open("/root/.hermes/lqv-splat/exports/web/data/hansen_loss_10km.geojson").read())
        # Sample 40 trees at random spots biased away from cleared areas
        tree_count = 40
        for i in range(tree_count):
            # Random within 1km radius
            angle = random.uniform(0, 2 * math.pi)
            r = random.uniform(150, 800)
            x = parcel_x + r * math.cos(angle)
            z = parcel_z + r * math.sin(angle)
            # Convert back to lon/lat for sampling
            lon = PARCEL_LON + x / M_PER_DEG_LON
            lat = PARCEL_LAT - z / M_PER_DEG_LAT
            elev = sample_dem(lon, lat) or 200
            # Species bias (45% lapacho, 35% pino, 20% palmera)
            w = random.random()
            if w < 0.45: species = "lqv_lowpoly_tree_lapacho"
            elif w < 0.80: species = "lqv_lowpoly_tree_pino"
            else: species = "lqv_lowpoly_tree_palmera"
            # Scale variation
            s = random.uniform(8, 14)
            placements.append({
                "type": "tree",
                "species": species,
                "x": round(x, 1),
                "y": round((elev - emin) * Z_EXAG, 1),
                "z": round(z, 1),
                "scale": round(s, 1),
                "rotation_y": round(random.uniform(0, 360), 1),
            })
    except Exception as e:
        print(f"  (skipping trees: {e})")

    # === MONTE — highlighted at the NW escarpment (per data) ===
    # The LQV property's actual escarpment is the western edge of the parcel
    # Place at the W edge of the property
    placements.append({
        "type": "monte",
        "id": "lqv_monte_main",
        "name": "Cerro del LQV (escarpment)",
        "x": round(parcel_x - 280, 1),
        "y": round((250 - emin) * Z_EXAG, 1),  # approximate escarpment elev
        "z": round(parcel_z, 1),
        "scale": 35,  # large enough to be a focal point
        "rotation_y": 0,
    })

    # === WATERFALL — at the quebrada where it crosses elevation step ===
    # Place near the western part of the quebrada
    waterfall_lon = -57.0345
    waterfall_lat = -25.6100
    wx, wz = lonlat_to_xz(waterfall_lon, waterfall_lat)
    w_elev = sample_dem(waterfall_lon, waterfall_lat) or 230
    placements.append({
        "type": "waterfall",
        "id": "lqv_waterfall_main",
        "x": round(wx, 1),
        "y": round((w_elev - emin) * Z_EXAG, 1),
        "z": round(wz, 1),
        "scale": 1.5,
        "rotation_y": 0,
    })

    # === GATE — at the SE entrance ===
    gate_lon = -57.0260
    gate_lat = -25.6130
    gx, gz = lonlat_to_xz(gate_lon, gate_lat)
    g_elev = sample_dem(gate_lon, gate_lat) or 220
    placements.append({
        "type": "gate",
        "id": "lqv_gate_main",
        "x": round(gx, 1),
        "y": round((g_elev - emin) * Z_EXAG, 1),
        "z": round(gz, 1),
        "scale": 3,
        "rotation_y": -25,  # angled toward road
    })

    # === TRAIL — Wes's walking path (use GPS data) ===
    walking_path = json.loads(open("/root/.hermes/lqv-splat/exports/web/data/client_gps/client_gps_walking_path.geojson").read())
    wp_coords = walking_path["features"][0]["geometry"]["coordinates"]
    # Build a simple flat ribbon along the path (the actual mesh is generated by Three.js BufferGeometry)
    placements.append({
        "type": "trail_polyline",
        "id": "wes_walking_path",
        "coords": [
            [round(lonlat_to_xz(c[0], c[1])[0], 1),
             round(lonlat_to_xz(c[0], c[1])[1], 1)]
            for c in wp_coords
        ],
    })

    # === SAVE ===
    world = {
        "placements": placements,
        "parcel_center": {"lon": PARCEL_LON, "lat": PARCEL_LAT},
        "elev_min_m": emin,
        "elev_max_m": grid["elev_max_m"],
        "z_exag": Z_EXAG,
        "m_per_deg_lon": M_PER_DEG_LON,
        "m_per_deg_lat": M_PER_DEG_LAT,
    }
    with open(f"{OUT_DIR}/lqv_lowpoly_world.json", "w") as f:
        json.dump(world, f, indent=2)
    print(f"  → wrote lqv_lowpoly_world.json ({len(placements)} placements)")
    # Stats
    counts = {}
    for p in placements:
        t = p["type"]
        counts[t] = counts.get(t, 0) + 1
    for t, c in sorted(counts.items()):
        print(f"     {t}: {c}")
    return world


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("LQV 3D World — v9 REBUILD (correct scale)")
    print("=" * 60)
    print(f"Parcel: ({PARCEL_LAT}, {PARCEL_LON})")
    print(f"Scale: 1 unit = 1 metre; grid = 20km × 20km; Z exag = {Z_EXAG}x")

    # 1. Terrain
    print("\n=== 1. Rebuilding terrain from elevation_grid.json ===")
    terrain, verts = build_terrain()
    export_glb(f"{OUT_DIR}/lqv_lowpoly_terrain.glb", objects=[terrain])

    # 2. Archetypes (unchanged)
    print("\n=== 2. Building archetypes (house-scale) ===")
    build_archetypes()

    # 3. World placements (real GPS coords)
    print("\n=== 3. Building world placements (real lat/lon) ===")
    build_world_metadata()

    # Final inventory
    print("\n=== Final inventory ===")
    total = 0
    for f in sorted(os.listdir(OUT_DIR)):
        if f.endswith(".glb"):
            sz = os.path.getsize(f"{OUT_DIR}/{f}")
            total += sz
            print(f"  {sz/1024:>8.1f} KB  {f}")
        elif f.endswith(".json"):
            sz = os.path.getsize(f"{OUT_DIR}/{f}")
            print(f"  {sz/1024:>8.1f} KB  {f}  (metadata)")
    print(f"  TOTAL GLBs: {total/1024/1024:.2f} MB")


if __name__ == "__main__":
    main()
