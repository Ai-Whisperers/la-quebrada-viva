"""Assemble the Wesley escritura-day deliverable bundle.

Single zip containing the artefacts the buyer (Wesley van de Camp) and the
notary need on 2026-06-27: PDF brief, 18 hero/cliff/dusk/terrace renders
(A/B/C), 6 terrain digital-twin renders, DEM A/B cross-check, BoQ in three
formats, PROVENANCE.md, satdata brief, escritura deck v6, and the Pelton
head feasibility map. SHA-256 sidecar accompanies the zip for tamper
verification.

Run:  python3 scripts/build_wesley_bundle.py
Outputs:
  dist/wesley_bundle_<YYYYMMDD-HHMM>.zip
  dist/wesley_bundle_<YYYYMMDD-HHMM>.zip.sha256
  dist/wesley_bundle_<YYYYMMDD-HHMM>.manifest.txt
"""
from __future__ import annotations

import datetime as dt
import hashlib
import sys
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DIST = PROJECT_ROOT / "dist"

FINAL_RENDER_BASENAMES = (
    "hero", "cliff", "dusk", "petal_macro", "stream_up", "terrace",
)
VARIANTS = ("A", "B", "C")


def _gather() -> list[tuple[Path, str]]:
    """Return (source_path, arcname) tuples to include in the zip."""
    items: list[tuple[Path, str]] = []

    # PDF v-final brief (one-pager)
    pdf_brief = PROJECT_ROOT / "docs/wesley_brief_onepager.pdf"
    if pdf_brief.exists():
        items.append((pdf_brief, "01_brief/wesley_brief_onepager.pdf"))

    # Escritura deck v6
    deck = PROJECT_ROOT / "docs/escritura_deck/escritura_deck_v6.pdf"
    if deck.exists():
        items.append((deck, "02_escritura_deck/escritura_deck_v6.pdf"))

    # 18 hero finals (6 cams × 3 variants A/B/C)
    for v in VARIANTS:
        for base in FINAL_RENDER_BASENAMES:
            png = PROJECT_ROOT / f"renders/{v}_{base}.png"
            if png.exists():
                items.append((png, f"03_renders_finals/{v}_{base}.png"))

    # Terrain digital twin — v5_arrowfix birdseye + oblique (A/B/C each)
    for cam in ("birdseye", "oblique"):
        for v in VARIANTS:
            png = PROJECT_ROOT / (
                f"renders/sub/runs/20260611_dt_run_v5_arrowfix_terrain_62ha_{cam}/{v}.png"
            )
            if png.exists():
                items.append((png, f"04_terrain_digital_twin/{cam}_{v}.png"))

    # DEM A/B contact sheet
    dem_ab = PROJECT_ROOT / "docs/site_data/dem_ab_contact.png"
    if dem_ab.exists():
        items.append((dem_ab, "05_dem_ab/dem_ab_contact.png"))

    # Pelton head feasibility map + sidecar + labeled contact sheet
    # + named candidate siting (P1/P2/P3) with within-radius flags
    for fn in (
        "pelton_head_map.png",
        "pelton_head_map.json",
        "pelton_head_map_contact.png",
        "pelton_siting.json",
        "pelton_siting_contact.png",
    ):
        p = PROJECT_ROOT / "docs/site_data" / fn
        if p.exists():
            items.append((p, f"06_pelton_feasibility/{fn}"))

    # BoQ trio
    for ext in ("csv", "md", "pdf"):
        p = PROJECT_ROOT / f"docs/boq/boq_rollup.{ext}"
        if p.exists():
            items.append((p, f"07_boq/boq_rollup.{ext}"))

    # PROVENANCE + satdata brief
    prov = PROJECT_ROOT / "PROVENANCE.md"
    if prov.exists():
        items.append((prov, "08_provenance/PROVENANCE.md"))
    satb = PROJECT_ROOT / "docs/site_data/satdata_brief.md"
    if satb.exists():
        items.append((satb, "08_provenance/satdata_brief.md"))

    return items


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    DIST.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M")
    zip_path = DIST / f"wesley_bundle_{stamp}.zip"
    sha_path = DIST / f"wesley_bundle_{stamp}.zip.sha256"
    manifest_path = DIST / f"wesley_bundle_{stamp}.manifest.txt"

    items = _gather()
    missing: list[str] = []
    expected = {
        "wesley_brief_onepager.pdf", "escritura_deck_v6.pdf",
        "dem_ab_contact.png", "pelton_head_map.png", "pelton_head_map.json",
        "pelton_siting.json", "pelton_siting_contact.png",
        "boq_rollup.csv", "boq_rollup.md", "boq_rollup.pdf",
        "PROVENANCE.md", "satdata_brief.md",
    }
    present = {p.name for p, _ in items}
    missing = sorted(expected - present)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for src, arc in items:
            zf.write(src, arcname=arc)

    digest = _sha256(zip_path)
    sha_path.write_text(f"{digest}  {zip_path.name}\n")

    manifest_lines = [
        f"# Wesley deliverable bundle — La Quebrada Viva",
        f"# Built: {dt.datetime.now().isoformat(timespec='seconds')}",
        f"# Escritura signing: 2026-06-27 (T-12 from 2026-06-15)",
        f"# Buyer: Wesley van de Camp",
        f"# Zip: {zip_path.name}",
        f"# SHA-256: {digest}",
        f"# File count: {len(items)}",
        "",
    ]
    for src, arc in items:
        manifest_lines.append(f"{_sha256(src)}  {arc}  ({src.stat().st_size} B)")
    if missing:
        manifest_lines.append("")
        manifest_lines.append("# MISSING (expected but not found in repo):")
        for m in missing:
            manifest_lines.append(f"#   {m}")
    manifest_path.write_text("\n".join(manifest_lines) + "\n")

    print(f"WROTE {zip_path.relative_to(PROJECT_ROOT)}  ({zip_path.stat().st_size // 1024} KB, {len(items)} files)")
    print(f"WROTE {sha_path.relative_to(PROJECT_ROOT)}  (sha256={digest[:16]}…)")
    print(f"WROTE {manifest_path.relative_to(PROJECT_ROOT)}")
    if missing:
        print(f"WARN: missing expected files: {', '.join(missing)}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
