"""Single source of truth for the USD->PYG exchange rate.

Historically the rate was a magic constant ``7300.0`` baked into
:mod:`lqv.boq`. As the BoQ output became the input to the escritura PDF +
investor deck the constant grew copies in three other modules, and the
day BCP moves the rate someone has to grep the repo, miss one, and ship
a doc with mismatched totals. This module collapses the trail of tears
to one JSON file (``docs/finance/fx.json``) and one accessor.

The accessor is cached per-process so writers (BoQ, escritura, deck)
share the same rate within a single run. To force a reload — e.g. a
test mutating ``docs/finance/fx.json`` between cases — call
:func:`reset_cache`.
"""
from __future__ import annotations

import json
import os
from typing import Optional

# Repo root = three levels up from this file (lqv/finance/__init__.py).
_PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
FX_JSON_PATH = os.path.join(_PROJECT_ROOT, 'docs', 'finance', 'fx.json')

# Last-ditch fallback if the JSON file is missing/corrupt — same rate the
# repo carried as a magic constant for months, so downstream output stays
# numerically stable even on a botched checkout.
FALLBACK_USD_PYG = 7300.0

_cache: Optional[dict] = None


def _load() -> dict:
    global _cache
    if _cache is not None:
        return _cache
    try:
        with open(FX_JSON_PATH, encoding='utf-8') as f:
            data = json.load(f)
        if 'USD_PYG' not in data:
            raise ValueError(f'fx.json missing USD_PYG key, got {sorted(data)}')
        # Coerce + sanity-bound — PYG/USD historically lives 5000–10000.
        rate = float(data['USD_PYG'])
        if rate < 1000.0 or rate > 20000.0:
            raise ValueError(
                f'fx.json USD_PYG={rate} is outside sane range 1000..20000; '
                f'refusing to use a corrupt rate.'
            )
        data['USD_PYG'] = rate
        _cache = data
    except (OSError, ValueError, json.JSONDecodeError) as e:
        import sys
        print(
            f'[lqv.finance] WARN failed to read {FX_JSON_PATH}: '
            f'{type(e).__name__}: {e}; using fallback USD_PYG={FALLBACK_USD_PYG}',
            file=sys.stderr,
        )
        _cache = {
            'USD_PYG': FALLBACK_USD_PYG,
            'as_of': 'fallback',
            'source': f'fallback (fx.json unreadable: {e})',
        }
    return _cache


def get_usd_to_pyg() -> float:
    """Return the current USD->PYG conversion factor."""
    return float(_load()['USD_PYG'])


def get_fx_metadata() -> dict:
    """Return a copy of the FX record (rate + as_of + source + notes)."""
    return dict(_load())


def reset_cache() -> None:
    """Drop the in-process cache. Tests + long-running daemons may call this
    after editing ``docs/finance/fx.json`` to force a re-read.
    """
    global _cache
    _cache = None


__all__ = [
    'FX_JSON_PATH',
    'FALLBACK_USD_PYG',
    'get_usd_to_pyg',
    'get_fx_metadata',
    'reset_cache',
]
