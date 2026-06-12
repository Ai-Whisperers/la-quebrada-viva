"""
blender_render_monday.py — Render the Cataratas del Monday test scene (12 houses around a creek).

Self-contained Blender 4.2.x script. Run headless:
  blender --background --python blender_render_monday.py

What it does:
  1. Loads the 2.5m terrarium DEM as a real-world terrain mesh
  2. Applies procedural green/brown albedo based on elevation
  3. Places 12 house markers + 1 community marker at topology-driven positions
  4. Adds creek water plane along the Rio Monday
  5. Renders the overview shot
  6. Saves the .blend for the user

Houses are simple geometry placeholders (boxes for typology footprints) with
material proxies. The point is to test the topology pipeline, not ship a final
arch-viz render. When we have the real client parcel + Anexo I, we swap the
AOI + add full house models.
"""
import bpy
import bmesh
import sys, os, json
from mathutils import Vector
import numpy as np
import rasterio
from pyproj import Transformer

HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
DEM_PATH    = os.path.join(HERE, "dem/terrarium_monday_2_5m_utm21j.tif")
OUT_BLEND   = os.path.join(HERE, "blender/monday_test_scene.blend")
OUT_DIR     = os.path.join(HERE, "renders_monday")
os.makedirs(os.path.dirname(OUT_BLEND), exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# Cascade center in UTM 21J
CENTER_E, CENTER_N = 737860.0, 7170615.0
AOI_RADIUS = 500  # 1km diameter scene, not the full 2km data box

# --- House typology spec (footprint, height, material, label) ---
HOUSES = [
    # Cluster A — Italian (upper terrace, cobble)
    {"name": "A1_italian_small",  "cx":-220, "cy": 60, "w":5.5, "d":4.0, "h":3.8, "style":"italian_small",  "rotation": 15,  "cluster":"A"},
    {"name": "A2_italian_mid",    "cx":-180, "cy": 30, "w":6.2, "d":4.2, "h":3.8, "style":"italian_mid",    "rotation": 25,  "cluster":"A"},
    {"name": "A3_italian_river",  "cx":-140, "cy":  0, "w":8.5, "d":4.0, "h":3.8, "style":"italian_river",  "rotation": 0,   "cluster":"A"},
    # Cluster B — Bamboo (mid-slope, palms)
    {"name": "B1_bamboo_30",      "cx": -60, "cy":-50, "w":6.0, "d":6.0, "h":4.2, "style":"bamboo_30",      "rotation": 0,   "cluster":"B"},
    {"name": "B2_bamboo_75",      "cx": -10, "cy":-90, "w":9.8, "d":9.8, "h":4.8, "style":"bamboo_75",      "rotation": 0,   "cluster":"B"},
    {"name": "B3_wigwam",         "cx":  50, "cy":-80, "w":7.5, "d":7.5, "h":6.6, "style":"wigwam",         "rotation": 0,   "cluster":"B"},
    # Cluster C — Over the Creek (on stilts at the water)
    {"name": "C1_bamboo_river",   "cx": 120, "cy":-30, "w":7.2, "d":5.9, "h":4.7, "style":"bamboo_river",   "rotation": 90,  "cluster":"C"},
    {"name": "C2_bamboo_river_2", "cx": 180, "cy": 20, "w":7.2, "d":5.9, "h":4.7, "style":"bamboo_river",   "rotation": 90,  "cluster":"C"},
    {"name": "C3_container",      "cx": 230, "cy": 70, "w":12.2,"d":2.6, "h":3.0, "style":"container",      "rotation": 0,   "cluster":"C"},
    # Cluster D — Earth and Tree (hidden, premium)
    {"name": "D1_hobbit",         "cx": 250, "cy": 200,"w":7.6, "d":5.2, "h":4.0, "style":"hobbit",         "rotation": 0,   "cluster":"D"},
    {"name": "D2_treehouse",      "cx": 180, "cy": 240,"w":5.5, "d":5.0, "h":4.4, "style":"treehouse",      "rotation": 0,   "cluster":"D"},
    # Communal — Labrisa lounge (between A and C, central)
    {"name": "COMM_labrisa",      "cx": -20, "cy":-20, "w":15.0,"d":10.0,"h":3.0, "style":"labrisa",        "rotation": 0,   "cluster":"COMM"},
]

STYLE_COLORS = {
    "italian_small": ("Tropical Wood", 0.55, 0.35, 0.20, 0.4),
    "italian_mid":   ("Warm Stone",     0.78, 0.65, 0.45, 0.4),
    "italian_river": ("Lime Stucco",    0.92, 0.86, 0.74, 0.4),
    "bamboo_30":     ("Bamboo Golden",  0.78, 0.60, 0.30, 0.5),
    "bamboo_75":     ("Bamboo Dark",    0.55, 0.40, 0.20, 0.5),
    "wigwam":        ("Woven Wicker",   0.65, 0.50, 0.30, 0.5),
    "bamboo_river":  ("River Bamboo",   0.60, 0.50, 0.30, 0.5),
    "container":     ("Container Steel",0.20, 0.20, 0.22, 0.6),
    "hobbit":        ("Earth Berm",     0.45, 0.40, 0.25, 0.5),
    "treehouse":     ("Treehouse Wood", 0.55, 0.40, 0.20, 0.5),
    "labrisa":       ("Labrisa Wood",   0.50, 0.38, 0.22, 0.5),
}

# === 1. Load DEM ===
print(f"[monday] loading DEM from {DEM_PATH}")
with rasterio.open(DEM_PATH) as ds:
    dem = ds.read(1).astype(np.float32)
    dem_transform = ds.transform
print(f"  DEM: {dem.shape}  res {ds.res[0]:.2f}m  range {dem.min():.1f}..{dem.max():.1f}m")
dem[dem == 0] = dem[dem > 0].min() if (dem > 0).any() else 0
DEM_BASE = float(dem.min())
e0, n0 = dem_transform.c, dem_transform.f
W_m = abs(dem_transform.a) * dem.shape[1]
H_m = abs(dem_transform.e) * dem.shape[0]
print(f"  ground area: {W_m:.0f}m x {H_m:.0f}m ({W_m*H_m/1e6:.2f} km^2)")

# === 2. Build terrain mesh ===
print(f"[monday] building terrain mesh from {dem.shape} DEM")
verts = []
for row in range(dem.shape[0]):
    for col in range(dem.shape[1]):
        x = e0 + col * dem_transform.a - CENTER_E
        y = n0 + row * dem_transform.e - CENTER_N
        z = float(dem[row, col]) - DEM_BASE
        verts.append((x, y, z))
print(f"  {len(verts)} verts")
faces = []
for row in range(dem.shape[0] - 1):
    for col in range(dem.shape[1] - 1):
        i0 = row * dem.shape[1] + col
        i1 = i0 + 1
        i2 = i0 + dem.shape[1] + 1
        i3 = i0 + dem.shape[1]
        faces.append((i0, i1, i2, i3))
mesh = bpy.data.meshes.new("MondayTerrainMesh")
mesh.from_pydata(verts, [], faces)
mesh.update()
terrain = bpy.data.objects.new("MondayTerrain", mesh)
bpy.context.collection.objects.link(terrain)

# === 3. Material: procedural elevation-based color ===
mat = bpy.data.materials.new("MondayGround")
mat.use_nodes = True
nt = mat.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
out = nt.nodes.new("ShaderNodeOutputMaterial")
bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
mix = nt.nodes.new("ShaderNodeMixRGB")
mix.blend_type = "MIX"
mix.inputs[1].default_value = (0.55, 0.42, 0.28, 1)  # laterite
mix.inputs[2].default_value = (0.18, 0.32, 0.12, 1)  # forest
pos = nt.nodes.new("ShaderNodeNewGeometry")
separate = nt.nodes.new("ShaderNodeSeparateXYZ")
math = nt.nodes.new("ShaderNodeMath")
math.operation = "DIVIDE"
math.inputs[1].default_value = 120.0
nt.links.new(pos.outputs["Position"], separate.inputs["Vector"])
nt.links.new(separate.outputs["Z"], math.inputs[0])
nt.links.new(math.outputs["Value"], mix.inputs["Fac"])
nt.links.new(mix.outputs["Color"], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.85
nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
terrain.data.materials.append(mat)

# === 4. Creek water plane ===
print("[monday] adding creek water plane")
bpy.ops.mesh.primitive_plane_add(size=2000, enter_editmode=False, location=(0, -100, -10))
water = bpy.context.active_object
water.name = "Creek"
water.scale = (1.0, 0.1, 1.0)
mat_w = bpy.data.materials.new("CreekWater")
mat_w.use_nodes = True
nt = mat_w.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
out = nt.nodes.new("ShaderNodeOutputMaterial")
bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
bsdf.inputs["Base Color"].default_value = (0.18, 0.32, 0.28, 1)
bsdf.inputs["Roughness"].default_value = 0.1
bsdf.inputs["Transmission Weight"].default_value = 0.85
bsdf.inputs["Alpha"].default_value = 0.85
nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
water.data.materials.append(mat_w)

# === 5. Place 12 houses ===
print(f"[monday] placing {len(HOUSES)} houses + 1 community")
for h in HOUSES:
    style = h["style"]
    color = STYLE_COLORS[style]
    bpy.ops.mesh.primitive_cube_add(size=1.0, enter_editmode=False,
                                    location=(h["cx"], h["cy"], 0))
    cube = bpy.context.active_object
    cube.name = h["name"]
    cube.scale = (h["w"]/2, h["d"]/2, h["h"]/2)
    cube.rotation_euler = (0, 0, h["rotation"] * 3.14159 / 180)
    m = bpy.data.materials.new(h["name"]+"_mat")
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = (color[1], color[2], color[3], 1)
    bsdf.inputs["Roughness"].default_value = color[4]
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    cube.data.materials.append(m)
    cube["cluster"] = h["cluster"]
    cube["style"] = h["style"]

# === 6. Sun + camera ===
print("[monday] setting up sun + hero camera")
bpy.ops.object.light_add(type='SUN', location=(0, 0, 500))
sun = bpy.context.active_object
sun.data.energy = 4.0
sun.rotation_euler = (1.2, 0.0, 0.6)

# === 7. Render settings ===
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.world.use_nodes = True
wn = scene.world.node_tree
for n in list(wn.nodes): wn.nodes.remove(n)
wn_out = wn.nodes.new("ShaderNodeOutputWorld")
wn_bg = wn.nodes.new("ShaderNodeBackground")
wn_bg.inputs["Color"].default_value = (0.6, 0.75, 0.9, 1)
wn_bg.inputs["Strength"].default_value = 1.0
wn.links.new(wn_bg.outputs["Background"], wn_out.inputs["Surface"])

# === 8. Save .blend + render overview ===
print(f"[monday] saving .blend to {OUT_BLEND}")
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print(f"  Houses placed:")
for h in HOUSES:
    print(f"    {h['name']:25s} {h['cluster']:5s} {h['style']:18s} {h['w']}m x {h['d']}m x {h['h']}m @ ({h['cx']:>4}, {h['cy']:>4})")

# === 9. Multiple hero cameras per cluster ===
print(f"[monday] setting up 4 hero cameras (one per cluster)")

# Hide the giant 6km terrain beyond ~600m radius to speed up render
# We'll do this with a clipping plane + camera limits
scene.cycles.clip_start = 0.1
scene.cycles.clip_end = 800  # 800m view distance, ignore the rest of the 6km

# 4 cameras, one per cluster
CAM_PRESETS = [
    # name, position (x,y,z), look-at point, lens
    ("Cam_Overview",   ( 200, -200, 280),  ( 0,    0,  20), 35),  # top-down-ish, sees all clusters
    ("Cam_A_Italian",  (-180,   60,  80),  (-180,  0,  30), 45),  # Cluster A on upper terrace
    ("Cam_B_Bamboo",   ( -10, -120,  60),  (  10, -50,  10), 45),  # Cluster B mid-slope
    ("Cam_C_Creek",    ( 200,   20,  35),  ( 100,  20,   0), 50),  # Cluster C at the water
    ("Cam_D_EarthTree",( 250,  220,  70),  ( 200, 200,  20), 45),  # Cluster D hidden
]
for i, (name, pos, look, lens) in enumerate(CAM_PRESETS):
    bpy.ops.object.camera_add(location=pos)
    c = bpy.context.active_object
    c.name = name
    c.data.lens = lens
    # point at look-at
    direction = Vector(look) - Vector(pos)
    rot = direction.to_track_quat('-Z', 'Y').to_euler()
    c.rotation_euler = rot

# render overview first
bpy.context.scene.camera = bpy.data.objects["Cam_Overview"]
print(f"[monday] rendering overview to {OUT_DIR}/monday_overview.png")
scene.render.filepath = os.path.join(OUT_DIR, "monday_overview.png")
bpy.ops.render.render(write_still=True)

# render each cluster hero
for name, _, _, _ in CAM_PRESETS[1:]:
    bpy.context.scene.camera = bpy.data.objects[name]
    out = os.path.join(OUT_DIR, f"monday_{name.lower()}.png")
    print(f"[monday] rendering {name} to {out}")
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)

print(f"\n[monday] DONE - .blend + 5 renders at {OUT_DIR}")
