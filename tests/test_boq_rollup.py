"""BoQ per-material rollup invariants.

Guards against the regression that motivated [[boq.py#per_material_rollup]]:
earlier versions keyed the rollup on ``material`` alone, so when the same
material appeared with two different units (e.g. ``adobe_brick`` as
``count`` in one typology and as ``m3`` in another) both rows collapsed
into a single ``unit='mixed', total_quantity=0.0`` row. The USD aggregate
was still right, but procurement had a zero-quantity row and no way to
order. The fix splits rows per ``(material, unit)``.
"""
from __future__ import annotations

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _ensure_stubs() -> None:
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)
    from lqv import boq
    boq._install_stubs_if_needed()


def test_no_mixed_zero_qty_row():
    _ensure_stubs()
    from lqv.boq import BoQLine, per_material_rollup

    lines = [
        BoQLine(module='casita', material='adobe_brick', quantity=4200,
                unit='count', unit_cost_usd=0.35,
                subtotal_usd=1470.0, subtotal_pyg=1470.0 * 7300),
        BoQLine(module='trombe_wall', material='adobe_brick', quantity=3.2,
                unit='m3', unit_cost_usd=110.0,
                subtotal_usd=352.0, subtotal_pyg=352.0 * 7300),
    ]

    rows = per_material_rollup(lines)

    by_unit = {r['unit']: r for r in rows if r['material'] == 'adobe_brick'}
    assert 'count' in by_unit and 'm3' in by_unit, (
        f"expected adobe_brick rows for both 'count' and 'm3' units, got {list(by_unit)}"
    )
    assert by_unit['count']['total_quantity'] == 4200
    assert by_unit['m3']['total_quantity'] == 3.2
    assert all(r['unit'] != 'mixed' for r in rows), (
        f"no row should land in the legacy 'mixed' bucket; rows={rows}"
    )
    assert all(r['total_quantity'] > 0 for r in rows), (
        f"no row should have zero quantity; rows={rows}"
    )


def test_rollup_deterministic_usd_desc():
    _ensure_stubs()
    from lqv.boq import BoQLine, per_material_rollup

    lines = [
        BoQLine(module='a', material='wood_beam', quantity=10, unit='m',
                unit_cost_usd=5.0, subtotal_usd=50.0, subtotal_pyg=50.0 * 7300),
        BoQLine(module='b', material='adobe_brick', quantity=1000, unit='count',
                unit_cost_usd=0.35, subtotal_usd=350.0, subtotal_pyg=350.0 * 7300),
        BoQLine(module='c', material='cob_mix', quantity=2.0, unit='m3',
                unit_cost_usd=80.0, subtotal_usd=160.0, subtotal_pyg=160.0 * 7300),
    ]

    rows = per_material_rollup(lines)
    usd_in_order = [r['total_usd'] for r in rows]
    assert usd_in_order == sorted(usd_in_order, reverse=True), (
        f"rows must sort by total_usd descending; got {usd_in_order}"
    )
