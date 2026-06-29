"""Build the post-escritura property map from satellite + DEM + OSM data.

Inputs (all live in docs/site_data/):
  escobar_property_polygon.geojson        EPSG:4326 — Wesley's 30.9 ha polygon
  extended_aoi/polygon_ndvi.tif           EPSG:32721 — Sentinel-2 NDVI
  extended_aoi/cop30_dem.tif              EPSG:4326 — Copernicus 30 m DEM
  /tmp/.../scratchpad/osm_*.json          Overpass raw — buildings, roads, natural

Outputs (under docs/site_data/property_map/):
  vector/buildings_osm.geojson            9 OSM building polygons (EPSG:4326)
  vector/roads_osm.geojson                1 OSM road LineString — Camino a Escobar
  vector/natural_osm.geojson              2 OSM farmland polygons
  vector/canopy_classes.geojson           NDVI-derived 4-class polygons (EPSG:4326)
  vector/hydrography_dem.geojson          D8 flow accumulation streams (EPSG:4326)
  raster/canopy_classes.tif               int8 class raster (EPSG:32721)
  quicklooks/canopy.png                   NDVI classes alone
  quicklooks/water.png                    DEM hydrography alone
  property_map.png                        Composite — 300 dpi, EPSG:32721 axes

Trees DEFERRED: 10 m Sentinel-2 cannot identify individual crowns. Need sub-1m
imagery or R35 drone LiDAR. Canopy density classes ship instead.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from matplotlib.colors import LightSource, ListedColormap, BoundaryNorm
from pyproj import Transformer
from rasterio.features import shapes as rio_shapes
from rasterio.transform import xy as rio_xy
from rasterio.warp import Resampling, calculate_default_transform, reproject, transform_geom

ROOT = Path("/home/ai-whisperers/blender-projects/la-quebrada-viva")
POLY = ROOT / "docs/site_data/escobar_property_polygon.geojson"
NDVI = ROOT / "docs/site_data/extended_aoi/polygon_ndvi.tif"
DEM = ROOT / "docs/site_data/extended_aoi/cop30_dem.tif"
SCRATCH = Path(
    "/tmp/claude-1000/-home-ai-whisperers-blender-projects/"
    "588baf01-c2bb-47a3-83d8-58eaa8f69ae8/scratchpad"
)
OUT = ROOT / "docs/site_data/property_map"
FETCHED = "2026-06-28"

# --- polygon -----------------------------------------------------------------

def load_polygon_4326():
    raw = json.loads(POLY.read_text())
    for feat in raw["features"]:
        if feat["geometry"]["type"] == "Polygon":
            return feat["geometry"]
    raise RuntimeError("no Polygon feature in escobar_property_polygon.geojson")


# --- OSM ---------------------------------------------------------------------

def _osm_to_features(path: Path, default_kind: str) -> list[dict]:
    """Resolve Overpass element list to GeoJSON Features.

    Closed ways (first id == last id) → Polygon. Open ways → LineString.
    Bare nodes are skipped (they are vertex-only references for ways).
    """
    raw = json.loads(path.read_text())
    elems = raw.get("elements", [])
    nodes = {n["id"]: (n["lon"], n["lat"]) for n in elems if n["type"] == "node"}
    feats = []
    for el in elems:
        if el["type"] != "way":
            continue
        ids = el.get("nodes") or []
        if len(ids) < 2:
            continue
        coords = [nodes[i] for i in ids if i in nodes]
        if len(coords) < 2:
            continue
        tags = el.get("tags") or {}
        is_closed = ids[0] == ids[-1] and len(coords) >= 3
        if is_closed:
            geom = {"type": "Polygon", "coordinates": [coords]}
        else:
            geom = {"type": "LineString", "coordinates": coords}
        props = {
            "source": "OSM",
            "osm_id": el["id"],
            "fetched": FETCHED,
            "verification": "pending photos",
            "kind": default_kind,
            **tags,
        }
        feats.append({"type": "Feature", "properties": props, "geometry": geom})
    return feats


def write_fc(path: Path, features: list[dict], name: str, description: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fc = {
        "type": "FeatureCollection",
        "name": name,
        "description": description,
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": features,
    }
    path.write_text(json.dumps(fc, indent=2))


# --- canopy classes ----------------------------------------------------------

CANOPY_BINS = [-1.0, 0.3, 0.6, 0.85, 1.01]
CANOPY_LABELS = {1: "bare (<0.30)", 2: "sparse (0.30–0.60)", 3: "mid (0.60–0.85)", 4: "dense (>0.85)"}
CANOPY_COLORS = {1: "#c97d4a", 2: "#d6c060", 3: "#8aa055", 4: "#2f4a1e"}


def build_canopy_layers(poly_4326: dict) -> dict:
    """Classify NDVI into 4 density bins; write GeoJSON + GeoTIFF + quicklook."""
    with rasterio.open(NDVI) as src:
        ndvi = src.read(1)
        transform = src.transform
        src_crs = src.crs
        bounds = src.bounds
    classes = np.digitize(ndvi, CANOPY_BINS[1:-1]).astype(np.int16) + 1
    classes[np.isnan(ndvi)] = 0
    valid_mask = classes > 0

    (OUT / "raster").mkdir(parents=True, exist_ok=True)
    out_raster = OUT / "raster/canopy_classes.tif"
    profile = {
        "driver": "GTiff", "dtype": "uint8", "count": 1,
        "height": ndvi.shape[0], "width": ndvi.shape[1],
        "transform": transform, "crs": src_crs, "nodata": 0,
        "compress": "deflate", "predictor": 2, "tiled": True,
    }
    with rasterio.open(out_raster, "w", **profile) as dst:
        dst.write(classes.astype(np.uint8), 1)

    feats = []
    for geom, val in rio_shapes(classes.astype(np.int32), mask=valid_mask, transform=transform):
        ival = int(val)
        if ival == 0:
            continue
        geom_4326 = transform_geom(src_crs.to_string(), "EPSG:4326", geom)
        feats.append({
            "type": "Feature",
            "properties": {
                "class_id": ival,
                "class_label": CANOPY_LABELS[ival],
                "source": "Sentinel-2 S2B_21JVM_20260512_0_L2A NDVI",
                "method": "digitize 4 bins [<0.30, 0.30-0.60, 0.60-0.85, >0.85]",
                "fetched": FETCHED,
                "verification": "pending photos",
            },
            "geometry": geom_4326,
        })
    write_fc(
        OUT / "vector/canopy_classes.geojson", feats,
        "canopy_classes",
        "NDVI-derived canopy density classes (4 bins) within the 30.9 ha polygon. "
        "Individual tree positions DEFERRED to R35 / sub-1m imagery.",
    )

    # quicklook in NDVI native CRS (UTM 21S)
    fig, ax = plt.subplots(figsize=(8, 7))
    cmap = ListedColormap([CANOPY_COLORS[1], CANOPY_COLORS[2], CANOPY_COLORS[3], CANOPY_COLORS[4]])
    norm = BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5], cmap.N)
    show = np.ma.masked_where(~valid_mask, classes)
    extent = (bounds.left, bounds.right, bounds.bottom, bounds.top)
    ax.imshow(show, extent=extent, origin="upper", cmap=cmap, norm=norm)
    poly_utm = transform_geom("EPSG:4326", src_crs.to_string(), poly_4326)
    xs = [c[0] for c in poly_utm["coordinates"][0]]
    ys = [c[1] for c in poly_utm["coordinates"][0]]
    ax.plot(xs, ys, color="white", lw=2, label="polygon")
    ax.plot(xs, ys, color="black", lw=1)
    handles = [mpatches.Patch(color=CANOPY_COLORS[k], label=CANOPY_LABELS[k]) for k in (1, 2, 3, 4)]
    ax.legend(handles=handles, loc="lower left", fontsize=8)
    ax.set_title("Canopy density (NDVI) — 30.9 ha polygon\nSentinel-2 2026-05-12, 10 m, photo verification pending")
    ax.set_xlabel("UTM 21S Easting (m)")
    ax.set_ylabel("UTM 21S Northing (m)")
    (OUT / "quicklooks").mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "quicklooks/canopy.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    return {
        "classes": classes,
        "valid": valid_mask,
        "transform": transform,
        "src_crs": src_crs,
        "bounds": bounds,
    }


# --- hydrography (pure-numpy D8) --------------------------------------------

D8_CODE = np.array([32, 64, 128, 16, 1, 4, 2, 8], dtype=np.int16)
D8_DY = np.array([-1, -1, -1, 0, 0, 1, 1, 1], dtype=np.int8)
D8_DX = np.array([-1, 0, 1, -1, 1, -1, 0, 1], dtype=np.int8)


def fill_pits(dem: np.ndarray, max_iter: int = 50) -> np.ndarray:
    """Iterative pit-filling: raise interior cells to the min of any neighbour
    above them by an epsilon. Cheap and good enough for sub-parcel streams."""
    f = dem.copy().astype(np.float32)
    h, w = f.shape
    for _ in range(max_iter):
        changed = False
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                nb = f[y - 1:y + 2, x - 1:x + 2]
                nb_min = nb.min()
                if f[y, x] < nb_min:
                    f[y, x] = nb_min + 1e-4
                    changed = True
        if not changed:
            break
    return f


def d8_flow_dir(fdem: np.ndarray) -> np.ndarray:
    h, w = fdem.shape
    fdir = np.zeros((h, w), dtype=np.int16)
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            best_drop = 0.0
            best_code = 0
            here = fdem[y, x]
            for k in range(8):
                dy, dx = int(D8_DY[k]), int(D8_DX[k])
                dist = math.sqrt(dy * dy + dx * dx)
                drop = (here - fdem[y + dy, x + dx]) / dist
                if drop > best_drop:
                    best_drop = drop
                    best_code = int(D8_CODE[k])
            fdir[y, x] = best_code
    return fdir


def flow_accum(fdir: np.ndarray) -> np.ndarray:
    h, w = fdir.shape
    acc = np.ones((h, w), dtype=np.int32)
    code_to_dydx = {int(D8_CODE[k]): (int(D8_DY[k]), int(D8_DX[k])) for k in range(8)}
    # in-degree
    indeg = np.zeros((h, w), dtype=np.int16)
    for y in range(h):
        for x in range(w):
            c = int(fdir[y, x])
            if c == 0:
                continue
            dy, dx = code_to_dydx[c]
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w:
                indeg[ny, nx] += 1
    # Kahn-style topological accumulation
    stack = [(y, x) for y in range(h) for x in range(w) if indeg[y, x] == 0]
    while stack:
        y, x = stack.pop()
        c = int(fdir[y, x])
        if c == 0:
            continue
        dy, dx = code_to_dydx[c]
        ny, nx = y + dy, x + dx
        if not (0 <= ny < h and 0 <= nx < w):
            continue
        acc[ny, nx] += acc[y, x]
        indeg[ny, nx] -= 1
        if indeg[ny, nx] == 0:
            stack.append((ny, nx))
    return acc


def trace_streams(fdir: np.ndarray, acc: np.ndarray, threshold: int) -> list[list[tuple[int, int]]]:
    """For each stream-cell with no upstream stream-cell, walk downstream until
    the chain leaves the stream mask. Returns a list of (row, col) chains."""
    h, w = fdir.shape
    is_stream = acc >= threshold
    code_to_dydx = {int(D8_CODE[k]): (int(D8_DY[k]), int(D8_DX[k])) for k in range(8)}
    # heads = stream cell with no upstream stream-cell flowing into it
    heads = []
    for y in range(h):
        for x in range(w):
            if not is_stream[y, x]:
                continue
            has_upstream = False
            for k in range(8):
                ny, nx = y - int(D8_DY[k]), x - int(D8_DX[k])
                if not (0 <= ny < h and 0 <= nx < w):
                    continue
                if not is_stream[ny, nx]:
                    continue
                c = int(fdir[ny, nx])
                if c == 0:
                    continue
                ddy, ddx = code_to_dydx[c]
                if ny + ddy == y and nx + ddx == x:
                    has_upstream = True
                    break
            if not has_upstream:
                heads.append((y, x))
    chains = []
    seen = set()
    for hy, hx in heads:
        y, x = hy, hx
        chain = []
        while is_stream[y, x] and (y, x) not in seen:
            chain.append((y, x))
            seen.add((y, x))
            c = int(fdir[y, x])
            if c == 0:
                break
            dy, dx = code_to_dydx[c]
            ny, nx = y + dy, x + dx
            if not (0 <= ny < h and 0 <= nx < w):
                break
            y, x = ny, nx
        if len(chain) >= 2:
            chains.append(chain)
    return chains


def build_hydrography(poly_4326: dict, threshold_cells: int = 30) -> dict:
    with rasterio.open(DEM) as src:
        dem = src.read(1).astype(np.float32)
        dem_transform = src.transform
        dem_crs = src.crs
        dem_bounds = src.bounds
    fdem = fill_pits(dem)
    fdir = d8_flow_dir(fdem)
    acc = flow_accum(fdir)
    chains = trace_streams(fdir, acc, threshold=threshold_cells)

    # Polygon bbox (with 60 m / ~0.00055° buffer) for clipping
    coords = poly_4326["coordinates"][0]
    lons = [c[0] for c in coords]
    lats = [c[1] for c in coords]
    pad = 60.0 / 111_320.0  # ~60 m at equator, fine for 25°S latitude
    bbox = (min(lons) - pad, min(lats) - pad, max(lons) + pad, max(lats) + pad)

    feats = []
    for chain in chains:
        ll = [rio_xy(dem_transform, r, c, offset="center") for (r, c) in chain]
        # clip to bbox
        keep = [(x, y) for (x, y) in ll if bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3]]
        if len(keep) < 2:
            continue
        feats.append({
            "type": "Feature",
            "properties": {
                "source": "flow_accum_cop30",
                "method": f"D8 fill_pits + flow_accum, threshold={threshold_cells} cells (~{threshold_cells*30*30/10000:.1f} ha catchment)",
                "vertex_count": len(keep),
                "fetched": FETCHED,
                "verification": "pending photos",
            },
            "geometry": {"type": "LineString", "coordinates": keep},
        })
    write_fc(
        OUT / "vector/hydrography_dem.geojson", feats,
        "hydrography_dem",
        "DEM-derived stream lines from Copernicus 30 m D8 flow accumulation. "
        "All segments PHOTO-PENDING — NDWI = 0 % open water inside polygon.",
    )

    # quicklook (DEM hillshade + streams)
    ls = LightSource(azdeg=315, altdeg=45)
    hs = ls.hillshade(dem, vert_exag=2.0, dx=30, dy=30)
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.imshow(hs, extent=(dem_bounds.left, dem_bounds.right, dem_bounds.bottom, dem_bounds.top),
              origin="upper", cmap="gray")
    for f in feats:
        xs, ys = zip(*f["geometry"]["coordinates"])
        ax.plot(xs, ys, color="steelblue", lw=1.6)
    poly_xs = [c[0] for c in coords]
    poly_ys = [c[1] for c in coords]
    ax.plot(poly_xs, poly_ys, color="red", lw=1.5, label="polygon")
    ax.set_xlim(bbox[0], bbox[2])
    ax.set_ylim(bbox[1], bbox[3])
    ax.set_title(f"DEM hydrography — D8 flow accumulation\nthreshold={threshold_cells} cells (~{threshold_cells*30*30/10000:.1f} ha catchment), pending photo verification")
    ax.set_xlabel("Lon (EPSG:4326)")
    ax.set_ylabel("Lat (EPSG:4326)")
    fig.savefig(OUT / "quicklooks/water.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    return {"features": feats, "dem": dem, "transform": dem_transform, "crs": dem_crs}


# --- composite ---------------------------------------------------------------

def reproject_dem_to_utm(target_crs: str = "EPSG:32721", padding_m: float = 60.0):
    with rasterio.open(DEM) as src:
        # Pad bounds in degrees roughly equivalent to padding_m
        pad_deg = padding_m / 111_320.0
        b = src.bounds
        target_w, target_s, target_e, target_n = (
            b.left - pad_deg, b.bottom - pad_deg, b.right + pad_deg, b.top + pad_deg
        )
        transform, width, height = calculate_default_transform(
            src.crs, target_crs,
            src.width, src.height,
            target_w, target_s, target_e, target_n,
            resolution=30.0,
        )
        out = np.zeros((height, width), dtype=np.float32)
        reproject(
            source=rasterio.band(src, 1),
            destination=out,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=transform,
            dst_crs=target_crs,
            resampling=Resampling.bilinear,
        )
    return out, transform


def composite(poly_4326, canopy, hydro, buildings, roads, naturals):
    target_crs = "EPSG:32721"
    dem_u, dem_u_transform = reproject_dem_to_utm(target_crs)

    # axes extent in UTM
    h, w = dem_u.shape
    dem_left = dem_u_transform.c
    dem_top = dem_u_transform.f
    dem_right = dem_left + w * dem_u_transform.a
    dem_bottom = dem_top + h * dem_u_transform.e  # e is negative

    # polygon → UTM
    poly_utm = transform_geom("EPSG:4326", target_crs, poly_4326)
    poly_xy = poly_utm["coordinates"][0]
    poly_xs = [c[0] for c in poly_xy]
    poly_ys = [c[1] for c in poly_xy]

    # polygon-tight extent with 80 m padding
    pad = 80.0
    xmin, xmax = min(poly_xs) - pad, max(poly_xs) + pad
    ymin, ymax = min(poly_ys) - pad, max(poly_ys) + pad

    ls = LightSource(azdeg=315, altdeg=45)
    hs = ls.hillshade(dem_u, vert_exag=2.0, dx=30, dy=30)

    fig, ax = plt.subplots(figsize=(12, 11))
    ax.imshow(hs, extent=(dem_left, dem_right, dem_bottom, dem_top),
              origin="upper", cmap="gray", alpha=0.85)

    # canopy classes (still in EPSG:32721 native) — re-read for masked overlay
    classes = canopy["classes"]
    valid = canopy["valid"]
    cb = canopy["bounds"]
    cmap = ListedColormap([CANOPY_COLORS[1], CANOPY_COLORS[2], CANOPY_COLORS[3], CANOPY_COLORS[4]])
    norm = BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5], cmap.N)
    ax.imshow(
        np.ma.masked_where(~valid, classes),
        extent=(cb.left, cb.right, cb.bottom, cb.top),
        origin="upper", cmap=cmap, norm=norm, alpha=0.55,
    )

    # streams (reproject from 4326 to UTM)
    tx = Transformer.from_crs("EPSG:4326", target_crs, always_xy=True)
    for f in hydro["features"]:
        xs, ys = zip(*f["geometry"]["coordinates"])
        xu, yu = tx.transform(xs, ys)
        ax.plot(xu, yu, color="steelblue", lw=2.0, alpha=0.95)

    # buildings (polygons)
    for f in buildings:
        coords = f["geometry"]["coordinates"][0]
        xs, ys = zip(*coords)
        xu, yu = tx.transform(xs, ys)
        ax.fill(xu, yu, facecolor="#cc3333", edgecolor="#660000", lw=1.0, alpha=0.9)

    # roads (LineString)
    for f in roads:
        coords = f["geometry"]["coordinates"]
        xs, ys = zip(*coords)
        xu, yu = tx.transform(xs, ys)
        ax.plot(xu, yu, color="#a07040", lw=1.6, linestyle="--", alpha=0.9)

    # naturals (farmland polygons, hashed)
    for f in naturals:
        coords = f["geometry"]["coordinates"][0]
        xs, ys = zip(*coords)
        xu, yu = tx.transform(xs, ys)
        ax.fill(xu, yu, facecolor="none", edgecolor="#9b8b3a", hatch="///", lw=0.8, alpha=0.6)

    # polygon boundary on top
    ax.plot(poly_xs, poly_ys, color="white", lw=3)
    ax.plot(poly_xs, poly_ys, color="black", lw=1.5)

    # scale bar (200 m) in the bottom-left
    sb_x = xmin + 60
    sb_y = ymin + 60
    ax.plot([sb_x, sb_x + 200], [sb_y, sb_y], color="black", lw=3)
    ax.text(sb_x + 100, sb_y + 12, "200 m", ha="center", va="bottom", fontsize=10, color="black")

    # north arrow (top-right)
    na_x = xmax - 80
    na_y = ymax - 120
    ax.annotate("N", xy=(na_x, na_y + 120), xytext=(na_x, na_y),
                ha="center", fontsize=13, color="black",
                arrowprops=dict(arrowstyle="->", color="black", lw=2))

    # legend
    handles = [
        mpatches.Patch(color=CANOPY_COLORS[4], label="dense canopy (NDVI>0.85)"),
        mpatches.Patch(color=CANOPY_COLORS[3], label="mid canopy (0.60–0.85)"),
        mpatches.Patch(color=CANOPY_COLORS[2], label="sparse (0.30–0.60)"),
        mpatches.Patch(color=CANOPY_COLORS[1], label="bare (<0.30)"),
        mpatches.Patch(color="steelblue", label="DEM stream (D8 flow-accum, pending verify)"),
        mpatches.Patch(color="#cc3333", label="OSM building (n=9)"),
        mpatches.Patch(color="#a07040", label="OSM unpaved road — Camino a Escobar"),
        mpatches.Patch(facecolor="none", edgecolor="#9b8b3a", hatch="///", label="OSM farmland (n=2)"),
    ]
    ax.legend(handles=handles, loc="lower right", fontsize=8, framealpha=0.92)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.set_title(
        "La Quebrada Viva — property map (post-escritura, T+1)\n"
        "30.9 ha buildable Mbopicua cluster per Wesley's KML — scope-lock 2026-06-28 (DECISIONS.md)\n"
        "Sentinel-2 NDVI canopy · COP30 hydrography · OSM buildings/road — ALL PHOTO-PENDING",
        fontsize=11, pad=14,
    )
    ax.set_xlabel("UTM 21S Easting (m)")
    ax.set_ylabel("UTM 21S Northing (m)")

    out_png = OUT / "property_map.png"
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)

    return out_png


# --- main --------------------------------------------------------------------

def main():
    poly_4326 = load_polygon_4326()

    print("[1/5] OSM → GeoJSON")
    buildings = _osm_to_features(SCRATCH / "osm_buildings.json", "building")
    roads = _osm_to_features(SCRATCH / "osm_roads.json", "road")
    naturals = _osm_to_features(SCRATCH / "osm_natural.json", "landuse")
    write_fc(OUT / "vector/buildings_osm.geojson", buildings,
             "buildings_osm", f"OSM building features, fetched {FETCHED}.")
    write_fc(OUT / "vector/roads_osm.geojson", roads,
             "roads_osm", f"OSM road LineStrings, fetched {FETCHED}.")
    write_fc(OUT / "vector/natural_osm.geojson", naturals,
             "natural_osm", f"OSM natural/landuse polygons, fetched {FETCHED}.")
    print(f"     buildings={len(buildings)} roads={len(roads)} natural={len(naturals)}")

    print("[2/5] canopy classes")
    canopy = build_canopy_layers(poly_4326)

    print("[3/5] hydrography (D8 flow accumulation)")
    hydro = build_hydrography(poly_4326, threshold_cells=30)
    print(f"     streams={len(hydro['features'])}")

    print("[4/5] composite map")
    out = composite(poly_4326, canopy, hydro, buildings, roads, naturals)
    print(f"     wrote {out}")

    print("[5/5] done")


if __name__ == "__main__":
    main()
