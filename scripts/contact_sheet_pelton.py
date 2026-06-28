"""Pelton head-map contact sheet — colourised + thresholded for notary review.

The raw `docs/site_data/pelton_head_map.png` is an 8-bit greyscale ramp the
script `build_pelton_head_map.py` writes for downstream consumption. That's
correct for tooling but illegible to a non-technical reviewer (the notary,
Wesley). This script promotes the head map into a single contact sheet:

  - Left panel: COP30 head map rendered with the `viridis` colormap, with
    contour overlays at the Pelton minimum (30 m) and Pelton "good" (80 m)
    thresholds.
  - Right panel: histogram of head values with the two thresholds marked,
    so the percent-of-footprint claims in the caption are visually backed.
  - Caption: head_max / mean / p95 and the two percent-feasible figures.
  - Footer: SHA-256 of the source DEM + method line, so the panel is
    self-verifying.

Output: `docs/site_data/pelton_head_map_contact.png`. Same `dem_ab_contact.png`
DNA — designed to drop straight into the Wesley deliverable bundle alongside it.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import rasterio
from matplotlib import cm
from matplotlib import colors as mcolors
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import maximum_filter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEM_TIF = PROJECT_ROOT / "docs/site_data/cop30_dem.tif"
JSON_IN = PROJECT_ROOT / "docs/site_data/pelton_head_map.json"
OUT_PNG = PROJECT_ROOT / "docs/site_data/pelton_head_map_contact.png"

MAP_PANEL = 512
HIST_PANEL_W = 512
HIST_PANEL_H = 512
GAP = 16
MARGIN = 24
TITLE_H = 56
CAPTION_H = 96
BG = (245, 245, 245)
FG = (20, 20, 20)
DIM = (90, 90, 90)
THRESH_MIN_COLOR = (255, 200, 0)
THRESH_GOOD_COLOR = (255, 80, 80)


def _font(size: int):
    for cand in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if Path(cand).exists():
            return ImageFont.truetype(cand, size=size)
    return ImageFont.load_default()


def _compute_head() -> tuple[np.ndarray, dict]:
    sidecar = json.loads(JSON_IN.read_text())
    window = int(sidecar["window_px"])
    with rasterio.open(DEM_TIF) as src:
        dem = src.read(1).astype(np.float32)
    upslope_max = maximum_filter(dem, size=window, mode="nearest")
    head = np.clip(upslope_max - dem, 0.0, None)
    return head, sidecar


def _render_map_panel(head: np.ndarray, head_max: float, sidecar: dict) -> Image.Image:
    norm = mcolors.Normalize(vmin=0.0, vmax=max(head_max, 1.0))
    rgba = (cm.get_cmap("viridis")(norm(head)) * 255).astype(np.uint8)
    img = Image.fromarray(rgba[..., :3], mode="RGB")
    img = img.resize((MAP_PANEL, MAP_PANEL), Image.Resampling.NEAREST)

    h_norm = head / max(head_max, 1.0)
    h_resized = np.array(
        Image.fromarray((h_norm * 1000).astype(np.uint16), mode="I;16").resize(
            (MAP_PANEL, MAP_PANEL), Image.Resampling.NEAREST
        ),
        dtype=np.float32,
    ) / 1000.0
    min_t = sidecar["pelton_min_head_m"] / max(head_max, 1.0)
    good_t = sidecar["pelton_good_head_m"] / max(head_max, 1.0)
    min_mask = (np.abs(h_resized - min_t) < 0.015).astype(np.uint8) * 255
    good_mask = (np.abs(h_resized - good_t) < 0.015).astype(np.uint8) * 255
    min_rgba = np.zeros((MAP_PANEL, MAP_PANEL, 4), dtype=np.uint8)
    min_rgba[..., 0] = THRESH_MIN_COLOR[0]
    min_rgba[..., 1] = THRESH_MIN_COLOR[1]
    min_rgba[..., 2] = THRESH_MIN_COLOR[2]
    min_rgba[..., 3] = min_mask
    good_rgba = np.zeros((MAP_PANEL, MAP_PANEL, 4), dtype=np.uint8)
    good_rgba[..., 0] = THRESH_GOOD_COLOR[0]
    good_rgba[..., 1] = THRESH_GOOD_COLOR[1]
    good_rgba[..., 2] = THRESH_GOOD_COLOR[2]
    good_rgba[..., 3] = good_mask
    img = Image.alpha_composite(img.convert("RGBA"), Image.fromarray(min_rgba, "RGBA"))
    img = Image.alpha_composite(img, Image.fromarray(good_rgba, "RGBA"))

    fdraw = ImageDraw.Draw(img)
    bar_w, bar_h, pad = 18, 220, 12
    bar_x = MAP_PANEL - bar_w - pad
    bar_y = pad + 18
    for i in range(bar_h):
        v = 1.0 - (i / max(bar_h - 1, 1))
        rgb = tuple(int(c * 255) for c in cm.get_cmap("viridis")(v)[:3])
        fdraw.line([(bar_x, bar_y + i), (bar_x + bar_w, bar_y + i)], fill=rgb)
    fdraw.rectangle(
        [(bar_x - 1, bar_y - 1), (bar_x + bar_w, bar_y + bar_h)],
        outline=(255, 255, 255),
        width=1,
    )
    sf = _font(11)
    fdraw.text((bar_x - 4, bar_y - 16), f"{head_max:.0f} m", fill=(255, 255, 255), font=sf, anchor="ra")
    fdraw.text((bar_x - 4, bar_y + bar_h), "0 m", fill=(255, 255, 255), font=sf, anchor="ra")
    fdraw.text((bar_x - 4, bar_y - 2), "head (m)", fill=(255, 255, 255), font=sf, anchor="ra")

    return img.convert("RGB")


def _render_hist_panel(head: np.ndarray, sidecar: dict) -> Image.Image:
    panel = Image.new("RGB", (HIST_PANEL_W, HIST_PANEL_H), (255, 255, 255))
    draw = ImageDraw.Draw(panel)
    pad_l, pad_r, pad_t, pad_b = 56, 18, 36, 44
    plot_w = HIST_PANEL_W - pad_l - pad_r
    plot_h = HIST_PANEL_H - pad_t - pad_b
    h_max = float(head.max())
    nbins = 60
    bin_edges = np.linspace(0.0, max(h_max, 1.0), nbins + 1)
    counts, _ = np.histogram(head, bins=bin_edges)
    pct = counts / counts.sum() * 100.0
    pct_max = max(pct.max(), 1.0)
    bar_w = plot_w / nbins
    for i in range(nbins):
        bin_mid = 0.5 * (bin_edges[i] + bin_edges[i + 1])
        v = bin_mid / max(h_max, 1.0)
        rgb = tuple(int(c * 255) for c in cm.get_cmap("viridis")(v)[:3])
        h_bar = int(round(pct[i] / pct_max * plot_h))
        x0 = pad_l + i * bar_w
        x1 = x0 + bar_w - 1
        y0 = pad_t + (plot_h - h_bar)
        y1 = pad_t + plot_h
        draw.rectangle([(x0, y0), (x1, y1)], fill=rgb)

    draw.line(
        [(pad_l, pad_t), (pad_l, pad_t + plot_h), (pad_l + plot_w, pad_t + plot_h)],
        fill=FG,
        width=1,
    )

    def x_at(h_m: float) -> int:
        return int(pad_l + (h_m / max(h_max, 1.0)) * plot_w)

    for h_m, colour, label in (
        (sidecar["pelton_min_head_m"], THRESH_MIN_COLOR, f"{int(sidecar['pelton_min_head_m'])} m min"),
        (sidecar["pelton_good_head_m"], THRESH_GOOD_COLOR, f"{int(sidecar['pelton_good_head_m'])} m good"),
    ):
        x = x_at(h_m)
        draw.line([(x, pad_t), (x, pad_t + plot_h)], fill=colour, width=2)
        draw.text((x + 4, pad_t + 4), label, fill=colour, font=_font(12))

    af = _font(11)
    for tick in (0, 30, 60, 90, 120, 150, 180):
        if tick > h_max:
            continue
        x = x_at(tick)
        draw.line([(x, pad_t + plot_h), (x, pad_t + plot_h + 4)], fill=FG)
        draw.text((x, pad_t + plot_h + 6), f"{tick}", fill=FG, font=af, anchor="ma")
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = pad_t + plot_h - int(frac * plot_h)
        draw.line([(pad_l - 4, y), (pad_l, y)], fill=FG)
        draw.text((pad_l - 8, y), f"{frac * pct_max:.1f}%", fill=FG, font=af, anchor="rm")
    draw.text((HIST_PANEL_W // 2, HIST_PANEL_H - 14), "head (m)", fill=FG, font=_font(13), anchor="ma")
    draw.text((14, pad_t + plot_h // 2), "% of footprint", fill=FG, font=_font(13), anchor="mm")
    return panel


def main() -> int:
    head, sidecar = _compute_head()
    head_max = float(head.max())

    map_panel = _render_map_panel(head, head_max, sidecar)
    hist_panel = _render_hist_panel(head, sidecar)

    w = MARGIN + MAP_PANEL + GAP + HIST_PANEL_W + MARGIN
    h = MARGIN + TITLE_H + max(MAP_PANEL, HIST_PANEL_H) + CAPTION_H + MARGIN
    canvas = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(canvas)

    title = "La Quebrada Viva — Pelton micro-hydro head feasibility (COP30, 300 m penstock radius)"
    draw.text((MARGIN, MARGIN), title, fill=FG, font=_font(22))

    panel_y = MARGIN + TITLE_H
    canvas.paste(map_panel, (MARGIN, panel_y))
    canvas.paste(hist_panel, (MARGIN + MAP_PANEL + GAP, panel_y))

    cap_y = panel_y + max(MAP_PANEL, HIST_PANEL_H) + 10
    big = _font(15)
    small = _font(12)
    head_mean = float(head.mean())
    head_p95 = float(np.percentile(head, 95))
    pct_min = float((head >= sidecar["pelton_min_head_m"]).mean() * 100.0)
    pct_good = float((head >= sidecar["pelton_good_head_m"]).mean() * 100.0)

    lines = [
        (
            big,
            FG,
            f"head_max {head_max:.1f} m  ·  mean {head_mean:.1f} m  ·  p95 {head_p95:.1f} m  ·  "
            f"{pct_min:.1f}% of footprint ≥ 30 m (Pelton min)  ·  {pct_good:.1f}% ≥ 80 m (Pelton good)",
        ),
        (
            small,
            DIM,
            "Method: head = max_z_within_300m − own_z, COP30 30 m DEM, scipy.ndimage.maximum_filter 21×21 px window (~588 m a side).",
        ),
        (
            small,
            DIM,
            f"Source DEM sha256 {sidecar['source_dem_sha256'][:16]}…  ·  bounds "
            f"{sidecar['dem_bounds_wgs84']['left']:.4f}, {sidecar['dem_bounds_wgs84']['bottom']:.4f} → "
            f"{sidecar['dem_bounds_wgs84']['right']:.4f}, {sidecar['dem_bounds_wgs84']['top']:.4f}  ·  shape "
            f"{sidecar['dem_shape'][0]}×{sidecar['dem_shape'][1]}",
        ),
        (
            small,
            DIM,
            "Contour overlays: yellow = 30 m (Pelton minimum); red = 80 m (Pelton good range). Justifies Rule 7 (critical systems outage-proof).",
        ),
    ]
    for i, (font, colour, text) in enumerate(lines):
        draw.text((MARGIN, cap_y + i * 19), text, fill=colour, font=font)

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT_PNG, optimize=True)
    print(
        f"WROTE {OUT_PNG.relative_to(PROJECT_ROOT)}  "
        f"({OUT_PNG.stat().st_size // 1024} KB)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
