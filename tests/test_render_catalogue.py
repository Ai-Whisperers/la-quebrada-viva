"""Catalogue sidecar invariants.

`scripts/build_render_catalogue.py` writes `docs/render_catalogue/catalogue.json`
as the machine-readable source of truth for the catalogue UI (INDEX.md,
per-asset pages, contact-sheet gallery). These tests guard the invariants the
downstream consumers rely on:

  1. `total_renders` matches the sum of per-asset record counts.
  2. `by_source` sums to `total_renders` (every record is attributed once).
  3. `generated_at` is a parseable ISO-8601 UTC timestamp.
  4. Top-level dict keys are sorted (so re-runs produce byte-identical diffs).

If any of these fail, the catalogue regenerator has drifted from its contract
and `make catalogue` will start churning git history or under-counting.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
CATALOGUE = REPO / "docs/render_catalogue/catalogue.json"


@pytest.fixture(scope="module")
def payload() -> dict:
    if not CATALOGUE.exists():
        pytest.skip(f"{CATALOGUE} not present — run `make catalogue` first")
    return json.loads(CATALOGUE.read_text())


def test_total_renders_matches_asset_sum(payload: dict) -> None:
    total = payload["total_renders"]
    asset_sum = sum(len(recs) for recs in payload["assets"].values())
    assert total == asset_sum, (
        f"total_renders={total} but per-asset records sum to {asset_sum}"
    )


def test_by_source_sums_to_total(payload: dict) -> None:
    total = payload["total_renders"]
    source_sum = sum(payload["by_source"].values())
    assert total == source_sum, (
        f"total_renders={total} but by_source sums to {source_sum}"
    )


def test_generated_at_is_iso8601(payload: dict) -> None:
    ts = payload["generated_at"]
    # Sidecar writes `...Z`; parse via Python's `fromisoformat` after the
    # standard `Z` → `+00:00` swap so this stays valid on Python <3.11.
    datetime.fromisoformat(ts.replace("Z", "+00:00"))


def test_assets_dict_keys_sorted(payload: dict) -> None:
    keys = list(payload["assets"].keys())
    assert keys == sorted(keys), "assets dict must be sorted for stable diffs"


def test_by_source_dict_keys_sorted(payload: dict) -> None:
    keys = list(payload["by_source"].keys())
    assert keys == sorted(keys), "by_source dict must be sorted for stable diffs"
