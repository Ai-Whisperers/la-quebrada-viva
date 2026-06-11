"""RNG-seed-ordering audit (Code Invariant #1, CLAUDE.md §82).

The build pipeline must call ``random.seed()`` AFTER
``materials.build_materials()`` and BEFORE the first ``build_*`` geometry call.
Reordering silently changes which `random.*` draws each builder sees, which
shifts every scattered prop — fireflies, petal carpet, flora positions — by
a deterministic but invisible amount that ruins reproducibility.

This audit parses ``build_scene.py`` statically (no Blender imports) and
flags violations.  Run with:

    python3 -m lqv.util.random_audit          # exits non-zero on violation
    python3 -m lqv.util.random_audit --json   # machine-readable
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import sys
from typing import List, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DRIVER = os.path.join(ROOT, 'build_scene.py')


def _collect_calls(tree: ast.AST) -> List[Tuple[int, str]]:
    """Return [(lineno, fullname), ...] for every function-call expression."""
    out: List[Tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            parts: List[str] = []
            while isinstance(fn, ast.Attribute):
                parts.insert(0, fn.attr)
                fn = fn.value
            if isinstance(fn, ast.Name):
                parts.insert(0, fn.id)
            if parts:
                out.append((node.lineno, '.'.join(parts)))
    return out


def audit(path: str = DRIVER) -> dict:
    with open(path, encoding='utf-8') as fh:
        tree = ast.parse(fh.read(), filename=path)
    calls = _collect_calls(tree)

    seed_line = next((ln for ln, n in calls if n.endswith('random.seed') or n == 'seed'), None)
    materials_line = next((ln for ln, n in calls if 'build_materials' in n), None)
    build_lines = [(ln, n) for ln, n in calls if n.startswith('build_') and 'build_materials' not in n]
    random_use_lines = [(ln, n) for ln, n in calls if n.startswith('random.') and not n.endswith('seed')]

    violations: List[str] = []
    if seed_line is None:
        violations.append('no random.seed() call found in build_scene.py')
    if materials_line is None:
        violations.append('no build_materials() call found in build_scene.py')
    if seed_line and materials_line and seed_line < materials_line:
        violations.append(
            f'random.seed() at line {seed_line} runs BEFORE build_materials() at line {materials_line}'
        )
    if seed_line and build_lines:
        first_build_ln = min(ln for ln, _ in build_lines)
        if seed_line > first_build_ln:
            violations.append(
                f'random.seed() at line {seed_line} runs AFTER first build_* at line {first_build_ln}'
            )
    for ln, n in random_use_lines:
        if seed_line and ln < seed_line:
            violations.append(f'random.* call ({n}) at line {ln} runs BEFORE seed at line {seed_line}')

    return {
        'seed_line': seed_line,
        'materials_line': materials_line,
        'first_build_line': min((ln for ln, _ in build_lines), default=None),
        'violations': violations,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--json', action='store_true')
    args = p.parse_args()
    result = audit()
    if args.json:
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write('\n')
    else:
        print(f"seed_line={result['seed_line']}  "
              f"materials_line={result['materials_line']}  "
              f"first_build_line={result['first_build_line']}")
        for v in result['violations']:
            print(f"  VIOLATION: {v}")
        if not result['violations']:
            print("  OK")
    return 2 if result['violations'] else 0


if __name__ == '__main__':
    sys.exit(main())
