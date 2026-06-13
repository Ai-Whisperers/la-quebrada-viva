"""Typology-package contract — every name in :data:`TYPOLOGIES` is importable.

The :data:`lqv.typologies.TYPOLOGIES` tuple is a public manifest of buildable
typologies (per ``docs/TERRAIN_PIVOT.md`` §3). The contract is that every
entry must resolve as a real ``lqv.typologies.<name>`` module — otherwise
downstream tools (BoQ rollup, escritura deck, render queue) silently skip
the entry and the manifest lies about what's shippable.

This test catches drift between the manifest and the actual package layout.
It avoids importing typology modules that would fail outside Blender by
stubbing ``bpy`` first (the existing boq stub installer is reused).
"""
from __future__ import annotations

import importlib
import importlib.util
import os
import sys


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _ensure_stubs() -> None:
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)
    # Reuse the boq.py permissive bpy stub installer so we can import
    # typology modules outside Blender.
    from lqv import boq
    boq._install_stubs_if_needed()


def test_every_typology_has_a_module():
    _ensure_stubs()
    from lqv.typologies import TYPOLOGIES

    missing: list[str] = []
    for name in TYPOLOGIES:
        spec = importlib.util.find_spec(f"lqv.typologies.{name}")
        if spec is None:
            missing.append(name)
    assert not missing, (
        f"TYPOLOGIES entries with no matching module under "
        f"lqv/typologies/: {missing}. Either remove the entry or add the "
        f"module."
    )


def test_every_typology_imports_cleanly():
    _ensure_stubs()
    from lqv.typologies import TYPOLOGIES

    failures: list[tuple[str, str]] = []
    for name in TYPOLOGIES:
        try:
            importlib.import_module(f"lqv.typologies.{name}")
        except Exception as e:  # noqa: BLE001 — report-and-aggregate
            failures.append((name, f"{type(e).__name__}: {e}"))
    assert not failures, (
        "TYPOLOGIES entries that fail to import: "
        + ", ".join(f"{n} ({err})" for n, err in failures)
    )


def test_cob_bottle_lqv_intentionally_absent():
    """LQV reference is a subscene driver, not a buildable typology stub.

    Guards against accidental re-addition during refactors. If the cob/
    bottle reference is ever promoted to a buildable typology, delete
    this test and add 'cob_bottle_lqv' to TYPOLOGIES.
    """
    from lqv.typologies import TYPOLOGIES
    assert 'cob_bottle_lqv' not in TYPOLOGIES, (
        "cob_bottle_lqv must not appear in TYPOLOGIES — it ships from "
        "build_scene.py + lqv/subscene/cob_bottle_lqv.py, not as a "
        "typology stub."
    )


def test_typologies_count_matches_doc_pivot():
    """TERRAIN_PIVOT.md §3 enumerates exactly 13 buildable typologies."""
    from lqv.typologies import TYPOLOGIES
    assert len(TYPOLOGIES) == 13, (
        f"TYPOLOGIES length drifted from doc TERRAIN_PIVOT.md §3 (13). "
        f"Current: {len(TYPOLOGIES)}. If this is intentional, update the "
        f"doc + this test together."
    )
