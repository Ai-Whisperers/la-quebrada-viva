"""House-construction-scale terrain DSL.

The 62-ha satellite-DEM pivot (``lqv/site/terrain_62ha.py``) resolves the parcel
as one undifferentiated bowl. This module gives a meter-scale heightfield with
named features (hills, creek, river, paths, tree scatters) and explicit
``place_house`` snapping so Wesley's 14 typologies and 4 amenities can be sited
on a terrain that registers their footprints, not the parcel envelope.

Internal model: a 2-D ``numpy.ndarray[H, W]`` heightfield in metres, plus three
feature lists (``features``, ``scatters``, ``placements``). All public coords
are in metres in world space (``origin`` is the world-space xy of grid cell
[0, 0]). The DSL is renderer-agnostic — ``to_blender()`` lifts the heightfield
into Cycles geometry, but the data model can also be serialized for BoQ
rollups and validation without Blender.

Single-river invariant: ``river()`` raises on second call.

Snap modes for ``place_house()``:
    ``'pad'``    — flatten under the footprint to the local average height,
                   adding a pad collar of ``pad_size_m`` (default 1.0 m).
    ``'stilts'`` — leave the heightfield untouched; the builder lifts the
                   structure on stilts.
    ``'cut'``   — excavate the hillside under the footprint by the maximum
                   delta between footprint corners and the lowest corner
                   (hobbit-house / cob-bottle case).

See ``docs/TERRAIN_PIVOT.md`` §5 for the long-form design and §3/§4 for the
per-typology / per-amenity DSL hookup. Critical for parcel-scale renders:
the caller MUST set ``cam.data.clip_end`` to >= ``self.z_clip_end`` (default
20_000 m) before rendering, or the HDRI is all that survives the clip
(memory ``feedback_subscene_clip_end``).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Iterable, Literal, Sequence

import numpy as np

Vec2 = tuple[float, float]
Vec3 = tuple[float, float, float]
Polyline = Sequence[Vec2]
Polygon = Sequence[Vec2]
Falloff = Literal['gaussian', 'linear', 'cosine']
SnapMode = Literal['pad', 'stilts', 'cut', 'flatten_to_min']


# --- Feature dataclasses ---------------------------------------------------

@dataclass
class Feature:
    """Generic terrain feature record (hill, creek, river, path)."""
    kind: str
    params: dict = field(default_factory=dict)


@dataclass
class ScatterCluster:
    """Tree / shrub scatter polygon — actual placement is deferred to
    ``to_blender()`` so the cluster can be re-driven without rebuilding the
    heightfield.
    """
    species: str
    polygon: tuple[Vec2, ...]
    density_per_ha: float
    jitter: float
    seed: int
    # populated lazily by ``_resolve_scatters`` during ``to_blender()``:
    points: list[Vec3] = field(default_factory=list)


@dataclass
class Placement:
    """A house/amenity footprint placed at a world-space xy with rotation.

    ``footprint`` is a tuple of (x, y) corners in the local footprint frame
    (so a 6x4 m rectangle is e.g. ((-3,-2),(3,-2),(3,2),(-3,2))). It is
    rotated by ``rotation_deg`` and translated to ``xy`` before being applied
    to the heightfield in ``snap`` mode.
    """
    footprint: tuple[Vec2, ...]
    xy: Vec2
    rotation_deg: float
    snap: SnapMode
    pad_size_m: float
    cut_depth_m: float = 0.6  # only used by snap='cut'
    # populated by ``_apply_placement``:
    base_z: float = 0.0
    world_corners: tuple[Vec3, ...] = ()


# --- Heightfield primitives -------------------------------------------------

def _xy_to_ij(x: float, y: float, origin: Vec2, cell_m: float) -> tuple[float, float]:
    """World metres → grid index (sub-cell floats, no clipping)."""
    return (y - origin[1]) / cell_m, (x - origin[0]) / cell_m


def _polyline_length(polyline: Polyline) -> float:
    out = 0.0
    for (x0, y0), (x1, y1) in zip(polyline, polyline[1:]):
        out += math.hypot(x1 - x0, y1 - y0)
    return out


def _polygon_area_m2(polygon: Polygon) -> float:
    """Shoelace, magnitude only."""
    if len(polygon) < 3:
        return 0.0
    s = 0.0
    n = len(polygon)
    for i in range(n):
        x0, y0 = polygon[i]
        x1, y1 = polygon[(i + 1) % n]
        s += x0 * y1 - x1 * y0
    return abs(s) * 0.5


def _point_in_polygon(x: float, y: float, polygon: Polygon) -> bool:
    """Ray-casting; edge cases tie-break consistently."""
    inside = False
    n = len(polygon)
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        intersect = ((yi > y) != (yj > y)) and \
            (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi)
        if intersect:
            inside = not inside
        j = i
    return inside


def _polygons_intersect_sat(a: Sequence[Vec2], b: Sequence[Vec2]) -> bool:
    """Separating Axis Theorem on two convex polygons.

    Returns True iff the polygons overlap (share interior area) or one
    contains the other. Prior overlap check used axis-aligned bounding
    boxes which produces a torrent of false positives whenever two
    rectangular footprints sit corner-to-corner along an off-axis row:
    AABBs overlap, polygons don't, validate_geo() yells, layout author
    fights the validator instead of trusting it.

    SAT only correctly handles convex polygons. House footprints in the
    LQV DSL are always convex rectangles (and the few non-rect typology
    footprints are still convex), so this is sufficient. If a typology
    ever ships a concave footprint, decompose to a convex hull or
    triangulate before calling.
    """
    if len(a) < 3 or len(b) < 3:
        return False
    for poly in (a, b):
        n = len(poly)
        for i in range(n):
            x0, y0 = poly[i]
            x1, y1 = poly[(i + 1) % n]
            # outward normal of edge (x0,y0)->(x1,y1):
            nx, ny = y1 - y0, -(x1 - x0)
            # project both polygons onto this axis
            a_min = a_max = a[0][0] * nx + a[0][1] * ny
            for (x, y) in a[1:]:
                v = x * nx + y * ny
                if v < a_min:
                    a_min = v
                if v > a_max:
                    a_max = v
            b_min = b_max = b[0][0] * nx + b[0][1] * ny
            for (x, y) in b[1:]:
                v = x * nx + y * ny
                if v < b_min:
                    b_min = v
                if v > b_max:
                    b_max = v
            # any axis with a gap separates the polygons
            if a_max < b_min or b_max < a_min:
                return False
    return True


def _rotate_footprint(footprint: Iterable[Vec2], rotation_deg: float,
                      xy: Vec2) -> tuple[Vec2, ...]:
    rad = math.radians(rotation_deg)
    cos_r, sin_r = math.cos(rad), math.sin(rad)
    out = []
    for (x, y) in footprint:
        rx = x * cos_r - y * sin_r + xy[0]
        ry = x * sin_r + y * cos_r + xy[1]
        out.append((rx, ry))
    return tuple(out)


# --- Terrain ----------------------------------------------------------------

class Terrain:
    """House-scale heightfield with named features.

    All public coordinates are metres. The heightfield grid has cell size
    ``cell_m`` (default 0.5 m); ``width_m`` is the +x extent and ``depth_m``
    is the +y extent. ``origin`` is the world-space (x, y) of grid cell
    [0, 0] (lower-left corner of the grid).
    """

    def __init__(self, width_m: float, depth_m: float,
                 cell_m: float = 0.5, origin: Vec2 = (0.0, 0.0),
                 z_clip_end: float = 20000.0):
        if width_m <= 0 or depth_m <= 0:
            raise ValueError(f"width_m/depth_m must be > 0, got {width_m}/{depth_m}")
        if cell_m <= 0:
            raise ValueError(f"cell_m must be > 0, got {cell_m}")
        self.width_m = float(width_m)
        self.depth_m = float(depth_m)
        self.cell_m = float(cell_m)
        self.origin = (float(origin[0]), float(origin[1]))
        self.z_clip_end = float(z_clip_end)

        self.W = max(2, int(math.ceil(self.width_m / self.cell_m)) + 1)
        self.H = max(2, int(math.ceil(self.depth_m / self.cell_m)) + 1)
        self.height = np.zeros((self.H, self.W), dtype=np.float32)
        # Snapshot of the heightfield **before** any channel incision. The
        # houses-under-water check in validate_geo() compares house base_z
        # against the original ground at the water polyline (the height the
        # bank "wants" to be), not the already-carved channel bottom; using
        # the post-carve height happily passed any house planted directly
        # above the incised trough because the trough was lower than the
        # house. See `tests/test_terrain_dsl.py::test_house_above_creek...`.
        # Lazily set on first incision so callers that never carve a
        # channel pay no extra memory.
        self._pre_carve_heights: np.ndarray | None = None

        self.features: list[Feature] = []
        self.scatters: list[ScatterCluster] = []
        self.placements: list[Placement] = []
        self._river_count = 0

    # ----- mesh grid helpers ------------------------------------------------

    def _grid_xy(self) -> tuple[np.ndarray, np.ndarray]:
        xs = self.origin[0] + np.arange(self.W, dtype=np.float32) * self.cell_m
        ys = self.origin[1] + np.arange(self.H, dtype=np.float32) * self.cell_m
        return np.meshgrid(xs, ys)  # XX[H,W], YY[H,W]

    def sample_height(self, x: float, y: float) -> float:
        """Bilinear sample at world (x, y). Clamped outside grid."""
        return self._sample_grid(self.height, x, y)

    def sample_pre_carve_height(self, x: float, y: float) -> float:
        """Bilinear sample of the heightfield as it was **before any
        creek/river incision**. Falls back to the current heightfield if
        no channel has been carved yet (so callers don't need to special-
        case the no-water terrain).

        Use this for stream-bank questions ("how high was the ground
        before we cut the channel?") — the carved trough is by definition
        below grade, so comparing house elevations against the trough
        bottom is meaningless.
        """
        grid = self._pre_carve_heights if self._pre_carve_heights is not None \
            else self.height
        return self._sample_grid(grid, x, y)

    def _sample_grid(self, grid: np.ndarray, x: float, y: float) -> float:
        i = (y - self.origin[1]) / self.cell_m
        j = (x - self.origin[0]) / self.cell_m
        i = float(np.clip(i, 0.0, self.H - 1.001))
        j = float(np.clip(j, 0.0, self.W - 1.001))
        i0, j0 = int(i), int(j)
        di, dj = i - i0, j - j0
        h00 = grid[i0, j0]
        h01 = grid[i0, j0 + 1]
        h10 = grid[i0 + 1, j0]
        h11 = grid[i0 + 1, j0 + 1]
        return float(
            h00 * (1 - di) * (1 - dj)
            + h01 * (1 - di) * dj
            + h10 * di * (1 - dj)
            + h11 * di * dj
        )

    # ----- feature API ------------------------------------------------------

    def hill(self, center: Vec2, radius_m: float, height_m: float,
             falloff: Falloff = 'gaussian') -> Feature:
        """Additive radial hill. Falloff modes:
            ``gaussian``: exp(-(r/radius)^2 * 4) — 86% of peak at r=0.5R
            ``linear``: max(0, 1 - r/radius)
            ``cosine``: 0.5*(1 + cos(pi*r/radius)) on r<radius
        """
        XX, YY = self._grid_xy()
        rr = np.sqrt((XX - center[0]) ** 2 + (YY - center[1]) ** 2)
        with np.errstate(divide='ignore', invalid='ignore'):
            if falloff == 'gaussian':
                k = np.exp(-(rr / max(radius_m, 1e-3)) ** 2 * 4.0)
            elif falloff == 'linear':
                k = np.clip(1.0 - rr / max(radius_m, 1e-3), 0.0, 1.0)
            elif falloff == 'cosine':
                t = np.clip(rr / max(radius_m, 1e-3), 0.0, 1.0)
                k = 0.5 * (1.0 + np.cos(math.pi * t))
                k = np.where(rr > radius_m, 0.0, k)
            else:
                raise ValueError(f"unknown falloff {falloff!r}")
        self.height = (self.height + (k * height_m).astype(np.float32))
        feat = Feature('hill', {
            'center': tuple(center), 'radius_m': float(radius_m),
            'height_m': float(height_m), 'falloff': falloff,
        })
        self.features.append(feat)
        return feat

    def creek(self, polyline: Polyline, width_m: float = 1.5,
              depth_m: float = 0.4, bed_material: str = 'river_cobble',
              flow_dir: Vec2 | None = None) -> Feature:
        """Incise a creek channel along ``polyline``. Subtractive trough
        with cosine cross-section so the banks blend naturally.
        """
        if len(polyline) < 2:
            raise ValueError("creek polyline needs >= 2 points")
        self._incise_channel(polyline, width_m, depth_m)
        feat = Feature('creek', {
            'polyline': tuple((float(x), float(y)) for (x, y) in polyline),
            'width_m': float(width_m), 'depth_m': float(depth_m),
            'bed_material': bed_material,
            'flow_dir': tuple(flow_dir) if flow_dir else None,
            'length_m': _polyline_length(polyline),
        })
        self.features.append(feat)
        return feat

    def river(self, polyline: Polyline, width_m: float = 8.0,
              depth_m: float = 1.2, bed_material: str = 'river_sand') -> Feature:
        """Single-river invariant — second call raises ``RuntimeError``."""
        if self._river_count >= 1:
            raise RuntimeError(
                "Terrain.river() may only be called once "
                "(single-river invariant; use creek() for tributaries)."
            )
        if len(polyline) < 2:
            raise ValueError("river polyline needs >= 2 points")
        self._incise_channel(polyline, width_m, depth_m)
        feat = Feature('river', {
            'polyline': tuple((float(x), float(y)) for (x, y) in polyline),
            'width_m': float(width_m), 'depth_m': float(depth_m),
            'bed_material': bed_material,
            'length_m': _polyline_length(polyline),
        })
        self.features.append(feat)
        self._river_count += 1
        return feat

    def _incise_channel(self, polyline: Polyline,
                        width_m: float, depth_m: float) -> None:
        """Compute distance-to-polyline mask, subtract a half-cosine trough.

        First call also snapshots the pre-carve heightfield to
        ``self._pre_carve_heights`` for use by validate_geo()'s
        houses-under-water check.
        """
        if self._pre_carve_heights is None:
            self._pre_carve_heights = self.height.copy()
        XX, YY = self._grid_xy()
        dist = np.full_like(XX, np.inf, dtype=np.float32)
        for (x0, y0), (x1, y1) in zip(polyline, polyline[1:]):
            dx, dy = x1 - x0, y1 - y0
            seg_len_sq = dx * dx + dy * dy
            if seg_len_sq < 1e-6:
                continue
            t = np.clip(((XX - x0) * dx + (YY - y0) * dy) / seg_len_sq, 0.0, 1.0)
            px, py = x0 + t * dx, y0 + t * dy
            d = np.sqrt((XX - px) ** 2 + (YY - py) ** 2)
            dist = np.minimum(dist, d)
        half_w = max(width_m, 1e-3) * 0.5
        mask = dist < half_w
        # cosine cross-section: 1 at centerline, 0 at bank
        k = np.where(mask, 0.5 * (1.0 + np.cos(math.pi * dist / half_w)), 0.0)
        self.height = (self.height - (k * depth_m).astype(np.float32))

    def tree_scatter(self, polygon: Polygon, species: str,
                     density_per_ha: float, jitter: float = 0.3,
                     seed: int | None = None) -> ScatterCluster:
        if len(polygon) < 3:
            raise ValueError("tree_scatter polygon needs >= 3 vertices")
        cluster = ScatterCluster(
            species=species,
            polygon=tuple((float(x), float(y)) for (x, y) in polygon),
            density_per_ha=float(density_per_ha),
            jitter=float(jitter),
            seed=int(seed) if seed is not None else 0,
        )
        self.scatters.append(cluster)
        return cluster

    def path(self, polyline: Polyline, width_m: float = 1.2,
             material: str = 'flagstone') -> Feature:
        if len(polyline) < 2:
            raise ValueError("path polyline needs >= 2 points")
        feat = Feature('path', {
            'polyline': tuple((float(x), float(y)) for (x, y) in polyline),
            'width_m': float(width_m), 'material': material,
            'length_m': _polyline_length(polyline),
        })
        self.features.append(feat)
        return feat

    def place_house(self, footprint: Iterable[Vec2], xy: Vec2,
                    rotation_deg: float = 0.0,
                    snap: SnapMode = 'pad',
                    pad_size_m: float = 1.0,
                    cut_depth_m: float = 0.6) -> Placement:
        """Snap modes:
        - ``pad``: flatten footprint+collar to mean corner height
        - ``stilts``: leave terrain untouched, base_z = max corner (builder lifts)
        - ``flatten_to_min``: flatten footprint+collar to min corner (was
          the old, misnamed ``'cut'`` — keeps the topology but doesn't
          actually dig into the slope)
        - ``cut``: real cut-and-fill bench — drop ``cut_depth_m`` below the
          min corner so the upslope side has a back-wall and the downslope
          side is filled to the bench level. Use this where a house is set
          into a hillside (the hobbit house, the cliff-edge typology) and
          the upslope earth needs to read as cut rather than as a magic
          floating pad.

        ``cut_depth_m`` is ignored for non-``cut`` modes.
        """
        fp = tuple((float(x), float(y)) for (x, y) in footprint)
        if len(fp) < 3:
            raise ValueError("footprint needs >= 3 corners")
        if snap not in ('pad', 'stilts', 'cut', 'flatten_to_min'):
            raise ValueError(
                f"snap must be pad|stilts|cut|flatten_to_min, got {snap!r}"
            )
        placement = Placement(
            footprint=fp, xy=(float(xy[0]), float(xy[1])),
            rotation_deg=float(rotation_deg),
            snap=snap, pad_size_m=float(pad_size_m),
            cut_depth_m=float(cut_depth_m),
        )
        self._apply_placement(placement)
        self.placements.append(placement)
        return placement

    def _apply_placement(self, p: Placement) -> None:
        world = _rotate_footprint(p.footprint, p.rotation_deg, p.xy)
        corner_heights = [self.sample_height(x, y) for (x, y) in world]
        if p.snap == 'stilts':
            p.base_z = max(corner_heights)  # builder lifts off this
            p.world_corners = tuple((x, y, self.sample_height(x, y)) for (x, y) in world)
            return

        if p.snap == 'pad':
            target_z = float(np.mean(corner_heights))
        elif p.snap == 'flatten_to_min':
            target_z = float(min(corner_heights))
        elif p.snap == 'cut':
            # Real cut-and-fill: bench sits ``cut_depth_m`` below the min
            # corner. The mask flattens the pad to the bench height — for
            # cells whose pre-existing height was above the bench (upslope
            # side) this digs material out; for cells below the bench
            # (downslope side) it fills in. Either way the footprint reads
            # as a deliberate bench cut into the slope.
            target_z = float(min(corner_heights)) - float(p.cut_depth_m)
        else:
            raise AssertionError("unreachable")

        # Expand footprint by pad_size_m collar — distance-from-polygon mask.
        XX, YY = self._grid_xy()
        d2 = self._signed_distance_to_polygon(XX, YY, world)
        mask = d2 <= p.pad_size_m
        if mask.any():
            self.height = np.where(mask, target_z, self.height).astype(np.float32)
        p.base_z = target_z
        p.world_corners = tuple((x, y, target_z) for (x, y) in world)

    @staticmethod
    def _signed_distance_to_polygon(XX, YY, polygon) -> np.ndarray:
        """Distance from each grid point to polygon edge. Negative inside.

        For pad snap we treat the polygon as a region; ``mask = d <= collar``
        catches both interior cells (d < 0) and the collar.
        """
        n = len(polygon)
        dist = np.full_like(XX, np.inf, dtype=np.float32)
        for i in range(n):
            x0, y0 = polygon[i]
            x1, y1 = polygon[(i + 1) % n]
            dx, dy = x1 - x0, y1 - y0
            seg_len_sq = dx * dx + dy * dy
            if seg_len_sq < 1e-6:
                continue
            t = np.clip(((XX - x0) * dx + (YY - y0) * dy) / seg_len_sq, 0.0, 1.0)
            px, py = x0 + t * dx, y0 + t * dy
            d = np.sqrt((XX - px) ** 2 + (YY - py) ** 2)
            dist = np.minimum(dist, d)
        # Sign: negative inside. Use vectorized point-in-polygon.
        inside = np.zeros_like(XX, dtype=bool)
        j = n - 1
        for i in range(n):
            xi, yi = polygon[i]
            xj, yj = polygon[j]
            cond = ((yi > YY) != (yj > YY)) & \
                (XX < (xj - xi) * (YY - yi) / (yj - yi + 1e-12) + xi)
            inside = np.where(cond, ~inside, inside)
            j = i
        return np.where(inside, -dist, dist).astype(np.float32)

    # ----- validation -------------------------------------------------------

    def validate_geo(self) -> list[str]:
        """Return a list of human-readable problems. Empty list == valid.

        Checks:
        - house base_z below the lowest creek/river surface elevation
        - creek crosses river polyline twice (creek joins river twice)
        - creek slope < 0.5% (still water risk per Rule 3)
        - overlapping house footprints (AABB overlap; tight enough heuristic)
        - tree_scatter polygon intersects any house footprint AABB
        """
        issues: list[str] = []

        river_polys = [f for f in self.features if f.kind == 'river']
        creek_polys = [f for f in self.features if f.kind == 'creek']

        # 1) houses under water — compare against PRE-CARVE ground at the
        # water polyline, not the incised channel bottom. The carve sinks
        # the heightfield by ``depth_m`` (0.4 m creek, 1.2 m river); a
        # house on a placement pad that's flush with the original ground
        # but next to the channel was wrongly judged "above water" because
        # ``sample_height`` after incision reports the trough bottom.
        # Pre-carve sampling reflects the bank height, which is what
        # actually drowns the house in a flood.
        if river_polys or creek_polys:
            water_z = []
            for f in river_polys + creek_polys:
                for (x, y) in f.params['polyline']:
                    water_z.append(self.sample_pre_carve_height(x, y))
            min_water_z = min(water_z) if water_z else float('-inf')
            for idx, p in enumerate(self.placements):
                if p.base_z < min_water_z - 0.05:
                    issues.append(
                        f"placement #{idx} base_z={p.base_z:.2f} is "
                        f"{min_water_z - p.base_z:.2f} m below lowest "
                        f"water level — under water"
                    )

        # 2) creek crosses river twice
        for c_idx, creek in enumerate(creek_polys):
            for river in river_polys:
                xings = _count_polyline_intersections(
                    creek.params['polyline'], river.params['polyline']
                )
                if xings >= 2:
                    issues.append(
                        f"creek #{c_idx} crosses river {xings} times — "
                        f"expected at most one confluence"
                    )

        # 3) creek slope check — uses PRE-CARVE heights so the trough
        # depth doesn't fake a gradient. Two failure modes:
        #   (a) absolute gradient < 0.5% → still water, dengue risk
        #       (Rule 3 — the "no standing water anywhere" mandate)
        #   (b) gradient is **uphill** (end higher than start) → physical
        #       impossibility, water doesn't flow up; means the polyline
        #       was authored in the wrong direction or routed across a
        #       ridge. The prior ``abs(z_start - z_end)`` swallowed this
        #       case silently and let the renderer ship reverse-flow
        #       creeks that read fine in a still frame but break the
        #       moment anyone animates flow direction.
        for c_idx, creek in enumerate(creek_polys):
            poly = creek.params['polyline']
            length = creek.params['length_m']
            if length < 1.0:
                continue
            z_start = self.sample_pre_carve_height(*poly[0])
            z_end = self.sample_pre_carve_height(*poly[-1])
            signed_drop = z_start - z_end  # positive = flows downhill
            slope_pct = (signed_drop / length) * 100.0 if length > 0 else 0.0
            if signed_drop < -0.05:
                # end is materially above start — reversed polyline
                issues.append(
                    f"creek #{c_idx} flows uphill: start z={z_start:.2f}, "
                    f"end z={z_end:.2f}, slope {slope_pct:.2f}% — reverse "
                    f"the polyline or check the route (Rule 3 — water "
                    f"doesn't run uphill)"
                )
            elif abs(slope_pct) < 0.5:
                issues.append(
                    f"creek #{c_idx} slope {slope_pct:.2f}% (|gradient| "
                    f"< 0.5%) — dengue-protocol still-water risk (Rule 3)"
                )

        # 4) overlapping house footprints — Separating Axis Theorem on
        # the rotated world-space polygons. The previous AABB heuristic
        # screamed "overlap" for any two rotated rectangles whose bounding
        # boxes intersected, even when the polygons themselves were
        # cleanly disjoint (the common case for off-axis rows of houses).
        house_polys = [
            _rotate_footprint(p.footprint, p.rotation_deg, p.xy)
            for p in self.placements
        ]
        for i in range(len(house_polys)):
            for j in range(i + 1, len(house_polys)):
                if _polygons_intersect_sat(house_polys[i], house_polys[j]):
                    issues.append(
                        f"house footprints #{i} and #{j} overlap (SAT)"
                    )

        # 5) tree_scatter polygon intersects any house footprint. SAT
        # again; scatter polygons are author-supplied so they may be
        # non-convex — for now we assume convex (true for every existing
        # scatter in the repo) and document the limitation.
        for s_idx, scatter in enumerate(self.scatters):
            scatter_poly = tuple(scatter.polygon)
            for h_idx, hp in enumerate(house_polys):
                if _polygons_intersect_sat(scatter_poly, hp):
                    issues.append(
                        f"tree_scatter #{s_idx} ({scatter.species}) "
                        f"overlaps house #{h_idx} footprint (SAT)"
                    )

        return issues

    # ----- scatter resolution ----------------------------------------------

    def _resolve_scatters(self) -> None:
        """Populate ``cluster.points`` from polygon + density_per_ha + jitter.
        Uses a Poisson-ish jittered grid (cheap, deterministic per seed).
        """
        for cluster in self.scatters:
            poly = cluster.polygon
            area_m2 = _polygon_area_m2(poly)
            area_ha = area_m2 / 10_000.0
            n_target = max(0, int(round(cluster.density_per_ha * area_ha)))
            if n_target == 0:
                cluster.points = []
                continue
            xs = [p[0] for p in poly]
            ys = [p[1] for p in poly]
            xmin, xmax = min(xs), max(xs)
            ymin, ymax = min(ys), max(ys)
            # grid spacing so jittered grid yields ~n_target points
            cell = math.sqrt(area_m2 / max(n_target, 1))
            rng = np.random.default_rng(cluster.seed)
            pts: list[Vec3] = []
            y = ymin + cell * 0.5
            while y <= ymax:
                x = xmin + cell * 0.5
                while x <= xmax:
                    jx = float(rng.uniform(-cluster.jitter, cluster.jitter)) * cell
                    jy = float(rng.uniform(-cluster.jitter, cluster.jitter)) * cell
                    px, py = x + jx, y + jy
                    if _point_in_polygon(px, py, poly):
                        pz = self.sample_height(px, py)
                        pts.append((px, py, pz))
                    x += cell
                y += cell
            cluster.points = pts

    # ----- Blender lift -----------------------------------------------------

    def to_blender(self, parent_collection=None, surface_material: str = 'laterite'):
        """Idempotent. Sets active camera ``clip_end >= self.z_clip_end``.

        ``surface_material`` is a key into ``lqv.materials.MAT``. If the key
        is missing the mesh is left unmaterialed (smoke-test mode).

        Returns the created ``bpy.types.Collection`` containing the terrain
        mesh + child markers (river/creek/path curves, scatter empties,
        placement empties). Calls ``validate_geo()`` first; raises if it
        returns non-empty.
        """
        issues = self.validate_geo()
        if issues:
            raise RuntimeError(
                "Terrain.validate_geo() found "
                f"{len(issues)} issue(s): {issues!r}"
            )

        self._resolve_scatters()

        import bpy

        # ----- collection (idempotent) -----
        coll_name = 'Terrain_DSL'
        if coll_name in bpy.data.collections:
            col = bpy.data.collections[coll_name]
            # purge previous contents so re-runs converge
            for obj in list(col.objects):
                bpy.data.objects.remove(obj, do_unlink=True)
        else:
            col = bpy.data.collections.new(coll_name)
            (parent_collection or bpy.context.scene.collection).children.link(col)

        # ----- terrain mesh -----
        mesh = bpy.data.meshes.new('Terrain_DSL_Mesh')
        verts: list[Vec3] = []
        # row-major, matching self.height[H, W] indexing
        for i in range(self.H):
            for j in range(self.W):
                x = self.origin[0] + j * self.cell_m
                y = self.origin[1] + i * self.cell_m
                z = float(self.height[i, j])
                verts.append((x, y, z))
        faces: list[tuple[int, int, int, int]] = []
        for i in range(self.H - 1):
            for j in range(self.W - 1):
                a = i * self.W + j
                b = a + 1
                c = a + self.W + 1
                d = a + self.W
                faces.append((a, b, c, d))
        mesh.from_pydata(verts, [], faces)
        mesh.update(calc_edges=True)
        obj = bpy.data.objects.new('Terrain_DSL_Surface', mesh)
        col.objects.link(obj)

        # ----- assign surface material if available -----
        try:
            from lqv.materials import MAT, assign as _assign
            mat = MAT.get(surface_material)
            if mat is not None:
                _assign(obj, mat)
        except ImportError:
            pass

        # ----- feature markers (lightweight empties) -----
        for k, feat in enumerate(self.features):
            kind = feat.kind
            if kind in ('creek', 'river', 'path'):
                self._make_polyline_curve(col, f"{kind}_{k}", feat.params['polyline'])
            elif kind == 'hill':
                emp = bpy.data.objects.new(f"hill_{k}", None)
                emp.empty_display_type = 'SPHERE'
                emp.empty_display_size = float(feat.params['radius_m'])
                cx, cy = feat.params['center']
                emp.location = (cx, cy, self.sample_height(cx, cy)
                                + feat.params['height_m'])
                col.objects.link(emp)

        # ----- scatter markers -----
        for s_idx, cluster in enumerate(self.scatters):
            for p_idx, (x, y, z) in enumerate(cluster.points):
                emp = bpy.data.objects.new(
                    f"scatter_{cluster.species}_{s_idx}_{p_idx}", None
                )
                emp.empty_display_type = 'PLAIN_AXES'
                emp.empty_display_size = 0.5
                emp.location = (x, y, z)
                col.objects.link(emp)

        # ----- placement markers -----
        for p_idx, p in enumerate(self.placements):
            emp = bpy.data.objects.new(f"placement_{p_idx}", None)
            emp.empty_display_type = 'CUBE'
            emp.empty_display_size = 1.0
            emp.location = (p.xy[0], p.xy[1], p.base_z)
            emp.rotation_euler = (0.0, 0.0, math.radians(p.rotation_deg))
            col.objects.link(emp)

        # ----- camera clip_end -----
        cam = bpy.context.scene.camera
        if cam is not None and cam.type == 'CAMERA':
            if cam.data.clip_end < self.z_clip_end:
                cam.data.clip_end = self.z_clip_end

        return col

    @staticmethod
    def _make_polyline_curve(col, name: str, polyline: Polyline):
        import bpy
        cu = bpy.data.curves.new(name, type='CURVE')
        cu.dimensions = '3D'
        spl = cu.splines.new('POLY')
        spl.points.add(len(polyline) - 1)
        for i, (x, y) in enumerate(polyline):
            spl.points[i].co = (float(x), float(y), 0.0, 1.0)
        obj = bpy.data.objects.new(name, cu)
        col.objects.link(obj)


def _segments_intersect(a, b, c, d) -> bool:
    """Strict-crossing test for line segments AB and CD."""
    def ccw(p, q, r):
        return (r[1] - p[1]) * (q[0] - p[0]) > (q[1] - p[1]) * (r[0] - p[0])
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)


def _count_polyline_intersections(p1: Polyline, p2: Polyline) -> int:
    n = 0
    for i in range(len(p1) - 1):
        for j in range(len(p2) - 1):
            if _segments_intersect(p1[i], p1[i + 1], p2[j], p2[j + 1]):
                n += 1
    return n
