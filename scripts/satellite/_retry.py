"""Retry + skip-if-exists helpers for long-running fetchers.

CHIRPS daily windows can be 365+ items; NICFI tile pulls can be 1000s of
tiles. We need exponential backoff on transient HTTP failures plus a
hard skip-if-exists guard so a partial run can resume without re-fetching.

Uses tenacity if available; falls back to a tiny built-in loop if not.
"""
from __future__ import annotations

import socket
import time
from collections.abc import Callable
from functools import wraps
from pathlib import Path
from typing import TypeVar

T = TypeVar("T")

DEFAULT_ATTEMPTS = 4
DEFAULT_BASE_DELAY = 1.5  # seconds

# A valid Cloud-Optimized GeoTIFF header alone is several KB; a single
# NICFI PNG tile with real content is ~10–40 KB. Anything under 8 KB is
# almost always a truncated download, an HTML error page, or an empty
# placeholder created mid-write. Skip-if-exists must reject these so a
# re-run can heal the corruption instead of silently inheriting it.
MIN_VALID_BYTES = 8192


def _retryable_exception_types() -> tuple[type[BaseException], ...]:
    """Transport-layer errors worth retrying — not bugs in our own code.

    AttributeError / KeyError / ValueError / TypeError from a misshapen
    response or bad call site should fail fast, not be hidden behind
    four exponential backoffs.
    """
    types: list[type[BaseException]] = [
        TimeoutError, ConnectionError, OSError,
        socket.timeout, socket.gaierror,
    ]
    try:
        import requests
        types.extend([
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.ChunkedEncodingError,
        ])
    except ImportError:
        pass
    try:
        import urllib3
        types.append(urllib3.exceptions.HTTPError)
    except ImportError:
        pass
    return tuple(types)


def with_retry(
    attempts: int = DEFAULT_ATTEMPTS,
    base_delay: float = DEFAULT_BASE_DELAY,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Exponential-backoff retry decorator.

    Retries only on transient transport errors (timeouts, connection
    drops, HTTP errors). Programmer errors (AttributeError, KeyError,
    TypeError, ValueError, etc.) propagate immediately so bugs surface
    on the first call instead of after a 60-second backoff loop.
    """
    retryable = _retryable_exception_types()

    try:
        from tenacity import (
            retry,
            retry_if_exception_type,
            stop_after_attempt,
            wait_exponential,
        )

        return retry(
            reraise=True,
            stop=stop_after_attempt(attempts),
            wait=wait_exponential(multiplier=base_delay, min=base_delay, max=60),
            retry=retry_if_exception_type(retryable),
        )
    except ImportError:
        pass

    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        @wraps(fn)
        def wrapper(*args, **kwargs) -> T:
            for attempt in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except retryable:
                    if attempt == attempts - 1:
                        raise
                    time.sleep(base_delay * (2 ** attempt))
            raise RuntimeError("with_retry: exhausted attempts without return or raise")

        return wrapper

    return decorator


def skip_if_exists(out: Path, min_bytes: int = MIN_VALID_BYTES) -> bool:
    """Return True if ``out`` exists with at least ``min_bytes`` bytes.

    Use as an early-skip guard at the top of per-item loops. The default
    floor of ``MIN_VALID_BYTES`` (8 KB) rejects truncated downloads and
    HTML error pages masquerading as raster assets.
    """
    return out.exists() and out.stat().st_size >= min_bytes
