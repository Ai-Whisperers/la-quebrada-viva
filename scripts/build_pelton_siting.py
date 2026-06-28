"""Pelton micro-hydro candidate siting — top-3 sites + overlay contact sheet.

The head map (`docs/site_data/pelton_head_map.json`) tells us 31.2% of the
footprint sits above the 30 m Pelton minimum head. This is a *percentage* claim
— evidence-backed but not actionable. This script promotes it to *three named
candidate sites* the notary or Wesley can point at: lat/lon, available head,
the upslope ridge each penstock would tap, and a hillshade-overlay contact
sheet.

Method:

  1. Reload the head field (same convolution as `build_pelton_head_map.py`).
  2. Greedy top-N: pick the highest-head pixel, then mask a 200 m exclusion
     radius around it, then pick the next highest, etc. — so three sites
     end up in three *different* parts of the parcel rather than three
     adjacent pixels on the same ridge.
  3. For each pick, locate the upslope ridge cell (the argmax inside the
     21×21 px penstock window) and record it.
  4. Render `pelton_siting_contact.png`: COP30 hillshade base-layer + viridis
     head overlay + numbered candidate markers and penstock arrows + caption
     with per-site head/lat/lon/elevation.

Outputs:

  docs/site_data/pelton_siting.json          per-candidate metadata + provenance
  docs/site_data/pelton_siting_contact.png   single-page evidence card

Why this matters: Rule 7 (critical-systems outage-proof) is the energy-budget
backbone of the brief. "31% feasible" is a stats claim; "site #1 at lat/lon X
gives 165 m head with a 270 m penstock to ridge Y" is an engineerable claim.
This is the artifact a project engineer continues from.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import matplotlib
import numpy as np
import rasterio
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import maximum_filter


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEM_TIF = PROJECT_ROOT / "docs/site_data/cop30_dem.tif"
HILLSHADE_PNG = PROJECT_ROOT / "docs/site_data/cop30_hillshade.png"
HEAD_JSON = PROJECT_ROOT / "docs/site_data/pelton_head_map.json"

OUT_JSON = PROJECT_ROOT / "docs/site_data/pelton_siting.json"
OUT_PNG = PROJECT_ROOT / "docs/site_data/pelton_siting_contact.png"

N_CANDIDATES = 3
EXCLUSION_RADIUS_M = 200.0

PANEL = 720
MARGIN = 24
TITLE_H = 56
CAPTION_H = 168
BG = (245, 245, 245)
FG = (20, 20, 20)
DIM = (90, 90, 90)
MARKER_COLOURS = ((255, 80, 80), (255, 200, 0), (120, 220, 120))


def _font(size: int):
    for cand in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if Path(cand).exists():
            return ImageFont.truetype(cand, size=size)
    return ImageFont.load_default()


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def _row_col_to_lonlat(row: int, col: int, bounds, shape) -> tuple[float, float]:
    h, w = shape
    lon = bounds.left + (col + 0.5) * (bounds.right - bounds.left) / w
    lat = bounds.top - (row + 0.5) * (bounds.top - bounds.bottom) / h
    return lon, lat


def _greedy_top_n(head: np.ndarray, n: int, exclusion_px: int) -> list[tuple[int, int]]:
    work = head.copy()
    picks: list[tuple[int, int]] = []
    h, w = work.shape
    for _ in range(n):
        idx = int(np.argmax(work))
        r, c = divmod(idx, w)
        if work[r, c] <= 0:
            break
        picks.append((r, c))
        r0 = max(0, r - exclusion_px)
        r1 = min(h, r + exclusion_px + 1)
        c0 = max(0, c - exclusion_px)
        c1 = min(w, c + exclusion_px + 1)
        work[r0:r1, c0:c1] = -1.0
    return picks


def _find_upslope_argmax(dem: np.ndarray, row: int, col: int, radius_px: int) -> tuple[int, int]:
    h, w = dem.shape
    r0 = max(0, row - radius_px)
    r1 = min(h, row + radius_px + 1)
    c0 = max(0, col - radius_px)
    c1 = min(w, col + radius_px + 1)
    window = dem[r0:r1, c0:c1]
    idx = int(np.argmax(window))
    rr, cc = divmod(idx, window.shape[1])
    return r0 + rr, c0 + cc


def main() -> int:
    head_sidecar = json.loads(HEAD_JSON.read_text())
    window_px = int(head_sidecar["window_px"])
    radius_px = int(head_sidecar["radius_px"])
    px_size_m = float(head_sidecar["px_size_m_approx"])
    exclusion_px = max(1, int(round(EXCLUSION_RADIUS_M / px_size_m)))

    with rasterio.open(DEM_TIF) as src:
        dem = src.read(1).astype(np.float32)
        bounds = src.bounds

    upslope_max = maximum_filter(dem, size=window_px, mode="nearest")
    head = np.clip(upslope_max - dem, 0.0, None)
    head_max = float(head.max())

    picks = _greedy_top_n(head, N_CANDIDATES, exclusion_px)

    penstock_max_m = float(head_sidecar["penstock_radius_m"])
    candidates = []
    for i, (r, c) in enumerate(picks, start=1):
        rr, cc = _find_upslope_argmax(dem, r, c, radius_px)
        lon, lat = _row_col_to_lonlat(r, c, bounds, dem.shape)
        rlon, rlat = _row_col_to_lonlat(rr, cc, bounds, dem.shape)
        dx_m = (cc - c) * px_size_m
        dy_m = (rr - r) * px_size_m
        penstock_horiz_m = float(np.hypot(dx_m, dy_m))
        candidates.append({
            "id": f"P{i}",
            "rank": i,
            "turbine_row": int(r),
            "turbine_col": int(c),
            "turbine_lon": round(lon, 6),
            "turbine_lat": round(lat, 6),
            "turbine_elev_m": round(float(dem[r, c]), 2),
            "ridge_row": int(rr),
            "ridge_col": int(cc),
            "ridge_lon": round(rlon, 6),
            "ridge_lat": round(rlat, 6),
            "ridge_elev_m": round(float(dem[rr, cc]), 2),
            "head_m": round(float(head[r, c]), 2),
            "penstock_horizontal_m": round(penstock_horiz_m, 1),
            "penstock_within_radius": bool(penstock_horiz_m <= penstock_max_m),
            "above_good_head": bool(head[r, c] >= float(head_sidecar["pelton_good_head_m"])),
        })

    sidecar = {
        "method": (
            "Greedy top-N siting: pick argmax(head), mask "
            f"{EXCLUSION_RADIUS_M:.0f} m exclusion ring (~{exclusion_px} px), repeat. "
            f"Upslope ridge = argmax(elevation) within the {window_px}x{window_px} px "
            "penstock search window (Chebyshev distance, square box ~ 2x300 m on each side; "
            "diagonal reach up to ~415 m — see penstock_within_radius flag per candidate). "
            "Head field matches build_pelton_head_map.py for headline-stat consistency."
        ),
        "n_candidates": N_CANDIDATES,
        "exclusion_radius_m": EXCLUSION_RADIUS_M,
        "exclusion_px": exclusion_px,
        "penstock_radius_m": float(head_sidecar["penstock_radius_m"]),
        "px_size_m_approx": px_size_m,
        "head_max_m": round(head_max, 2),
        "head_stats_inherited_from": str(HEAD_JSON.relative_to(PROJECT_ROOT)),
        "source_dem": str(DEM_TIF.relative_to(PROJECT_ROOT)),
        "source_dem_sha256": _sha256(DEM_TIF),
        "candidates": candidates,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(sidecar, indent=2) + "\n")

    hs = Image.open(HILLSHADE_PNG).convert("RGB").resize((PANEL, PANEL), Image.Resampling.LANCZOS)
    head_norm = head / max(head_max, 1.0)
    rgba = (matplotlib.colormaps["viridis"](head_norm) * 255).astype(np.uint8)
    overlay = Image.fromarray(rgba, mode="RGBA").resize((PANEL, PANEL), Image.Resampling.NEAREST)
    alpha = (np.clip(head_norm, 0.0, 1.0) * 180).astype(np.uint8)
    alpha_img = Image.fromarray(alpha, mode="L").resize((PANEL, PANEL), Image.Resampling.NEAREST)
    overlay.putalpha(alpha_img)
    map_panel = Image.alpha_composite(hs.convert("RGBA"), overlay).convert("RGB")

    draw = ImageDraw.Draw(map_panel)
    h_dem, w_dem = dem.shape

    def _to_panel(row: int, col: int) -> tuple[int, int]:
        x = int((col + 0.5) / w_dem * PANEL)
        y = int((row + 0.5) / h_dem * PANEL)
        return x, y

    for cand, colour in zip(candidates, MARKER_COLOURS):
        tx, ty = _to_panel(cand["turbine_row"], cand["turbine_col"])
        rx, ry = _to_panel(cand["ridge_row"], cand["ridge_col"])
        draw.line([(rx, ry), (tx, ty)], fill=colour, width=3)
        r_marker = 14
        draw.ellipse(
            [(tx - r_marker, ty - r_marker), (tx + r_marker, ty + r_marker)],
            outline=(255, 255, 255), width=3,
        )
        draw.ellipse(
            [(tx - r_marker + 3, ty - r_marker + 3), (tx + r_marker - 3, ty + r_marker - 3)],
            fill=colour,
        )
        draw.text((tx, ty), cand["id"], fill=(20, 20, 20), font=_font(13), anchor="mm")
        draw.ellipse([(rx - 6, ry - 6), (rx + 6, ry + 6)], fill=colour, outline=(255, 255, 255), width=2)

    title_text = "La Quebrada Viva — Pelton micro-hydro candidate siting (top 3, COP30 + hillshade)"
    w = MARGIN + PANEL + MARGIN
    h = MARGIN + TITLE_H + PANEL + CAPTION_H + MARGIN
    canvas = Image.new("RGB", (w, h), BG)
    cdraw = ImageDraw.Draw(canvas)
    cdraw.text((MARGIN, MARGIN), title_text, fill=FG, font=_font(20))
    canvas.paste(map_panel, (MARGIN, MARGIN + TITLE_H))

    cap_y = MARGIN + TITLE_H + PANEL + 12
    big = _font(15)
    small = _font(12)
    cdraw.text(
        (MARGIN, cap_y),
        "Markers: large disc = candidate turbine cell; small disc = upslope ridge tap; "
        "line = horizontal penstock projection. Per-candidate distance reported below.",
        fill=DIM, font=small,
    )
    cap_y += 22
    for cand, colour in zip(candidates, MARKER_COLOURS):
        flags = []
        if cand['above_good_head']:
            flags.append("≥80 m good range")
        if not cand['penstock_within_radius']:
            flags.append("penstock > 300 m — verify route")
        flag_str = ("  ·  " + "  ·  ".join(flags)) if flags else ""
        label = (
            f"{cand['id']}  ·  head {cand['head_m']:.1f} m  ·  "
            f"turbine {cand['turbine_lat']:.4f}, {cand['turbine_lon']:.4f} @ {cand['turbine_elev_m']:.0f} m  ·  "
            f"ridge {cand['ridge_lat']:.4f}, {cand['ridge_lon']:.4f} @ {cand['ridge_elev_m']:.0f} m  ·  "
            f"penstock {cand['penstock_horizontal_m']:.0f} m horiz."
            + flag_str
        )
        cdraw.ellipse([(MARGIN, cap_y + 3), (MARGIN + 12, cap_y + 15)], fill=colour, outline=FG)
        cdraw.text((MARGIN + 20, cap_y), label, fill=FG, font=big)
        cap_y += 22

    cdraw.text(
        (MARGIN, cap_y + 4),
        f"Method: {sidecar['method']}",
        fill=DIM, font=small,
    )
    cdraw.text(
        (MARGIN, cap_y + 22),
        f"Source DEM sha256 {sidecar['source_dem_sha256'][:16]}…  ·  exclusion radius "
        f"{EXCLUSION_RADIUS_M:.0f} m ({exclusion_px} px)  ·  derived from "
        f"{HEAD_JSON.name} (window {window_px}×{window_px} px, penstock radius "
        f"{sidecar['penstock_radius_m']:.0f} m).",
        fill=DIM, font=small,
    )

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT_PNG, optimize=True)

    print(
        f"WROTE {OUT_PNG.relative_to(PROJECT_ROOT)}  "
        f"({OUT_PNG.stat().st_size // 1024} KB)\n"
        f"WROTE {OUT_JSON.relative_to(PROJECT_ROOT)}"
    )
    for cand in candidates:
        print(
            f"  {cand['id']}  head={cand['head_m']:6.2f} m  "
            f"turbine=({cand['turbine_lat']:.5f},{cand['turbine_lon']:.5f}) {cand['turbine_elev_m']:.0f} m  "
            f"ridge=({cand['ridge_lat']:.5f},{cand['ridge_lon']:.5f}) {cand['ridge_elev_m']:.0f} m  "
            f"penstock={cand['penstock_horizontal_m']:.0f} m"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
