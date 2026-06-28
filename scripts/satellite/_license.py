"""License gate for the satellite fetchers.

Single source of truth for which licenses may end up in the redistribution
bundle. Mirrors the policy in ``LICENSE_BUNDLE.md``:

  - CC0-1.0 and CC-BY-4.0 are bundle-eligible.
  - CC-BY-NC (e.g. Planet NICFI) is deck-only — every sidecar gets
    ``deck_only=true`` and the bundle manifest excludes it.
  - CC-BY-SA is BLOCKED outright — its share-alike viral clause would
    force the deck to be re-licensed.

All fetchers call ``assert_compatible(license_id)`` before writing the
sidecar so banned licenses fail loudly at fetch time, not at bundle time.
"""
from __future__ import annotations

ALLOWED_IN_BUNDLE: frozenset[str] = frozenset({
    "CC0-1.0",
    "CC-BY-4.0",
    "public-domain",
    "USGS-PD",
    "NASA-PD",
})

DECK_ONLY: frozenset[str] = frozenset({
    "CC-BY-NC-4.0",
    "CC-BY-NC-2.0",
    "Planet-NICFI-Non-Commercial",
})

BLOCKED: frozenset[str] = frozenset({
    "CC-BY-SA-4.0",
    "CC-BY-SA-3.0",
    "CC-BY-NC-SA-4.0",
    "GPL-3.0",
    "AGPL-3.0",
})


class LicenseBlocked(RuntimeError):
    """Raised when a fetcher tries to write data under a blocked license."""


def classify(license_id: str) -> str:
    """Return one of: 'bundle', 'deck_only', 'blocked', 'unknown'."""
    if license_id in ALLOWED_IN_BUNDLE:
        return "bundle"
    if license_id in DECK_ONLY:
        return "deck_only"
    if license_id in BLOCKED:
        return "blocked"
    return "unknown"


def assert_compatible(license_id: str) -> str:
    """Raise on blocked licenses; return the classification otherwise.

    Unknown licenses warn but pass — fetchers should treat them as
    deck-only until reviewed.
    """
    cls = classify(license_id)
    if cls == "blocked":
        raise LicenseBlocked(
            f"License {license_id!r} is on the BLOCKED list; refusing to write. "
            f"See scripts.satellite._license.BLOCKED."
        )
    return cls
