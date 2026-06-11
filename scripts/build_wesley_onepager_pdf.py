"""Build docs/wesley_brief_onepager.pdf from the markdown source.

Pipeline: markdown -> HTML (with embedded print CSS + base64 hero thumbnail)
-> google-chrome --headless --print-to-pdf.

Why this stack: pandoc/weasyprint/wkhtmltopdf are not installed in this env;
google-chrome and the `markdown` Python package are. Chrome's print engine
honours @page rules, gives clean typography, and runs headless with no GUI.

Run via `make pdf` or directly:
    python3 scripts/build_wesley_onepager_pdf.py
"""
from __future__ import annotations

import base64
import io
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_MD = ROOT / "docs" / "wesley_brief_onepager.md"
OUT_PDF = ROOT / "docs" / "wesley_brief_onepager.pdf"
HERO_PNG = ROOT / "renders" / "A_hero.png"
TMP_HTML = Path("/tmp/wesley_brief_onepager.html")

CSS = """
@page { size: A4; margin: 16mm 18mm 16mm 18mm; }
html, body { font-family: Georgia, "Charter", "Liberation Serif", serif;
             font-size: 10.5pt; line-height: 1.38; color: #1a1a1a; }
h1 { font-size: 19pt; margin: 0 0 6pt 0; border-bottom: 2px solid #444;
     padding-bottom: 4pt; }
h2 { font-size: 13pt; margin: 14pt 0 4pt 0; color: #2a2a2a;
     border-bottom: 1px solid #bbb; padding-bottom: 2pt;
     page-break-after: avoid; }
h3 { font-size: 11.5pt; margin: 10pt 0 3pt 0; page-break-after: avoid; }
p  { margin: 4pt 0; }
ul, ol { margin: 4pt 0 4pt 18pt; padding: 0; }
li { margin: 1pt 0; }
blockquote { margin: 6pt 0 6pt 0; padding: 6pt 10pt;
             background: #f4f1ea; border-left: 3px solid #b08a3e;
             font-style: italic; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0;
        page-break-inside: avoid; font-size: 9.5pt; }
th, td { border: 1px solid #888; padding: 3pt 6pt; vertical-align: top;
         text-align: left; }
th { background: #ece6d6; font-weight: bold; }
code { font-family: "Source Code Pro", Menlo, Consolas, monospace;
       font-size: 9pt; background: #f0ede4; padding: 0 3px;
       border-radius: 2px; }
strong { color: #111; }
img.hero { display: block; width: 140mm; max-width: 100%; height: auto;
           margin: 6pt auto 10pt auto; border: 1px solid #888; }
.footer { margin-top: 12pt; font-size: 8.5pt; color: #666;
          border-top: 1px solid #ccc; padding-top: 4pt; text-align: center; }
"""

HTML_SHELL = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Wesley — Pre-closing Brief</title>
<style>{css}</style>
</head><body>
<img class="hero" src="{hero_data_uri}" alt="La Quebrada Viva — Variant A hero render">
{body}
<div class="footer">Generated from docs/wesley_brief_onepager.md via scripts/build_wesley_onepager_pdf.py</div>
</body></html>
"""


def _resize_hero_to_data_uri(src: Path, max_width_px: int = 1400) -> str:
    from PIL import Image
    img = Image.open(src)
    if img.mode != "RGB":
        img = img.convert("RGB")
    w, h = img.size
    if w > max_width_px:
        new_h = int(h * (max_width_px / w))
        img = img.resize((max_width_px, new_h), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=82, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def _md_to_html(text: str) -> str:
    import markdown
    return markdown.markdown(
        text,
        extensions=["extra", "tables", "sane_lists"],
        output_format="html",
    )


def _chrome_print(html_path: Path, pdf_path: Path) -> None:
    cmd = [
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if proc.returncode != 0 or not pdf_path.exists():
        sys.stderr.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        raise SystemExit(f"chrome print-to-pdf failed (rc={proc.returncode})")


def _page_count(pdf_path: Path) -> int | None:
    try:
        proc = subprocess.run(
            ["pdfinfo", str(pdf_path)], capture_output=True, text=True, timeout=10
        )
    except FileNotFoundError:
        return None
    for line in proc.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    return None


def main() -> int:
    if not SRC_MD.exists():
        raise SystemExit(f"missing source: {SRC_MD}")
    if not HERO_PNG.exists():
        raise SystemExit(f"missing hero render: {HERO_PNG}")
    hero_uri = _resize_hero_to_data_uri(HERO_PNG)
    body = _md_to_html(SRC_MD.read_text(encoding="utf-8"))
    html = HTML_SHELL.format(css=CSS, hero_data_uri=hero_uri, body=body)
    TMP_HTML.write_text(html, encoding="utf-8")
    _chrome_print(TMP_HTML, OUT_PDF)
    size_kb = OUT_PDF.stat().st_size / 1024
    pages = _page_count(OUT_PDF)
    pages_str = f"{pages} page(s)" if pages is not None else "page count unknown (pdfinfo not installed)"
    print(f"[wesley-pdf] wrote {OUT_PDF.relative_to(ROOT)} ({size_kb:.1f} KB, {pages_str})")
    if pages is not None and pages > 4:
        sys.stderr.write(f"[wesley-pdf] WARNING: PDF is {pages} pages (>4 page brief limit)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
