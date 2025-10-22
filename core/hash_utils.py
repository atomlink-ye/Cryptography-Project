"""Toy hash helpers."""
from __future__ import annotations

import hashlib

from .common import truncate_digest


DEFAULT_HASH_BITS = 20


def toy_hash(message: bytes, bits: int = DEFAULT_HASH_BITS) -> int:
    """Return ``bits``-bit toy hash using SHA-256 truncation.

    The function remains intentionally lightweight but deterministic so that
    visualizations can run in real time while still reflecting cryptographic
    dynamics.
    """

    digest = hashlib.sha256(message).digest()
    return truncate_digest(digest, bits)


__all__ = [
    "DEFAULT_HASH_BITS",
    "toy_hash",
]
