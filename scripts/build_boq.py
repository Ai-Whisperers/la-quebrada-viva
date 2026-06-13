"""CLI entry — generate the Bill-of-Quantities rollup outside Blender.

Typology + amenity modules import ``bpy`` at module top, so direct import
outside Blender fails. We install a permissive ``bpy`` stub on ``sys.modules``
before any LQV module loads. ``MATERIAL_TAKEOFF`` is a module-level dict
literal that does not touch Blender APIs, so this is safe.

Run from project root:

    python3 scripts/build_boq.py
"""
from __future__ import annotations

import os
import sys
import types
from typing import Any, cast

# Make project importable when run as `python3 scripts/build_boq.py`
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)


class _PermissiveNS(types.ModuleType):
    """Stand-in module that returns more permissive namespaces for any attribute."""

    def __init__(self, name: str) -> None:
        super().__init__(name)

    def __getattr__(self, name: str):  # noqa: D401
        child = _PermissiveNS(f'{self.__name__}.{name}')
        setattr(self, name, child)
        return child

    def __call__(self, *a, **kw):
        return _PermissiveNS(self.__name__ + '()')


def _install_bpy_stub() -> None:
    if 'bpy' in sys.modules:
        return
    bpy = cast(Any, _PermissiveNS('bpy'))
    # The common attribute hooks
    bpy.context = _PermissiveNS('bpy.context')
    bpy.data = _PermissiveNS('bpy.data')
    bpy.ops = _PermissiveNS('bpy.ops')
    bpy.types = cast(Any, _PermissiveNS('bpy.types'))
    # types.Collection / types.Object referenced as type hints — make them classes
    bpy.types.Collection = type('Collection', (), {})
    bpy.types.Object = type('Object', (), {})
    bpy.types.Material = type('Material', (), {})
    bpy.types.Mesh = type('Mesh', (), {})
    bpy.types.Camera = type('Camera', (), {})
    bpy.types.Light = type('Light', (), {})
    bpy.types.Scene = type('Scene', (), {})
    sys.modules['bpy'] = bpy
    sys.modules['bpy.types'] = bpy.types
    sys.modules['bpy.context'] = bpy.context
    sys.modules['bpy.data'] = bpy.data
    sys.modules['bpy.ops'] = bpy.ops
    # mathutils sometimes imported as well
    mathutils = cast(Any, _PermissiveNS('mathutils'))
    mathutils.Vector = lambda *a, **kw: a
    mathutils.Matrix = lambda *a, **kw: None
    mathutils.Euler = lambda *a, **kw: a
    mathutils.Quaternion = lambda *a, **kw: a
    sys.modules['mathutils'] = mathutils
    # bmesh
    bmesh = _PermissiveNS('bmesh')
    sys.modules['bmesh'] = bmesh


def _install_materials_stub() -> None:
    """No-op: the real ``lqv.materials`` package is safe to import once bpy is
    stubbed (its top-level imports only *define* shader helpers; the bpy calls
    inside them aren't executed at import time). Stubbing it broke transitive
    ``from lqv.materials._shaders import principled`` imports in
    ``lqv.house.*``, which silently dropped 8/17 typology + amenity modules
    from the BoQ rollup. Left as a function for back-compat in case future code
    needs to install a different stub.
    """
    return


def main() -> int:
    _install_bpy_stub()
    _install_materials_stub()

    from lqv import boq  # noqa: WPS433 — deferred until stubs installed

    # Write to docs/boq under project root
    out_dir = os.path.join(_ROOT, 'docs', 'boq')
    result = boq.main(out_dir=out_dir)

    print('=' * 64)
    print(f"Lines:    {result['lines_count']}")
    print(f"Assets:   {result['assets_count']}")
    print(f"Total:    ${result['total_usd']:,.2f} USD  "
          f"·  Gs. {result['total_pyg']:,.0f}")
    print(f"CSV:      {result['csv']}")
    print(f"Markdown: {result['md']}")
    print('=' * 64)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
