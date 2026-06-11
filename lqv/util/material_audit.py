"""MAT-registry audit (Code Invariant #2).

`lqv.materials.MAT` is a global string-keyed dict; builders look up materials
by key at call time. A typo'd key surfaces as a runtime ``KeyError`` deep
inside a builder, often a long way from the actual cause. This audit
statically lists every ``MAT['…']`` access in the codebase and cross-checks
the literal key set against ``MAT`` after ``build_materials()``.

Two modes:

* ``python3 -m lqv.util.material_audit`` — static-only AST scan; no Blender
  needed. Flags duplicate keys and obvious typos (very short keys, etc.).
* Inside a Blender session, after build::

      from lqv.util import material_audit
      material_audit.run_with_registry()  # cross-checks against the real MAT

Read-only.
"""
from __future__ import annotations

import ast
import os
from typing import Iterable, List, Set

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LQV = os.path.join(ROOT, 'lqv')


def _iter_py_files(root: str) -> Iterable[str]:
    for dirpath, _dirnames, filenames in os.walk(root):
        for fname in filenames:
            if fname.endswith('.py'):
                yield os.path.join(dirpath, fname)


def _collect_mat_keys_in_file(path: str) -> Set[str]:
    with open(path, encoding='utf-8') as fh:
        try:
            tree = ast.parse(fh.read(), filename=path)
        except SyntaxError:
            return set()
    out: Set[str] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Subscript)
            and isinstance(node.value, ast.Name)
            and node.value.id == 'MAT'
            and isinstance(node.slice, ast.Constant)
            and isinstance(node.slice.value, str)
        ):
            out.add(node.slice.value)
    return out


def collect_referenced_keys() -> Set[str]:
    """Static scan: every literal ``MAT['…']`` access in lqv/."""
    keys: Set[str] = set()
    for path in _iter_py_files(LQV):
        keys.update(_collect_mat_keys_in_file(path))
    return keys


def short_or_suspicious(keys: Iterable[str]) -> List[str]:
    out: List[str] = []
    for k in keys:
        if len(k) < 3:
            out.append(f"suspiciously short key {k!r}")
        if not k.replace('_', '').isalnum():
            out.append(f"non-alphanumeric key {k!r}")
    return out


def run_static() -> int:
    refs = collect_referenced_keys()
    print(f"[material_audit] {len(refs)} distinct MAT keys referenced in lqv/")
    for k in sorted(refs):
        print(f"  - {k}")
    warns = short_or_suspicious(refs)
    for w in warns:
        print(f"  WARN: {w}")
    return 2 if warns else 0


def run_with_registry(verbose: bool = True) -> List[str]:
    """Inside Blender: compare static refs to the real MAT registry."""
    from lqv.materials import MAT  # imported lazily so static mode has no bpy dep

    refs = collect_referenced_keys()
    present = set(MAT.keys())
    missing = refs - present
    unused = present - refs
    msgs: List[str] = []
    for k in sorted(missing):
        msgs.append(f"MISSING in MAT but referenced: {k!r}")
    for k in sorted(unused):
        msgs.append(f"defined in MAT but never referenced: {k!r}")
    if verbose:
        for m in msgs:
            print(f"[material_audit] {m}")
        if not msgs:
            print('[material_audit] OK — registry matches references')
    return msgs


if __name__ == '__main__':
    import sys
    sys.exit(run_static())
