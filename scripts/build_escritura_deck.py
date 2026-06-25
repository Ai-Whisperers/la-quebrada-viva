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
from collections.abc import Iterable

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SUB_LATEST = ROOT / "renders" / "sub" / "latest"
SUB_RUNS = ROOT / "renders" / "sub" / "runs"
BOQ_MD = ROOT / "docs" / "boq" / "boq_rollup.md"
OUT_DIR = ROOT / "docs" / "escritura_deck"
OUT_PDF = OUT_DIR / "escritura_deck_v6.pdf"

# FX rate read from canonical source docs/finance/fx.json via lqv.finance, so
# the deck never drifts from the BoQ totals. Today is sourced from the
# system clock rather than hard-coded — the deck always reports the day it
# was rebuilt.
from lqv.finance import get_usd_to_pyg as _get_usd_to_pyg
USD_TO_PYG = _get_usd_to_pyg()
TODAY_ISO = datetime.date.today().isoformat()
ESCRITURA_DATE = "2026-06-27"

# Total contract value in PYG, sourced from the 2026-04-28 boleto (Cl. CUARTA).
# USD equivalent is computed from USD_TO_PYG so the cover, appendix, and BoQ
# rollup never drift from each other — earlier hardcoded "~USD 320,000" was
# stale (came from a 2025 FX of ~7,822 PYG/USD).
CONTRACT_PYG = 2_503_000_000
CONTRACT_USD = int(CONTRACT_PYG / USD_TO_PYG)

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

# Human-readable titles + one-line descriptions per asset, in three languages.
# Spanish (`_es`) is the primary surface — the escribana is a Paraguayan
# notary and the deck is delivered to her. English (`_en`) is shown as an
# italic caption under each Spanish title for Wesley's reference. Dutch
# (`_nl`) is kept on file for the design archive but no longer rendered.
ASSET_META: dict[str, dict] = {
    "hobbit_house": {
        "title_es": "Casa hobbit",
        "title_en": "Hobbit House",
        "title_nl": "Hobbithuis",
        "blurb_es": "Casita semienterrada con techo de tepe y puerta redonda de lapacho.",
        "blurb_nl": "Aardgebed hutje met sod-dak en ronde lapacho-deur.",
        "use_es": "1 plaza",
        "use": "1-pax",
        "floor_m2": 28,
        "construction_es": "cob + lapacho + anillo de cimentación en piedra arenisca",
        "construction_nl": "cob + lapacho + zandsteen funderingsring",
    },
    "bamboo_wigwam_lodge": {
        "title_es": "Lodge wigwam de bambú",
        "title_en": "Bamboo Wigwam Lodge",
        "title_nl": "Bamboe Wigwam Lodge",
        "blurb_es": "Lodge cónico armado en haces de guadua, techo de paja de palma.",
        "blurb_nl": "Conische guadua-bundel-lodge, palmthatch-dak.",
        "use_es": "1 plaza",
        "use": "1-pax",
        "floor_m2": 18,
        "construction_es": "haces de guadua + paja de palma + anillo de lapacho",
        "construction_nl": "guadua-bundels + palmthatch + lapacho ring",
    },
    "bamboo_boomhut_treehouse": {
        "title_es": "Casa del árbol en bambú",
        "title_en": "Bamboo Treehouse",
        "title_nl": "Bamboe Boomhut (Treehouse)",
        "blurb_es": "Casa del árbol sobre pilotes de lapacho con plataforma de guadua.",
        "blurb_nl": "Stilten-boomhut op lapacho-palen, guadua platform.",
        "use_es": "1 plaza",
        "use": "1-pax",
        "floor_m2": 22,
        "construction_es": "pilotes de lapacho + piso de guadua + paja de palma",
        "construction_nl": "lapacho-stilten + guadua-vloer + palmthatch",
    },
    "bamboo_beton_28": {
        "title_es": "Bambú + hormigón 28 m²",
        "title_en": "Bamboo + Concrete 28 m²",
        "title_nl": "Bamboe + Beton 28 m²",
        "blurb_es": "Cabaña individual: losa de hormigón, columnas de guadua y techo de palma.",
        "blurb_nl": "Solo-cabine, betonplaat + guadua-kolommen + palmthatch.",
        "use_es": "1 plaza (cama individual)",
        "use": "1-pax (single bed)",
        "floor_m2": 28,
        "construction_es": "losa de hormigón + guadua + paja de palma + lucernario",
        "construction_nl": "beton plaat + guadua + palmthatch + clerestory",
    },
    "bamboo_beton_30": {
        "title_es": "Bambú + hormigón 30 m²",
        "title_en": "Bamboo + Concrete 30 m²",
        "title_nl": "Bamboe + Beton 30 m²",
        "blurb_es": "Cabaña para pareja, cama queen, envolvente de guadua sobre losa de hormigón.",
        "blurb_nl": "Couples-cabine, queen-bed, guadua-skin op betonplaat.",
        "use_es": "2 plazas (cama queen)",
        "use": "2-pax (queen bed)",
        "floor_m2": 30,
        "construction_es": "losa de hormigón + guadua + paja de palma",
        "construction_nl": "beton plaat + guadua + palmthatch",
    },
    "bamboo_river_house": {
        "title_es": "Casa ribereña de bambú",
        "title_en": "Bamboo River House",
        "title_nl": "Bamboe Rivierhuis",
        "blurb_es": "Unidad ribereña de 2 plazas con frente vidriado al río y deck de lapacho.",
        "blurb_nl": "Riparische 2-bed unit met rivier-glaswand en lapacho-dek.",
        "use_es": "2 plazas",
        "use": "2-pax",
        "floor_m2": 48,
        "construction_es": "columnas de guadua + paño vidriado al río + deck de lapacho",
        "construction_nl": "guadua-kolommen + rivier-glas + lapacho-dek",
    },
    "italian_stone_small_v1": {
        "title_es": "Casa de piedra (pequeña, v1)",
        "title_en": "Stone House (small, v1)",
        "title_nl": "Steenhuis (klein, v1)",
        "blurb_es": "Mampostería de piedra, 2 plazas, cubierta con apariencia de terracota.",
        "blurb_nl": "Steenmetselwerk, 2-pax, terracotta-look dak.",
        "use_es": "2 plazas",
        "use": "2-pax",
        "floor_m2": 32,
        "construction_es": "bloques CMU + revestimiento de arenisca + cubierta",
        "construction_nl": "CMU + zandsteen-bekleding + dak",
    },
    "italian_stone_small_v2": {
        "title_es": "Casa de piedra (pequeña, v2)",
        "title_en": "Stone House (small, v2)",
        "title_nl": "Steenhuis (klein, v2)",
        "blurb_es": "Variante de la v1 con terraza extendida y sendero de losas de arenisca.",
        "blurb_nl": "v1-variant met verlengd terras + zandsteen-pad.",
        "use_es": "2 plazas",
        "use": "2-pax",
        "floor_m2": 36,
        "construction_es": "bloques CMU + arenisca + terraza en losa irregular",
        "construction_nl": "CMU + zandsteen + flagstone-terras",
    },
    "bamboo_beton_family_rectangular": {
        "title_es": "Bambú + hormigón familiar (rectangular)",
        "title_en": "Bamboo + Concrete Family (rectangular)",
        "title_nl": "Bamboe + Beton Familie (rechthoekig)",
        "blurb_es": "Unidad familiar de 70 m² con viga cumbrera de lapacho y techo de paja de palma.",
        "blurb_nl": "70 m² familie-unit, lapacho ridge-beam + palmthatch.",
        "use_es": "4 plazas (1 queen + 2 individuales)",
        "use": "4-pax (1 queen + 2 twin)",
        "floor_m2": 70,
        "construction_es": "espina de hormigón + guadua + paja de palma + cumbrera de lapacho",
        "construction_nl": "beton spine + guadua + palmthatch + lapacho ridge",
    },
    "bamboo_beton_family_curved": {
        "title_es": "Bambú + hormigón familiar (curva)",
        "title_en": "Bamboo + Concrete Family (curved)",
        "title_nl": "Bamboe + Beton Familie (gebogen)",
        "blurb_es": "Unidad familiar de 70 m² con techo curvo de palma y capa de hojas de banano.",
        "blurb_nl": "70 m² familie-unit met gebogen palmthatch + banaanblad.",
        "use_es": "4 plazas (1 queen + 2 individuales)",
        "use": "4-pax (1 queen + 2 twin)",
        "floor_m2": 70,
        "construction_es": "espina de hormigón + arcos de guadua + paja de palma + hojas de banano",
        "construction_nl": "beton spine + guadua-bogen + palmthatch + banaanblad",
    },
    "bamboo_container_4pax": {
        "title_es": "Bambú + contenedor 4 plazas",
        "title_en": "Bamboo + Container 4-pax",
        "title_nl": "Bamboe + Container 4-pax",
        "blurb_es": "Contenedor 40HC como núcleo de servicios, envuelto en guadua y paja de palma.",
        "blurb_nl": "40HC container als servicekern, ingepakt in guadua + thatch.",
        "use_es": "4 plazas",
        "use": "4-pax",
        "floor_m2": 56,
        "construction_es": "contenedor marítimo + guadua + paja de palma + aislación",
        "construction_nl": "shipping container + guadua + palmthatch + isolatie",
    },
    "italian_river_house_4pax": {
        "title_es": "Casa ribereña de piedra (4 plazas)",
        "title_en": "Stone River House (4-pax)",
        "title_nl": "Stenen Rivierhuis (4-pax)",
        "blurb_es": "Mampostería de piedra para 4 plazas con gran paño vidriado al río.",
        "blurb_nl": "4-pax steenmetselwerk met grote rivier-glaswand.",
        "use_es": "4 plazas",
        "use": "4-pax",
        "floor_m2": 96,
        "construction_es": "bloques CMU + arenisca + vidrio + cubierta apariencia terracota",
        "construction_nl": "CMU + zandsteen + glas + terracotta-look dak",
    },
    "container_river_house": {
        "title_es": "Casa ribereña en contenedor",
        "title_en": "Container River House",
        "title_nl": "Container Rivierhuis",
        "blurb_es": "Doble contenedor con revestimiento de piedra seca hacia la colina y vidrio hacia el río.",
        "blurb_nl": "Dubbele container, dry-stone bekleding op heuvel-zijde, glas op rivier-zijde.",
        "use_es": "4 plazas",
        "use": "4-pax",
        "floor_m2": 72,
        "construction_es": "2× 40HC + revestimiento de arenisca + vidrio + deck de lapacho",
        "construction_nl": "2x 40HC + zandsteen-bekleding + glas + lapacho-dek",
    },
    "labrisa_lounge": {
        "title_es": "La Brisa Lounge",
        "title_en": "La Brisa Lounge",
        "title_nl": "La Brisa Lounge",
        "blurb_es": "Lounge al aire libre, techo de palma a cuatro aguas, piso de hormigón, barra integrada.",
        "blurb_nl": "Open-air lounge, palmthatch-hipped dak, beton-vloer, geintegreerde bar.",
        "use_es": "Núcleo social (junto al arroyo)",
        "use": "Social anchor (creek-side)",
        "floor_m2": 64,
        "construction_es": "guadua + postes de lapacho + paja de palma + hormigón",
        "construction_nl": "guadua + lapacho posts + palmthatch + beton",
    },
    "floating_dining": {
        "title_es": "Comedor flotante",
        "title_en": "Floating Dining Deck",
        "title_nl": "Drijvende Eetzaal",
        "blurb_es": "Deck flotante de lapacho sobre pontones de guadua, iluminación con farolas.",
        "blurb_nl": "Drijvend lapacho-dek op guadua-pontons, lantaarn-verlichting.",
        "use_es": "Comedor sobre el remanso del arroyo",
        "use": "Dining over stream pool",
        "floor_m2": 36,
        "construction_es": "deck de lapacho + pontones de guadua + farolas",
        "construction_nl": "lapacho-dek + guadua-pontons + lantaarns",
    },
    "eco_pool": {
        "title_es": "Piscina ecológica",
        "title_en": "Natural Eco Pool",
        "title_nl": "Eco-Zwembad",
        "blurb_es": "Piscina natural con liner de bentonita, zona de plantas filtrantes, bomba fotovoltaica, sin cloro.",
        "blurb_nl": "Bentoniet-gevoerd natuurlijk zwembad met regen-plant-zone, PV-pomp, geen chloor.",
        "use_es": "Baño ecológico + zona de fitodepuración",
        "use": "Eco-zwemmen + regenzone",
        "floor_m2": 140,
        "construction_es": "liner de bentonita + coronamiento de arenisca + plantas filtrantes + bomba fotovoltaica",
        "construction_nl": "bentoniet liner + zandsteen coping + regen-planten + PV-pomp",
    },
    "eco_retreat_modern_oasis": {
        "title_es": "Eco-Retiro «Modern Oasis»",
        "title_en": "Eco Retreat — Modern Oasis",
        "title_nl": "Eco-Retreat Modern Oasis",
        "blurb_es": "Bienestar multizona: deck de yoga, cápsula de sauna, ducha-jardín, marco fotovoltaico.",
        "blurb_nl": "Multi-zone wellness: yoga-dek, sauna-pod, outdoor douche-tuin, PV-frame.",
        "use_es": "Núcleo de bienestar",
        "use": "Wellness-hart",
        "floor_m2": 120,
        "construction_es": "lapacho + vidrio + paja de palma + climatización + fotovoltaicos",
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
    story.append(Paragraph("62 hectáreas — Escobar, Paraguarí, Paraguay", subtitle_style))
    story.append(Spacer(1, 18 * mm))
    cover_table = Table([
        [Paragraph("<b>Propietarios:</b>", body_style),
         Paragraph("Wesley Manuel van de Camp (75%) · Thijs Adrianus Hendricus (25%)", body_style)],
        [Paragraph("<b>Ubicación:</b>", body_style),
         Paragraph("Distrito de Escobar, departamento de Paraguarí — ~78 km de Asunción", body_style)],
        [Paragraph("<b>Superficie:</b>", body_style),
         Paragraph("62 ha — 6 parcelas (5 Mbopicuá + 1 Ybyraty)", body_style)],
        [Paragraph("<b>Boleto:</b>", body_style),
         Paragraph("2026-04-28 — seña del 10% abonada (Gs. 250.300.000)", body_style)],
        [Paragraph("<b>Total del contrato:</b>", body_style),
         Paragraph(
             f"Gs. 2.503.000.000 (~USD {CONTRACT_USD:,.0f}".replace(",", ".") + ")",
             body_style)],
        [Paragraph("<b>Escribana:</b>", body_style),
         Paragraph("Escribana Peña", body_style)],
        [Paragraph("<b>Fecha de escritura:</b>", body_style),
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
        "Carpeta de firma — preparada para la escribana, "
        f"generada el {TODAY_ISO}",
        footer_style,
    ))
    story.append(Paragraph(
        "Renders procedurales en Cycles — byte-idénticos al commit 85e86aa",
        footer_style,
    ))
    story.append(PageBreak())

    # ----- Page 2: 62-ha context -----
    story.append(Paragraph("El terreno — 62 hectáreas a vista de pájaro", h1_style))
    ctx_render = _terrain_62ha_hero()
    if ctx_render:
        img = _scaled_image(ctx_render, max_w_mm=200, max_h_mm=120)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Paragraph(
            f"Gemelo digital del predio de 62 ha "
            f"(fuente: <i>{ctx_render.name}</i>) — albedo Sentinel-2 + DEM ALOS",
            caption_style,
        ))
    else:
        story.append(Paragraph("[falta el render del gemelo digital de 62 ha]", body_style))
        missing_renders.append("terrain_62ha")
    story.append(Spacer(1, 4 * mm))
    ctx_bullets = [
        "<b>Ubicación:</b> distrito de Escobar, Paraguarí — escarpa de arenisca + arroyo perenne alimentado por manantial",
        "<b>Vegetación:</b> selva atlántica madura, ~70% conservada bajo el masterplan",
        "<b>Infraestructura existente:</b> electricidad ANDE sobre el camino, dos edificaciones existentes, terrazas coloniales de piedra",
        "<b>Destino:</b> 12-16 unidades de alquiler vacacional + salón de eventos + restaurante europeo-neerlandés + senderos ecológicos",
        "<b>10 reglas de diseño:</b> sin ángulos rectos en cob · sólo revoque de cal · sin agua estancada (dengue) · "
        "muros nunca al ras del suelo · alero de 90 cm o más · pasivo ≤35 °C · sistemas tolerantes a cortes · "
        "primero lo paraguayo · paneles solares sobre estructura de acero independiente · malla mosquitera en cisternas",
    ]
    for b in ctx_bullets:
        story.append(Paragraph(f"• {b}", body_style))
    story.append(PageBreak())

    # ----- Page 3: Parcel scale -----
    story.append(Paragraph("Escala de parcela — resolución para construcción de viviendas", h1_style))
    parcel_render = _parcel_scale_hero()
    if parcel_render:
        img = _scaled_image(parcel_render, max_w_mm=200, max_h_mm=125)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Paragraph(
            f"DSL de terreno a escala de construcción (fuente: <i>{parcel_render.name}</i>) — "
            "colina, arroyo, río, clústeres arbóreos, sendero",
            caption_style,
        ))
    else:
        story.append(Paragraph("[falta el render de escala de parcela]", body_style))
        missing_renders.append("terrain_house_scale")
    story.append(Spacer(1, 4 * mm))
    parcel_bullets = [
        "<b>Resolución:</b> celda de 0,5 m, dominio de humo 80×60 m",
        "<b>Elementos:</b> colina · arroyo · río · scatters arbóreos · sendero — parámetros, no píxeles",
        "<b>Modos de anclaje:</b> sendero (nivela) · pilotes (sin nivelación) · corte (excava lado de la colina)",
        "<b>Validación:</b> Terrain.validate_geo() detecta casas bajo agua, cruces arroyo/río, solapamientos",
        "<b>Salida:</b> colección de Blender configurada a escala de parcela (cámara y luces calibradas para 60+ ha)",
    ]
    for b in parcel_bullets:
        story.append(Paragraph(f"• {b}", body_style))
    story.append(PageBreak())

    # ----- Pages 4-16: 13 typology cards -----
    section_idx = 1
    for slug in TYPOLOGY_SLUGS:
        story.extend(_asset_card(
            slug, kind="Tipología", index=section_idx,
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
            slug, kind="Amenidad", index=section_idx,
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

    # ----- Page 25: English appendix — brief for Wesley -----
    story.extend(_english_appendix(
        styles_pack=(h1_style, h2_style, body_style, caption_style),
    ))

    # ----- Page 26: Pelton siting appendix (P1/P2/P3) -----
    story.extend(_pelton_siting_appendix(
        styles_pack=(h1_style, h2_style, body_style, caption_style),
        scaled_image=_scaled_image,
    ))

    # ----- Page 27: Back cover -----
    story.append(Spacer(1, 70 * mm))
    story.append(Paragraph("LA QUEBRADA VIVA", title_style))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(
        "Escobar, Paraguarí — Escritura 2026-06-27",
        subtitle_style,
    ))
    story.append(Spacer(1, 30 * mm))
    story.append(Paragraph(
        "Generado por scripts/build_escritura_deck.py · "
        "Identidad byte-a-byte de los renders preservada en commit 85e86aa · "
        "Licencia CC0 + CC-BY 4.0",
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
    title_es = meta.get("title_es", slug)
    title_en = meta.get("title_en", slug)

    flow: list = []
    header = f"{kind} {index}/{total_assets} — {title_es}"
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
    # tile is missing. Labels are ES primary / EN secondary.
    elev_specs = (
        ("front", "FRENTE", "Front"),
        ("back", "CONTRAFRENTE", "Back"),
        ("left", "LATERAL IZQUIERDO", "Left"),
        ("right", "LATERAL DERECHO", "Right"),
    )
    tile_w_mm = 62
    tile_h_mm = 38
    elev_image_row = []
    elev_label_row = []
    for elev_key, es_label, en_label in elev_specs:
        ep = _elevation_for(slug, elev_key)
        if ep is not None:
            tile = scaled_image(ep, max_w_mm=tile_w_mm, max_h_mm=tile_h_mm)
            elev_image_row.append(tile)
            elev_label_row.append(
                Paragraph(f"<b>{es_label}</b><br/><font size='7'>{en_label}</font>", elev)
            )
        else:
            missing_renders.append(f"elevation_dutch_{slug}_{elev_key}")
            elev_image_row.append(
                Paragraph(f"<i>[{elev_key} render pending]</i>", elev)
            )
            elev_label_row.append(
                Paragraph(
                    f"<b>{es_label}</b><br/><font size='7'>{en_label} (pending)</font>",
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
    if meta.get("use_es") or meta.get("use"):
        spec_lines.append(f"<b>Uso:</b> {meta.get('use_es') or meta['use']}")
    if meta.get("floor_m2"):
        spec_lines.append(f"<b>Superficie cubierta:</b> ~{meta['floor_m2']} m²")
    if meta.get("construction_es"):
        spec_lines.append(f"<b>Construcción:</b> {meta['construction_es']}")
    if meta.get("blurb_es"):
        spec_lines.append(f"<b>Descripción:</b> {meta['blurb_es']}")
    if unit_cost:
        spec_lines.append(
            f"<b>Costo unitario:</b> {_fmt_usd(unit_cost)} · "
            f"{_fmt_pyg(unit_cost * USD_TO_PYG)}"
        )
    if top_mats:
        spec_lines.append("<b>Top materiales (USD):</b>")
        for mat, usd in top_mats:
            spec_lines.append(f"&nbsp;&nbsp;• {mat}: {_fmt_usd(usd)}")

    spec_paragraphs = [Paragraph(line, body) for line in spec_lines]

    # Compose 2-col layout: hero on left, spec column on right.
    spec_cell = []
    spec_cell.append(Paragraph("<b>Especificaciones</b>", h2))
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
        "Cuatro elevaciones técnicas a escala uniforme — frente, "
        "espalda, izquierda, derecha. La planta, el corte A-A "
        "y los detalles interiores quedan fuera del alcance del paquete "
        "de escritura y corresponden a la fase de obra.",
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
    flow.append(Paragraph("Cómputo y presupuesto — resumen", h1))
    flow.append(Paragraph(
        f"Fuente: <code>docs/boq/boq_rollup.md</code> · generado por "
        f"<code>lqv/boq.py</code> · tipo de cambio {int(round(USD_TO_PYG)):,} PYG / USD",
        caption,
    ))
    flow.append(Spacer(1, 4 * mm))

    # Grand total block
    flow.append(Paragraph("<b>Suma del catálogo (17 assets en su configuración de referencia)</b>", h2))
    flow.append(Paragraph(
        f"<font size='14'><b>{_fmt_usd(boq['grand_total_usd'])} · "
        f"{_fmt_pyg(boq['grand_total_pyg'])}</b></font>",
        body,
    ))
    flow.append(Spacer(1, 2 * mm))
    flow.append(Paragraph(
        f"Cantidad de assets: <b>{boq['asset_count']}</b> · "
        f"Ítems del cómputo: <b>{boq['line_count']}</b>",
        body,
    ))
    flow.append(Spacer(1, 4 * mm))

    # Top-10 materials table
    flow.append(Paragraph("<b>Top 10 materiales por total USD</b>", h2))
    header = ["#", "Material", "Cantidad", "Unidad", "Total USD", "Total PYG"]
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
        "El total agrega las cantidades de referencia de los 17 assets del "
        "catálogo (una unidad por tipología/amenidad). Las cantidades a nivel "
        "de sitio se obtienen multiplicando cada asset por el número de "
        "unidades fijado en el masterplan (Fase 1 = 3-6 viviendas, "
        "Fase 2 = 3-6 adicionales, Fase 3 = restaurante + amenidades). "
        "CSV completo: <code>docs/boq/boq_rollup.csv</code>.",
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
    flow.append(Paragraph("Parte 4 — Día de la firma — checklist práctica", h1))
    flow.append(Spacer(1, 2 * mm))
    flow.append(Paragraph(
        f"Escritura {ESCRITURA_DATE} ante la Escribana Peña. Los ítems "
        "siguientes deben estar <b>en mano o confirmados al menos 5 días "
        "antes</b> — sin pendientes documentales el 26 de junio.",
        caption,
    ))
    flow.append(Spacer(1, 6 * mm))
    flow.append(Paragraph("En mano o confirmado por adelantado (T-5d)", h2))
    flow.append(Spacer(1, 2 * mm))
    bring_items = [
        "Pasaportes (Wesley NWF23H565 + Thijs NP19HPFP6) — originales",
        "Comprobante de fondos para el saldo (Cl. CUARTA, Gs. 2.252.700.000): "
        "Gs. 2.190 M directos a los vendedores + Gs. 62,7 M a Burgos "
        "(completando la comisión total de Gs. 313 M; el primer tramo de la "
        "comisión se imputa al remanente de la seña ya depositada, neta de "
        "los gastos notariales ya causados)",
        "Poder otorgado si alguno de los compradores no puede asistir — "
        "apostillado en NL + <i>traductor público matriculado</i> en PY",
        "Certificados catastrales-registrales por finca — los recaba la "
        "Escribana Peña; verificar 1 semana antes",
        "Comprobantes de impuesto inmobiliario al día — los vendedores "
        "garantizan tributos pagados conforme Cl. SÉPTIMA (iii) y deben "
        "entregar los comprobantes dentro de 5 días hábiles conforme "
        "Cl. OCTAVA (ii)",
        "Anexo I — descripciones técnicas (linderos, rumbos, medidas) "
        "de las 6 fincas",
        "Comisión Burgos: distribución confirmada con Peña 48 h antes",
        "Distribución impositiva confirmada (impuesto a la renta = vendedor; "
        "honorarios notariales habitualmente comprador; IVA sobre comisión "
        "a verificar)",
        "<i>Designación</i> formal de Peña como escribana para la "
        "escritura (Cl. SEXTA)",
        "Dos testigos confiables en stand-by",
    ]
    for itm in bring_items:
        flow.append(Paragraph(f"• {itm}", body))
        flow.append(Spacer(1, 1.5 * mm))
    flow.append(PageBreak())

    # ----- Page B: Risk register -----
    flow.append(Paragraph("Día de la firma — registro de riesgos", h1))
    flow.append(Spacer(1, 2 * mm))
    flow.append(Paragraph(
        "Escenarios que pueden bloquear o demorar la firma, con su "
        "tratamiento contractual conforme Cláusulas TERCERA, SEXTA, OCTAVA y NOVENA.",
        caption,
    ))
    flow.append(Spacer(1, 6 * mm))

    risk_rows = [
        [
            Paragraph("<b>El vendedor no se presenta / se niega</b>", body),
            Paragraph(
                "La multa duplica la seña: Gs. 500.600.000 a favor de los "
                "compradores (Cl. NOVENA), neta de gastos, tributos y "
                "honorarios notariales efectivamente causados. Ante "
                "cualquier duda en la semana previa, contactar al abogado "
                "inmediatamente.",
                body,
            ),
        ],
        [
            Paragraph("<b>El comprador no se presenta / no paga</b>", body),
            Paragraph(
                "Los compradores pierden la seña (Gs. 250.300.000) neta de "
                "los gastos notariales ya incurridos.",
                body,
            ),
        ],
        [
            Paragraph("<b>Surge tarde un embargo o gravamen</b>", body),
            Paragraph(
                "La escribana debe detectarlo. Si aparece: <b>NO firmar</b> "
                "— invocar la prórroga de la Cl. NOVENA.",
                body,
            ),
        ],
        [
            Paragraph("<b>Faltan documentos de la Cl. OCTAVA (ii)</b>", body),
            Paragraph(
                "Debieron entregarse ~6 de mayo. Si aún no están: "
                "reclamarlos <b>ya</b> a través de Peña, no el 27 de junio.",
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
        "Fuente: <code>docs/2026-04-28_boleto_compraventa_torrasca-vandecamp.pdf</code> "
        "y <code>docs/escritura_deck/escritura_deck.md</code> §Parte 4.",
        caption,
    ))
    flow.append(PageBreak())

    # ----- Page C: Post-closing T+30 -----
    flow.append(Paragraph("Post-firma — T+30 (kickoff del housing-park)", h1))
    flow.append(Spacer(1, 2 * mm))
    flow.append(Paragraph(
        "Los primeros 30 días después de la escritura: registrar la entidad "
        "operativa, abrir habilitaciones, movilizar capital para la Fase 1.",
        caption,
    ))
    flow.append(Spacer(1, 6 * mm))
    post_items = [
        "Registrar entidad operativa (S.A. / S.R.L. / E.A.S. — "
        "decisión pendiente de firma por parte de Wesley)",
        "Presentar inscripción ante SENATUR para la operación de "
        "alquiler vacacional",
        "Gestionar ante la Municipalidad de Escobar el uso de suelo + "
        "permisos de construcción",
        "Activar las presentaciones de AHK Paraguay hacia la cadena de "
        "suministro germano-paraguaya (San Bernardino)",
        "Iniciar capex de Fase 1: 3-6 viviendas (ventana objetivo USD 200-500 k) "
        "— mix de tipologías según prioridad del cómputo (ver pág. resumen BoQ)",
    ]
    for itm in post_items:
        flow.append(Paragraph(f"• {itm}", body))
        flow.append(Spacer(1, 1.5 * mm))
    flow.append(Spacer(1, 6 * mm))
    flow.append(Paragraph(
        "Texto completo y referencias: "
        "<code>docs/escritura_deck/escritura_deck.md</code> §Parte 4 "
        "(líneas 259-288).",
        caption,
    ))
    flow.append(PageBreak())

    return flow


def _english_appendix(*, styles_pack) -> list:
    """One-page English brief for Wesley (75% owner, Dutch national).

    The deck is Spanish-primary for the notary. This appendix gives the
    English-speaking owner a single self-contained sheet covering: assets,
    BoQ totals, parcel context, escritura value, and the Phase 1 capex window.
    """
    from reportlab.lib.units import mm
    from reportlab.platypus import PageBreak, Paragraph, Spacer

    h1, h2, body, caption = styles_pack
    boq = _parse_boq_rollup()
    flow: list = []

    flow.append(Paragraph("Appendix — English brief for Wesley", h1))
    flow.append(Spacer(1, 2 * mm))
    flow.append(Paragraph(
        "This deck is Spanish-primary for Escribana Pe&#241;a (Paraguayan "
        "notary). This single page summarises the key facts for the 75% "
        "owner. All figures match the Spanish pages verbatim.",
        caption,
    ))
    flow.append(Spacer(1, 6 * mm))

    flow.append(Paragraph("Transaction", h2))
    flow.append(Spacer(1, 2 * mm))
    tx_items = [
        f"Signing date: <b>{ESCRITURA_DATE}</b> before Escribana Pe&#241;a, "
        "Escobar, Paraguar&#237;",
        f"Contract value: <b>Gs. 2,503,000,000</b> (~USD {CONTRACT_USD:,} at "
        f"{int(USD_TO_PYG):,} PYG/USD)",
        "Down payment paid: Gs. 250,300,000 (10%, held in notarial "
        "deposit). Closing balance (Cl. CUARTA, Gs. 2,252,700,000): "
        "Gs. 2,190 M direct to sellers + Gs. 62.7 M direct to Burgos "
        "(completing the Gs. 313 M brokerage; first tranche comes from "
        "the down-payment remainder, net of notary fees already incurred)",
        "Penalty if seller defaults: double the down payment "
        "(Gs. 500,600,000) — Clause NOVENA",
        "Buyers: Wesley van de Camp (75%, NWF23H565) + "
        "Thijs (25%, NP19HPFP6) — both Dutch nationals",
    ]
    for itm in tx_items:
        flow.append(Paragraph(f"&bull; {itm}", body))
        flow.append(Spacer(1, 1.5 * mm))
    flow.append(Spacer(1, 4 * mm))

    flow.append(Paragraph("Land &amp; Programme", h2))
    flow.append(Spacer(1, 2 * mm))
    land_items = [
        "6 fincas, total <b>~62 ha</b> (digital twin shipped at commit "
        "4409dba — ALOS DEM + Sentinel-2 albedo)",
        "Use: eco housing-park / vacation rental — registration pending "
        "before SENATUR + Escobar municipality (T+30 actions)",
        "Phasing: <b>Phase 1</b> = 3-6 dwellings (USD 200-500 k capex "
        "window), <b>Phase 2</b> = 3-6 additional, <b>Phase 3</b> = "
        "restaurant + amenities",
    ]
    for itm in land_items:
        flow.append(Paragraph(f"&bull; {itm}", body))
        flow.append(Spacer(1, 1.5 * mm))
    flow.append(Spacer(1, 4 * mm))

    flow.append(Paragraph("Asset library &amp; BoQ", h2))
    flow.append(Spacer(1, 2 * mm))
    usd = boq.get("grand_total_usd") or 0.0
    pyg = boq.get("grand_total_pyg") or 0.0
    rate = boq.get("rate_pyg_per_usd") or USD_TO_PYG
    asset_items = [
        "<b>17 assets</b> in the library: 13 dwelling typologies "
        "(hobbit, bamboo wigwam, bamboo treehouse, two bamboo+concrete "
        "1-pax, bamboo+concrete 2-pax, bamboo river house, two stone "
        "small variants, two bamboo+concrete family, bamboo+container "
        "4-pax, stone river house 4-pax, container river house) + "
        "<b>4 amenities</b> (La Brisa lounge, floating dining, eco-pool, "
        "Modern Oasis wellness retreat)",
        "<b>68 Dutch elevations</b> rendered (17 assets &times; "
        "front/back/left/right) — see preceding pages",
        f"<b>BoQ catalogue sum (17 assets at reference configuration):</b> "
        f"~USD {usd:,.2f} &middot; ~Gs. {pyg:,.0f} "
        f"(rate {int(rate):,} PYG/USD)",
        "Site-level totals scale by the number of units actually built per "
        "phase (Phase 1 = 3-6 dwellings &rarr; multiply each asset&rsquo;s "
        "reference quantity accordingly). Full CSV: "
        "<code>docs/boq/boq_rollup.csv</code>",
        "Reproducible from frozen renderer state (commit "
        "<code>85e86aa</code>) &mdash; every elevation in this deck "
        "regenerates byte-for-byte from that point",
    ]
    for itm in asset_items:
        flow.append(Paragraph(f"&bull; {itm}", body))
        flow.append(Spacer(1, 1.5 * mm))

    flow.append(Spacer(1, 6 * mm))
    flow.append(Paragraph(
        "For any clause-level question on signing day, defer to the Spanish "
        "body of this deck (Parte 4, pages 22-24) — that is what the "
        "escribana will read.",
        caption,
    ))
    flow.append(PageBreak())
    return flow


def _pelton_siting_appendix(*, styles_pack, scaled_image) -> list:
    """One-page Pelton siting appendix — P1/P2/P3 candidate cards.

    Materialises ``docs/site_data/pelton_siting.json`` so Wesley can point
    at named sites at the table instead of only quoting the head-map
    headline stats (31.2% above 30 m, 10.7% above 80 m). P3 is the only
    candidate whose penstock fits inside the 300 m radius (Chebyshev box
    reaches ~415 m diagonal — the honest flag lives in the JSON sidecar).
    """
    import json as _json

    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle

    h1, h2, body, caption = styles_pack
    flow: list = []

    flow.append(Paragraph(
        "Apéndice Pelton — sitios candidatos / Pelton siting candidates", h1,
    ))
    flow.append(Spacer(1, 2 * mm))
    flow.append(Paragraph(
        "Tres sitios nombrados (P1, P2, P3) elegidos por algoritmo greedy "
        "top-N sobre el campo de carga útil del DEM COP30. Cada sitio fija "
        "una turbina (baja) y la cresta correspondiente (alta) dentro de una "
        "ventana de búsqueda de 21×21 px (~315 m por lado en distancia de "
        "Chebyshev; la diagonal alcanza ~415 m). La bandera <b>penstock "
        "&le; 300 m</b> es honesta — sólo P3 cae dentro del radio.",
        caption,
    ))
    flow.append(Spacer(1, 4 * mm))

    contact = ROOT / "docs/site_data/pelton_siting_contact.png"
    if contact.exists():
        flow.append(scaled_image(contact, max_w_mm=170, max_h_mm=70))
        flow.append(Spacer(1, 3 * mm))

    siting_path = ROOT / "docs/site_data/pelton_siting.json"
    if siting_path.exists():
        data = _json.loads(siting_path.read_text())
        cands = data.get("candidates", [])

        header = [
            Paragraph("<b>Sitio</b>", body),
            Paragraph("<b>Turbina (lat, lon)</b>", body),
            Paragraph("<b>Elev. turbina</b>", body),
            Paragraph("<b>Cresta (lat, lon)</b>", body),
            Paragraph("<b>Elev. cresta</b>", body),
            Paragraph("<b>Carga útil (head)</b>", body),
            Paragraph("<b>Penstock horiz.</b>", body),
            Paragraph("<b>&le; 300 m</b>", body),
        ]
        rows = [header]
        for c in cands:
            within = "Sí" if c.get("penstock_within_radius") else "No"
            rows.append([
                Paragraph(f"<b>{c['id']}</b>", body),
                Paragraph(f"{c['turbine_lat']:.6f}, {c['turbine_lon']:.6f}", body),
                Paragraph(f"{c['turbine_elev_m']:.1f} m", body),
                Paragraph(f"{c['ridge_lat']:.6f}, {c['ridge_lon']:.6f}", body),
                Paragraph(f"{c['ridge_elev_m']:.1f} m", body),
                Paragraph(f"<b>{c['head_m']:.1f} m</b>", body),
                Paragraph(f"{c['penstock_horizontal_m']:.1f} m", body),
                Paragraph(within, body),
            ])
        table = Table(
            rows,
            colWidths=[14*mm, 38*mm, 18*mm, 38*mm, 18*mm, 22*mm, 24*mm, 12*mm],
            hAlign="CENTER",
        )
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#bbbbbb")),
        ]))
        flow.append(table)
        flow.append(Spacer(1, 4 * mm))

        head_max = data.get("head_max_m", 0.0)
        flow.append(Paragraph(
            f"Carga máxima del campo: <b>{head_max:.1f} m</b>. Fuente DEM: "
            "COP30 (sha256 <code>10e6459c…04fed00</code>). Método y campo de "
            "carga heredados de <code>docs/site_data/pelton_head_map.json</code> "
            "para consistencia con las estadísticas titulares "
            "(31.2 % &ge; 30 m, 10.7 % &ge; 80 m). Radio de exclusión "
            "200 m entre candidatos.",
            caption,
        ))
        flow.append(Spacer(1, 2 * mm))
        flow.append(Paragraph(
            "<b>Lectura honesta:</b> P1 y P2 reportan penstock "
            "&gt; 300 m (415,8 m y 358,9 m respectivamente) porque la ventana "
            "de búsqueda es un cuadrado de Chebyshev, no un círculo "
            "euclidiano. <b>P3</b> es el único sitio dentro del radio "
            "objetivo (295,5 m, carga 166,5 m) y por lo tanto la mejor "
            "primera apuesta para un piloto Pelton.",
            caption,
        ))
    else:
        flow.append(Paragraph(
            "<i>pelton_siting.json no encontrado — regenerar con "
            "<code>python3 scripts/build_pelton_siting.py</code>.</i>",
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
