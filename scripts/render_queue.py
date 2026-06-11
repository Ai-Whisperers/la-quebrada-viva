#!/usr/bin/env python3
"""Read STATUS.md manifest and print only the ☐ (not-yet-rendered) entries.

Useful for partial-batch restart after a render crash or SIGKILL: pipe the
output into a shell loop instead of re-running `scripts/render_all_finals.sh`
(which would re-render the ☑ files that are already on disk).

    $ python3 scripts/render_queue.py
    C hero
    C stream_up
    ...

    $ python3 scripts/render_queue.py | while read v c; do
          scripts/render_final.sh "$v" "$c"
      done

Pure stdlib. Read-only. No side effects on scene.blend or renders/.
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUS = os.path.join(ROOT, 'STATUS.md')

ROW_RE = re.compile(r'^\|\s*([ABC])\s+([a-z_]+)\s*\|\s*`renders/[^`]+`\s*\|\s*(☑|☐)')


def main() -> int:
    if not os.path.isfile(STATUS):
        print(f"STATUS.md not found at {STATUS}", file=sys.stderr)
        return 2
    queued = 0
    with open(STATUS, encoding='utf-8') as fh:
        for line in fh:
            m = ROW_RE.match(line)
            if m and m.group(3) == '☐':
                print(f"{m.group(1)} {m.group(2)}")
                queued += 1
    print(f"# {queued} pending", file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
