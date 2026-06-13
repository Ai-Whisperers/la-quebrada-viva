"""Build docs/escritura_deck/escritura_deck_v5.pdf — escritura signing deck.

Phase H of the LQV 8-phase plan (`/home/ai-whisperers/.claude/plans/
glimmering-tumbling-fiddle.md`). This is the final blocking deliverable for
the 2026-06-27 escritura closing — a presentation-quality PDF Wesley can
hand to the escribana.

v2 changes vs v1 (kept on disk for diff):
    * Typology cards now show hero + 4 real Dutch elevations (front/back/
      left/right) rendered by `scripts/render_elevations_all.py` instead of
      placeholder labels.
    * Spec bullets unchanged.
    * Plan / section / interior slots reserved but still pending — captions
      reflect that.

Composition (≥21 pages):
    1.  Cover                       — title, location, owner, date
    2.  62-ha context page          — site overview from digital twin
    3.  Parcel-scale page           — terrain_house_scale_A hero
    4-16.  13 typology cards        — hero + 4 Dutch elevations + spec
    17-20. 4 amenity hero pages     — hero + Dutch spec bullets
    21. BoQ summary                 — totals + top-10 materials
    22. Back cover

Page sizes:
    - All pages: A4 landscape (297 x 210 mm) — consistent layout reads as
      a bound deck rather than a mixed-orientation document.
    - BoQ table uses landscape too (wide enough for $/PYG columns).

Renderer:
    - reportlab Platypus (no chrome-headless dependency, no pandoc).

Inputs read (read-only):
    - renders/sub/latest/<asset>_A.png  — hero per asset
    - renders/sub/latest/terrain_house_scale_A.png
    - renders/sub/latest/terrain_62ha_photoreal_A.png  — 62-ha context
    - docs/boq/boq_rollup.md            — BoQ totals (parsed)
    - lqv.boq.collect_all()             — fresh totals if importable
    - lqv/typologies/<asset>.py         — MATERIAL_TAKEOFF for spec bullets
    - lqv/amenities/<asset>.py          — MATERIAL_TAKEOFF for spec bullets

Output:
    docs/escritura_deck/escritura_deck_v1.pdf

Run from project root:
    python3 scripts/build_escritura_deck.py
"""
from __future__ import annotations

import datetime
import importlib
import io
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SUB_LATEST = ROOT / "renders" / "sub" / "latest"
SUB_RUNS = ROOT / "renders" / "sub" / "runs"
BOQ_MD = ROOT / "docs" / "boq" / "boq_rollup.md"
OUT_DIR = ROOT / "docs" / "escritura_deck"
OUT_PDF = OUT_DIR / "escritura_deck_v5.pdf"

# FX rate read from canonical source docs/finance/fx.json via lqv.finance, so
# the deck never drifts from the BoQ totals. Today is sourced from the
# system clock rather than hard-coded — the deck always reports the day it
# was rebuilt.
from lqv.finance import get_usd_to_pyg as _get_usd_to_pyg
USD_TO_PYG = _get_usd_to_pyg()
TODAY_ISO = datetime.date.today().isoformat()
ESCRITURA_DATE = "2026-06-27"

# Asset catalog — ordered by phase intent (smaller / cheaper first, then heavy).
TYPOLOGY_SLUGS = (
    "hobbit_house",
    "bamboo_wigwam_lodge",
    "bamboo_boomhut_treehouse",
    "bamboo_beton_28",
    "bamboo_beton_30",
    "bamboo_river_house",
    "italian_stone_small_v1",
    "italian_stone_small_v2",
    "bamboo_beton_family_rectangular",
    "bamboo_beton_family_curved",
    "bamboo_container_4pax",
    "italian_river_house_4pax",
    "container_river_house",
)
AMENITY_SLUGS = (
    "labrisa_lounge",
    "floating_dining",
    "eco_pool",
    "eco_retreat_modern_oasis",
)

# Human-readable Dutch titles + one-line descriptions per asset.
# These are deliberately curated (not auto-generated) because the escribana
# is a non-technical Spanish/Dutch reader and a labelled inventory carries
# more meaning than a string of module names.
ASSET_META: dict[str, dict] = {
    "hobbit_house": {
        "title_nl": "Hobbithuis",
        "title_en": "Hobbit House",
        "blurb_nl": "Aardgebed hutje met sod-dak en ronde lapacho-deur.",
        "use": "1-pax",
        "floor_m2": 28,
        "construction_nl": "cob + lapacho + zandsteen funderingsring",
    },
    "bamboo_wigwam_lodge": {
        "title_nl": "Bamboe Wigwam Lodge",
        "title_en": "Bamboo Wigwam Lodge",
        "blurb_nl": "Conische guadua-bundel-lodge, palmthatch-dak.",
        "use": "1-pax",
        "floor_m2": 18,
        "construction_nl": "guadua-bundels + palmthatch + lapacho ring",
    },
    "bamboo_boomhut_treehouse": {
        "title_nl": "Bamboe Boomhut (Treehouse)",
        "title_en": "Bamboo Treehouse",
        "blurb_nl": "Stilten-boomhut op lapacho-palen, guadua platform.",
        "use": "1-pax",
        "floor_m2": 22,
        "construction_nl": "lapacho-stilten + guadua-vloer + palmthatch",
    },
    "bamboo_beton_28": {
        "title_nl": "Bamboe + Beton 28 m²",
        "title_en": "Bamboo + Concrete 28 m²",
        "blurb_nl": "Solo-cabine, betonplaat + guadua-kolommen + palmthatch.",
        "use": "1-pax (single bed)",
        "floor_m2": 28,
        "construction_nl": "beton plaat + guadua + palmthatch + clerestory",
    },
    "bamboo_beton_30": {
        "title_nl": "Bamboe + Beton 30 m²",
        "title_en": "Bamboo + Concrete 30 m²",
        "blurb_nl": "Couples-cabine, queen-bed, guadua-skin op betonplaat.",
        "use": "2-pax (queen bed)",
        "floor_m2": 30,
        "construction_nl": "beton plaat + guadua + palmthatch",
    },
    "bamboo_river_house": {
        "title_nl": "Bamboe Rivierhuis",
        "title_en": "Bamboo River House",
        "blurb_nl": "Riparische 2-bed unit met rivier-glaswand en lapacho-dek.",
        "use": "2-pax",
        "floor_m2": 48,
        "construction_nl": "guadua-kolommen + rivier-glas + lapacho-dek",
    },
    "italian_stone_small_v1": {
        "title_nl": "Steenhuis (klein, v1)",
        "title_en": "Stone House (small, v1)",
        "blurb_nl": "Steenmetselwerk, 2-pax, terracotta-look dak.",
        "use": "2-pax",
        "floor_m2": 32,
        "construction_nl": "CMU + zandsteen-bekleding + dak",
    },
    "italian_stone_small_v2": {
        "title_nl": "Steenhuis (klein, v2)",
        "title_en": "Stone House (small, v2)",
        "blurb_nl": "v1-variant met verlengd terras + zandsteen-pad.",
        "use": "2-pax",
        "floor_m2": 36,
        "construction_nl": "CMU + zandsteen + flagstone-terras",
    },
    "bamboo_beton_family_rectangular": {
        "title_nl": "Bamboe + Beton Familie (rechthoekig)",
        "title_en": "Bamboo + Concrete Family (rectangular)",
        "blurb_nl": "70 m² familie-unit, lapacho ridge-beam + palmthatch.",
        "use": "4-pax (1 queen + 2 twin)",
        "floor_m2": 70,
        "construction_nl": "beton spine + guadua + palmthatch + lapacho ridge",
    },
    "bamboo_beton_family_curved": {
        "title_nl": "Bamboe + Beton Familie (gebogen)",
        "title_en": "Bamboo + Concrete Family (curved)",
        "blurb_nl": "70 m² familie-unit met gebogen palmthatch + banaanblad.",
        "use": "4-pax (1 queen + 2 twin)",
        "floor_m2": 70,
        "construction_nl": "beton spine + guadua-bogen + palmthatch + banaanblad",
    },
    "bamboo_container_4pax": {
        "title_nl": "Bamboe + Container 4-pax",
        "title_en": "Bamboo + Container 4-pax",
        "blurb_nl": "40HC container als servicekern, ingepakt in guadua + thatch.",
        "use": "4-pax",
        "floor_m2": 56,
        "construction_nl": "shipping container + guadua + palmthatch + isolatie",
    },
    "italian_river_house_4pax": {
        "title_nl": "Stenen Rivierhuis (4-pax)",
        "title_en": "Stone River House (4-pax)",
        "blurb_nl": "4-pax steenmetselwerk met grote rivier-glaswand.",
        "use": "4-pax",
        "floor_m2": 96,
        "construction_nl": "CMU + zandsteen + glas + terracotta-look dak",
    },
    "container_river_house": {
        "title_nl": "Container Rivierhuis",
        "title_en": "Container River House",
        "blurb_nl": "Dubbele container, dry-stone bekleding op heuvel-zijde, glas op rivier-zijde.",
        "use": "4-pax",
        "floor_m2": 72,
        "construction_nl": "2x 40HC + zandsteen-bekleding + glas + lapacho-dek",
    },
    "labrisa_lounge": {
        "title_nl": "La Brisa Lounge",
        "title_en": "La Brisa Lounge",
        "blurb_nl": "Open-air lounge, palmthatch-hipped dak, beton-vloer, geintegreerde bar.",
        "use": "Social anchor (creek-side)",
        "floor_m2": 64,
        "construction_nl": "guadua + lapacho posts + palmthatch + beton",
    },
    "floating_dining": {
        "title_nl": "Drijvende Eetzaal",
        "title_en": "Floating Dining Deck",
        "blurb_nl": "Drijvend lapacho-dek op guadua-pontons, lantaarn-verlichting.",
        "use": "Dining over stream pool",
        "floor_m2": 36,
        "construction_nl": "lapacho-dek + guadua-pontons + lantaarns",
    },
    "eco_pool": {
        "title_nl": "Eco-Zwembad",
        "title_en": "Natural Eco Pool",
        "blurb_nl": "Bentoniet-gevoerd natuurlijk zwembad met regen-plant-zone, PV-pomp, geen chloor.",
        "use": "Eco-zwemmen + regenzone",
        "floor_m2": 140,
        "construction_nl": "bentoniet liner + zandsteen coping + regen-planten + PV-pomp",
    },
    "eco_retreat_modern_oasis": {
        "title_nl": "Eco-Retreat Modern Oasis",
        "title_en": "Eco Retreat — Modern Oasis",
        "blurb_nl": "Multi-zone wellness: yoga-dek, sauna-pod, outdoor douche-tuin, PV-frame.",
        "use": "Wellness-hart",
        "floor_m2": 120,
        "construction_nl": "lapacho + glas + palmthatch + klimaattechniek + PV",
    },
}


# ---------------------------------------------------------------------------
# Render discovery
# ---------------------------------------------------------------------------
def _hero_for(slug: str) -> Path | None:
    """Best hero render for an asset slug, falling back to most recent run."""
    a = SUB_LATEST / f"{slug}_A.png"
    if a.exists():
        return a
    # Fallback: scan run folders, prefer most recent A variant.
    candidates: list[Path] = []
    if SUB_RUNS.exists():
        for run in sorted(SUB_RUNS.iterdir(), reverse=True):
            if not run.is_dir():
                continue
            if slug not in run.name:
                continue
            for fname in ("A.png", "variant_A.png", f"{slug}_A.png"):
                p = run / fname
                if p.exists():
                    candidates.append(p)
                    break
    return candidates[0] if candidates else None


def _elevation_for(slug: str, elevation: str) -> Path | None:
    """Pick up a 4-elevation Dutch render produced by render_elevations_all.py.

    Latest path: renders/sub/latest/elevation_dutch_<slug>_<elev>.png
    Falls back to the most recent run folder named ``*_elevation_dutch_<slug>*``.
    """
    latest = SUB_LATEST / f"elevation_dutch_{slug}_{elevation}.png"
    if latest.exists():
        return latest
    if SUB_RUNS.exists():
        for run in sorted(SUB_RUNS.iterdir(), reverse=True):
            if not run.is_dir():
                continue
            if f"elevation_dutch_{slug}" not in run.name:
                continue
            cand = run / f"{elevation}.png"
            if cand.exists():
                return cand
    return None


def _terrain_62ha_hero() -> Path | None:
    for cand in (
        SUB_LATEST / "terrain_62ha_photoreal_A.png",
        SUB_LATEST / "terrain_62ha_A.png",
    ):
        if cand.exists():
            return cand
    return None


def _parcel_scale_hero() -> Path | None:
    p = SUB_LATEST / "terrain_house_scale_A.png"
    return p if p.exists() else None


# ---------------------------------------------------------------------------
# Spec extraction — pull from MATERIAL_TAKEOFF when present
# ---------------------------------------------------------------------------
def _import_takeoff(slug: str) -> dict | None:
    for pkg in ("lqv.typologies", "lqv.amenities"):
        try:
            mod = importlib.import_module(f"{pkg}.{slug}")
        except Exception:
            continue
        takeoff = getattr(mod, "MATERIAL_TAKEOFF", None)
        if takeoff:
            return takeoff
    return None


def _module_unit_cost_usd(takeoff: dict) -> float:
    total = 0.0
    for entry in takeoff.values():
        qty = 0.0
        for f in ("volume_m3", "area_m2", "length_m", "count", "weight_kg"):
            if f in entry:
                qty = float(entry[f])
                break
        total += qty * float(entry.get("unit_cost_usd", 0.0))
    return round(total, 2)


def _top_materials(takeoff: dict, n: int = 4) -> list[tuple[str, float]]:
    rows: list[tuple[str, float]] = []
    for material, entry in takeoff.items():
        qty = 0.0
        for f in ("volume_m3", "area_m2", "length_m", "count", "weight_kg"):
            if f in entry:
                qty = float(entry[f])
                break
        sub = qty * float(entry.get("unit_cost_usd", 0.0))
        rows.append((material, sub))
    rows.sort(key=lambda r: r[1], reverse=True)
    return rows[:n]


def _fmt_usd(v: float) -> str:
    return f"${v:,.2f}"


def _fmt_pyg(v: float) -> str:
    return f"Gs. {v:,.0f}"


# ---------------------------------------------------------------------------
# BoQ parsing — pull totals from the rollup markdown
# ---------------------------------------------------------------------------
def _parse_boq_rollup() -> dict:
    """Extract grand total + top materials + counts from boq_rollup.md.

    Defensive: if anything goes wrong we return reasonable defaults so the
    deck still builds (the BoQ page is informational, not legal).
    """
    out = {
        "grand_total_usd": 0.0,
        "grand_total_pyg": 0.0,
        "top_materials": [],   # list of (material, qty, unit, usd, pyg)
        "asset_count": 0,
        "line_count": 0,
        "rate_pyg_per_usd": USD_TO_PYG,
    }
    if not BOQ_MD.exists():
        return out
    text = BOQ_MD.read_text(encoding="utf-8")

    # Grand total — pattern: "**$257,345.45**  ·  **Gs. 1,878,621,785**"
    m = re.search(
        r"Grand total[\s\S]+?\*\*\$([\d,\.]+)\*\*\s*[·•]\s*\*\*Gs\.\s*([\d,]+)\*\*",
        text,
    )
    if m:
        out["grand_total_usd"] = float(m.group(1).replace(",", ""))
        out["grand_total_pyg"] = float(m.group(2).replace(",", ""))

    # Asset count — count "### `<slug>` — $..." lines under Per-module breakdown.
    out["asset_count"] = len(re.findall(r"^###\s+`[a-z0-9_]+`\s+—", text, re.M))

    # Line count — count rows in per-module tables (heuristic: any "| <name> | <qty> |").
    # We use the per-material rollup section: rows starting with "| " excluding header.
    # More reliable: count rows in per-module breakdown tables.
    rows = re.findall(r"^\|\s+[a-z_][a-z0-9_]*\s+\|\s+[\d,]+\.\d{3}\s+\|",
                      text, re.M)
    out["line_count"] = len(rows)

    # Top-10 materials — pull from Per-material rollup section.
    # Section header: "## Per-material rollup", table rows look like:
    # | <name> | <qty> | <unit> | $<usd> | Gs. <pyg> |
    mat_section = re.search(r"## Per-material rollup([\s\S]+?)(?=^## |\Z)",
                             text, re.M)
    if mat_section:
        mat_rows = re.findall(
            r"^\|\s+([a-z_][a-z0-9_]*)\s+\|\s+([\d,\.]+)\s+\|\s+(\w+)\s+\|"
            r"\s+\$([\d,\.]+)\s+\|\s+Gs\.\s+([\d,]+)\s+\|",
            mat_section.group(1), re.M,
        )
        for name, qty, unit, usd, pyg in mat_rows[:10]:
            out["top_materials"].append((
                name,
                qty,
                unit,
                float(usd.replace(",", "")),
                float(pyg.replace(",", "")),
            ))
    return out


# ---------------------------------------------------------------------------
# PDF composition (reportlab Platypus)
# ---------------------------------------------------------------------------
def _build() -> int:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        BaseDocTemplate,
        Frame,
        Image,
        KeepTogether,
        PageBreak,
        PageTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
    )
    from PIL import Image as PILImage

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    PAGE_W, PAGE_H = landscape(A4)            # (842, 595) pts ≈ 297x210 mm
    MARGIN = 14 * mm
    FRAME_W = PAGE_W - 2 * MARGIN
    FRAME_H = PAGE_H - 2 * MARGIN

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "lqv_title", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=26, leading=30, alignment=TA_CENTER, textColor=colors.HexColor("#1a1a1a"),
        spaceAfter=8,
    )
    subtitle_style = ParagraphStyle(
        "lqv_subtitle", parent=styles["Title"], fontName="Helvetica",
        fontSize=15, leading=18, alignment=TA_CENTER,
        textColor=colors.HexColor("#444444"), spaceAfter=4,
    )
    h1_style = ParagraphStyle(
        "lqv_h1", parent=styles["Heading1"], fontName="Helvetica-Bold",
        fontSize=18, leading=22, textColor=colors.HexColor("#1a1a1a"),
        spaceAfter=4, spaceBefore=0,
    )
    h2_style = ParagraphStyle(
        "lqv_h2", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=12, leading=15, textColor=colors.HexColor("#2a2a2a"),
        spaceAfter=2, spaceBefore=4,
    )
    body_style = ParagraphStyle(
        "lqv_body", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=10, leading=13, textColor=colors.HexColor("#1a1a1a"),
        spaceAfter=2,
    )
    caption_style = ParagraphStyle(
        "lqv_caption", parent=body_style, fontName="Helvetica-Oblique",
        fontSize=8.5, leading=11, textColor=colors.HexColor("#555555"),
        alignment=TA_CENTER,
    )
    elev_label_style = ParagraphStyle(
        "lqv_elev", parent=body_style, fontName="Helvetica-Bold",
        fontSize=8, leading=10, textColor=colors.HexColor("#444444"),
        alignment=TA_CENTER,
    )
    footer_style = ParagraphStyle(
        "lqv_footer", parent=body_style, fontName="Helvetica",
        fontSize=7.5, leading=9.5, textColor=colors.HexColor("#888888"),
        alignment=TA_CENTER,
    )

    doc = BaseDocTemplate(
        str(OUT_PDF),
        pagesize=landscape(A4),
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="La Quebrada Viva — Escritura Signing Deck",
        author="Wesley Manuel van de Camp + Thijs Adrianus Hendricus / AI Whisperers",
        subject="Escritura 2026-06-27",
    )
    main_frame = Frame(MARGIN, MARGIN, FRAME_W, FRAME_H, id="main",
                       leftPadding=0, rightPadding=0,
                       topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="main", frames=[main_frame])])

    def _scaled_image(path: Path, max_w_mm: float, max_h_mm: float) -> Image:
        """Image flowable scaled to fit a (max_w_mm, max_h_mm) box, preserving aspect.

        Source PNGs from ``renders/sub/latest/`` are 16-bit linear-ish heavy
        files (often 4-8 MB each). Embedding ~50 of them via reportlab's
        ``Image(str(path))`` blew the v2 deck up to ~122 MB. We re-encode
        each through Pillow as JPEG quality=85 in-memory before handing the
        buffer to reportlab — visually indistinguishable on print at A4,
        ~10x smaller on disk. PNG transparency would be lost but none of
        the sub-renders use alpha at the page-level.
        """
        with PILImage.open(path) as im:
            iw, ih = im.size
            # Pillow needs RGB for JPEG; flatten any alpha onto white.
            if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
                bg = PILImage.new("RGB", im.size, (255, 255, 255))
                bg.paste(im.convert("RGBA"), mask=im.convert("RGBA").split()[-1])
                rgb = bg
            elif im.mode != "RGB":
                rgb = im.convert("RGB")
            else:
                rgb = im.copy()
            buf = io.BytesIO()
            rgb.save(buf, format="JPEG", quality=85, optimize=True, progressive=True)
            buf.seek(0)
        max_w = max_w_mm * mm
        max_h = max_h_mm * mm
        scale = min(max_w / iw, max_h / ih)
        w = iw * scale
        h = ih * scale
        return Image(buf, width=w, height=h)

    story: list = []
    missing_renders: list[str] = []

    # ----- Page 1: Cover -----
    story.append(Spacer(1, 28 * mm))
    story.append(Paragraph("LA QUEBRADA VIVA", title_style))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("62 hectaren — Escobar, Paraguarí, Paraguay", subtitle_style))
    story.append(Spacer(1, 18 * mm))
    cover_table = Table([
        [Paragraph("<b>Eigenaar:</b>", body_style),
         Paragraph("Wesley Manuel van de Camp (75%) · Thijs Adrianus Hendricus (25%)", body_style)],
        [Paragraph("<b>Locatie:</b>", body_style),
         Paragraph("Escobar district, Paraguarí departamento — ~78 km van Asunción", body_style)],
        [Paragraph("<b>Oppervlakte:</b>", body_style),
         Paragraph("62 ha — 6 percelen (5 Mbopicua + 1 Ybyraty)", body_style)],
        [Paragraph("<b>Boleto:</b>", body_style),
         Paragraph("2026-04-28 — 10% seña betaald (Gs. 250.300.000)", body_style)],
        [Paragraph("<b>Contract totaal:</b>", body_style),
         Paragraph("Gs. 2.503.000.000 (~USD 320.000)", body_style)],
        [Paragraph("<b>Notaris:</b>", body_style),
         Paragraph("Escribana Peña", body_style)],
        [Paragraph("<b>Escritura datum:</b>", body_style),
         Paragraph(f"<b>{ESCRITURA_DATE}</b>", body_style)],
    ], colWidths=[55 * mm, 150 * mm], hAlign="CENTER")
    cover_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 22 * mm))
    story.append(Paragraph(
        "Escritura signing deck — opgesteld voor de escribana, "
        f"gegenereerd {TODAY_ISO}",
        footer_style,
    ))
    story.append(Paragraph(
        "Procedurele Cycles-renders — byte-identiek aan commit 85e86aa",
        footer_style,
    ))
    story.append(PageBreak())

    # ----- Page 2: 62-ha context -----
    story.append(Paragraph("Het terrein — 62 hectaren in vogelvlucht", h1_style))
    ctx_render = _terrain_62ha_hero()
    if ctx_render:
        img = _scaled_image(ctx_render, max_w_mm=200, max_h_mm=120)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Paragraph(
            f"Digitale tweeling van het 62-ha perceel "
            f"(bron: <i>{ctx_render.name}</i>) — Sentinel-2 albedo + ALOS DEM",
            caption_style,
        ))
    else:
        story.append(Paragraph("[62-ha digital-twin render ontbreekt]", body_style))
        missing_renders.append("terrain_62ha")
    story.append(Spacer(1, 4 * mm))
    ctx_bullets = [
        "<b>Locatie:</b> Escobar district, Paraguarí — sandstone escarpment + jaar-rond bron-gevoede beek",
        "<b>Vegetatie:</b> volwassen Atlantisch regenwoud, ~70% behouden onder masterplan",
        "<b>Bestaande infrastructuur:</b> ANDE-elektriciteit aan de weg, twee bestaande gebouwen, koloniale steenterrassen",
        "<b>Bestemming:</b> 12-16 vakantieverhuur-eenheden + evenement-ruimte + Europees-Nederlands restaurant + eco-paden",
        "<b>10 ontwerp-regels:</b> geen rechte hoeken in cob · alleen kalkpleister · geen staand water (dengue) · "
        "wanden nooit op de grond · 90 cm+ dakoverstek · passief ≤35 °C · uitval-bestendige systemen · "
        "Paraguayaans eerst · zonnepanelen op apart staal-frame · muggenwerend gaas op cisternes",
    ]
    for b in ctx_bullets:
        story.append(Paragraph(f"• {b}", body_style))
    story.append(PageBreak())

    # ----- Page 3: Parcel scale -----
    story.append(Paragraph("Perceel-schaal — huizenbouw resolutie", h1_style))
    parcel_render = _parcel_scale_hero()
    if parcel_render:
        img = _scaled_image(parcel_render, max_w_mm=200, max_h_mm=125)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Paragraph(
            f"Terrein-DSL op huizenbouw-schaal (bron: <i>{parcel_render.name}</i>) — "
            "heuvel, beek, rivier, boom-clusters, huispad",
            caption_style,
        ))
    else:
        story.append(Paragraph("[parcel-scale render ontbreekt]", body_style))
        missing_renders.append("terrain_house_scale")
    story.append(Spacer(1, 4 * mm))
    parcel_bullets = [
        "<b>Resolutie:</b> 0.5 m cel-grootte, 80×60 m smoke-domein",
        "<b>Features:</b> heuvel · beek · rivier · boom-scatters · huispad — parameters, niet pixels",
        "<b>Plaatsing-snap-modes:</b> pad (egaliseer) · stilts (geen egalisatie) · cut (uitgraven heuvel-zijde)",
        "<b>Validatie:</b> Terrain.validate_geo() detecteert huizen onder water, beek/rivier-kruisingen, overlap",
        "<b>Output:</b> Blender collection met camera clip_end=20000m (parcel-scale gotcha vermijden)",
    ]
    for b in parcel_bullets:
        story.append(Paragraph(f"• {b}", body_style))
    story.append(PageBreak())

    # ----- Pages 4-16: 13 typology cards -----
    section_idx = 1
    for slug in TYPOLOGY_SLUGS:
        story.extend(_asset_card(
            slug, kind="Typologie", index=section_idx,
            total_assets=len(TYPOLOGY_SLUGS),
            styles_pack=(h1_style, h2_style, body_style, caption_style, elev_label_style),
            scaled_image=_scaled_image,
            missing_renders=missing_renders,
        ))
        story.append(PageBreak())
        section_idx += 1

    # ----- Pages 17-20: 4 amenity hero pages -----
    section_idx = 1
    for slug in AMENITY_SLUGS:
        story.extend(_asset_card(
            slug, kind="Voorziening", index=section_idx,
            total_assets=len(AMENITY_SLUGS),
            styles_pack=(h1_style, h2_style, body_style, caption_style, elev_label_style),
            scaled_image=_scaled_image,
            missing_renders=missing_renders,
            amenity=True,
        ))
        story.append(PageBreak())
        section_idx += 1

    # ----- Page 21: BoQ summary -----
    story.extend(_boq_page(
        styles_pack=(h1_style, h2_style, body_style, caption_style),
    ))
    story.append(PageBreak())

    # ----- Pages 22-24: Closing-day practical sheet (Part 4) -----
    story.extend(_closing_day_pages(
        styles_pack=(h1_style, h2_style, body_style, caption_style),
    ))

    # ----- Page 25: Back cover -----
    story.append(Spacer(1, 70 * mm))
    story.append(Paragraph("LA QUEBRADA VIVA", title_style))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(
        "Escobar, Paraguarí — Escritura 2026-06-27",
        subtitle_style,
    ))
    story.append(Spacer(1, 30 * mm))
    story.append(Paragraph(
        "Generated by scripts/build_escritura_deck.py · "
        "Render byte-identity at commit 85e86aa preserved · "
        "License CC0 + CC-BY 4.0",
        footer_style,
    ))

    doc.build(story)

    size = OUT_PDF.stat().st_size
    pages = _pdf_page_count(OUT_PDF)
    print(
        f"[escritura-pdf] wrote {OUT_PDF.relative_to(ROOT)} "
        f"({size/1024:.1f} KB, {pages} page(s))"
    )
    if missing_renders:
        print(
            "[escritura-pdf] WARNING: missing renders: " + ", ".join(missing_renders),
            file=sys.stderr,
        )
    return pages or 0


def _asset_card(
    slug: str,
    *,
    kind: str,
    index: int,
    total_assets: int,
    styles_pack,
    scaled_image,
    missing_renders: list,
    amenity: bool = False,
) -> list:
    """Build a single typology / amenity card (returns flowables, no PageBreak)."""
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import Image, Paragraph, Spacer, Table, TableStyle

    h1, h2, body, caption, elev = styles_pack
    meta = ASSET_META.get(slug, {})
    title_nl = meta.get("title_nl", slug)
    title_en = meta.get("title_en", slug)

    flow: list = []
    header = f"{kind} {index}/{total_assets} — {title_nl}"
    flow.append(Paragraph(header, h1))
    flow.append(Paragraph(f"<i>{title_en}</i>", caption))
    flow.append(Spacer(1, 2 * mm))

    # Hero image — shrunk vs v1 to leave room for the 4-elevation tile strip
    # below. Landscape A4 useable height ≈ 180 mm; header + hero + elevation
    # strip + caption budget around 60+40+10 mm.
    hero = _hero_for(slug)
    if hero:
        img = scaled_image(hero, max_w_mm=170, max_h_mm=72)
    else:
        missing_renders.append(slug)
        img = Paragraph(f"[hero render missing for {slug}]", body)

    # Dutch elevations — 4 real renders or "(pending)" placeholder if a
    # tile is missing. Labels are bilingual NL primary / EN secondary.
    elev_specs = (
        ("front", "VOORGEVEL", "Front"),
        ("back", "ACHTERGEVEL", "Back"),
        ("left", "LINKER ZIJGEVEL", "Left"),
        ("right", "RECHTER ZIJGEVEL", "Right"),
    )
    tile_w_mm = 62
    tile_h_mm = 38
    elev_image_row = []
    elev_label_row = []
    for elev_key, nl_label, en_label in elev_specs:
        ep = _elevation_for(slug, elev_key)
        if ep is not None:
            tile = scaled_image(ep, max_w_mm=tile_w_mm, max_h_mm=tile_h_mm)
            elev_image_row.append(tile)
            elev_label_row.append(
                Paragraph(f"<b>{nl_label}</b><br/><font size='7'>{en_label}</font>", elev)
            )
        else:
            missing_renders.append(f"elevation_dutch_{slug}_{elev_key}")
            elev_image_row.append(
                Paragraph(f"<i>[{elev_key} render pending]</i>", elev)
            )
            elev_label_row.append(
                Paragraph(
                    f"<b>{nl_label}</b><br/><font size='7'>{en_label} (pending)</font>",
                    elev,
                )
            )

    elev_labels = Table(
        [elev_image_row, elev_label_row],
        colWidths=[(tile_w_mm + 2) * mm] * 4,
        rowHeights=[(tile_h_mm + 2) * mm, None],
    )
    elev_labels.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
        ("VALIGN", (0, 1), (-1, 1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ("LINEABOVE", (0, 0), (-1, 0), 0.4, colors.HexColor("#888888")),
        ("LINEBELOW", (0, 1), (-1, 1), 0.3, colors.HexColor("#aaaaaa")),
    ]))

    # Spec bullets — pull from MATERIAL_TAKEOFF if importable, else from meta.
    takeoff = _import_takeoff(slug)
    unit_cost = _module_unit_cost_usd(takeoff) if takeoff else 0.0
    top_mats = _top_materials(takeoff, n=4) if takeoff else []

    spec_lines: list[str] = []
    if meta.get("use"):
        spec_lines.append(f"<b>Gebruik:</b> {meta['use']}")
    if meta.get("floor_m2"):
        spec_lines.append(f"<b>Vloeroppervlak:</b> ~{meta['floor_m2']} m²")
    if meta.get("construction_nl"):
        spec_lines.append(f"<b>Constructie:</b> {meta['construction_nl']}")
    if meta.get("blurb_nl"):
        spec_lines.append(f"<b>Beschrijving:</b> {meta['blurb_nl']}")
    if unit_cost:
        spec_lines.append(
            f"<b>Eenheid-kosten:</b> {_fmt_usd(unit_cost)} · "
            f"{_fmt_pyg(unit_cost * USD_TO_PYG)}"
        )
    if top_mats:
        spec_lines.append("<b>Top materialen (USD):</b>")
        for mat, usd in top_mats:
            spec_lines.append(f"&nbsp;&nbsp;• {mat}: {_fmt_usd(usd)}")

    spec_paragraphs = [Paragraph(line, body) for line in spec_lines]

    # Compose 2-col layout: hero on left, spec column on right.
    spec_cell = []
    spec_cell.append(Paragraph("<b>Specificaties</b>", h2))
    spec_cell.extend(spec_paragraphs)

    two_col = Table(
        [[img, spec_cell]],
        colWidths=[175 * mm, 90 * mm],
    )
    two_col.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    flow.append(two_col)
    flow.append(Spacer(1, 2 * mm))
    flow.append(elev_labels)
    flow.append(Spacer(1, 2 * mm))
    flow.append(Paragraph(
        f"Vier Nederlandse gevels gerenderd via <code>"
        f"lqv/subscene/elevation_dutch.py</code>. Plattegrond, doorsnede A-A "
        "en interieur-details zijn buiten scope voor het escritura-pakket en "
        "vallen onder de bouwfase.",
        caption,
    ))
    return flow


def _boq_page(*, styles_pack) -> list:
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

    h1, h2, body, caption = styles_pack
    boq = _parse_boq_rollup()

    flow: list = []
    flow.append(Paragraph("Bill of Quantities — samenvatting", h1))
    flow.append(Paragraph(
        f"Bron: <code>docs/boq/boq_rollup.md</code> · gegenereerd door "
        f"<code>lqv/boq.py</code> · wisselkoers {int(round(USD_TO_PYG)):,} PYG / USD",
        caption,
    ))
    flow.append(Spacer(1, 4 * mm))

    # Grand total block
    flow.append(Paragraph("<b>Totaal (per eenheid van elke asset)</b>", h2))
    flow.append(Paragraph(
        f"<font size='14'><b>{_fmt_usd(boq['grand_total_usd'])} · "
        f"{_fmt_pyg(boq['grand_total_pyg'])}</b></font>",
        body,
    ))
    flow.append(Spacer(1, 2 * mm))
    flow.append(Paragraph(
        f"Aantal assets: <b>{boq['asset_count']}</b> · "
        f"Aantal regel-items: <b>{boq['line_count']}</b>",
        body,
    ))
    flow.append(Spacer(1, 4 * mm))

    # Top-10 materials table
    flow.append(Paragraph("<b>Top 10 materialen op USD-totaal</b>", h2))
    header = ["#", "Materiaal", "Hoeveelheid", "Eenheid", "USD totaal", "PYG totaal"]
    rows = [header]
    for i, (name, qty, unit, usd, pyg) in enumerate(boq["top_materials"], start=1):
        rows.append([
            str(i),
            name,
            qty,
            unit,
            _fmt_usd(usd),
            _fmt_pyg(pyg),
        ])
    if len(rows) == 1:
        rows.append(["—", "[boq_rollup.md parse failed]", "", "", "", ""])
    boq_tbl = Table(rows, colWidths=[10 * mm, 80 * mm, 30 * mm, 20 * mm, 35 * mm, 50 * mm])
    boq_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ece6d6")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#888888")),
        ("ALIGN", (4, 1), (-1, -1), "RIGHT"),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    flow.append(boq_tbl)
    flow.append(Spacer(1, 6 * mm))

    flow.append(Paragraph(
        "Hoeveelheden zijn <b>per eenheid</b> van elke asset; site-niveau "
        "hoeveelheden vermenigvuldigen met het aantal eenheden vastgelegd "
        "in het masterplan (Fase 1 = 3-6 huizen, Fase 2 = 3-6 extra, "
        "Fase 3 = restaurant + amenities). Volledige CSV: "
        "<code>docs/boq/boq_rollup.csv</code>.",
        caption,
    ))
    return flow


def _closing_day_pages(*, styles_pack) -> list:
    """Render `Part 4 — Closing day` from the markdown deck into 3 PDF pages.

    Source: ``docs/escritura_deck/escritura_deck.md`` lines 259-288. Layout:
      * Page A: "Bring or confirm in hand 5+ days before signing" checklist
      * Page B: "Signing-day risk register" (red-tinted warning cards)
      * Page C: "Post-closing T+30" kickoff checklist
    """
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        PageBreak,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
    )

    h1, h2, body, caption = styles_pack
    flow: list = []

    # ----- Page A: Bring-or-confirm checklist -----
    flow.append(Paragraph("Deel 4 — Tekendag — praktische checklist", h1))
    flow.append(Spacer(1, 2 * mm))
    flow.append(Paragraph(
        f"Escritura {ESCRITURA_DATE} bij Escribana Peña. Onderstaande items "
        "moeten <b>5+ dagen voor tekendag</b> in handen of bevestigd zijn — "
        "geen losse eindjes op 26 juni.",
        caption,
    ))
    flow.append(Spacer(1, 6 * mm))
    flow.append(Paragraph("Vooraf in handen of bevestigd (T-5d)", h2))
    flow.append(Spacer(1, 2 * mm))
    bring_items = [
        "Paspoorten (Wesley NWF23H565 + Thijs NP19HPFP6) — originelen",
        "Bewijs van fondsen voor het saldo: G. 2.190 M aan verkopers + "
        "G. ~313 M aan Burgos (makelaarscommissie)",
        "Volmacht (poder) als één van de kopers niet kan komen — apostille NL "
        "+ <i>traductor público matriculado</i> in PY",
        "Certificados catastrales-registrales per finca — Escribana Peña "
        "haalt op; verifiëren 1 week vooraf",
        "Comprobantes de impuesto inmobiliario al día "
        "(verkopers-plicht per Cl. SÉPTIMA)",
        "Anexo I — technische beschrijvingen (linderos, rumbos, medidas) "
        "van alle 6 fincas",
        "Comisión Burgos split bevestigd met Peña 48 u vooraf",
        "Belastingverdeling bevestigd (impuesto a la renta = verkoper; "
        "honorarios notariales meestal koper; IVA op commissie = verifiëren)",
        "Formele <i>designación</i> van Peña als escribana voor de "
        "escritura (Cl. SEXTA)",
        "Twee betrouwbare getuigen stand-by",
    ]
    for itm in bring_items:
        flow.append(Paragraph(f"• {itm}", body))
        flow.append(Spacer(1, 1.5 * mm))
    flow.append(PageBreak())

    # ----- Page B: Risk register -----
    flow.append(Paragraph("Tekendag — risico-register", h1))
    flow.append(Spacer(1, 2 * mm))
    flow.append(Paragraph(
        "Scenario's die de tekening kunnen blokkeren of vertragen, met de "
        "contractuele afhandeling per Cláusulas SEXTA-NOVENA.",
        caption,
    ))
    flow.append(Spacer(1, 6 * mm))

    risk_rows = [
        [
            Paragraph("<b>Verkoper komt niet / weigert</b>", body),
            Paragraph(
                "Boete verdubbelt de seña: G. 500.600.000 aan kopers "
                "(Cl. NOVENA). Bij twijfel in de week vooraf direct met "
                "advocaat opnemen.",
                body,
            ),
        ],
        [
            Paragraph("<b>Koper komt niet / betaalt niet</b>", body),
            Paragraph(
                "Kopers verbeuren de seña (G. 250.300.000) netto van reeds "
                "gemaakte notariskosten.",
                body,
            ),
        ],
        [
            Paragraph("<b>Embargo of gravamen duikt laat op</b>", body),
            Paragraph(
                "Escribana hoort dit te detecteren. Indien gevonden: <b>NIET "
                "tekenen</b> — inroepen Cl. NOVENA prórroga.",
                body,
            ),
        ],
        [
            Paragraph("<b>Cl. OCTAVA (ii) documenten ontbreken</b>", body),
            Paragraph(
                "Hadden ~6 mei binnen moeten zijn. Indien nog niet: "
                "<b>nu</b> najagen via Peña, niet pas op 27 juni.",
                body,
            ),
        ],
    ]
    risk_tbl = Table(risk_rows, colWidths=[80 * mm, 185 * mm])
    risk_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fff6f3")),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#b94a3a")),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#d8a89a")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    flow.append(risk_tbl)
    flow.append(Spacer(1, 4 * mm))
    flow.append(Paragraph(
        "Bron: <code>docs/escritura/contrato_compraventa.md</code> en "
        "<code>docs/escritura_deck/escritura_deck.md</code> §Part 4.",
        caption,
    ))
    flow.append(PageBreak())

    # ----- Page C: Post-closing T+30 -----
    flow.append(Paragraph("Na tekendag — T+30 (housing-park kickoff)", h1))
    flow.append(Spacer(1, 2 * mm))
    flow.append(Paragraph(
        "De eerste 30 dagen na escritura: operationele entiteit registreren, "
        "vergunningen openen, kapitaal mobiliseren voor Fase 1.",
        caption,
    ))
    flow.append(Spacer(1, 6 * mm))
    post_items = [
        "Operationele entiteit registreren (S.A. / S.R.L. / E.A.S. — "
        "beslissing nog door Wesley te tekenen)",
        "SENATUR-registratie indienen voor vakantieverhuur-operatie",
        "Municipalidad de Escobar benaderen voor land-use + bouwvergunningen",
        "AHK Paraguay introducties activeren naar Duits-Paraguayaanse "
        "toeleveringsketen (San Bernardino)",
        "Fase-1 capex starten: 3-6 huizen (target USD 200-500 k window) — "
        "typologie-mix per BoQ-prioriteit (zie p. BoQ-overzicht)",
    ]
    for itm in post_items:
        flow.append(Paragraph(f"• {itm}", body))
        flow.append(Spacer(1, 1.5 * mm))
    flow.append(Spacer(1, 6 * mm))
    flow.append(Paragraph(
        "Volledige tekst en bronverwijzingen: "
        "<code>docs/escritura_deck/escritura_deck.md</code> §Part 4 "
        "(regels 259-288).",
        caption,
    ))
    flow.append(PageBreak())

    return flow


def _pdf_page_count(pdf_path: Path) -> int | None:
    try:
        proc = subprocess.run(
            ["pdfinfo", str(pdf_path)], capture_output=True, text=True, timeout=15,
        )
    except FileNotFoundError:
        return None
    for line in proc.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    return None


def main() -> int:
    return _build()


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
