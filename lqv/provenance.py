"""Render provenance capture — embed git SHA, RNG seed, and LQV env vars
into the PNG itself so any image on disk is reproducible from disk.

The output PNG is 16-bit RGBA (see ``engine.setup_render_output``). Pillow's
re-encoding path would force an 8-bit round-trip and lose colour fidelity,
so we inject raw PNG ``tEXt`` chunks immediately before ``IEND``. Format
follows the PNG 1.2 spec §4.2.3.3: keyword (Latin-1, <=79 bytes) + NUL +
text (Latin-1). A sidecar ``<name>.json`` next to the PNG carries the same
data in machine-readable form for grep / catalogue scripts that don't want
to parse PNG chunks.

Read back with :func:`read_from_png` or via ``python3 -m lqv.provenance
<path>``. The CLI returns non-zero if the file lacks an ``lqv:git_sha``
chunk, which lets ``make audit`` reject finals shipped without provenance.
"""
from __future__ import annotations

import json
import os
import struct
import subprocess
import sys
import zlib
from typing import Any

from lqv import config

# tEXt keywords are namespaced with ``lqv:`` so a third-party tool dumping
# the PNG (Blender's image properties, ImageMagick `identify -verbose`) can
# tell our metadata from anything stock Blender writes.
_KEY_PREFIX = 'lqv:'

# These env vars steer render behaviour and belong in the trace alongside
# the git SHA. Anything else (PATH, HOME) is noise; keep this list tight.
_TRACKED_ENV: tuple[str, ...] = (
    'RENDER_RUN_ID',
    'RENDER_RES',
    'RENDER_VARIANT',
    'RENDER_VIEW',
    'RENDER_SKIP',
    'LQV_ALLOW_CPU_FALLBACK',
    'LQV_ALLOW_TIMESTAMP_RUN_ID',
    'LQV_BOQ_SCOPE',
    'LQV_SMOKE_SUBSCENE_SAMPLE',
)


def _git_sha() -> str:
    """Short SHA of HEAD, or ``'unknown'`` if we're not in a git repo /
    git binary missing. Trailing ``-dirty`` if the worktree has uncommitted
    edits — keeps the trace honest about ``"this was rendered from a WIP
    tree"`` vs ``"this is a tagged-commit render"``."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        sha = subprocess.check_output(
            ['git', '-C', repo_root, 'rev-parse', '--short=12', 'HEAD'],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        dirty = subprocess.call(
            ['git', '-C', repo_root, 'diff', '--quiet', '--ignore-submodules', 'HEAD'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        return f"{sha}-dirty" if dirty != 0 else sha
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return 'unknown'


def collect(asset: str, variant: str, view: str, seed: int,
            extra: dict[str, Any] | None = None) -> dict[str, str]:
    """Build the metadata dict for one render. All values stringified so
    the same dict can be dropped straight into PNG tEXt chunks and JSON."""
    data: dict[str, str] = {
        'asset': asset,
        'variant': variant,
        'view': view,
        'seed': str(seed),
        'config_seed': str(config.SEED),
        'git_sha': _git_sha(),
    }
    for key in _TRACKED_ENV:
        val = os.environ.get(key)
        if val is not None:
            data[f'env.{key}'] = val
    if extra:
        for k, v in extra.items():
            data[k] = str(v)
    return data


def _chunk(kind: bytes, payload: bytes) -> bytes:
    """Assemble a PNG chunk: [len:4 BE][type:4][data:N][crc:4]. CRC covers
    type+data per PNG spec §3.2."""
    length = struct.pack('>I', len(payload))
    crc = struct.pack('>I', zlib.crc32(kind + payload) & 0xFFFFFFFF)
    return length + kind + payload + crc


def _text_chunk(keyword: str, text: str) -> bytes:
    """tEXt chunk. Keyword + NUL + text, both Latin-1. Non-Latin-1 chars
    get replaced rather than raising — provenance should never break a
    render save."""
    kw = keyword.encode('latin-1', errors='replace')[:79]
    txt = str(text).encode('latin-1', errors='replace')
    return _chunk(b'tEXt', kw + b'\x00' + txt)


def inject_into_png(png_path: str, data: dict[str, str]) -> None:
    """Insert ``lqv:<key>`` tEXt chunks immediately before IEND.

    No re-encode, so 16-bit PNGs stay 16-bit. Silently no-ops if the file
    isn't a PNG (defensive — a future driver might switch formats and we
    don't want it to crash mid-batch)."""
    with open(png_path, 'rb') as fh:
        blob = fh.read()
    if not blob.startswith(b'\x89PNG\r\n\x1a\n'):
        print(f'[provenance] {png_path} not a PNG, skipping injection',
              file=sys.stderr)
        return
    # IEND is the last chunk: [0x00 0x00 0x00 0x00][IEND][CRC]. The
    # 4-byte length is always 0 so the literal byte sequence below is
    # unambiguous and safer than scanning for the bare 'IEND' tag.
    iend_marker = b'\x00\x00\x00\x00IEND\xaeB`\x82'
    idx = blob.rfind(iend_marker)
    if idx < 0:
        print(f'[provenance] {png_path} missing IEND, skipping injection',
              file=sys.stderr)
        return
    inserted = b''.join(_text_chunk(_KEY_PREFIX + k, v) for k, v in data.items())
    with open(png_path, 'wb') as fh:
        fh.write(blob[:idx] + inserted + blob[idx:])


def write_sidecar(png_path: str, data: dict[str, str]) -> str:
    """Write ``<png_path stem>.json`` next to the PNG. Returns the path.
    Catalogue scripts that already walk renders/ for PNGs can grep these
    without parsing chunks."""
    sidecar = os.path.splitext(png_path)[0] + '.json'
    with open(sidecar, 'w') as fh:
        json.dump(data, fh, indent=2, sort_keys=True)
    return sidecar


def read_from_png(png_path: str) -> dict[str, str]:
    """Extract every ``lqv:`` tEXt chunk. Returns ``{}`` if the file has
    no LQV provenance (e.g. a render from before CC-TOOL.8 shipped)."""
    with open(png_path, 'rb') as fh:
        blob = fh.read()
    if not blob.startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError(f'{png_path} is not a PNG')
    out: dict[str, str] = {}
    pos = 8  # skip signature
    while pos + 8 <= len(blob):
        length = struct.unpack('>I', blob[pos:pos + 4])[0]
        kind = blob[pos + 4:pos + 8]
        data = blob[pos + 8:pos + 8 + length]
        pos += 8 + length + 4  # +4 for CRC
        if kind == b'IEND':
            break
        if kind != b'tEXt':
            continue
        nul = data.find(b'\x00')
        if nul < 0:
            continue
        keyword = data[:nul].decode('latin-1', errors='replace')
        text = data[nul + 1:].decode('latin-1', errors='replace')
        if keyword.startswith(_KEY_PREFIX):
            out[keyword[len(_KEY_PREFIX):]] = text
    return out


def _cli(argv: list[str]) -> int:
    if not argv or argv[0] in ('-h', '--help'):
        print('usage: python3 -m lqv.provenance <png> [<png> ...]')
        return 0
    rc = 0
    for path in argv:
        try:
            data = read_from_png(path)
        except (OSError, ValueError) as exc:
            print(f'{path}: error: {exc}', file=sys.stderr)
            rc = 2
            continue
        if not data:
            print(f'{path}: no lqv provenance found', file=sys.stderr)
            rc = 1
            continue
        print(f'=== {path}')
        for k in sorted(data):
            print(f'  {k}: {data[k]}')
    return rc


if __name__ == '__main__':
    sys.exit(_cli(sys.argv[1:]))
