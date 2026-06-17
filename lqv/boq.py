"""Bill-of-Quantities rollup across typologies + amenities.

Walks every ``lqv.typologies.*`` and ``lqv.amenities.*`` module (skipping
``__init__`` and any ``_*`` private module), reads each module's
``MATERIAL_TAKEOFF: dict[str, dict]`` constant, sums quantities per material,
multiplies by ``unit_cost_usd``, converts USD -> PYG at the canonical 7300
PYG/USD rate, and emits:

    docs/boq/boq_rollup.csv
    docs/boq/boq_rollup.md
    docs/boq/boq_rollup.pdf

Each ``MATERIAL_TAKEOFF`` entry has exactly one of
``volume_m3 | area_m2 | length_m | count | weight_kg`` plus ``unit_cost_usd``.
Material-name granularity is preserved (no canonicalisation): same-name
materials are summed across modules; module-specific synthetic line-items
(e.g. ``lapacho_dome_struts``) stay as their own rows.

Runs both as:

    python3 lqv/boq.py              # direct (installs bpy stub inline)
    python3 scripts/build_boq.py    # via existing driver that installs stubs

In either case the result of ``main(out_dir=...)`` is a dict that
``scripts/build_boq.py`` consumes for its CLI banner.
"""
from __future__ import annotations

import csv
import datetime as _dt
import importlib
import os
import pkgutil
import shutil
import subprocess
import sys
import types
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, cast

from lqv.finance import get_usd_to_pyg as _get_usd_to_pyg

# Module-level snapshot so the rate stays stable across a single rollup run
# even if `docs/finance/fx.json` is edited mid-run. `main()` re-reads via the
# accessor before each invocation; tests can mutate the JSON and call
# `lqv.finance.reset_cache()` between cases.
USD_TO_PYG = _get_usd_to_pyg()  # see docs/finance/fx.json — canonical rate

_QTY_FIELDS = ('volume_m3', 'area_m2', 'length_m', 'count', 'weight_kg')
_QTY_UNIT = {
    'volume_m3': 'm3',
    'area_m2': 'm2',
    'length_m': 'm',
    'count': 'count',
    'weight_kg': 'kg',
}


# ---------------------------------------------------------------------------
# bpy/materials stub installation — only when run directly (not from
# scripts/build_boq.py which already installs richer stubs).
# ---------------------------------------------------------------------------
class _PermissiveNS(types.ModuleType):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def __getattr__(self, name: str):
        child = _PermissiveNS(f'{self.__name__}.{name}')
        setattr(self, name, child)
        return child

    def __call__(self, *a, **kw):
        return _PermissiveNS(self.__name__ + '()')


def _install_stubs_if_needed() -> None:
    """Install lightweight bpy + lqv.materials stubs if not already present.

    Typology and amenity modules ``import bpy`` at module top, so direct import
    outside Blender would fail. ``MATERIAL_TAKEOFF`` is a top-level dict literal
    that doesn't touch Blender APIs, so a permissive stub is safe.
    """
    if 'bpy' not in sys.modules:
        bpy = cast(Any, _PermissiveNS('bpy'))
        bpy.context = _PermissiveNS('bpy.context')
        bpy.data = _PermissiveNS('bpy.data')
        bpy.ops = _PermissiveNS('bpy.ops')
        bpy.types = _PermissiveNS('bpy.types')
        for cls_name in ('Collection', 'Object', 'Material', 'Mesh',
                         'Camera', 'Light', 'Scene'):
            setattr(bpy.types, cls_name, type(cls_name, (), {}))
        sys.modules['bpy'] = bpy
        sys.modules['bpy.types'] = bpy.types
    if 'mathutils' not in sys.modules:
        mathutils = cast(Any, _PermissiveNS('mathutils'))
        mathutils.Vector = lambda *a, **kw: a
        mathutils.Matrix = lambda *a, **kw: None
        mathutils.Euler = lambda *a, **kw: a
        mathutils.Quaternion = lambda *a, **kw: a
        sys.modules['mathutils'] = mathutils
    if 'bmesh' not in sys.modules:
        sys.modules['bmesh'] = _PermissiveNS('bmesh')
    # NB: do NOT stub ``lqv.materials`` — the real package's top-level imports
    # only define functions; principled() etc. don't touch bpy until called
    # inside build() at scene-build time. Stubbing it breaks transitive
    # imports like ``from lqv.house.bamboo_frame import ...`` that re-import
    # ``principled`` via ``from lqv.materials._shaders import principled``.


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class BoQLine:
    module: str
    material: str
    quantity: float
    unit: str           # m3 | m2 | m | count | kg
    unit_cost_usd: float
    subtotal_usd: float
    subtotal_pyg: float


def _infer_qty(entry: dict) -> tuple[float, str]:
    """Pull (quantity, unit) from a MATERIAL_TAKEOFF entry.

    Each entry MUST carry exactly one of :data:`_QTY_FIELDS`. Silently
    defaulting to ``(0.0, 'count')`` on missing quantity (the prior
    behaviour) let typos like ``volumem3`` or ``counts`` ship as $0 lines
    that vanished into the rollup — a single missing quantity could
    swallow tens of thousands of USD with no warning. We now raise so the
    rollup driver either logs+skips the module (with ``skip_broken=True``)
    or fails the whole run loudly.
    """
    for field in _QTY_FIELDS:
        if field in entry:
            return float(entry[field]), _QTY_UNIT[field]
    raise ValueError(
        f"MATERIAL_TAKEOFF entry missing quantity field; expected one of "
        f"{_QTY_FIELDS}, got keys={sorted(entry.keys())!r}"
    )


def _iter_modules(package_name: str) -> Iterable[str]:
    pkg = importlib.import_module(package_name)
    # Sort by module name so row order in boq_rollup.{csv,md} is deterministic
    # across hosts (pkgutil.iter_modules returns filesystem order, which
    # diverges between ext4 / xfs / macOS APFS and breaks diff-based review).
    for info in sorted(pkgutil.iter_modules(pkg.__path__), key=lambda m: m.name):
        if info.name.startswith('_'):
            continue
        yield f'{package_name}.{info.name}'


def _collect_from_module(modname: str) -> list[BoQLine]:
    mod = importlib.import_module(modname)
    takeoff = getattr(mod, 'MATERIAL_TAKEOFF', None)
    if not takeoff:
        return []
    short = modname.rsplit('.', 1)[-1]
    out: list[BoQLine] = []
    for material, entry in takeoff.items():
        qty, unit = _infer_qty(entry)
        unit_cost = float(entry.get('unit_cost_usd', 0.0))
        subtotal_usd = qty * unit_cost
        out.append(BoQLine(
            module=short,
            material=material,
            quantity=qty,
            unit=unit,
            unit_cost_usd=unit_cost,
            subtotal_usd=subtotal_usd,
            subtotal_pyg=subtotal_usd * USD_TO_PYG,
        ))
    return out


def collect_all(*, skip_broken: bool = True) -> list[BoQLine]:
    """Walk typologies + amenities, return every BoQ line.

    Modules that fail to import (e.g. missing bpy attrs the stub doesn't cover)
    are logged to stderr **with a full traceback** and skipped when
    ``skip_broken`` is True. The traceback matters: prior versions printed
    only the exception ``repr`` which collapsed a 12-frame KeyError chain
    inside an amenity's MATERIAL_TAKEOFF into a one-line ``KeyError: 'foo'``
    — useless for diagnosing which line of which module dropped the row,
    so the BoQ silently undercounted by tens of thousands of USD until
    someone noticed the totals didn't match the deck.
    """
    import traceback
    lines: list[BoQLine] = []
    for pkg in ('lqv.typologies', 'lqv.amenities'):
        for modname in _iter_modules(pkg):
            try:
                lines.extend(_collect_from_module(modname))
            except Exception as e:  # noqa: BLE001 — aggregate + log per spec
                print(
                    f'[boq] WARN skip {modname}: {type(e).__name__}: {e}',
                    file=sys.stderr,
                )
                traceback.print_exc(file=sys.stderr)
                if not skip_broken:
                    raise
    return lines


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------
def per_material_rollup(lines: Iterable[BoQLine]) -> list[dict]:
    """Sum quantity + subtotal per (material, unit) pair.

    Earlier versions keyed only on ``material`` and collapsed mixed-unit
    groups to ``unit='mixed', total_quantity=0.0``. That hides real demand
    — e.g. ``adobe_brick`` counted as ``count`` (bricks) in one typology
    and ``m3`` (volumetric mix) in another both appeared in the rollup as
    a single zero-quantity row, so the procurement team had no idea how
    many bricks to actually order. Splitting per unit keeps each row
    summable and orderable; the USD totals are unchanged in aggregate.
    """
    by_key: dict[tuple[str, str], dict] = {}
    for line in lines:
        key = (line.material, line.unit)
        slot = by_key.setdefault(key, {
            'material': line.material,
            'total_quantity': 0.0,
            'unit': line.unit,
            'total_usd': 0.0,
            'total_pyg': 0.0,
        })
        slot['total_quantity'] += line.quantity
        slot['total_usd'] += line.subtotal_usd
        slot['total_pyg'] += line.subtotal_pyg

    rows = list(by_key.values())
    # Primary sort: USD descending (biggest spend first for procurement).
    # Secondary: material name then unit, so rows for the same material
    # but different units cluster (helps cross-checking the split).
    rows.sort(key=lambda r: (-r['total_usd'], r['material'], r['unit']))
    return rows


def grand_total_usd(lines: Iterable[BoQLine]) -> float:
    return round(sum(line.subtotal_usd for line in lines), 2)


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------
_CSV_LINE_COLS = ['module', 'material', 'quantity', 'unit',
                  'unit_cost_usd', 'subtotal_usd', 'subtotal_pyg']
_CSV_ROLLUP_COLS = ['material', 'total_quantity', 'unit', 'total_usd', 'total_pyg']


def write_csv(lines: list[BoQLine], out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    rollup = per_material_rollup(lines)
    total_usd = grand_total_usd(lines)
    total_pyg = total_usd * USD_TO_PYG

    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        # Section 1: per-module line items
        w.writerow(['# Per-module line items'])
        w.writerow(_CSV_LINE_COLS)
        for line in lines:
            w.writerow([
                line.module,
                line.material,
                f'{line.quantity:.4f}',
                line.unit,
                f'{line.unit_cost_usd:.2f}',
                f'{line.subtotal_usd:.2f}',
                f'{line.subtotal_pyg:.0f}',
            ])
        w.writerow([])
        # Section 2: per-material rollup
        w.writerow(['# Per-material rollup'])
        w.writerow(_CSV_ROLLUP_COLS)
        for r in rollup:
            w.writerow([
                r['material'],
                f"{r['total_quantity']:.4f}",
                r['unit'],
                f"{r['total_usd']:.2f}",
                f"{r['total_pyg']:.0f}",
            ])
        w.writerow([])
        # Section 3: grand total
        w.writerow(['GRAND_TOTAL', '', '', f'{total_usd:.2f}', f'{total_pyg:.0f}'])


def _fmt_usd(v: float) -> str:
    return f'${v:,.2f}'


def _fmt_pyg(v: float) -> str:
    return f'Gs. {v:,.0f}'


def write_markdown(lines: list[BoQLine], out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    today = _dt.date.today().isoformat()
    rollup = per_material_rollup(lines)
    total_usd = grand_total_usd(lines)
    total_pyg = total_usd * USD_TO_PYG

    parts: list[str] = []
    parts.append('# La Quebrada Viva — Bill of Quantities')
    parts.append('')
    parts.append(f'Generated: **{today}**')
    parts.append('')
    parts.append(f'USD -> PYG rate: **{USD_TO_PYG:,.0f} PYG / USD**')
    parts.append('')
    parts.append('Auto-generated from `MATERIAL_TAKEOFF` dicts across every '
                 '`lqv.typologies.*` and `lqv.amenities.*` module. Material '
                 'names are preserved verbatim across modules (no '
                 'canonicalisation); same-name materials are summed.')
    parts.append('')

    # --- Per-module breakdown ---
    parts.append('## Per-module breakdown')
    parts.append('')
    # Group lines by module. Sorted alphabetically so the diff between
    # successive BoQ runs is stable — discovery order depends on
    # ``pkgutil.iter_modules`` which is not guaranteed across Python /
    # filesystem versions, so an unsorted dict made every run look like
    # a "BoQ reshuffled" diff in git review.
    by_module: dict[str, list[BoQLine]] = {}
    for line in lines:
        by_module.setdefault(line.module, []).append(line)
    for module in sorted(by_module.keys()):
        mod_lines = by_module[module]
        mod_subtotal = sum(l.subtotal_usd for l in mod_lines)
        parts.append(f'### `{module}` — {_fmt_usd(mod_subtotal)}')
        parts.append('')
        parts.append('| material | quantity | unit | $/unit | subtotal USD | subtotal PYG |')
        parts.append('|---|---:|---|---:|---:|---:|')
        for line in mod_lines:
            parts.append(
                f'| {line.material} | {line.quantity:,.3f} | {line.unit} | '
                f'{_fmt_usd(line.unit_cost_usd)} | '
                f'{_fmt_usd(line.subtotal_usd)} | {_fmt_pyg(line.subtotal_pyg)} |'
            )
        parts.append('')

    # --- Per-material rollup ---
    parts.append('## Per-material rollup')
    parts.append('')
    parts.append('Sorted by total USD descending. Materials used with more '
                 'than one unit appear as one row per unit (e.g. adobe_brick '
                 'in `count` and in `m3`) so every row remains summable and '
                 'orderable; USD aggregates are unchanged.')
    parts.append('')
    parts.append('| material | total quantity | unit | total USD | total PYG |')
    parts.append('|---|---:|---|---:|---:|')
    for r in rollup:
        parts.append(
            f"| {r['material']} | {r['total_quantity']:,.3f} | {r['unit']} | "
            f"{_fmt_usd(r['total_usd'])} | {_fmt_pyg(r['total_pyg'])} |"
        )
    parts.append('')

    # --- Grand total ---
    parts.append('## Grand total')
    parts.append('')
    parts.append(f'**{_fmt_usd(total_usd)}**  ·  **{_fmt_pyg(total_pyg)}**  '
                 f'@ {USD_TO_PYG:,.0f} PYG/USD')
    parts.append('')

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts))


def write_pdf(md_path: str, pdf_path: str, lines: list[BoQLine]) -> str:
    """Write PDF. Returns the renderer used: 'pandoc' or 'reportlab'.

    Tries pandoc first if available; on failure (likely missing LaTeX engine)
    falls back to a minimal reportlab report containing the per-material
    rollup + grand total only.
    """
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    pandoc = shutil.which('pandoc')
    if pandoc:
        try:
            proc = subprocess.run(
                [pandoc, md_path, '-o', pdf_path],
                capture_output=True, text=True, timeout=120,
            )
            if proc.returncode == 0 and _is_pdf_file(pdf_path):
                return 'pandoc'
            # Either pandoc said it succeeded but wrote a non-PDF (happens
            # when the missing LaTeX engine silently produces an empty or
            # HTML-tagged file), or it failed outright. Either way: log,
            # remove the bogus artefact so reportlab's writer doesn't see
            # stale half-output, and fall through.
            print(f'[boq] pandoc rc={proc.returncode} or non-PDF output; '
                  f'falling back to reportlab', file=sys.stderr)
            if proc.stderr:
                print(f'[boq] pandoc stderr: {proc.stderr.strip()[:400]}',
                      file=sys.stderr)
            if os.path.exists(pdf_path):
                try:
                    os.remove(pdf_path)
                except OSError as rm_err:
                    print(f'[boq] WARN could not remove stale pdf '
                          f'{pdf_path}: {rm_err}', file=sys.stderr)
        except (subprocess.TimeoutExpired, OSError) as e:
            print(f'[boq] pandoc failed: {e}; falling back to reportlab',
                  file=sys.stderr)

    _write_pdf_reportlab(pdf_path, lines)
    if not _is_pdf_file(pdf_path):
        raise RuntimeError(
            f'reportlab wrote {pdf_path} but it does not start with %PDF- '
            f'magic bytes; refusing to ship a corrupt PDF.'
        )
    return 'reportlab'


def _is_pdf_file(path: str) -> bool:
    """Magic-byte check: a real PDF starts with ``%PDF-``.

    Pandoc with no LaTeX engine produces empty/HTML output but still
    exit-zeros on some distros, and the prior check (``getsize > 0``)
    happily shipped those. Anyone downstream — investor deck, escritura
    appendix, BCP submission — gets a "the file is corrupted" surprise
    only after rendering or sending. Catch it here.
    """
    try:
        if not os.path.exists(path) or os.path.getsize(path) < 5:
            return False
        with open(path, 'rb') as f:
            head = f.read(5)
        return head == b'%PDF-'
    except OSError:
        return False


def _write_pdf_reportlab(pdf_path: str, lines: list[BoQLine]) -> None:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import (
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    today = _dt.date.today().isoformat()
    rollup = per_material_rollup(lines)
    total_usd = grand_total_usd(lines)
    total_pyg = total_usd * USD_TO_PYG

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(
        pdf_path, pagesize=letter,
        leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36,
    )
    story = [
        Paragraph('La Quebrada Viva — Bill of Quantities', styles['Title']),
        Paragraph(f'Generated: <b>{today}</b>', styles['Normal']),
        Paragraph(f'USD &rarr; PYG rate: <b>{USD_TO_PYG:,.0f} PYG / USD</b>',
                  styles['Normal']),
        Spacer(1, 8),
        Paragraph(
            'Per-module breakdown is in the companion Markdown file; '
            'this PDF carries the per-material rollup and grand total only.',
            styles['Italic'],
        ),
        Spacer(1, 10),
        Paragraph('Per-material rollup', styles['Heading2']),
    ]

    header = ['material', 'total qty', 'unit', 'total USD', 'total PYG']
    data = [header]
    for r in rollup:
        data.append([
            r['material'],
            f"{r['total_quantity']:,.2f}",
            r['unit'],
            _fmt_usd(r['total_usd']),
            _fmt_pyg(r['total_pyg']),
        ])
    table = Table(data, repeatRows=1, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ece6d6')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('ALIGN', (3, 1), (4, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        f'<b>Grand total: {_fmt_usd(total_usd)}  &middot;  '
        f'{_fmt_pyg(total_pyg)}</b>',
        styles['Heading3'],
    ))
    doc.build(story)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main(out_dir: str = 'docs/boq') -> dict:
    """Collect, write CSV + MD + PDF, return a summary dict."""
    _install_stubs_if_needed()
    # Re-read FX in case the JSON moved since module import (long-running
    # daemons, tests). The module-level USD_TO_PYG constant is rebound here
    # so all downstream writers see the same value.
    from lqv import finance as _finance
    _finance.reset_cache()
    global USD_TO_PYG
    USD_TO_PYG = _finance.get_usd_to_pyg()
    lines = collect_all(skip_broken=True)
    csv_path = os.path.join(out_dir, 'boq_rollup.csv')
    md_path = os.path.join(out_dir, 'boq_rollup.md')
    pdf_path = os.path.join(out_dir, 'boq_rollup.pdf')
    write_csv(lines, csv_path)
    write_markdown(lines, md_path)
    pdf_engine = write_pdf(md_path, pdf_path, lines)

    rollup = per_material_rollup(lines)
    total_usd = grand_total_usd(lines)
    modules_seen = {l.module for l in lines}
    return {
        'lines_count': len(lines),
        'assets_count': len(modules_seen),
        'modules_count': len(modules_seen),
        'materials_count': len(rollup),
        'total_usd': total_usd,
        'total_pyg': total_usd * USD_TO_PYG,
        'csv': csv_path,
        'md': md_path,
        'pdf': pdf_path,
        'pdf_engine': pdf_engine,
    }


if __name__ == '__main__':
    # Make project root importable when run as `python lqv/boq.py`
    _here = os.path.dirname(os.path.abspath(__file__))
    _root = os.path.dirname(_here)
    if _root not in sys.path:
        sys.path.insert(0, _root)
    out_dir = os.path.join(_root, 'docs', 'boq')
    result = main(out_dir=out_dir)
    print(
        f"[boq] wrote {os.path.relpath(result['csv'], _root)} "
        f"({result['materials_count']} materials, "
        f"{result['modules_count']} modules, "
        f"${result['total_usd'] / 1000:,.2f}k USD total, "
        f"PDF via {result['pdf_engine']})"
    )
    raise SystemExit(0)
