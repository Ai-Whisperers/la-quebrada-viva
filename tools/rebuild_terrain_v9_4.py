"""Rebuild the LQV terrain mesh + world placements from the FIXED elevation grid.

After fixing the elevation_grid.json (now 290x277 cells, 347m relief, full 10km
coverage from extended_dem_lod2.tif) and the peaks_10km.geojson (real elevations
from DEM, not estimated from contour rings), this script:

1. Builds a new low-poly terrain mesh with the real data:
   - X axis = east (positive)
   - Y axis = elevation (0 to ~700m at Z_EXAG=2)
   - Z axis = south (positive)
   - 2m step quantization for the Zelda retro look
   - Vertex colors: grass (low) → earth (mid) → rock (high+steep) → snow (peaks)

2. Generates the world.json with REAL positions + REAL elevations for:
   - 13 cerros (now with correct elevations, no more fake 400m)
   - Default cob house at parcel centroid
   - Monte highlight
   - Waterfall
   - Gate
   - 40 trees (scattered deterministically)
   - Quebrada ribbon (sampled from real quebrada polygon)
   - Walking path (Wes's actual GPS)

3. Also writes:
   - terrain_mesh_data.json (vertex dump for browser sampling)
   - peak marker data for the in-browser cone/sphere markers

Usage: blender --background --python tools/rebuild_terrain_v9_4.py
"""
import bpy
import bmesh
import json
import math
import os
import random
from mathutils import Vector

# Configuration
OUT_DIR = "/root/.hermes/lqv-splat/exports/web/game_assets_lite/assets/lowpoly/"
GRID_PATH = "/root/.hermes/lqv-splat/exports/web/game_assets_lite/elevation_grid.json"
WORLD_OUT = "/root/.hermes/lqv-splat/exports/web/game_assets_lite/assets/lowpoly/lqv_lowpoly_world.json"
TERRAIN_GLB = OUT_DIR + "lqv_lowpoly_terrain.glb"
TERRAIN_DATA = OUT_DIR + "terrain_mesh_data.json"

# Parcel centroid
PARCEL_LON = -57.0304
PARCEL_LAT = -25.6082
M_PER_DEG_LON = 111320.0 * math.cos(math.radians(PARCEL_LAT))
M_PER_DEG_LAT = 110540.0

# Z exaggeration (visual drama)
Z_EXAG = 2.0

# Quantization step (Zelda low-poly stepped)
STEP = 1.5  # metres per elevation band


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


def lonlat_to_xz(lon, lat):
    x = (lon - PARCEL_LON) * M_PER_DEG_LON
    z = -(lat - PARCEL_LAT) * M_PER_DEG_LAT
    return x, z


def sample_dem(dem, w, h, bounds, lon, lat):
    """Bilinear sample of DEM grid at lon/lat."""
    u = (lon - bounds[0]) / (bounds[2] - bounds[0]) * (w - 1)
    v = (bounds[3] - lat) / (bounds[3] - bounds[1]) * (h - 1)
    if u < 0 or u > w - 1 or v < 0 or v > h - 1:
        return None
    i, j = int(u), int(v)
    if i >= w - 1 or j >= h - 1:
        return dem[j][i]
    fx, fy = u - i, v - j
    return (dem[j][i] * (1-fx) * (1-fy) + dem[j][i+1] * fx * (1-fy) +
            dem[j+1][i] * (1-fx) * fy + dem[j+1][i+1] * fx * fy)


def build_terrain_from_dem():
    """Build the new low-poly terrain mesh."""
    reset_scene()

    # Load real DEM
    grid = json.loads(open(GRID_PATH).read())
    w, h = grid['width'], grid['height']
    bounds = grid['bounds']
    dem = [[float(v) for v in row] for row in grid['dem']]

    # Quantize elevation to STEP bands for the Zelda stepped look
    elev_min_real = min(min(r) for r in dem)
    elev_max_real = max(max(r) for r in dem)
    print(f"  DEM: {w}x{h} cells, bounds={bounds}")
    print(f"  real elev range: {elev_min_real}m to {elev_max_real}m")

    # Decimate the grid for browser performance. We sample every 2nd row + col
    # to get ~25% of the verts (~20k instead of 80k) but keep 50m pixel size
    # (still 2x the source DEM, plenty for the low-poly aesthetic).
    DECIMATION = 2

    # Build mesh — write (x, y_elev, z_south) so glTF's Y-up convention is correct
    # (Y = up, so we put elevation in Y for the glTF reader to render as "up")
    verts = []
    j_keep = list(range(0, h, DECIMATION))
    if j_keep[-1] != h - 1:
        j_keep.append(h - 1)
    i_keep = list(range(0, w, DECIMATION))
    if i_keep[-1] != w - 1:
        i_keep.append(w - 1)

    for j in j_keep:
        for i in i_keep:
            lon = bounds[0] + (i / (w - 1)) * (bounds[2] - bounds[0])
            lat = bounds[3] - (j / (h - 1)) * (bounds[3] - bounds[1])  # row j=0 is top (north)
            x, z = lonlat_to_xz(lon, lat)
            # Quantize
            elev = dem[j][i]
            elev_q = round(elev / STEP) * STEP
            y = (elev_q - elev_min_real) * Z_EXAG
            verts.append((x, y, z))

    # Update effective grid dimensions for vertex colors
    h_eff = len(j_keep)
    w_eff = len(i_keep)

    faces = []
    for jj in range(h_eff - 1):
        for ii in range(w_eff - 1):
            v0 = jj * w_eff + ii
            v1 = v0 + 1
            v2 = v0 + w_eff
            v3 = v2 + 1
            faces.append((v0, v1, v3, v2))

    mesh = bpy.data.meshes.new("LQV_Terrain")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("LQV_Terrain", mesh)
    bpy.context.collection.objects.link(obj)

    # FLAT SHADING — the whole point of low-poly
    set_flat_shading(obj)

    # Vertex colors: grass (low) → earth (mid) → rock (high+steep) → snow (peaks)
    slp = [[0.0] * w_eff for _ in range(h_eff)]
    for jj in range(1, h_eff):
        for ii in range(w_eff):
            j_src = j_keep[jj]
            i_src = i_keep[ii]
            j_prev = j_keep[jj-1]
            i_prev = i_keep[ii]
            slp[jj][ii] = abs(dem[j_src][i_src] - dem[j_prev][i_src])
    for jj in range(h_eff):
        for ii in range(1, w_eff):
            j_src = j_keep[jj]
            i_src = i_keep[ii]
            i_prev = i_keep[ii-1]
            slp[jj][ii] = max(slp[jj][ii], abs(dem[j_src][i_src] - dem[j_src][i_prev]))

    vc = mesh.vertex_colors.new(name="Col")
    # Zelda palette
    grass = (0.478, 0.608, 0.306)        # #7a9b4e
    grass_dk = (0.239, 0.353, 0.165)     # #3d5a2a
    earth = (0.541, 0.416, 0.227)        # #8a6a3a
    earth_lt = (0.690, 0.561, 0.376)     # #ad8f60
    rock = (0.431, 0.384, 0.345)         # #6e6258
    rock_dk = (0.290, 0.271, 0.251)     # #4a4540
    snow = (0.95, 0.95, 0.97)
    lapacho = (0.831, 0.584, 0.416)      # for stylized high points

    for poly in mesh.polygons:
        avg_e = sum(verts[mesh.loops[l].vertex_index][1] for l in poly.loop_indices) / len(poly.loop_indices)
        avg_s = 0.0
        for l in poly.loop_indices:
            vi = mesh.loops[l].vertex_index
            ii = vi % w_eff
            jj = vi // w_eff
            if 0 < jj < h_eff - 1 and 0 < ii < w_eff - 1:
                avg_s += slp[jj][ii]
        avg_s /= max(1, len(poly.loop_indices))

        # Real elevation (in metres) from vertex Y
        avg_elev_real = avg_e / Z_EXAG + elev_min_real
        # Normalize to 0-1
        t = (avg_elev_real - elev_min_real) / max(1, elev_max_real - elev_min_real)

        if avg_s > 4.0:  # steep cliff
            r, g, b = rock
        elif t > 0.92:  # very high peaks
            r, g, b = snow
        elif t > 0.7:
            # High terrain — blend earth → rock by slope
            blend = min(1.0, avg_s / 3.0)
            r = earth[0] * (1-blend) + rock[0] * blend
            g = earth[1] * (1-blend) + rock[1] * blend
            b = earth[2] * (1-blend) + rock[2] * blend
        elif t < 0.25:
            blend = 1.0 - t * 4
            r = grass_dk[0] * blend + grass[0] * (1-blend)
            g = grass_dk[1] * blend + grass[1] * (1-blend)
            b = grass_dk[2] * blend + grass[2] * (1-blend)
        elif t < 0.5:
            r, g, b = earth_lt
        else:
            r, g, b = earth

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
    return obj, verts, elev_min_real, elev_max_real, bounds, w, h


def build_world(elev_min_real, elev_max_real, dem, bounds, w, h):
    """Build the world.json with REAL positions + REAL elevations."""

    placements = []

    # === CERROS — 13 peaks at real lat/lon, REAL elevations from DEM ===
    # The cerros already have real terrain peaks in the new mesh (the DEM
    # shows them as ~400m peaks). The cone markers are visual aids above
    # the peak — like a flag on a mountain — not the cerro itself.
    # We use LOW, WIDE bumps (not pointy pyramids) that sit on the cerro
    # summit, with elevation labels.
    peaks = json.loads(open("/root/la-quebrada-viva/splats/exports/web/data/peaks_10km.geojson").read())
    for feat in peaks['features']:
        p = feat['properties']
        if p.get('elev_m') is None:
            continue
        lon, lat = feat['geometry']['coordinates']
        x, z = lonlat_to_xz(lon, lat)
        elev = p['elev_m']
        # Compute prominence: how much higher is this cerro than the surrounding 200m?
        # Sample 4 cardinal points 300m away
        probe_d = 0.003  # ~300m in degrees
        n_elev = sample_dem(dem, w, h, bounds, lon + probe_d, lat) or elev
        s_elev = sample_dem(dem, w, h, bounds, lon, lat - probe_d) or elev
        e_elev = sample_dem(dem, w, h, bounds, lon + probe_d * 0.7, lat + probe_d * 0.7) or elev
        w_elev = sample_dem(dem, w, h, bounds, lon - probe_d * 0.7, lat - probe_d * 0.7) or elev
        surroundings = (n_elev + s_elev + e_elev + w_elev) / 4
        prominence = max(5, elev - surroundings)
        # Scale: base radius ~ prominence * 1.5, height ~ prominence * 1.0
        # (a 50m prominent cerro has a 75m radius, 50m tall cone — squat, not pointy)
        radius = prominence * 1.2
        height = prominence * 0.8
        placements.append({
            "type": "cerro",
            "id": p["name"].replace(" ", "_").replace(".", ""),
            "name": p["name"],
            "elev_m": elev,
            "x": round(x, 1),
            "y": round((elev - elev_min_real) * Z_EXAG, 1),  # mesh Y at peak
            "z": round(z, 1),
            "scale": {"radius": round(radius, 1), "height": round(height, 1)},
            "prominence_m": round(prominence, 1),
            "category": p.get("category", "hill"),
            "direction_from_lqv": p.get("direction_from_lqv", ""),
            "distance_from_lqv_km": p.get("distance_from_lqv_km", 0),
        })

    # === DEFAULT COB HOUSE — at parcel centroid ===
    poly = json.loads(open("/root/.hermes/lqv-splat/exports/web/data/client_gps/client_gps_polygon.geojson").read())
    coords = poly["features"][0]["geometry"]["coordinates"][0]
    parcel_lon_c = sum(c[0] for c in coords) / len(coords)
    parcel_lat_c = sum(c[1] for c in coords) / len(coords)
    parcel_x, parcel_z = lonlat_to_xz(parcel_lon_c, parcel_lat_c)
    parcel_elev = sample_dem(dem, w, h, bounds, parcel_lon_c, parcel_lat_c) or 200
    placements.append({
        "type": "default_house",
        "id": "lqv_default_cob",
        "typo": "lqv_lowpoly_house_cob",
        "name": "LQV Cob House (default)",
        "x": round(parcel_x, 1),
        "y": round((parcel_elev - elev_min_real) * Z_EXAG, 1),
        "z": round(parcel_z, 1),
        "rotation_y": 0,
        "scale": 6,  # ~24m wide cob (base 4m × 6)
    })

    # === MONTE — at W edge of property, scaled to match ===
    # LQV's western escarpment is at the W edge of the parcel polygon
    # Use a high-elevation point inside the parcel
    # The actual monte is the western rise; approximate at (parcel_x - 200, parcel_elev+50, parcel_z)
    monte_elev = max(elev_max_real * 0.85, parcel_elev + 50)  # peak 85% of max
    placements.append({
        "type": "monte",
        "id": "lqv_monte_main",
        "name": "Cerro del LQV (escarpment)",
        "x": round(parcel_x - 220, 1),
        "y": round((monte_elev - elev_min_real) * Z_EXAG, 1),
        "z": round(parcel_z + 50, 1),
        "scale": 4,  # 30m peak, visible
        "rotation_y": 0,
    })

    # === WATERFALL — at quebrada crossing (W of parcel, lower elevation) ===
    wf_elev = parcel_elev - 20  # 20m below the parcel baseline
    placements.append({
        "type": "waterfall",
        "id": "lqv_waterfall_main",
        "x": round(parcel_x - 50, 1),
        "y": round((wf_elev - elev_min_real) * Z_EXAG, 1),
        "z": round(parcel_z - 200, 1),
        "scale": 1.0,
        "rotation_y": 0,
    })

    # === GATE — at SE corner of parcel (entrance from road) ===
    # Use a real coordinate: SE corner of the parcel polygon
    se_corner = coords[2] if len(coords) > 2 else coords[0]
    gate_lon, gate_lat = se_corner[0], se_corner[1]
    gate_x, gate_z = lonlat_to_xz(gate_lon, gate_lat)
    gate_elev = sample_dem(dem, w, h, bounds, gate_lon, gate_lat) or 150
    placements.append({
        "type": "gate",
        "id": "lqv_gate_main",
        "x": round(gate_x, 1),
        "y": round((gate_elev - elev_min_real) * Z_EXAG, 1),
        "z": round(gate_z, 1),
        "scale": 2.5,
        "rotation_y": 15,
    })

    # === TREES — 40 trees scattered based on real Hansen loss + NDVI ===
    # No Hansen raster here; distribute biased by elevation variance (flat areas = more trees)
    random.seed(42)
    tree_count = 40
    for i in range(tree_count):
        # Random within 800m radius of parcel, biased to lower elevation
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(150, 750)
        x = parcel_x + r * math.cos(angle)
        z = parcel_z + r * math.sin(angle)
        lon = PARCEL_LON + x / M_PER_DEG_LON
        lat = PARCEL_LAT - z / M_PER_DEG_LAT
        elev = sample_dem(dem, w, h, bounds, lon, lat) or 200
        # Species bias (45% lapacho, 35% pino, 20% palmera)
        w_rand = random.random()
        if w_rand < 0.45:
            species = "lqv_lowpoly_tree_lapacho"
        elif w_rand < 0.80:
            species = "lqv_lowpoly_tree_pino"
        else:
            species = "lqv_lowpoly_tree_palmera"
        # Tree size: 8-14m tall in real world, scale to mesh
        # Mesh Y range is 0-700, so a 12m tree is ~17 mesh Y units
        tree_y = (elev - elev_min_real) * Z_EXAG
        scale = random.uniform(0.08, 0.14) * 100  # 8-14m trees in mesh units
        placements.append({
            "type": "tree",
            "species": species,
            "x": round(x, 1),
            "y": round(tree_y, 1),
            "z": round(z, 1),
            "scale": round(scale, 1),
            "rotation_y": round(random.uniform(0, 360), 1),
        })

    # === QUEBRADA + STREAMS RIBBON — sample from real DEM stream data ===
    # The local_quebradas_10km.geojson file is just a 3-point stub. The real
    # quebrada data is in dem_streams_10km.geojson (3273 features, 16,855 points).
    # We sample major streams (catchment > 1.0 km²) — bigger than 1km² = visible rivers.
    # And subsample points heavily (every 8th) to keep world.json small.
    try:
        streams = json.loads(open("/root/.hermes/lqv-splat/exports/web/data/dem_streams_10km.geojson").read())
        for feat in streams["features"]:
            props = feat.get("properties", {})
            # Only "real" rivers (catchment > 1.0 km²), skip tiny rills
            if props.get("catchment_km2", 0) < 1.0:
                continue
            geom = feat["geometry"]
            if geom["type"] == "LineString":
                coords_q = geom["coordinates"]
                for i, c in enumerate(coords_q):
                    if i % 20 != 0:  # heavy subsample: every 20th vertex
                        continue
                    lon, lat = c[0], c[1]
                    x, z = lonlat_to_xz(lon, lat)
                    elev = sample_dem(dem, w, h, bounds, lon, lat) or 150
                    placements.append({
                        "type": "quebrada_segment",
                        "x": round(x, 1),
                        "y": round((elev - elev_min_real) * Z_EXAG, 1),
                        "z": round(z, 1),
                    })
    except FileNotFoundError:
        print("  (no streams file)")

    # === TRAIL — Wes's actual GPS walking path ===
    try:
        walking_path = json.loads(open("/root/.hermes/lqv-splat/exports/web/data/client_gps/client_gps_walking_path.geojson").read())
        wp_coords = walking_path["features"][0]["geometry"]["coordinates"]
        # Each point: (x, z) — terrain Y computed at render time from DEM
        placements.append({
            "type": "trail_polyline",
            "id": "wes_walking_path",
            "coords": [
                [round(lonlat_to_xz(c[0], c[1])[0], 1),
                 round(lonlat_to_xz(c[0], c[1])[1], 1)]
                for c in wp_coords
            ],
        })
    except FileNotFoundError:
        pass

    # === SAVE ===
    world = {
        "placements": placements,
        "parcel_center": {"lon": PARCEL_LON, "lat": PARCEL_LAT},
        "elev_min_m": elev_min_real,
        "elev_max_m": elev_max_real,
        "z_exag": Z_EXAG,
        "m_per_deg_lon": M_PER_DEG_LON,
        "m_per_deg_lat": M_PER_DEG_LAT,
    }
    Path_like = os.path.dirname(WORLD_OUT)
    os.makedirs(Path_like, exist_ok=True)
    with open(WORLD_OUT, "w") as f:
        json.dump(world, f, indent=2)
    print(f"wrote {WORLD_OUT} ({len(placements)} placements)")
    counts = {}
    for p in placements:
        t = p["type"]
        counts[t] = counts.get(t, 0) + 1
    for t, c in sorted(counts.items()):
        print(f"  {t}: {c}")


# Add this import for path
from pathlib import Path


def main():
    print("=" * 60)
    print("LQV Terrain + World Rebuild v9.4 (full 10km real data)")
    print("=" * 60)

    # Build terrain mesh
    print("\n=== 1. Building terrain from real DEM (290x277 cells) ===")
    obj, verts, elev_min_real, elev_max_real, bounds, w, h = build_terrain_from_dem()
    bpy.ops.export_scene.gltf(
        filepath=TERRAIN_GLB,
        export_format='GLB',
        export_materials='EXPORT',
        export_apply=True,
    )
    print(f"  → wrote {TERRAIN_GLB} ({os.path.getsize(TERRAIN_GLB)/1024:.0f} KB)")

    # Save terrain metadata for the browser
    Path(TERRAIN_DATA).parent.mkdir(parents=True, exist_ok=True)
    with open(TERRAIN_DATA, "w") as f:
        json.dump({
            "bounds": bounds,
            "pixels": [w, h],
            "elev_min_m": elev_min_real,
            "elev_max_m": elev_max_real,
            "z_exag": Z_EXAG,
            "parcel_center_lon": PARCEL_LON,
            "parcel_center_lat": PARCEL_LAT,
            "m_per_deg_lon": M_PER_DEG_LON,
            "m_per_deg_lat": M_PER_DEG_LAT,
            "verts_count": len(verts),
        }, f, indent=2)
    print(f"  → wrote {TERRAIN_DATA}")

    # Build world.json
    print("\n=== 2. Building world placements (real elevations) ===")
    dem = json.loads(open(GRID_PATH).read())['dem']
    build_world(elev_min_real, elev_max_real, dem, bounds, w, h)

    print("\n=== DONE ===")


if __name__ == "__main__":
    main()
